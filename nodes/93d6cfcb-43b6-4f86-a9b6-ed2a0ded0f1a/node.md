---
id: "93d6cfcb-43b6-4f86-a9b6-ed2a0ded0f1a"
name: "Prioritize Readable Progress in the Live Dashboard"
micro_summary: "Records team and visitor feedback on the relative value of state, score, tree and logs in the SearchHack demonstration."
status: "resolved"
scope: "Preserve the reported audience feedback, team layout discussion and their presentation implications without claiming dashboard variations were built."
see_also: [{"target":"75d4a132-b1ea-4bbd-ab8c-e2f4d8d7cac7","reason":"The presentation applied this discussion as a visual handoff explaining what to watch on the live screen."}]
position: 3072
---
**Kind:** What We Learned

## Observed conditions — November 14, 2026

Jack supplied a long dictated conversation among teammates and a visiting person whom he described as a judge. The speaker identities, separate audio and judge status were not independently verified here. The evidence is the text Jack supplied, not a separate interview or a unanimous judging-panel requirement.

The team discussed making the state machine largest, followed by the score graph with its plain-search baseline, then the growing method tree. Logs and “answers handed in” mattered least as material to read; their motion mainly signalled that something was happening. Suggestions included a thin streaming strip, moving logs to another page, showing the tree only as it grows, and using small agent-role lights rather than a large separate agents pane. They did not settle whether one overview or multiple screens was best.

The visiting speaker said they would probably not be able to read logs, wanted to understand what was working or needed attention, cared about clear explanation and replicable results, and would try different input rather than simply replay the team's chosen question. The speaker also qualified that they were only one judge; this is not a survey result.

The team wanted the actual question and task buttons much larger. Search count, money spent and method in use were useful; incidental phase/iteration labels, automatic “latest” run details and noise statistics crowded the screen. Jack asked for static HTML variations **after alignment**, intuitive to a layperson and with “no supplementary text” not directly important to the displayed thing. He invoked minimum viable text, explicitly not a new styling source.

## Inference and response

The assistant proposed three unbuilt choices: one screen with state/score and a small activity strip; two screens separating main progress from tree/log detail; or a large state view with graph/tree below. These were proposals, not an accepted dashboard layout or proof of usability. This session did not implement the static variations or resolve the team's screen-count disagreement.

Jack subsequently asked to apply the feedback to the presentation. That produced the handoff before the demo: who is working, whether scores exceed the baseline, what methods were retained/discarded and, at his additional request, what was just added in the tree delta. The closing invites the audience to ask their own question. The export later used the concurrently developed dashboard renderer; that does not mean this agent delivered the discussed live-dashboard redesign.

## Completion and remaining choice

This synthesis is complete because it preserves the audience report, team priorities, unresolved choice and actual presentation response. The parent live-debugger work remains open. The dashboard variations remain unbuilt and await a layout choice/alignment if Jack resumes that work; no new next marker or implementation commitment is inferred from this capture.

Source: Pi session `01a1dc0c-a596-779d-89b4-26e063f0bfba`, user `d1d52401` (full supplied conversation), assistant's following alignment response, user `280f7a27` (apply feedback to presentation) and `4e3d5a53` (tree delta). `artifacts/chats/pi-searchhack-narrated-presentation.jsonl` links the retained session; `artifacts/repository` links the existing checkout at `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. No external project was moved or changed by this save.
