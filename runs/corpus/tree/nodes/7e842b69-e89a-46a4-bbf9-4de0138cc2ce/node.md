---
id: "7e842b69-e89a-46a4-bbf9-4de0138cc2ce"
name: "Intersection hunts need a coverage ledger, not repeated joint-condition searches"
micro_summary: "Both attempts returned only correct items but left the population incompletely inspected. Repeated conjunction queries and familiar-name guesses did not establish coverage. Enumerate a tractable side,"
status: "in_progress"
kind: "What We Learned"
see_also: []
---
**Kind:** What We Learned

Both attempts returned only correct items but left the population incompletely inspected. Repeated conjunction queries and familiar-name guesses did not establish coverage. Enumerate a tractable side, explicitly test the other condition, track unresolved identities, and retain the exact eligibility rules. The second attempt correctly distinguished a namesake from a similarly named person, illustrating why name overlap alone is insufficient.

**Tested scope:** Enumeration, intersection verification, and identity resolution

**Evidence attempts:** ['dde6c45b34', '68feaccc35']

- Round 2: seen again in attempt a5fb1e8aae: Despite full train recall, the trace repeatedly rephrased conjunction searches and guessed familiar candidates instead of enforcing the two-no-new-candidate pivot and explicit frontier coverage.

- Round 2: seen again in attempt 62f1804b27: Full train recall does not erase the repeated conjunction-query pattern: numerous similar variants continued after initial checking rather than documenting new partition coverage.

- Round 4: seen again in attempt 74f4f7599e: Repeated conjunction searches and familiar-name checks persisted, while queries largely narrowed surface features to craters and Nobel categories to scientists/physics. The attempt missed one item and stopped with 0.025 remaining; the log does not establish which coverage gap caused the miss. This repeats the existing coverage-ledger failure rather than proving a new lesson.

- Round 4: seen again in attempt 323d9d4463: Despite full recall, the trace repeats conjunction variants and familiar-name checks. This matches the existing coverage failure rather than establishing a new failure.

- Round 5: seen again in attempt 8dc4c7b9b7: Repeated conjunction variants and familiar-name queries persisted despite v007's pivot rule; 48 searches still returned three of four items. This repeats the coverage-control failure, not evidence for a newly identified missing subtype.

- Round 5: seen again in attempt 59f7c7f036: Discovery repeatedly restricted the population to familiar occupations and feature types, followed by large familiar-name checks; a partial list was not converted into explicit record coverage. The matched successful attempt supports testing record inspection, but does not establish causality.
