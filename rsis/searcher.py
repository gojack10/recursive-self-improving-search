import json
import time
import uuid

from . import method as M
from .config import ATTEMPT_BUDGET
from .llm import Chat, parse_obj, tool
from .telem import PROVIDERS, Telem

MAX_TURNS = 30
MAX_RESULT_CHARS = 40000


def as_list(v):
    return [v] if isinstance(v, str) else list(v or [])


def fit(out):
    """Serialize a tool result within MAX_RESULT_CHARS as valid JSON, budget first, dropping the lowest-ranked rows."""
    out = {"budget_left": out.get("budget_left"), **out}
    text = json.dumps(out, ensure_ascii=False)
    rows = out.get("results")
    while len(text) > MAX_RESULT_CHARS and rows:
        rows.sort(key=lambda r: r.get("rank") or 0)
        del rows[max(1, len(rows) * 3 // 4) if len(rows) > 4 else len(rows) - 1:]
        text = json.dumps(out, ensure_ascii=False)
    checks = out.get("checks")
    while len(text) > MAX_RESULT_CHARS and checks and max(len(v) for v in checks.values() if isinstance(v, list)) > 1:
        for k, v in checks.items():
            if isinstance(v, list) and len(v) > 1:
                checks[k] = v[:-1]
        text = json.dumps(out, ensure_ascii=False)
    while len(text) > MAX_RESULT_CHARS and checks:
        for r in (v for v in checks.values() if isinstance(v, list)):
            for row in r:
                row["summary"] = (row.get("summary") or "")[:len(row.get("summary") or "") // 2]
        text = json.dumps(out, ensure_ascii=False)
        if all(not row.get("summary") for v in checks.values() if isinstance(v, list) for row in v):
            break
    return text if len(text) <= MAX_RESULT_CHARS else text[:MAX_RESULT_CHARS]

SEARCH_TOOL = tool("web_search", "Search the web through the Telem router. Omit providers to use the method's default route.", {
    "query": {"type": "string"},
    "also": {"type": "array", "items": {"type": "string"}, "maxItems": 4,
             "description": "Extra query variants run concurrently in the same Telem batch call. Each is billed per provider."},
    "providers": {"type": "array", "items": {"type": "string", "enum": PROVIDERS},
                  "description": "Pin this search to these providers. Each provider is billed separately."},
    "auto_routing": {"type": "boolean", "description": "Let Telem choose providers for this query."},
    "tier": {"type": "string", "enum": ["minimalist", "default", "extended"]},
    "num_results": {"type": "integer", "minimum": 1, "maximum": 20},
    "include_domains": {"type": "array", "items": {"type": "string"}, "description": "Restrict to these host names."},
    "published_after": {"type": "string"}, "published_before": {"type": "string"}}, ["query"])
FETCH_TOOL = tool("fetch_pages", "Fetch full text of up to 5 URLs through Telem.", {
    "urls": {"type": "array", "items": {"type": "string"}}}, ["urls"])
CHECK_TOOL = tool("check_candidates",
    "Anchor-and-verify for 'X and Y' hunts: run one targeted search per candidate for the condition the candidate list "
    "does not already prove, batched through Telem. Returns the top results per candidate so you can keep or drop each.", {
    "candidates": {"type": "array", "items": {"type": "string"}, "maxItems": 25},
    "condition": {"type": "string", "description": "The condition to verify, phrased as search words, e.g. 'medical doctor MD'."},
    "providers": {"type": "array", "items": {"type": "string", "enum": PROVIDERS},
                  "description": "Omit to use the method's verify route. Cheap providers make wide checks affordable."},
    "per_candidate": {"type": "integer", "minimum": 1, "maximum": 5}}, ["candidates", "condition"])
SUBMIT_TOOL = tool("submit", "Submit your final list. Each find needs the URL that supports it. Wrong finds cost points.", {
    "finds": {"type": "array", "items": {"type": "object", "properties": {
        "name": {"type": "string"}, "evidence_url": {"type": "string"}}, "required": ["name", "evidence_url"]}},
    "notes": {"type": "string", "description": "What worked and what did not, in two or three sentences."}}, ["finds"])


def run_search(m, query, args, telem):
    r = m["routing"]
    providers = args.get("providers")
    auto = args.get("auto_routing", r.get("auto_routing") if not providers else False)
    return telem.search(query, also=as_list(args.get("also")), providers=providers or (None if auto else r.get("providers")), auto_routing=auto,
                        tier=args.get("tier", r.get("tier", "default")),
                        num_results=args.get("num_results", r.get("num_results", 8)),
                        include_domains=args.get("include_domains"),
                        published_after=args.get("published_after"), published_before=args.get("published_before"))


def check_candidates(m, args, telem):
    """One query per candidate, sent to Telem as batches of five. Results come back grouped by candidate."""
    r = m["routing"]
    providers = args.get("providers") or r.get("verify_providers") or r.get("providers")
    per = args.get("per_candidate", 2)
    queries = [f"{c} {args['condition']}" for c in as_list(args.get("candidates"))[:25]]
    grouped, budget_left = {}, None
    for i in range(0, len(queries), 5):
        chunk = queries[i:i + 5]
        try:
            out = telem.search(chunk[0], also=chunk[1:], providers=providers, auto_routing=not providers,
                               tier="default", num_results=per)
        except Exception as e:
            out = {"error": str(e)[:300]}
        if out.get("error"):
            grouped["_error"] = out["error"]
            break
        budget_left = out["budget_left"]
        for res in out["results"]:
            grouped.setdefault(res.get("query") or chunk[0], []).append(
                {k: res[k] for k in ("provider", "url", "title", "summary")})
    return {"checks": grouped, "budget_left": budget_left}


def attempt(m, hunt, budget=ATTEMPT_BUDGET, role="searcher"):
    """One agent's full try at one hunt. Returns the log; the referee scores it separately."""
    chat = Chat(role)
    telem = Telem(budget)
    system = (f"You are a web search agent working on an open hunt. Follow your search method.\n\n{M.render(m)}\n\n"
              f"You have ${budget:.2f} of Telem search budget. Every tool result reports what is left. "
              "When the budget runs out or you are done, call submit. Only submit items you have evidence for. "
              "Each find must cite a URL you retrieved in this attempt whose text, as you saw it, names the item; "
              "otherwise it scores as wrong.")
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": f"{hunt['question']}\n\nCondition X: {hunt['x']}\nCondition Y: {hunt['y']}"}]
    tools = [SEARCH_TOOL, FETCH_TOOL, CHECK_TOOL, SUBMIT_TOOL]
    trace, finds, notes = [], [], ""
    t0 = time.time()
    for turn in range(MAX_TURNS):
        last = turn >= MAX_TURNS - 2
        msg = chat.complete(messages, tools=[SUBMIT_TOOL] if last else tools, force="submit" if last else None)
        messages.append({**msg, "role": "assistant", "content": msg.get("content") or ""})
        calls = msg.get("tool_calls") or []
        if not calls:
            messages.append({"role": "user", "content": "Call submit with your finds now."})
            continue
        done = False
        for c in calls:
            name = c["function"]["name"]
            args = parse_obj(c["function"].get("arguments"))
            try:
                if name == "web_search":
                    out = run_search(m, args.pop("query", "") or hunt["question"], args, telem)
                elif name == "fetch_pages":
                    urls = as_list(args.get("urls"))[:5]
                    out = telem.fetch(urls, max_chars=MAX_RESULT_CHARS // max(1, len(urls)) - 500)
                elif name == "check_candidates":
                    out = check_candidates(m, args, telem)
                elif name == "submit":
                    if not isinstance(args.get("finds"), list) and not last:
                        out = {"error": "submit arguments did not parse; call submit again with a finds list"}
                    else:
                        finds = [f for f in as_list(args.get("finds")) if isinstance(f, dict)]
                        notes, done = args.get("notes", ""), True
                        out = {"ok": True}
                else:
                    out = {"error": f"unknown tool {name}"}
            except Exception as e:
                out = {"error": str(e)[:500]}
            trace.append({"tool": name, "args": args, "summary": {k: out[k] for k in out if k not in ("results", "pages", "checks")}})
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": fit(out)})
        if done:
            break
    return {"attempt_id": uuid.uuid4().hex[:10], "method": m["id"], "hunt": hunt["name"], "kind": hunt["kind"],
            "x": hunt["x"], "y": hunt["y"],
            "pool": hunt["pool"], "finds": finds, "notes": notes, "telem_calls": telem.calls,
            "telem_spent": round(telem.spent, 4), "telem_session": telem.session_id, "trace": trace,
            "url_providers": {u: sorted(p) for u, p in telem.url_providers.items()}, "url_text": telem.url_text,
            "seconds": round(time.time() - t0, 1), "tokens": chat.usage}
