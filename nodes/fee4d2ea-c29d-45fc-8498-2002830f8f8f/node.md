---
id: "fee4d2ea-c29d-45fc-8498-2002830f8f8f"
name: "Run the First Complete SearchHack Iteration"
micro_summary: "Run one Pi iteration under the selected models and inspect the scored result before scaling."
status: "resolved"
kind: "Agreed Work"
see_also: []
position: 2048
---

## Observed conditions

Jack owns the live model run on his Mac. The pushed branch and local startup checks are recorded by the parent. One earlier Luna search completed, but no full Pi iteration has run. Jack asked that the next step be obvious.

## Originally selected next action

With the local Telem key and Codex Personal settings, Jack runs one iteration on the existing executable task pools from the SearchHack checkout:

```sh
uv run --no-project python -m rsis round --name pi-first -k 1
```

Use Terra-fast high for searchers, Astra medium for the improver and the existing Sol low gap judge. This is a suggested first command. The README's proposed pilot questions are separate from the executable pools.

Finish when a run records train searches, a usable proposed method, paired selection scores and a held-out winner score, or exposes a concrete blocker to fix. Inspect the report and failed searches before starting a longer run. A successful iteration establishes that the wiring works. A claim of improvement still needs a matched baseline on the same tasks and budget. If the task scores sit near the ceiling or the search allowance buys too few queries, revisit task difficulty or routing using the run evidence.

## Completion — November 14, 2026

### Observed conditions
Jack authorized reconciliation and the one-iteration run: "reconcile then run". The assistant fetched `main` at `b571662`, including two newer runtime-fix commits, and merged it into `pi-searcher`. The sole content conflict in `rsis/tavily.py` was resolved by retaining the Telem-only route and its existing credit cap rather than restoring direct Tavily billing. Local merge commit `eab1366` includes the reconciliation. The CLI started with `--help`; no test suite ran. This agent did not push the merge or the preceding viewer-animation commit `f4acbde`.

The exact command above ran once as background job 1, under the existing local Terra-fast high / Astra medium / Sol low settings. It exited 0 after **351 seconds (5m 51s)**. The existing viewer was activated through browser-harness at `http://127.0.0.1:8765/?run=pi-first` at Jack's request.

| Stage | Method | Task | Score | Correct | Wrong | Answer-set size |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Train | v000 | women_chem_nobel | 0.4375 | 5 | 3 | 8 |
| Train | v000 | calatrava_bridges | 0.7500 | 29 | 13 | 30 |
| Select | v000 | turing_uk | 1.0000 | 6 | 0 | 6 |
| Select | v001 | turing_uk | 1.0000 | 6 | 0 | 6 |
| Select | v000 | pritzker_riba | 1.0000 | 28 | 0 | 28 |
| Select | v001 | pritzker_riba | 1.0000 | 28 | 0 | 28 |
| Held out | v000 | nobel_wolf_physics | 0.9630 | 26 | 0 | 27 |
| Held out | v000 | air_disasters_300 | 0.8333 | 6 | 2 | 6 |
| Held out | v000 | booker_films | 0.9286 | 14 | 2 | 14 |
| Held out | v000 | hadid | 0.6181 | 47 | 5 | 72 |

Astra proposed `v001`. Both methods tied at 1.0 on the two selection tasks, so the strict-better adoption rule kept `v000`. `state.json` records round 1, current `v000`, `adopted: false`, new lessons, and held-out mean **0.8357** (rounded to 0.836 in the conversation). Scores apply the repository's correct-minus-half-wrong formula; they are not improvement percentages or probabilities of truth. Answer keys and judge decisions constrain their meaning.

### Inference and response
This completes the bounded first-iteration work: training, a usable proposal, paired selection and held-out scoring all occurred. No method improvement or recursive improvement was demonstrated. The observed comparison tasks gave no separation between methods in this run; that is not a universal proof of their difficulty. The held-out score describes the retained original method, not a gain over a matched held-out baseline.

Jack found the visual phase label opaque and the duration too long. Those outcomes motivate separate viewer and speed work rather than reopening this completed iteration. His task-difficulty discussion also produced a separate fixed-budget criterion and teammate research request. No second iteration or additional agent was launched.

## Sources and artifacts
Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`, retained at [conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl). `artifacts/repository` links the existing checkout `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`; run evidence remains at `runs/pi-first/{attempts.jsonl,state.json,methods/,logs/,report.html}`. The small terminal completion log is retained as `artifacts/first-iteration.log`. Its original background log was `/var/folders/pp/mbjn4xws00jdzs_7knjx9d8w0000gn/T/pi-bg-1794690881102-1.log`.
