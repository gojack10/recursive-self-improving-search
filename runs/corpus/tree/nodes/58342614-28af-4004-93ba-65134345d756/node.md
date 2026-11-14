---
id: "58342614-28af-4004-93ba-65134345d756"
name: "Audit the weak predicate independently of the candidate's asserted match"
micro_summary: "Attempt dd908a9aad found all four valid items but submitted one additional wrong item. The trace repeatedly embedded the supposed match and date into searches, checked its other predicate, and submitt"
status: "in_progress"
kind: "What We Learned"
see_also: []
---
**Kind:** What We Learned

Attempt dd908a9aad found all four valid items but submitted one additional wrong item. The trace repeatedly embedded the supposed match and date into searches, checked its other predicate, and submitted a URL without fetching that candidate's underlying record. This does not establish the precise cause, but motivates a distinct evidence gate: independently retrieve the weak predicate using neutral identity queries, and require source content rather than a plausible URL or repeated search assertions. Parallel's aggregate 163.8 correct finds/dollar versus Exa's 60.7 favors keeping cheap discovery while spending selectively on this audit.

**Tested scope:** General intersection hunts; unsupported identity joins and query-premise contamination

**Evidence attempts:** ['dd908a9aad']
