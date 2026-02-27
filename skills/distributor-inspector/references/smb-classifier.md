# SMB Classifier - Small Business Detection

> **Purpose:** Classify companies as SMB vs. Mid-Market vs. Key Account
> **Application:** Applied AFTER company profile extraction, BEFORE hard gates
> **Last Updated:** 2026-02-27

---

## Overview

This document provides classification rules to determine company scale and sophistication. The output determines:
1. **Score cap** (max eligible points)
2. **Routing priority** (SMBs typically route to nurture/explore)
3. **Sales motion** (KA = enterprise motion, SMB = transactional)

---

## Classification Decision Tree

```
                        ┌─────────────────────────┐
                        │  Start Classification   │
                        └───────────┬─────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │  Extracted Employee   │
                        │  Count from Profile   │
                        └───────────┬───────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │   < 20        │       │   20 - 500    │       │   > 500       │
    │   employees   │       │   employees   │       │   employees   │
    └───────┬───────┘       └───────┬───────┘       └───────┬───────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │  CHECK:       │       │  CHECK:       │       │     KA        │
    │  Locations,   │       │  Locations,   │       │  (full 100)   │
    │  Structure    │       │  Structure    │       │               │
    └───────┬───────┘       └───────┬───────┘       └───────────────┘
            │                       │
            ▼                       ▼
    ┌───────────────┐       ┌───────────────┐
    │ Single loc +  │       │ 2-5 locations │
    │ no depts      │       │ OR departments│
    └───────┬───────┘       └───────┬───────┘
            │                       │
            ▼                       ▼
    ┌───────────────┐       ┌───────────────┐
    │     SMB       │       │  MID-MARKET   │
    │  (cap at 50)  │       │  (cap at 75)  │
    └───────────────┘       └───────────────┘
```

---

## Classification Criteria

### Primary Signals (Extracted from Company Profile)

| Signal | SMB | Mid-Market | KA |
|--------|-----|------------|-----|
| **Employees** | <20 | 20-500 | 500+ |
| **Locations** | Single property | 2-5 branches | 6+ branches |
| **Team Structure** | No departments | 2-3 departments | 4+ departments |
| **Revenue** | Not stated / <€5M | €5M-€50M | €50M+ |
| **Procurement** | Not visible | Mentioned | Dedicated function |
| **Web Maturity** | Basic info only | Some case studies | Resource center |

### Secondary Signals (Confidence Boosters)

| Signal | Indicates |
|--------|-----------|
| "Family business", "Familienbetrieb" | Likely SMB |
| "Gasthof", "Pension", single hotel | Likely SMB |
| Team photo <10 people | Likely SMB |
| Multiple locations listed | Not SMB |
| "Group", "Holdings", "International" | Likely KA |
| Investor backing mentioned | Likely KA |
| Careers page with multiple roles | Not SMB |
| Case studies from named enterprises | Not SMB |

---

## Classification Rules

### Rule 1: Employee Count (Highest Confidence)

```python
if explicit_employee_count:
    if count < 20:
        classification = "SMB"
        confidence = "HIGH"
    elif 20 <= count <= 500:
        classification = "MID-MARKET"
        confidence = "HIGH"
    elif count > 500:
        classification = "KA"
        confidence = "HIGH"
```

### Rule 2: Location Count (High Confidence)

```python
if location_count == 1 and employee_count_unknown:
    # Check for department structure
    if no_departments_visible and family_business_mentioned:
        classification = "SMB"
        confidence = "MEDIUM"
    elif departments_visible:
        classification = "MID-MARKET"
        confidence = "MEDIUM"

elif location_count >= 2 and location_count <= 5:
    classification = "MID-MARKET"
    confidence = "HIGH"

elif location_count > 5:
    classification = "KA"
    confidence = "HIGH"
```

### Rule 3: Structure Inference (Medium Confidence)

```python
# Check for organizational sophistication
signals = {
    'procurement_function': 'Einkauf' in page or 'Procurement' in page,
    'dedicated_service_page': '/service' in urls or 'Service' in nav,
    'careers_page': '/careers' in urls or 'Jobs' in nav,
    'case_studies': '/references' in urls or 'Case Studies' section,
    'investor_relations': 'Investors' mentioned,
    'multiple_brands': Multiple consumer-facing brands,
}

sophistication_score = sum(signals.values())

if sophistication_score <= 1 and location_count == 1:
    classification = "SMB"
    confidence = "MEDIUM"
elif sophistication_score >= 4:
    classification = "KA"
    confidence = "MEDIUM"
```

### Rule 4: Industry-Type Heuristics (Lower Confidence)

```python
# Certain business types are typically SMB
smb_business_types = [
    'Gasthof', 'Pension', 'Gasthaus',  # Austrian/German inns
    'Einzelhandel', 'Retail shop',      # Single retail
    'Praxis', 'Practice',               # Medical/legal practice
    'Handwerk', 'Tradesman',            # Skilled trades
]

ka_business_types = [
    'Gruppe', 'Group', 'Holding',
    'International', 'Multinational',
    'AG', 'SE',  # Corporate structures
]

if any(smb_type in business_description for smb_type in smb_business_types):
    classification = "SMB"
    confidence = "LOW"  # Override if other signals contradict

if any(ka_type in business_description for ka_type in ka_business_types):
    classification = "KA"
    confidence = "LOW"  # Override if other signals contradict
```

---

## Classification Decision Matrix

