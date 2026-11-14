---
id: "2f708580-00da-4bad-a64c-8c318beefbb9"
name: "Score One Pi-Run Search on Calatrava Bridges"
micro_summary: "Runs the seed method once as a headless Pi agent through Telem and scores it with and without the gap judge."
status: "resolved"
see_also: [{"target":"919d9854-bd80-4845-aaef-0fef947fbc1f","reason":"Records the unjudged 0.0 row from this search and the proposal to drop the judge."},{"target":"ef8ce25e-76e5-429d-86d5-433010cbd615","reason":"Supplied the working hackathon router address and per-provider prices."}]
position: 1024
---
**Kind:** Probe

## Creation — November 14, 2026

### Observed conditions

Under [Run the Harness Through Pi on Codex Personal](../a21a1d82-0ac0-4a8e-8ddf-eee4b76c6d02/node.md), the assistant checked the route before building anything:

- The repository's own `python -m rsis smoke` reached the hackathon Telem router. Auto-routing returned 21 results from seven providers, all eleven providers answered when pinned, and fetch returned page text. It spent about $0.07, then stopped at the missing `TAVILY_API_KEY`.
- `pi --list-models` showed `openai-codex-personal` with Astra, Sol and Luna. Terra appeared only under `openai` and OpenRouter.
- One headless Pi call to `openai-codex-personal/gpt-6-astra:medium`, with discovery off and only `codex-workspaces.ts` loaded, answered in 2.2 seconds.

The assistant then built the Pi searcher and ran it once.

### Inference and response

Run the seed method `v000` as a Pi agent on one train task, `calatrava_bridges`, with Luna at high effort, and score it with the repository's referee.

## Completion — November 14, 2026

### Observed conditions

| | |
|---|---|
| Model | `openai-codex-personal/gpt-6-luna:high` |
| Time | 74.0 seconds, 6 Pi turns |
| Telem | 3 auto-routed searches and 1 fetch, $0.0862; the fourth search returned "budget exhausted" |
| Tokens | 55,338 input, 2,316 output |
| Submitted | 35 finds |

Each auto-routed search used seven providers and cost $0.02805.

**Scored without the judge** (`check_gaps=False`): 0.0. The referee counted 9 correct, 21 wrong, 4 unsupported and 1 duplicate, against 23 Wikidata answers.

**Scored with the judge.** The assistant set the judge to `pi:openai-codex-personal/gpt-6-sol` at low effort and the gap check to Telem pinned to Tavily, then re-scored the same 35 finds. The result was **0.7903**: 27 correct, 5 wrong, 31 total, 4 Wikidata answers missed. Rows were 19 correct, 8 verified gaps, 3 duplicates, 4 unsupported and 1 wrong. Re-scoring took 104 seconds.

Most of the swing is naming. The judge matched English names to Wikidata's local labels: "Alamillo Bridge" to Puente del Alamillo, "Campo Volantín Footbridge" to Zubizuri, and "Serreria Bridge" to Assut de l'Or. Gaps it accepted include the Mimico Creek Pedestrian Bridge in Toronto and the Reggio Emilia bridges. It rejected "Three Trillizas Bridges (Oviedo)".

### Inference and response

The Pi path works end to end on Codex personal and Telem with no API keys. The judge decides whether this task scores 0.0 or 0.79, so the unjudged score mostly measures name matching, not search.

At 0.79 after three queries, this task leaves little room for a method to show improvement. That is one search on one train task. It does not measure the other tasks or the run-to-run spread.

Telem's $0.08 cap bought three queries because auto-routing fans out to seven providers. A method pinned to one provider could afford many more queries. That is an inference from the observed per-call cost, not a tested method.

## Source

Claude Code session `a5499697-1483-4ea4-b150-ec7263fe5161`, retained under the parent at [artifacts/chats/claude-searchhack-pi-harness.jsonl](artifacts/chats/claude-searchhack-pi-harness.jsonl). The search log is `runs/pi-trial/logs/28c25f546e.json` in the repository checkout. It is untracked, and its `referee` field now holds the judged score.
