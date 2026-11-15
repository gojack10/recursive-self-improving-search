---
id: "08dfa32b-ed6d-4559-8682-15893d92334e"
name: "Remove a Requested Ask Result and Keep New Searches Local"
micro_summary: "Records one authorized result deletion and distinguishes ignored ad hoc searches from the published demo corpus."
status: "resolved"
kind: "Agreed Work"
see_also: [{"target":"0915aad5-fdae-435e-9620-e2e38b14d35a","reason":"Follows the public demo delivery; its deliberately tracked corpus is not the ad hoc search data covered by this deletion and ignore request."}]
position: 2048
---
## Creation — November 14, 2026

### Observed conditions
After the earlier corpus/demo save, Jack asked to restart the local server. Later he supplied `http://127.0.0.1:8765/?id=20261114-170739-f3d1` and said "delete this result plz", followed by "make sure search results are gitignored btw".

The local code now had an Ask interface in addition to the recorded corpus. `ASKS` pointed to the project-root `asks/` directory; the two sides of this specific result had already written `A/result.json` and `B/result.json`. The ad hoc judge cache was separate from the recorded demo cache, at `asks/judge_verdicts.sqlite`.

### Response
Remove exactly the identified result and its task-specific cached verdicts, not all searches or the demonstration corpus. Preserve the existing ignore rule and avoid claiming it was newly implemented or pushed by this maintenance action.

## Completion

- The listener on port 8765 was stopped and the viewer relaunched from the canonical checkout with `uv run --no-project python -m rsis.view`. The subsequent startup request returned HTTP 200. This is a startup observation, not a rendered-page or end-to-end Ask evaluation.
- The assistant deleted six SQLite verdict rows with task exactly `20261114-170739-f3d1`, then removed only `asks/20261114-170739-f3d1/`. The directory was absent afterwards and remained absent at Commit-time inspection. Both sides had finished before removal; their answer contents were not copied into this knowledge record.
- `.gitignore` already contained `asks/` as an uncommitted local change when inspected. `git check-ignore -v` identified that rule for result paths, and `git ls-files asks` returned no tracked Ask files. The assistant made no further ignore-file edit. This ignores the ad hoc results and their separate cache; it does not retroactively untrack `runs/corpus/`.
- The deliberately published corpus and `runs/judge_verdicts.sqlite` remain tracked, as Jack previously requested for inspectable demo history. Nothing in this maintenance action removed them, rewrote Git history, or committed/pushed the unrelated local work.

This bounded deletion/local-retention request resolves. It does not claim general deletion controls, a new Ask implementation, deletion from backups, or a new published release.

## Later local workspace observation

At this Commit the shared checkout is dirty with concurrent Ask/browser/model and documentation changes. `rsis/view.py` routes `/` to the Ask page and `/history` to the recorded dashboard, and its Ask model reference is `v013`. Those are source observations, not this assistant's implementation or a measured evaluation. The locally recorded remote main remains `8e0dec9`; no fetch or new publication was performed during this maintenance save. Treat earlier clean-checkout and root-dashboard statements as observations of that published snapshot, not a guarantee about the later local runtime.

## Source and artifacts

[Native conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), Pi session `01a1dc03-df6d-7244-951f-6fc59de7978d`: restart request `9d3320ee`, deletion `6ace37ab`, ignore request `1753f700`, and their following command results. The transcript is retained once under the SearchHack root and linked here; it contains the deletion receipt, not a restored result directory. `artifacts/repository` links `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. Do not use this evidence link as a reason to recreate the deleted result.