Combine all signals:

| Primary Signal | Secondary Signal | Final Classification |
|----------------|------------------|---------------------|
| Employees <20 | Single location | **SMB** (HIGH) |
| Employees <20 | 2+ locations | **MID-MARKET** (MEDIUM) |
| Employees 20-500 | Single location | **MID-MARKET** (HIGH) |
| Employees 20-500 | 2+ locations | **KA** (MEDIUM) |
| Employees 500+ | Any | **KA** (HIGH) |
| Unknown | Family + single + no depts | **SMB** (MEDIUM) |
| Unknown | Multiple locations + depts | **KA** (MEDIUM) |

---

## Output Format

After classification, output:

```markdown
### Classification Result

| Criterion | Value | Signal |
|-----------|-------|--------|
| Employees | {count or "Unknown"} | {SMB/KA signal} |
| Locations | {count} | {SMB/KA signal} |
| Structure | {description} | {SMB/KA signal} |

**Classification:** {SMB | MID-MARKET | KA}
**Confidence:** {HIGH | MEDIUM | LOW}
**Score Cap:** {50 | 75 | 100}
```

---

## Score Caps by Classification

| Classification | Max Score | Max Grade | Typical Action |
|----------------|-----------|-----------|----------------|
| **SMB** | 50 | C | nurture / explore |
| **MID-MARKET** | 75 | B | standard |
| **KA** | 100 | A | prioritize |

**Note:** Score caps are applied AFTER bonus scoring but BEFORE grade mapping.

---

## Special Cases

### Hospitality Single-Property (Gasthof Pendl Pattern)

```
Pattern: Single hotel/restaurant, family-operated, <50 rooms

Classification: SMB (regardless of revenue)
Rationale: Single-property hospitality lacks:
  - Multi-site scaling opportunity
  - Dedicated procurement function
  - Department structure

Exception: Hotel CHAINS (3+ properties) → MID-MARKET or KA
```

### Service Providers (Cleaning Companies)

```
Pattern: Cleaning services (not equipment distribution)

Classification: Evaluate normally, but tag as `cleaning-services-provider`
Action Override: service-provider-prospect (not prioritize)
Rationale: End-user, not channel partner
```

### Competitor Distributors

```
Pattern: Already sells Pudu/Gausium/LionsBot

Classification: Evaluate normally
Action Override: route-to-sales (regardless of classification)
Play: competitive-conversion
Rationale: Immediate revenue opportunity
```

---

## Integration with Hard Gates

Classification and Hard Gates work independently but both affect final score:

```
┌──────────────────────────────────────────────────────────────┐
│  Classification: SMB                                         │
│  Hard Gates: MOST_FAIL (3+ fails)                            │
│  Result: Score cap 50 (SMB) + Base = 0 (gates) = 0          │
│  Action: exclude                                             │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  Classification: KA                                          │
│  Hard Gates: SOME_FAIL (1-2 fails)                           │
│  Result: Score cap 50 (gates) + bonuses = up to 50          │
│  Action: explore                                             │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  Classification: KA                                          │
│  Hard Gates: ALL_PASS                                        │
│  Result: Score cap 100 + bonuses = up to 100                │
│  Action: prioritize (if score >= 90)                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Examples

### Example 1: Gasthof Pendl (Hospitality, Single Property)

```
Extracted Profile:
  - Employees: Not stated (family business)
  - Locations: 1 (Kalsdorf only)
  - Structure: "Family-operated Gasthof"
  - Revenue: Not stated
  - Departments: None visible

Classification Logic:
  - Employee count unknown → Check secondary signals
  - Single location + "family-operated" + no departments
  - Hospitality single-property pattern match

Result:
  Classification: SMB
  Confidence: HIGH (multiple signals align)
  Score Cap: 50
```

### Example 2: FrigoSystem (German Equipment Distributor)

```
Extracted Profile:
  - Employees: "35 Mitarbeiter" (explicit)
  - Locations: 3 (Hamburg, Munich, Berlin)
  - Structure: Sales, Service, Administration pages
  - Revenue: "€8M Umsatz" mentioned
  - Departments: Vertrieb, Service, Logistik visible

Classification Logic:
  - Employee count = 35 → MID-MARKET baseline
  - 3 locations → reinforces MID-MARKET
  - Multiple departments → confirms sophistication

Result:
  Classification: MID-MARKET
  Confidence: HIGH (explicit data)
  Score Cap: 75
```

### Example 3: International Cleaning Group

```
Extracted Profile:
  - Employees: "600+ employees worldwide"
  - Locations: 12 offices across DACH region
  - Structure: Group structure with divisions
  - Revenue: "€75M annual revenue"
  - Departments: Multiple divisions, dedicated procurement

Classification Logic:
  - Employee count = 600+ → KA baseline
  - 12 locations → confirms KA
  - Group structure → confirms KA

Result:
  Classification: KA
  Confidence: HIGH (explicit data)
  Score Cap: 100
```

---

## Implementation Notes

1. **Always extract evidence** - Show what signals were found
2. **Confidence matters** - LOW confidence should trigger manual review flag
3. **Override hierarchy** - Classification cap applies AFTER gate caps (whichever is lower)
4. **Unknown is valid** - If no signals available, classify as "Unknown" with manual review flag

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `hard-gates.md` | Minimum capability thresholds |
| `scoring-matrix.md` | Bonus scoring rules |
| `gate-translation.md` | How to interpret gates |
