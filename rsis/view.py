"""Live debugger view of a run: the active state, each agent's live Pi log, the run tree and method iterations.

    python -m rsis.view            # then open http://127.0.0.1:8765

Read-only, and it only watches. Everything is derived from the files a run already writes under runs/<name>/,
so start it before or after the run. It follows the run that changed most recently unless one is chosen on the page,
and shows either the whole run or one question of it.
"""
import argparse
import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import ROOT

RUNS = ROOT / "runs"
PAGE = Path(__file__).with_name("view.html")
TOOL_STATE = {"web_search": "web_search", "fetch_pages": "fetch_pages", "check_candidates": "check_candidates",
              "search_history": "history", "read_attempt": "history", "read_log": "history",
              "submit": "submit", "propose": "submit"}
STREAMS, LOCK = {}, threading.Lock()
KEEP_LINES, SHOW_LINES, LIVE_CHARS, STALE_SECONDS = 300, 80, 1500, 900
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


class Stream:
    """One agent's Pi event stream, read incrementally: each poll parses only the bytes written since the last one."""

    def __init__(self, path):
        self.path = path
        self.reset()

    def reset(self):
        self.pos, self.rest = 0, b""
        self.states, self.lines, self.count = [], [], 0
        self.live, self.turns, self.model, self.ended, self.left, self.tokens = "", 0, None, False, None, 0
        self.about, self.seen_phase = None, None

    def go(self, state):
        if not self.states or self.states[-1] != state:
            self.states.append(state)

    def say(self, kind, text):
        text = " ".join(str(text or "").split())
        if text:
            self.lines.append([kind, text[:600]])
            self.count += 1
            del self.lines[:-KEEP_LINES]

    def read(self):
        try:
            size = self.path.stat().st_size
        except OSError:
            return
        if size < self.pos:
            self.reset()
        if size == self.pos:
            return
        with self.path.open("rb") as f:
            f.seek(self.pos)
            data = self.rest + f.read()
            self.pos = f.tell()
        *whole, self.rest = data.split(b"\n")
        for raw in whole:
            self.event(raw.decode("utf-8", "replace").strip())

    def event(self, line):
        if not line:
            return
        try:
            e = json.loads(line)
        except ValueError:
            return self.say("error", line)
        if not isinstance(e, dict):
            return
        kind = e.get("type")
        if kind == "turn_start":
            self.turns += 1
            self.go("thinking")
            self.say("turn", f"turn {self.turns}")
        elif kind == "message_update":
            u = e.get("assistantMessageEvent") or {}
            t = u.get("type") or ""
            if t == "toolcall_start":
                self.go("writing")
                self.live = (u.get("toolName") or "tool") + " "
            elif t.endswith("_start"):
                self.live = ""
            elif t.endswith("_delta"):
                self.live = (self.live + str(u.get("delta") or ""))[-LIVE_CHARS:]
            elif t in ("thinking_end", "text_end"):
                self.say("think" if t == "thinking_end" else "say", u.get("content"))
                self.live = ""
            elif t == "toolcall_end":
                self.live = ""
        elif kind == "tool_execution_start":
            name = e.get("toolName")
            self.go(TOOL_STATE.get(name, "history"))
            self.say("call", f"{name} {brief_args(e.get('args'))}")
        elif kind == "tool_execution_end":
            name = e.get("toolName")
            if TOOL_STATE.get(name) != "submit":
                self.go("result")
            text = next((c.get("text") for c in ((e.get("result") or {}).get("content") or []) if isinstance(c, dict)), "")
            try:
                r = json.loads(text)
            except (TypeError, ValueError):
                r = text
            if isinstance(r, dict) and r.get("budget_left") is not None:
                self.left = r["budget_left"]
            elif isinstance(r, str) and (m := re.match(r'\{"budget_left": ([0-9.]+)', r)):   # a result cut off mid-JSON
                self.left, r = float(m.group(1)), f"budget_left={m.group(1)} (long result, cut)"
            self.say("error" if e.get("isError") else "result", f"{name} {e.get('durationMs')}ms {brief(r)}")
            for key in ("results", "pages"):
                for item in (r.get(key) or [])[:4] if isinstance(r, dict) else []:
                    if isinstance(item, dict):
                        self.say("hit", f"{item.get('title') or item.get('status') or ''} {item.get('url') or ''}")
        elif kind == "turn_end":
            m = e.get("message") or {}
            self.tokens += (m.get("usage") or {}).get("totalTokens") or 0
            if m.get("model"):
                self.model = m["model"] + (f":{m['thinkingLevel']}" if m.get("thinkingLevel") else "")
            if m.get("errorMessage"):
                self.say("error", m["errorMessage"])
        elif kind == "agent_end":
            self.ended, self.live = True, ""

    def describe(self, state_file):
        """Who this agent is, read once from the state file the runner wrote before starting it."""
        if self.about is None:
            s = read_json(state_file)
            if s is None:
                return {}
            m = s.get("method")
            if isinstance(m, str):
                try:
                    m = json.loads(m)
                except ValueError:
                    m = {"id": m[:12]}
            self.about = {"actor": s.get("actor"), "method": (m or {}).get("id"), "task": s.get("question") or "",
                          "hunt": s.get("hunt"), "budget": s.get("budget")}
        return self.about


