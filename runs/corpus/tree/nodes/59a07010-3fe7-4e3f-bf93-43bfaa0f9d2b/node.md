---
id: "59a07010-3fe7-4e3f-bf93-43bfaa0f9d2b"
name: "Method v012"
micro_summary: "Keep v007's routing and scope safeguards, but add a conditional discovery path for predicates expressed through intermediate entities rather than the requested person's name. Search source-backed grou"
status: "resolved"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v007

```json
{
 "id": "v012",
 "parent": "v007",
 "round": 6,
 "title": "Source Grounded Bridge Expansion",
 "rationale": "Keep v007's routing and scope safeguards, but add a conditional discovery path for predicates expressed through intermediate entities rather than the requested person's name. Search source-backed group, work, event or record relationships before guessing more familiar people. This is neither a census join nor blanket source-bundle allocation: it expands only eligibility-relevant relation paths. Multi-hop retrieval literature motivates the mechanism (https://aclanthology.org/2023.findings-acl.657.pdf); the inspected logs show group-credit and alias cases but do not establish an incremental recall gain.",
 "instructions": "Define X and Y exactly, including requested entity unit, exclusions, subtypes, group-membership rules and effective dates. Start sequentially with broad X-only, Y-only and conjunction searches. Maintain deduplicated frontiers, identity/evidence and scope ledgers as in v007: record accidental restrictions, derive a few source-backed sibling partitions, and never treat restricted success as parent-category coverage. Add a compact relation ledger only when sources show that a predicate is recorded on a different entity unit: for example a qualifying group, credited work, event, institution or named record linked to the requested entity. Record the intermediate entity, the explicit relationship, source, applicable date and missing edge. Treat shared names as identity questions, not relationships. After the baseline, ask whether either frontier systematically hides eligible entities behind such a relationship. If so, substitute one source-grounded bridge probe for a normal discovery probe: retrieve the qualifying intermediate entity's explicit recipients, named members, creators or other eligibility-relevant roster, and bring newly identified requested-unit entities into the frontier. A confirmed find may supply a bridge lead, but do not infer that its associates qualify. Expand only relationships permitted by the hunt, at most one intermediate entity between the requested entity and each predicate; do not crawl arbitrary collaborators or biographies. Select one promising bridge at a time and check at most three new identities before expanding further. Prefer paths that establish one predicate for several new identities and leave only one inexpensive check each. Stop a bridge family after two probes add neither source-backed candidates nor useful missing-edge evidence; return to ordinary opposite-frontier or residual-scope discovery. No bridge is mandatory when the source structure provides no justification. Run small discovery/check rounds prioritized by total resolution cost, with a genuine neglected-scope probe each round. Check only unresolved predicates and identity edges, preserving established facts. Group membership or work association does not automatically transfer an award or status: require the hunt's exact qualifying relationship and date. Silence remains unresolved. After two unproductive discovery searches, prohibit synonymous conjunction searches and try an untested sibling or unrestricted parent on the opposite frontier, or an evidenced untested relation path. Reserve at least 35% of initial funds for checks; stop discovery when pending checks consume the remainder. Perform up to three affordable final residual probes on distinct untested restrictions or relation paths, stopping after two without candidates or useful evidence. Submit only deduplicated entities with both predicates and every required identity or relationship edge supported.",
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
 "routing_rules": "Parallel alone, default tier, 8 results for baseline, bridge and residual discovery; 4 for exact missing-edge checks and check_candidates. Use verified intermediate-entity names and neutral relationship questions, not asserted eligibility. Price each candidate and query separately, including downstream relationship checks. No routine also variants, auto-routing or multi-provider requests. Escalate only promising ambiguous, conflicting or inaccessible individual cases to Exa alone with 4 results. At most one initial Exa discovery probe after genuinely different Parallel scope or relation partitions stagnate, continued only if it adds useful identities or evidence. Domain-filter targeted roster, credit or authoritative-record checks, not broad frontier coverage; relax failed filters. Publication-date filters apply only when publication date defines eligibility; check relationship and status effective dates in content.",
 "fetch_policy": "Reuse cached evidence. Prefer fetching the specific roster, credit table, namesake origin or record section that can expose and support a missing relation edge. Inspect its entity unit, inclusion rules, dates and relevant pagination before treating it as covered. Extract explicit identities rather than guessed associates, and preserve the source supporting each edge. Fetch authoritative missing-predicate pages when needed; do not fetch every result or enumerate a whole institutional census. After a blocked or uninformative page, try one targeted alternate source. No acceptance based solely on a generated relationship summary or an uninspected plausible URL.",
 "status": "candidate"
}
```
