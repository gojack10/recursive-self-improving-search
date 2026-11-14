---
id: "2cd7a6e5-01df-4b90-9e33-e572f2147e22"
name: "Method v008"
micro_summary: "Evidence-conditioned query repair: retain v006's interruptible sampling but make a zero-progress sample trigger a bounded vocabulary diagnostic when relevant source evidence supports one. This changes"
status: "discarded"
kind: "Idea"
see_also: []
---
**Kind:** Idea

Parent: v006

```json
{
 "id": "v008",
 "parent": "v006",
 "round": 4,
 "rationale": "Evidence-conditioned query repair: retain v006's interruptible sampling but make a zero-progress sample trigger a bounded vocabulary diagnostic when relevant source evidence supports one. This changes how samples are interpreted, rather than requiring a census, source bundles, or a terminal residual-coverage pass. Harvest source-native relationship labels, identifiers and aliases to improve later missing-fact checks and reopen selected parked candidates. Parallel's attributed 135 correct/dollar versus Exa's 56.8 supports keeping cheap retrieval as the default, not a causal quality claim. The improvement remains untested.",
 "instructions": "Define X and Y precisely, including entity unit, eligible subtypes, exclusions and effective dates. Start sequentially with one X search, one Y search and one conjunction search. Maintain deduplicated dual frontiers and a ledger of canonical identities, aliases, predicate evidence, unresolved facts, retrieval formulations and estimated next-action cost. Anchor spending on evidence-backed near-intersections before speculative one-sided candidates. Group candidates only into meaningful discovery-source or subtype cohorts.\nAdd an evidence-derived vocabulary map for each predicate: record source-native relationship terms, registry identifiers, historical names and aliases actually encountered in relevant material. Keep these separate from eligibility rules: retrieval vocabulary may change, eligibility must not. Prefer a candidate's name or stable identifier plus the missing relationship, not a query requiring both predicates to appear on one page. Use known evidence without paying to reverify settled facts.\nFor a speculative cohort, sample at most three diverse candidates, with each dispatch capped at 10% of initial budget except a necessary affordable single check. Inspect evidence before continuing. On zero verified additions or material evidence progress, distinguish explicit disqualifying evidence from absent or off-topic retrieval. For absent/off-topic retrieval, allow one cheap repair only if cached relevant evidence supplies a concrete alternative term, identifier or alias. Retry the most promising unresolved sampled candidate with that evidence-derived formulation. This repair must replace, not supplement, the next exploratory action and remains within the dispatch cap. If no supported alternative exists or the repair adds no evidence, park the cohort and change frontier or partition. Do not generate synonym lists or repeated conjunction paraphrases.\nWhere an existing known-positive record reveals why the original formulation was mismatched, diagnose this from cached evidence first. At most one paid known-positive retrieval diagnostic per hunt is allowed when its result would change several pending checks; it tests retrieval, not eligibility. A successful diagnostic is not a new find and does not justify cohort-wide retries. Reopen at most three promising parked cases when genuinely new source vocabulary creates a distinct resolution path; continue only after useful incremental evidence.\nExpand productive cohorts in small rounds, comparing verified additions and evidence progress per actual spend with discovery alternatives. Retain a neglected-cohort or reverse-frontier probe after two productive rounds. After two discovery queries produce no plausible identities, change source, subtype or frontier. No-hit candidates remain unresolved, never rejected by absence alone; neither sampling nor successful diagnostics establishes completeness. Keep at least 35% of initial budget for verification and resolution, stopping discovery earlier if the pending queue requires it. End with identity, scope and effective-date checks; submit only individually evidenced intersections.",
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
 "routing_rules": "Use Parallel alone, default tier, 8 results for discovery and 4 for exact-name checks, bounded query repairs and first-pass check_candidates. Pass source-derived terminology only where supported and direct checks to missing facts while retaining identity-matched evidence for both predicates. Estimate spend per candidate and provider; lower result counts do not imply lower cost. A vocabulary repair is optional and must not become a mandatory extra step before escalation. Escalate individual promising unresolved candidates to Exa alone with 4 results after a cheap check or targeted fetch fails. Never escalate an entire cohort. After baseline sampling and genuine Parallel stagnation, allow one Exa discovery probe on the weaker frontier if the resolution reserve remains intact; continue only for incremental evidence or identities. No routine concurrent variants or broad auto-routing. Apply domain filters to targeted evidence retrieval, relaxing them when necessary, not to the entire discovery frontier. Publication-date filters apply only when publication date defines eligibility; otherwise inspect effective dates in source content.",
 "fetch_policy": "Cache URLs, facts and source-native terminology. Fetch when content can resolve material identity or predicate uncertainty, expose relevant relationship labels, or provide several plausible candidates. Prefer authoritative sources and shared evidence that reduces pending-check cost, without making source bundles mandatory. Do not fetch solely to build an exhaustive vocabulary map or fetch every result. After a blocked or uninformative page, try one targeted alternate source rather than a fetch chain. Historical terminology can aid retrieval but cannot substitute for evidence of current eligibility.",
 "status": "candidate"
}
```

Discarded in round 4: select 0.382 vs current 0.852.
