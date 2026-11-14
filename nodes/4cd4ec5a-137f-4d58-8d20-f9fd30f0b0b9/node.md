---
id: "4cd4ec5a-137f-4d58-8d20-f9fd30f0b0b9"
name: "Task Difficulty Must Reward Better Methods at a Fixed Budget"
micro_summary: "Distinguish tasks that need improved search strategies from tasks completed by spending more turns."
status: "resolved"
kind: "What We Learned"
see_also: [{"target":"fee4d2ea-c29d-45fc-8498-2002830f8f8f","reason":"Produced by discussing the first iteration's perfect selection-score tie and its lack of improvement evidence."}]
position: 1024
---
## Creation — November 14, 2026

### Observed conditions
The first iteration's original and proposed methods both scored 1.000 on both selection tasks. Jack asked who supplied the Turing question; Git traced its exact wording to teammate Alyssa's original pipeline commit `780cf98`. No new task was invented for that run.

Jack supplied seventeen pilot questions and asked for difficulty tiers. The first nine were already README proposals, separate from the executable pools; the other eight were absent from the inspected local question lists. The assistant's difficulty estimates were not measured model results.

The assistant's tier 3 combined records, such as astronauts who flew Gemini, traveled to the Moon on two Apollo missions and walked on the Moon at least once. Tier 4 required exhaustive lists, such as all officially designated US national parks or every full UN member state with its admission date. Jack initially chose both, then rejected tier 3 as too easy to one-shot.

His principal reason was room for sustained iterations: "we need it questions that are that are hard enough to have iterations and have like clear improvements basically." He wanted potentially more than five or fifteen iterations rather than a one-step jump to perfect. He then clarified why complexity alone was insufficient: "it's just turns. Like more turns solve this, not a recursively improving search" (excerpt).

The assistant asked: "Is the real requirement: at the same search budget, the starting method misses substantial answers, and later iterations must discover better ways to find them—not simply spend more turns?" Jack answered: "yes exactly".

### Inference and response
The selected criterion is improved search method at a fixed budget, not a difficulty-tier label or larger output. An exhaustive list on one official page, including the suggested UN table example, may still fail it. Cross-record tasks solvable by simply extending an obvious procedure are not Jack's selected direction.

The hoped-for workload has discoverable but scattered answers: a starting method finds some, then better queries, sources or strategies are needed to improve coverage within the same allowance. This is a task-selection hypothesis. No new candidate has been qualified as producing a sustained curve, and 5–15+ iterations is a desired research horizon, not an achieved result or a reason to manufacture gradual gains.

The assistant distinguished improving search performance from proving recursive improvement: a rising score alone does not establish that the improved search method improves the process of generating future methods. The parent's earlier recursion question remains open.

## Completion
Jack's explicit confirmation settles the task-selection criterion and supersedes the temporary tier-3-and-tier-4 choice. It does not establish task difficulty, a new answer key or measured search improvement. The sibling task-finding work owns obtaining questions and held-out answers.

## Source
[Conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl), Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`, including the seventeen supplied questions, both tiering passes, the reasoning question and Jack's confirmation. `artifacts/repository` links the inspected SearchHack checkout at `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search` for the README/executable-pool distinction and Git provenance.
