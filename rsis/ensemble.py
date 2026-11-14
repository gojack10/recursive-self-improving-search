import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from .config import ATTEMPT_BUDGET
from .llm import Chat
from .referee import norm
from .searcher import attempt, check_candidates
from .telem import Telem, url_key

RECALL = ("For this attempt, first write down every item you can recall from memory that might qualify, then search "
          "for pages that list the answer set directly, and verify every recalled item before submitting.")
# Each question shape gets lenses that make sense for it: anchoring on "did NOT win Y" is not a list anyone publishes.
LENSES = {
    "intersection": [
        "For this attempt, anchor on condition X: enumerate everything that meets X, then verify Y for each candidate.",
        "For this attempt, anchor on condition Y: enumerate everything that meets Y, then verify X for each candidate.",
        RECALL],
    "triple": [
        "For this attempt, find the narrowest published list that already combines two of the conditions, "
        "then verify the remaining condition for each candidate.",
        "For this attempt, anchor on condition Y, then verify condition X (all of its parts) for each candidate.",
        RECALL],
    "negation": [
        "For this attempt, fetch the complete list for condition X and the complete list for the opposite of Y, "
        "then submit the X items that are absent from the second list. Read both lists in full before subtracting.",
        "For this attempt, enumerate X, then for each candidate look for an explicit statement that rules out Y "
        "(for example an awards list it does not appear on). Drop candidates where you cannot rule Y out.",
        RECALL],
    "sequence": [
        "For this attempt, anchor on the later step (Y), which is usually the rarer list, then verify the earlier step X.",
        "For this attempt, anchor on the earlier step (X), then verify that each candidate later did Y.",
        RECALL],
    "events": [
        "For this attempt, anchor on lists already sorted by the numeric or date condition ('deadliest ...', "
        "'largest ...', '... by year'), then verify the figure on each event's own page.",
        "For this attempt, enumerate events of type X from category and timeline pages, then verify Y for each.",
        RECALL],
}
VERIFY_BUDGET = 0.06


def ensemble_budget(n, budget=ATTEMPT_BUDGET):
    return n * budget + VERIFY_BUDGET


def frame(hunt):
    return hunt.get("frame") or ("events" if hunt.get("kind") == "events" else "intersection")


def lens(m, hunt, i):
    ls = LENSES.get(frame(hunt), LENSES["intersection"])
    return {**m, "id": f"{m['id']}+lens{i}", "instructions": m["instructions"] + "\n\n" + ls[i % len(ls)]}


def merge(logs):
    """Union of finds across searchers, keyed by normalized name, with how many searchers found each."""
    items = {}
    for log in logs:
        for f in log["finds"]:
            k = norm(str(f.get("name") or ""))
            if not k:
                continue
            it = items.setdefault(k, {"name": str(f["name"]), "urls": [], "votes": set()})
            if url_key(str(f.get("evidence_url") or "")) in {url_key(u) for u in log["url_providers"]}:
                it["urls"].append(f["evidence_url"])
            it["votes"].add(log["attempt_id"])
    return items


def safe_attempt(m, hunt, budget, role):
    """One failed searcher should not discard the other searchers' paid work."""
    try:
        return attempt(m, hunt, budget=budget, role=role)
    except Exception as e:
        print(f"  ensemble searcher {m['id']} failed: {str(e)[:200]}", flush=True)
        return None


def merged_text(sources):
    out = {}
    for src in sources:
        for u, t in src.items():
            out[u] = out.get(u, "") + " " + t
    return out


def judge_checks(chat, hunt, checks):
    """keep: results make it more likely than not that the candidate meets both conditions.
    reject: results positively show it fails a condition. Silence is neither."""
    keep, reject = set(), set()
    names = list(checks)
    for i in range(0, len(names), 6):
        part = {n: [{**r, "summary": (r.get("summary") or "")[:200]} for r in checks[n]] for n in names[i:i + 6]}
        v = chat.json(
            "You verify candidate answers from search results. Reply as JSON {\"keep\": [names], \"reject\": [names]}. "
            "Put a candidate in keep if its results make it more likely than not that it meets BOTH conditions. "
            "Put it in reject only if the results show it fails a condition (for example it meets only one). "
            "Leave it out of both lists if the results say nothing useful.",
            f"Condition X: {hunt['x']}\nCondition Y: {hunt['y']}\nResults per candidate:\n{json.dumps(part)}")
        keep |= {norm(k) for k in v.get("keep", []) if isinstance(k, str)}
        reject |= {norm(k) for k in v.get("reject", []) if isinstance(k, str)}
    return keep, reject


