# Scoring Rules for Distributor Inspector

> **Status:** Legacy scoring rules - preserved for reference
> **Current:** See `icp-skill/scoring-matrix.md` for active scoring
> **Updated:** 2026-02-27

---

## Current Scoring Implementation

**This file has been superseded by the new ICP structure.** For current scoring rules, see:

| Document | Purpose |
|----------|---------|
| `icp-summary.md` | Quick reference for sales + AI |
| `icp-sales/hard-gates.md` | Hard qualification gates |
| `icp-sales/bonus-criteria.md` | Bonus criteria from sales ICP |
| `icp-skill/gate-translation.md` | How AI interprets each gate |
| `icp-skill/scoring-matrix.md` | Complete bonus scoring matrix |
| `icp-skill/customer-overlap-rules.md` | Explicit customer overlap scoring |

---

## Legacy Scoring Components (Reference Only)

The table below shows the original scoring structure for historical reference.

| Component | Points | Current Location |
|-----------|--------|------------------|
| Required: Sells as expected | PASS/FAIL | `icp-sales/hard-gates.md` |
| Bonus: Customer overlap | +0 to +50 | `icp-skill/customer-overlap-rules.md` |
| Bonus: Cleaning equipment | +30 to +90 | `icp-sales/bonus-criteria.md` |
| Bonus: Competitor footprint | +30 to +90 | `icp-sales/bonus-criteria.md` |
| Bonus: Channel capability | +0 to +20 | `icp-skill/scoring-matrix.md` (expanded) |

---

## Key Changes (v2.0 Update)

### 1. Hard Gates Now Enforced

**Before:** Single gate ("sells as expected")

**After:** 6 hard gates from Sales ICP:
- Company size (20-500 employees)
- Team capability (sales + deployment + after-sales)
- SLA capability (quantifiable response times)
- PoC capability (demo/trial support)
- Market coverage (1-3 cities)
- Price discipline (MSRP adherence)

**Impact:** Companies like D.S.Weiss (5 employees, no SLA) now correctly route to `exclude` or `explore` instead of `standard`.

---

### 2. Customer Overlap Rules Clarified

**Before:** Vague "one type" vs "2+ types"

**After:** Explicit category-based scoring:
- 5 non-overlapping categories (Industrial, Commercial Real Estate, Retail, Hospitality, Public/Institutional)
- Points per category with evidence strength
- Multiple customers in same segment = +5 bonus

**Impact:** Consistent scoring across different AI sessions.

---

### 3. Expanded Bonus Criteria

**Before:** 4 bonus components

**After:** 9 bonus components matching Sales ICP:
- Distribution network (+20)
- System integration capability (+20)
- Existing FM/property customers (+15)
- After-sales maturity (+15)
- Demo/showroom capability (+10)
- Marketing investment (+10)

**Impact:** Better differentiation between good and great distributors.

---

### 4. Country Strategy Integration

**Before:** No country adjustments

**After:** Country-specific scoring adjustments:
- France: Competitor footprint +10 bonus
- Spain: After-sales maturity +10 bonus
- Germany: System integration +10 bonus

**Impact:** Aligns with country-specific sales strategies.

---

### 5. Gate-Based Score Capping

**Before:** All companies scored 0-100

**After:** Score caps based on gate performance:
- All gates pass: Cap at 100 (A/B grade eligible)
- 1-2 gates fail: Cap at 50 (explore tier only)
- 3+ gates fail: Route to exclude

**Impact:** Prevents unqualified companies from scoring into "standard" tier.

---

## Grade & Action Mapping (Unchanged)

| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90-100 | All gates pass | prioritize |
| B | 70-89 | All gates pass | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |

**Special routing (overrides score):**
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`
- Tagged `pure-2c-retail` with NO commercial products: `exclude`

---

## Migration Notes

**For the AI Skill:**

1. Check hard gates FIRST before applying any bonus scoring
2. Use `icp-skill/gate-translation.md` for gate detection logic
3. Apply bonus scoring from `icp-skill/scoring-matrix.md`
4. Cap scores based on gate results
5. Apply country adjustments last

**For the Sales Team:**

1. Use `icp-summary.md` as your quick reference
2. Hard gates are non-negotiable qualification criteria
3. Bonus criteria differentiate good from great distributors
4. Country strategies adjust priorities by market

---

## Appendix: Original Scoring Details

Preserved below for historical reference.

### Original Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment | +30 |
| Moderate | Has product category | +50 |
| Strong | Core offering, multiple products | +70 |
| Dominant | Primary business, extensive catalog | +90 |

### Original Competitor Footprint Bonus

| Tier | Evidence | Points |
|------|----------|--------|
| Tier 1 | Official distributor / Authorized partner | +90 |
| Tier 2 | Product pages / Sales evidence | +60 |
| Tier 3 | Mentions only | +30 |

### Original Customer Overlap Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| None | No target customer mentions | +0 |
| Light | One target customer type | +20 |
| Moderate | 2+ types OR recurring focus | +35 |
| Strong | Core customer base is target sectors | +50 |

---

**See:** `docs/plans/2026-02-27-scoring-refactor-design.md` for the full reorganization plan.
