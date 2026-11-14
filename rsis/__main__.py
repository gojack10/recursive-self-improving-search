import argparse
import json

from . import hunts, loop, report


def smoke():
    """One cheap call to each external service, so key and model problems show before a run."""
    from . import tavily
    from .llm import Chat
    from .telem import PROVIDERS, Telem

    t = Telem(1.0)
    r = t.search("Abel Prize laureates list", auto_routing=True, num_results=3)
    print("telem auto-routing:", r["providers_used"], len(r["results"]), "results", t.calls[-1]["routing"])
    for p in PROVIDERS:
        try:
            r = t.search("Niklaus Wirth programming languages", providers=[p], num_results=2)
            print(f"telem {p}: {len(r['results'])} results")
        except RuntimeError as e:
            print(f"telem {p}: {str(e)[:120]}")
    print("telem fetch:", [(p['provider'], len(p['content'])) for p in t.fetch(["https://en.wikipedia.org/wiki/Abel_Prize"])["pages"]])
    print(f"telem smoke spend ${t.spent:.4f}, session {t.session_id}")
    r = tavily.search("Ada Yonath Nobel Prize in Chemistry", max_results=2)
    print("tavily:", r.get("answer", "")[:100], "credits", tavily.credits_used)
    for role in ("searcher", "improver", "judge", "frontier"):
        c = Chat(role)
        print(role, c.cfg["model"], "->", (c.complete([{"role": "user", "content": "Reply with the word ok."}]).get("content") or "")[:40])


p = argparse.ArgumentParser(prog="python -m rsis")
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("build-hunts")
sub.add_parser("smoke")
tr = sub.add_parser("trial")
tr.add_argument("methods", nargs="+", help="method JSON files, e.g. methods/v000.json methods/anchor_verify.json")
tr.add_argument("--hunts", nargs="*")
tr.add_argument("--repeats", type=int, default=1)
tr.add_argument("--pool", default="test", help="run every task of this pool when --hunts is not given; open is the file questions")
tr.add_argument("--name", default="trials", help="run directory under runs/")
cp = sub.add_parser("compare")
cp.add_argument("--method", help="method JSON; default is the current method of --run, else methods/anchor_verify.json")
cp.add_argument("--run", default="main")
cp.add_argument("--hunts", nargs="*")
cp.add_argument("-n", type=int, default=3, help="searchers in the ensemble")
cp.add_argument("--repeats", type=int, default=2)
for c in ("calibrate", "round", "run", "recursion-test", "report"):
    s = sub.add_parser(c)
    s.add_argument("--name", default="main")
    if c == "run":
        s.add_argument("--rounds", type=int, default=8)
        s.add_argument("--max-spend", type=float, default=30.0)
        s.add_argument("--keep-going", action="store_true", help="do not stop when the run has levelled off")
    if c in ("run", "round"):
        s.add_argument("-k", type=int, default=2)
    if c == "recursion-test":
        s.add_argument("--gens", nargs="*")
a = p.parse_args()

if a.cmd == "build-hunts":
    hunts.build()
elif a.cmd == "smoke":
    smoke()
elif a.cmd == "trial":
    loop.trial(a.methods, a.hunts, a.repeats, name=a.name, pool=a.pool)
elif a.cmd == "compare":
    loop.compare(a.method, a.run, a.hunts, a.n, repeats=a.repeats)
elif a.cmd == "calibrate":
    loop.calibrate(a.name)
elif a.cmd == "round":
    loop.baseline(a.name)
    loop.one_round(a.name, k=a.k)
elif a.cmd == "run":
    loop.run(a.name, a.rounds, k=a.k, max_spend=a.max_spend, keep_going=a.keep_going)
elif a.cmd == "recursion-test":
    print(json.dumps(loop.recursion_test(a.name, a.gens), indent=1))
if a.cmd in ("calibrate", "round", "run", "recursion-test", "report"):
    print("report:", report.write(a.name))
