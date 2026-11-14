import json
import time

from .config import role
from .http import post_json


class Chat:
    def __init__(self, role_name):
        self.cfg = role(role_name)
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    def complete(self, messages, tools=None, json_mode=False, force=None):
        if self.cfg["model"].startswith("pi:"):
            return self.complete_through_pi(messages, tools)
        body = {"model": self.cfg["model"], "messages": messages}
        if tools:
            body["tools"] = tools
        if self.cfg["effort"]:
            body["reasoning_effort"] = self.cfg["effort"]
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        if force:
            # Some endpoints reject a forced function choice; fall back to the unforced call.
            try:
                return self._send({**body, "tool_choice": {"type": "function", "function": {"name": force}}})
            except RuntimeError:
                pass
        return self._send(body)

    def _send(self, body):
        for i in range(3):
            r = post_json(self.cfg["base_url"].rstrip("/") + "/chat/completions", body,
                          {"Authorization": f"Bearer {self.cfg['api_key']}"}, timeout=300)
            if r.get("choices"):
                break
            time.sleep(2 ** i * 2)
        else:
            raise RuntimeError(f"no choices from {self.cfg['model']}: {str(r)[:300]}")
        for k in self.usage:
            self.usage[k] += ((r.get("usage") or {}).get(k) or 0)
        return r["choices"][0]["message"]

    def complete_through_pi(self, messages, tools):
        """A role whose model is 'pi:<provider>/<id>' answers through headless Pi instead of an API key."""
        if tools:
            raise RuntimeError("tool-calling roles run as Pi agents (rsis.pi_searcher), not through Chat")
        from . import pi
        model = self.cfg["model"][3:] + (f":{self.cfg['effort']}" if self.cfg["effort"] else "")
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        prompt = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
        return {"content": pi.complete(model, system, prompt)}

    def json(self, system, user):
        msg = self.complete([{"role": "system", "content": system}, {"role": "user", "content": user}], json_mode=True)
        return parse_obj(msg.get("content"))


def parse_obj(text):
    if isinstance(text, dict):
        return text
    text = text or ""
    start, end = text.find("{"), text.rfind("}")
    try:
        v = json.loads(text[start:end + 1])
    except ValueError:
        return {}
    return v if isinstance(v, dict) else {}


def tool(name, description, properties, required):
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": properties, "required": required}}}
