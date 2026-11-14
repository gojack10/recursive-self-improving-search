# Recursive Self-Improving Search

SearchHack project exploring whether a search agent can use evidence from previous attempts to improve the way it searches.

- [SearchHack project tree](nodes/5a004683-3bed-443c-98e9-d011b1e0f5c4/node.md)
- [SiftText Knowledge Base](nodes/38a9fc79-8a84-494d-a962-2ec5134bc856/node.md), copied from [SiftText Core](https://github.com/gojack10/sifttext-core/commit/3975312b8f6ede794dd0eefed1c9d2ab77aee19a).

## Reading the knowledge tree

Agents can work directly with the Markdown files in this repo using their usual file tools. SiftText, `rg`, and `fd` are optional.

1. **Start at the root.** Read the [SearchHack project node](nodes/5a004683-3bed-443c-98e9-d011b1e0f5c4/node.md) for project context. For SiftText usage and conventions, start with the [bundled onboarding entry](nodes/5e565245-14fe-406c-977c-cf94a9be246b/node.md).
2. **Walk the tree.** Each node lives at `nodes/<id>/node.md`. Its `children/` directory lists the IDs of its immediate children. Open `nodes/<child-id>/node.md` for each relevant child and repeat as needed. This works even when your checkout or file viewer displays the child links as plain files. Relative Markdown links and `see_also` IDs point to related nodes.
3. **Search if you need a starting point.** Use your file search tool, or run the commands below from the repo root. Search covers both the project tree and the bundled KB. Use the child links to confirm which nodes belong to the project, then read the full matching node for context.

```sh
cat nodes/5a004683-3bed-443c-98e9-d011b1e0f5c4/node.md
ls nodes/5a004683-3bed-443c-98e9-d011b1e0f5c4/children
find nodes -name node.md -type f -exec grep -inF 'recursive search' {} +
```

To update an existing project node, edit its `node.md` and preserve its UUID and placement in the tree. Commit the edit through the team's GitHub workflow.

## What the pipeline does

The searcher that searches for how to search. A search method is a frozen JSON file: instructions for the searcher plus a routing policy over Telem's providers (which engines, auto-routing or pinned, tier, results per provider, domain and date filters, batch query variants, when to fetch). Each round:

1. **Train.** The current method runs two train hunts. Every web call goes through Telem, one Telem session per attempt.
2. **Improve.** The improver reads the score table, the Telem provider-yield table and the losing logs, writes lessons as nodes, and proposes candidate methods. It searches the history tree and the web *with the current method*, so a better method also makes a better improver.
3. **Select.** The current method and each candidate run the same two unseen select hunts at the same Telem budget. The best one is adopted only if it beats the current method.
4. **Test.** The round's winner re-runs on the four fixed held-out test hunts. That re-run is the curve we plot, which guards against a lucky best-of-k pick.

The seed method `v000` is Telem's own auto-routing with a plain agent, so the curve shows how far a learned routing policy gets past Telem's default.

**Hunts.** Twelve "find every X" hunts across people, works and structures (`rsis/hunts.py`). Each answer set is computed from Wikidata and cached in `data/hunts/`. Searchers never see it, and `wikidata.org` results are dropped in the Telem wrapper.

**Referee.** Finds are matched to Wikidata labels and aliases. A find Wikidata lacks gets an independent check through Tavily (a separate route from the searcher's Telem calls) and a judge model outside the improver's model family. Score = (correct - 0.5 x wrong) / answer-set size. Duplicates don't count. Every find must cite a URL that the attempt actually retrieved through Telem (search result, verify check or fetched page). A find recited from memory counts as wrong, so the score measures search, not model knowledge. Only the closed-book contestant in `compare` is exempt. The `hadid` answer set includes Wikidata items such as individual stations named after places ("Alpenzoo", "Hungerburg"), so no contestant's ceiling there is 1.0. We disclose that and do not prune it.

**X-and-Y hunts.** Every hunt is "items that meet condition X and condition Y" (Hugo *and* Nebula, astronaut *and* physician). Each hunt names its two conditions, and the searcher sees them. The fastest reliable way through such a hunt is anchor-and-verify:

1. Pick the side that is easier to list completely (an award's winners, an architect's works) as the anchor.
2. Enumerate it from list pages, using Telem batch query variants and a list-friendly route.
3. Verify the other condition for every candidate with `check_candidates`. It sends one query per candidate in Telem batches of five over a cheap verify route (`routing.verify_providers`).
4. Submit only the candidates that pass.

The referee's judge records whether a wrong find met only X or only Y (`x_only`, `y_only`). The improver sees those counts, so "returned half-matches" is a failure it can learn from. Which side to anchor, and how to route each phase, belong to the method. That keeps them learnable rather than hard-coded: the seed `v000` doesn't use the tactic, and the hand-written `methods/anchor_verify.json` is a reference to trial against.

**Plateau matrix.** If the winner's test re-run doesn't beat the best so far by more than the noise band for two rounds in a row, the next round is a breakout round: fresh improvers, each given a different slice of history and a different earlier version. Two breakouts in a row without a gain stops the run as "levelled off".

**Recursion test.** Generations 0, 3, 6... each get the same improvement job: start from `v000`, with history (attempts, lineage, provider yield, tree nodes) frozen at the end of round 1, and the same budget. Only the method the improver searches with changes. The improver's prompt always shows `v000`, so it can't just copy generation N's text; generation N only drives its searches, and the number of searches it ran is recorded. The improver never sees test-pool scores. Rising successor scores mean the system got better at improving, not only at searching. Flat bars mean continual learning, and we report it that way.

**Records.** Attempts are numeric rows in `runs/<name>/attempts.jsonl`. Method versions, lessons, rounds and adoptions are nodes in the SiftText `node.md` layout under `runs/<name>/tree/`, kept apart from the synced `nodes/` tree.

## Running it, step by step

Needs Python 3.10+ and nothing else (standard library only).

1. Copy `.env.example` to `.env`. Fill in `TELEM_API_KEY`, `TAVILY_API_KEY` and an OpenAI-compatible endpoint (`LLM_BASE_URL`, `LLM_API_KEY`). Set the model IDs your endpoint uses for the searcher (Terra 6.1, high), the improver (GPT 6 Astra, medium) and the judge.
2. Check every key and model with one cheap call each:
   ```
   python -m rsis smoke
   ```
   It also tries each Telem provider name. Remove from `SEARCH_PRICE` in `rsis/telem.py` any provider that returns an error.
3. (Optional) Rebuild the answer sets from Wikidata. They are already committed.
   ```
   python -m rsis build-hunts
   ```
4. Measure the noise band. This runs `v000` three times on the four test hunts. A failed attempt scores 0 and is logged to `runs/main/errors.jsonl`; check that file if a score looks off.
   ```
   python -m rsis calibrate --name main
   ```
5. Run the loop. It stops early at the spend cap or when it levels off.
   ```
   python -m rsis run --name main --rounds 6 --max-spend 20
   ```
6. Compare against the frontier model: `python -m rsis compare --run main`. Then run the recursion test on the adopted generations, for example:
   ```
   python -m rsis recursion-test --name main --gens v000 v003 v006
   ```
7. Open `runs/main/report.html`. It shows the test curve against the Telem auto-routing baseline, the recursion bars, Telem provider yield (correct finds per dollar for each provider) and the method lineage.

`python -m rsis round --name main` runs a single round.

To test a search tactic by hand, write a method JSON and run it head to head against others on the same hunts and budget:
```
python -m rsis trial methods/v000.json methods/anchor_verify.json --hunts turing_uk abel --repeats 2
```
It prints score, correct, wrong, x_only, y_only and Telem spend for each method. Attempts go to `runs/trials/`.

## Beating a frontier model

`python -m rsis compare` puts our system against a frontier model on the held-out test hunts, all scored by the same referee:

| contestant | what it is |
|---|---|
| `frontier-closed-book` | `FRONTIER_MODEL` (e.g. Opus or GPT Astra) answering from memory, no search |
| `frontier+our-method` | the frontier model running our best method in one attempt with the ensemble's whole Telem budget |
| `ours-method` | the cheap searcher with the best evolved method (or `methods/anchor_verify.json` if no run exists) |
| `ours-ensemble` | three cheap searchers with that method, each through a different lens (anchor on X, anchor on Y, recall then verify). Finds that two searchers agree on are kept; the rest go through batched Telem verification and a judge before submission |

Why the ensemble should win on accuracy:
- **Recall:** different anchors and memory recall find different items, and the union covers more of the answer set than one pass.
- **Precision:** every find needs agreement or a verified search result, so half-matches and recalled-but-wrong items get dropped. A closed-book frontier answer has no such check.
- **Cost:** cheap verify routes keep it affordable, at about $0.30 of Telem per hunt.

This is a design argument, not a measured result; the table comes from the first real run. `frontier+our-method` gets the same Telem budget as the ensemble, so a win can't come from extra spend alone. Each contestant runs each hunt twice by default (`--repeats`). Finds the judge accepted as Wikidata gaps are printed for a hand check before any score is quoted.

**Number for the slide:** the final method's held-out test score minus `v000`'s, each run three times under evidence-required scoring, shown against the noise band, with the closed-book score beside it.

**Framing for Telem:** `v000` is Telem's default routing. The evolved method is expressed entirely in Telem knobs (providers, tier, batch queries, verify route), so it is a tuning layer on top of Telem's router rather than a replacement. Show the Telem console trajectories for `v000` and the winning method side by side; the session IDs are in `attempts.jsonl`.

```
python -m rsis compare --run main -n 3
```

## Budget

The Telem spend cap is $0.08 per attempt (`ATTEMPT_BUDGET`), so a cheaper route buys more searches. A round at k=2 runs 12 attempts plus one improver session: at most about $1.06 of Telem and up to 144 Tavily credits. Calibration (12 attempts), six rounds and a three-generation recursion test (12 attempts) come to at most about $8.30 of Telem, well inside the $50 credit. Telem costs are estimated from the published per-provider prices; the console has the exact figures.
