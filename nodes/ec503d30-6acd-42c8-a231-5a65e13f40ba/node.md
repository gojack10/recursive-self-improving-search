---
id: "ec503d30-6acd-42c8-a231-5a65e13f40ba"
name: "Compare the Hand-Written Method on Two Live Questions"
micro_summary: "Run plain search and v013 on the asteroid and Le Mans lists under the browser judge."
status: "resolved"
kind: "Probe"
see_also: []
position: 1024
---
## Creation

The assistant ran one new comparison of the revised method on the same asteroid question, then one on the different-shaped Formula 1/Le Mans question, to see whether the manual breadth change still lost. Both sides used the same $0.08 search cap and the configured Pi searcher. No selection-pool experiment, repeated-run estimate or training-loop recursion comparison was performed.

## Completion and observations

| Local Ask run | Question | Plain v000 | Hand-written v013 |
|---|---|---|---|
| `20261114-175607-36db` | Turing Award winners with an asteroid | 6 browser-confirmed; 19.9 search seconds; $0.06 rounded | 6 browser-confirmed; 80.8 seconds; $0.06 rounded |
| `20261114-175814-57e9` | F1 world champions who won Le Mans | 5 browser-confirmed; 11.7 seconds; $0.03 rounded | 5 browser-confirmed; 28.4 seconds; $0.01 rounded |

Asteroid lists shared Knuth, Thompson, Ritchie, Wirth and Gray. Only baseline submitted Backus; only v013 submitted Berners-Lee. The Le Mans lists were identical: Hawthorn, Phil Hill, Rindt, Graham Hill and Alonso. All were accepted by the browser judge in these runs; this reports the model’s rulings, not an independently exhaustive ground-truth audit. Shared futures mean overlapping answers reuse the same judgment rather than obtaining two independent confirmations.

The submitted answer lists, result JSON, judge state/streams and proofs remain under the repository’s git-ignored `asks/` directories. The Le Mans method spent only $0.007 before stopping; compliance with the new budget instruction was not established. The assistant called it ignored, but did not establish whether its explicit two-empty-probes exception applied. No extra spending is inherently a goal.

The attempts ran and their output was recorded, satisfying this Probe’s finish line. They did not produce evidence that v013 beats baseline on answer count.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
