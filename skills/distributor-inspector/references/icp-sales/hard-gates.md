# Hard Gates - Distributor Qualification

> **Status:** Required gates from Sales ICP
> **Enforcement:** ALL gates must pass for A/B grade eligibility
> **Updated:** 2026-02-27

---

## Overview

These criteria represent the **minimum viable distributor profile**. Companies that fail these gates lack the fundamental capability to sell, deploy, or support cleaning robots effectively.

**Gate Logic:**
- **ALL PASS** → Eligible for full scoring (A/B grade possible)
- **1-2 FAIL** → Cap max score at 50 (explore tier only)
- **3+ FAIL** → Route to `exclude` regardless of other signals

---

## Gate 1: Company Size & Financials

### ICP Requirement
- **Employees:** 20-500
- **Revenue:** ~€10M annual (€5M minimum soft threshold)
- **Investment:** Strong industry commitment (expansions, hires, capex)

### AI Detection Method

| Signal | How to Detect | Pass Threshold |
|--------|---------------|----------------|
| Employee count | About page, Impressum, LinkedIn, "unser Team" | 20 ≤ count ≤ 500 |
| Revenue mentions | "€10M", "X million", "Umsatz", turnover | ≥ €5M mentioned |
| Team photos | Group photos, org charts | Count visible team members |
| Multiple departments | Sales, service, admin sections | 3+ distinct functions |
| Growth signals | "New location", "expanding", recent hires | Any positive signal |

### Decision Rules

```
PASS: (20 ≤ employees ≤ 500) AND (revenue ≥ €5M OR strong investment signals)
SOFT_PASS: employees < 20 BUT revenue ≥ €10M (specialized high-value firm)
FAIL: employees < 20 AND revenue < €5M AND no investment signals
UNCLEAR: No employee/revenue data → Flag for manual review, proceed with -10 penalty
```

### Examples

**PASS:** "Unser 50-köpfiges Team" + "€12M Umsatz" → PASS
**SOFT_PASS:** "8 employees" + "€15M revenue, 3 locations" → SOFT_PASS (specialized)
**FAIL:** "5-person family team" + no revenue data → FAIL

---

## Gate 2: Team Capability (Sales + Deployment + After-sales)

### ICP Requirement
Must have THREE distinct functions:
1. **Sales/BD** - Lead follow-up, bidding, commercial negotiations
2. **Deployment/Delivery** - On-site implementation, training, acceptance
3. **After-sales/Repair** - Response, spare parts, maintenance

### AI Detection Method

| Function | Keywords (DE/EN/FR) | Detection Location |
|----------|---------------------|-------------------|
| Sales/BD | "Vertrieb", "sales", "BD", "commercial", "ventes" | Team page, contact structure |
| Deployment | "Installation", "deployment", "Inbetriebnahme", "montage" | Services page, project descriptions |
| After-sales | "Service", "repair", "maintenance", "SAV", "Kundendienst", "après-vente" | Dedicated service section |

### Decision Rules

```
PASS: All 3 functions detected with dedicated pages or named contacts
SOFT_PASS: 2 functions clear, 1 implied (e.g., service mentioned but no dedicated page)
FAIL: Only 1 or 0 functions detected, or all rolled into "general business"
```

### Examples

**PASS:** Separate "Vertrieb", "Projekt", and "Service" pages → PASS
**SOFT_PASS:** Sales team listed, service mentioned but no dedicated page → SOFT_PASS
**FAIL:** Only "contact us for everything" with no function separation → FAIL

---

## Gate 3: SLA Capability

### ICP Requirement
Can commit to quantifiable response times and processes:
- Remote support response time
- On-site arrival time
- Spare parts delivery time
- Ticket/communication mechanism

### AI Detection Method

| Signal | Keywords | Strength |
|--------|----------|----------|
| Time commitment | "24h", "48h", "within 2 days", "same-day" | Strong |
| SLA mention | "SLA", "service level", "response guarantee" | Strong |
| Support channels | "Hotline", "support line", "ticket system" | Medium |
| Spare parts | "spare parts", "Ersatzteile", "parts inventory" | Medium |
| Service territory | "nationwide", "DACH-wide", "within 100km" | Weak |

### Decision Rules

