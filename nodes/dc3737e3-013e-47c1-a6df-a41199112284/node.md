---
id: "dc3737e3-013e-47c1-a6df-a41199112284"
name: "Qualify the Manual Revision Without Calling a Tie a Win"
micro_summary: "Interpret the two live comparisons separately from selection evidence and latency claims."
status: "resolved"
kind: "What We Learned"
see_also: [{"target": "ec503d30-6acd-42c8-a231-5a65e13f40ba", "reason": "produced by the two live browser-judged comparisons, which were count ties rather than wins."}]
position: 2048
---
## Observed conditions

The completed two-question Probe found count ties after the manual v013 change, whereas the preceding v007 asteroid run had lost six to three. The revised method was about four times slower on the asteroid run and about 2.4 times slower on Le Mans; the latter used less search spend. Each method got one run per question. The asteroid question was the very example used to revise the prompt, not a clean held-out transfer trial.

## Inference and response

The assistant reported that the change “removed the failure,” then qualified that neither trial showed superiority. A narrower conclusion is warranted: these observed revised-method samples did not repeat the lower count, but do not establish a durable fix or a win. Runtime remains a real trade-off; concurrent display avoids adding both durations but cannot turn a slower method into a faster one. Equal maximum search dollars are not equal wall-clock time, actual spend, model tokens or judge cost.

The assistant offered committing as-is or trying a harder question. Jack instead invoked SiftText Commit with the epistemic-state-machine requirement. No harder-query mission, repository commit, push, automatic writer round or selection promotion was authorized by that save request. The assistant’s suggestion that harder lists would reveal an edge is unmeasured, not a discovered capability.

## Completion

The scoped interpretation is complete: v013 is the locally selected hand-written Ask method with two count ties and remaining latency cost, not the published benchmark champion or demonstrated recursive improvement. Preserve this uncertainty beside the result rather than inventing a new research commitment.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