def brief(v, limit=220):
    if isinstance(v, dict):
        parts = []
        for k, x in v.items():
            if isinstance(x, (list, dict)):
                parts.append(f"{k}[{len(x)}]")
            elif isinstance(x, str) and len(x) > 60:
                parts.append(f"{k}={x[:60]}…")
            else:
                parts.append(f"{k}={x}")
        return " ".join(parts)[:limit]
    return str(v)[:limit]


def brief_args(args, limit=300):
    if not isinstance(args, dict):
        return str(args or "")[:limit]
    parts = []
    for k, x in args.items():
        if isinstance(x, list) and all(isinstance(i, str) for i in x):
            parts.append(" | ".join(x))
        elif isinstance(x, (list, dict)):
            parts.append(f"{k}[{len(x)}]")
        else:
            parts.append(str(x))
    return " ".join(parts)[:limit]


def judge_progress(path):
    """How far the judge is through one search's unmatched finds, and its verdicts as log lines."""
    events = read_rows(path)
    plan = next((e for e in events if e.get("event") == "plan"), None)
    if not plan:
        return None, []
    ends = [e for e in events if e.get("event") == "end"]
    lines = [["judge", f"{plan['unmatched']} finds not in the answer key: {plan['reused']} already judged, {plan['to_check']} to check"]]
    for e in ends:
        took = "reused" if e.get("reused") else f"{e.get('seconds')}s"
        lines.append(["verdict", f"{e.get('status')} · {e.get('name')} ({took}) {e.get('reason') or ''}"[:400]])
    checked = sum(not e.get("reused") for e in ends)
    return {"to_check": plan["to_check"], "checked": checked, "reused": plan["reused"],
            "in_flight": sum(e.get("event") == "start" for e in events) - checked,
            "done": any(e.get("event") == "done" for e in events)}, lines


def agents(d, rows):
    """Every Pi agent of the run, with the states it has actually passed through and its readable log."""
    logs = d / "logs"
    by_id = {r["attempt_id"]: r for r in rows}
    now, out = time.time(), []
    for f in sorted(logs.glob("*.pi.jsonl")) if logs.exists() else []:
        aid = f.name.split(".")[0]
        with LOCK:
            s = STREAMS.get(f)
            if s is None:
                s = STREAMS[f] = Stream(f)
            s.read()
            about = s.describe(logs / f"{aid}.state.json")
            improver = about.get("actor") == "improver"
            row, scored_file = by_id.get(aid), logs / f"{aid}.json"
            started, last = born(f), f.stat().st_mtime
            path = list(s.states)
            judge, judged = judge_progress(logs / f"{aid}.judge.jsonl")
            if s.ended and not improver:
                path.append("scoring")
            if judge and judge["to_check"]:
                path.append("judging")
            if row or scored_file.exists() or (s.ended and improver):
                path.append("done")
            final = bool(path) and path[-1] == "done"
            stalled = not final and now - last > STALE_SECONDS
            finished = (born(scored_file) if scored_file.exists() else last) if final else None
            out.append((s, {
                "id": aid, "role": "improver" if improver else (row or {}).get("role"), "model": s.model,
                "method": about.get("method"), "task": about.get("task"), "hunt": about.get("hunt") or (row or {}).get("hunt"), "budget": about.get("budget"), "left": s.left,
                "state": "stalled" if stalled else path[-1] if path else "starting", "running": not final and not stalled,
                "path": path, "turns": s.turns, "tokens": s.tokens, "started": started, "finished": finished,
                "agent_s": round((last if s.ended else now) - started, 1),
                "scoring_s": round((finished or now) - last, 1) if s.ended and not improver and not stalled else None,
                "score": {k: row[k] for k in ("score", "correct", "wrong", "total")} if row else None,
                "judge": judge, "lines": (s.lines + judged)[-SHOW_LINES:], "live": s.live,
                "v": f"{s.count}:{len(s.live)}:{len(path)}:{len(judged)}"}))
    return out


