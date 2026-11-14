import json
import random
from concurrent.futures import ThreadPoolExecutor

from . import history as H
from . import hunts as HU
from . import method as M
from . import referee, tavily
from .config import ROOT
from .improver import improve
from .searcher import attempt
from .tree import Tree

WORKERS = 6


def run_dir(name):
    d = ROOT / "runs" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def state(d):
    p = d / "state.json"
    return json.loads(p.read_text()) if p.exists() else None


def save_state(d, s):
    (d / "state.json").write_text(json.dumps(s, indent=1))


def init(name):
    d = run_dir(name)
    if state(d):
        return d
    tree = Tree(d)
    seed = json.loads((M.SEED / "v000.json").read_text(encoding="utf-8"))
    goal = tree.write("Goal", "Recursive self-improving search run " + name,
                      "Improve a search method by searching with that same method.",
                      "Hunts are scored by a Wikidata referee; methods route searches through Telem.")
    seed["node"] = tree.write("Idea", "Method v000", seed["rationale"], f"```json\n{json.dumps(seed, indent=1)}\n```", parent=goal)
    seed["status"] = "adopted"
    M.save(d, seed)
    save_state(d, {"goal": goal, "current": "v000", "round": 0, "best_test": None, "noise": None,
                   "flat_rounds": 0, "breakouts_without_gain": 0, "test_points": []})
    return d


def run_and_score(d, m, hunt_name, rnd, role, check_gaps=True):
    hunt = HU.load(hunt_name)
    log = attempt(m, hunt)
    log["round"], log["role"] = rnd, role
    log["referee"] = referee.score(log["finds"], hunt, log["url_providers"], check_gaps=check_gaps)
    H.save_log(d, log)
    row = H.table_row(log, log["referee"])
    H.append(d, "attempts.jsonl", row)
    print(f"  r{rnd} {role:9} {m['id']} {hunt_name:22} score={row['score']:.3f} "
          f"{row['correct']}/{row['total']} wrong={row['wrong']} ${row['spent']:.3f}", flush=True)
    return row


def safe_run(d, m, hunt_name, rnd, role):
    try:
        return run_and_score(d, m, hunt_name, rnd, role)
    except Exception as e:
        print(f"  r{rnd} {role:9} {m['id']} {hunt_name:22} FAILED: {str(e)[:200]}", flush=True)
        H.append(d, "errors.jsonl", {"round": rnd, "role": role, "method": m["id"], "hunt": hunt_name, "error": str(e)[:1000]})
        return {"method": m["id"], "hunt": hunt_name, "score": 0.0, "failed": True}


def batch(d, jobs, rnd):
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(lambda j: safe_run(d, j[0], j[1], rnd, j[2]), jobs))


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def rotate(pool, rnd, n):
    return [pool[(rnd * n + i) % len(pool)] for i in range(n)]


def telem_total(d):
    return round(sum(r["spent"] for r in H.rows(d, "attempts.jsonl")), 4)


def calibrate(name, runs=3):
    """Noise band: run the current method several times on the fixed held-out test hunts."""
    d = init(name)
    s = state(d)
    m = M.load(d, s["current"])
    test = HU.pool("test")
    rows = batch(d, [(m, h, "noise") for _ in range(runs) for h in test], 0)
    per_run = [mean([r["score"] for r in rows[i * len(test):(i + 1) * len(test)]]) for i in range(runs)]
    s["noise"] = round(max(per_run) - min(per_run), 4)
    s["best_test"] = round(mean(per_run), 4)
    s["baseline_test"] = s["best_test"]
    save_state(d, s)
    print(f"noise band {s['noise']}  baseline test {s['best_test']}")


def merge_routing(base, new):
    new = new if isinstance(new, dict) else {}
    r = {**base, **new}
    if new.get("providers") and "auto_routing" not in new:
        r["auto_routing"] = False
    return r


def new_candidates(d, tree, props, parent, rnd):
    out = []
    for c in props.get("candidates", []):
        if not isinstance(c, dict) or not c.get("instructions"):
            continue
        m = {"id": M.next_id(d), "parent": parent["id"], "round": rnd, "rationale": c.get("rationale", ""),
             "instructions": c["instructions"], "routing": merge_routing(parent["routing"], c.get("routing")),
             "routing_rules": c.get("routing_rules", ""), "fetch_policy": c.get("fetch_policy", ""), "status": "candidate"}
        m["node"] = tree.write("Idea", f"Method {m['id']}", c["rationale"][:200],
                               f"Parent: {parent['id']}\n\n```json\n{json.dumps(m, indent=1, ensure_ascii=False)}\n```",
                               parent=parent["node"])
        out.append(M.save(d, m))
    return out


