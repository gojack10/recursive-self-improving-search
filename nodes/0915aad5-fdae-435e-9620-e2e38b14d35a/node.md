---
id: "0915aad5-fdae-435e-9620-e2e38b14d35a"
name: "Publish the Runnable Demo and Recorded Results on Main"
micro_summary: "Delivers the viewer, corpus recordings and result documentation without credentials."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"b8186822-2aae-4874-9e04-9b1ec191aa33","reason":"Publishes this run's results and records, with their noise and retrospective-scoring qualifications."},{"target":"7c3eef5a-62d9-4385-9f6c-da2acd114a4a","reason":"Publishes the selected dashboard and the screenshots supplied by Jack."}]
position: 1024
---
## Creation — November 14, 2026

### Observed conditions
Jack asked to commit and push the build, then specified "squash merge into main not pi branch", include existing data, and make it usable from a clone: "just work". He reinforced "NO API KEYS". He then supplied a thumbnail, requested an accurate README understandable by an agent or lay reader, a full baseline-versus-ours results table including losses, and five result screenshots linked to the relevant tasks.

## Completion

### Published result
GitHub repository: https://github.com/gojack10/recursive-self-improving-search . The public `main` tip inspected at the save is `8e0dec91235cbf48fee66a598026a8e350437b16`.

| Commit on main | Contribution |
|---|---|
| `7e94c0a` | Initial squash of the Pi harness, scorer, corpus, dashboard, recordings and rewritten README |
| `479eb0b` | Full method-7 comparison, completion searches and corrected baseline-first question chart |
| `70df637` | Corrected judge treatment, re-scored recordings and results through iteration 6 |
| `8e0dec9` | Five supplied result screenshots and README links/captions |

`pi-searcher` was also pushed and remains the local branch. The task was not delivered only there. The local checkout was clean at final inspection; no improvement run was active. Later commits or a resumed run must be inspected afresh rather than inferred from this snapshot.

### Usable entry point
From the repository root, `uv run --no-project python -m rsis.view`, then open `http://127.0.0.1:8765`. The README also gives `python3 -m rsis.view` for humans with Python 3.10+. Viewer startup needs neither a model account nor any key because it reads the committed data. Running new searches does require the user's own Pi login/model access and Telem credentials, configured in local `.env`.

A separate clean checkout of merged main, without `.env` and with a cleared environment, served HTTP 200 and loaded 18 tasks, methods and tree data. This established startup and file loading only, not a rendered-browser or multi-platform usability result. Python code is standard-library based; Node/Pi are needed for new model calls, not viewing saved results.

### Data, privacy and documentation
`runs/corpus/` and `runs/judge_verdicts.sqlite` were committed deliberately, about 218 MB uncompressed at the first snapshot; the repository is correspondingly heavy. The assistant scanned run data against the actual local Telem key and common credential patterns and found no matches. `.env` remains ignored; `.env.example` has blank key fields. This is a bounded scan, not a guarantee that every possible private value was audited. Raw native chat transcripts were not published.

README now explains the loop, keys versus judge pool, accounts needed only for new work, noise, resuming, and unbuilt replay. `docs/rsis-thumbnail.png` is near the top. Jack's five screenshots are `result-all-unseen.png`, `result-nobel-moon.png`, `result-grammy-mercury.png`, `result-freedom-mercury.png`, and `result-pulitzer-venus.png` under `docs/`. Relevant question rows link to them. Their latest/best values need not equal the method-7 repeated-run averages in the table; the README calls out that distinction. Submission to Devpost itself was not observed.

This publication work resolves. It does not complete the separate replay-player or custom-question/model-key UI requests, prove the search gain, or silently sync these newly saved SiftText nodes back into the project's copied knowledge tree.

## Source and artifacts
[Conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), main-delivery request `95cf8642`, no-keys correction `27539adc`, thumbnail/readability `5538d528`, all-results request `db9d3da5`, screenshots `2771b3b7`. `artifacts/repository` links the actual checkout, where Git history, source and image files stay. The SiftText transcript is retained locally once and linked, not copied into GitHub.
