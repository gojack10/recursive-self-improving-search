---
id: "240a8b42-07e1-47b2-a20f-75214f3c8b43"
name: "Record the Re-scored SearchHack Corpus Results"
micro_summary: "Separates the corrected-scoring run evidence used in the demonstration from earlier ties, raw records and the unmeasured recursion claim."
status: "resolved"
scope: "Record the versioned corpus evidence inspected for the presentation and its limits, without treating export work as a new evaluation."
see_also: [{"target":"3e40c32a-addf-4e28-8a28-9b192957c09e","reason":"The narration-synced video freezes this evidence and labels selected individual results separately from all unseen questions."}]
position: 14336
---
**Kind:** What We Learned

## Observed conditions — November 14, 2026

The earlier first Pi iteration tied on selection and retained version zero. During the presentation work, the assistant then inspected later `runs/corpus` history. Initially its raw scores were about 0.63 at baseline and 0.81 by round four. Jack subsequently said the team had adjusted the scorer because it was hurting results and asked to rerecord the evidence. He supplied dashboard links for Grammy/Mercury, Freedom/Venus, Nobel physics/Moon and Grammy/Venus.

The inspected checkout's history included `b3a7ff9` (“referee: second lookup before ruling, and only contradicted answers count as wrong”) and `0d2445b` (corpus re-scored through round six). Those changes came from the project work outside this export; this assistant did not implement the scorer, rerun its searches or independently validate every answer. It read the resulting local API and saved a snapshot in `replay-data.json`.

### Corrected-scoring snapshot used for the final film

The recorded baseline is **0.6202**. The saved corrected `state.test_points` were:

| Round | Retained method | Score on unseen questions |
|---|---|---|
| 1 | v002 | 0.6909 |
| 2 | v003 | 0.7215 |
| 3 | v006 | 0.7741 |
| 4 | v007 | 0.8187 |
| 5 | v007 | 0.7935 |
| 6 | v012 | 0.8495 |

Thus the final all-unseen screen shows **85% versus 62%, +23 percentage points**, not a monotonically rising six-round trajectory: round five dipped. The replay's final snapshots came from `/api/run?name=corpus` and the task-specific endpoints served at `127.0.0.1:8765`. Corrected state/API values were used because raw `rounds.jsonl` still held earlier test scores, including 0.8188 for round six instead of corrected 0.8495.

The three selected detail screens show:

| Task | Use in the run | Ours shown | Plain-search baseline shown |
|---|---|---|---|
| grammy_mercury | unseen | 100%, 15/15 | 73% |
| nobel_physics_moon | unseen | 79%, 33/42 | 47% |
| freedom_venus | selection | 71%, 5/7 | 43% |

These are the finished dashboard's latest available answerer for each task, not each task's historical best. The earlier 86% Freedom/Venus claim was a different method's peak; the final frame showed 71%. Grammy/Venus was not selected: it was a practice question and its sparse graph did not show a useful multi-method trajectory. Calling the three screens “Best questions” is the video's selection label, not a claim that they are an unbiased sample or the top three scores across all tasks.

## Inference and response

The assistant updated the presentation's evidence from “pending” to the **observed higher held-out score in this recorded run**, while leaving better-improver/recursion measurement pending. The old first-run tie remains true as its own historical result; it is no longer an adequate description of all subsequent run observations.

The video did not perform a new evaluation. It shows existing re-scored search traces and the final API snapshot; the scorer correction is a changed measurement condition, not additional learned-method progress. Earlier commentary compared the round-four gain to a 0.2605 repeat-run noise estimate. That estimate predates the correction and cannot by itself establish confidence for the re-scored comparison. No significance analysis, independent holdout replication or controlled stronger-method-improver comparison was performed here. A higher search score alone does not establish recursive self-improvement.

The two unseen detail examples remain distinguishable from Freedom/Venus, which was used for selection. The five unseen questions are the relevant recorded aggregate; presentation highlights and practice/selection results must not be substituted for that aggregate.

## Completion, source and artifacts

This record resolves the bounded evidence capture, not the project's research goal. `artifacts/presentation` links `/Users/jack/sifttext/nodes/9863dbdd-2c88-4d32-972c-91c30e18199c/artifacts/explainer`, where `replay-data.json` freezes these values and `export-replay.py` shows their extraction. `artifacts/repository` links `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`; that mutable checkout is not the frozen evidence version. No external project was relocated.

Source: retained Pi session `01a1dc0c-a596-779d-89b4-26e063f0bfba`, via `artifacts/chats/pi-searchhack-narrated-presentation.jsonl`; user `356c571f` requested the re-scored examples; API/checkout reads immediately following it establish the versions and values. Tool records `c47b3531` and `6b923d86` establish which numbers actually appeared after the rendering repair. The copied export receipts are recovered session tool output, not independent reruns of the evaluation.
