import json
import os
import random
import threading
import time
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
    os.environ["RSIS_RUN_DIR"] = str(d)
    return d


def state(d):
    p = d / "state.json"
    return json.loads(p.read_text()) if p.exists() else None


def save_state(d, s):
    tmp = d / "state.json.tmp"
    tmp.write_text(json.dumps(s, indent=1))
    os.replace(tmp, d / "state.json")


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


def run_and_score(d, m, hunt_name, rnd, role, check_gaps=True, make=None):
    hunt = HU.load(hunt_name)
    log = make(hunt) if make else attempt(m, hunt)
    if log.get("error") and method_caused(log["error"]) and "finds" in log:
        # The method itself broke the attempt (e.g. its fetch policy overflowed the context): that is a result, score it.
        log["finds"] = []
    elif log.get("error"):
        print(f"  r{rnd} {role:9} {log['method']} {hunt_name:22} FAILED after ${log['telem_spent']:.3f}: {log['error'][:150]}", flush=True)
        H.append(d, "errors.jsonl", {"round": rnd, "role": role, "method": log["method"], "hunt": hunt_name,
                                     "error": log["error"], "spent": log["telem_spent"]})
        return {"method": log["method"], "hunt": hunt_name, "label": role, "score": 0.0, "failed": True,
                "correct": 0, "wrong": 0, "x_only": 0, "y_only": 0, "spent": log["telem_spent"]}
    log["round"], log["role"] = rnd, role
    try:
        log["referee"] = referee.score(log["finds"], hunt, log["url_providers"], check_gaps=check_gaps,
                                       require_evidence=not log["method"].startswith("closed-book"),
                                       url_text=log.get("url_text"), on_event=judge_events(d, log["attempt_id"]))
    except Exception as e:
        log["error"] = f"scoring failed: {str(e)[:400]}"
        H.save_log(d, log)
        H.append(d, "errors.jsonl", {"round": rnd, "role": role, "method": log["method"], "hunt": hunt_name,
                                     "error": log["error"], "spent": log["telem_spent"]})
        return {"method": log["method"], "hunt": hunt_name, "label": role, "score": 0.0, "failed": True,
                "correct": 0, "wrong": 0, "x_only": 0, "y_only": 0, "spent": log["telem_spent"]}
    H.save_log(d, log)
    row = H.table_row(log, log["referee"])
    H.append(d, "attempts.jsonl", row)
    print(f"  r{rnd} {role:9} {log['method']} {hunt_name:22} score={row['score']:.3f} "
          f"{row['correct']}/{row['total']} wrong={row['wrong']} ${row['spent']:.3f}", flush=True)
    row["label"] = role
    return row


def judge_events(d, attempt_id):
    """The judge's progress on one search, appended to logs/<attempt>.judge.jsonl for the live view."""
    path, lock = d / "logs" / f"{attempt_id}.judge.jsonl", threading.Lock()

    def emit(**event):
        path.parent.mkdir(parents=True, exist_ok=True)
        with lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"t": round(time.time(), 2), **event}) + "\n")
    return emit


def method_caused(error):
    e = error.lower()
    return ("http 400" in e or "http 413" in e) and any(w in e for w in ("context", "token", "too long", "maximum"))


def safe_run(d, m, hunt_name, rnd, role, make=None):
    try:
        return run_and_score(d, m, hunt_name, rnd, role, make=make)
    except Exception as e:
        mid = m["id"] if m else role
        print(f"  r{rnd} {role:9} {mid} {hunt_name:22} FAILED: {str(e)[:200]}", flush=True)
        H.append(d, "errors.jsonl", {"round": rnd, "role": role, "method": mid, "hunt": hunt_name, "error": str(e)[:1000]})
        return {"method": mid, "hunt": hunt_name, "label": role, "score": 0.0, "failed": True,
                "correct": 0, "wrong": 0, "x_only": 0, "y_only": 0, "spent": 0.0}


