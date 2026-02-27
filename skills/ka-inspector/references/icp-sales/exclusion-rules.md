# Exclusion Rules - KA End Customer

> **Purpose:** Define companies that should NOT be pursued as KA prospects
> **Updated:** 2026-02-27

---

## Overview

Exclusion rules prevent wasted sales effort on companies that cannot purchase or deploy cleaning robots. These are **hard filters**.

---

## Exclusion 1: No Budget Ownership

### ICP Rationale
"无预算所有权且无采购路径" - Companies without budget authority cannot make purchasing decisions.

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| No procurement function | No purchasing department, no procurement page |
| No facilities budget | No facility management mentioned |
| No CapEx signals | No capital investment, equipment budget mentions |
| Sole proprietor | One-person operation, no organizational structure |

### Decision Logic

```
IF (no procurement) AND (no facilities budget) AND (no CapEx signals):
  → EXCLUDE
```

---

## Exclusion 2: No On-site Contact

### ICP Rationale
"无现场对接人，无法配合部署" - Companies without on-site contacts cannot coordinate robot deployment.

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| No team page | No "About", "Team", "Leadership" section |
| No facilities role | No facilities/operations/IT/engineering mentioned |
| Sole operator | Single person company |
| No contact info | Only generic contact form |

### Decision Logic

```
IF (no team page) AND (no facilities role) AND (no named contacts):
  → EXCLUDE
```

---

## Exclusion 3: Research Only

### ICP Rationale
"仅调研无落地时间表" - Companies only researching with no implementation timeline.

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| Research language | "Research", "study", "evaluating options" |
| No timeline | "Someday", "future consideration" |
| No project mentions | No active projects, no initiatives |

### Decision Logic

```
IF (research language) AND (no timeline) AND (no active projects):
  → EXCLUDE
```

---

## Exclusion Decision Tree

```
Does company have budget/procurement function?
├─ NO → Does it have facilities budget?
│   ├─ NO → EXCLUDE (no budget ownership)
│   └─ YES → Continue
└─ YES → Continue

Does company have on-site contact/facilities team?
├─ NO → EXCLUDE (no deployment contact)
└─ YES → Continue

Does company have implementation timeline?
├─ NO → Is it research-only?
│   ├─ YES → EXCLUDE (research only)
│   └─ NO → Continue (unknown timeline)
└─ YES → PASS all exclusions
```

---

## Exclusion vs. Low Score

| Situation | Action | Rationale |
|-----------|--------|-----------|
| No budget authority | EXCLUDE | Cannot purchase |
| No facilities team | EXCLUDE | Cannot deploy |
| Research only, no timeline | EXCLUDE | Won't convert soon |
| Single location | LOW SCORE (not exclude) | Less potential, but still viable |
| No digital systems | LOW SCORE (not exclude) | Manual processes, but can still use robot |
| Unknown KPI | LOW SCORE (not exclude) | KPI clarity is bonus, not requirement |
