# RSIS: Recursive Self-Improving Search

![RSIS: search that improves itself, built on Telem](docs/rsis-thumbnail.png)

RSIS is a search agent that rewrites its own search method. It answers "find every X" questions, sees how it scored, writes down what it learned, proposes a new way to search, and keeps the new way only if it scores better. Built for SearchHack on [Telem](https://telem.ai).

## See it in two minutes (no accounts, no API keys)

A full recorded run is committed in `runs/corpus/`. The viewer only reads those files.

```sh
git clone https://github.com/gojack10/recursive-self-improving-search
cd recursive-self-improving-search
python3 -m rsis.view
```

Open <http://127.0.0.1:8765>. You need Python 3.10 or newer and nothing else. `uv run --no-project python -m rsis.view` works too.

What is on the screen:

| Part | What it shows |
|---|---|
| Question bar | The question being shown. Click a question to see only that one; "All unseen questions" is the average over the questions the method never practised on. |
| Lights | How many agents are searching, whether new methods are being written, and how far the judge is through its checks. |
| What is happening now | Left: the loop. Right: the steps one agent goes through; each dot is one running agent. |
| Tree | Every method tried, with its number and a short name. Green tick: kept. Red cross: dropped. Entries marked "learned" are the lessons the next methods were written from. |
| Score | Our method (green) against plain search (orange, dashed) at the same search budget. "Show answers" puts plain search's answer list beside ours. |

## What the recorded run shows

Plain search is method `v000`: an ordinary agent using Telem's default routing. Every later method was written by the system itself.

| Round | Method in use | Score on the 5 unseen questions |
|---|---|---|
| start | plain search (`v000`), 3 runs | 62% |
| 1 | `v002` | 69% |
| 2 | `v003` | 72% |
| 3 | `v006` | 77% |
| 4 | `v007` | 82% |
| 5 | `v007` (no change) | 79% |
| 6 | `v012` | 85% |

Read this honestly:

- **The score went from 62% to 85%** at the same $0.08 search budget per question.
- **It is not proven beyond noise.** Plain search run three times on the same five questions varied by 26 points, almost all from the two Moon questions. Round 5 repeated method 7 and moved 3 points with no change to the method.
- **All 18 questions share one shape** (an award crossed with a planet). The run shows the method got better at this kind of question, not at search in general.
- **Scores were re-computed once** from the saved answers after the judge was fixed: it had been counting answers it could not confirm as wrong. It now makes a second lookup, and only an answer the evidence contradicts costs points. Which method each round kept was decided on the earlier scores.
- **The system found answers the answer key lacks.** The judge confirmed five, including Muddy Waters (Waters crater, Mercury) and Ariel Durant (Venus). These are added to the answer list for every method, plain search included.

## Plain search against method 7, question by question

Method 7 (`v007`) is the latest method that has answered all 18 questions. Method 12 replaced it in round 6 and has only answered the selection and unseen questions. Both sides had the same $0.08 search budget per question. Scores are averaged where a method answered a question more than once.

| Question | Used for | Answers in key | Plain search | Ours (method 7) | Points |
|---|---|---|---|---|---|
| nobel moon | unseen | 107 | 39% · 42 found · 3 runs | 79% · 84 found · 2 runs | +40 |
| pulitzer mercury | unseen | 11 | 70% · 8 found · 3 runs | 84% · 10 found · 2 runs | +14 |
| grammy mercury | unseen | 13 | 73% · 11 found · 3 runs | 87% · 13 found · 2 runs | +14 |
| nobel physics moon | unseen | 42 | 47% · 20 found · 3 runs | 79% · 33 found · 2 runs | +32 |
| freedom mercury | unseen | 9 | 81% · 7 found · 3 runs | 75% · 7 found · 2 runs | -6 |
| nobel mercury | selection | 17 | 71% · 13 found | 60% · 10 found · 2 runs | -11 |
| nobel venus | selection | 11 | 82% · 9 found | 100% · 11 found · 2 runs | +18 |
| pulitzer venus | selection | 9 | 60% · 6 found | 90% · 9 found | +30 |
| freedom venus | selection | 6 | 43% · 3 found | 86% · 6 found | +43 |
| nobel mars | practice | 10 | 80% · 8 found | 30% · 4 found | -50 |
| oscar venus | practice | 4 | 50% · 2 found | 88% · 4 found · 2 runs | +38 |
| oscar mercury | practice | 4 | 75% · 3 found | 75% · 3 found · 2 runs | 0 |
| grammy venus | practice | 5 | 40% · 2 found | 100% · 5 found · 2 runs | +60 |
| olympic venus | practice | 1 | 0% · 0 found | 100% · 1 found · 2 runs | +100 |
| rock hall venus | practice | 1 | 100% · 1 found | 100% · 1 found | 0 |
| rock hall mercury | practice | 4 | 80% · 4 found | 100% · 5 found | +20 |
| kennedy venus | practice | 2 | 100% · 2 found | 100% · 2 found | 0 |
| kennedy mercury | practice | 4 | 100% · 4 found | 62% · 3 found | -38 |
| **Average, 5 unseen** | | | **62%** | **81%** | **+19** |
| **Average, all 18** | | | **66%** | **83%** | **+17** |

- Method 7 is ahead on 11 questions, level on 3 and behind on 4.
- "Found" is correct answers. The score also subtracts half a point for each answer the evidence contradicts or that cites a page not mentioning it.
- Only the five "unseen" rows are a fair test. Method 7 was chosen using the selection questions, and the practice questions fed the lessons it was written from.
- Every question in this corpus has an answer key. The viewer's "Show answers" button lists both sides' answers for any question.

## How it works

One search method is one JSON file: instructions for the searching agent plus a routing policy over Telem's search providers (which engines, how many results, when to read a page).

Each round:

1. **Search.** The method in use answers two practice questions.
2. **Write new methods.** A method-writer agent reads the scores, the lessons so far and the failed searches, writes new lessons, and proposes two new methods. It does its own research with the method in use, so a better search method is also a better tool for writing the next one.
3. **Pick the winner.** The method in use and both new methods answer the same two selection questions at the same budget. A new method is kept only if it beats the method in use.
4. **Score unseen questions.** The winner answers five questions that are never used for practice or selection. That score is the line on the graph.

Before round 1, plain search runs on every question, so each question has a baseline to compare against.

**Scoring.** Each answer must cite a page the agent actually retrieved, and that page must mention the answer. Answers that match the answer key by name are marked correct. Every other answer goes to a judge model, which looks it up through a separate search route and rules it correct, wrong, or another name for a known answer. Verdicts are stored in `runs/judge_verdicts.sqlite` and reused, so each distinct answer is judged once.

`score = (correct - 0.5 x wrong) / number of answers`

The number of answers is the answer key plus anything the judge has verified that the key lacks. A question with no answer key is scored against the best verified list found so far.

**Questions.** `data/questions.json` holds 18 questions: 9 for practice (`train`), 4 for selection (`select`) and 5 unseen (`test`). Add your own by adding an entry with a `question`, a `pool`, and an optional `answers` list.

**When a run stops.** At the round limit, at the spend cap, or when it has levelled off (two "breakout" rounds in a row with no gain). `--keep-going` ignores the levelled-off stop.

## Run it yourself (needs accounts)

You need Python 3.10+, Node.js 22.19+, [Pi](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) signed in to a ChatGPT account, and a Telem API key.

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi                      # enter /login, choose OpenAI (ChatGPT Plus/Pro), sign in, then exit
cp .env.example .env    # then put your Telem key in TELEM_API_KEY
```

`.env` is ignored by git. Never commit it.

```sh
python3 -m rsis smoke                                  # one cheap call per key and model
python3 -m rsis run --name mine --rounds 4 --max-spend 10
python3 -m rsis.view                                   # watch it live
```

Running the same `run` command again resumes the run: `--rounds` means that many more rounds. The round in progress when a run was interrupted starts over.

| Command | What it does |
|---|---|
| `run --name N --rounds R` | Measure plain search, then run up to R rounds. |
| `round --name N` | One round. |
| `trial METHOD.json --hunts Q1 Q2` | Run one or more method files on chosen questions, outside the loop. |
| `calibrate --name N` | Run the method in use three times on the unseen questions to measure run-to-run spread. |
| `recursion-test --name N --gens v000 v003` | Give the method writer the same job using different generations' search methods. Not run in the recorded run. |
| `compare --run N` | Our method against a frontier model answering from memory. Not run in the recorded run. |

Models are set per role in `.env` (`SEARCHER_MODEL`, `IMPROVER_MODEL`, `JUDGE_MODEL`). The recorded run used GPT Terra for the searchers and GPT Astra for the method writer and the judge. The judge and the method writer are the same model family, so the judge is a separate evidence check, not an independent one.

## What is recorded

Everything the viewer shows comes from `runs/<name>/`:

| File | Contents |
|---|---|
| `attempts.jsonl` | One row per scored search: question, method, score, counts, spend, time. |
| `rounds.jsonl`, `state.json` | Each round's result and the run's current state. |
| `methods/` | Every method the system wrote. |
| `tree/`, `tree_events.jsonl` | Rounds, methods and lessons as a tree, and each change to it in order. |
| `logs/<id>.pi.jsonl` | Every event of one agent, each with its arrival time. |
| `logs/<id>.judge.jsonl` | The judge's verdict on each answer of one search. |
| `logs/<id>.json` | The answers handed in, the pages retrieved and the scoring detail. |

A replay player is not built yet. The recordings carry the timestamps it needs.

## Known limits

- The gain in the recorded run is inside the measured noise (see above).
- Plain search has one run on most questions and three on the five unseen ones.
- A stored judge verdict is reused even if it was wrong, until its row is deleted.
- The older Wikidata question set (`data/hunts/`, `rsis/hunts.py`) is only used when `data/questions.json` is absent.
- `rsis/open_hunts.py` and `rsis/ensemble.py` are earlier experiments and were not part of the recorded run.

## Project notes

The team's working notes are kept as a SiftText tree under `nodes/`.

- [SearchHack project tree](nodes/5a004683-3bed-443c-98e9-d011b1e0f5c4/node.md)
- [SiftText Knowledge Base](nodes/38a9fc79-8a84-494d-a962-2ec5134bc856/node.md), copied from [SiftText Core](https://github.com/gojack10/sifttext-core/commit/3975312b8f6ede794dd0eefed1c9d2ab77aee19a).

### Reading the knowledge tree

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
