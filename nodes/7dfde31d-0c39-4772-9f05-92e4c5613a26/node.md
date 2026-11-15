---
id: "7dfde31d-0c39-4772-9f05-92e4c5613a26"
name: "The Searcher That Searches for How to Search"
micro_summary: "Develops a search agent that improves its own method by searching its history and the web with that same method."
status: "in_progress"
kind: "Idea"
scope: "Preserve the originating recursive design, its later implementation and evidential limits without treating higher search scores as proof of better improving."
see_also: [{"target":"2f0d64f3-6886-4dc8-8256-81fec882d62c","reason":"Jack's November 13 lean toward calling this continual learning; this node records his November 14 choice of recursion for the hackathon."},{"target":"9a2b74d6-d0f2-44a5-b6d3-a35fbf465439","reason":"Owns the still-unselected task, scorer and comparison this design depends on."},{"target":"f12a53f8-8dc2-4c1b-b482-cfde6778d2bb","reason":"Research findings that shaped the improver, history index and stall trigger proposals."},{"target":"bf8823dd-9e4e-4bed-8430-ca258d5471fd","reason":"Jack approved a light form of this model for the nodes the hackathon agents write."},{"target":"32e42590-c3cd-42d2-ad59-b2ff06b72f22","reason":"Deferred lineage-and-progress visual; Jack supplied a reference image for the progress side."},{"target":"c5749fc3-e9ea-4a72-84d7-e2fbeac032c5","reason":"Faithful record-keeping and improved later performance remain separate claims."}]
position: 7168
---
**Kind:** Idea

## Creation — November 13–14, 2026

### Observed conditions

Jack resumed SearchHack planning in a Claude Code session on the night before the hackathon. The assistant read this tree and the Chris session that produced [Adapt Retrieval to the Person and the Domain](../2f0d64f3-6886-4dc8-8256-81fec882d62c/node.md). It found no later definition of the project and no record that the planned PoC had run. It proposed paper-finding lookup tasks with known answers, scored across a switch between research fields.

Jack then rejected that direction and chose recursion over continual learning:

> "not sure if i like the paper analogy after sitting with it for a while. ideally we do something grand, this is a hackathon after all. shoot for recursive, not continual because again recusion is the thing that turns heads but im not sure how it could be pulled off and im not sure how i will prove its going recursive, other than "being better than plain nodes.md file""

He attached a reference image from an X post as "exactly the visual i wanted": a prompt x on the left, many sampled paths z fanning right, and a circled region labelled as the set of correct answers that some red paths reach. He also linked the Bespoke Labs post analysed in [Exploration Collapse Findings From RSI-top and Bespoke](../f12a53f8-8dc2-4c1b-b482-cfde6778d2bb/node.md).

The assistant proposed the core: to improve a search method, an agent must search its own record of past attempts and the web for better techniques, so it should do that searching with the method being improved. Generation N's method then produces generation N+1. Jack confirmed: "the searcher that searches for how to search is correct".

### Inference and response

The assistant proposed this mechanism. Except where the Agreed Work linked below says otherwise, it is unselected.

- **Searchers and an improver.** Searchers run the hunt. An improver agent reads the score table, opens a few losing logs, writes lessons as nodes, writes two or three candidate next versions, trials them and keeps the best. It should use the same cheap model as the searchers, so the method rather than model strength does the work.
- **Recursion test.** Beating a notes.md file shows better memory, not recursion. Instead, give generations 0, 3 and 6 the same improvement job (same starting method, failure record and budget) and score the successor each writes. Rising successors would show improved ability to improve; flat bars would mean continual learning, reported as such.
- **Two record layers.** Attempts are numeric rows in a plain table kept in the owning node's artifacts, because hosted Commit is too slow per attempt (from message timestamps, the assistant estimated that the November 13 Chris Commit took about 40 minutes; it saved in four splits). Method versions and lessons are nodes. RSI-top's fixed numeric dashboard is the contrast: here the method that reads the history is itself rewritten.
- **Definitions.** A search is one query; an attempt is one agent's full try at one question or hunt and is one table row. A method version is one frozen instruction node; a new version is a new child, never an edit. Correctness needs a referee rather than a known answer key: an exact or model-judged match for lookups, or source-verified finds for open hunts. The agent never sees answers, and versions are scored on unseen work.
- **Repeated failures.** A script assigns coarse types such as out of budget or unsupported answer. A cheap model matches the failed attempt against existing failure-node cards or returns none; that match is a judgment, not a measurement. Because this is a search over the tree with the current method, a better searcher should also recognise its repeated failures better.
- **Diversity.** Shared history can cause the collapse RSI-top calls context inertia, so searchers should see different parts of the history and build on different lineages, connecting Jack's deferred [Vary Retrieved Evidence and Reading Order](../87e216ba-5f84-408a-a381-c15b71b4937b/node.md).
- **Fit to the day.** The assistant estimated one round at about ten minutes and the build at about four hours. It proposed keeping the live loop, one rising curve and the growing tree, and cutting the idea map, automatic failure matching and the notes.md comparison. It proposed running the recursion test once in the last hour, and treating a fresh knowledge home with a lighter write path as needed so each new version can be saved within about a minute. A flat curve by 2 PM would justify a stronger improver model, disclosed.

The assistant judged SiftText suited to the method-and-lessons layer: its outline cards and on-demand reads resemble RSI-top's look-then-open index, and methods can live in the same store as the history they search. That is an inference from the RSI-top page, not a tested advantage.

## Correction — November 14: decisions moved to Agreed Work

The first save of this node listed Jack's four choices in a "Jack's selections" section here: recursion as the framing, the core design, failure links to nodes and a light state-machine form for agent-written nodes. Under the [Epistemic State Machine](../bf8823dd-9e4e-4bed-8430-ca258d5471fd/node.md), a commitment to act is Agreed Work, not part of an Idea. Jack asked for the fix. Those choices and their quotations now live in the sibling [Build the Hackathon Around the Recursive Searcher](../9ec1b5d1-69ee-4649-b30f-680e04c0fed9/node.md), decided from this node.

This Idea stays in progress for the parts not chosen. The two-layer record split, task choice, recursion test, improver details and day plan above were offered but not selected. No loop was built, no task was run and no improvement or recursion result exists.

## November 14 — mechanism implemented, recursion test unrun

The earlier no-loop/no-result statement belongs to this Idea's first capture. [Run Six Corpus Iterations and Record Their Limits](../b8186822-2aae-4874-9e04-9b1ec191aa33/node.md) now records the implemented mechanism: a method writer uses the current method for research and reads retained lessons/logs to propose successors. The completed searches show a descriptive score gain under a corrected referee, not independent evidence that its improving ability improved.

Jack explicitly did not want the separate `recursion-test` for this demo. That counterfactual and any broader claim about recursion remain unobserved; they are not automatic new work. The public README states that the command exists but was not run. This update records application without turning the historical Idea into Agreed Work or reclassifying the evidence as proof.

Source: [corpus/demo conversation](artifacts/chats/pi-searchhack-corpus-demo.jsonl), `6bbc4b90` and `0d79d8d5`.

## Source

Claude Code session `feef5eb9-2574-4813-9a7a-3a66a476810e`, November 13–14, 2026, retained at [artifacts/chats/claude-searchhack-recursive-design.jsonl](artifacts/chats/claude-searchhack-recursive-design.jsonl). Jack's reference image is retained at [artifacts/reference-visual-samples-of-z.png](artifacts/reference-visual-samples-of-z.png).
