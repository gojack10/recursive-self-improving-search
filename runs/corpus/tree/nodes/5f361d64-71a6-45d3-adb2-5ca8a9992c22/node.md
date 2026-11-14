---
id: "5f361d64-71a6-45d3-adb2-5ca8a9992c22"
name: "Broad auto-routing consumed enumeration and verification budgets too early"
micro_summary: "The first attempt spent 0.08415 on three variants routed across seven providers and missed three items. The second spent 0.0561 on two seven-provider searches before completing its census, then exhaus"
status: "in_progress"
kind: "What We Learned"
see_also: []
---
**Kind:** What We Learned

The first attempt spent 0.08415 on three variants routed across seven providers and missed three items. The second spent 0.0561 on two seven-provider searches before completing its census, then exhausted its remaining budget on fetches and missed one item. Prefer explicitly priced narrow routes and reserve verification spend. Parallel produced 200 attributed correct finds per dollar versus Exa's 85.7, though Exa surfaced more correct finds overall; these five-search samples support cheap discovery plus selective Exa escalation, not claims of universal superiority. Attribution can overlap across providers.

**Tested scope:** Budget allocation and provider routing

**Evidence attempts:** ['dde6c45b34', '68feaccc35']
