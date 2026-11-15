---
id: "72cfa59a-de11-4374-8049-6ba0e76c6061"
name: "Diagnose First-Iteration Latency"
micro_summary: "Accounts for the critical path of the 351-second iteration before choosing a speed change."
status: "resolved"
kind: "Probe"
see_also: []
position: 1024
---
## Creation — November 14, 2026

### Observed conditions
The parent work targeted 30–60 seconds per complete iteration after `pi-first` took 351 seconds. Jack dispatched an Astra xhigh subagent on Codex Personal to find the cause. Its assignment was read-only: use the existing run, change no code, make no new paid searches or model requests, and report workload/scoring/budget tradeoffs rather than silently cut the experiment.

## Completion

### Reported measurements
The subagent's completed receipt and the assigning assistant's report give this critical path:

| Stage | Seconds |
|---|---:|
| Training, including scoring | ~117 |
| Improver | 44.6 |
| Selection, including scoring | 57.6 |
| Held-out, including scoring | 131.7 |

Serial per-answer referee checks accounted for about 214 seconds on that path. Calatrava and Hadid each spent about 100 seconds being scored after their searching agents finished. Across the run, 68 gap checks included 39 that merely recognized alternate names for known answers. The search-row `seconds` field excluded scoring.

### Inference and response
The subagent recommended bounded parallel judge checks while keeping prompts, eligibility, caps and score ordering unchanged. Even instantaneous scoring would leave roughly 145 seconds with the observed agent timings and dependent stage order. Thus concurrency alone did not establish the requested 30–60-second target.

The diagnosis completed; it did not implement or measure the proposed optimization. Subsequent authorization, uncapping and persistence belong to [Judge Every Unmatched Answer and Reuse Verdicts](../82df17c2-9999-4aba-9009-91d932430e9f/node.md). The parent speed work remains open because complete iterations still took minutes, not the requested target.

## Evidence and custody
[Assigning conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), Pi session `01a1dc03-df6d-7244-951f-6fc59de7978d`, dispatch `bad0606c`, completion notification `8a26e688`. Report `/tmp/searchhack-speed/report.md` was read during the chat but is unavailable at Commit time; the receipt and attributed summary remain in the native transcript. The original `pi-first` run was later deleted at Jack's explicit corpus reset. These numbers are retained reported measurements, not a fresh independent timing run.
