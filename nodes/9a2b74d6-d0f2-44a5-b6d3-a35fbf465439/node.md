---
id: "9a2b74d6-d0f2-44a5-b6d3-a35fbf465439"
name: "Choose the PoC Task and Success Evidence"
micro_summary: "Holds the unresolved workload, comparison, scorer and meaning of recursive improvement."
status: "in_progress"
see_also: [{"target":"c5749fc3-e9ea-4a72-84d7-e2fbeac032c5","reason":"Construction fidelity and downstream efficacy must remain distinct; a package gain also differs from its cause."}]
scope: "Carry open design questions forward without pretending earlier assistant examples were an approved experiment."
position: 1024
---
Kind: Question.

## Creation

### Observed conditions
The assistant alternated between searching SiftText for known nodes and answering live web-research questions. It proposed practice and held-out tasks, no-memory/notes/vector/SiftText arms, repeated runs, and several different task counts. Jack did not select an exact workload, scorer, comparison set, sample size or budget. His latest instruction was PoC first.

### Inference and response
The next design must settle what the agent searches, what is allowed to change, and what independent observation would show improvement. A method version, an agent attempt and a search task are different objects; the graph must not conflate them.

Assistant-proposed evidence includes unseen-task performance against the same frozen starting procedure and a credible notes baseline, with matched model/tool/resource conditions and full improvement, retrieval and writing cost. Those are candidates, not an authorized specification. A known target UUID only scores record retrieval; it does not mechanically establish the quality of an open literature synthesis.

The recursion claim also needs a boundary: improving the task procedure is different from improving how the system proposes or selects future improvements. Candidate reuse, a branching graph, or one successful retry does not by itself establish either broader capability or SiftText's causal contribution. No result, including non-degradation, follows from a flat curve without an appropriate comparison.

Source: current Pi session's assistant proposals and user record `3063667d`; root conversation artifact.

## November 13–14 — lookup tasks rejected; checkable hunts proposed

### Observed conditions

In a Claude Code session the night before the hackathon, the assistant proposed paper-finding lookups with known answers, scored across a research-field switch. Jack rejected the "paper analogy" and asked for something grand and recursive. He then said: "i feel like the answers should be either long horizon or opaque or extremely difficult, almost i have the feeling it should be so hard we shouldnt even know the answer, is that possible? or nah, do we always need the answer?" His stated purpose was "ample time to improve our methods and show real improvement".

### Inference and response

The assistant answered that a task needs a referee, not a known answer, and separated three kinds: known but hard-to-find answers; unknown but checkable results; and unknown, uncheckable outputs graded by opinion, which it advised against for a one-day event. It proposed open hunts ("find every documented case of X") scored by verified, deduplicated finds with no ceiling. For the scored task it proposed hunts whose full answer a public database such as Wikidata can compute while the agent only has web search, with an open model-judged hunt as a closing showpiece. Database gaps would mark some true finds wrong; no such question was tested.

It also warned that each attempt must still take minutes, and that a growing list alone does not show method improvement: compare versions on the same fresh hunt and budget. Jack did not select a task, referee or comparison. Hackathon fit and the recursion test are carried by [The Searcher That Searches for How to Search](../7dfde31d-0c39-4772-9f05-92e4c5613a26/node.md). Source: that node's retained Claude Code session.

## November 14 — Jack prefers a general method across hunt kinds

### Observed conditions

While answering the reward-hacking question in [Define and Prevent Reward Hacking in the Search Loop](../e9cf4b7a-3426-4266-a93e-e9aa6491ee9d/node.md), Jack asked: "Or are we looking for a general method across many searches? Because I actually that would be preferred I think, if we could pull that off." The assistant answered that scoring every version on unseen hunts of mixed kinds would support a claim of better search in general. It proposed mixing at least two hunt kinds. Jack replied "ok next".

### Inference and response

This narrows the comparison toward mixed-kind unseen hunts, with Jack's preference stated tentatively. The task, its kinds, the referee, the sample size and the budget are still unselected.

## November 14 — at the event: a known-answer task first, an unknown-answer comparison if time allows

### Observed conditions

During the team introductions recorded in [Team Backgrounds and a Proposed Work Split](../a7769974-3ff8-4e30-9fd4-975bf08ff6f2/node.md), Amala described a buoy-placement project where existing models are "just best guesses". The source is an unlabelled speech-to-text transcript; the reply below is attributed to Jack from its content.

> "Whoa, that's actually really relevant to what we're doing because there's no set answer. There's no answer for that. [Our] thing actually has an answer, and part of the reason why is because I wanted to make sure we were improving. But if our thing actually ends up being good, we might want to do searches that are like we don't even know the answer yet. And then compare it to baseline. Like if we just had AI search with telem or whatever, what would it be? And then compare that to we've proved that our thing it's better. So what is our improved final search what does that bring back? [...] And then this is like more of a human judging thing, but like which answer do we think is better? [...] We might be if we if we put have time we can pull that off."

The transcript reads "R thing" where the quotation has "[Our] thing".

### Inference and response

Jack told the team that the scored task has an answer, and gave his reason: to be sure the method is improving. The transcript does not name that task or its referee, so this node still does not record them.

He also floated a second comparison, conditional on the method working and on time: searches with no known answer, the final improved method against plain AI search through Telem, with people judging which answer is better. The assistant's earlier "closing showpiece" was a model-judged open hunt. Jack's version names a baseline and uses human judges. It is a possibility he raised, not selected work.

The assistant suggested that the judges compare the two answers without knowing which method produced which. Jack did not respond to that. The sample size and budget remain unselected.

Source: Pi session `01a1db79-c926-7284-80b0-36135ff23ffd`, retained under [Team Backgrounds and a Proposed Work Split](../a7769974-3ff8-4e30-9fd4-975bf08ff6f2/node.md) at `artifacts/chats/pi-searchhack-team-intros.jsonl`.

## November 14 — left to the next agent at the hackathon

### Observed conditions

In a separate Pi session during the SearchHack kickoff, that session's assistant twice told Jack that building needed one decision from him: what the searchers hunt for, and how a right answer is told from a wrong one. Jack replied:

> "what the searchers hunt for" next agent thinks about this

He chose no task, referee, comparison or budget in that session.

Three things observed that morning bear on the choice. The kickoff's judging slide puts 40% on use of Telem, and submission is at 4:15 PM with a three-minute walkthrough; both are recorded in [SearchHack Participation and Rules](../5c47051d-90b9-43e6-ba5a-1b885c7f4ad3/node.md). Telem's hackathon console has a Benchmarks form that runs a task corpus against several configurations and judges the results, and it shows a judge state on every logged conversation; [Probe Telem's Hackathon Console and Router](../ef8ce25e-76e5-429d-86d5-433010cbd615/node.md) records that the corpus list was empty and that no judge score had appeared.

### Inference and response

The question stays open and now belongs to the next agent working with Jack. That assistant suggested asking an organizer how to obtain a corpus and what an arm looks like, since a usable Benchmarks run could serve as referee and comparison. That is a lead, not a selection. The preferences Jack stated in the sections above, including a scored task with a known answer, stand as he left them.

Source: Pi session `01a1db5b-1827-7182-a648-9aafa0a72ac9`, November 14, 2026, retained under the probe node at `artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl`.