def batch(d, jobs, rnd):
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(lambda j: safe_run(d, j[0], j[1], rnd, j[2]), jobs))


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def rotate(pool, rnd, n):
    return [pool[(rnd * n + i) % len(pool)] for i in range(n)]


def telem_total(d):
    return round(sum(r["spent"] for r in H.rows(d, "attempts.jsonl"))
                 + sum(r.get("spent", 0) for r in H.rows(d, "errors.jsonl"))
                 + sum(r.get("spent", 0) for r in H.rows(d, "improver_spend.jsonl")), 4)


def paired(rows, key):
    """Restrict rows to hunts where every group (method, run) has a successful attempt."""
    groups = {}
    for r in rows:
        groups.setdefault(key(r), set())
        if not r.get("failed"):
            groups[key(r)].add(r["hunt"])
    # A group with no successful hunt (a crashed candidate) drops out instead of emptying the comparison.
    live = [g for g in groups.values() if g]
    common = set.intersection(*live) if live else set()
    return [r for r in rows if r["hunt"] in common and not r.get("failed")]


def ok_mean(rows):
    """Mean over attempts that ran; a crash is not evidence about a method. None if nothing ran."""
    good = [r["score"] for r in rows if not r.get("failed")]
    return sum(good) / len(good) if good else None


def calibrate(name, runs=3):
    """Noise band: run the current method several times on the fixed held-out test hunts."""
    d = init(name)
    s = state(d)
    m = M.load(d, s["current"])
    test = HU.pool("test")
    rows = batch(d, [(m, h, "noise") for _ in range(runs) for h in test], 0)
    # A calibration run with any failed hunt is dropped, so every run averages the same hunts.
    # Runs are compared on the hunts they all completed; a run with nothing in common drops out.
    for i, r in enumerate(rows):
        r["run"] = i // len(test)
    fair = paired(rows, lambda r: r["run"])
    per_run = [x for x in (ok_mean([r for r in fair if r["run"] == i]) for i in range(runs)) if x is not None]
    if not per_run:
        raise RuntimeError("every calibration run failed; see errors.jsonl")
    s["noise"] = round(max(per_run) - min(per_run), 4)
    s["best_test"] = round(mean(per_run), 4)
    s["baseline_test"] = s["best_test"]
    save_state(d, s)
    print(f"noise band {s['noise']}  baseline test {s['best_test']}")


def merge_routing(base, new):
    new = new if isinstance(new, dict) else {}
    r = {**base, **new}
    for k in ("providers", "verify_providers"):
        if r.get(k) is not None:
            v = [r[k]] if isinstance(r[k], str) else r[k] if isinstance(r[k], list) else []
            r[k] = [p for p in v if isinstance(p, str)] or None
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
        m["rationale"] = str(m["rationale"])
        m["node"] = tree.write("Idea", f"Method {m['id']}", m["rationale"][:200],
                               f"Parent: {parent['id']}\n\n```json\n{json.dumps(m, indent=1, ensure_ascii=False)}\n```",
                               parent=parent["node"])
        out.append(M.save(d, m))
    return out


def record_lessons(tree, props, probe, rnd=0):
    for l in props.get("lessons") or []:
        if not isinstance(l, dict) or not l.get("body"):
            continue
        body = str(l["body"])
        tree.write("What We Learned", str(l.get("title") or body[:60]), body[:200],
                   f"{body}\n\n**Tested scope:** {l.get('scope', 'not stated')}\n\n**Evidence attempts:** {l.get('evidence_attempts', [])}",
                   parent=probe)
    for f in props.get("failure_links") or []:
        if isinstance(f, dict) and tree.exists(f.get("node_id")):
            tree.append(f["node_id"], f"- Round {rnd}: seen again in attempt {f.get('attempt_id')}: {' '.join(str(f.get('why', '')).split())}")
    return bool(props.get("lessons"))


