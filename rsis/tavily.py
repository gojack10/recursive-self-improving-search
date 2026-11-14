"""Referee evidence through Telem pinned to Tavily; no separate Tavily credential."""
import os
import threading

from .telem import Telem

credits_used = 0
CREDIT_CAP = int(os.environ.get("TAVILY_CREDIT_CAP", "3000"))
_lock = threading.Lock()


def search(query, max_results=5, include_answer=True, exclude_domains=None):
    global credits_used
    with _lock:
        if credits_used >= CREDIT_CAP:
            raise RuntimeError(f"Tavily credit cap {CREDIT_CAP} reached for this process")
        credits_used += 1
    r = Telem(1.0).search(query, providers=["tavily"], num_results=max_results)
    if r.get("error"):
        raise RuntimeError(r["error"])
    return {"answer": "", "results": [{"title": x["title"], "content": x["summary"], "url": x["url"]}
                                      for x in r["results"]]}
