# Hard Gates - KA End Customer Qualification

> **Status:** Required gates from KA ICP
> **Enforcement:** ALL gates must pass for pilot-ready status
> **Updated:** 2026-02-27

---

## Overview

These criteria represent the **minimum viable KA prospect**. Companies that fail these gates lack the fundamental capability to purchase and deploy cleaning robots.

**Gate Logic:**
- **ALL PASS** → Eligible for pilot-ready (A/B grade)
- **1 FAIL** → Route to nurture (C grade max)
- **2+ FAIL** → Route to exclude

---

## Gate 1: Budget/Procurement Capability

### ICP Requirement
- Has equipment procurement function
- Has facility management budget
- Clear purchasing process

### AI Detection Method

| Signal | How to Detect | Strength |
|--------|---------------|----------|
| Procurement page | "Procurement", "purchasing", "Einkauf" | Strong |
| Facilities budget | "Facility management", "FM budget" | Strong |
| CapEx mentions | "Capital investment", "equipment budget" | Medium |
| Hiring for roles | Careers: procurement, facilities manager | Medium |
| Investor relations | Public company with budget disclosures | Weak |

### Decision Rules

```
PASS: Procurement page OR facilities budget mentioned
SOFT_PASS: Hiring for procurement/facilities roles
FAIL: No budget/procurement signals detected
```

---

## Gate 2: On-site Contact Capability

### ICP Requirement
- Has on-site contact person
- Facilities/operations/IT/engineering team
- Can coordinate deployment

### AI Detection Method

| Signal | Keywords | Detection Location |
|--------|----------|-------------------|
| Facilities team | "Facilities", "property management", "Haustechnik" | Team page, About |
| Operations team | "Operations", "Betrieb", "logistics" | Team page, Services |
| IT/Engineering | "IT", "engineering", "technische" | Team page, Careers |
| Leadership | Named executives with roles | Leadership/About page |

### Decision Rules

```
PASS: Named facilities/operations contact OR dedicated team page
SOFT_PASS: General operations mentioned but no named contact
FAIL: No team/contact information, solopreneur
```

---

## Gate 3: Pilot Timeline Capability

### ICP Requirement
- Single-site can launch quickly
- No long renovation cycle needed
- Implementation timeline is reasonable (days, not months)

### AI Detection Method

| Signal | Keywords | Strength |
|--------|----------|----------|
| Quick deployment | "Fast deployment", "quick rollout" | Strong |
| Pilot mentions | "Pilot", "trial", "test", "PoC" | Strong |
| Project timeline | "X weeks", "X months" for projects | Medium |
| Renovation signals | "Construction", "renovation", "remodeling" | Negative |

### Decision Rules

```
PASS: Quick deployment language OR pilot program mentioned
SOFT_PASS: No timeline signals (neutral)
FAIL: Long renovation cycle mentioned (6+ months)
```

---

## Gate Summary Table

| Gate | Pass | Soft Pass | Fail |
|------|------|-----------|------|
| Budget/Procurement | Procurement page/facilities budget | Hiring for roles | No signals |
| On-site Contact | Named contact/team page | General mention | No team info |
| Pilot Timeline | Quick deployment/pilot mentioned | Neutral | Long renovation |

---

## Implementation Notes for AI Skill

1. **Extract evidence** for each gate, don't just pass/fail
2. **Show your work** in the report - list what was found
3. **UNCLEAR is valid** - if information is missing, flag it
4. **KA-specific:** Focus on END USER signals, not distribution capability
