# Gate Translation: Sales ICP → Skill Implementation

> **Purpose:** Translate sales team requirements into AI-detectable signals
> **Updated:** 2026-02-27

---

## Overview

This document bridges the gap between **sales team requirements** (written for humans) and **AI skill implementation** (what the AI can actually detect from website snapshots).

---

## Gate Translation Table

| Sales ICP Criterion | Skill Interpretation | Detection Method | Evidence Required |
|---------------------|---------------------|------------------|-------------------|
| 20-500 employees | Team size extractable from website | About/Impressum page, team photos, LinkedIn | Named team members, explicit count, or revenue hints |
| €10M revenue | Revenue signals or scale indicators | "Million", revenue mentions, multiple locations | At least 2 scale signals |
| Sales/BD team | Dedicated sales function | Team page with sales contacts, "Vertrieb" section | Named sales contacts OR sales department |
| Deployment team | Installation/delivery offering | Services page with "installation", "deployment" | Service description with implementation |
| After-sales team | Service/repair capability | "Service", "repair", "SAV", "Kundendienst" section | Dedicated service page or section |
| SLA capability | Response time commitments | "24h", "48h", "SLA", "response time" | Specific time commitment |
| PoC capability | Demo/trial availability | "Demo", "trial", "showroom", "test" | Demo policy or showroom mention |
| Market coverage | Multi-city service area | Multiple locations, service area mentions | 2+ cities or regions |
| Price discipline | Authorized dealer status | "Authorized", "MSRP", brand partnerships | Brand partnership language |

---

## Detailed Detection Rules

### Gate 1: Company Size (20-500 employees)

**What Sales Means:**
"Companies with enough people to have specialized teams but not so large they're bureaucratic."

**What AI Detects:**

| Signal | Extraction Pattern | Confidence |
|--------|-------------------|------------|
| Explicit count | "X Mitarbeiter", "team of X", "X-person" | High |
| Team photo count | Count faces in team section | Medium |
| Department count | 3+ departments (sales, service, admin) | Medium |
| Location count | 2+ branches = likely 20+ employees | Low |
| Revenue hints | "€X million", "X-figure revenue" | Low |

**Decision Logic:**

```python
if explicit_count:
    if 20 <= count <= 500:
        return PASS
    elif count < 20:
        return FAIL  # Too small
    else:
        return PASS  # Large but acceptable
elif team_photo_count:
    if 10 <= count <= 400:  # Photos usually show subset
        return SOFT_PASS
    elif count < 10:
        return FAIL
elif department_count >= 3:
    return SOFT_PASS  # Likely 20+ employees
else:
    return UNCLEAR  # Flag for manual review
```

---

### Gate 2: Team Capability (Sales + Deployment + After-sales)

**What Sales Means:**
"They need people dedicated to selling, installing, and servicing - not just a general 'we do everything' team."

**What AI Detects:**

| Function | Keywords (DE) | Keywords (EN) | Keywords (FR) |
|----------|--------------|---------------|---------------|
| Sales | Vertrieb, Verkauf, Außenhandel | Sales, BD, Commercial | Ventes, Commercial |
| Deployment | Installation, Inbetriebnahme, Projekt | Deployment, Implementation | Installation, Déploiement |
| After-sales | Service, Kundendienst, Reparatur | Service, Repair, Maintenance | SAV, Service, Maintenance |

**Decision Logic:**

```python
functions_detected = {
    'sales': any(keyword in page for keyword in sales_keywords),
    'deployment': any(keyword in page for keyword in deployment_keywords),
    'after_sales': any(keyword in page for keyword in after_sales_keywords)
}

count = sum(functions_detected.values())

if count == 3:
    return PASS
elif count == 2:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 3: SLA Capability

**What Sales Means:**
"They can commit to specific response times, not just 'we provide good service'."

**What AI Detects:**

| Signal | Pattern | Strength |
|--------|---------|----------|
| Time commitment | "\d+h", "24 Stunden", "48 hours", "sous 48h" | Strong |
| SLA mention | "SLA", "Service Level", "Garantie" | Strong |
| Support channel | "Hotline", "Support-Line", "helpdesk" | Medium |
| Spare parts | "Ersatzteile", "spare parts", "pièces détachées" | Medium |
| Territory | "nationwide", "DACH-wide", "countrywide" | Weak |

**Decision Logic:**

```python
score = 0
if time_commitment_detected:
    score += 2
