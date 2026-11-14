---
id: "5a004683-3bed-443c-98e9-d011b1e0f5c4"
name: "Recursive Self-Improving Search for SearchHack"
micro_summary: "Investigate whether SiftText-maintained experience improves an agent's search method across tasks."
status: "in_progress"
see_also: [{"target":"f698383d-0da4-477d-bf7e-764da7040d40","reason":"Existing evaluation program; this hackathon project is a bounded investigation, not a replacement."},{"target":"c1a97fd5-476c-44c5-b9d6-64b6405df06b","reason":"Earlier thesis that the method used to develop an answer can itself evolve through preserved experience."},{"target":"bf8823dd-9e4e-4bed-8430-ca258d5471fd","reason":"Jack requested this project's records follow the epistemic-state-machine model without changing global methods."}]
scope: "Develop and qualify a search-method improvement prototype for SearchHack, beginning with a pre-hackathon proof of concept."
warnings: "The first complete Pi iteration ran on November 14, but both methods tied on selection tasks and the original stayed. No search improvement or recursive improvement is established. Viewer clarity, iteration speed and harder fixed-budget tasks remain open."
position: 0
---
Kind: Goal.

## Creation

### Observed conditions
Jack came to this conversation with a SearchHack invitation and rejected generic memory/research demonstrations as too tame. He developed the title "recursive self-improving search" and wanted SiftText to feed the improvement process, with a possible later product feature and research paper.

### Inference and response
The working goal is a search agent whose experience improves how later searches are performed, rather than merely returning a remembered answer to a similar question. SiftText would retain the evidence, conditions, interpretations and method successors that feed that process. This is Jack's intended capability, not an observed result.

[Choose Recursive Self-Improving Search](../2878409c-4a52-4d1d-bc3c-ef75c58e62bd/node.md) preserves the selection. [Establish a PoC Before Demo Work](../6b472da5-be58-4ce8-9568-05393919bf1f/node.md) owns the immediate continuation; the demo was a separate deferred branch at creation. Later success or failure belongs in new developments, not rewritten into this origin.

## November 14 — visual-debugger frontier

Jack explicitly resumed [the lineage-and-progress visual](../32e42590-c3cd-42d2-ad59-b2ff06b72f22/node.md) as a passive debugger: run the CLI, watch block-state transitions and the growing run tree beside method iterations. Its child work records code commit `f4acbde`, startup observations, sampling limits and the remaining human visual judgment. This is not evidence that the root goal of improved search has been met.

## November 14 — first iteration and continuation

[Run the First Complete SearchHack Iteration](../fee4d2ea-c29d-45fc-8498-2002830f8f8f/node.md) records the completed 351-second run, the proposed method's perfect-score selection tie and the original method's 0.8357 held-out score. The next independent work is [live activity visibility](../49b9b605-895f-4812-ad18-c874bbc354d8/node.md), [iteration latency](../4f4ad38a-2e27-420b-8fa1-0d72b19ce3e5/node.md), and [task/answer-key research requested from the teammate](../0acb1796-9cdb-4916-b35f-45c44938c867/node.md). Jack confirmed that task difficulty must reward a better method at the same search budget, not simply more turns. These records preserve a completed run and unfinished work, not an improvement claim or fresh agent dispatch.

## Source
Pi session `01a1c899-999a-74b0-9115-d80780824acd`, November 10, 2026 local time. Source snapshot proposed at `artifacts/chats/pi-searchhack-planning.jsonl`; the other new nodes will link to that one retained copy. No remote transcript backup is requested.
