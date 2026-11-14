---
id: "19febaf5-6ef3-49be-ba5b-92482a64fb08"
name: "Method v009"
micro_summary: "Make v007's largely advisory pivot rule executable through query admission and persistent cooldowns. The inspected 48-search attempt illustrates noncompliance rather than disproving the pivot hypothes"
status: "in_progress"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v007

```json
{
 "id": "v009",
 "parent": "v007",
 "round": 5,
 "title": "Enforced Discovery State Transitions",
 "rationale": "Make v007's largely advisory pivot rule executable through query admission and persistent cooldowns. The inspected 48-search attempt illustrates noncompliance rather than disproving the pivot hypothesis. Retain Parallel: observed attributed yield is 162.3 correct finds per dollar versus Exa's 84.5, not a controlled accuracy comparison. This candidate changes search scheduling, not the anchoring unit.",
 "instructions": "Define X and Y, entity unit, exclusions, eligible subtypes, membership rules and effective dates. Sequentially run one unrestricted X-only search, one unrestricted Y-only search and one broad conjunction. Maintain deduplicated frontiers, an identity/evidence ledger and a scope ledger. Reserve at least 35% of initial funds for evidence; price all candidate queries and fetches before discovery.\nUse explicit states: DISCOVER, RESOLVE, PIVOT, AUDIT. Before each discovery call write a compact action ticket: frontier; source-backed partition; added restrictions; genuinely new coverage expected; cost including likely checks. Reject a ticket that merely paraphrases an already tried conjunction or adds familiar names without a source-backed reason. Equivalent predicate/subtype/source combinations share one query-family ID, regardless of wording. Record new identities and useful evidence after each call.\nIn DISCOVER, permit at most two consecutive discovery calls before resolving promising pending identities. Select the next frontier by expected verified additions per total resolution cost. Check only unresolved predicates in small affordable Parallel batches, supplying identity and existing evidence. No result is unresolved, not rejection. Reject only on contradiction or an exhaustive applicable record. Escalate selected ambiguous or conflicting cases individually to Exa.\nTwo discovery calls yielding no plausible new identity force PIVOT. Freeze their query families for the rest of the hunt unless newly retrieved evidence changes the question. The next discovery action must be an X-only or Y-only source-backed sibling partition or unrestricted parent on the opposite frontier; it must omit the other predicate and remove a recorded restriction. Resolve resulting candidates before further discovery. If that pivot fails, try at most one distinct source partition or one permitted provider-diversity probe; do not return to frozen conjunctions. A genuinely new source or identity can reopen only its relevant family, not reset all counters.\nStop discovery when pending resolution costs consume remaining funds. Before submission, use up to three affordable residual probes for distinct untested restrictions, stopping after two with neither candidates nor useful evidence. Audit identity, both predicates, membership, subtype and dates. Submit supported intersections only; saturation is not completeness.",
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
 "routing_rules": "Parallel alone, default tier, 8 results for discovery and 4 for exact missing facts and check_candidates. No routine also variants or auto-routing. Charge each candidate and provider separately; result limits are not assumed to reduce prices. Exa alone, 4 results, for individual evidence conflicts or identity ambiguity. Allow at most one Exa discovery probe only after a genuinely different Parallel scope partition fails, continuing only on useful incremental identities or evidence. Use domain filters only for targeted source checks, relax failed filters, and use publication-date filters only when publication date determines eligibility.",
 "fetch_policy": "Reuse cached facts. Fetch authoritative pages settling missing facts or useful candidate lists. Record each list's scope, date, sections and pagination; never equate an excerpt with coverage. Fetch only sections justified by an action ticket. A blocked or uninformative fetch permits one targeted alternate source, not a chain. Include fetch costs in action tickets.",
 "status": "candidate"
}
```
