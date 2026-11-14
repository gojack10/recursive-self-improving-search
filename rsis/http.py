import http.client
import json
import time
import urllib.error
import urllib.request


def post_json(url, body, headers, timeout=120, retries=3):
    """HTTP error statuses (rate limits, 5xx) are retried up to 3 times: the server answered, so nothing was billed.
    Network failures and timeouts are retried only `retries` times, since the request may have gone through."""
    data = json.dumps(body).encode()
    h = {"Content-Type": "application/json", **headers}
    net_failures = 0
    for i in range(max(retries, 3)):
        req = urllib.request.Request(url, data=data, headers=h, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and i < 2:
                time.sleep(2 ** i * 2)
                continue
            raise RuntimeError(f"{url} -> HTTP {e.code}: {msg}") from None
        except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError, OSError, ValueError):
            net_failures += 1
            if net_failures < retries:
                time.sleep(2 ** i * 2)
                continue
            raise
    raise RuntimeError(f"{url}: retries exhausted")
