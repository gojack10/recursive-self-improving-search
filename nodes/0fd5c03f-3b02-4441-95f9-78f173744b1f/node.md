---
id: "0fd5c03f-3b02-4441-95f9-78f173744b1f"
name: "Build Method Versions From Telem Settings"
micro_summary: "Proposes fitting the recursive searcher to the judging rubric by making each method version a Telem request configuration."
status: "in_progress"
see_also: [{"target":"7dfde31d-0c39-4772-9f05-92e4c5613a26","reason":"The recursive design this proposal adapts; its mechanism and recursion test are owned there."},{"target":"5c47051d-90b9-43e6-ba5a-1b885c7f4ad3","reason":"Owns the kickoff rubric, schedule and tracks this proposal responds to."},{"target":"ef8ce25e-76e5-429d-86d5-433010cbd615","reason":"Supplies the observed Telem prices, routing output and Benchmarks form."}]
scope: "Preserve the assistant's hackathon-day advice on how the project should use Telem and be pitched; Jack has not selected it."
position: 11264
---
**Kind:** Idea

## Creation — November 14, 2026

### Observed conditions

On the morning of SearchHack, Jack asked: "how does talem ai work in my recent sifttext hackathon project is it too similar to our hackathon project or nah, its better? remains to be seen because it hasnt been build but use judgement". "Talem" is his dictated spelling of Telem.

The assistant read this tree and four pages of Telem's docs. It answered that the two are not too similar: Telem sends one search to several providers and returns one format, while the project is a method that changes across generations. It named one overlap, Telem's auto-routing, which picks providers per query. It advised leaving auto-routing on and not making "which engine" the thing the method learns.

Jack then pasted the kickoff's judging slide and a transcript of the kickoff talk, recorded in [SearchHack Participation and Rules](../5c47051d-90b9-43e6-ba5a-1b885c7f4ad3/node.md), and asked "ok does this change any strategy?". The slide gives 40% to use of Telem, described as "something that would be hard to build without Telem". In the talk the host said Telem benchmarks every provider daily to decide how to answer requests, and that current search "does not really have a memory of yourself".

### Inference and response

All of the following is the assistant's proposal. Jack did not select any of it; his replies moved to which search backend to start on.

- **Reversal on provider choice.** With 40% on Telem use, the assistant withdrew its first advice. It proposed that each method version be a Telem request configuration plus instructions: provider lists, tier and filters. Telem's auto-routing would be generation 0 and the baseline.
- **Its reading of the score.** Against the slide, it judged the project as designed weak on Telem use, undefined on venture potential, strong on innovation and at risk on execution because nothing was built.
- **Pitch.** Since Telem already ranks providers in general, the assistant advised against claiming better routing. It proposed: Telem knows which provider is best in general, and the loop remembers what worked for this user's questions.
- **Venture slice.** It suggested naming one customer with a recurring search domain and offered patent or merger-diligence research as examples. Those examples are the assistant's, not Jack's.
- **Time.** With submission announced for 4:15, it advised cutting the generation 0, 3 and 6 recursion test and building a live loop with one rising curve first.
- **Failure record.** It proposed logging each result's provider, `latency_ms` and `warnings` per attempt.
- **Monitors.** It advised against pivoting to Telem's monitors, the feature the host promoted, because they do not fit the loop and the Pi package lacks the monitor tools.
- **Benchmarks as referee.** After reading the console, it suggested that each method generation could be a benchmark arm judged by Telem, if a corpus can be obtained. [Probe Telem's Hackathon Console and Router](../ef8ce25e-76e5-429d-86d5-433010cbd615/node.md) records why that is unconfirmed.
- **Pi tools.** Because the Pi tools take no provider or tier parameter, it noted that either the improver writes Telem's config file per version or the searchers call an SDK.

None of this was built or tested. The score reading is a judgment, not a measurement.

## Source

Pi session `01a1db5b-1827-7182-a648-9aafa0a72ac9`, November 14, 2026, retained under the probe node at `artifacts/chats/pi-searchhack-kickoff-telem-probe.jsonl`.
