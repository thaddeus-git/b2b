# Scoring Matrix - KA End Customer

> **Purpose:** Complete bonus scoring matrix for KA prospects
> **Application:** Applied AFTER hard gates are evaluated
> **Total:** Capped at 100 points
> **Updated:** 2026-02-27

---

## Overview

This document provides the **complete scoring matrix** for the ka-inspector skill. All bonus points are accumulated and capped at 100.

**Scoring Flow:**
1. Check hard gates → Determine max eligible grade
2. Apply bonus scoring → Calculate raw score
3. Cap at 100 → Final score
4. Map score + gates to action

---

## Base Score

| Component | Points | Condition |
|-----------|--------|-----------|
| Base for qualified KA prospect | 50 | Has budget + on-site contact |
| Base for partial | 30 | 1 gate fail |
| Base for unqualified | 0 | 2+ gates fail (exclude) |

---

## Bonus Scoring Matrix

### 1. Multi-site Potential (Max +30)

| Level | Evidence | Points |
|-------|----------|--------|
| Light | 2-5 locations mentioned | +10 |
| Moderate | 6-20 locations or "chain" language | +20 |
| Strong | 20+ locations or "national chain" | +30 |

**Detection:** Locations page, branch count, "our stores", "our properties"

---

### 2. Digital Maturity (Max +20)

| Signal | Points |
|--------|--------|
| Work order system | +5 |
| Asset management | +5 |
| IoT/Smart building | +5 |
| Digital transformation | +5 |

**Accumulation:** Up to +20

**Detection:** "Work order", "ticketing", "BMS", "IoT", "digital transformation"

---

### 3. Pilot KPI Clarity (Max +20)

| Signal | Points |
|--------|--------|
| Efficiency metrics | +5 |
| Cost reduction | +5 |
| Stability/reliability | +5 |
| SLA mentions | +5 |

**Accumulation:** Up to +20

**Detection:** "Efficiency", "productivity", "cost reduction", "SLA", "uptime"

---

### 4. Cross-team Coordination (Max +15)

| Signal | Points |
|--------|--------|
| Facilities + Operations | +5 |
| Procurement involvement | +5 |
| Project management | +5 |

**Accumulation:** Up to +15

**Detection:** Multiple departments mentioned, "cross-functional", "project team"

---

## Complete Scoring Example

### Company: German Retail Chain

**Profile:**
- 50 supermarket locations across Germany
- Facilities management department
- Hiring for automation roles
- Uses work order system
-mentions "efficiency" and "cost optimization"

**Scoring:**

| Component | Calculation | Points |
|-----------|-------------|--------|
| Base score | Has budget + contact | 50 |
| Multi-site | 50 locations (strong) | +30 |
| Digital maturity | Work order system | +5 |
| Pilot KPI | Efficiency + cost mentions | +10 |
| Cross-team | Facilities mentioned | +5 |
| **Raw Total** | | **100** |
| **Capped at 100** | | **100** |

**Hard Gates:** All pass
**Final Grade:** A (100/100)
**Action:** pilot-ready (prioritize)

---

### Company: Single Hotel

**Profile:**
- One hotel property
- Small facilities team
- No digital systems mentioned
- No clear budget signals

**Scoring:**

| Component | Calculation | Points |
|-----------|-------------|--------|
| Base score | Partial (1 gate fail) | 30 |
| Multi-site | Single location | +0 |
| Digital maturity | No signals | +0 |
| Pilot KPI | No signals | +0 |
| Cross-team | Operations mentioned | +5 |
| **Raw Total** | | **35** |
| **Capped (nurture tier)** | | **35** |

**Hard Gates:** 1 fail (budget unclear)
**Final Grade:** D (35/100)
**Action:** exclude

---

## Score to Grade Mapping

| Score Range | Gates Met | Grade | Action |
|-------------|-----------|-------|--------|
| 80-100 | All | A | pilot-ready (prioritize) |
| 60-79 | All | B | pilot-ready (standard) |
| 40-59 | Any | C | nurture |
| <40 | Any | D/F | exclude |

---

## Implementation Pseudocode

```python
def calculate_score(ka_profile):
    # Step 1: Check hard gates
    gate_result = check_hard_gates(ka_profile)

    # Step 2: Determine base score and max cap
    if gate_result == 'ALL_PASS':
        base_score = 50
        max_cap = 100
    elif gate_result == 'SOME_FAIL':  # 1 fail
        base_score = 30
        max_cap = 59  # Cap at nurture tier
    else:  # 2+ fails
        return 0, 'exclude'

    # Step 3: Calculate bonuses
    bonuses = {
        'multi_site': score_multi_site(ka_profile),
        'digital_maturity': score_digital_maturity(ka_profile),
        'pilot_kpi': score_pilot_kpi(ka_profile),
        'cross_team': score_cross_team(ka_profile),
    }

    # Step 4: Sum and cap
    raw_total = base_score + sum(bonuses.values())
    final_score = min(raw_total, max_cap)

    # Step 5: Map to grade and action
    grade, action = map_to_action(final_score, gate_result)

    return final_score, grade, action
```

---

## Quick Reference Table

| Bonus Criterion | Max | Detection |
|-----------------|-----|-----------|
| Multi-site potential | +30 | Location count, chain language |
| Digital maturity | +20 | Work order, IoT, BMS |
| Pilot KPI | +20 | Efficiency, cost, SLA |
| Cross-team coordination | +15 | Multiple departments |

**Base:** 50 (has budget + contact) or 30 (partial)
**Cap:** 100 (or 59 for nurture tier)
