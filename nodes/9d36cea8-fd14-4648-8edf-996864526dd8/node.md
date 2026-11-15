---
id: "9d36cea8-fd14-4648-8edf-996864526dd8"
name: "Record SearchHack Runs for Programmatic Replay"
micro_summary: "Preserves the replay requirement, available event records and the remaining player and historical-scoring gaps."
status: "in_progress"
kind: "Agreed Work"
see_also: [{"target":"0915aad5-fdae-435e-9620-e2e38b14d35a","reason":"The canonical corpus recordings and screenshots were published with the runnable viewer on main."},{"target":"bd434935-7e66-4ef0-81e2-e835905031ea","reason":"Its retrospective score correction changes what a faithful replay can claim about earlier decisions."},{"target":"3e40c32a-addf-4e28-8a28-9b192957c09e","reason":"Separately completed an export-side replay adapter for the narrated film; it is not an in-repository replay feature."}]
position: 4096
---
## Creation — November 14, 2026

### Observed conditions
Jack wanted all run data saved so the team could select runs and replay them programmatically, including at 2x speed in HTML, for its demo. He later asked whether the scorer correction could appear in those recordings, then whether he could re-record the demo. He also wanted others to clone the repository, inspect history and eventually use a replay tab, without private API keys being included.

### Selected response
Retain actual event timing and search evidence rather than fake a moving demonstration. The existing viewer remains a live file reader; a recorded run must be distinguished from live execution, and revised scores from historical decisions.

## Work completed

`corpus` began after arrival timestamps were added to Pi events. The run records:

| Record | Information |
|---|---|
| `logs/<id>.pi.jsonl` | Agent turns, deltas and tool events with arrival time `t` |
| `logs/<id>.state.json` and `<id>.json` | Task/role/method, raw answers, retrieved evidence and scored detail |
| `logs/<id>.judge.jsonl` | Per-answer judge progress/verdicts, reuse and times, not the judge's internal Pi stream |
| `attempts.jsonl`, `rounds.jsonl` | Scored search/iteration rows with write times |
| `tree/`, `tree_events.jsonl` | Present tree and timestamped node/status changes |
| `methods/`, `state.json` | Method versions and the latest loop state/curve |

The viewer reads agent times from recorded events, not checkout file dates. The complete snapshot and verdict SQLite file were committed under `runs/` and pushed to `main`; no extra private archive of all runs is required. The earlier five run directories were deleted under Jack's corpus-reset instruction, so they cannot supply full replays now merely because a note mentions them.

## Remaining work and limits

**No playback player was implemented in the repository.** Opening a stopped run shows final-state files, not a timed replay; stale unfinished actors can appear temporarily running or stalled. There is no 2x clock, seeking, historical-state reducer or replay tab. This unit remains open.

A player must reconstruct state from the timestamped records rather than use the current final files as if they were historical snapshots. The corrected run's `attempts.jsonl` and `state.json` were rewritten after re-judging; `rounds.jsonl`, tree judgments and selection aggregates were not all rewritten. Final event arrival times alone do not produce a scoring-history-perfect replay. Git retains earlier editions, while the new correction must be identified explicitly.

A concurrent session did build a read-only export adapter outside the repository for [the narrated video](../3e40c32a-addf-4e28-8a28-9b192957c09e/node.md). Its retained record describes a 177x reconstruction followed by corrected final API snapshots, not live inference or a portable repo player. That adapter and its local dependencies live in the presentation artifact directory. This is evidence of an export-side reconstruction, not grounds to claim all replay work is absent or finished.

Next work for this repo is the actual player and its honest handling of stopped/interrupted actors, evolving verdict pools and scorer changes. Do not tell the team it can already press play at 2x, or imply that a successful HTTP startup verified replay. Re-recording the current screen can capture the final graphs and trees; motion requires either real live work or the unbuilt replay, clearly labelled.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), initial recording request `e5e7bd40`, 2x request `d454cc8a`, public replay intent `b2660cf4`, re-scoring/replay concern `0feca6b7`, re-record question `596859a4`. `artifacts/repository` links the canonical project; final published snapshot is GitHub `8e0dec9`. Raw transcripts remain outside that public repository and knowledge Git.
