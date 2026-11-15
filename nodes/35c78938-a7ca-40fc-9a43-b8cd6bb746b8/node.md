---
id: "35c78938-a7ca-40fc-9a43-b8cd6bb746b8"
name: "Build in the recursive-self-improving-search Repository"
micro_summary: "Records the GitHub repository and local checkout that hold the SearchHack build, and the current gap between them."
status: "in_progress"
kind: "Agreed Work"
scope: "Carry the repository as the build workspace for the SearchHack loop; this work completes when the build outcome is recorded or the workspace is replaced."
see_also: [{"target":"9ec1b5d1-69ee-4649-b30f-680e04c0fed9","reason":"Owns Jack's commitments for the November 14 build that this repository carries out."},{"target":"a7769974-3ff8-4e30-9fd4-975bf08ff6f2","reason":"Records the teammates and the proposed split; the repository is how teammates without Pi take part through GitHub and plain files."}]
position: 13312
---
**Kind:** Agreed Work

## Creation — November 14, 2026

### Observed conditions

In the current Pi session Jack reported that he had made the GitHub repository, that it was on this machine somewhere, and that it should be put into SiftText at some point. He then sent the address: https://github.com/gojack10/recursive-self-improving-search#reading-the-knowledge-tree

The assistant located the local checkout with `fd` at `/Users/jack/Documents/Codex/2026-11-14/how/work/recursive-self-improving-search`. At inspection time its Git state was:

- HEAD `e7b8959a272c02b77cf3309435f8eabc09008331`, "docs: explain how to read the knowledge tree with standard tools".
- Branch `main`, clean, with no remotes configured.
- Non-node files only `LICENSE` and `README.md`; no `rsis` package in that checkout.

GitHub's `main` was ahead of that checkout. The repository API listed `.env.example`, `data`, `methods`, `rsis` and `trees` at the root. Its recent commits included `780cf98e59308556657697180e0492a297ee51d1` "Add recursive self-improving search pipeline" and `684175518d8c3ecda55647ae24a8d5b9a181d8ed` "searchhack: sync accepted SiftText tree (deb3a89a59f0)".

Before this save, `rg` over the SiftText home found no GitHub address or local path for the repository. The recent SearchHack commits `dc8faaaae` and `d5edf7615` recorded the kickoff rubric, the Telem probe, the Telem-settings proposal and the browser-harness start; they did not associate the repository.

### Inference and response

The GitHub repository is the build workspace for the SearchHack loop. It is also the participation route for teammates who do not have Pi: they can work through GitHub and plain Markdown, Python and JSON files on Windows.

The local checkout is not current. It sits under a Codex work directory, has no remote configured, and lacks the pipeline commit that GitHub already has. Do not treat its files as the current build until it is connected to the remote and fetched. The GitHub address above is the durable reference; the local path is where this machine's copy was found.

This node records the workspace and its state at inspection time. It does not record that the pipeline has run, that any hunt has been scored, or that search improved.

## November 14 — checkout connected and visual debugger committed

Later inspection in Pi session `01a1dba0-2171-7284-80b0-361440318b9c` found the same checkout on `pi-searcher`, now with `origin` configured and the `rsis` pipeline present. The earlier no-remote, documentation-only state above is historical, not an instruction to reconnect it. Concurrent integration committed the Pi route and viewer (`097328b` and `5f5be36`). This agent then committed only `rsis/view.html` as `f4acbde`, making the debugger smaller and animating its block-state transitions. It did not push that commit or stage `runs/`.

[Watch SearchHack Run Through a Visual Debugger](../125b3125-6dfd-4a2f-87fd-c4cf6815f5ee/node.md) owns the request, runtime-view limits and outstanding human visual judgment. The repository is an active shared workspace; leave teammates' runtime reconciliation alone when working on the visual layer.

## November 14 — current published workspace

[Publish the Runnable Demo and Recorded Results on Main](../0915aad5-fdae-435e-9620-e2e38b14d35a/node.md) completes the later delivery: requested squash into main at `7e94c0a`, corrected scorer/recordings at `70df637`, and the final supplied screenshots/README at `8e0dec9`. The earlier no-remote, unpushed and missing-pipeline states are historical. `pi-searcher` also remains pushed; it was not substituted for main delivery.

The recorded corpus, methods, tree, raw search/Pi logs and verdict SQLite file are now intentionally committed. Viewing them works without credentials; new searches need local accounts/keys. No API key values or `.env` were intentionally published, and the bounded scan found no matching credentials. The checkout was clean and the loop stopped at final inspection. `artifacts/recursive-self-improving-search` still links the canonical external project rather than a copied archive.

The project contains an earlier snapshot of SiftText's project/KB nodes. This new knowledge save does not silently update that copied tree on GitHub. Source: [later conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl).

## Source

Current Pi session `01a1db79-c926-7284-80b0-36135ff23ffd`, November 14, 2026. Repository inspection used `fd`, `rg`, Git and the GitHub repository API on the same day.
