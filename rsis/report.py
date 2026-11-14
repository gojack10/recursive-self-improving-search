import html
import json

from . import history as H
from . import method as M
from .loop import run_dir, state


def line_chart(points, baseline, w=640, h=240):
    if not points:
        return "<p>No rounds yet.</p>"
    xs = [p["round"] for p in points]
    top = max([p["test"] for p in points] + [baseline or 0, 0.1]) * 1.15
    sx = lambda x: 40 + (x - min(xs)) * (w - 60) / max(1, max(xs) - min(xs))
    sy = lambda y: h - 30 - y * (h - 50) / top
    path = " ".join(f"{'M' if i == 0 else 'L'}{sx(p['round']):.1f},{sy(p['test']):.1f}" for i, p in enumerate(points))
    dots = "".join(f'<circle cx="{sx(p["round"]):.1f}" cy="{sy(p["test"]):.1f}" r="4" class="{"adopt" if p["adopted"] else "keep"}">'
                   f'<title>round {p["round"]}: {p["method"]} test {p["test"]}</title></circle>' for p in points)
    base = (f'<line x1="40" x2="{w - 20}" y1="{sy(baseline):.1f}" y2="{sy(baseline):.1f}" class="base"/>'
            f'<text x="{w - 20}" y="{sy(baseline) - 6:.1f}" text-anchor="end" class="lbl">v000 (Telem auto-routing) {baseline}</text>'
            if baseline is not None else "")
    ticks = "".join(f'<text x="{sx(x):.1f}" y="{h - 10}" text-anchor="middle" class="lbl">{x}</text>' for x in xs)
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Held-out test score by round">'
            f'<line x1="40" x2="{w - 20}" y1="{h - 30}" y2="{h - 30}" class="axis"/>{base}'
            f'<path d="{path}" class="ln"/>{dots}{ticks}</svg>')


def bars(rows):
    if not rows:
        return "<p>Not run yet.</p>"
    top = max(r["score"] for r in rows) or 1
    return "".join(f'<div class="bar"><span>{html.escape(r["generation"])}</span><i style="width:{100 * r["score"] / top:.0f}%"></i>'
                   f'<b>{r["score"]:.3f}</b></div>' for r in rows)


def write(name):
    d = run_dir(name)
    s = state(d)
    if s is None:
        return f"no run named {name}"
    methods = M.all_methods(d)
    py = H.provider_yield(d)
    attempts = H.rows(d, "attempts.jsonl")
    rt = H.rows(d, "recursion_test.jsonl")
    cmp = H.rows(run_dir("compare"), "compare.jsonl")
    cmp_rows = "".join(f"<tr><td>{c['contestant']}</td><td>{c['score']:.3f}</td><td>{c['correct']}</td><td>{c['wrong']}</td>"
                       f"<td>{c['x_only']}</td><td>{c['y_only']}</td><td>${c['spend']:.3f}</td></tr>" for c in (cmp[-1]["summary"] if cmp else []))
    spend = sum(r["spent"] for r in attempts)
    yield_rows = "".join(f"<tr><td>{p}</td><td>{v['searches']}</td><td>${v['spend']:.3f}</td><td>{v['results']}</td>"
                         f"<td>{v['correct_finds']}</td><td>{v['wrong_finds']}</td><td>{v['correct_per_dollar']}</td></tr>"
                         for p, v in py.items())
    lineage = "".join(
        f"<tr class='{m.get('status')}'><td>{m['id']}</td><td>{m.get('parent') or ''}</td><td>{m.get('status')}</td>"
        f"<td>{m.get('select_score', '')}</td><td>{html.escape(json.dumps(m['routing']))}</td>"
        f"<td>{html.escape(str(m.get('rationale') or '')[:240])}</td></tr>" for m in methods)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Recursive Search Run</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--acc:#2f6fdb;--ok:#2e8b57;--line:#ddd9d0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--fg:#ecebe6;--mut:#a3a19a;--acc:#7aa7ff;--ok:#62c48f;--line:#38372f}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:980px;margin:0 auto;padding:24px 16px}}
h1{{font-size:1.5rem}} h2{{font-size:1.1rem;margin-top:2rem}} .mut{{color:var(--mut)}}
table{{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow-x:auto}} td,th{{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}}
svg{{width:100%;height:auto}} .ln{{fill:none;stroke:var(--acc);stroke-width:2}} .axis{{stroke:var(--line)}} .base{{stroke:var(--mut);stroke-dasharray:4 4}}
.lbl{{fill:var(--mut);font-size:11px}} circle.adopt{{fill:var(--ok)}} circle.keep{{fill:var(--acc)}}
.bar{{display:flex;gap:8px;align-items:center;margin:4px 0}} .bar span{{width:90px}} .bar i{{height:14px;background:var(--acc);display:block}}
.kpi{{display:flex;gap:24px;flex-wrap:wrap}} .kpi div b{{display:block;font-size:1.4rem}}
tr.discarded td{{color:var(--mut)}}
</style></head><body>
<h1>Recursive self-improving search: run "{html.escape(name)}"</h1>
<p class="mut">Searchers and the improver route every web call through Telem. A Wikidata referee scores finds; Tavily independently checks finds Wikidata lacks.</p>
<div class="kpi"><div><b>{s['round']}</b>rounds</div><div><b>{s['current']}</b>current method</div>
<div><b>{s.get('baseline_test')}</b>baseline test</div><div><b>{s['best_test']}</b>best test</div>
<div><b>{s['noise']}</b>noise band</div><div><b>${spend:.2f}</b>Telem spend (searchers)</div><div><b>{len(attempts)}</b>attempts</div></div>
<h2>Held-out test score of each round's winner</h2>{line_chart(s['test_points'], s.get('baseline_test'))}
<h2>Recursion test: same improvement job, improver searching with generation N's method</h2>{bars(rt[-1]['results'] if rt else [])}
<h2>Against a frontier model (same hunts, same referee)</h2>
<table><tr><th>contestant</th><th>score</th><th>correct</th><th>wrong</th><th>x only</th><th>y only</th><th>Telem spend</th></tr>{cmp_rows or "<tr><td>Run python -m rsis compare</td></tr>"}</table>
<h2>Telem provider yield</h2><table><tr><th>provider</th><th>searches</th><th>spend</th><th>results</th><th>correct finds</th><th>wrong finds</th><th>correct per $</th></tr>{yield_rows}</table>
<h2>Method lineage</h2><table><tr><th>id</th><th>parent</th><th>status</th><th>select</th><th>routing</th><th>rationale</th></tr>{lineage}</table>
</body></html>"""
    out = d / "report.html"
    out.write_text(page, encoding="utf-8")
    return out
