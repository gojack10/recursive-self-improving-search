import http.client
import json
import time
import urllib.error
import urllib.request


def post_json(url, body, headers, timeout=120, retries=3):
    data = json.dumps(body).encode()
    h = {"Content-Type": "application/json", **headers}
    for i in range(retries):
        req = urllib.request.Request(url, data=data, headers=h, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(2 ** i * 2)
                continue
            raise RuntimeError(f"{url} -> HTTP {e.code}: {msg}") from None
        except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError, OSError, ValueError):
            if i < retries - 1:
                time.sleep(2 ** i * 2)
                continue
            raise
