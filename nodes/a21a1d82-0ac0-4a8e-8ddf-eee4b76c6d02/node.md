---
id: "a21a1d82-0ac0-4a8e-8ddf-eee4b76c6d02"
name: "Run the Harness Through Pi on Codex Personal"
micro_summary: "Commits the SearchHack harness to headless Pi agents on Jack's Codex personal route with Telem as the only search service."
status: "in_progress"
kind: "Agreed Work"
see_also: [{"target":"35c78938-a7ca-40fc-9a43-b8cd6bb746b8","reason":"Owns the repository and local checkout where this work lives."},{"target":"66c093b3-8a71-4111-8f04-33d6aab95079","reason":"Earlier commitment to start on browser-harness; this build runs on Telem only and the commitment was not revisited."},{"target":"919d9854-bd80-4845-aaef-0fef947fbc1f","reason":"Explains the score fields; the judged re-score of the first Pi search is recorded there."},{"target":"9a2b74d6-d0f2-44a5-b6d3-a35fbf465439","reason":"Still owns task choice; the task-difficulty question below bears on it."}]
position: 2048
---
**Kind:** Agreed Work

## Creation — November 14, 2026

### Observed conditions

At about noon Jack asked a Claude Code session to read his recent SearchHack commits and the repository README, because he had said he would build the harness that hour. The assistant found that a full pipeline was already on GitHub `main`, pushed from Alyssa's account (`allyalyssa`) starting 11:21, and that the README described it accurately. The pipeline called models through an OpenAI-compatible API key and the referee called Tavily directly. Jack then said:

> "Okay, looks like my group mate finished up some harness stuff. Um and I'm gonna pick up the harness stuff for now. They're focusing on search."

When the assistant asked for a Tavily key and a model key, Jack answered:

> "I think we should just use t telem only unless you think we should use Tel Aviv as well. I mean I'm open to anything, I'm not married to anything. For models, don't forget we're using Pi as our harness and we're gonna do a custom pie harness. We can use my Pi harness as like an example, right? [...] Um we have codex personal connections, right? So we can utilize that for Astra and also for um Terra."

"Tel Aviv" is a dictation of Tavily.

### Inference and response

Jack's commitments for the harness:

- **Telem is the only search service.** Tavily is called only as a provider inside Telem.
- **Pi is the harness.** Searchers run as headless Pi agents with custom tools, using his own Pi setup as the example.
- **Models come from Codex personal**, Pi's `openai-codex-personal` route, not from API keys.

He named Astra and Terra for that route. Terra is not on it; see below.

[Score One Pi-Run Search on Calatrava Bridges](../2f708580-00da-4bad-a64c-8c318beefbb9/node.md) records the first run under these commitments.

## Where the work stopped — historical first handoff

All code is on the local branch `pi-searcher` in `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`, **uncommitted and not pushed**. The branch starts at `c308b93`. GitHub `main` has moved on since: `25e6db0` from Alyssa's account at 12:27, "shape-aware ensemble lenses, verify agreed finds, two-list join".

**Built and run once:**

- `pi/search-tools.ts`, a Pi extension with `web_search`, `fetch_pages` and `submit` tools. Each call runs `python -m rsis.pi_tool`.
- `rsis/pi_tool.py`, the tool backend. It reuses the repository's Telem client, keeping the spend ledger, pricing and the wikidata.org block in one place, and stores each search's ledger in a locked state file.
- `rsis/pi_searcher.py`, which runs one search as `pi --print --mode json` with discovery off and only the Codex router and search tools loaded. It returns the same log shape as `searcher.attempt`, so the referee and history read it unchanged. `python -m rsis.pi_searcher METHOD TASK` runs and scores one search.
- `rsis/pi.py`, the shared Pi command line.
- `rsis/llm.py`: a role whose model is written `pi:<provider>/<id>` answers through headless Pi without tools.
- `rsis/tavily.py`: with no `TAVILY_API_KEY`, the referee's double-check goes through Telem pinned to Tavily.
- A git-ignored `.env` with the hackathon Telem key, `TELEM_BASE_URL=https://hack.telem.ai/api/router` and `JUDGE_MODEL=pi:openai-codex-personal/gpt-6-sol`. The other model fields are still the example placeholders.

**Not done:**

1. The improver still calls `Chat("improver")` with tool calls. That path raises an error for Pi roles; the improver must become a Pi agent like the searcher.
2. `rsis/loop.py` still calls the old API `searcher.attempt`, not `pi_searcher.attempt`.
3. The searcher omits `check_candidates`, the anchor-and-verify tool the API searcher has.
4. `.env.example` and the README do not mention `TELEM_BASE_URL`. Teammates using the default `router.telem.ai` will get a 401.
5. Nothing is committed, merged with `main` or pushed.

## Open questions

