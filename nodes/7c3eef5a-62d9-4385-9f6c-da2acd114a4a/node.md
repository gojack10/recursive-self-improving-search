---
id: "7c3eef5a-62d9-4385-9f6c-da2acd114a4a"
name: "Simplify the Demo Dashboard Around Activity and Scores"
micro_summary: "Carries the four-pane prototype into the selected two-panel view while keeping method lineage distinct from answers."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"49b9b605-895f-4812-ad18-c874bbc354d8","reason":"Follows the delivered granular four-pane viewer; supersedes its visible log panes after the team chose a simpler demo."},{"target":"d0dfd848-85dd-42da-87eb-f70522696fff","reason":"Jack invoked the Shoulder Surfing Funnel: useful actual activity before aesthetic motion."}]
position: 3072
---
## Creation — November 14, 2026

### Observed conditions
Jack first specified four panes: active state top left, per-agent Pi log streams bottom left, run tree top right, method iterations bottom right. That was built. Question tabs then mistakenly replaced the approach tree with right/wrong answers. Jack corrected the ownership: the tree must show approaches, discarded methods, branches and lessons under the epistemic state machine, not answer rows.

In a later dictated team/judge conversation, the team prioritized the state machine, score graph, approach tree, then logs. Jack said log motion made the system feel alive; the reported judge response was that unreadable logs were less useful than working/not-working/attention indicators. This is Jack's supplied conversation transcript, not an independently observed interview.

The assistant made three static alternatives in `~/Downloads/rsis-dashboard-options.html`. Jack chose C, asked for stronger colour and boldness while retaining square edges, then asked to make the machine vertical and distinguish its parts. He selected cutting logs and answer rows, keeping a short tree, enlarging the question and making ours versus baseline obvious.

## Completion — delivered layout

`rsis/view.html` and the read-only `rsis/view.py` now provide:

- A large question and clickable task tabs. The default is the average of five held-out tasks. Each tab's small score is its best recorded score, not necessarily the current method's latest result.
- Indicator lights: cyan searchers, yellow method writer, violet judge/progress, red failures.
- Two primary panels. The left shows a vertical loop and per-agent state graph beside a compact nested run tree. The right shows large ours/plain-search/gap values, current method, searches and money, then a green line against an orange dashed baseline.
- One dot per active actor, dimly coloured blocks at rest and solid active blocks. Agent transitions come from the Pi event stream; the loop phase is still inferred from files, not an exact event trace.
- Nested method branches and lessons with bracketed status glyphs. Method entries carry a number and short title; dropped ones retain their place and are struck through. A flat coloured list was rejected and replaced with the tree. Text was reduced to 12px, wrapped and less deeply indented in a 380px column after Jack could not read clipped names.
- Fixed-size arrowheads and orthogonal tool/return rails after a supplied screenshot exposed crossing arrows and inconsistent token speed.
- New tree entries and graph points animate when data changes, not as invented improvement. Supplemental legend, log panes, answer tree, and the visible run selector were removed at Jack's request.

### Comparison controls and chart correction
Each question shows the maximum count found. `Show answers` reveals plain search's best list beside ours, including on keyed tasks; all 18 current tasks are keyed. This overlay is not part of the epistemic tree. The curve originally plotted late-run plain search at the end of our line, falsely suggesting a regression; plain search is now placed first, and only non-baseline searches follow it. Multiple searches of the same method remain visible, so repeat-run drops can be real.

The button/overlay compares best found counts, while the large score can be the latest current-method row or fall back to an older row. These views are not interchangeable. The final screenshots supplied by Jack show the layout; they are retained as `docs/result-*.png` in the repository. This confirms what was shown, not a comprehensive visual acceptance or correctness check. Routine agent checks were compile/start/script parsing, not browser testing or agent-created screenshots.

### Scope and later ideas
The passive viewer is delivered and this bounded redesign resolves. [Record SearchHack Runs for Programmatic Replay](../9d36cea8-fd14-4648-8edf-996864526dd8/node.md) owns the unfinished replay player. Jack also requested, explicitly for later, UI entry for keys/model selection and a custom question run against plain search. Those controls were not built; running searches still uses the CLI. Keep the later user-question A/B idea separate from claiming the present app does it.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), four-pane specification `75190b2c`, tree correction `108cbd5b`, team discussion `bba5d371`, simplify `b2660cf4`, C selection `da7e4ae3`, vertical machine `7dfd3232`, rejected flat tree `94b57e5e`. `artifacts/repository` links the actual source and committed screenshots. The static Downloads file is an intermediate, not the live app or required runtime input.