if sla_mention:
    score += 2
if support_channel:
    score += 1
if spare_parts:
    score += 1

if score >= 4:
    return PASS
elif score >= 2:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 4: PoC/Trial Capability

**What Sales Means:**
"They can handle a 1-week proof-of-concept with customer training."

**What AI Detects:**

| Signal | Pattern | Strength |
|--------|---------|----------|
| Demo policy | "Demo", "test unit", "probe" | Strong |
| Showroom | "Showroom", "demo center", "exhibition" | Strong |
| Training | "Training", "Schulung", "formation" | Medium |
| Acceptance | "Acceptance", "Abnahme", "commissioning" | Medium |

**Decision Logic:**

```python
if (demo_policy OR showroom) AND training:
    return PASS
elif demo_policy OR showroom:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 5: Market Coverage

**What Sales Means:**
"They cover enough geography to scale - not just one city."

**What AI Detects:**

| Signal | Pattern | Strength |
|--------|---------|----------|
| Multiple HQ/branches | "Locations", "branches", " Niederlassungen" | Strong |
| Service area | "Service area", "coverage", "Einsatzgebiet" | Medium |
| Customer locations | Testimonials from multiple cities | Medium |
| Cross-city | "DACH-wide", "nationwide", "across" | Weak |

**Decision Logic:**

```python
if branch_count >= 2:
    return PASS
elif service_area_mentions >= 2:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 6: Price Discipline

**What Sales Means:**
"They won't undercut prices and destroy market value."

**What AI Detects:**

| Signal | Pattern | Strength |
|--------|---------|----------|
| MSRP/MAP | "MSRP", "MAP", "UVP", "price policy" | Strong |
| Authorized dealer | "Authorized dealer", "official partner" | Strong |
| Brand partnership | "Distributor of X", "partner of Y" | Medium |
| B2B quote model | No public prices, "request quote" | Weak |
| Discount language | "Discount", "cheap", "lowest price" | Negative |

**Decision Logic:**

```python
if discount_language_detected:
    return FAIL  # Red flag
if msrp_mention OR authorized_dealer:
    return PASS
elif brand_partnership AND b2b_quote_model:
    return SOFT_PASS
else:
    return UNCLEAR  # Default to neutral
```

---

## Gate Summary: Pass/Fail Thresholds

| Gate | PASS | SOFT_PASS | FAIL | UNCLEAR |
|------|------|-----------|------|---------|
| Company Size | 20-500 emp | <20 but €10M+ rev | <20 emp, <€5M rev | No data |
| Team Capability | 3 functions | 2 functions | 0-1 functions | No data |
| SLA Capability | Time+channel+parts | Time OR channel+parts | No signals | No data |
| PoC Capability | Demo+training | Demo only | No demo | No data |
| Market Coverage | 2+ branches | Nationwide claim | Single location | No data |
| Price Discipline | MSRP/authorized | B2B quote+brands | Discount focus | No data |

---

## Gate Logic for Scoring

```python
def calculate_gate_result(gates):
    """
    gates: dict of gate_name -> result (PASS/SOFT_PASS/FAIL/UNCLEAR)
    """
    pass_count = sum(1 for v in gates.values() if v == 'PASS')
    soft_pass_count = sum(1 for v in gates.values() if v == 'SOFT_PASS')
    fail_count = sum(1 for v in gates.values() if v == 'FAIL')

    # Convert soft passes to half-pass
    effective_pass = pass_count + (soft_pass_count * 0.5)

    if fail_count == 0:
        return 'ALL_PASS'  # Eligible for A/B grade
    elif fail_count <= 2:
        return 'SOME_FAIL'  # Cap at 50 points (explore tier)
    else:
        return 'MOST_FAIL'  # Route to exclude
```

---

## Implementation Notes

1. **Always show evidence** - Don't just pass/fail, list what was found
2. **UNCLEAR is valid** - If info is missing, flag it rather than guessing
3. **Language detection** - Use detected language to select keyword set
4. **German-specific** - Impressum often has employee count hints
5. **French-specific** - Look for SIRET, "chiffre d'affaires"
6. **Soft pass handling** - 2 soft passes = 1 fail for counting purposes
