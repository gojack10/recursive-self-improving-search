---
id: "bd434935-7e66-4ef0-81e2-e835905031ea"
name: "Correct Unconfirmed-Answer Penalties and Re-score the Corpus"
micro_summary: "Separates contradicted from unconfirmed answers and records the retrospective scoring correction."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"82df17c2-9999-4aba-9009-91d932430e9f","reason":"Follows the parallel cached judge; replaces its treatment of unsuccessful confirmation as a wrong answer."},{"target":"b8186822-2aae-4874-9e04-9b1ec191aa33","reason":"Recomputes recorded corpus outcomes without rerunning the agents or changing the historical method choices."}]
position: 2048
---
## Creation — November 14, 2026

### Observed conditions
Jack saw methods finding more answers but receiving lower scores. Part of that was the explicit half-point penalty for rejected answers. Inspection showed some judge reasons were only missing evidence after one lookup, not evidence that the answer was false: Muddy Waters and Charles Ives were examples. These rejections were cached and reused.

Jack said, "WTF!!! we should get higher score for that! IMPLEMENT THAT AND RESTART", then asked whether the recordings could reflect it because the demo needed replay. With about ten minutes left before submission, he challenged the proposed loop restart. The assistant stopped improvement work and limited the finish to re-judging, updating results and pushing. No new search iteration was started afterwards.

## Completion

### Implemented response
The judge prompt now distinguishes `yes`, `no`, `unknown`, and `same`. It requests a targeted missing-fact query; if it has not accepted or matched the answer and supplies that query, a second lookup precedes the final ruling. `yes` credits a verified missing answer; `no` counts wrong; an unsettled answer or failed lookup becomes `unconfirmed`, with neither credit nor penalty. Evidence that contradicts an answer and a submission with unsupported retrieved-page evidence can still cost half a point.

The assistant deleted 14 stored `wrong` verdicts, then re-scored saved searches in two passes so denominators settled after all newly accepted answers entered the pool. It updated per-search referee detail, `attempts.jsonl`, and the held-out curve and baseline in `state.json`. The 217-second job ended with exit 0. The final SQLite snapshot has 102 `same`, five `verified_gap`, two `unconfirmed`, and seven `wrong` rows (some people occur under more than one task or spelling).

The five model-verified gaps are Muddy Waters for Rock Hall/Mercury; Muddy Waters and Charles Ives for Grammy/Mercury; Ariel Durant for Pulitzer/Venus; and Georgia O’Keeffe for Medal of Freedom/Venus. These are judge outcomes, not an independently human-audited answer key. Béla Bartók and Alicia de Larrocha remain unconfirmed for Grammy/Mercury rather than being called false.

### Other corrections exposed during this conversation
Method 8's Nobel/Venus search had found all 11 names but scored zero because its names continued after an em dash. The deterministic matcher was fixed to split at an em dash or semicolon and that search was re-scored to 1.0. Separately, two HTTP 429 judge failures had been treated as wrong in method 7's Nobel/Mars search; re-judging them raised that row from 0.0 to 0.3. These corrections are not gains from a new method.

### Historical boundary
Raw submissions, retrieved pages and agent event timing were reused, not recreated. Method adoptions were **not** replayed under the new scorer. `rounds.jsonl`, selection aggregates in the saved iteration points, and historical tree judgments still contain decisions/scores from before re-scoring; `attempts.jsonl` and `state.json` carry the corrected numerical view. A future replay must label the scorer/version and this discrepancy rather than imply the historical choices were made using the corrected scores.

The change and re-scored run shipped to GitHub `main` in `70df637`. The requested scoring repair completed; fairness of every verdict and counterfactual winners remain unestablished.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), challenge `0feca6b7`, deadline `214d5b74`, restart correction `727cd86a`, re-score completion `3601fa16`. `artifacts/repository` links the project; `runs/corpus/`, the verdict SQLite file and Git history retain the concrete outputs and earlier editions. The temporary re-score script was removed after publication.
