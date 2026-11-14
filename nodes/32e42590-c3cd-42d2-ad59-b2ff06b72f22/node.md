---
id: "32e42590-c3cd-42d2-ad59-b2ff06b72f22"
name: "Show Instruction Lineage Beside Agent Progress"
micro_summary: "Connects a downward-growing instruction tree with a time-and-score view of agent attempts."
status: "in_progress"
see_also: []
scope: "Preserve the accepted visual concept, not a completed interface or scripted outcome."
position: 4096
---
Kind: Idea.

## Creation

### Observed conditions
Jack pictured two views: a browser-harness-like instruction tree growing downward, and agents moving rightward through a hill-climbing graph as they branch, work and stop. The assistant proposed showing both at once, linked by color for the instruction version used. Jack replied, "yeah alright anything else we need to think about?"

### Inference and response
The left view would show actual SiftText work and method lineage under Commit rules. The right view would show actual attempt time, score and branching, with each attempt linked to its method version. These are linked but different structures.

The proposed demo story was a replay of earlier work followed by a live fresh-agent attempt. Neither a basin, a successful escape nor a transfer gain may be staged as an observed result. A prerecorded fallback was an assistant suggestion, not a new recording authorization. Jack subsequently put all demo work behind the PoC.

Source: current Pi session, user records `44a2aeb1`, `4fc4420e`, `3063667d`; root conversation artifact.

## November 14 — resumed as a passive visual debugger

The former deferral was: "Resume only after the pre-hackathon PoC establishes a result worth demonstrating and Jack elects to build the presentation." Jack now explicitly requested the visual work, but not as proof of a successful PoC or as a learning interface. He wants to run the CLI and watch a state-machine debugger above the run tree growing down and method iterations growing right, without starting or steering the run from HTML.

[Watch SearchHack Run Through a Visual Debugger](../125b3125-6dfd-4a2f-87fd-c4cf6815f5ee/node.md) owns that commitment, implementation and visual corrections. The original reference image remains inspiration; the implemented right-hand view uses method scores rather than invented spatial search trajectories. This Idea is resumed while the chosen application remains under review; no search-improvement result follows.

Source: Pi session `01a1dba0-2171-7284-80b0-361440318b9c`, retained under the child work's `artifacts/chats/pi-searchhack-visual-debugger.jsonl`.
