---
id: "470f3346-72ed-4ca1-919a-1363987348ca"
name: "Verification batches must be budgeted per candidate, not per tool call"
micro_summary: "In a5fb1e8aae, a six-candidate Exa check cost 0.042 of a 0.080 initial budget; in 62f1804b27, four candidates cost 0.028. Batching did not eliminate per-candidate provider charges. Both achieved full "
status: "in_progress"
kind: "What We Learned"
see_also: []
---
**Kind:** What We Learned

In a5fb1e8aae, a six-candidate Exa check cost 0.042 of a 0.080 initial budget; in 62f1804b27, four candidates cost 0.028. Batching did not eliminate per-candidate provider charges. Both achieved full train recall, so these traces establish a cost concentration, not demonstrated recall loss. Estimate the whole batch before dispatch, reuse established predicate evidence, and test cheap first-pass checks or shared-source resolution before paying for speculative expensive checks. Aggregate attribution favors Parallel (78 correct/dollar versus Exa 46.5), but overlaps and differing tasks prevent a causal provider-quality conclusion.

**Tested scope:** Verification routing and budget accounting

**Evidence attempts:** ['a5fb1e8aae', '62f1804b27']

- Round 3: seen again in attempt 323d9d4463: The successful attempt still committed 0.018 to an eighteen-name first-pass batch, illustrating the existing per-candidate cost concentration. This is an opportunity for interruptible allocation, not evidence of missed finds.
