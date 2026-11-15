---
id: "caf3eda0-04d1-4465-9b8e-1e0800b11d4c"
name: "Check Parallel Browser-Harness Sessions on Headless CDP"
micro_summary: "Try isolated harness connections to establish whether page-reading sessions can run side by side."
status: "resolved"
kind: "Probe"
see_also: []
position: 1024
---
## Creation

Jack asked whether headless Chrome actually exposed browser-harness CDP and how the assistant had verified it. The assistant corrected its earlier evidence: its initial 3-second Minor Planet Center check used Chrome `--dump-dom`, no CDP and no harness, so it did not establish interactive iteration or concurrency.

## Completion and observations

A later explicit probe started two headless Chromes on ports 9411 and 9412 with separate temporary profiles and invoked `python -m browser_harness.run` through uv against the source checkout. Each received its own BU_CDP_URL and BU_NAME. A first shared BH_TMP_DIR caused both invocations to reach one daemon and a “No target with given id found” failure. Distinct BH_TMP_DIR values fixed that collision. One harness session read asteroid 300909 (Ken Thompson) in 2.9 seconds and the other 21656 (Knuth) in 3.7 seconds; both finished in four seconds total.

The normal installed wrapper strips the direct-CDP environment, so this probe invoked the source module, not that wrapper. It demonstrated two independent harness page reads, not four simultaneous complete LLM verifications or reliable Google search in headless Chrome. The subsequent judge work supplied the real Pi integration. Telem remained the discovery tool; no independent Google-blocking trial was established here. Cleanup killed the probe Chromes and included a broad browser_harness.daemon pkill; the assistant disclosed that it could also have stopped an unrelated daemon. That broad cleanup is an incident, not a recommended procedure.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
