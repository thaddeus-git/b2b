# Scoring Matrix - Distributor Qualification

> **Purpose:** Complete bonus scoring matrix with all ICP criteria
> **Application:** Applied AFTER hard gates are evaluated
> **Total:** Capped at 100 points
> **Updated:** 2026-02-27

---

## Overview

This document provides the **complete scoring matrix** for the distributor-inspector skill. All bonus points are accumulated and capped at 100.

**Scoring Flow:**
1. Check hard gates → Determine max eligible grade
2. Apply bonus scoring → Calculate raw score
3. Cap at 100 → Final score
4. Map score + gates to action

---

## Base Score

| Component | Points | Condition |
|-----------|--------|-----------|
| Base for qualified B2B company | 60 | Passes hard gates (all or most) |
| Base for partially qualified | 40 | 1-2 gate fails (explore tier) |
| Base for unqualified | 0 | 3+ gate fails (exclude) |

---

## Bonus Scoring Matrix

### 1. Cleaning Equipment Focus (Max +90)

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment in passing | +30 |
| Moderate | Has dedicated cleaning equipment product category | +50 |
| Strong | Core offering, multiple cleaning equipment lines | +70 |
| Dominant | Primary business, extensive catalog, multiple brands | +90 |

**Detection:** Product pages, catalog structure, brand portfolio

---

### 2. Competitor Footprint (Max +90)

| Tier | Evidence | Points |
|------|----------|--------|
| Tier 1 | Official distributor / Authorized partner | +90 |
| Tier 2 | Product pages / Clear sales evidence | +60 |
| Tier 3 | Mentions only (blog, comparison) | +30 |

**Detection:** Brand partnership language, product listings

**Country Adjustment:**
- France: +10 bonus (Tier 1: +100→cap, Tier 2: +70, Tier 3: +40)

---

### 3. Distribution Network (Max +20)

| Signal | Points |
|--------|--------|
| ANY distribution network signal | +20 |

**Detection:**
- Reseller program page
- "Become a dealer" language
- Partner directory
- Tier-2 distributor mentions

---

### 4. System Integration Capability (Max +20)

| Signal | Points |
|--------|--------|
| ANY system integration signal | +20 |

**Detection:**
- Integration services mentioned
- API/SDK keywords
- Customization capability
- "Solutions provider" language

**Country Adjustment:**
- Germany: +10 bonus (total +30)

---

### 5. Existing FM/Property Customers (Max +15)

| Evidence | Points |
|----------|--------|
| FM case study | +5 |
| Property testimonial | +5 |
| FM references listed | +5 |
| Dedicated FM sector section | +5 |

**Detection:** Customer names, sector pages, case studies

---

### 6. After-sales Maturity (Max +15)

| Signal | Points |
|--------|--------|
| SLA page or dedicated section | +5 |
| Spare parts inventory mentioned | +5 |
| Ticket/support portal | +5 |
| Certified technicians | +5 |
| 24/7 support mentioned | +5 |

**Accumulation:** Up to +15

**Country Adjustment:**
- Spain: +10 bonus (total +25)

---

### 7. Demo/Showroom Capability (Max +10)

| Signal | Points |
|--------|--------|
| Showroom/demo center | +5 |
| Demo policy mentioned | +5 |
| Training center | +5 |
| Mobile demo capability | +5 |

**Accumulation:** Up to +10

---

### 8. Marketing Investment (Max +10)

| Signal | Points |
|--------|--------|
| Exhibition/trade fair mentions | +5 |
| Marketing budget mentioned | +5 |
| Content marketing (blog, videos) | +5 |
| Active social media | +5 |

**Accumulation:** Up to +10

---

### 9. Customer Overlap (Max +50)

| Evidence | Points |
|----------|--------|
| Per customer category (best evidence) | +10 to +15 |
| Multiple in same segment bonus | +5 |

**Accumulation:** Up to +50

**See:** `icp-skill/customer-overlap-rules.md` for detailed logic

---

## Complete Scoring Example

### Company: German Cleaning Equipment Distributor

**Profile:**
- Sells Tennant scrubbers and Nilfisk vacuums (competitor footprint)
- Has 3 branches in DACH region
- Service page with "24h response, spare parts warehouse"
- Case studies: BMW factory, Edeka supermarket, Marriott hotel
- Showroom with demo machines
- Active on LinkedIn, exhibits at ISSA Messe

**Scoring:**

| Component | Calculation | Points |
|-----------|-------------|--------|
| Base score | Qualified B2B | 60 |
| Cleaning equipment | Strong (multiple brands) | +70 |
| Competitor footprint | Tier 2 (Tennant, Nilfisk products) | +60 |
| Distribution network | Partner page found | +20 |
| System integration | No signals | +0 |
| FM customers | Factory + retail + hotel (3 categories) | +30 |
| After-sales maturity | SLA + spare parts (2 signals) | +10 |
| Demo capability | Showroom + demo policy | +10 |
| Marketing | Exhibition + social media | +10 |
| **Raw Total** | | **270** |
| **Capped at 100** | | **100** |

**Hard Gates:** All pass
**Final Grade:** A (100/100)
**Action:** prioritize

---

### Company: French HVAC Company (No Cleaning Equipment)

