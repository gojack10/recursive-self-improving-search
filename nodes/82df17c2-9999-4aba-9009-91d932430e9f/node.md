---
id: "82df17c2-9999-4aba-9009-91d932430e9f"
name: "Judge Every Unmatched Answer and Reuse Verdicts"
micro_summary: "Replaces capped serial checks with bounded parallel judging and stored per-task verdicts."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"72cfa59a-de11-4374-8049-6ba0e76c6061","reason":"Decided from the latency diagnosis that serial referee calls dominated the first iteration."}]
position: 1024
---
## Creation — November 14, 2026

### Observed conditions
Jack selected Astra for the judge, corrected low effort to medium, and later explicitly kept that selection. Local `.env` changed from Sol low to Astra medium. The next one-candidate iteration, `pi-second`, took 454 seconds; its selection tasks again tied at 1.0. The longer judge waits in that run do not isolate model speed because the submitted answers differed.

The scorer already had two paths: deterministic name/alias matches against the answer key, then a model judge for unmatched answers with retrieved evidence. The cap of 20 gap checks applied separately to each search, not globally. Every eligible answer after the twentieth was nevertheless marked wrong unseen. Jack initially understood the cap as a runaway guard, then selected checking every unmatched answer and storing verdicts so repeat answers would not need judging again:

> "we should just do it for all of them, especially if we don't know if the answer is right or wrong"

### Decision
Use Astra medium. Run gap checks concurrently, remove the 20-check cap, persist judged answers per task, and make the logs and state machine show scoring progress. Keep Telem as the only search service; judge lookups use Telem pinned to Tavily.

## Completion

### Delivered behavior
`rsis/referee.py` uses a shared pool of 10 judge workers by default (`JUDGE_WORKERS`) and writes normalized per-task answer verdicts to `runs/judge_verdicts.sqlite`. The remaining 3,000-credit Tavily guard is per process and resets on process restart. `rsis/loop.py` emits per-search plan/start/end/done events in `logs/<id>.judge.jsonl`; the viewer shows progress and reused verdicts. The judge's model transport remains Pi text mode, not a saved stream of its own internal Pi turns.

An answer that matches the key is scored deterministically. Eligible unmatched answers go to the judge, and stored verdicts are reused. All tasks can be loaded with or without keys: the score's denominator is the key plus the pool of verified missing answers. For a keyless task that pool is the whole known answer set. Newly verified answers therefore affect every method's denominator, not just the discoverer's numerator.

### Limits and successor
This first implementation still counted unsuccessful confirmation as wrong, and stored those rejections. [Correct Unconfirmed-Answer Penalties and Re-score the Corpus](../bd434935-7e66-4ef0-81e2-e835905031ea/node.md) supersedes that part after Jack challenged its effect. Concurrent checks can also insert different spellings of the same newly discovered person before either is in the pool; no complete within-batch canonicalization was demonstrated. Reused verdicts are model judgments, not infallible facts.

Code and progress events shipped; this unit resolves for the implementation, not for correctness of every verdict or the speed target. First judge commit: `b6708e1`; subsequent pooled/file-question work was integrated on `main`.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), effort correction `f7f0cdc9`, parallel approval `3b3d0c58`, uncapping/cache request `f349330f`. `artifacts/repository` links the existing project checkout; inspect `rsis/referee.py`, `rsis/loop.py`, and `runs/judge_verdicts.sqlite` in place. No credentials belong in this knowledge or the published repository.
