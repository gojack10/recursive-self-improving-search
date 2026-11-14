---
id: "66c093b3-8a71-4111-8f04-33d6aab95079"
name: "Start the Searchers on browser-harness"
micro_summary: "Commits the first searcher runs to browser-harness web search, with Telem deferred until the proof of concept works."
status: "not_examined"
see_also: [{"target":"ef8ce25e-76e5-429d-86d5-433010cbd615","reason":"The Telem probe Jack asked for while deciding; its cost finding preceded this choice."},{"target":"0fd5c03f-3b02-4441-95f9-78f173744b1f","reason":"The assistant's contrary proposal to build on Telem's settings from the first call."},{"target":"6b472da5-be58-4ce8-9568-05393919bf1f","reason":"The proof of concept this backend choice serves."}]
scope: "Record Jack's choice of search backend for the start of the November 14 build; the work completes when the first searcher runs on browser-harness are attempted and their outcome recorded."
position: 12288
---
**Kind:** Agreed Work

## Creation — November 14, 2026

### Observed conditions

During the SearchHack kickoff, Jack stated his plan:

> "We'll use browser harness on this machine first to get something started just for free so we can probe and maybe we'll probe the API a few times for telem. And then after that [...] we'll s like switch over to telem at the last minute after we know our proof of concept works."

The assistant advised the opposite order. It then ran the probe Jack asked for, recorded in [Probe Telem's Hackathon Console and Router](../ef8ce25e-76e5-429d-86d5-433010cbd615/node.md), and reported that Telem works and draws on a $50 credit. The exchange continued:

- Jack: "ok then we will use browser harness in the meantime".
- The assistant reported that browser-harness has no helper that runs a web search and returns results, and that on this Mac one script holds the browser at a time.
- Jack: "might as well just use only talem right to keep it simple?" The assistant agreed.
- Jack: "cool we will use browser harness in the beginning".

### Inference and response

Jack's last statement is the commitment: the first searcher runs use browser-harness for web search. His opening statement placed the switch to Telem "at the last minute after we know our proof of concept works"; his last statement did not restate when the switch happens.

The assistant disagreed and recommended Telem from the first call. Its reasons were that a method tuned on browser searching may not carry over to Telem's settings, that a result produced without Telem is not evidence for the 40% Telem criterion, that searchers would take turns in one browser, and that a backend swap near the 4:15 deadline is risky. These are the assistant's judgments and were not tested.

The assistant also proposed keeping all searching behind one function with two backends so the switch is a one-file change. Jack did not respond to that proposal.

Nothing was built in that session. What the searchers hunt for was left to the next agent in [Choose the PoC Task and Success Evidence](../9a2b74d6-d0f2-44a5-b6d3-a35fbf465439/node.md).

## Source

Pi session `01a1db5b-1827-7182-a648-9aafa0a72ac9`, November 14, 2026, retained under the probe node at `artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl`.
