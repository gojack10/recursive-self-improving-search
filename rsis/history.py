import json
import re
from collections import defaultdict

from .telem import SEARCH_PRICE


def append(run_dir, name, row):
    with open(run_dir / name, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def rows(run_dir, name):
    p = run_dir / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def save_log(run_dir, log):
    d = run_dir / "logs"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{log['attempt_id']}.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")


def load_log(run_dir, attempt_id):
    return json.loads((run_dir / "logs" / f"{attempt_id}.json").read_text(encoding="utf-8"))


def table_row(log, s):
    """The numeric row kept for every attempt."""
    return {"attempt_id": log["attempt_id"], "round": log.get("round"), "role": log.get("role"), "method": log["method"],
            "hunt": log["hunt"], "kind": log["kind"], "pool": log["pool"], "score": s["score"], "correct": s["correct"],
            "wrong": s["wrong"], "total": s["total"], "duplicates": s["duplicates"],
            "x_only": s.get("x_only", 0), "y_only": s.get("y_only", 0), "spent": log["telem_spent"],
            "searches": sum(c["kind"] == "search" for c in log["telem_calls"]),
            "fetches": sum(c["kind"] == "fetch" for c in log["telem_calls"]),
            "seconds": log["seconds"], "telem_session": log["telem_session"]}


def provider_yield(run_dir, attempt_rows=None):
    """Per Telem provider: calls, spend, URLs surfaced, and correct finds whose evidence it surfaced."""
    y = defaultdict(lambda: {"searches": 0, "spend": 0.0, "results": 0, "correct_finds": 0, "wrong_finds": 0})
    for r in attempt_rows if attempt_rows is not None else rows(run_dir, "attempts.jsonl"):
        log = load_log(run_dir, r["attempt_id"])
        for c in log["telem_calls"]:
            if c["kind"] == "search":
                for p in c["used"]:
                    y[p]["searches"] += 1
                    y[p]["spend"] += SEARCH_PRICE.get(p, 0.005)
        for p_list in log["url_providers"].values():
            for p in p_list:
                y[p]["results"] += 1
        for f in log.get("referee", {}).get("rows", []):
            for p in f["providers"]:
                if f["status"] in ("correct", "verified_gap"):
                    y[p]["correct_finds"] += 1
                elif f["status"] == "wrong":
                    y[p]["wrong_finds"] += 1
    out = {}
    for p, v in y.items():
        v["spend"] = round(v["spend"], 4)
        v["correct_per_dollar"] = round(v["correct_finds"] / v["spend"], 1) if v["spend"] else None
        out[p] = v
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["correct_finds"]))


def method_scores(attempt_rows):
    agg = defaultdict(lambda: defaultdict(list))
    for r in attempt_rows:
        agg[r["method"]][r["pool"]].append(r["score"])
    return {m: {p: round(sum(v) / len(v), 3) for p, v in pools.items()} for m, pools in agg.items()}


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())
