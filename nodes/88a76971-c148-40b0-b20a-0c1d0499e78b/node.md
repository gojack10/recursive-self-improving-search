---
id: "88a76971-c148-40b0-b20a-0c1d0499e78b"
name: "How Search Memory and Basin Escape Reach a Live Searcher"
micro_summary: "Locate the actual memory-reading and breakout boundaries behind Jack’s live-learning expectation."
status: "resolved"
kind: "Question"
see_also: [{"target": "3c5ecf94-5d23-41ca-be8f-14981de57d96", "reason": "The subsequent hand-written method change is the selected response to this memory-boundary clarification."}]
position: 5120
---
## Creation

After seeing v007 lose, Jack asked whether the result could go “on the tree raw,” whether idea-basin handling already solved repeated searches, and whether the tree remembered what searches were happening. He said he was confused. Earlier he also asked how continual learning differs from a recursive loop.

## Answer and completion

Inspection of `rsis/pi.py`, `pi_tool.py`, `loop.py` and the run tree established distinct consumers. Ordinary searchers receive a frozen method and tools for search, fetching pages, checking candidates and submitting. They do not have search_history, read_node or read_attempt. The method writer does have those history tools and can read prior traces, verdicts and retained lessons to propose successors. Tree memory reaches a normal searcher only through the method instructions selected before it starts. The new Ask records do not automatically enter the training tree or trigger a writer; this session’s capture and method change were manual.

Basin/plateau handling exists between training rounds: two flat rounds trigger a breakout proposal round. It does not detect and interrupt a single searcher repeating Jim Gray queries mid-episode. Saving a node therefore does not itself fix a live search. The manual-iteration work is the chosen response, not evidence that an existing automated live-memory path operated.

The assistant explained continual adaptation as later methods using prior experience; the recursive design is that the improver itself researches using the current search method, which may help invent its successor. These describe different aspects and can coexist. A score climb alone does not establish improved successor-generation ability. The separate frozen-job recursion comparison was not run. Earlier assistant wording that higher scores “prove” continual learning or that the improver had empirically improved was too strong for these noisy bounded observations. Jack said he understood the student/teacher analogy; that settles this explanation, not the empirical claim.

This question resolves because the implemented boundary was identified. Direct searcher tree retrieval, mid-search basin detection and automatic Ask-to-training ingestion were not implemented or implicitly selected.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
