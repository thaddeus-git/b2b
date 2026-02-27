# Gate Translation: KA ICP → Skill Implementation

> **Purpose:** Translate sales team requirements into AI-detectable signals
> **Updated:** 2026-02-27

---

## Overview

This document bridges the gap between **sales team requirements** (KA ICP) and **AI skill implementation** (what the AI can detect from website snapshots).

---

## Gate Translation Table

| KA ICP Criterion | Skill Interpretation | Detection Method | Evidence Required |
|------------------|---------------------|------------------|-------------------|
| Budget/Procurement | Has procurement/facilities function | Careers, procurement page, organizational structure | Procurement mentioned OR facilities role |
| On-site Contact | Has facilities/operations team | Team page, leadership, department mentions | Named contact OR department page |
| Pilot Timeline | Can deploy quickly | Project mentions, deployment language | No long renovation signals |

---

## Detailed Detection Rules

### Gate 1: Budget/Procurement

**What Sales Means:**
"They have budget authority and a purchasing process for equipment."

**What AI Detects:**

| Signal | Extraction Pattern | Confidence |
|--------|-------------------|------------|
| Procurement page | "Procurement", "purchasing", "Einkauf" | High |
| Facilities budget | "Facility management", "FM budget" | High |
| Hiring for roles | Careers: procurement manager, facilities manager | Medium |
| CapEx language | "Capital investment", "equipment budget" | Medium |
| Investor relations | Public company with budget disclosures | Low |

**Decision Logic:**

```python
if procurement_page OR facilities_budget:
    return PASS
elif hiring_procurement OR hiring_facilities:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 2: On-site Contact

**What Sales Means:**
"There's someone on-site who can coordinate the robot deployment."

**What AI Detects:**

| Signal | Keywords | Detection Location |
|--------|----------|-------------------|
| Facilities team | "Facilities", "property management", "Haustechnik" | Team/About page |
| Operations team | "Operations", "Betrieb", "logistics" | Team/About page |
| IT/Engineering | "IT", "engineering", "technische" | Team/Careers page |
| Leadership | Named executives with roles | Leadership page |

**Decision Logic:**

```python
if named_facilities_contact OR dedicated_facilities_page:
    return PASS
elif operations_mentioned OR team_page_exists:
    return SOFT_PASS
else:
    return FAIL
```

---

### Gate 3: Pilot Timeline

**What Sales Means:**
"They can deploy quickly without major construction."

**What AI Detects:**

| Signal | Pattern | Strength |
|--------|---------|----------|
| Quick deployment | "Fast deployment", "quick rollout", "plug-and-play" | Strong |
| Pilot mentions | "Pilot", "trial", "test", "PoC" | Strong |
| Project mentions | "Project", "implementation", "rollout" | Medium |
| Renovation signals | "Construction", "renovation", "remodeling" | Negative |

**Decision Logic:**

```python
if quick_deployment_language OR pilot_program:
    return PASS
elif no_timeline_signals:
    return SOFT_PASS  # Neutral, need to verify
elif long_renovation_mentioned:
    return FAIL
else:
    return SOFT_PASS
```

---

## Gate Summary: Pass/Fail Thresholds

| Gate | PASS | SOFT_PASS | FAIL |
|------|------|-----------|------|
| Budget/Procurement | Procurement page/facilities budget | Hiring for roles | No signals |
| On-site Contact | Named contact/team page | General mention | No team info |
| Pilot Timeline | Quick deployment/pilot | Neutral | Long renovation |

---

## Gate Logic for Scoring

```python
def calculate_gate_result(gates):
    """
    gates: dict of gate_name -> result (PASS/SOFT_PASS/FAIL)
    """
    pass_count = sum(1 for v in gates.values() if v == 'PASS')
    soft_pass_count = sum(1 for v in gates.values() if v == 'SOFT_PASS')
    fail_count = sum(1 for v in gates.values() if v == 'FAIL')

    if fail_count == 0:
        return 'ALL_PASS'  # Eligible for pilot-ready
    elif fail_count == 1:
        return 'SOME_FAIL'  # Nurture tier
    else:
        return 'MOST_FAIL'  # Exclude
```

---

## Implementation Notes

1. **Extract evidence** - Don't just pass/fail, list what was found
2. **UNCLEAR is valid** - If info is missing, flag it
3. **KA-specific:** Focus on END USER signals, not distribution capability
