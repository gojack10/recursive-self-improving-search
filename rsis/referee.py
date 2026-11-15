import os
import re
import sqlite3
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher

from . import tavily
from .config import REFEREE_DOMAINS, ROOT
from .llm import Chat
from .telem import url_key

WRONG_PENALTY = 0.5
# Gap checks from every search being scored share this pool; each one is a Tavily search and a judge call.
JUDGE_POOL = ThreadPoolExecutor(int(os.environ.get("JUDGE_WORKERS", "10")))
VERDICTS = ROOT / "runs" / "judge_verdicts.sqlite"
verdicts_lock = threading.Lock()


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"^(the|a|an) ", "", s.strip())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def match(name, truth):
    for variant in (name, re.split(r" by | - | – | — |; |, | \(", name)[0]):
        q = match_one(variant, truth)
        if q:
            return q
    return None


def match_one(name, truth):
    n = norm(name)
    if not n:
        return None
    best, best_r = None, 0.0
    for t in truth:
        for cand in [t["label"], *t["aliases"]]:
            c = norm(cand)
            if not c:
                continue
            if n == c:
                return t["qid"]
            if re.findall(r"\d+", n) != re.findall(r"\d+", c):
                continue
            r = SequenceMatcher(None, n, c).ratio()
            if r > best_r:
                best, best_r = t["qid"], r
    return best if best_r >= 0.9 else None


STOP = {"the", "and", "of", "for", "flight", "prize", "award", "airport", "disaster", "novel", "film", "river", "bridge"}


def mentions(text, name):
    """Every number in the name and at least one distinctive word (4+ letters, not generic) appear in the text."""
    toks = norm(name).split()
    digits = [w for w in toks if w.isdigit()]
    words = [w for w in toks if len(w) >= 4 and w not in STOP and not w.isdigit()] or [w for w in toks if not w.isdigit()]
    padded = f" {text} "
    return all(f" {d} " in padded for d in digits) and (not words or any(f" {w} " in padded for w in words))


def judge_call(judge, hunt, name, known, r, snippets):
    return judge.json(
        "You check one claimed answer against web evidence. Reply as JSON {\"verdict\": \"yes\"|\"no\"|\"unknown\"|\"same\", "
        "\"same_as\": str|null, \"meets_x\": bool, \"meets_y\": bool, \"reason\": str, \"search\": str|null}. "
        "Say same, and copy the known item's name into same_as, if the claimed item is another name for one of the "
        "already-known items. "
        "Say yes only if it is a different item and the evidence clearly shows it satisfies the criterion. "
        "Say no only if the evidence shows it fails the criterion. Say unknown if the evidence does not settle it, "
        "and put in search one short web query that would settle the missing fact. "
        "meets_x and meets_y say which of the two conditions the evidence supports.",
        f"Criterion: {hunt['criterion']}\n" + (f"Condition X: {hunt['x']}\nCondition Y: {hunt['y']}\n" if hunt["y"] else "") +
        f"Already-known items: {known}\nClaimed item: {name}\n"
        f"Tavily answer: {r.get('answer')}\nEvidence:\n{snippets}")


def gap_check(name, hunt, judge, verified):
    """Independent check, through Tavily rather than the searcher's Telem route, for a find the answer key lacks.
    verified maps the normalized name of each answer the judge has already accepted for this task to its name."""
    r = tavily.search(f"{name} {hunt['criterion']}", max_results=5, exclude_domains=REFEREE_DOMAINS)
    snippets = "\n".join(f"- {x.get('title') or ''}: {(x.get('content') or '')[:300]}" for x in (r.get("results") or []) if isinstance(x, dict))
    known = "; ".join([*(t["label"] for t in hunt["truth"]), *verified.values()])
    v = judge_call(judge, hunt, name, known, r, snippets)
    if v.get("verdict") not in ("yes", "same") and v.get("search"):
        # One lookup rarely returns both halves of a criterion: look up the fact the judge is missing, then rule again.
        more = tavily.search(str(v["search"])[:200], max_results=5, exclude_domains=REFEREE_DOMAINS)
        snippets += "\n" + "\n".join(f"- {x.get('title') or ''}: {(x.get('content') or '')[:300]}" for x in (more.get("results") or []) if isinstance(x, dict))
        v = judge_call(judge, hunt, name, known, r, snippets)
    if v.get("verdict") == "same":
        same = str(v.get("same_as") or "")
        return "same", v.get("reason", ""), match_one(same, hunt["truth"]) or (norm(same) if norm(same) in verified else None)
    # Wrong only when the evidence contradicts the answer; an answer nobody could settle is unconfirmed and costs nothing.
    status = {"yes": "verified_gap", "no": "wrong"}.get(v.get("verdict"), "unconfirmed")
    half = None
    if status != "verified_gap":
        half = "x_only" if v.get("meets_x") and not v.get("meets_y") else "y_only" if v.get("meets_y") and not v.get("meets_x") else "neither"
    return status, v.get("reason", ""), half


def verdicts_db():
    VERDICTS.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(VERDICTS)
    db.execute("CREATE TABLE IF NOT EXISTS verdicts (task TEXT, answer TEXT, name TEXT, status TEXT, reason TEXT, extra TEXT, "
               "judge TEXT, checked_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (task, answer))")
    return db


