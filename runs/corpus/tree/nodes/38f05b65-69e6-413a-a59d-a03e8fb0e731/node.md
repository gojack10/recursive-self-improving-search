---
id: "38f05b65-69e6-413a-a59d-a03e8fb0e731"
name: "Method v002"
micro_summary: "Adaptive two-frontier search is a distinct alternative for hunts without a trustworthy finite census: expand both predicates cheaply, then allocate spend by marginal verified yield rather than committ"
status: "resolved"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v000

```json
{
 "id": "v002",
 "parent": "v000",
 "round": 1,
 "rationale": "Adaptive two-frontier search is a distinct alternative for hunts without a trustworthy finite census: expand both predicates cheaply, then allocate spend by marginal verified yield rather than committing to one anchor.",
 "instructions": "Translate X and Y into precise eligibility tests, including exclusions and time boundaries. Maintain two deduplicated candidate frontiers, one surfaced from X and one from Y, plus a ledger of verified, rejected, and unresolved identities. Begin with one search focused on each predicate and one conjunction search, sequentially so results inform the next query. Cross-match the frontiers, but verify identity and both conditions rather than treating name overlap as proof. Alternate short discovery and check_candidates rounds. Partition discovery by source, subtype, geography, era, or alphabet only where meaningful; include less obvious eligible subtypes rather than repeatedly rephrasing a successful query. Measure newly verified items per spend and new plausible candidates per search. Favor the more productive frontier while keeping a small reverse-side gap check. After two searches add no plausible candidates, change partition, provider, or frontier instead of repeating. Keep at least 35% of the initial budget for checking and evidence resolution; stop discovery earlier if the pending queue needs it. Submit only evidenced intersections, deduplicated at the hunt's entity level; do not claim completeness from search saturation alone.",
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
 "routing_rules": "Run baseline discovery on Parallel alone, default tier, 8 results. Use Exa alone for batched check_candidates, explicitly requesting both eligibility tests and identity-matched evidence. Once baseline frontiers are sampled, allow one Exa discovery probe on the weaker frontier if affordable; retain it for further discovery only if it adds useful candidates or unique evidence. Compare marginal outcomes, recognizing provider attribution is overlapping and the initial yield sample is small. Use Parallel for cheap exact-name follow-ups and Exa for consequential unresolved checks; do not repeat settled checks. Budget every variant separately and never trigger broad auto-routing. Exact checks may use 4 results; discovery remains at 8. Apply authoritative-domain filters to evidence checks, not the entire discovery frontier. Use date filters only when logically appropriate, not as a substitute for checking event or effective dates.",
 "fetch_policy": "Fetch only when summaries leave material eligibility or identity uncertain, or when a discovered list offers several new candidates. Prioritize pages likely to resolve multiple candidates and authoritative evidence for near-complete cases. Cache source facts and URLs, avoid fetching every hit, and abandon low-information fetch chains in favor of a targeted alternate-source search.",
 "status": "candidate"
}
```
