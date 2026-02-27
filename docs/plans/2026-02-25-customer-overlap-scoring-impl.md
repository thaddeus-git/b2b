# Implementation Plan: Customer Overlap Scoring

## Overview

Add a new "Customer Overlap" bonus component to the distributor-inspector scoring model to recognize value in adjacent industry distributors (e.g., forklift dealers serving warehouses/factories).

## Files to Modify

| File | Change |
|------|--------|
| `skills/distributor-inspector/SKILL.md` | Add customer overlap bonus, update scoring tables, update routing logic |
| `skills/distributor-inspector/references/keywords.md` | Add target customer keywords |

## Step 1: Add Target Customer Keywords to keywords.md

**Location:** After line ~120 (after Bonus Signals section)

**Add:**
```markdown
---

## Target Customer Keywords (for Customer Overlap Bonus)

Detect if the company serves the same customers OrionStar robots would clean.

| Category | Keywords |
|----------|----------|
| Warehouses/Logistics | warehouse, logistics, distribution center, fulfillment, storage, depot, almacén, logística, entrepôt, logistique, magazzino, logistica |
| Factories/Industrial | factory, manufacturing, industrial, production, plant, fábrica, fabricante, industrial, usine, fabrication, fabbrica, produzione |
| Property/FM | property management, facility management, building services, real estate, gestión inmobiliaria, gestión de instalaciones, gestion immobilière, facility management |
| Retail chains | supermarket, retail chain, stores, multi-site, supermercado, cadena, tiendas, supermarché, chaîne, magasins |

**Detection approach:**
- Look for these keywords in product descriptions, services, customer testimonials, case studies
- Spanish/German/French/Italian variants included for European market coverage
```

## Step 2: Update Scoring Table in SKILL.md

**Location:** Lines 59-66

**Replace:**
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |
```

**With:**
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |
```

## Step 3: Update Grade/Action Table in SKILL.md

**Location:** Lines 69-78

**Replace:**
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

**With:**
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

## Step 4: Update Output Format Table in SKILL.md

**Location:** Lines 107-114 (Scoring Details table)

**Replace:**
```markdown
| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | {pass/fail with reason} | — |
| Cleaning equipment bonus | {level with evidence} | +{bonus} |
| Competitor footprint bonus | {tier with evidence} | +{bonus} |
| Channel capability bonus | {signals detected} | +{bonus} |
| **Total** | (capped at 100) | **{total}** |
```

**With:**
```markdown
| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | {pass/fail with reason} | — |
| Customer overlap bonus | {level with evidence} | +{bonus} |
| Cleaning equipment bonus | {level with evidence} | +{bonus} |
| Competitor footprint bonus | {tier with evidence} | +{bonus} |
| Channel capability bonus | {signals detected} | +{bonus} |
| **Total** | (capped at 100) | **{total}** |
```

## Step 5: Add Customer Overlap Bonus Section in SKILL.md

**Location:** After line 295 (after Channel Capability Bonus section)

**Add:**
```markdown
## Customer Overlap Bonus

Award points for serving target customers that OrionStar robots would clean. This bonus recognizes that distributors in adjacent industries (e.g., forklifts, material handling) may have valuable customer relationships and channel capabilities.

| Level | Evidence | Points |
|-------|----------|--------|
| None | No target customer mentions | +0 |
| Light | One target customer type mentioned | +20 |
| Moderate | 2+ types OR recurring focus | +35 |
| Strong | Core customer base is target sectors | +50 |

**Target customer categories:**
- **Warehouses/Logistics:** warehouse, logistics, distribution center, fulfillment, storage, depot
- **Factories/Industrial:** factory, manufacturing, industrial, production, plant
- **Property/FM:** property management, facility management, building services, real estate
- **Retail chains:** supermarket, retail chain, stores, multi-site

**Detection approach:**
- Look for customer testimonials, case studies, "our clients" sections
- Check service descriptions for target industries
- Identify mentions of warehouse/logistics/factory/retail customers

**Important:** This bonus applies regardless of whether "sells as expected" passes or fails. A forklift distributor serving warehouses can score 50+ through customer overlap + channel capability alone.
```

## Step 6: Update Process Section in SKILL.md

**Location:** Lines 220-226 (Step 4: Score section)

**Replace:**
```markdown
### Step 4: Score

Run required gate check + apply bonuses:
- Required: Sells as expected (PASS/FAIL)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.
```

**With:**
```markdown
### Step 4: Score

Apply all bonuses (even if "sells as expected" fails):
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.
```

## Step 7: Update Step 5: Route Section in SKILL.md

**Location:** Lines 229-242

**Replace:**
```markdown
### Step 5: Route

Return action + play recommendation:

**For distributors (PASS required gate):**
- Grade A (90+): `prioritize`
- Grade B (70-89): `standard`
- Grade C (50-69): `explore`
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play

**For non-distributors (FAIL required gate):**
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka` + note "Use KA-inspector for Key Account evaluation"
- All others: `exclude`
```

**With:**
```markdown
### Step 5: Route

Return action + play recommendation based on score:

| Score | Gate | Action |
|-------|------|--------|
| 90+ | PASS | `prioritize` |
| 70-89 | PASS | `standard` |
| 50-69 | Any | `explore` |
| <50 | Any | `exclude` |

**Special routing (overrides score):**
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:** Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`.
```

## Verification

After implementation, re-inspect Tomi Maquinaria (https://tomimaquinaria.com/) and verify:
1. Customer overlap bonus detected: +50 (Strong - warehouses, factories, logistics)
2. Channel capability bonus: +20 (SAT, parts, training, multi-location)
3. Total score: 70/100
4. Action: `standard` (not `exclude`)