def judge_all(names, hunt, emit):
    """A verdict for every find the answer key lacks. A verdict the judge already gave for this task is reused,
    so each distinct answer is judged once, however many searches submit it."""
    with verdicts_lock:
        db = verdicts_db()
        stored = db.execute("SELECT answer, name, status, reason, extra FROM verdicts WHERE task = ?", (hunt["name"],)).fetchall()
        db.close()
    known = {a: (st, why, extra) for a, _, st, why, extra in stored}
    verified = {a: name for a, name, st, _, _ in stored if st == "verified_gap"}
    todo = list({norm(n): n for n in names if norm(n) not in known}.values())
    if names:
        emit(event="plan", unmatched=len(names), reused=len(names) - len(todo), to_check=len(todo))
    for n in names:
        if norm(n) in known:
            st, why, _ = known[norm(n)]
            emit(event="end", name=n, status=st, reason=why, reused=True)
    judge = Chat("judge")

    def one(name):
        emit(event="start", name=name)
        started = time.monotonic()
        try:
            verdict = gap_check(name, hunt, judge, verified)
        except Exception as e:
            # Unchecked, so not credited and not remembered: the next search to submit it is checked again.
            verdict = ("unconfirmed", f"gap check unavailable: {str(e)[:120]}", None)
        else:
            with verdicts_lock:
                db = verdicts_db()
                db.execute("INSERT OR REPLACE INTO verdicts (task, answer, name, status, reason, extra, judge) VALUES (?,?,?,?,?,?,?)",
                           (hunt["name"], norm(name), name, *verdict, judge.cfg["model"]))
                db.commit()
                db.close()
        emit(event="end", name=name, status=verdict[0], reason=verdict[1], seconds=round(time.monotonic() - started, 1))
        return norm(name), verdict

    known.update(JUDGE_POOL.map(one, todo))
    if names:
        emit(event="done")
    return known


def score(finds, hunt, url_providers, check_gaps=True, require_evidence=True, url_text=None, on_event=None):
    truth = hunt["truth"]
    retrieved = {url_key(u) for u in url_providers if url_key(u)}
    texts = {}
    for u, txt in (url_text or {}).items():
        texts[url_key(u)] = texts.get(url_key(u), "") + " " + norm(txt)

    by_qid = {t["qid"]: [t["label"], *t["aliases"]] for t in truth}

    def supported(url, name, qid=None):
        # A matched find may be named on the page by any of its known names, not only the searcher's spelling.
        names = [name, *by_qid.get(qid, [])]
        return url_key(url) in retrieved and (not texts or any(mentions(texts.get(url_key(url), ""), n) for n in names))

    def walk(verdict):
        seen, rows, unsupported_seen = set(), [], set()
        for f in finds:
            if not isinstance(f, dict):
                continue
            name = str(f.get("name") or "").strip()
            url = str(f.get("evidence_url") or "")
            qid = match(name, truth)
            key = qid or norm(name)
            row = {"name": name, "url": url, "providers": sorted(next((p for u, p in url_providers.items() if url_key(u) == url_key(url)), []))}
            if not key:
                row["status"] = "wrong"
            elif key in seen or (key in unsupported_seen and not supported(url, name, qid)):
                row["status"] = "duplicate"
            elif require_evidence and not supported(url, name, qid):
                # The cited URL must be one this attempt retrieved through Telem, and its text must mention the find,
                # so recital from memory with an arbitrary retrieved URL scores as wrong.
                row["status"] = "unsupported"
                unsupported_seen.add(key)
            elif qid:
                row["status"], row["qid"] = "correct", qid
                seen.add(qid)
            elif check_gaps:
                status, row["reason"], extra = verdict(name)
                if status == "same":
                    # Another name for an item in the key or already verified: correct the first time it is found.
                    row["status"] = "duplicate" if extra is None or extra in seen else "correct"
                    if extra:
                        row["qid"] = extra
                        seen.add(extra)
                else:
                    row["status"], row["half"] = status, extra
                seen.add(key)
            else:
                row["status"] = "wrong"
                seen.add(key)
            rows.append(row)
        return rows, seen

    # Which finds need the judge does not depend on its verdicts, so collect them, judge them together, then score.
    unmatched = []
    walk(lambda name: unmatched.append(name) or ("wrong", "", None))
    verdicts = judge_all(unmatched, hunt, on_event or (lambda **e: None)) if check_gaps else {}
    rows, seen = walk(lambda name: verdicts[norm(name)])
    # A find first cited badly and later cited properly is a duplicate, not a wrong answer.
    for r in rows:
        if r["status"] == "unsupported" and (match(r["name"], truth) or norm(r["name"])) in seen:
            r["status"] = "duplicate"
    correct = sum(r["status"] in ("correct", "verified_gap") for r in rows)
    wrong = sum(r["status"] in ("wrong", "unsupported") for r in rows)
    # The full answer is the key plus every answer the judge has verified for this task, in this search or an earlier one.
    # A question with no key is therefore scored against the best list found so far.
    pool = {a: v for a, v in verdicts.items() if v[0] == "verified_gap"}
    total = len(truth) + len(pool)
    return {"score": round(max(0.0, correct - WRONG_PENALTY * wrong) / max(total, 1), 4),
            "correct": correct, "wrong": wrong, "total": total,
            "duplicates": sum(r["status"] == "duplicate" for r in rows),
            "unsupported": sum(r["status"] == "unsupported" for r in rows),
            "x_only": sum(r.get("half") == "x_only" for r in rows), "y_only": sum(r.get("half") == "y_only" for r in rows),
            "missed": [t["label"] for t in truth if t["qid"] not in seen] + [a for a in pool if a not in seen], "rows": rows}