def record_lessons(tree, props, probe):
    for l in props.get("lessons", []):
        tree.write("What We Learned", l["title"], l["body"][:200],
                   f"{l['body']}\n\n**Tested scope:** {l['scope']}\n\n**Evidence attempts:** {l.get('evidence_attempts', [])}",
                   parent=probe)
    for f in props.get("failure_links", []):
        if f.get("node_id") and (tree.dir / f["node_id"]).exists():
            tree.append(f["node_id"], f"- Seen again in attempt {f.get('attempt_id')}: {f.get('why', '')}")
    return bool(props.get("lessons"))


def one_round(name, k=2, breakout=False):
    d = init(name)
    tree = Tree(d)
    s = state(d)
    rnd = s["round"] + 1
    cur = M.load(d, s["current"])
    print(f"round {rnd}: current {cur['id']}{' (breakout)' if breakout else ''}", flush=True)
    probe = tree.write("Probe", f"Round {rnd}", f"Improve {cur['id']} and trial candidates on unseen hunts.",
                       f"Current method: {cur['id']}", parent=s["goal"])

    train_rows = batch(d, [(cur, h, "train") for h in rotate(HU.pool("train"), rnd, 2)], rnd)
    train_ids = {r["attempt_id"] for r in H.rows(d, "attempts.jsonl") if r["pool"] == "train"}

    if not breakout:
        props, _ = improve(d, tree, cur, cur, train_ids, k=k)
        cands = new_candidates(d, tree, props, cur, rnd)
        new_lessons = record_lessons(tree, props, probe)
    else:
        # Fresh improvers, each with a different slice of history and a different earlier version to build on.
        olds = [m for m in M.all_methods(d) if m.get("status") in ("adopted", "superseded")] or [cur]
        cands, new_lessons = [], False
        for _ in range(k):
            base = random.choice(olds)
            ids = set(random.sample(sorted(train_ids), max(1, len(train_ids) // 2)))
            props, _ = improve(d, tree, base, base, ids, k=1)
            cands += new_candidates(d, tree, props, base, rnd)
            new_lessons |= record_lessons(tree, props, probe)

    sel = rotate(HU.pool("select"), rnd, 2)
    rows = batch(d, [(m, h, "select") for m in [cur, *cands] for h in sel], rnd)
    by = {m["id"]: round(mean([r["score"] for r in rows if r["method"] == m["id"]]), 4) for m in [cur, *cands]}
    winner_id = max(by, key=by.get)
    adopted = winner_id != cur["id"] and by[winner_id] > by[cur["id"]]
    for m in cands:
        m["select_score"] = by[m["id"]]
        if m["id"] == winner_id and adopted:
            m["status"] = "adopted"
            tree.set_status(m["node"], "resolved")
            tree.write("Agreed Work", f"Adopt {m['id']}", f"{m['id']} beat {cur['id']} on unseen select hunts.",
                       f"Select scores: {json.dumps(by)}\nHunts: {sel}", parent=m["node"])
            cur["status"] = "superseded"
            M.save(d, cur)
        else:
            m["status"] = "discarded"
            tree.set_status(m["node"], "discarded")
            tree.append(m["node"], f"Discarded in round {rnd}: select {by[m['id']]:.3f} vs current {by[cur['id']]:.3f}.")
        M.save(d, m)
    winner = M.load(d, winner_id if adopted else cur["id"])

    # Guard against best-of-k luck: re-run the round's winner on unseen test hunts and plot the re-run.
    test_rows = batch(d, [(winner, h, "test") for h in HU.pool("test")], rnd)
    test_score = mean([r["score"] for r in test_rows])
    noise = s["noise"] or 0.0
    gained = s["best_test"] is None or test_score > s["best_test"] + noise
    if gained:
        s["best_test"], s["flat_rounds"], s["breakouts_without_gain"] = round(test_score, 4), 0, 0
    else:
        s["flat_rounds"] += 1
        if breakout:
            s["breakouts_without_gain"] += 1
    s["current"], s["round"] = winner["id"], rnd
    point = {"round": rnd, "method": winner["id"], "test": round(test_score, 4), "adopted": adopted, "select": by,
             "train": round(mean([r["score"] for r in train_rows]), 4), "breakout": breakout,
             "new_lessons": new_lessons, "telem_total": telem_total(d), "tavily_credits": tavily.credits_used}
    s["test_points"].append(point)
    if rnd == 1:
        s["tree_r1"] = [n["id"] for n in tree.nodes()]
    tree.append(probe, f"Select scores: {json.dumps(by)}\nWinner: {winner['id']} (adopted={adopted})\n"
                       f"Test re-run: {test_score:.3f} (best {s['best_test']}, noise {noise})")
    tree.set_status(probe, "resolved")
    save_state(d, s)
    H.append(d, "rounds.jsonl", point)
    print(f"round {rnd} done: winner {winner['id']} adopted={adopted} test={test_score:.3f} flat={s['flat_rounds']}")
    return s


def run(name, rounds, k=2, max_spend=30.0):
    """Main loop with the plateau matrix: two flat rounds in a row trigger a breakout round;
    two breakouts in a row without a counted gain stop the run as 'levelled off'."""
    d = init(name)
    if state(d)["noise"] is None:
        calibrate(name)
    for _ in range(rounds):
        s = state(d)
        if telem_total(d) > max_spend:
            print("spend cap reached")
            break
        if s["breakouts_without_gain"] >= 2:
            print("levelled off: two breakout rounds without a counted gain")
            break
        last = s["test_points"][-1] if s["test_points"] else None
        if last and last["test"] > 0.8:
            print("test hunts near ceiling; switch to harder hunts")
        one_round(name, k=k, breakout=s["flat_rounds"] >= 2)


def recursion_test(name, gens=None):
    """Same improvement job for several generations: start from v000 with the round-1 history (attempts, lineage,
    provider yield and tree nodes frozen at the end of round 1) and the same budget; only the search method the
    improver uses changes. Rising successor scores mean better ability to improve."""
    d = init(name)
    tree = Tree(d)
    s = state(d)
    v0 = M.load(d, "v000")
    adopted = [m for m in M.all_methods(d) if m.get("status") in ("adopted", "superseded")]
    gens = gens or [m["id"] for m in adopted]
    first_ids = {r["attempt_id"] for r in H.rows(d, "attempts.jsonl") if r["pool"] == "train" and r["round"] == 1}
    allowed = set(s.get("tree_r1", []))
    test = HU.pool("test")
    out = []
    for g in gens:
        props, _ = improve(d, tree, v0, M.load(d, g), first_ids, k=1, as_of_round=1, allowed_nodes=allowed)
        c = next(c for c in props["candidates"] if isinstance(c, dict) and c.get("instructions"))
        succ = {"id": f"rt-{g}", "parent": "v000", "rationale": c.get("rationale", ""), "instructions": c["instructions"],
                "routing": merge_routing(v0["routing"], c.get("routing")), "routing_rules": c.get("routing_rules", ""),
                "fetch_policy": c.get("fetch_policy", ""), "status": "recursion-test", "node": None}
        M.save(d, succ)
        rows = batch(d, [(succ, h, "rtest") for h in test], 0)
        out.append({"generation": g, "successor": succ["id"], "score": round(mean([r["score"] for r in rows]), 4)})
        print(out[-1], flush=True)
    H.append(d, "recursion_test.jsonl", {"results": out, "hunts": test})
    return out


def trial(method_paths, hunt_names=None, repeats=1, name="trials"):
    """Run hand-written methods head to head on the same hunts and budget. For testing tactics outside the loop."""
    d = run_dir(name)
    methods = [json.loads(open(p, encoding="utf-8").read()) for p in method_paths]
    hunt_names = hunt_names or HU.pool("test")
    rows = batch(d, [(m, h, "trial") for m in methods for h in hunt_names for _ in range(repeats)], 0)
    print(f"{'method':16} {'score':>6} {'correct':>8} {'wrong':>6} {'x_only':>7} {'y_only':>7} {'spend':>7}")
    for m in methods:
        rs = [r for r in rows if r["method"] == m["id"] and not r.get("failed")]
        print(f"{m['id']:16} {mean([r['score'] for r in rs]):6.3f} {sum(r['correct'] for r in rs):8} "
              f"{sum(r['wrong'] for r in rs):6} {sum(r['x_only'] for r in rs):7} {sum(r['y_only'] for r in rs):7} "
              f"${sum(r['spent'] for r in rs):6.3f}")
    return rows
