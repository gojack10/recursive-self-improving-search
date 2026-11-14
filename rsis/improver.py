import json

from . import history as H
from . import method as M
from .llm import Chat, parse_obj, tool
from .searcher import SEARCH_TOOL, run_search
from .telem import Telem

MAX_TURNS = 24
IMPROVER_BUDGET = 0.10

HIST_TOOL = tool("search_history", "Search the tree of past method versions, lessons, failures and trial rounds. Returns outline cards.",
                 {"query": {"type": "string"}, "kinds": {"type": "array", "items": {"type": "string"}}}, ["query"])
READ_TOOL = tool("read_node", "Open one node from search_history in full.", {"id": {"type": "string"}}, ["id"])
LOG_TOOL = tool("read_attempt", "Open one attempt log: its searches, routes, spend, finds, and the referee's verdicts.",
                {"attempt_id": {"type": "string"}}, ["attempt_id"])
PROPOSE_TOOL = tool("propose", "Finish: record lessons, link repeated failures to existing nodes, and propose candidate methods.", {
    "lessons": {"type": "array", "items": {"type": "object", "properties": {
        "title": {"type": "string"}, "body": {"type": "string"}, "scope": {"type": "string"},
        "evidence_attempts": {"type": "array", "items": {"type": "string"}}}, "required": ["title", "body", "scope"]}},
    "failure_links": {"type": "array", "items": {"type": "object", "properties": {
        "attempt_id": {"type": "string"}, "node_id": {"type": "string"}, "why": {"type": "string"}}}},
    "candidates": {"type": "array", "items": {"type": "object", "properties": {
        "rationale": {"type": "string"}, "instructions": {"type": "string"},
        "routing": {"type": "object", "properties": {
            "auto_routing": {"type": "boolean"}, "providers": {"type": "array", "items": {"type": "string"}},
            "tier": {"type": "string"}, "num_results": {"type": "integer"},
            "verify_providers": {"type": "array", "items": {"type": "string"}}}},
        "routing_rules": {"type": "string"}, "fetch_policy": {"type": "string"}},
        "required": ["rationale", "instructions", "routing", "routing_rules", "fetch_policy"]}}},
    ["lessons", "candidates"])

SYSTEM = """You improve a web search method. Searchers follow the method on open hunts ("find every X"); a referee scores
verified finds and penalizes wrong ones. Your job is to write {k} candidate successor methods that will find more on
hunts nobody has seen yet, at the same Telem budget. Candidates must be general tactics, not answers to past hunts.

The method controls the searcher's instructions and its routing across Telem's providers (which engines, auto-routing,
tier, results per provider, domain and date filters, when to fetch, and which providers check_candidates uses).
Every hunt is "items that meet condition X and condition Y". Searchers can enumerate one side and verify the other
with check_candidates; which side to anchor on, and how to route each phase, are part of the method. Provider spend comes out of a fixed budget, so a
cheaper route buys more searches. Use the provider yield table: it attributes each correct find to the providers that
surfaced its evidence.

You search the same way the searchers do: use YOUR search method below when you search the history tree and the web
for better techniques. A failure that matches an existing failure or lesson node should be linked to that node with
failure_links instead of written again as a new lesson.

{method}

Make the candidates differ from each other in a meaningful way. Call propose when done."""