**Profile:**
- Sells HVAC equipment (not cleaning)
- No competitor robotics brands
- Serves office buildings and hospitals
- Has service team but no dedicated SLA page
- Single location, no branches

**Scoring:**

| Component | Calculation | Points |
|-----------|-------------|--------|
| Base score | Partially qualified (1 gate fail) | 40 |
| Cleaning equipment | None | +0 |
| Competitor footprint | None | +0 |
| Distribution network | Not detected | +0 |
| System integration | No signals | +0 |
| FM customers | Office buildings + hospitals (2 categories) | +20 |
| After-sales maturity | Service mentioned only | +5 |
| Demo capability | No showroom | +0 |
| Marketing | Minimal signals | +0 |
| **Raw Total** | | **65** |
| **Capped (explore tier max)** | | **50** |

**Hard Gates:** 1-2 fails (SLA, market coverage)
**Final Grade:** C (50/100)
**Action:** explore

---

### Company: Spanish Cleaning Services Company

**Profile:**
- Provides cleaning services (not equipment sales)
- Serves hotels, offices, retail chains
- Has 5 locations across Spain
- Service page with "2h response" SLA
- No robot competitors, no cleaning equipment sales

**Scoring:**

| Component | Calculation | Points |
|-----------|-------------|--------|
| Base score | Qualified (service provider) | 60 |
| Cleaning equipment | Service, not equipment | +0 |
| Competitor footprint | None | +0 |
| Distribution network | N/A (service co) | +0 |
| System integration | No signals | +0 |
| FM customers | Hospitality + retail + offices (3 categories) | +30 |
| After-sales maturity | SLA page (strong) | +15 |
| Demo capability | No | +0 |
| Marketing | Some signals | +5 |
| **Raw Total** | | **110** |
| **Capped at 100** | | **100** |

**Hard Gates:** All pass
**Special Tag:** `cleaning-services-provider`
**Final Grade:** A (100/100)
**Action:** service-provider-prospect (not prioritize)

---

## Score to Grade Mapping

| Score Range | Gates Met | Grade | Action |
|-------------|-----------|-------|--------|
| 90-100 | All gates pass | A | prioritize |
| 70-89 | All gates pass | B | standard |
| 50-69 | Any | C | explore |
| < 50 | Any | D/F | exclude |

**Special routing overrides:**

| Condition | Override Action |
|-----------|-----------------|
| Competitor distributor (Tier 1-2) | route-to-sales |
| `cleaning-services-provider` tag | service-provider-prospect |
| `hospitality-service-provider` tag | route-to-ka |
| `pure-2c-retail` with no commercial | exclude |

---

## Country Adjustment Summary

| Country | Adjustment | Applied To |
|---------|------------|------------|
| France (FR) | Competitor +10 | Competitor footprint |
| Spain (ES) | After-sales +10 | After-sales maturity |
| Germany (DE) | Integration +10 | System integration |

---

## Implementation Pseudocode

```python
def calculate_score(company_profile, country):
    # Step 1: Check hard gates
    gate_result = check_hard_gates(company_profile)

    # Step 2: Determine base score and max cap
    if gate_result == 'ALL_PASS':
        base_score = 60
        max_cap = 100
    elif gate_result == 'SOME_FAIL':  # 1-2 fails
        base_score = 40
        max_cap = 50  # Cap at explore tier
    else:  # 3+ fails
        return 0, 'exclude'

    # Step 3: Calculate bonuses
    bonuses = {
        'cleaning_equipment': score_cleaning_equipment(company_profile),
        'competitor_footprint': score_competitor_footprint(company_profile),
        'distribution_network': score_distribution_network(company_profile),
        'system_integration': score_system_integration(company_profile),
        'fm_customers': score_fm_customers(company_profile),
        'after_sales': score_after_sales(company_profile),
        'demo_capability': score_demo_capability(company_profile),
        'marketing': score_marketing(company_profile),
        'customer_overlap': score_customer_overlap(company_profile),
    }

    # Step 4: Apply country adjustments
    if country == 'FR':
        bonuses['competitor_footprint'] = min(bonuses['competitor_footprint'] + 10, 90)
    elif country == 'ES':
        bonuses['after_sales'] = min(bonuses['after_sales'] + 10, 15)
    elif country == 'DE':
        bonuses['system_integration'] = min(bonuses['system_integration'] + 10, 20)

    # Step 5: Sum and cap
    raw_total = base_score + sum(bonuses.values())
    final_score = min(raw_total, max_cap)

    # Step 6: Map to grade and action
    grade, action = map_to_action(final_score, gate_result, company_profile.tags)

    return final_score, grade, action
```

---

## Quick Reference Table

| Bonus Criterion | Max | Detection |
|-----------------|-----|-----------|
| Cleaning equipment | +90 | Product catalog |
| Competitor footprint | +90 | Brand partnerships |
| Distribution network | +20 | Reseller program |
| System integration | +20 | API/solutions |
| FM customers | +15 | Case studies |
| After-sales maturity | +15 | SLA/spare parts |
| Demo capability | +10 | Showroom/demo |
| Marketing | +10 | Exhibitions/social |
| Customer overlap | +50 | Target customers |

**Base:** 60 (qualified) or 40 (partial)
**Cap:** 100 (or 50 for explore tier)
