"""Open hunts: niche "times X and Y happened" questions with no answer key.

Nobody knows the full answer, so there is no recall score. Every find must cite a URL the attempt retrieved
through Telem, and then passes an independent Tavily check and a judge on both conditions. The result is a
count of verified finds and a count of rejected ones. These are showpieces, kept out of the improvement loop's
scores.

    python -m rsis.open_hunts methods/anchor_verify.json --hunts goldfish_memory_rebuttals dog_pickle_beach
"""
import argparse
import json
import time

from . import referee
from .config import ROOT
from .searcher import attempt

OPEN = {
    "dog_pickle_beach": dict(frame="while", x="a dog ate a pickle on a beach", y="while lying in its owner's arms",
        question="Find every reported case of a dog eating a pickle on a beach while lying in its owner's arms.",
        note="Stress test. Probably no real cases; the right answer may be zero, and inventing one costs points."),
    "dog_beach_vet": dict(frame="while", x="a dog swallowed food or an object while at a beach",
        y="needed veterinary treatment afterwards",
        question="Find every reported case of a dog that swallowed food or an object while at a beach and then needed veterinary treatment."),
    "fair_goldfish_20y": dict(frame="sequence", x="a goldfish won at a fair, fete or carnival", y="lived for 20 years or more",
        question="Find every reported goldfish that was won at a fair, fete or carnival and then lived for 20 years or more."),
    "goldfish_memory_rebuttals": dict(frame="opposition", x="a study or experiment on goldfish memory",
        y="found goldfish remember things for far longer than three seconds",
        question="Find every study or experiment whose results contradict the popular claim that goldfish have a three-second memory."),
    "power_pose_nonreplications": dict(frame="opposition", x="a study testing the power-posing effect",
        y="failed to replicate it or found no hormonal or behavioural effect",
        question="Find every published study that tried to replicate the 'power posing' effect and failed to."),
    "lightning_live_match": dict(frame="while", x="lightning struck players, officials or a stadium",
        y="during a live football (soccer) match",
        question="Find every time lightning struck players, officials or the stadium during a live football (soccer) match."),
    "shoe_at_leader": dict(frame="events", x="a shoe was thrown at someone", y="the target was a sitting head of state or government",
        question="Find every time a shoe was thrown at a sitting head of state or head of government during a public appearance."),
    "marathon_wrong_turn_won": dict(frame="sequence", x="the race leader went off course in a marathon or championship road race",
        y="still won the race",
        question="Find every marathon or championship road race in which the leader went off course and still won."),
}


def hunt(name):
    h = OPEN[name]
    return {**h, "name": name, "kind": h["frame"], "pool": "open", "truth": [],
            "criterion": f"{h['x']}, and {h['y']}"}


def run(method_path, names, out_dir=ROOT / "runs" / "open"):
    m = json.loads(open(method_path, encoding="utf-8").read())
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        h = hunt(name)
        log = attempt(m, h)
        s = referee.score(log["finds"], h, log["url_providers"], url_text=log["url_text"])
        log["referee"] = s
        (out_dir / f"{name}-{log['attempt_id']}.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
        verified = [r for r in s["rows"] if r["status"] == "verified_gap"]
        print(f"\n{name} [{h['frame']}]  verified {len(verified)}  rejected {s['wrong']}  "
              f"duplicates {s['duplicates']}  telem ${log['telem_spent']:.3f}  {log['seconds']:.0f}s")
        print(f"  how many: {len(verified)} verified so far")
        for r in s["rows"]:
            print(f"  {r['status']:13} {r['name'][:70]}  {r.get('url') or ''}")
        if h.get("note"):
            print(f"  note: {h['note']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("method")
    ap.add_argument("--hunts", nargs="*", default=list(OPEN))
    a = ap.parse_args()
    run(a.method, a.hunts)
