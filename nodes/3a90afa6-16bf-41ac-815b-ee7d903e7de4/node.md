---
id: "3a90afa6-16bf-41ac-815b-ee7d903e7de4"
name: "Build the Live Ask Comparison Beside Recorded History"
micro_summary: "Provide a question-entry page that compares plain and retained search methods while preserving the recorded dashboard."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target": "93d6cfcb-43b6-4f86-a9b6-ed2a0ded0f1a", "reason": "The visitor report motivated live unfamiliar input rather than a replay-only demonstration."}]
position: 3072
---
## Creation — live input instead of a replay alone

### Observed conditions
Jack asked to work backwards from the visitor’s request to try different input, preserved in Prioritize Readable Progress in the Live Dashboard. He was worried about latency, an overstated recursion claim, and a demo viewers could only watch rather than use. He selected two pages: a main chatbox with Claude Code-like activity, and the historical dashboard with video. He explicitly required `http://127.0.0.1:8765/` and the machine’s existing harness backend.

### Inference and response
The assistant proposed concurrent equal-search-budget A/B, streamed steps and answer checks, rather than training while the visitor waits. Jack approved that implementation. Earlier assistant advice to show only ours-only answers was withdrawn as cherry-picking: the comparison must also show both-found and baseline-only answers. Blinding labels does not equalize runtime or hide clues in the traces.

## Completion — local implementation

`rsis/ask.html` is served at `/`; `/history` serves the existing dashboard with a Film control for `docs/rsis-film.mp4`, copied from the final 2m50 export. Both searchers launch together through the existing Pi route and Telem tools, initially v000 versus v007 and later v000 versus the hand-written v013. A/B assignment is random, with a reveal button. Streaming shows actual tool steps. Answers appear only at hand-in, not as soon as an internal candidate is discovered; the searcher commits its list only then. Browser-judge progress and rulings then appear per answer. The page compares confirmed both-found, only-A and only-B lists. Time and search spend stay visible; judge time is separate from search time.

At Jack’s later request, confirmed answers sort first and are larger with a green bar. Proof opens one judge’s Markdown write-up containing its ruling, quoted reason, source link and action trail, rather than opening the evidence website directly. Judge again rechecks saved hand-ins. A proof trail containing several searches is that judge’s work, not evidence that all other questions were combined. The assistant also repeatedly invoked re-judging during development.

The viewer was restarted on 8765; routes and script syntax were checked, and live comparisons ran. Jack said “looks great!” before requesting proof/sort changes. There was no screenshot or browser visual-verification pass. Questions and logs live under git-ignored `asks/`. This is local working-tree delivery, not a new published release or an automatic learning service. The historical in-repository replay player was not built by adding the film control.

The browser judge and manual iteration have separate child records. The proposed live method-family-tree visual was not implemented here.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