- **Terra.** Codex personal offers Astra, Sol and Luna. Terra 6.1 appears only under the separately billed `openai` provider. The run used Luna on the assistant's guess that Terra was meant as a searcher weaker than the improver. Jack has not chosen.
- **Judge family.** The README's guard keeps the judge outside the improver's model family. On Codex personal, judge and improver are both GPT models.
- **Task difficulty.** In the team discussion a groupmate asked why a frontier model would not answer the tasks easily. Jack answered that searchers are cut off from Wikidata and can only use Telem. The assistant observed that this blocks the lookup route, not the model's memory. Before opening the answer files it recalled 8 of 8 women Chemistry laureates, 6 of 6 UK-born Turing winners and 3 of 3 Palme d'Or and Best Picture films. That is the assistant's recall, not a measured model score. Since then Alyssa's account added an evidence-required rule and harder test tasks.
- **Budget and routing.** Each auto-routed query fans out to seven providers at about $0.028, so the $0.08 per-search cap allows about three queries. Whether the cap should change, or whether cheaper routing is the first lesson the improver should find, is open.
- **Baseline.** The assistant proposed running the seed method on every task to find the ones with room to improve, estimating about ten minutes and $3 of Telem. Jack did not answer before asking for this save.

## Next

Jack asked that the next agent assess the open questions and unfinished items. Before running anything, it should pull the latest search work from `main` and judge whether it is relevant to the Pi path:

> "document where we left off your open questions and not done yet next agent will asses that stuff and pull latest search stuff is it relevatn to us before we run anything? we did recent sifttext commits and also groupmates committed more"

`rsis/llm.py` and `rsis/tavily.py` are the files most likely to conflict with work on `main`.

## Source

Claude Code session `a5499697-1483-4ea4-b150-ec7263fe5161`, November 14, 2026, retained at [artifacts/chats/claude-searchhack-pi-harness.jsonl](artifacts/chats/claude-searchhack-pi-harness.jsonl). Repository state was read with Git and the GitHub API during the session.

## November 14 development — branch delivered

Jack confirmed Terra high for searchers and Astra medium for the improver, then specified Terra-fast and authorized the local Codex Personal hotpatch. The assistant refreshed the installed Pi catalog, enabled Terra in the account registry, and set the Codex compatibility flag for max output tokens. The Pi startup model listing showed ordinary Terra and Terra-fast. SearchHack's local settings select Terra-fast high, Astra medium and the existing Sol low gap judge. No live request established that Terra-fast was accepted or served at priority.

Jack then asked to push the SearchHack branch and document stock Pi login so teammates could use their own Codex accounts. The assistant pushed [pi-searcher at 5f5be36](https://github.com/gojack10/recursive-self-improving-search/commit/5f5be36), including the teammate fixes through 53730e9, Pi searcher and improver dispatch, evidence text and candidate verification, Telem-backed Tavily checks, and the live viewer. The README covers stock Pi with openai-codex and the separate local Codex Personal route. The CLI started. The earlier list of missing integration work above is historical.

**Continuation at branch delivery:** [Run the First Complete SearchHack Iteration](../fee4d2ea-c29d-45fc-8498-2002830f8f8f/node.md). At that point Jack said he would run models on his machine, and no completed iteration or measured improvement had been recorded.

Evidence: November 14 Codex session 01a1dbcf-50f5-7863-8922-e412ff6886fa, including the model listing, CLI startup and successful Git push.

## November 14 development — first iteration completed

The first-iteration child now records the authorized `pi-first` run and reconciliation commit `eab1366`. Ten scored searches and one candidate proposal completed in 351 seconds. Original `v000` and proposed `v001` tied at perfect selection scores; `v000` stayed and scored 0.8357 on held-out tasks. No improvement is established. The merge and viewer-animation commit remain local in this session; runtime files and `runs/` were not pushed by this agent.

At that handoff the next independent harness work was [Reduce SearchHack Iteration Time](../4f4ad38a-2e27-420b-8fa1-0d72b19ce3e5/node.md); the visual branch owns actual-activity visibility and Pi event display. Coordinate shared runner/logging edits. Task-difficulty and answer-key work belongs to the task-selection branch. No new worker has been launched by this save. Source: the first-iteration child's retained conversation and run artifacts.

## November 14 — full corpus delivery

[Run Six Corpus Iterations and Record Their Limits](../b8186822-2aae-4874-9e04-9b1ec191aa33/node.md) records the later run on the replacement 18-task corpus: Terra-fast high searchers, Astra medium improver **and judge**, plain search on every task, and six completed iterations. Both the improver and judge now use the same family by Jack's explicit model selection; the earlier outside-family guard is not satisfied and must not be claimed. The judge is a separate evidence route, not independent model-family confirmation.

[Judge Every Unmatched Answer and Reuse Verdicts](../82df17c2-9999-4aba-9009-91d932430e9f/node.md) and its correction replace capped serial judging with persisted parallel verdicts. The first Pi integration's unfinished items above were delivered before this final run. The previous run folders were deleted with Jack's explicit reset; their notes remain history rather than working replay inputs.

The [published demo](../0915aad5-fdae-435e-9620-e2e38b14d35a/node.md) is on GitHub main at `8e0dec9` with blank example keys, stock-Pi instructions and committed corpus data. The loop is stopped, not running indefinitely. This harness owner stays active through the unresolved speed and interpretation limitations, not because source code is still uncommitted. Source: [corpus/demo conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl).
