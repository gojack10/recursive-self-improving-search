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

## November 14 — diagnosis and later limitation

[Diagnose First-Iteration Latency](../72cfa59a-de11-4374-8049-6ba0e76c6061/node.md) completes the bounded read-only investigation: serial referee calls accounted for about 214 seconds on the first iteration's path, and even instantaneous scoring left about 145 seconds in that measurement. [Parallel cached judging](../82df17c2-9999-4aba-9009-91d932430e9f/node.md) was subsequently implemented with Jack's approval, while the task set, cap and judge model also changed. The later corpus job took 2,149 seconds for calibration/baselines and four iterations before its stop, not 30–60 seconds per iteration. No controlled before/after measurement holds those changed conditions fixed. This parent stays in progress for the target, with the cause and authorized response now known; it is no longer waiting for initial dispatch.

Source: [later conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl). The original `pi-first` directory referenced below was later deleted under Jack's explicit reset; use the retained first-iteration record and later diagnostic receipt rather than treating that path as available.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-first-iteration.jsonl), Pi session `01a1dbe5-7190-7284-80b0-36172f8d088c`. `artifacts/repository` links `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`; inspect its `runs/pi-first/` and runner source in place. The first-iteration owner retains the small terminal completion log.
