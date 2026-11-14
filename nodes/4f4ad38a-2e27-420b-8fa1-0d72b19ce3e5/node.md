---
id: "4f4ad38a-2e27-420b-8fa1-0d72b19ce3e5"
name: "Reduce SearchHack Iteration Time"
micro_summary: "Investigate complete-iteration latency against the requested 30–60 second target without weakening the comparison."
status: "in_progress"
kind: "Agreed Work"
see_also: [{"target":"fee4d2ea-c29d-45fc-8498-2002830f8f8f","reason":"Follows the first completed iteration's observed 351-second wall time."}]
position: 3072
---
## Creation — November 14, 2026

### Observed conditions
The first complete Pi iteration took 351 seconds (5m 51s), ending with exit 0. It ran two training searches, an improver proposing one candidate, four selection searches comparing two methods, and four held-out searches. Its exact results live in the first-iteration node and repository `runs/pi-first/`.

Jack said: "It should be at least 30 seconds or a minute per iteration. So let's have next agent look into why it might be slow." He described a second agent making the live system understandable in parallel. This was discussion of future work; he explicitly did not want implementation or design in the current chat.

Source inspection found that search batches use a six-worker thread pool, while the outer train → improve → select → held-out stages depend on one another. Searchers and improver retain Pi JSON events; judge calls currently collect final stdout through `pi.complete`. These facts identify places to inspect, not a measured attribution of the 351 seconds.

### Inference and response
The requested target is a complete iteration in roughly 30–60 seconds. Its feasibility and the dominant delay remain unknown. The next agent should explain where the actual elapsed time is spent before choosing an optimization. No claim that the judge, model speed, Telem, subprocess startup or serialization caused the observed duration was established here.

The assistant recommended preserving the intended search/scoring work and comparison while investigating speed. Jack's later confirmed fixed-budget task criterion also rules out treating extra search turns as method improvement. If meeting the target requires changing workload, scoring or budget, that is a substantive tradeoff to bring back rather than silently reducing the experiment.

This is parallel to the viewer work, with shared runner/logging changes coordinated between owners. It is not a request for a new harness or a test suite. No speed implementation, extra experiment or agent dispatch occurred in this conversation after the first iteration. Complete this unit by recording the measured cause, the authorized response and its resulting duration or explicit remaining limitation.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl), Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`. `artifacts/repository` links `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`; inspect its `runs/pi-first/` and runner source in place. The first-iteration owner retains the small terminal completion log.
