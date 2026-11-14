---
id: "48b3110c-8d87-4e0d-9f58-f987bb3a98f9"
name: "Method v004"
micro_summary: "Source-bundle adaptive search: change the unit of allocation from individual names to evidence-rich source sections. Keep both frontiers and Exa verification, but amortize discovery and proof across m"
status: "discarded"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v002

```json
{
 "id": "v004",
 "parent": "v002",
 "round": 2,
 "rationale": "Source-bundle adaptive search: change the unit of allocation from individual names to evidence-rich source sections. Keep both frontiers and Exa verification, but amortize discovery and proof across multiple entities without repeating v001's unconditional census commitment.",
 "instructions": "Translate both predicates into exact tests, including entity unit, time boundaries, exclusions and membership rules. Sample X, Y and their conjunction sequentially with one search each. Maintain both candidate frontiers plus a source-section queue: each section records its predicate, scope, pagination, unseen candidates, available facts and extraction/check cost. Prefer sources that explicitly establish one predicate for several identities and offer discriminating fields for checking the other. Run a small pilot on the most promising section: extract canonical identities and aliases, preserve row-level evidence, and check the missing predicate for a small batch before expanding the section. Choose the next section or frontier by newly verified identities per total discovery, extraction and verification spend, not apparent roster size. Never require a complete census before checking; abandon low-yield sections after a pilot and retain unresolved identities for later. Use source subtypes, date ranges, geography or categories to uncover unseen sections, with a reverse-frontier gap check after each productive section. Include unusual eligible subtypes; source descriptions are ranking signals, not grounds for exclusion. Shared evidence can establish X or Y for multiple candidates, but identity and both predicates must be evidenced individually. Resolve aliases, group membership and namesakes explicitly. After two searches produce no new plausible identities, switch source family or frontier instead of rephrasing. Reserve at least 35% of initial budget for checking and resolution, estimate each pending batch's full cost, and stop source expansion when that reserve is needed. Submit evidenced deduplicated intersections; report unresolved scope rather than asserting exhaustive coverage.",
 "routing": {
  "auto_routing": false,
  "providers": [
   "parallel"
  ],
  "tier": "default",
  "num_results": 8,
  "verify_providers": [
   "exa"
  ]
 },
 "routing_rules": "Parallel alone, default tier, 8 results for discovery of source sections and targeted alternate sources. Use 4 results for exact-identity follow-ups. Exa alone for small check_candidates batches whose candidates have source-backed anchor evidence; supply that evidence and the exact missing predicate while requiring the final decision to satisfy both tests. Do not pay for a new check when a retrieved source already explicitly settles both conditions and identity. Pilot only as many candidates as can be resolved within the reserve, accounting for per-candidate billing. Allow one Exa source-discovery probe when distinct Parallel source searches stagnate; expand only if marginal yield justifies its higher cost. No auto-routing, routine multi-provider fan-out or broad simultaneous query variants. Restrict domains for source-specific evidence checks, not general discovery. Use publication filters only for logically applicable publication constraints, never as proxies for effective dates.",
 "fetch_policy": "Prioritize a discovered table, directory section or export that supplies evidence for several candidates; confirm scope and pagination before interpreting omissions. Extract candidate identities and useful predicate facts immediately rather than fetching a list and continuing generic conjunction searches. Fetch the next section only after the pilot demonstrates useful yield. Cache row-level provenance and fetch individual authoritative records only for unresolved identities, eligibility or dates. A partial or truncated roster cannot justify rejection or completeness.",
 "status": "candidate"
}
```

Discarded in round 2: select 0.632 vs current 0.793.
