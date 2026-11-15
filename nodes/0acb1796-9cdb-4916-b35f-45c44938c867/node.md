---
id: "0acb1796-9cdb-4916-b35f-45c44938c867"
name: "Find Fixed-Budget Search Tasks and Held-Out Answers"
micro_summary: "Develop exhaustive-search questions with verified answer keys and room for sustained method improvement."
status: "in_progress"
kind: "Agreed Work"
see_also: [{"target":"4cd4ec5a-137f-4d58-8d20-f9fd30f0b0b9","reason":"Decided from Jack's confirmed distinction between better methods and simply spending more search turns."}]
position: 2048
---
## Creation — November 14, 2026

### Observed conditions
After the first iteration tied at perfect selection scores, Jack asked for a teammate message requesting harder questions and numerical held-out answers. The assistant recovered his reason before finalizing it: room for sustained fixed-budget method improvement rather than one-shot solutions or longer searches. Jack confirmed the criterion recorded by the sibling learning.

The assistant drafted the following message. Jack subsequently reported: "I already sent that Discord message." The assistant did not operate Discord or independently inspect delivery, a recipient acknowledgment or resulting work.

### Message supplied to the teammate

> Our first iteration tied at perfect scores, leaving no room to demonstrate improvement.
>
> We need exhaustive-search tasks where the starting method finds only part of the answer within a fixed search budget. Later iterations should improve coverage by discovering better queries, sources, or search strategies—not by receiving more turns or money.
>
> Look for answers scattered across sources, where finding the obvious examples is easy but finding the remaining ones requires a better approach. Avoid trivia, straightforward cross-checks, and lists obtainable from one authoritative table.
>
> We’d like enough room for improvement over 5–15+ iterations, but treat that as a research target, not a guaranteed property.
>
> For each candidate, provide:
> - The question and precise inclusion rules/date cutoff.
> - A verified total count and complete answer list, with sources.
> - Why a basic search might miss answers, and what makes the answer key trustworthy.
> - A proposed development/held-out split, keeping held-out answers out of the searcher and improver’s context.
>
> The difficulty claims are hypotheses until we run the tasks. Don’t manufacture difficulty through ambiguous questions or incomplete answer keys.

Formatting emphasis from the chat is omitted; wording is retained.

### Inference and response
The teammate request has been sent according to Jack. The new questions, verified answer counts/lists and split have not been delivered in this conversation. The existing executable pools have not been replaced and no additional run was started. The earlier README designation of some pilot questions as held out is not a completed split or answer key for this revised workload.

This third workstream proceeds separately from the viewer-understandability and iteration-speed work. The next agent should recover the teammate's contribution when available, distinguish proposed difficulty from observed behavior, and agree any runnable task-pool change with Jack. This record does not dispatch another question-research agent over the teammate's assignment. Completion requires a usable candidate set with supported counts/lists and a clear development/held-out separation, or an explicitly recorded limitation.

## November 14 — clean corpus delivered and used

The missing contribution above arrived as clean `questions.json` and `keys.json` files after a damaged paste. [Adopt the Planetary-Naming Corpus and Baseline Every Task](../7dc331bd-57dc-44b2-8003-fc468a6ccae4/node.md) owns loading 18 keyed tasks, the assistant-selected 9/4/5 split, deletion of provisional runs at Jack's request, and the corrected requirement that plain search runs on every task. [Run Six Corpus Iterations and Record Their Limits](../b8186822-2aae-4874-9e04-9b1ec191aa33/node.md) supplies the observed trajectory.

The supplied keys were not independently proven complete: the judge accepted five missing task-answer pairs. The split is implemented, but all tasks share the award/planet shape and the originally requested trustworthy, broadly discriminating benchmark is not fully established. This work remains in progress for that limitation, no longer waiting for teammate delivery. Every task in the final corpus has a key; support for keyless tasks is not evidence that such a task was run in this experiment.

Source: [later conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), clean input `4a10c050` and reset authorization `1816c6ed`. `artifacts/repository` links the canonical `data/questions.json` and recorded run; the external source Downloads directory remains in place.

## Source
[Conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl), Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`, especially the final revised message and Jack's next statement that he sent it. The full seventeen-question source list and earlier rejected tiers remain in that transcript.
