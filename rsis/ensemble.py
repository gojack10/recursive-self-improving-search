import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from .config import ATTEMPT_BUDGET
from .llm import Chat
from .referee import norm
from .searcher import attempt, check_candidates
from .telem import Telem, url_key

LENSES = [
    "For this attempt, anchor on condition X: enumerate everything that meets X, then verify Y for each candidate.",
    "For this attempt, anchor on condition Y: enumerate everything that meets Y, then verify X for each candidate.",
    "For this attempt, first write down every item you can recall from memory that might meet both conditions, "
    "then search for pages that list the intersection directly, and verify every recalled item before submitting.",
]
VERIFY_BUDGET = 0.06


def ensemble_budget(n, budget=ATTEMPT_BUDGET):
    return n * budget + VERIFY_BUDGET


def lens(m, i):
    return {**m, "id": f"{m['id']}+lens{i}", "instructions": m["instructions"] + "\n\n" + LENSES[i % len(LENSES)]}


def merge(logs):
    """Union of finds across searchers, keyed by normalized name, with how many searchers found each."""
    items = {}
    for log in logs:
        for f in log["finds"]:
            k = norm(f.get("name") or "")
            if not k:
                continue
            it = items.setdefault(k, {"name": f["name"], "urls": [], "votes": set()})
            if url_key(f.get("evidence_url")) in {url_key(u) for u in log["url_providers"]}:
                it["urls"].append(f["evidence_url"])
            it["votes"].add(log["attempt_id"])
    return items


def judge_checks(chat, hunt, checks):
    keep = set()
    names = list(checks)
    for i in range(0, len(names), 12):
        part = {n: checks[n] for n in names[i:i + 12]}
        v = chat.json(
            "You verify candidate answers from search results. Reply as JSON {\"keep\": [candidate strings]}. "
            "Keep a candidate if its results make it more likely than not that it meets BOTH conditions. "
            "Drop it if the results show it meets only one condition or say nothing about it.",
            f"Condition X: {hunt['x']}\nCondition Y: {hunt['y']}\nResults per candidate:\n{json.dumps(part)[:20000]}")
        keep |= {k for k in v.get("keep", []) if isinstance(k, str)}
    return keep


def answer(m, hunt, n=3, budget=ATTEMPT_BUDGET, role="searcher"):
    """Search-time scaling: n searchers with different lenses in parallel, union their finds, keep finds that two or
    more searchers agree on, and send the rest through batched Telem verification before submitting."""
    t0 = time.time()
    with ThreadPoolExecutor(n) as ex:
        logs = list(ex.map(lambda i: attempt(lens(m, i), hunt, budget=budget, role=role), range(n)))
    items = merge(logs)
    # Agreement needs at least one searcher-retrieved URL; anything else goes through verification.
    agreed = [it for it in items.values() if len(it["votes"]) >= 2 and it["urls"]]
    single = [it for it in items.values() if not (len(it["votes"]) >= 2 and it["urls"])]
    telem = Telem(VERIFY_BUDGET)
    kept = []
    if single:
        by_norm = {norm(it["name"]): it for it in single}
        checks = {}
        for i in range(0, len(single), 25):
            out = check_candidates(m, {"candidates": [it["name"] for it in single[i:i + 25]],
                                       "condition": hunt["criterion"], "per_candidate": 3}, telem)
            for q, results in out["checks"].items():
                if q == "_error":
                    continue
                cand = q[:-len(hunt["criterion"])].strip() if q.endswith(hunt["criterion"]) else q
                checks[cand] = results
        for k in judge_checks(Chat(role), hunt, checks):
            it = by_norm.get(norm(k[:-len(hunt["criterion"])] if k.endswith(hunt["criterion"]) else k))
            if it:
                urls = [r["url"] for r in checks.get(it["name"], [])]
                if urls or it["urls"]:
                    kept.append({**it, "evidence_url": urls[0] if urls else it["urls"][0]})
    finds = [{"name": it["name"], "evidence_url": it.get("evidence_url") or it["urls"][0]} for it in agreed + kept]
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
            "telem_calls": [], "telem_spent": 0.0, "telem_session": None, "trace": [], "url_providers": {},
            "seconds": round(time.time() - t0, 1), "tokens": chat.usage}
