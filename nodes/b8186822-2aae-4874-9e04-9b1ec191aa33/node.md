---
id: "b8186822-2aae-4874-9e04-9b1ec191aa33"
name: "Run Six Corpus Iterations and Record Their Limits"
micro_summary: "Records the corpus trajectory, continuation overrides, baseline comparison and the limits of re-scored results."
status: "resolved"
kind: "Probe"
see_also: [{"target":"7dc331bd-57dc-44b2-8003-fc468a6ccae4","reason":"Uses the replacement 18-task corpus and its train/selection/held-out split."},{"target":"bd434935-7e66-4ef0-81e2-e835905031ea","reason":"The numerical results below use its retrospective corrected referee, not the scores used to choose the historical winners."},{"target":"420ced74-9291-45ef-b2ec-546f2224c283","reason":"Applied the original plateau defaults, then continued with the explicitly described agent-side overrides."},{"target":"240a8b42-07e1-47b2-a20f-75214f3c8b43","reason":"The presentation evidence capture reads the same re-scored run, not an independent replication; this Probe records execution and continuation details."}]
position: 4096
---
## Creation — November 14, 2026

### Observed conditions
The previous one-candidate runs (`pi-first`, 351 seconds, and `pi-second`, 454 seconds) both kept `v000` after perfect-score selection ties. Jack supplied a clean corpus, authorized resetting data, and asked to iterate. The assistant started `corpus` with up to eight iterations, two candidates per iteration and a $30 estimated search-spend cap. Searchers used Terra-fast high; improver and judge used Astra medium through Codex Personal. All search traffic, including Tavily judge lookups, went through Telem.

The initial job finished after four iterations in 2,149 seconds, stopping on the plateau rule rather than an API failure. It had measured a 0.2605 noise band from three plain-search runs of the five held-out tasks. Later Jack authorized another 20 iterations. The assistant added `--keep-going`, changed this run's `noise` to zero, retained `measured_noise=0.2605`, reset plateau counters, and raised the cumulative estimated search-spend ceiling to $40. Jack authorized continuation, not a new empirically validated noise rule; setting the band to zero was the assistant's implementation choice.

Several restarts for scoring and method-title changes discarded unfinished iterations. The final continuation completed iteration 6 before being stopped for the submission-time re-score. Twenty additional iterations did not complete.

## Completion — recorded results

After the [referee correction](../bd434935-7e66-4ef0-81e2-e835905031ea/node.md), saved `state.json` reports:

| Iteration | Method in use | Held-out mean |
|---|---|---:|
| Plain search (`v000`), three runs | v000 | 0.6202 |
| 1 | v002 | 0.6909 |
| 2 | v003 | 0.7215 |
| 3 | v006 | 0.7741 |
| 4 | v007 | 0.8187 |
| 5, no new adoption | v007 | 0.7935 |
| 6 | v012 | 0.8495 |

At final inspection there are 112 scored searches and $7.377 of recorded estimated search spend. This excludes judge lookup spend and model/subscription cost; it is not total experiment cost. `v012` is current. No `rsis run` or `trial` process remained at Commit time. An incomplete next iteration can leave an in-progress node and a stale activity indicator; that is not a live worker.

### Like-for-like complete method comparison
Method 7 was separately run on seven missing tasks so one evolved method, rather than a mixture of generations, could be compared on all 18. Averaging repeats within each task, then tasks equally: plain search is 66% and method 7 is 83% across all 18 (11 higher, three equal, four lower). On the held-out five, the corresponding means are 62% and 81%. The README includes every task, including losses.

Method 12 has completed rows on **eight** tasks: five held-out, two selection and one training task. Earlier assistant summaries saying nine or all selection tasks were mistaken. Its 85% is a single held-out pass, not an all-18 aggregate. The question screenshots' large number can therefore differ from the method-7 table and can sometimes be an older method's result where current-method coverage is absent.

### Interpretation and limits
The corrected recorded outcome is a rise from about 62% to 85% at the same $0.08 search budget per task. It is descriptive evidence, not a demonstrated gain beyond noise. The originally measured 26-point spread predates the scoring correction, so it is not a confidence estimate for this revised comparison. Iteration 5 varies by about three points without changing method. All tasks share one award/planet domain; the five designated held-out tasks were repeatedly evaluated and visible to the human directing the work, so they are not a single untouched final benchmark.

The method writer researches with the current method and reads lessons/history. That recursive mechanism is implemented. A growing tree and higher search score do not separately measure an improvement in ability to improve; Jack explicitly did not want the proposed `recursion-test` run. No ablation or counterfactual is claimed. The model weights were not trained.

Re-scoring did not replay adoptions. The earlier scorer, its mistakes, the changing verdict pool and continuation overrides all belong to interpreting the trajectory. The root goal stays open; this Probe resolves because this bounded run and its limits are recorded, not because the thesis is proved.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), initial completion `5012f216`, 20-more request `6bbc4b90`, no-recursion-test request `0d79d8d5`, submission stop/re-score exchanges around `727cd86a` and `3601fa16`. `artifacts/repository` links the checkout. Inspect `runs/corpus/state.json`, `attempts.jsonl`, logs and tree at published GitHub commit `8e0dec9`; the numerical audit was repeated during this Commit without running models or searches.