def context(run_dir, start, attempt_ids, extra="", as_of_round=None):
    """What the improver sees. as_of_round freezes the view, so every recursion-test generation gets the same job."""
    def visible(r):
        return r.get("role") != "rtest" and (as_of_round is None or (r.get("round") or 0) <= as_of_round)
    rows = [r for r in H.rows(run_dir, "attempts.jsonl") if visible(r)]
    scores = H.method_scores(rows)
    methods = [m for m in M.all_methods(run_dir) if m.get("status") != "recursion-test"
               and (as_of_round is None or (m.get("round") or 0) <= as_of_round)]
    lineage = "\n".join(f"- {m['id']} (parent {m.get('parent')}, {m.get('status', 'seed')}): {m['rationale'][:200]} "
                        f"scores={scores.get(m['id'], {})}" for m in methods)
    att = [r for r in rows if r["attempt_id"] in attempt_ids]
    return (f"Method to improve:\n```json\n{json.dumps(start, indent=1)}\n```\n\nLineage so far:\n{lineage}\n\n"
            f"Provider yield:\n```json\n{json.dumps(H.provider_yield(run_dir, rows), indent=1)}\n```\n\n"
            f"Attempts you may open with read_attempt (train hunts only):\n"
            + "\n".join(json.dumps({k: r[k] for k in ('attempt_id', 'method', 'hunt', 'kind', 'score', 'correct', 'wrong',
                                                         'total', 'x_only', 'y_only', 'spent', 'searches', 'fetches') if k in r}) for r in att)
            + "\n\nx_only / y_only count wrong finds that met only one of the hunt's two conditions." + extra)


def improve(run_dir, tree, start, search_method, attempt_ids, k=2, role="improver", extra="",
            as_of_round=None, allowed_nodes=None):
    """Write k candidates from `start`, searching with `search_method`. In normal rounds both are the current method;
    the recursion test holds `start` fixed and varies `search_method` across generations."""
    chat = Chat(role)
    telem = Telem(IMPROVER_BUDGET)
    messages = [{"role": "system", "content": SYSTEM.format(k=k, method=M.render(search_method))},
                {"role": "user", "content": context(run_dir, start, attempt_ids, extra, as_of_round)}]
    tools = [HIST_TOOL, READ_TOOL, LOG_TOOL, SEARCH_TOOL, PROPOSE_TOOL]
    trace = []
    for _ in range(MAX_TURNS):
        msg = chat.complete(messages, tools=tools)
        messages.append({**msg, "role": "assistant", "content": msg.get("content") or ""})
        calls = msg.get("tool_calls") or []
        if not calls:
            messages.append({"role": "user", "content": "Call propose now."})
            continue
        for c in calls:
            name = c["function"]["name"]
            args = parse_obj(c["function"].get("arguments"))
            trace.append({"tool": name, "args": args if name != "propose" else "..."})
            if name == "propose" and args.get("candidates"):
                return args, {"trace": trace, "telem_spent": telem.spent, "telem_session": telem.session_id,
                              "tokens": chat.usage}
            try:
                if name == "propose":
                    out = {"error": "propose needs at least one candidate"}
                elif name == "search_history":
                    out = tree.search(args.get("query", ""), kinds=args.get("kinds"), allowed=allowed_nodes)
                elif name == "read_node":
                    nid = args.get("id", "")
                    out = tree.read(nid)[:6000] if allowed_nodes is None or nid in allowed_nodes else "not available"
                elif name == "read_attempt":
                    if args.get("attempt_id") not in attempt_ids:
                        out = "not available"
                    else:
                        log = H.load_log(run_dir, args["attempt_id"])
                        ref = log.get("referee", {})
                        out = {"hunt": log["hunt"], "notes": log["notes"], "trace": log["trace"][:40],
                               "telem_calls": log["telem_calls"][:40], "spent": log["telem_spent"],
                               "conditions": {"x": log.get("x"), "y": log.get("y")},
                               "verdicts": [{kk: r.get(kk) for kk in ("name", "status", "half", "providers")} for r in ref.get("rows", [])],
                               "missed_count": len(ref.get("missed", []))}
                elif name == "web_search":
                    out = run_search(search_method, args.pop("query", "") or "search tactics for exhaustive list finding", args, telem)
                else:
                    out = {"error": f"unknown tool {name}"}
            except Exception as e:
                out = {"error": str(e)[:500]}
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(out, ensure_ascii=False)[:12000]})
    raise RuntimeError("improver did not propose")
