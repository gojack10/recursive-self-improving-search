---
id: "46e25542-1842-409f-9e82-18df9310f863"
name: "Separate Run Trees From Search Traces"
micro_summary: "Distinguishes the run-local knowledge tree, live Pi search state and scored method iterations."
status: "resolved"
scope: "Explain what the November 14 viewer can faithfully show from the inspected code and what remains inferred."
see_also: []
position: 1024
---
**Kind:** What We Learned

## Creation — November 14, 2026

### Observed conditions
While requesting the visual debugger, Jack asked whether the current code really used SiftText trees and could run, with one tree growing down and another view growing right. The assistant inspected `rsis/tree.py`, `loop.py`, `improver.py`, the Pi searcher/tool bridge and the viewer on the `pi-searcher` checkout. The visual animation was committed in `f4acbde`; runtime integration was concurrently changing and was owned by another model.

### Inference and response
Three different records should not be drawn as if they were one tree:

- **Knowledge downwards.** `rsis/tree.py` writes run-local `node.md` files with kind, status and child relationships under `runs/<name>/tree/nodes/`. The loop creates a Goal, method Ideas, iteration Probes, lessons and adoption records. It is a lightweight writer and BM25 reader in a SiftText-like layout, not a call through SiftText Core's Commit, checker or hosted knowledge home. The viewer reads stored node statuses and relationships; its styling does not establish Core enforcement of epistemic transitions.
- **Search activity.** A single Pi search writes a ledger in `<id>.state.json` and a Pi JSON event stream in `runs/<name>/logs/`. Those expose tool starts and finishes while it runs. The viewer derives the current search state from these files, without displaying query text. One standalone trial does not produce the knowledge tree.
- **Methods rightwards.** The viewer plots the iteration winner's held-out test re-run from `state.json`'s `test_points`. Candidate branches use select scores from method files or each point's `select` table. These are different task sets; candidate dots are not directly comparable to the test curve as if all dots shared one measurement. No iteration data means no measured improvement curve.

The loop phase is inferred by the viewer from open Probe nodes, method records and completed search rows. It is not an explicit authoritative runtime phase event. Searches through the chat API only become visible after finished logs are written. Live visibility from the Pi event stream is richer, but it is still sampled once per second.

The animated SVG fills polling gaps by finding a path through its drawn graph and moving a token along that route. Disappearance from the running list is treated visually as progress to scored. These are presentation inferences, not a retained event-by-event execution trace or proof that scoring succeeded. A future debugger that needs exact transitions must consume explicit sequenced runtime events, including errors and aborts; that integration is not delivered by `f4acbde`.

## Completion
The inspected code supports the distinction above. The viewer server returned HTTP 200 on port 8765. A real standalone `v000` Pi search on `hugo_nebula` completed with the recorded referee score 0.9286, 26 correct, zero wrong, denominator 28 and estimated Telem spend $0.0301. This establishes that that search path ran, not that a whole iteration, recursive improvement, or the final visual design succeeded. The parent work retains the outstanding visual judgment and complete-loop observation.

## Source and artifacts
[Retained Pi conversation](artifacts/chats/pi-searchhack-visual-debugger.jsonl), session `01a1dba0-2171-7284-80b0-361440318b9c`; shared with the parent evidence owner. `artifacts/repository` links the existing checkout at `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. The trial's native logs are under its `runs/pi-trial/` directory; quoted scores are from its completed log, not from the shape of an animated path.
