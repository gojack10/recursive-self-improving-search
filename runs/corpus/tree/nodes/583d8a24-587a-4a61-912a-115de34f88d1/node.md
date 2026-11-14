---
id: "583d8a24-587a-4a61-912a-115de34f88d1"
name: "Method v010"
micro_summary: "Test a conditional record-level join instead of relying on search rankings to surface intersections. The full-recall 387787ee6f inspected list sections and checked source-backed identities, whereas 59"
status: "in_progress"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v007

```json
{
 "id": "v010",
 "parent": "v007",
 "round": 5,
 "title": "Bounded Record Join Search",
 "rationale": "Test a conditional record-level join instead of relying on search rankings to surface intersections. The full-recall 387787ee6f inspected list sections and checked source-backed identities, whereas 59f7c7f036 missed one despite speculative checks. This is a hypothesis, not proof that section fetching caused the gain. Unlike discarded census-first and source-bundle methods, this uses a capped pilot on either frontier, retains cheap verification, and abandons low-yield extraction early.",
 "instructions": "Define X and Y exactly, including entity unit, exclusions, eligible subtypes, group membership and effective dates. Begin sequentially with broad X-only, Y-only and conjunction searches. Maintain deduplicated identity/evidence and scope ledgers. Reserve at least 35% of initial funds for resolution and price candidate checks individually.\nAssess both frontiers for a finite, accessible source with explicit records proving one predicate. Choose the side with lower expected extraction plus missing-predicate verification cost, not simply fewer apparent members. Do not commit to a census. If neither side has usable records, use short adaptive dual-frontier discovery/check rounds with v007-style scope correction.\nWhen a useful source exists, spend at most 10% of initial funds on a record-join pilot, including fetching and checks. Inspect the source's taxonomy, pagination, effective dates and actual returned extent. Select one small source-defined section with plausible overlap and one previously uninspected section not chosen for familiar names. Extract identities and existing predicate evidence from records, not search snippets alone. Check the missing predicate for at most three source-backed identities at a time, resolving those before extending the section. Record section position and unresolved records so partial inspection cannot masquerade as exhaustion. A record's abbreviated occupation or description is not a reason to reject it.\nContinue record inspection only if the pilot supplies a verified addition or concrete evidence making another small batch competitive with ordinary discovery. If two consecutive batches add neither verified intersections nor useful evidence, suspend that source, retain unresolved identities, and switch frontier or discovery mode. Extension is always incremental; do not extract the entire catalog or buy checks for a large speculative queue. Within a chosen section, avoid repeatedly selecting only recognizable identities. At each extension compare total resolution cost with an untested sibling partition on the other frontier.\nUse Parallel checks only for unresolved facts, supplying existing evidence and identity. Treat no result as unresolved and reject only on contradiction or an exhaustive applicable source. Escalate promising ambiguity or conflict individually to Exa. After two ordinary discovery searches yield no identities, prohibit synonymous conjunctions and use a distinct source section or a less restricted opposite-frontier probe. Stop discovery when pending checks need the remaining budget. With spare funds, inspect up to three distinct residual partitions, stopping after two fruitless probes and preserving verification funds. Finish with identity, predicate, membership, subtype and effective-date audits; submit only supported intersections without claiming completeness from partial source coverage.",
 "routing": {
  "auto_routing": false,
  "providers": [
   "parallel"
  ],
  "tier": "default",
  "num_results": 8,
  "verify_providers": [
   "parallel"
  ]
 },
 "routing_rules": "Parallel alone, default tier, 8 results for source discovery and residual probes; 4 for exact unresolved facts and check_candidates. No routine also variants, auto-routing or bulk Exa checking. Budget each candidate separately and do not presume fewer results cost less. Exa alone with 4 results for selected ambiguous or conflicting identities; at most one initial discovery probe after a different Parallel partition has failed, continued only with useful incremental evidence. Authoritative-domain filters target record evidence, not general coverage; relax failed filters. Publication-date filters apply only to publication-date eligibility; verify effective dates in source content.",
 "fetch_policy": "Fetch a promising structured list or source section once, recording actual visible rows, section boundaries, filters, pagination and dates. Reuse all extracted facts. Follow a next-page or section link only within the capped pilot or an explicitly justified incremental extension. Prefer accessible record views over repeated fetches of truncated pages. Do not assume a requested large page size was honored. One targeted alternate-source attempt after a blocked or uninformative fetch; abandon extraction if still unusable. Fetch authoritative individual records to settle identity or unresolved predicates, not every search result.",
 "status": "candidate"
}
```
