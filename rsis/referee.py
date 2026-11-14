import re
import unicodedata
from difflib import SequenceMatcher

from . import tavily
from .config import REFEREE_DOMAINS
from .llm import Chat
from .telem import url_key

WRONG_PENALTY = 0.5
MAX_GAP_CHECKS = 20


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"^(the|a|an) ", "", s.strip())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def match(name, truth):
    for variant in (name, re.split(r" by | - | – |, | \(", name)[0]):
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


def gap_check(name, hunt, judge):
    """Independent check, through Tavily rather than the searcher's Telem route, for a find Wikidata lacks."""
    try:
        r = tavily.search(f"{name} {hunt['criterion']}", max_results=5, exclude_domains=REFEREE_DOMAINS)
    except RuntimeError as e:
        # Unchecked, so not credited: the same treatment as a find past MAX_GAP_CHECKS.
        return "wrong", f"gap check unavailable: {str(e)[:120]}", None
    snippets = "\n".join(f"- {x['title']}: {x['content'][:300]}" for x in r.get("results", []))
    known = "; ".join(t["label"] for t in hunt["truth"])
    v = judge.json(
        "You check one claimed answer against web evidence. Reply as JSON {\"verdict\": \"yes\"|\"no\"|\"same\", "
        "\"same_as\": str|null, \"meets_x\": bool, \"meets_y\": bool, \"reason\": str}. "
        "Say same, and copy the known item's name into same_as, if the claimed item is another name for one of the "
        "already-known items. "
        "Say yes only if it is a different item and the evidence clearly shows it satisfies the criterion. "
        "meets_x and meets_y say which of the two conditions the evidence supports.",
        f"Criterion: {hunt['criterion']}\nCondition X: {hunt['x']}\nCondition Y: {hunt['y']}\n"
        f"Already-known items: {known}\nClaimed item: {name}\n"
        f"Tavily answer: {r.get('answer')}\nEvidence:\n{snippets}")
    if v.get("verdict") == "same":
        return "same", v.get("reason", ""), match_one(str(v.get("same_as") or ""), hunt["truth"])
    status = "verified_gap" if v.get("verdict") == "yes" else "wrong"
    half = None
    if status == "wrong":
        half = "x_only" if v.get("meets_x") and not v.get("meets_y") else "y_only" if v.get("meets_y") and not v.get("meets_x") else "neither"
    return status, v.get("reason", ""), half


def score(finds, hunt, url_providers, check_gaps=True, require_evidence=True, url_text=None):
    truth = hunt["truth"]
    seen, rows = set(), []
    retrieved = {url_key(u) for u in url_providers if url_key(u)}
    texts = {}
    for u, txt in (url_text or {}).items():
        texts[url_key(u)] = texts.get(url_key(u), "") + " " + norm(txt)
    unsupported_seen = set()

    by_qid = {t["qid"]: [t["label"], *t["aliases"]] for t in truth}

    def supported(url, name, qid=None):
        # A matched find may be named on the page by any of its known names, not only the searcher's spelling.
        names = [name, *by_qid.get(qid, [])]
        return url_key(url) in retrieved and (not texts or any(mentions(texts.get(url_key(url), ""), n) for n in names))
    judge = Chat("judge") if check_gaps else None
    gaps = 0
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
        elif check_gaps and gaps < MAX_GAP_CHECKS:
            gaps += 1
            status, row["reason"], extra = gap_check(name, hunt, judge)
            if status == "same":
                # Another name for a known item: correct the first time it is found.
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
    # A find first cited badly and later cited properly is a duplicate, not a wrong answer.
    for r in rows:
        if r["status"] == "unsupported" and (match(r["name"], truth) or norm(r["name"])) in seen:
            r["status"] = "duplicate"
    correct = sum(r["status"] in ("correct", "verified_gap") for r in rows)
    wrong = sum(r["status"] in ("wrong", "unsupported") for r in rows)
    total = len(truth) + sum(r["status"] == "verified_gap" for r in rows)
    return {"score": round(max(0.0, correct - WRONG_PENALTY * wrong) / max(total, 1), 4),
            "correct": correct, "wrong": wrong, "total": total,
            "duplicates": sum(r["status"] == "duplicate" for r in rows),
            "unsupported": sum(r["status"] == "unsupported" for r in rows),
            "x_only": sum(r.get("half") == "x_only" for r in rows), "y_only": sum(r.get("half") == "y_only" for r in rows),
            "missed": [t["label"] for t in truth if t["qid"] not in seen], "rows": rows}
