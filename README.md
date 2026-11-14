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

**Question shapes.** Scored hunts cover several "times X and Y happened" shapes, so a better method has to be better across them (`FRAMES` in `rsis/hunts.py`):

| shape | example hunt |
|---|---|
| intersection | novels that won both the Hugo and the Nebula |
| triple | women who are both astronauts and physicians |
| negation | Hugo winners that did *not* win the Nebula |
| sequence | astronauts who later sat in a national legislature |
| events | air disasters with 300 or more deaths |

**Open hunts** (`rsis/open_hunts.py`) push the same shapes into niche territory where no answer key exists, such as reported dogs that swallowed something at a beach and needed a vet, studies that contradict the "three-second goldfish memory" claim, or lightning strikes during a live football match. There is no recall score. Every find must cite a URL the attempt retrieved, then passes a Tavily check and a judge on both conditions, and the result is "how many verified". One stress test (a dog eating a pickle on a beach in its owner's arms) probably has zero real cases, so it measures whether the system invents answers. Open hunts are demo pieces and stay out of the loop's scores.

The ensemble picks its three lenses by shape. For "X but not Y" it subtracts the Y list from the X list rather than anchoring on "not Y"; for sequences it anchors on the later, rarer step; for events it starts from lists sorted by the number or date. Every candidate is verified, including those two searchers agreed on, because two searchers can submit the same half-match. Agreed finds survive unless the checks show they fail a condition; single finds need positive evidence.

Two hand-written methods are there to trial against the evolved ones: `methods/anchor_verify.json` (enumerate one side, verify the other per candidate) and `methods/two_list_join.json` (fetch both lists in full and join them). `data/aliases.json` adds alternative names for answers whose Wikidata label nobody would search for, and drops one duplicate (Pan Am N736PA is an aircraft in the Tenerife disaster, which is already in the set). It was written before any live run.
```
python -m rsis.open_hunts methods/anchor_verify.json --hunts goldfish_memory_rebuttals dog_pickle_beach
```

**Plateau matrix.** If the winner's test re-run doesn't beat the best so far by more than the noise band for two rounds in a row, the next round is a breakout round: fresh improvers, each given a different slice of history and a different earlier version. Two breakouts in a row without a gain stops the run as "levelled off".

**Recursion test.** Generations 0, 3, 6... each get the same improvement job: start from `v000`, with history (attempts, lineage, provider yield, tree nodes) frozen at the end of round 1, and the same budget. Only the method the improver searches with changes. The improver's prompt always shows `v000`, so it can't just copy generation N's text; generation N only drives its searches, and the number of searches it ran is recorded. The improver never sees test-pool scores. Rising successor scores mean the system got better at improving, not only at searching. Flat bars mean continual learning, and we report it that way.

**Records.** Attempts are numeric rows in `runs/<name>/attempts.jsonl`. Method versions, lessons, rounds and adoptions are nodes in the SiftText `node.md` layout under `runs/<name>/tree/`, kept apart from the synced `nodes/` tree.

## Running it, step by step

Needs Python 3.10+ (standard library only), Node.js 22.19+, and Pi for subscription-based model calls.

### Install Pi and connect your own Codex account

Install [Node.js](https://nodejs.org/) and [Python](https://www.python.org/downloads/) if needed, then:

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi
```

Inside Pi, enter `/login`, select **OpenAI (ChatGPT Plus/Pro)** / **openai-codex**, and finish the browser sign-in with your own account. Exit Pi after login. Credentials stay in your local Pi setup; do not commit or share them.

From this repository, copy `.env.example` to `.env` (`cp .env.example .env` on macOS/Linux, `Copy-Item .env.example .env` in PowerShell). Fill in `TELEM_API_KEY`. The example uses stock Pi's `openai-codex` provider, so no custom account router or model API key is required. `TELEM_BASE_URL` is the hackathon router. Tavily evidence checks also go through Telem; no separate Tavily key is needed.

```dotenv
SEARCHER_MODEL=pi:openai-codex/gpt-6.1-terra
SEARCHER_EFFORT=high
IMPROVER_MODEL=pi:openai-codex/gpt-6-astra
IMPROVER_EFFORT=medium
JUDGE_MODEL=pi:openai-codex/gpt-6-sol
JUDGE_EFFORT=low
```

Use `pi --list-models 'openai-codex'` to see models your installed Pi exposes. If Terra is missing, update Pi before running. Both the searcher and improver run as Pi agents using this repository's tools; the judge runs through Pi without tools. The same-family judge is a separate evidence check, not independent model-family confirmation.

**Jack's machine:** the same code also accepts `pi:openai-codex-personal/gpt-6.1-terra-fast` for the searcher and `pi:openai-codex-personal/gpt-6-astra` for the improver. Only that provider loads `~/.pi/agent/extensions/codex-workspaces.ts`. The `-fast` aliases belong to Jack's custom router; stock Pi users should use the ordinary IDs above. Keep these personal overrides in the untracked `.env`.

### Run the pipeline

For the live local viewer, run `python -m rsis.view` and open `http://127.0.0.1:8765`.
It reads the run files; add `?run=<name>` to follow one run.

1. Finish the local `.env` setup above. The existing API path also remains available: use plain model IDs and configure `LLM_BASE_URL` / `LLM_API_KEY` instead of `pi:` roles.
2. Check every key and model with one cheap call each:
   ```
   python -m rsis smoke
   ```
   It also tries each Telem provider name. Remove from `SEARCH_PRICE` in `rsis/telem.py` any provider that returns an error.
3. (Optional) Rebuild the answer sets from Wikidata. They are already committed.
   ```
   python -m rsis build-hunts
   ```
4. Measure the noise band. This runs `v000` three times on the four test hunts. An attempt that fails for infrastructure reasons (API errors, timeouts) is logged to `runs/main/errors.jsonl` and left out of averages, and comparisons use only hunts that every side completed. An attempt the method itself breaks (for example by overflowing the model's context) scores 0.
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

## Proposed pilot questions

These nine questions are a proposed pilot for the demo. The executable benchmark uses the train, select, and test pools in [rsis/hunts.py](rsis/hunts.py).

For each question, return the total, list each qualifying record once, and cite evidence for every record. The difficulty labels describe the expected search work. Both methods use the same model, Telem configuration, and query and page-fetch limits.

- **Development (4 questions).** The learning loop can review these runs and their scores to diagnose misses and revise the search method.
- **Held-out evaluation (5 questions).** Keep these questions and their results out of the learning loop. Once the learned method is frozen, run both the starting method and the learned method on the same five questions. Keep the verified answer keys in the evaluator and score verified matches, misses, and false positives.

| Difficulty | Split | Question |
| --- | --- | --- |
| Easy | Development | How many crewed missions flew in NASA's Gemini program? List the mission designations. |
| Easy | Held out | How many men's FIFA World Cup editions from 1930 through 2022 were won by a host nation? In a co-hosted edition, either host qualifies. |
| Easy | Development | How many individual people had received the Nobel Prize in Chemistry twice by the end of 2024? |
| Medium | Held out | How many men's FIFA World Cup finals through 2022 were decided by a penalty shootout? |
| Medium | Development | How many distinct films won both the Cannes Palme d'Or and the Academy Award for Best Picture through the 2025 Oscar ceremony? Count only Cannes awards named Palme d'Or. |
| Medium | Development | How many separate Apollo missions landed astronauts on the Moon? List the mission numbers. |
| Hard | Held out | How many astronauts flew on a crewed Gemini mission and later traveled to the Moon on an Apollo mission? Include lunar flybys, orbits, and landings. Count each person once. |
| Hard | Held out | How many drivers had won both the Formula 1 World Drivers' Championship and the Indianapolis 500 by December 31, 2024? Count each driver once. |
| Hard | Held out | How many men's FIFA World Cup finals from 1930 through 2022 went to extra time? Include finals that subsequently went to penalties. Count only editions with a final match. |

If a held-out question is used to tune the method during a pilot or demo rehearsal, move it into development and replace it with a fresh evaluation question.
