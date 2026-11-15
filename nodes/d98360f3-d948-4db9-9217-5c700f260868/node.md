---
id: "d98360f3-d948-4db9-9217-5c700f260868"
name: "Judge Live Answers With Astra and Iterative Browsing"
micro_summary: "Check each distinct live answer against pages an Astra opens in its own headless browser."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target": "1347dcde-fa33-4933-9769-8d9386808b21", "reason": "decided from the evidence-gate and snippet limitations exposed by the first live comparison."}]
position: 2048
---
## Creation

Jack challenged the snippet evidence, proposed one Astra per answer with “verify if X is correct,” and asked that similar names around 90% count as the same item. He then clarified that a single headless DOM dump was insufficient: the LLM must iterate through browser-harness on a headless Chrome’s CDP connection. His explicit build authorization was “ok well make it work as an iteration on our porject so astras really judge this shit for real yes build.”

## Completion — Ask-only judge

`rsis/browser.py` manages four headless Chromes by default (`JUDGE_BROWSERS`), with distinct debugging ports starting at 9411 and separate profiles and harness scratch directories under `/tmp/rsis-judge`. `rsis/browser_judge.py` runs the configured judge role through Pi: GPT-6 Astra at medium effort in the observed local configuration. It has web_search, open_page, browser and verdict tools; the browser tool can run harness Python to inspect and interact. Telem/Tavily finds candidate URLs; browser-harness reads real pages. The source checkout defaults to `~/projects/browser-harness` (`BROWSER_HARNESS`), with its `.venv/bin/python`; this bypasses the normal everyday-Chrome wrapper. Chrome and this separate checkout are local prerequisites.

The prompt treats exactly one submitted item as a membership claim, not an attempted complete list. Snippets and model memory are leads, never proof. It requires opened-page evidence for every membership fact, and asks for yes, no or unsure with a quoted reason and proof URL. Yes/no submission checks that the proof URL was opened; it does not independently machine-validate the quote or all factual reasoning. Four judges work concurrently; extra answers wait. There is a 14-tool-call budget and a 420-second per-agent limit. Errors/non-submissions become unconfirmed, not wrong. Development exposed real prompt failures: early Astras wrongly rejected an item because it omitted other list members, and one run had a no-submission. The membership prompt was repaired and the server restarted; later rulings confirmed the submitted members. More browsing alone did not remove prompt error.

Shared in-process futures give the two methods one ruling for the same/sufficiently similar item. The existing name matcher accepts normalized variants at 0.9 similarity, with number checks; this is a heuristic, not entity-resolution proof. Cached reuse is in memory for this server process, not a persistent cross-restart verdict service. Per-side result JSON, Pi state/streams and judge Markdown are saved under the Ask directory. Re-judge drops the in-memory question rulings and runs new judges. The old snippet SQLite file is not the browser judge’s cache.

Each Markdown proof records one answer’s ruling, quoted sentence, proof page, searcher citation, configured judge and its action sequence. The Ask page renders this rather than a search-results page. The corpus scorer and prior benchmark scores remain separate. This completed local feature does not change the training loop’s judging or prove that all browser verdicts are correct.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
