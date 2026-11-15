---
id: "1347dcde-fa33-4933-9769-8d9386808b21"
name: "Separate Evidence-Gate Failures From Missing Search Answers"
micro_summary: "Explain how the original name gate and snippet judge distorted the first live comparison."
status: "resolved"
kind: "What We Learned"
see_also: []
position: 1024
---
## Observed conditions

Jack pasted a Turing Award/asteroid comparison: both methods handed in six names, but ours showed one confirmed and plain search four. Three of ours failed before the model judge with “source does not name it.” Inspection found two separate stages: a string gate requiring every number and a distinctive name word in retrieved text, then GPT-6 Astra at medium effort ruling from a Tavily-pinned search through Telem and five 300-character snippets, with one possible follow-up search. The gate’s normalization strips parenthesized content; decorated answer labels and asteroid numbers could therefore fail even when a person was named. The model did not receive the searcher’s cited page text. Searching a decorated answer plus the entire question often returned biographies that omitted the asteroid fact.

The assistant’s relaxed checks on saved text were diagnostic, not corrected final verdicts. The original Ask directory `20261114-170739-f3d1` was later absent during implementation; its pasted output and inspections survive in the retained dialogue, not as a recovered original directory.

## Inference and response

A lower confirmed count could reflect bad evidence handling rather than fewer true members found. The assistant initially defended snippets/full-page fetch over the browser harness because of speed and replication. Jack corrected the deployment assumption: this demo runs on his laptop, and he wanted an Astra able to browse iteratively. The browser-judge work follows that choice. The historical scorer `rsis/referee.py` was left intact rather than silently changing the published corpus’s judging basis.

The assistant previously asserted the judge was unlikely to accept false answers and inferred that method 7’s caution was learned because of the old judge. Neither error rate nor that causal learning history was measured. They remain hypotheses, not findings from this comparison. A later page-reading comparison genuinely had plain search submit six and v007 three; the gate problem is not an excuse for every loss.

## Completion

The distinction between search coverage and judging failures is recorded with the observed failure mechanisms. It does not certify any judge infallible or revise the 62%→85% corpus figures.

## Sources and artifacts

Pi session `01a1dca5-5a49-7752-b607-0409d8641da4`, November 14, 2026 local time, from the hackathon retrospective through the manual-method results and Jack’s Commit request `f87d5484`. Full native transcript: [retained dialogue](artifacts/chats/pi-searchhack-live-ask.jsonl).

[Project checkout](artifacts/repository) → `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. This is an external working directory, not an immutable release.
