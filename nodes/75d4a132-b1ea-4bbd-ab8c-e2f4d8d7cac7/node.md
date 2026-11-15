---
id: "75d4a132-b1ea-4bbd-ab8c-e2f4d8d7cac7"
name: "Build the Narrated SearchHack Presentation"
micro_summary: "Develop a separate, layman-readable SearchHack explainer from the team script, Blank Page references and SiftText styling."
status: "resolved"
scope: "Build the explanatory presentation and handoff to the team's live demonstration, not the live dashboard itself."
see_also: [{"target":"93d6cfcb-43b6-4f86-a9b6-ed2a0ded0f1a","reason":"The team and visitor feedback supplied the dashboard handoff and minimal-text requirements."},{"target":"240a8b42-07e1-47b2-a20f-75214f3c8b43","reason":"The evidence chapter uses the later recorded corpus results while keeping recursion measurement separate."}]
position: 1024
---
**Kind:** Agreed Work

## Creation — November 14, 2026

### Observed conditions
Jack selected the SiftText look for a **separate narrated presentation**, inspired by the supplied Claude HTML artifacts. The purpose was to explain what RSIS is, why the team is doing it and how it works, then hand off to teammates demonstrating the running system. He accepted explanation before demonstration, wanted positioning worked backwards from the SearchHack judging context, and said to use Blank Page rather than skip its reference procedure. He later supplied the team's V1 and V2 scripts and said “Go to build.”

The first source was `/Users/jack/Downloads/RSIS Demo (Copy).html`; the later teammate version was `/Users/jack/Downloads/RSIS Demo (Copy) (1).html`. Jack also supplied `https://claude.ai/artifact/U7RGSEGggESFFmfzsVpEF8`; this session used the local HTML, not a claimed write into that hosted artifact. Script sources are `rsis-demo-script.txt` and `rsis-demo-script-v2.txt` in `/Users/jack/project/jack-rewriter/corpus/working`.

### Inference and response
The assistant selected a standalone 16:9 HTML stage, not a dashboard modification. It used the SiftText landing-page typography, near-black ground, square panels and status glyphs; Blank Page supplied still/motion reference gathering and a beat-oriented brief. The skill was cloned/read and its are.na reference workflow used. No Stewdio renderer or plugin was installed.

## Development — less clutter, then purposeful colour

The first hourglass/compression visual was unclear to Jack. The more detailed successor was also rejected: “It's too cluttered” and “a layman is looking at this thing.” He selected “minimalism” / “understated luxury”, not text-only minimalism: the audience's eyes should know where to look.

The resulting design keeps one primary explanation at a time, large type, breathing room and straight edges. It removes terminal command headers and dense incidental statistics. It restores useful panes and small concrete pictures: two condition tiles per candidate, answer squares, competing-method bars, a four-step round and a two-box recursion loop. The cast rail lights the relevant role. Blue marks search, green verification/retention, and amber failure/learning. Blue and green were brightened from the SiftText status palette; amber is an assistant-added accent, not a native SiftText failure status. Jack asked to consult `pbakaus/impeccable`; colour-role guidance was read through `gh`, without installing it or replacing the SiftText look.

Jack requested spoken-word highlighting, a reserved blank demonstration slide, a stronger closing and fixes for diagrams escaping their panes. The handoff now explains four things to watch: the active agent block, score against the baseline, kept/discarded methods, and the tree delta as methods and lessons are written. The closing invites the viewer to ask their own question.

In the first build request, Jack said “we're just gonna pretend that our thing is better”, explaining that otherwise the hackathon would not be submitted. The assistant did not implement invented winning numbers. The later V2 script explicitly corrected invented results and separated better search from better improving. Early slides used actual tied runs or left results blank rather than presenting fabricated wins. A later Moon/Nobel example was added, then the exported film returned to Hugo/Nebula because that is what Jack's opening recording actually says. The later corpus results changed the search-evidence slide, not the still-unmeasured recursion claim.

## Completion

The HTML explainer, fonts, brief, references, one-file export and narration-specific film source were produced. This completes the requested build, not a claim that Jack approved every final frame or that a public Claude artifact was updated. The child [Export the Narration-Synced SearchHack Video](../3e40c32a-addf-4e28-8a28-9b192957c09e/node.md) owns the four recordings, replay, export failures and final 2:50 delivery.

`/Users/jack/Downloads/rsis-explainer` is a symlink to the existing durable directory `/Users/jack/sifttext/nodes/9863dbdd-2c88-4d32-972c-91c30e18199c/artifacts/explainer`. This node's `artifacts/presentation` associates that directory; it contains `brief.md`, `.context/refs/rsis-explainer/`, `fonts/`, `rsis-explainer.html`, `rsis-explainer-v1.html`, `rsis-explainer-v2.html`, `rsis-explainer.single.html`, `rsis-recorded-opening.html` and `rsis-film.html`. These are distinct outputs: the one-file interactive HTML is not the final MP4, and its script can differ from the recorded narration. `artifacts/script-sources` links the existing rewriter working directory; copies of the two supplied HTML inputs are retained with the presentation sources. No source directory was moved.

## Source
Pi session `01a1dc0c-a596-779d-89b4-26e063f0bfba`, retained via `artifacts/chats/pi-searchhack-narrated-presentation.jsonl`. Decisive user records: `228d812a` (artifact), `c87fe147` (scope/look/flow), `c5aa6b82` (Blank Page), `a961f93a` (build/V1), `68a5312e` (V2, reserved slide and spoken-word highlight), `baddfc10` (layman clarity), `e5bd7144` (colour and visual explanations), `280f7a27` (apply demo feedback), `4e3d5a53` (tree delta). The assistant's candidate brief is in the associated presentation directory.
