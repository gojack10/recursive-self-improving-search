"""Live debugger view of a run: the active state, the run tree growing down, and method iterations growing right.

    python -m rsis.view            # then open http://127.0.0.1:8765  (add ?run=<name> to pin a run)

Read-only, and it only watches. Everything is derived from the files a run already writes under runs/<name>/,
so start it before or after the run. Without ?run it follows the run that changed most recently.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import ROOT

RUNS = ROOT / "runs"
PAGE = Path(__file__).with_name("view.html")
TOOL_STATE = {"web_search": "query", "fetch_pages": "fetch", "check_candidates": "check", "submit": "submit"}
ROLE_PHASE = {"noise": "calibrate", "train": "train", "select": "select", "test": "test", "rtest": "recursion",
              "trial": "trial", "pi-trial": "trial"}


def born(p):
    st = p.stat()
    return getattr(st, "st_birthtime", st.st_ctime)


def read_json(p, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):  # missing, or caught mid-write
        return default


def read_rows(p):
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def running_search(logs, state_file):
    """A search running as a Pi agent. Its state file and Pi's event stream are written while it runs,
    so the step it is on right now can be read from them."""
    aid = state_file.name.split(".")[0]
    s = read_json(state_file, {})
    state, steps, done = "deciding", 0, False
    stream = logs / f"{aid}.pi.jsonl"
    if stream.exists():
        for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
            head = line[:48]
            if '"tool_execution_start"' in head:
                steps += 1
                tool = line.split('"toolName":"', 1)[-1].split('"', 1)[0]
                state = TOOL_STATE.get(tool, "query")
            elif '"tool_execution_end"' in head:
                state = "referee" if state == "submit" else "deciding"
            elif '"agent_end"' in head:
                done = True
    if done:
        state = "referee"
    trace = s.get("trace") or []
    left = next((t["summary"]["budget_left"] for t in reversed(trace) if (t.get("summary") or {}).get("budget_left") is not None), s.get("budget"))
    return {"id": aid, "method": (s.get("method") or {}).get("id"), "task": (s.get("question") or "")[:80],
            "state": state, "steps": steps, "left": left, "started": born(state_file), "runner": "Pi agent"}


def tree_nodes(run_dir, methods):
    base = run_dir / "tree" / "nodes"
    nodes, parent = [], {}
    if not base.exists():
        return nodes
    by_node = {m.get("node"): m for m in methods}
    for d in base.iterdir():
        f = d / "node.md"
        if not f.exists():
            continue
        front = f.read_text(encoding="utf-8").split("\n---\n", 1)[0].removeprefix("---\n")
        head = {}
        for line in front.splitlines():
            if ": " in line:
                k, v = line.split(": ", 1)
                try:
                    head[k] = json.loads(v)
                except ValueError:
                    head[k] = v
        for c in (d / "children").glob("*"):
            parent[c.name] = d.name
        m = by_node.get(d.name)
        nodes.append({"id": d.name, "name": head.get("name"), "kind": head.get("kind"), "status": head.get("status"),
                      "summary": head.get("micro_summary"), "t": born(d),
                      "select_score": m.get("select_score") if m else None})
    for n in nodes:
        n["parent"] = parent.get(n["id"])
    return sorted(nodes, key=lambda n: n["t"])


def phase(state, nodes, rows, errors, methods, running):
    """Which loop state the run is in, read from what it has written so far."""
    probe = next((n for n in reversed(nodes) if n["kind"] == "Probe" and n["status"] == "in_progress"), None)
    if probe:
        rnd = (state or {}).get("round", 0) + 1
        def count(role):
            return sum(r.get("round") == rnd and r.get("role") == role for r in rows + errors)
        cands = sum(m.get("round") == rnd and m.get("status") != "recursion-test" for m in methods)
        sel = count("select")
        if count("test") >= 4:
            return "tally", rnd
        if count("test") or sel >= 2 * (1 + cands):
            return "test", rnd
        if sel or cands:
            return "select", rnd
        return ("improve" if count("train") >= 2 else "train"), rnd
    if running:
        return ("calibrate" if rows and rows[-1].get("role") == "noise" else "trial"), None
    if rows:
        last = rows[-1].get("role")
        return "idle after " + ROLE_PHASE.get(last, "compare"), None
    return "idle", None


def snapshot(name):
    d = RUNS / name
    logs = d / "logs"
    rows, errors = read_rows(d / "attempts.jsonl"), read_rows(d / "errors.jsonl")
    finished = {r["attempt_id"] for r in rows}
    methods = [m for m in (read_json(p) for p in sorted((d / "methods").glob("*.json"))) if m] if (d / "methods").exists() else []
    state = read_json(d / "state.json")
    nodes = tree_nodes(d, methods)
    running = []
    for sf in sorted(logs.glob("*.state.json")) if logs.exists() else []:
        aid = sf.name.split(".")[0]
        if aid not in finished and not (logs / f"{aid}.json").exists():
            running.append(running_search(logs, sf))
    ph, rnd = phase(state, nodes, rows, errors, methods, running)
    feed = [{"t": born(logs / f"{r['attempt_id']}.json") if (logs / f"{r['attempt_id']}.json").exists() else 0,
             "text": f"search {r['attempt_id']} scored {r['score']:.2f}: {r['method']} on {r['hunt']} ({r.get('role')}), "
                     f"{r['correct']} correct, {r['wrong']} wrong of {r['total']}, ${r['spent']:.3f}"} for r in rows[-40:]]
    feed += [{"t": n["t"], "text": f"tree + {n['kind']}: {n['name']}"} for n in nodes[-40:]]
    return {
        "name": name, "phase": ph, "iteration": rnd, "state": state, "running": running, "nodes": nodes,
        "methods": [{k: m.get(k) for k in ("id", "parent", "round", "status", "select_score")} for m in methods],
        "spend": round(sum(r.get("spent") or 0 for r in rows), 3), "searches_done": len(rows), "failed": len(errors),
        "last_error": (errors[-1].get("error") or "")[:300] if errors else None,
        "feed": [f for f in sorted(feed, key=lambda f: -f["t"])[:14]],
    }


def latest_run():
    runs = [p for p in RUNS.iterdir() if p.is_dir()] if RUNS.exists() else []
    def changed(p):
        return max((f.stat().st_mtime for f in [p, *p.glob("*"), *(p / "logs").glob("*")]), default=0)
    return max(runs, key=changed).name if runs else None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/run":
            name = (parse_qs(u.query).get("name") or [""])[0] or latest_run()
            if not name or "/" in name or not (RUNS / name).is_dir():
                return self.send(json.dumps({"name": None}), "application/json")
            self.send(json.dumps(snapshot(name)), "application/json")
        elif u.path == "/":
            self.send(PAGE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        else:
            self.send("not found", "text/plain", 404)

    def send(self, body, kind, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="python -m rsis.view")
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    print(f"http://127.0.0.1:{a.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