def answer(m, hunt, n=3, budget=ATTEMPT_BUDGET, role="searcher"):
    """Search-time scaling: n searchers with different lenses in parallel, union their finds, keep finds that two or
    more searchers agree on, and send the rest through batched Telem verification before submitting."""
    t0 = time.time()
    with ThreadPoolExecutor(n) as ex:
        logs = [l for l in ex.map(lambda i: safe_attempt(lens(m, hunt, i), hunt, budget, role), range(n)) if l]
    if not logs:
        raise RuntimeError("every ensemble searcher failed")
    items = merge(logs)
    agreed = [it for it in items.values() if len(it["votes"]) >= 2 and it["urls"]]
    single = [it for it in items.values() if not (len(it["votes"]) >= 2 and it["urls"])]
    # Verify singles first, then agreed finds while budget lasts: two searchers can share the same half-match.
    telem = Telem(VERIFY_BUDGET)
    queue = single + agreed
    checks = {}
    for i in range(0, len(queue), 25):
        out = check_candidates(m, {"candidates": [it["name"] for it in queue[i:i + 25]],
                                   "condition": hunt["criterion"], "per_candidate": 3}, telem)
        failed = out["checks"].pop("_error", None)
        for q, results in out["checks"].items():
            checks[norm(q[:-len(hunt["criterion"])] if q.endswith(hunt["criterion"]) else q)] = results
        if failed:
            break
    keep, reject = judge_checks(Chat(role), hunt, {it["name"]: checks[norm(it["name"])] for it in queue
                                                   if norm(it["name"]) in checks}) if checks else (set(), set())
    finds = []
    for it in queue:
        k = norm(it["name"])
        urls = [r["url"] for r in checks.get(k, [])] + it["urls"]
        ok = k in keep if it in single else k not in reject
        if ok and urls:
            finds.append({"name": it["name"], "evidence_url": it["urls"][0] if it["urls"] else urls[0]})
    kept = [f for f in finds if norm(f["name"]) not in {norm(a["name"]) for a in agreed}]
    url_providers = {}
    for log in logs:
        for u, ps in log["url_providers"].items():
            url_providers.setdefault(u, set()).update(ps)
    for u, ps in telem.url_providers.items():
        url_providers.setdefault(u, set()).update(ps)
    return {"attempt_id": uuid.uuid4().hex[:10], "method": f"{m['id']}+ensemble{n}", "hunt": hunt["name"],
            "kind": hunt["kind"], "pool": hunt["pool"], "x": hunt["x"], "y": hunt["y"], "finds": finds,
            "notes": f"{len(items)} unique candidates, {len(agreed)} agreed, {len(kept)}/{len(single)} singles verified",
            "telem_calls": [c for log in logs for c in log["telem_calls"]] + telem.calls,
            "telem_spent": round(sum(l["telem_spent"] for l in logs) + telem.spent, 4),
            "telem_session": logs[0]["telem_session"], "trace": [],
            "url_providers": {u: sorted(p) for u, p in url_providers.items()},
            "url_text": merged_text([log["url_text"] for log in logs] + [telem.url_text]),
            "seconds": round(time.time() - t0, 1), "sub_attempts": [l["attempt_id"] for l in logs]}


def closed_book(hunt, role="frontier"):
    """A frontier model answering from its own knowledge, with no search."""
    t0 = time.time()
    chat = Chat(role)
    v = chat.json("Answer from your own knowledge. Reply as JSON {\"finds\": [{\"name\": str}]}. List every item you are "
                  "confident about; wrong items cost points.", f"{hunt['question']}\nCondition X: {hunt['x']}\nCondition Y: {hunt['y']}")
    finds = [{"name": f["name"], "evidence_url": None} for f in v.get("finds", []) if isinstance(f, dict) and f.get("name")]
    return {"attempt_id": uuid.uuid4().hex[:10], "method": f"closed-book:{chat.cfg['model']}", "hunt": hunt["name"],
            "kind": hunt["kind"], "pool": hunt["pool"], "x": hunt["x"], "y": hunt["y"], "finds": finds, "notes": "",
            "telem_calls": [], "telem_spent": 0.0, "telem_session": None, "trace": [], "url_providers": {}, "url_text": {},
            "seconds": round(time.time() - t0, 1), "tokens": chat.usage}
