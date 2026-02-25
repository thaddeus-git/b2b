# Design: Customer Overlap Scoring for Distributor Inspector

## Problem

Tomi Maquinaria (forklift distributor) was scored 0/100 despite having:
- Strong B2B distribution model
- After-sales service (SAT), parts, training
- Multi-location presence in Spain
- Customer base of warehouses and factories

The sales team considers them valuable because they **serve the same customers** OrientStar robots would clean.

The current scoring model has a hard PASS/FAIL gate on "sells as expected" (cleaning equipment). If a company fails this gate, score = 0 regardless of other strengths.

## Solution

### 1. Remove Hard Gate Behavior

Change scoring so bonuses apply even when "sells as expected" FAILs. A company can still score 50+ through customer overlap + channel capability.

### 2. Add New "Customer Overlap" Bonus

Award points for serving target customers that OrientStar robots would clean:

| Level | Evidence | Points |
|-------|----------|--------|
| None | No target customer mentions | +0 |
| Light | One target customer type mentioned | +20 |
| Moderate | 2+ target customer types OR recurring focus | +35 |
| Strong | Core customer base is target sectors | +50 |

**Target customer keywords by category:**

| Category | Keywords |
|----------|----------|
| Warehouses/Logistics | warehouse, logistics, distribution center, fulfillment, storage, depot |
| Factories/Industrial | factory, manufacturing, industrial, production, plant |
| Property/FM | property management, facility management, building services, real estate |
| Retail chains | supermarket, retail chain, stores, multi-site |

## New Scoring Model

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL (informational) |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

**Total capped at 100.**

## New Routing Logic

| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90+ | PASS gate | prioritize |
| B | 70-89 | PASS gate | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |
| — | — | Tier 1-2 competitor | route-to-sales |
| — | — | cleaning-services-provider | service-provider-prospect |
| — | — | hospitality-service-provider | route-to-ka |

**Key change:** FAIL + score ≥50 now routes to `explore` instead of `exclude`.

## Example: Tomi Maquinaria Re-scored

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | FAIL - Material handling equipment | — |
| Customer overlap | Strong - Warehouses, factories, logistics focus | +50 |
| Cleaning equipment | None | +0 |
| Competitor footprint | None | +0 |
| Channel capability | Strong (SAT, parts, training, multi-location) | +20 |
| **Total** | | **70/100** |

**Grade: B** → Action: **standard** (not exclude)

## Files to Modify

- `skills/distributor-inspector/SKILL.md`

## Changes to SKILL.md

### A. Update Scoring Table (line ~59-66)

Replace:
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |
```

With:
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |
```

### B. Update Grade/Action Table (line ~69-78)

Replace:
```markdown
| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude (or non-distributor routing) |
| Tier 1-2 competitor footprint | — | route-to-sales + play |
| cleaning-services-provider tag | — | service-provider-prospect |
| hospitality-service-provider tag | — | route-to-ka |
```

With:
```markdown
| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90+ | PASS gate | prioritize |
| B | 70-89 | PASS gate | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |
| — | — | Tier 1-2 competitor | route-to-sales |
| — | — | cleaning-services-provider | service-provider-prospect |
| — | — | hospitality-service-provider | route-to-ka |
```

### C. Add Customer Overlap Bonus Section (after line ~295)

Add new section:
```markdown
## Customer Overlap Bonus

Award points for serving target customers that OrientStar robots would clean.

| Level | Evidence | Points |
|-------|----------|--------|
| Light | One target customer type mentioned | +20 |
| Moderate | 2+ types OR recurring focus | +35 |
| Strong | Core customer base is target sectors | +50 |

**Target customer keywords:**
- Warehouses/Logistics: warehouse, logistics, distribution center, fulfillment
- Factories/Industrial: factory, manufacturing, industrial, production
- Property/FM: property management, facility management, building services
- Retail chains: supermarket, retail chain, stores, multi-site
```

### D. Update Output Format Table (line ~107-114)

Add row:
```markdown
| Customer overlap bonus | {level with evidence} | +{bonus} |
```

## Success Criteria

1. Tomi Maquinaria scores 60+ (reaches "explore" or "standard")
2. Cleaning equipment distributors still score high (no regression)
3. Competitor footprint still triggers `route-to-sales`
4. Adjacent industry distributors with strong customer overlap + channel capability score 50+