```
PASS: Time commitment (24-48h) + support channel + spare parts mention
SOFT_PASS: Time commitment OR (support channel + spare parts)
FAIL: No SLA signals, or only "we provide good service" without specifics
```

### Examples

**PASS:** "24h response, 48h on-site, spare parts warehouse" → PASS
**SOFT_PASS:** "Fast service, nationwide coverage" → SOFT_PASS (vague but positive)
**FAIL:** No service commitment language → FAIL

---

## Gate 4: Trial/PoC Capability

### ICP Requirement
Can support 1-week proof-of-concept with:
- Demo machine availability (own or demo-price purchase)
- On-site training capability
- Acceptance testing process

### AI Detection Method

| Signal | Keywords | Strength |
|--------|----------|----------|
| Demo/trial | "demo", "trial", "test", "PoC", "probe" | Strong |
| Showroom | "showroom", "demo center", "exhibition room" | Strong |
| Test policy | "test drive", "on-site test", "customer trial" | Strong |
| Training | "training", "Schulung", "customer education" | Medium |
| Acceptance | "acceptance", "Abnahme", "commissioning" | Medium |

### Decision Rules

```
PASS: Demo/trial policy OR showroom + training mentioned
SOFT_PASS: Demo mentioned but no clear policy
FAIL: No demo/trial/test language, or "contact for info" only
```

### Examples

**PASS:** "Demo center available", "1-week trial possible" → PASS
**SOFT_PASS:** "We offer product demonstrations" (no policy details) → SOFT_PASS
**FAIL:** No demo/test language → FAIL

---

## Gate 5: Market Coverage

### ICP Requirement
- Covers at least 1-3 cities in top 10 GDP cities / core economic zones
- Cross-city service capability

### AI Detection Method

| Signal | Detection Method |
|--------|------------------|
| HQ location | Address on imprint/contact page |
| Branch offices | "Locations", "branches", " Niederlassungen" |
| Service area | "Service area", "coverage", "Einsatzgebiet" |
| Customer locations | Project map, customer testimonials by region |
| Travel radius | "Within X km", "region-wide" |

### Decision Rules

```
PASS: HQ + 1+ branches OR stated coverage of multiple cities/regions
SOFT_PASS: Single location but "nationwide service" claim
FAIL: Single location with no coverage claims, hyper-local only
```

---

## Gate 6: Price Discipline

### ICP Requirement
- Willing to execute MSRP / MAP
- No price dumping as primary acquisition method
- Can enforce price discipline with downstream channels

### AI Detection Method

| Signal | Keywords | Strength |
|--------|----------|----------|
| MSRP/MAP | "MSRP", "MAP", "price policy", "UVP" | Strong |
| Authorized dealer | "Authorized dealer", "certified partner", "official" | Strong |
| Brand partnership | "Official partner of X", "authorized distributor" | Medium |
| Price consistency | No visible prices (B2B quote model) | Weak |
| Discount language | "Discount", "cheap", "lowest price" | Negative signal |

### Decision Rules

```
PASS: MSRP/MAP mention OR authorized dealer language with major brands
SOFT_PASS: B2B quote model (no public pricing) + brand partnerships
FAIL: Heavy discount language, "cheapest prices" claims
```

---

## Gate Summary Table

| Gate | Pass | Soft Pass | Fail |
|------|------|-----------|------|
| Company Size | 20-500 emp + €5M+ rev | <20 emp but €10M+ rev | <20 emp + <€5M rev |
| Team Capability | 3 functions clear | 2 functions clear | 0-1 functions |
| SLA Capability | Time + channel + parts | Time OR channel+parts | No specific signals |
| Trial Capability | Demo policy + training | Demo mentioned | No demo language |
| Market Coverage | Multi-city/branch | Nationwide claim | Single location only |
| Price Discipline | MSRP/authorized dealer | B2B quote model | Discount focus |

---

## Implementation Notes for AI Skill

1. **Extract evidence** for each gate, don't just pass/fail
2. **Show your work** in the report - list what was found
3. **UNCLEAR is valid** - if information is missing, flag it
4. **German-specific:** Look for "Impressum" which often has employee count and revenue hints
5. **French-specific:** "SIRET" and "chiffre d'affaires" for company data
6. **Soft pass counting:** 2 soft passes = 1 fail for gate counting purposes
