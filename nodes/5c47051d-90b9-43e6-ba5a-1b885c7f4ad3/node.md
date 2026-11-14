---
id: "5c47051d-90b9-43e6-ba5a-1b885c7f4ad3"
name: "SearchHack Participation and Rules"
micro_summary: "Keeps the event context, registration boundary and unresolved eligibility conditions for the project."
status: "in_progress"
see_also: []
scope: "Preserve this conversation's event investigation without claiming current registration or settled competition rules."
position: 5120
---
Kind: Question.

## Creation

### Observed conditions
Jack supplied [the SearchHack invitation](https://luma.com/e13wf1bd) and asked whether to participate. Browser research in this session reported a free in-person Sunnyvale hackathon on November 14, 2026. Luma listed 10 AM-7 PM and a 4:15 PM submission time; Devpost's rules listed 5 PM and an 8 PM end, while its dates page also listed 4:15 PM.

Jack then asked the assistant to fill the Luma form without submitting. The assistant reported leaving a generic memory-aware research-agent draft open, with terms and photo/video consent unchecked. The new project idea was not subsequently entered or submitted in this conversation.

### Inference and response
Existing-code eligibility, IP/public-source terms, team limits and required sponsor-tool use were not established. Using existing SiftText, Pi, autoresearch and browser-harness must not be assumed competition-compliant. A pre-hackathon PoC and a submission claimed to have been built during the hackathon need their origins disclosed and the rules confirmed.

The form state is a historical observation, not a promise that an unsaved browser draft persists. This capture does not submit registration or accept terms.

Source: this Pi session's browser research and form-fill exchanges; [Devpost rules](https://searchhack.devpost.com/rules) and [dates](https://searchhack.devpost.com/details/dates). No new browser verification was performed for this capture.

## November 13–14 — sponsor, schedule and registration check

### Observed conditions

The assistant read the event's Devpost overview, rules and resources pages, the Luma page and Telem's site and docs on the night before the event. Devpost is subtitled "Agentic web search challenge using Telem AI" and lists building from 11:00 with submissions due at 5:00. Luma lists submissions at 4:15 and judging at 4:30. Judges are six investors, scoring Innovation, Technical Execution, Search Intelligence and Impact. Neither page published a rule on prior code or required tools; rules are announced at the 10:30 kickoff. Sponsors are Telem AI and Tavily.

Jack pasted his Devpost page showing "You're registered for this hackathon." Luma requires host approval and shows the address only after approval. The assistant's browser was not signed in as Jack, so his Luma status remains unverified.

[Telem](https://docs.telem.ai/) presents the event. It routes one search request to providers such as Exa, Tavily and Brave and normalises results. It fetches pages as text, logs calls to a console and ships a Pi package with search and fetch tools. Its docs list $20 of first sign-in credit and per-provider prices around $0.005 per search.

### Inference and response

The assistant advised planning to use Telem for the searchers' web access and asking in the event Discord about required tools and prior code. Engine choice, date windows and domain filters give the search method concrete settings to learn. No Telem account, key, install or registration change was made in that session.

## November 14 — kickoff schedule, judging weights and tracks

### Observed conditions

On the morning of the event Jack pasted three things into a Pi session: his Devpost page, the text of the kickoff's tracks and judging slides, and a speech-to-text transcript of the kickoff talk. The slide text and the transcript are garbled in places.

**Devpost page.** It showed 29 participants, three non-cash prizes, six investor judges and the criteria Innovation, Technical Execution, Search Intelligence and Impact. Jack was registered.

**Judging slide.** It lists four criteria: Use of Telem AI, "Strong query understanding, retrieval, ranking and grounded results, and something that would be hard to build without Telem"; Startup & Venture Potential, a clear customer with an urgent problem, a sizable market, a credible business model and an edge; Innovation; and Technical Execution, "Whether it works, how well it is built, and how much was achieved in the time". The pasted weights are 40%, 20%, 20% and 20% in that order.

**Tracks slide.** Nine tracks, described as "Starting points, not rules": intelligent retrieval, long context and memory, search routing, agentic search, efficient search, knowledge and discovery, personalized search, multimodal search and new interfaces.

**Kickoff talk.** The host said building officially starts at 11 and could begin at once, lunch is at 1 PM, submission is at 4:15 PM, judges evaluate the top submissions from 4:30, final presentations are at 5:30 and winners are announced at 6:50. Each team submits "a three-minute walkthrough, you know, via video or anything like uh slides". He said "we're going to dynamic dynamically grade your product based on the number of members in your team". He said Telem has its "own benchmark system that benchmarks every APA every day and knows what is the best way to answer requests", played a video on Telem's monitors and called the feature "Something you could build on top of it", and said current search "does not really have a memory of yourself".

### Inference and response

The assistant took 4:15 PM as the submission time, which settles the earlier 4:15 versus 5:00 conflict in favour of what was announced in the room. It matched the 40% weight to Use of Telem AI from the order of the pasted text; the slide itself was not seen. The slide's criteria differ from the four on Devpost, and the assistant treated the slide as current because it was shown at kickoff.

Still not established: any rule on prior code, the formula behind team-size grading, and whether any tool is required beyond what the rubric rewards. Jack's Luma approval was not checked. [Build Method Versions From Telem Settings](../0fd5c03f-3b02-4441-95f9-78f173744b1f/node.md) holds the assistant's advice in response to this rubric, and [Probe Telem's Hackathon Console and Router](../ef8ce25e-76e5-429d-86d5-433010cbd615/node.md) holds what Telem's hackathon deployment actually did.

Source: Pi session `01a1db5b-1827-7182-a648-9aafa0a72ac9`, November 14, 2026, retained under the probe node at `artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl`.
