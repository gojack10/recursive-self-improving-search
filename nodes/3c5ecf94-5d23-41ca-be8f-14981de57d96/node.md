---
id: "3c5ecf94-5d23-41ca-be8f-14981de57d96"
name: "Write a Breadth-First Successor to Method Seven"
micro_summary: "Capture the live loss and manually revise the search instructions without claiming an automatic improvement round."
status: "resolved"
kind: "Agreed Work"
see_also: []
position: 3072
---
## Creation

After the page-reading judge confirmed all six baseline submissions and all three v007 submissions, Jack asked to save the raw result and then said “ok manually can we iterate and lock our shit in?” The assistant chose a manual instruction revision rather than running the method writer or a full selection round.

## Completion — v013

The assistant appended two nodes beneath v007 in the project-local tree `runs/corpus/tree/nodes/`: lesson `f2bc3f87-0458-4729-a3a5-a2325750addc` and method idea `0b83e468-8474-4626-a43a-0cf0849cee39`. The supporting Ask run is `20261114-173851-5272`: v000 took 40.6 search seconds and handed in six; v007 took 73.1 and handed in three. In v007’s 20 calls, seven revisited Jim Gray; it checked Knuth but omitted him and stopped at $0.029 spent of $0.08. The assistant’s causal explanation that the old judge taught this caution was conjecture, even though the project-local lesson phrases it more strongly.

`runs/corpus/methods/v013.json` is a hand-written child of v007, title “Breadth-first residual search, written by hand.” It prefixes v007 with candidate collection before deep checking, at most two tool calls per candidate, no repeated checks of settled or irrelevant details, submission of every retrieved-source-supported member, plain answer names, and a budget-use rule allowing early stop only after two empty residual probes. Routing allows up to two wording variants on discovery queries. These are prompt instructions, not mechanically enforced limits. The full method stays in the project artifact, not copied into knowledge prose.

The Ask page’s OURS constant became v013, and the viewer restarted. The training state still names v012 as current; no selection-pool gate promoted v013 and no automatic recursive round wrote it. Historical corpus scores were not re-scored, but the recorded tree is no longer byte-for-byte untouched: it has the appended lesson, method and tree events.

The two follow-up comparisons and their bounded interpretation have their own records. As of this save, project source/UI/browser-judge changes, video and v013 were uncommitted working-tree changes. Jack requested a SiftText Commit, not a repository commit/push. This work resolves the manual revision, not speed, superiority, automatic learning or publication.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