def shown(found, ph, now, task):
    """Running agents, those that finished in the last half minute, then the most recent others up to four cards.
    With a task chosen, only that task's agents, up to six."""
    for s, a in found:
        if not a["role"]:
            if a["running"] and not s.seen_phase and ph in ROLE_PHASE.values():
                s.seen_phase = ph
            a["role"] = s.seen_phase or "search"
        a["recent"] = a["running"] or (a["finished"] is not None and now - a["finished"] < 30)
    all_agents = [a for _, a in found if not task or a["hunt"] == task]
    keep = [a for a in all_agents if a["recent"]]
    rest = sorted((a for a in all_agents if not a["recent"] and a["finished"]), key=lambda a: -a["finished"])
    return sorted(keep + rest[:max(0, (6 if task else 4) - len(keep))], key=lambda a: a["started"])


def tasks(rows, found):
    """Each question the run has touched: its text, how many agents are on it now, and every scored search of it."""
    out = {}
    def task(name):
        return out.setdefault(name, {"name": name, "question": "", "running": 0, "searches": []})
    for _, a in found:
        if a["hunt"]:
            t = task(a["hunt"])
            t["question"], t["running"] = a["task"], t["running"] + a["running"]
    for r in rows:
        task(r["hunt"])["searches"].append({k: r.get(k) for k in ("method", "role", "round", "score", "correct", "wrong", "total", "spent")})
    return list(out.values())


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
                      "summary": head.get("micro_summary"), "t": born(d), "method": m.get("id") if m else None,
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


def task_searches(d, rows, task):
    """Every scored search of one question with the verdict on each answer it handed in and the answers it missed."""
    out = []
    for r in rows:
        if r["hunt"] != task:
            continue
        ref = (read_json(d / "logs" / f"{r['attempt_id']}.json") or {}).get("referee") or {}
        out.append({**{k: r.get(k) for k in ("attempt_id", "method", "role", "round", "score", "correct", "wrong", "total")},
                    "answers": [{k: a.get(k) for k in ("name", "status", "reason", "url")} for a in ref.get("rows") or []],
                    "missed": ref.get("missed") or []})
    return out


def baseline(name, rows, task):
    """The starting method's mean score on one question: from this run if it searched it, else the latest run that did."""
    for run_rows in [rows, *(read_rows(RUNS / r / "attempts.jsonl") for r in runs_by_recency() if r != name)]:
        scores = [r["score"] for r in run_rows if r.get("hunt") == task and r.get("method") == "v000"]
        if scores:
            return round(sum(scores) / len(scores), 4)
    return None


def snapshot(name, task=None):
    d = RUNS / name
    logs = d / "logs"
    rows, errors = read_rows(d / "attempts.jsonl"), read_rows(d / "errors.jsonl")
    methods = [m for m in (read_json(p) for p in sorted((d / "methods").glob("*.json"))) if m] if (d / "methods").exists() else []
    state = read_json(d / "state.json")
    nodes = tree_nodes(d, methods)
    found = agents(d, rows)
    ph, rnd = phase(state, nodes, rows, errors, methods, any(a["running"] for _, a in found))
    return {
        "name": name, "phase": ph, "iteration": rnd, "state": state, "agents": shown(found, ph, time.time(), task), "nodes": nodes,
        "runs": runs_by_recency(), "tasks": tasks(rows, found), "task": task,
        "task_searches": task_searches(d, rows, task) if task else None, "baseline": baseline(name, rows, task) if task else None,
        "methods": [{k: m.get(k) for k in ("id", "parent", "round", "status", "select_score")} for m in methods],
        "spend": round(sum(r.get("spent") or 0 for r in rows), 3), "searches_done": len(rows), "failed": len(errors),
        "last_error": (errors[-1].get("error") or "")[:300] if errors else None,
    }


def runs_by_recency():
    runs = [p for p in RUNS.iterdir() if p.is_dir()] if RUNS.exists() else []
    def changed(p):
        return max((f.stat().st_mtime for f in [p, *p.glob("*"), *(p / "logs").glob("*")]), default=0)
    return [p.name for p in sorted(runs, key=changed, reverse=True)]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/run":
            q = parse_qs(u.query)
            name = (q.get("name") or [""])[0] or next(iter(runs_by_recency()), None)
            if not name or "/" in name or not (RUNS / name).is_dir():
                return self.send(json.dumps({"name": None}), "application/json")
            self.send(json.dumps(snapshot(name, (q.get("task") or [""])[0] or None)), "application/json")
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
