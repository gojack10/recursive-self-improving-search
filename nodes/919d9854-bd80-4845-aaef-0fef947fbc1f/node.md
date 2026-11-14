---
id: "919d9854-bd80-4845-aaef-0fef947fbc1f"
name: "SearchHack Score and Search Record Fields"
micro_summary: "Explains what the per-search fields mean and which values determine the score."
status: "resolved"
kind: "What We Learned"
see_also: []
position: 1024
---
**Kind:** What We Learned

## Observed conditions

On November 14, Jack asked which fields in a single SearchHack run determine its score and what the remaining fields do. He reiterated the term **task**, saying “we're we're swapping hunt with task”. The code and existing records use `hunt`. A **search** is one run of one method on one task. A **query** is a web search within that run.

| Field | Meaning and use |
| --- | --- |
| `attempt_id` | Identifies this search so the improver can open its full record. |
| `method` | Method version, such as `v000`. Groups scores by version. |
| `task` (stored as `hunt`) | Assignment the search ran, such as `calatrava_bridges`. Identifies its answer key. |
| `kind` | Task category, such as `structures`. Gives the improver context. |
| `score` | Calculated result. The harness compares mean scores on selection tasks to choose a method. |
| `correct` | Finds credited by the referee, including verified gaps when enabled. Score input. |
| `wrong` | Finds marked wrong or unsupported. Score input. |
| `total` | Answer-key size plus any verified gaps. Score input. |
| `x_only`, `y_only` | Wrong finds the gap judge classified as meeting just one condition. Already included in `wrong`. |
| `spent` | Estimated Telem dollars used. Tracks cost and run budget. |
| `searches`, `fetches` | Counts of recorded Telem search and page-fetch calls. A batched search call can carry several queries. |

The referee is Python code. It compares submitted finds with the stored Wikidata answer key and in evidence-required runs requires a URL retrieved during that search. Recognized duplicates carry no extra penalty. It computes `score = max(0, correct − 0.5 × wrong) / max(total, 1)`, rounded to four decimal places. The optional **Judge** checks eligible unmatched finds with independent Tavily evidence. An accepted missing answer increases both `correct` and `total`. The **Frontier** model submits answers as a contestant in the separate comparison command.

The local Pi trial used `check_gaps=False`. Its `v000` row for `calatrava_bridges` had 9 correct, 25 wrong, and 23 total. The formula gives `max(0, 9 − 12.5) / 23 = 0`, matching the logged `0.0`. The row also had `kind=structures`, `x_only=0`, `y_only=0`, `spent=0.0862`, `searches=3`, and `fetches=1`. The standard loop default still enabled gap checking at inspection. A paired score using the Judge on the same finds was unavailable.

## Inference and response

Only `correct`, `wrong`, and `total` enter the formula. The assistant proposed keeping the answer-key referee and removing the model-based gap check. This would also remove the producer of `x_only` and `y_only`, with legitimate finds missing from the answer key potentially losing credit. Jack authorized saving the clarification. The Judge cut remains a proposal, and `task` is the selected terminology.

## Sources

[Codex conversation](artifacts/chats/codex-searchhack-scoring-fields.jsonl), lines 243–286. The [referee](https://github.com/gojack10/recursive-self-improving-search/blob/6a49311/rsis/referee.py#L71), [stored row](https://github.com/gojack10/recursive-self-improving-search/blob/6a49311/rsis/history.py#L30), [improver context](https://github.com/gojack10/recursive-self-improving-search/blob/6a49311/rsis/improver.py#L53), and [comparison command](https://github.com/gojack10/recursive-self-improving-search/blob/6a49311/rsis/loop.py#L281) establish the field uses. The Pi example came from `runs/pi-trial/attempts.jsonl` and `rsis/pi_searcher.py` on the local `pi-searcher` branch.
