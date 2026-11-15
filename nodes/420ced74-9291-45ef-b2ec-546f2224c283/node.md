---
id: "420ced74-9291-45ef-b2ec-546f2224c283"
name: "Detect a Plateau in the Improvement Loop"
micro_summary: "Asks how the loop should recognize that improvement has stalled and what should happen then."
status: "resolved"
kind: "Question"
scope: "Answer how the SearchHack loop recognizes a stall and responds, keeping Jack's endorsement separate from untested thresholds and unobserved results."
see_also: [{"target":"9b2ff11d-f8bd-4aec-b03f-c7052c3bdd8d","reason":"Deferred question on detecting idea basins; Jack's note names idea basins as a possible answer."},{"target":"f12a53f8-8dc2-4c1b-b482-cfde6778d2bb","reason":"Reports of stalled runs, a flat-best-score trigger and the Bespoke Labs idea-basin findings; the authors' numbers, about code and ML tasks, not web search."},{"target":"c83b7182-abe0-444a-9a4d-e5b05812a4ef","reason":"Fork-and-Flush's never-firing stall trigger and its fresh-context result shaped the noise band and the breakout round."},{"target":"9ec1b5d1-69ee-4649-b30f-680e04c0fed9","reason":"The repeat-round signal reuses Jack's selected rule that a failure seen before links to an existing node."},{"target":"1f90ecfa-a4a4-4e6b-9861-9744aeba6ce5","reason":"The breakout round draws on this deferred fresh-agent idea; its status is unchanged here."},{"target":"87e216ba-5f84-408a-a381-c15b71b4937b","reason":"The breakout round gives each fresh improver a different slice of history, drawing on this deferred idea; its status is unchanged here."}]
position: 3072
---
**Kind:** Question

## Creation — November 14, 2026

### Observed conditions

As the third of his open questions, after the assistant's synthetic walkthrough, Jack asked:

> "how do we know when we hit a plateu?"

He added that more research might answer it, and that "idea basins and the recent blog post and our overall research findings the internet + nodes we already have might already have the answer, idk. question not for you but for next model".

### Inference and response

Existing records give leads but no answer for this project. [Exploration Collapse Findings From RSI-top and Bespoke](../f12a53f8-8dc2-4c1b-b482-cfde6778d2bb/node.md) records one study that acted when the best score stayed flat, and another that clustered runs into idea basins. [Detect Idea Basins Before Restarting](../9b2ff11d-f8bd-4aec-b03f-c7052c3bdd8d/node.md) already holds the narrower question of detecting a basin, and notes that a flat score alone does not establish one.

The assistant's earlier answer on how improvement would be known proposed comparing method versions on the same unseen hunts at the same budget, with several runs because one run is noisy. No sample size or budget was selected, so a flat reading cannot yet be told from noise. How many flat rounds count, what the loop does after one, and whether a plateau means a stronger improver, a new lineage or stopping are all open. No loop has run, so no plateau has been observed.

## November 14 development — plateau rule and response matrix

### Observed conditions

On the morning of the event, Jack asked a new Claude Code session to "tackle the questions 1 by 1". The assistant read this node, [Exploration Collapse Findings From RSI-top and Bespoke](../f12a53f8-8dc2-4c1b-b482-cfde6778d2bb/node.md), [Study Fork-and-Flush](../c83b7182-abe0-444a-9a4d-e5b05812a4ef/node.md) and [Detect Idea Basins Before Restarting](../9b2ff11d-f8bd-4aec-b03f-c7052c3bdd8d/node.md). The points it relied on are those records' reports of the authors' findings:

- In Fork-and-Flush, a stall-clock trigger never fired in 15 of 25 development runs because tiny gains kept resetting it.
- Fresh context broke idea basins. A "pick a DIFFERENT approach" directive did not measurably help: directed branches won 46% of rounds against 50% chance.
- RSI-top answers a flat best score with several agents, each seeing part of the history and building on a different lineage.
- Bespoke reports about nine times the gain after a switch to a new basin compared with a refinement step.

After questions 1 and 2, Jack said "ok next". The assistant then proposed this answer:

