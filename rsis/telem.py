import os
import threading
from urllib.parse import urlparse

from .config import REFEREE_DOMAINS
from .http import post_json

BASE = os.environ.get("TELEM_BASE_URL", "https://router.telem.ai").rstrip("/")

# Dollars per search call, from docs.telem.ai/pricing (Nov 14 2026). Exa varies; 0.007 is our estimate.
SEARCH_PRICE = {"brave": 0.005, "ceramic": 0.00005, "linkup": 0.005, "parallel": 0.001, "perplexity": 0.005,
                "seltz": 0.005, "serpapi": 0.006, "tavily": 0.005, "you": 0.005, "tinyfish": 0.0, "exa": 0.007}
EXTENDED_SURCHARGE = {"tavily": 0.005, "parallel": 0.004}
FETCH_PRICE = 0.001
PROVIDERS = sorted(SEARCH_PRICE)


def url_key(url):
    u = (url or "").strip().lower().split("#")[0]
    for pre in ("https://", "http://"):
        u = u.removeprefix(pre)
    return u.removeprefix("www.").rstrip("/")


def blocked(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in REFEREE_DOMAINS)


class Telem:
    """One Telem session per attempt, with a dollar ledger and per-provider attribution."""

    def __init__(self, budget):
        self.key = os.environ["TELEM_API_KEY"]
        self.budget = budget
        self.spent = 0.0
        self.session_id = None
        self.calls = []
        self.url_providers = {}
        self.url_text = {}
        self.lock = threading.Lock()

    def _post(self, path, body):
        if self.session_id:
            body["session_id"] = self.session_id
        r = post_json(BASE + path, body, {"Authorization": f"Bearer {self.key}"})
        self.session_id = r.get("session_id") or self.session_id
        return r

    def search(self, query, providers=None, also=None, auto_routing=False, tier="default", num_results=8,
               include_domains=None, published_after=None, published_before=None):
        if self.spent >= self.budget:
            return {"error": "budget exhausted", "results": []}
        s = {"tier": tier, "num_results": num_results}
        if auto_routing:
            s["auto_routing"] = "accuracy"
        if providers:
            s["providers"] = {"include": providers}
        if include_domains:
            s["include_domains"] = include_domains
        if published_after:
            s["published_after"] = published_after
        if published_before:
            s["published_before"] = published_before
        queries = [query, *(also or [])][:5]
        per_query = sum(SEARCH_PRICE.get(p, 0.005) for p in providers) if providers else 0.010
        if tier in ("extended", "max"):
            per_query += sum(EXTENDED_SURCHARGE.get(p, 0) for p in (providers or []))
        affordable = int((self.budget - self.spent) // per_query) if per_query else len(queries)
        if affordable < 1:
            return {"error": "budget exhausted", "results": [], "budget_left": round(self.budget - self.spent, 4)}
        queries = queries[:affordable]
        query = queries[0]
        user_input = {"query": query} if len(queries) == 1 else [{"query": q} for q in queries]
        r = self._post("/v1/search", {"user_input": user_input, "search": s})
        results, used, dropped = [], [], 0
        cost = 0.0
        for run in r.get("preprocessor_runs", []):
            p = run.get("preprocessor_name", "?")
            if run.get("error"):
                continue
            used.append(p)
            cost += SEARCH_PRICE.get(p, 0.005) + (EXTENDED_SURCHARGE.get(p, 0) if tier in ("extended", "max") else 0)
            for res in (run.get("output_payload") or {}).get("results", []):
                url = res.get("url", "")
                if blocked(url):
                    dropped += 1
                    continue
                if not url:
                    continue
                with self.lock:
                    self.url_providers.setdefault(url, set()).add(p)
                    if len(self.url_text.get(url, "")) < 4000:
                        self.url_text[url] = (self.url_text.get(url, "") + " " + (res.get("title") or "") + " "
                                              + (res.get("summary") or res.get("excerpt") or "")[:400])
                results.append({"provider": p, "query": run.get("query"), "rank": res.get("rank"), "url": url, "title": res.get("title"),
                                "summary": (res.get("summary") or res.get("excerpt") or "")[:400]})
        with self.lock:
            self.spent += cost
        self.calls.append({"kind": "search", "query": queries, "requested": providers, "auto_routing": auto_routing,
                           "routing": r.get("routing"), "used": used, "n": len(results), "dropped_referee": dropped,
                           "cost": round(cost, 5), "include_domains": include_domains})
        return {"results": results, "providers_used": used, "cost": round(cost, 5),
                "budget_left": round(self.budget - self.spent, 4)}

    def fetch(self, urls, max_chars=30000):
        urls = [u for u in urls if not blocked(u)][:5]
        if not urls:
            return {"pages": []}
        if self.spent >= self.budget:
            return {"error": "budget exhausted", "pages": []}
        r = self._post("/v1/fetch", {"urls": urls, "options": {"tier": "default"}})
        pages = []
        for run in r.get("preprocessor_runs", []):
            for f in (run.get("output_payload") or {}).get("fetched_results", []):
                if f.get("content"):
                    with self.lock:
                        self.url_providers.setdefault(f.get("url"), set()).add("fetch:" + str(f.get("provider")))
                        self.url_text[f.get("url")] = self.url_text.get(f.get("url"), "") + " " + f["content"][:max_chars]
                pages.append({"url": f.get("url"), "status": f.get("status"), "provider": f.get("provider"),
                              "content": (f.get("content") or "")[:max_chars]})
        cost = FETCH_PRICE * len(urls)
        with self.lock:
            self.spent += cost
        self.calls.append({"kind": "fetch", "urls": urls, "ok": sum(p["content"] != "" for p in pages), "cost": cost})
        return {"pages": pages, "budget_left": round(self.budget - self.spent, 4)}
