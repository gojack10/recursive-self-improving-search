import json
import re
import math
import uuid
from collections import Counter

from .history import append, tokens


class Tree:
    """Agent-written nodes in the SiftText node.md layout, kept apart from the synced nodes/ tree."""

    def __init__(self, run_dir):
        self.dir = run_dir / "tree" / "nodes"
        self.dir.mkdir(parents=True, exist_ok=True)

    def write(self, kind, name, summary, body, parent=None, status="in_progress", see_also=()):
        nid = str(uuid.uuid4())
        d = self.dir / nid
        (d / "children").mkdir(parents=True)
        front = {"id": nid, "name": name, "micro_summary": summary, "status": status, "kind": kind,
                 "see_also": [{"target": t, "reason": r} for t, r in see_also]}
        text = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in front.items()) + "---\n"
        (d / "node.md").write_text(text + f"**Kind:** {kind}\n\n{body}\n", encoding="utf-8")
        if parent:
            (self.dir / parent / "children" / nid).write_text("", encoding="utf-8")
        self.record(event="write", id=nid, kind=kind, name=name, summary=summary, status=status, parent=parent)
        return nid

    def record(self, **event):
        """Tree changes in the order they happened; node files only hold the latest state."""
        append(self.dir.parent.parent, "tree_events.jsonl", event)

    def nodes(self):
        out = []
        for p in self.dir.glob("*/node.md"):
            text = p.read_text(encoding="utf-8")
            front = text.split("\n---\n", 1)[0].removeprefix("---\n")
            head = dict(l.split(": ", 1) for l in front.split("\n") if ": " in l)
            out.append({"id": json.loads(head["id"]), "name": json.loads(head["name"]), "kind": json.loads(head["kind"]),
                        "summary": json.loads(head["micro_summary"]), "status": json.loads(head["status"]), "text": text})
        return out

    def search(self, query, k=6, kinds=None, allowed=None):
        """BM25 over node text. Returns outline cards; read() opens one."""
        docs = [n for n in self.nodes() if (not kinds or n["kind"] in kinds) and (allowed is None or n["id"] in allowed)]
        if not docs:
            return []
        toks = [tokens(n["text"]) for n in docs]
        avg = sum(map(len, toks)) / len(toks)
        df = Counter(t for ts in toks for t in set(ts))
        q = tokens(query)
        scored = []
        for n, ts in zip(docs, toks):
            tf = Counter(ts)
            s = sum(math.log(1 + (len(docs) - df[t] + 0.5) / (df[t] + 0.5)) * tf[t] * 2.2 /
                    (tf[t] + 1.2 * (0.25 + 0.75 * len(ts) / avg)) for t in q if tf[t])
            scored.append((s, n))
        scored.sort(key=lambda x: -x[0])
        return [{"id": n["id"], "kind": n["kind"], "name": n["name"], "summary": n["summary"], "status": n["status"]}
                for s, n in scored[:k] if s > 0]

    def exists(self, nid):
        # Node ids come from model output; only plain UUIDs may name a path, so nothing escapes the run's tree.
        uuid_like = isinstance(nid, str) and re.fullmatch(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}", nid)
        return bool(uuid_like) and (self.dir / nid / "node.md").exists()

    def read(self, nid, max_round=None):
        if not self.exists(nid):
            return "no such node"
        p = self.dir / nid / "node.md"
        text = p.read_text(encoding="utf-8")
        if max_round is not None:
            text = "\n".join(l for l in text.split("\n")
                             if not (re.match(r"- Round (\d+):", l) and int(re.match(r"- Round (\d+):", l)[1]) > max_round))
        return text

    def set_status(self, nid, status):
        if not self.exists(nid):
            return
        p = self.dir / nid / "node.md"
        t = p.read_text(encoding="utf-8")
        old = next(l for l in t.splitlines() if l.startswith("status: "))
        p.write_text(t.replace(old, f"status: {json.dumps(status)}", 1), encoding="utf-8")
        self.record(event="status", id=nid, status=status)

    def append(self, nid, section):
        if not self.exists(nid):
            return
        p = self.dir / nid / "node.md"
        p.write_text(p.read_text(encoding="utf-8") + "\n" + section + "\n", encoding="utf-8")
