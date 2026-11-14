---
id: "ef8ce25e-76e5-429d-86d5-433010cbd615"
name: "Probe Telem's Hackathon Console and Router"
micro_summary: "Tests whether the hackathon's Telem deployment answers searches and fetches, what it charges and what its console records."
status: "resolved"
see_also: [{"target":"5c47051d-90b9-43e6-ba5a-1b885c7f4ad3","reason":"Owns the event rules and the earlier reading of Telem's public docs that this probe extends."},{"target":"9a2b74d6-d0f2-44a5-b6d3-a35fbf465439","reason":"The console's Benchmarks form and judge bear on the still-open task and referee."}]
scope: "Record one bounded attempt against Telem's SearchHack deployment on November 14, 2026: what was called, what came back and what stayed unknown."
position: 10240
---
**Kind:** Probe

## Creation — November 14, 2026

### Observed conditions

At SearchHack, Jack pasted two signed-in links, his Tavily dashboard and his project in Telem's hackathon console at `hack.telem.ai`, and asked "ok what can we learn from this". The assistant read both through browser-harness in Jack's Chrome. It reported that the Telem project was empty. Relying on an overview line reading "Usage is real; billing is not implemented", it later told Jack that Telem looked free there.

Jack then asked: "test talem to make sure it works and is free probe that". "Talem" is his dictated spelling of Telem. He added: "you have full authority to make keys and roll them and stuff".

### Inference and response

The assistant planned to issue a key, send one search and one fetch, and read what the console recorded and charged.

## Completion — November 14, 2026

### Observed conditions

**Key.** The assistant issued a key named `pi-probe` in the console with the Benchmarks, Traffic data and Search & monitors permissions, leaving "Providers, routing & keys" off. The key is stored at `~/.telem-hack-key` with owner-only permissions and was never printed. While locating the right address it was sent once to Telem's production router, which rejected it, and once to the bare console host.

**Address.** The documented production router, `https://router.telem.ai`, returned 401 "Invalid API key". The console's `runtime-config.json` names the router as `/api/router`. `POST https://hack.telem.ai/api/router/v1/search` and `/v1/fetch` both returned 200.

**Calls.** Times are whole-request times from this Mac.

| Call | Body | Result | Time | Ledger charge |
|---|---|---|---|---|
| Search | `{"user_input":{"query":"…"},"search":{"auto_routing":"accuracy"}}` | 200; seven providers ran | 1.8 s | seven lines, $0.028 in total |
| Search | `"search":{"tier":"minimalist","providers":{"include":["brave"]}}` | 200; Brave only | 0.8 s | $0.005 |
| Fetch | `{"urls":["https://docs.telem.ai/pricing/"]}` | 200; full page text | 0.8 s | $0.001 |

A fetch body shaped `{"user_input":{"urls":[…]}}` returned 422 "Field required".

**Search response.** Each provider appears as its own run with a status, latency and results. The seven chosen were exa, tavily, brave, parallel, ceramic, seltz and you; six returned five results and ceramic returned none. The `routing` entry carried `topic: "general"` and `score: 0.0033` beside the provider list. The response also carries `session_id`, `trajectory_id` and `parent_trajectory_id`.

**Charges.** The organization's Billing page shows a signup grant of $50.00 at 10:46 that morning and $49.97 available after the three calls. Each provider call is its own ledger line. Telem's pricing page, fetched through Telem, says each answering provider is charged at its own published price with no markup, that a failed call is free, and lists most providers at $0.005 a search, `parallel` at $0.001, `ceramic` at $0.00005 and `tinyfish` as free. Project settings have fields for a monthly spend limit and a maximum request cost; none was set.

**Console record.** Traffic listed all three calls as conversations under Jack's account, with columns REL, PREC, ILD and JUDGE. All three still read "pending" when last read, about three minutes after the first call. The Benchmarks page offers "Start a run" with this text: "A run executes the corpus against each arm and judges the results. It cannot be edited once started." Corpus is "The set of tasks each arm will be run against" and Arms is "One JSON object per configuration to compare." The corpus list was empty. The assistant opened and closed the form without submitting.

**Scores from code.** The console reads benchmarks and traffic from `/api/observability/v1/…`. With the `pi-probe` key, the benchmark list, the corpus list and the conversation list each returned 401 "Invalid bearer token".

**Tavily.** Jack's Tavily account is on the Researcher plan with 0 of 9,000 credits used, one key and a 100 requests-per-minute limit. Its dashboard says keys will only be shown at creation from November 20. Tavily is one of the providers Telem calls.

**Public docs.** Auto-routing is described as on by default for installed plugins and off by default in the raw search parameters. The Pi package provides `telem_search` and `telem_fetch`; the docs state that no tool has a parameter for providers or tier, which come from `.telem/telem.json` or `TELEM_*` variables. The Pi package is not among the integrations listed as having monitor tools. The SDKs read `TELEM_BASE_URL`.

### Inference and response

The assistant's conclusions:

- Telem works at the hackathon address and is not free. Its earlier "looks free" statement was wrong: the line it relied on described subscriptions and invoices, and the Billing page shows a real prepaid balance.
- At the observed prices, $50 covers roughly 1,800 searches that fan out to seven providers, or about 10,000 single-provider searches.
- On this one query auto-routing chose seven providers. One query does not show how it behaves in general.
- REL, PREC and ILD were read as relevance, precision and result diversity. That reading is a guess from the labels.

Not established: whether or when the judge scores a conversation and what it measures; how a corpus is added and what an arm's JSON contains; whether judge scores or benchmark results can be read with an API key; whether the SDKs or the Pi package work against the hackathon address.

## Source

Pi session `01a1db5b-1827-7182-a648-9aafa0a72ac9`, November 14, 2026, retained at [artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl](artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl).