- **Plateau rule.** A plateau is two rounds in a row where the winner's re-run does not beat the best so far by more than a noise band.
- **Noise band.** Before round one, run the starting method three times on unseen hunts. The band is the spread between the highest and lowest score.
- **Response matrix.** When the rule fires, read the candidates:

| What you see | What it means | Response |
|---|---|---|
| Candidates repeat ideas already tried | Idea basin | Breakout round |
| Candidates are new but don't win | Near the limit for this hunt and budget | Check the next row, then stop |
| Scores above about 80% of the hunt's total | Hunt is too easy to show gains | Switch to harder hunts |

- **Repeat signal.** A round that only links failures to existing nodes and creates no new lesson node counts as a repeat round. This reuses Jack's selected rule in [Build the Hackathon Around the Recursive Searcher](../9ec1b5d1-69ee-4649-b30f-680e04c0fed9/node.md) that a failure seen before links to a node.
- **Breakout round.** Start two or three fresh improvers with empty chats. Give each a different slice of the history and a different earlier version to build on, then keep the best candidate. This draws on the deferred [Parallel Fresh-Agent Exploration](../1f90ecfa-a4a4-4e6b-9861-9744aeba6ce5/node.md) and [Vary Retrieved Evidence and Reading Order](../87e216ba-5f84-408a-a381-c15b71b4937b/node.md).
- **Stop rule.** Stop after two breakout rounds in a row with no counted gain, and report "levelled off", not failure.

The assistant said the two-round and 80% numbers were its own picks for a day of roughly 10 to 15 rounds, not tested values. Jack replied:

> "love this matrix save it to sifttext"

### Inference and response

Jack's endorsement named the matrix: the three situations and the response to each. He did not separately comment on the noise band, the two-round trigger, the 80% line, the breakout sizing or the stop rule. Those remain the assistant's revisable picks.

The breakout round uses ideas from two deferred nodes as a proposed mechanism. This record does not change their status or select them as implemented.

No loop has run. No noise band has been measured and no plateau, basin or breakout gain has been observed. The nine-times figure is Bespoke's report about code tasks; it does not predict the size of a jump in this loop.

## Completion

Answered for the SearchHack build by Jack's judgment on November 14, 2026. The decisive answer is the response matrix above: a repeated-idea plateau gets a breakout round, a new-but-losing plateau leads to a difficulty check and then stopping, and a near-ceiling score leads to harder hunts. The detection thresholds and stop rule are kept with it as revisable defaults, not as tested or separately endorsed values.

## November 14 — observed stop and continuation override

The earlier "No loop has run" statements describe the original answer's evidence, not the final day's state. The [six-iteration corpus Probe](../b8186822-2aae-4874-9e04-9b1ec191aa33/node.md) applied these defaults. Its 0.2605 calibration spread was too large for the gradual single-iteration gains to count; two breakout iterations therefore stopped the first job after iteration 4. That stop was observed, but did not establish an idea basin or a true ceiling.

Jack then authorized another 20 iterations. The assistant introduced `--keep-going`, set this run's operational band to zero, retained the original measurement separately, reset counters, and used a $40 cumulative estimated search-spend cap. Those are continuation choices, not a revalidated noise estimator or a newly confirmed plateau law. The loop was stopped for submission after iteration 6; rerunning as-is is not evidence a further 20 already completed. The `run` command's iteration count means additional iterations, while its spend cap is cumulative across resumes. This question stays resolved as an adopted practical answer with later observations; the defaults are still revisable.

Source: [later conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), 20-more approval `6bbc4b90` and submission-time stop correction `727cd86a`.

## Source

Creation: Claude Code session `806eebdc-8059-4465-9101-d683b6efe555`, November 14, 2026 (local time, about 1 AM), retained at `artifacts/chats/claude-searchhack-open-questions.jsonl` under [Can the Improver Be a Stronger Model Than the Searchers](../8955e243-3ef1-4938-9a32-65729724f2db/node.md).

November 14 development and Completion: Claude Code session `4e8b589f-0715-428e-a9d1-de646827b5e8`, November 14, 2026 (morning, local time), retained at [artifacts/chats/claude-searchhack-questions-answered.jsonl](artifacts/chats/claude-searchhack-questions-answered.jsonl).
