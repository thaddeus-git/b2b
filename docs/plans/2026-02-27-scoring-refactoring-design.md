# Scoring Refactoring - Distributor ICP Reorganization

**Date:** 2026-02-27
**Owner:** distributor-inspector skill
**Status:** Implemented

---

## Summary

Reorganized the distributor-inspector skill's scoring logic to properly implement the Sales ICP requirements from `human_input/Distributor ICP.md`. The key change: **hard gates are now checked BEFORE bonus scoring**, preventing unqualified companies from receiving high scores.

---

## Problem

The original scoring system had a critical flaw: it awarded high scores to companies that failed fundamental qualification criteria.

**Example: D.S.Weiss Kälte-Klima-Service**
- Scored 75/100 (B grade, "standard" action)
- Reality: 5-6 employees (fails 20-500 gate), no SLA detected (fails SLA gate), manufacturer not distributor (wrong business model)

The scoring logic was inverted:
- **What it did:** "Related industry + customer overlap = good prospect"
- **What ICP says:** "Hard gates first, THEN bonus scoring"

---

## Solution

Created a new ICP reference structure that separates:
1. **Hard gates** (must-pass qualifications)
2. **Bonus criteria** (differentiators for qualified companies)
3. **Gate translation logic** (how AI detects each requirement)

---

## Files Created

### Sales Team Reference (`references/icp-sales/`)

| File | Purpose |
|------|---------|
| `hard-gates.md` | 6 hard gates with AI detection methods |
| `bonus-criteria.md` | 9 bonus criteria from Sales ICP |
| `target-industries.md` | Priority-ordered industry list |
| `exclusion-rules.md` | Exclusion criteria with examples |
| `country-strategies.md` | FR/ES/DE/HU/CH/GR specific approaches |

### AI Skill Implementation (`references/icp-skill/`)

| File | Purpose |
|------|---------|
| `gate-translation.md` | How AI interprets each sales requirement |
| `scoring-matrix.md` | Complete bonus scoring matrix |
| `customer-overlap-rules.md` | Explicit customer overlap scoring |

### Quick Reference

| File | Purpose |
|------|---------|
| `references/icp-summary.md` | Single-page reference for sales + AI |

---

## Key Changes

### 1. Hard Gates Enforced

**Before:** Single gate ("sells as expected")

**After:** 6 hard gates:
1. Company Size (20-500 employees, €10M revenue)
2. Team Capability (Sales + Deployment + After-sales)
3. SLA Capability (quantifiable response times)
4. PoC Capability (demo/trial support)
5. Market Coverage (1-3 cities)
6. Price Discipline (MSRP adherence)

**Gate Logic:**
- ALL PASS → Eligible for A/B grade
- 1-2 FAIL → Cap at 50 points (explore tier)
- 3+ FAIL → Route to exclude

---

### 2. Customer Overlap Rules Clarified

**Before:** Vague "one type" vs "2+ types"

**After:** Explicit category-based scoring:
- 5 non-overlapping categories (Industrial, Commercial Real Estate, Retail, Hospitality, Public/Institutional)
- +10 to +15 per category based on evidence strength
- +5 bonus for multiple customers in same segment
- Capped at +50

**Example:**
- Company serves warehouses + factories + logistics = 1 category (Industrial) = +15 max
- Company serves supermarkets + office buildings + hotels = 3 categories = +30 to +45

---

### 3. Expanded Bonus Criteria

**Before:** 4 bonus components

**After:** 9 bonus components:
- Cleaning equipment focus (+90)
- Competitor footprint (+90)
- Distribution network (+20)
- System integration capability (+20)
- Existing FM/property customers (+15)
- After-sales maturity (+15)
- Demo/showroom capability (+10)
- Marketing investment (+10)
- Customer overlap (+50)

---

### 4. Country Strategy Integration

**Added:** Country-specific scoring adjustments:
- France: Competitor footprint +10 bonus
- Spain: After-sales maturity +10 bonus
- Germany: System integration +10 bonus

---

### 5. Updated Output Format

**Added to reports:**
- Hard Gates Evaluation table (6 gates with evidence)
- Gate Result summary (ALL_PASS / SOME_FAIL / MOST_FAIL)
- Expanded scoring breakdown (9 bonus components)

---

## Impact on Example Cases

### D.S.Weiss Kälte-Klima-Service (Re-evaluated)

**Original Score:** 75/100 (B grade, standard)

**Re-evaluated Gates:**
| Gate | Result | Evidence |
|------|--------|----------|
| Company Size | FAIL | 5-6 employees (< 20) |
| Team Capability | FAIL | No clear sales/deployment separation |
| SLA Capability | FAIL | No SLA detected |
| PoC Capability | UNCLEAR | No demo policy mentioned |
| Market Coverage | PASS | International projects (Austria, Ivory Coast) |
| Price Discipline | UNCLEAR | No pricing language |

**Gate Result:** 3+ FAIL → Route to `exclude`

**Corrected Action:** `exclude` (or `explore` if manually reviewed and found to have specialized value)

---

## Migration Notes

### For the AI Skill

**Scoring Flow:**
1. Extract company profile from snapshot
2. Check hard gates → Determine max eligible grade
3. Apply bonus scoring → Calculate raw score
4. Cap at 100 or 50 based on gates
5. Apply country adjustments
6. Map to action (considering special routing)

**Key Files:**
- `icp-sales/hard-gates.md` - Gate detection
- `icp-skill/gate-translation.md` - Translation logic
- `icp-skill/scoring-matrix.md` - Bonus scoring

### For the Sales Team

**What Changed:**
- Scores now reflect ICP qualification logic
- Companies failing hard gates won't appear as "A/B" prospects
- Customer overlap is scored consistently

**What Stayed the Same:**
- Output format (enhanced with gate table)
- Action routing (prioritize/standard/explore/exclude)
- Special routing for competitor distributors

---

## Testing Plan

**Test Cases:**

| Company Type | Expected Gate Result | Expected Action |
|--------------|---------------------|-----------------|
| Qualified cleaning equipment distributor (50 emp, €15M, 3 branches) | ALL_PASS | prioritize (if high bonuses) or standard |
| Small specialized firm (8 emp, €12M, no service team) | SOME_FAIL (1-2) | explore (capped at 50) |
| Manufacturer/service provider (5 emp, no SLA) | MOST_FAIL (3+) | exclude |
| Competitor distributor (Pudu official partner) | ALL_PASS + competitor bonus | route-to-sales |
| Pure B2C retail (no commercial products) | N/A (pre-check) | exclude |
| Cleaning services company | ALL_PASS (if gates met) | service-provider-prospect |

**Validation:**
- Run existing test URLs through updated skill
- Verify D.S.Weiss-type companies route to exclude/explore
- Verify competitor distributors still route to sales

---

## Future Improvements

1. **LinkedIn Integration:** Automate employee count verification
2. **Revenue Detection:** Improve financial signal extraction
3. **SLA Extraction:** Dedicated SLA page detection
4. **Demo Policy:** Structured demo/trial policy extraction
5. **Country Expansion:** Add more country strategies (IT, NL, BE, etc.)

---

## References

- Sales ICP: `human_input/Distributor ICP.md`
- Original Scoring: `references/scoring-rules.md` (superseded)
- Quick Reference: `references/icp-summary.md`
