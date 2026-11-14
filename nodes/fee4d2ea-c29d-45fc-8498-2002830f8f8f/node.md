---
id: "fee4d2ea-c29d-45fc-8498-2002830f8f8f"
name: "Run the First Complete SearchHack Iteration"
micro_summary: "Run one Pi iteration under the selected models and inspect the scored result before scaling."
status: "in_progress"
kind: "Agreed Work"
see_also: []
position: 2048
---

## Observed conditions

Jack owns the live model run on his Mac. The pushed branch and local startup checks are recorded by the parent. One earlier Luna search completed, but no full Pi iteration has run. Jack asked that the next step be obvious.

## Next action

With the local Telem key and Codex Personal settings, Jack runs one iteration on the existing executable task pools from the SearchHack checkout:

```sh
uv run --no-project python -m rsis round --name pi-first -k 1
```

Use Terra-fast high for searchers, Astra medium for the improver and the existing Sol low gap judge. This is a suggested first command. The README's proposed pilot questions are separate from the executable pools.

Finish when a run records train searches, a usable proposed method, paired selection scores and a held-out winner score, or exposes a concrete blocker to fix. Inspect the report and failed searches before starting a longer run. A successful iteration establishes that the wiring works. A claim of improvement still needs a matched baseline on the same tasks and budget. If the task scores sit near the ceiling or the search allowance buys too few queries, revisit task difficulty or routing using the run evidence.