def safe_improve(d, tree, start, search_method, ids, k):
    try:
        props, meta = improve(d, tree, start, search_method, ids, k=k)
        H.append(d, "improver_spend.jsonl", {"method": start["id"], "spent": round(meta["telem_spent"], 4)})
        return props
    except Exception as e:
        print(f"improver failed, round continues with no candidates: {str(e)[:200]}", flush=True)
        H.append(d, "errors.jsonl", {"role": "improver", "method": start["id"], "error": str(e)[:1000],
                                     "spent": round(getattr(e, "telem_spent", 0.0), 4)})
        return {}


def one_round(name, k=2, breakout=False):
    d = init(name)
    tree = Tree(d)
    s = state(d)
    rnd = s["round"] + 1
    for m in M.all_methods(d):
        if m.get("status") == "adopted" and m["id"] != s["current"]:
            m["status"] = "discarded" if m.get("round", 0) >= rnd else "superseded"
            M.save(d, m)
        elif m.get("status") == "candidate":
            # Left over from a round that was killed before selection finished.
            m["status"] = "discarded"
            M.save(d, m)
            if m.get("node"):
                Tree(d).set_status(m["node"], "discarded")
                Tree(d).append(m["node"], "Discarded: its round was interrupted before selection.")
    cur = M.load(d, s["current"])
    if cur.get("status") != "adopted":
        cur["status"] = "adopted"
        M.save(d, cur)
    print(f"round {rnd}: current {cur['id']}{' (breakout)' if breakout else ''}", flush=True)
    probe = tree.write("Probe", f"Round {rnd}", f"Improve {cur['id']} and trial candidates on unseen hunts.",
                       f"Current method: {cur['id']}", parent=s["goal"])

    train_rows = batch(d, [(cur, h, "train") for h in rotate(HU.pool("train"), rnd, 2)], rnd)
    train_ids = {r["attempt_id"] for r in H.rows(d, "attempts.jsonl") if r["pool"] == "train"}

    if not breakout:
        props = safe_improve(d, tree, cur, cur, train_ids, k)
        cands = new_candidates(d, tree, props, cur, rnd)
        new_lessons = record_lessons(tree, props, probe, rnd)
    else:
        # Fresh improvers, each with a different slice of history and a different earlier version to build on.
        olds = [m for m in M.all_methods(d) if m.get("status") in ("adopted", "superseded")] or [cur]
        cands, new_lessons = [], False
        for _ in range(k):
            base = random.choice(olds)
            ids = set(random.sample(sorted(train_ids), max(1, len(train_ids) // 2))) if train_ids else set()
            props = safe_improve(d, tree, base, base, ids, 1)
            cands += new_candidates(d, tree, props, base, rnd)
            new_lessons |= record_lessons(tree, props, probe, rnd)

    sel = rotate(HU.pool("select"), rnd, 2)
    rows = batch(d, [(m, h, "select") for m in [cur, *cands] for h in sel], rnd)
    fair = paired(rows, lambda r: r["method"])
    raw = {m["id"]: ok_mean([r for r in fair if r["method"] == m["id"]]) for m in [cur, *cands]}
    by = {k: round(v, 4) if v is not None else -1.0 for k, v in raw.items()}
    winner_id = max(by, key=by.get)
    # No adoption unless the current method actually ran on the select hunts.
    adopted = raw[cur["id"]] is not None and winner_id != cur["id"] and by[winner_id] > by[cur["id"]]
    for m in cands:
        m["select_score"] = by[m["id"]]
        if m["id"] == winner_id and adopted:
            m["status"] = "adopted"
            tree.set_status(m["node"], "resolved")
            tree.write("Agreed Work", f"Adopt {m['id']}", f"{m['id']} beat {cur['id']} on unseen select hunts.",
                       f"Select scores: {json.dumps(by)}", parent=m["node"])
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
    if any(r.get("failed") for r in test_rows):
        # A partial test set is not comparable to earlier points; record the round without a test point.
        print("a test re-run failed; no test point this round, plateau state unchanged", flush=True)
        s["current"], s["round"] = winner["id"], rnd
        if rnd == 1:
            s["tree_r1"] = [n["id"] for n in tree.nodes()]
        tree.append(probe, f"Select scores: {json.dumps(by)}\nWinner: {winner['id']} (adopted={adopted})")
        tree.set_status(probe, "resolved")
        save_state(d, s)
        return s
    test_score = ok_mean(test_rows)
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
             "train": round(ok_mean(train_rows) or 0.0, 4), "breakout": breakout,
             "new_lessons": new_lessons, "telem_total": telem_total(d), "tavily_credits": tavily.credits_used}
    s["test_points"].append(point)
    if rnd == 1:
        s["tree_r1"] = [n["id"] for n in tree.nodes()]
    tree.append(probe, f"Select scores: {json.dumps(by)}\nWinner: {winner['id']} (adopted={adopted})")
    tree.set_status(probe, "resolved")
    save_state(d, s)
    H.append(d, "rounds.jsonl", point)
    print(f"round {rnd} done: winner {winner['id']} adopted={adopted} test={test_score:.3f} flat={s['flat_rounds']}")
    return s


def run(name, rounds, k=2, max_spend=30.0, keep_going=False):
    """Main loop with the plateau matrix: two flat rounds in a row trigger a breakout round;
    two breakouts in a row without a counted gain stop the run as 'levelled off', unless keep_going."""
    d = init(name)
    if state(d)["noise"] is None:
        calibrate(name)
    for _ in range(rounds):
        s = state(d)
        if telem_total(d) > max_spend:
            print("spend cap reached")
            break
        if s["breakouts_without_gain"] >= 2 and not keep_going:
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
        try:
            props, meta = improve(d, tree, v0, M.load(d, g), first_ids, k=1, as_of_round=1, allowed_nodes=allowed,
                                  prompt_method=v0)
            H.append(d, "improver_spend.jsonl", {"method": f"rt-{g}", "spent": round(meta["telem_spent"], 4)})
        except Exception as e:
            print(f"generation {g}: improver failed: {str(e)[:200]}", flush=True)
            H.append(d, "improver_spend.jsonl", {"method": f"rt-{g}", "spent": round(getattr(e, "telem_spent", 0.0), 4)})
            continue
        c = next((c for c in props["candidates"] if isinstance(c, dict) and c.get("instructions")), None)
        if c is None:
            print(f"generation {g}: improver proposed no usable candidate", flush=True)
            continue
        succ = {"id": f"rt-{g}", "parent": "v000", "rationale": str(c.get("rationale") or ""), "instructions": c["instructions"],
                "routing": merge_routing(v0["routing"], c.get("routing")), "routing_rules": c.get("routing_rules", ""),
                "fetch_policy": c.get("fetch_policy", ""), "status": "recursion-test", "node": None}
        M.save(d, succ)
        rows = batch(d, [(succ, h, "rtest") for h in test], 0)
        if any(r.get("failed") for r in rows):
            print(f"generation {g}: a test hunt failed; generation skipped", flush=True)
            continue
        out.append({"generation": g, "successor": succ["id"], "score": round(ok_mean(rows), 4),
                    "improver_web_searches": meta["web_searches"]})
        print(out[-1], flush=True)
    H.append(d, "recursion_test.jsonl", {"results": out, "hunts": test})
    return out


def trial(method_paths, hunt_names=None, repeats=1, name="trials", pool="test"):
    """Run hand-written methods head to head on the same hunts and budget. For testing tactics outside the loop."""
    d = run_dir(name)
    methods = [json.loads(open(p, encoding="utf-8").read()) for p in method_paths]
    hunt_names = hunt_names or HU.pool(pool)
    rows = batch(d, [(m, h, "trial") for m in methods for h in hunt_names for _ in range(repeats)], 0)
    print(f"{'method':16} {'score':>6} {'correct':>8} {'wrong':>6} {'x_only':>7} {'y_only':>7} {'spend':>7}")
    for m in methods:
        rs = [r for r in rows if r["method"] == m["id"]]
        print(f"{m['id']:16} {ok_mean(rs) or 0.0:6.3f} {sum(r['correct'] for r in rs):8} "
              f"{sum(r['wrong'] for r in rs):6} {sum(r['x_only'] for r in rs):7} {sum(r['y_only'] for r in rs):7} "
              f"${sum(r['spent'] for r in rs):6.3f}  failed {sum(1 for r in rs if r.get('failed'))}")
    return rows


def compare(method_path=None, run_name="main", hunt_names=None, n=3, name="compare", repeats=2):
    """Our cheap-searcher system against a frontier model on the same hunts and referee.
    Contestants: frontier closed-book, frontier with the plain v000 harness, our best method, our ensemble of it."""
    from .config import ATTEMPT_BUDGET
    from .ensemble import answer, closed_book, ensemble_budget
    d = run_dir(name)
    if method_path:
        best = json.loads(open(method_path, encoding="utf-8").read())
    else:
        rd = ROOT / "runs" / run_name
        best = M.load(rd, state(rd)["current"]) if state(rd) else json.loads((M.SEED / "anchor_verify.json").read_text(encoding="utf-8"))
    v0 = json.loads((M.SEED / "v000.json").read_text(encoding="utf-8"))
    hunt_names = hunt_names or HU.pool("test")
    big = ensemble_budget(n)
    contestants = [
        ("frontier-closed-book", None, lambda h: closed_book(h)),
        # The frontier model gets our best method and the ensemble's whole Telem budget in one attempt.
        ("frontier+our-method", best, lambda h: attempt({**best, "id": f"frontier+{best['id']}"}, h, budget=big, role="frontier")),
        ("ours-method", best, lambda h: attempt(best, h, budget=ATTEMPT_BUDGET)),
        ("ours-ensemble", best, lambda h: answer(best, h, n=n)),
    ]
    jobs = [(label, m, h, make) for label, m, make in contestants for h in hunt_names for _ in range(repeats)]
    with ThreadPoolExecutor(WORKERS) as ex:
        rows = list(ex.map(lambda j: safe_run(d, j[1], j[2], 0, j[0], make=j[3]), jobs))
    summary = []
    fair = paired(rows, lambda r: r["label"])
    print(f"{'contestant':22} {'score':>6} {'correct':>8} {'wrong':>6} {'x_only':>7} {'y_only':>7} {'spend':>7}")
    for label, *_ in contestants:
        rs = [r for r in rows if r["label"] == label]
        s = {"contestant": label, "score": round(ok_mean([r for r in fair if r["label"] == label]) or 0.0, 4),
             "correct": sum(r["correct"] for r in rs), "wrong": sum(r["wrong"] for r in rs),
             "x_only": sum(r["x_only"] for r in rs), "y_only": sum(r["y_only"] for r in rs),
             "spend": round(sum(r["spent"] for r in rs), 4), "failed": sum(1 for r in rows if r["label"] == label and r.get("failed"))}
        summary.append(s)
        print(f"{label:22} {s['score']:6.3f} {s['correct']:8} {s['wrong']:6} {s['x_only']:7} {s['y_only']:7} ${s['spend']:6.3f}  failed {s['failed']}")
    gaps = []
    for r in rows:
        if r.get("failed"):
            continue
        log = H.load_log(d, r["attempt_id"])
        gaps += [{"contestant": r.get("role"), "hunt": r["hunt"], "name": x["name"], "reason": x.get("reason")}
                 for x in log["referee"]["rows"] if x["status"] == "verified_gap"]
    if gaps:
        print("Wikidata-gap finds the judge accepted; check these by hand before quoting scores:")
        for g in gaps:
            print(f"  {g['contestant']:22} {g['hunt']:20} {g['name']}")
    H.append(d, "compare.jsonl", {"gaps_to_hand_check": gaps, "method": best["id"], "hunts": hunt_names, "summary": summary,
                                  "per_hunt": [{k: r.get(k) for k in ("label", "hunt", "score", "correct", "wrong", "total")} for r in rows]})
    return summary
