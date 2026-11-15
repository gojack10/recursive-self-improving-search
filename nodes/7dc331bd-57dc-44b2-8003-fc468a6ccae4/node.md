---
id: "7dc331bd-57dc-44b2-8003-fc468a6ccae4"
name: "Adopt the Planetary-Naming Corpus and Baseline Every Task"
micro_summary: "Loads the supplied questions and keys, fixes the split, and requires plain search on every task."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"82df17c2-9999-4aba-9009-91d932430e9f","reason":"The pooled judge allows incomplete answer keys and keyless tasks without rejecting every name missing from the supplied list."}]
position: 1024
---
## Creation — November 14, 2026

### Observed conditions
The earlier tasks tied at perfect selection scores. Jack's first paste of 18 award/planet questions was damaged: names and question text were cut or merged. The assistant temporarily seeded eight intact questions and ran `questions-baseline` in 206 seconds. That provisional corpus was not the final set.

Jack then supplied `/Users/jack/Downloads/questions.json` and `/Users/jack/Downloads/keys.json` and explicitly requested clearing all old data and runs. The assistant removed the five previous run directories and verdict store, adopted the clean file's 18 tasks, and started a new run named `corpus`. Counts and wording from the earlier damaged paste are not authoritative. In particular, clean question 12 is Nobel Physics/Moon with 42 names, not the zero-answer First Ladies question from the paste.

### Chosen application
`data/questions.json` becomes the whole executable corpus when present. Each entry has a name, question, optional answer list/aliases and a pool. No answers means the judge builds the known verified pool; none of the 18 supplied tasks is actually keyless. Unique crater feature names from `keys.json` became aliases for the first four Nobel tasks, avoiding ambiguous shared feature names.

## Completion

### Agent-selected split
The supplied file had no split. The assistant chose this one under Jack's proceed instruction:

| Pool | Tasks and supplied key sizes |
|---|---|
| Held-out (`test`) | Nobel/Moon 107; Nobel Physics/Moon 42; Pulitzer/Mercury 11; Grammy/Mercury 13; Medal of Freedom/Mercury 9 |
| Selection (`select`) | Nobel/Mercury 17; Nobel/Venus 11; Pulitzer/Venus 9; Medal of Freedom/Venus 6 |
| Training (`train`) | Nobel/Mars 10; Oscars/Venus 4; Oscars/Mercury 4; Grammy/Venus 5; Olympic/Venus 1; Rock Hall/Venus 1; Rock Hall/Mercury 4; Kennedy/Venus 2; Kennedy/Mercury 4 |

Every task intersects an award/recognition list with IAU planetary naming. The split supports within-domain comparison, not a claim of general search transfer. The judge later accepted five task-answer gaps in the keys; key lengths and final denominators can differ.

### Baseline correction
The loop originally calibrated `v000` on the five held-out tasks, then stopped using it once it adopted a new method. Consequently nine tasks had no plain-search comparison. Jack corrected that explicitly: "plain search MUST be run per each one" and "should be default". A separate 150-second job filled those nine missing baselines. `loop.baseline` now runs `v000` on any corpus task without a recorded plain-search row before `run`, including resume, and the single-iteration CLI path calls it too.

At final inspection all 18 have a baseline. The held-out five have three baseline searches apiece; the other 13 have one. Method 7 also has results on all 18, after a separate completion batch. This requirement is not satisfied merely by showing an orange line when no row exists.

Loading, splitting and minimum baseline coverage completed. The original research request for trustworthy, broadly difficult tasks is not thereby proven fulfilled: these are supplied lists, not independently validated keys, and the domain is narrow.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl): clean file paths `4a10c050`, reset/proceed `1816c6ed`, baseline corrections `49cafd8b` and `95cf8642`. `artifacts/repository` links the checkout; the canonical transformed corpus is committed as `data/questions.json`. Downloads are source inputs kept in place, not the runnable corpus. No new file movement or old-run recovery is claimed.
