---
id: "49b9b605-895f-4812-ad18-c874bbc354d8"
name: "Expose SearchHack Activity and Pi Turns"
micro_summary: "Make the passive viewer show actual work and readable agent output rather than an opaque phase label."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"fee4d2ea-c29d-45fc-8498-2002830f8f8f","reason":"Follows Jack watching the first complete iteration and finding its activity opaque."},{"target":"4f4ad38a-2e27-420b-8fa1-0d72b19ce3e5","reason":"Parallel latency work may share runner and event changes; coordinate ownership rather than replace the same plumbing independently."}]
position: 2048
---
## Creation — November 14, 2026

### Observed conditions
Jack watched `http://127.0.0.1:8765/?run=pi-first` after authorizing the first iteration. He saw a flashing train block but could not tell what was happening. He asked what training meant; the assistant explained that these were searches whose outcomes feed method revision, not model-weight training. Both training searches had submitted when inspected, while one score had not returned.

Jack: "In that case I it should say scoring and not training." He wanted more granular visible state and the stream of Pi responses/turns in readable blocks: "I just want to see shit." He repeatedly limited this conversation to dialogue, not implementation or detailed design. He later selected understandability and speed as parallel work for the next agents.

Inspected `rsis/pi.py` already runs searchers and improver with `--mode json`, writing live events under `runs/<name>/logs/*.pi.jsonl`. Pi's JSON Event Stream documentation provides message updates, completed messages, tool execution events and turn boundaries. An SDK/RPC migration is not needed merely to expose that existing stream; this is the assistant's recommendation, not a chosen design.

The judge uses a different collection path: `Chat.json` in `rsis/llm.py` calls `pi.complete`, which launches headless Pi in text mode and collects stdout after completion. Its answer is JSON containing a verdict and reason; "text mode" describes transport, not an unstructured verdict. That path does not currently retain live judge JSON events. Jack responded: "we should def be using json."

### Inference and response
The next agent owns making actual activity understandable, including distinguishing searching from scoring and exposing readable Pi output. No UI layout, event schema or streaming architecture was selected or implemented during this conversation. The passive, read-only viewer remains the intended interface.

Phase names such as train/select/test describe a search's role in the experiment; they do not say whether an actor is generating, querying, fetching, submitting or being scored. The prior viewer derives phases and animates inferred paths; it must not present those animations as an exact execution trace. The concrete failure is a broad train label concealing scoring work, not evidence that all runtime state needs replacing.

Coordinate changes to shared runner/logging code with the latency work. This save records continuation, not dispatch of either agent. Finish when Jack can follow what each actor is doing and inspect its inputs/outputs; visual acceptance remains his.

Jack also approved a concise explanation style for this project after rejecting score-heavy summaries: begin with "We tried to make the search agent better. This run didn’t show an improvement," then explain the few steps. For a comparison question, headings and actual actor inputs/outputs made the Turing task and tie understandable. He said "keep this style."

## Completion and subsequent UI selection — November 14

The next session implemented the requested granular state and readable per-agent Pi log panes in the four-pane viewer. The scorer emits per-answer progress so completed searching no longer appears only as an opaque train block. This bounded implementation completed; the later lack of visible log panes is an explicit design change, not evidence it never ran.

Jack and the team then chose to cut unreadable streaming panes from the demo. The sibling [Simplify the Demo Dashboard Around Activity and Scores](../7c3eef5a-62d9-4385-9f6c-da2acd114a4a/node.md) records that choice and delivered lights/dots, while preserving raw Pi streams on disk. The judge emits JSON progress per check but its internal Pi transport remains text; a full live judge Pi-turn stream was not delivered. The visual debugger parent remains open for separate replay work and remaining presentation limits; resolution here is not comprehensive visual acceptance.

Source: [later conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), initial four-pane request `75190b2c`, later simplification `b2660cf4` and selected C `da7e4ae3`.

## Source and artifacts
Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`, retained once under the first-iteration owner and linked here as [conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl). `artifacts/repository` links `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`; source files and existing Pi logs stay there. Pi documentation was read at `/Users/jack/.local/share/pi-mono/packages/coding-agent/docs/json.md`. No screenshots were taken.
