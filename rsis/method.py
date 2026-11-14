import json
import time

from .config import ROOT

SEED = ROOT / "methods"


def path(run_dir, mid):
    return run_dir / "methods" / f"{mid}.json"


def load(run_dir, mid):
    return json.loads(path(run_dir, mid).read_text(encoding="utf-8"))


def save(run_dir, m):
    p = path(run_dir, m["id"])
    p.parent.mkdir(parents=True, exist_ok=True)
    m.setdefault("created", time.strftime("%Y-%m-%dT%H:%M:%S"))
    p.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    return m


def all_methods(run_dir):
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((run_dir / "methods").glob("*.json"))]


def next_id(run_dir):
    return f"v{len(list((run_dir / 'methods').glob('*.json'))):03d}"


def render(m):
    """The method as the searcher sees it."""
    r = m["routing"]
    default = "Telem auto-routing (accuracy)" if r.get("auto_routing") else f"providers {r.get('providers')}"
    return (f"## Search method {m['id']}\n\n{m['instructions']}\n\n### Routing policy\n"
            f"Default route: {default}, tier {r.get('tier', 'default')}, {r.get('num_results', 8)} results per provider.\n"
            f"check_candidates route: {r.get('verify_providers') or 'same as default'}.\n"
            f"{m.get('routing_rules', '')}\n\n### Fetch policy\n{m.get('fetch_policy', '')}")
