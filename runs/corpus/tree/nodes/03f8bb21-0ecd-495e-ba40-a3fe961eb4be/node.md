---
id: "03f8bb21-0ecd-495e-ba40-a3fe961eb4be"
name: "Method v005"
micro_summary: "Preserve v003's successful cheap adaptive exploration, but add a weakest-link evidence audit and neutral verification queries. This differs from census-first and source-bundle methods: it changes how "
status: "discarded"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v000

```json
{
 "id": "v005",
 "parent": "v000",
 "round": 3,
 "rationale": "Preserve v003's successful cheap adaptive exploration, but add a weakest-link evidence audit and neutral verification queries. This differs from census-first and source-bundle methods: it changes how tentative matches become accepted, while using saved provider spend for uncovered partitions rather than repeated confirmation.",
 "instructions": "Define X and Y, entity unit, aliases, exclusions, eligible subtypes, group rules and effective cutoff. Begin with one X-only, one Y-only and one conjunction search. Maintain deduplicated dual frontiers and a ledger with canonical identity, exact source-supported X and Y facts, URLs, identity-bridge evidence, unresolved questions and coverage partitions. Prefer the frontier yielding new plausible candidates per total discovery-plus-resolution cost; do not require a finite census. Check source-backed candidates' missing predicate first. Supply canonical names and verified aliases, not conjectured matches, dates or titles as established facts. Use neutral queries asking which entity a record identifies or whether the predicate is documented. A check_candidates answer or plausible URL is a lead unless retrieved evidence explicitly supports it. Distinguish supported, contradicted and unresolved; search silence is unresolved. Do not recheck strong facts merely because the other predicate remains weak. For every tentative intersection, audit its weakest edge: source identity, predicate scope or effective date. If acceptance depends on a generated summary, ambiguous surname, inferred affiliation, or uninspected URL, fetch the underlying record before accepting; if unclear, use one neutral authoritative lookup then selective Exa escalation. Require both predicates and their identity bridge, not two facts about similarly named entities. Explicit source excerpts can satisfy this without mandatory fetching of every item. Continue short discovery/check rounds, with a neglected subtype or reverse-frontier probe each round. After two searches yield no new plausible identities, switch partition, source or frontier rather than rephrasing the conjunction. Spend remaining exploration funds on uninspected partitions and source-backed unresolved candidates, not familiar-name guessing or confirmations of accepted items. Reserve at least 35% of initial budget for resolution and final weak-edge audits; stop discovery when pending resolution costs consume the remainder. End by submitting only supported intersections, deduplicated by the requested unit; never infer completeness from saturation.",
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
 "routing_rules": "Use Parallel alone for discovery (8 results) and first-pass check_candidates (4 results per candidate). Use Exa alone, usually 4 results, only for promising unresolved candidates after a targeted cheap lookup or failed source inspection, or one discovery probe after genuinely different Parallel partitions stagnate. Do not escalate a whole batch for one uncertain item. Budget each candidate/provider query separately; fewer results and batching do not imply lower charges. Avoid routine multi-provider routing and also variants. Apply domain filters for targeted authoritative proof, not general discovery; relax filters if they obstruct evidence. Use publication-date filters only when publication date itself defines eligibility; otherwise check effective dates in content. Prefer independent missing-fact retrieval over queries containing an unverified claimed relationship.",
 "fetch_policy": "Reuse cached evidence. Fetch authoritative records when a tentative acceptance rests on summaries, identity ambiguity or an uninspected URL, and fetch useful lists when they cheaply expose new candidates. Prefer Tavily fetch when available: it surfaced evidence for 39 correct finds and no wrong finds in the supplied attribution, although that is observational rather than a guarantee. Do not refetch sufficient evidence. After one blocked or uninformative fetch, try one targeted alternate authoritative source before selective escalation; leave unresolved items unsubmitted.",
 "status": "candidate"
}
```

Discarded in round 3: select 0.792 vs current 0.778.
