"""Referee evidence through Telem pinned to Tavily; no separate Tavily credential."""
import threading

from .telem import Telem

credits_used = 0
_lock = threading.Lock()


def search(query, max_results=5, include_answer=True, exclude_domains=None):
    global credits_used
    r = Telem(1.0).search(query, providers=["tavily"], num_results=max_results)
    if r.get("error"):
        raise RuntimeError(r["error"])
    with _lock:
        credits_used += 1
    return {"answer": "", "results": [{"title": x["title"], "content": x["summary"], "url": x["url"]}
                                      for x in r["results"]]}
