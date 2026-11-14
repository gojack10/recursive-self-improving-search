import json
import time

from .config import role
from .http import post_json


class Chat:
    def __init__(self, role_name):
        self.cfg = role(role_name)
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    def complete(self, messages, tools=None, json_mode=False, force=None):
        body = {"model": self.cfg["model"], "messages": messages}
        if tools:
            body["tools"] = tools
        if force:
            body["tool_choice"] = {"type": "function", "function": {"name": force}}
        if self.cfg["effort"]:
            body["reasoning_effort"] = self.cfg["effort"]
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        for i in range(3):
            r = post_json(self.cfg["base_url"].rstrip("/") + "/chat/completions", body,
                          {"Authorization": f"Bearer {self.cfg['api_key']}"}, timeout=300)
            if r.get("choices"):
                break
            time.sleep(2 ** i * 2)
        else:
            raise RuntimeError(f"no choices from {self.cfg['model']}: {str(r)[:300]}")
        for k in self.usage:
            self.usage[k] += (r.get("usage") or {}).get(k, 0)
        return r["choices"][0]["message"]

    def json(self, system, user):
        msg = self.complete([{"role": "system", "content": system}, {"role": "user", "content": user}], json_mode=True)
        return parse_obj(msg.get("content"))


def parse_obj(text):
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
