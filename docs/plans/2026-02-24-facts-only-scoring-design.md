# Design: Facts-Only Distributor Inspector

**Date:** 2026-02-24
**Status:** Approved
**Target:** `skills/distributor-inspector/SKILL.md`

## Problem Statement

1. **Inference in outputs** — Current outputs include inferred claims ("trained teams", "after-sales established", "customer base") that aren't explicitly supported by website evidence.

2. **Scoring inconsistency** — Channel Capability scoring uses undefined signals (partner portal, warehouse/logistics) that aren't in the rubric.

## Design Decision

**STRICT mode (facts-only):**
- Do not infer capabilities
- Only award points for explicitly defined signals
- Indirect hints become Observations, not scoring evidence

## Changes

### 1. Evidence Policy (New Section)

**Location:** After Overview, before Process

```md
## Evidence Policy (Facts-Only)

**Hard rule:** Only include claims and scoring evidence that are explicitly supported by website content.

- If a capability is not explicitly stated, mark it as **Unknown** — do not infer.
- Do not write implied statements like "trained teams", "after-sales established", "customer base" unless the site explicitly states it.
- Indirect hints go in **Observations**, not capability claims or scoring.
```

### 2. Output Format Changes

**Add after Tags line:**
```md
**Confidence:** {high|medium|low}
```

**Replace `### Key Signals` with:**
```md
### Verified Evidence (quotes/snippets)
- {verbatim or close paraphrase + page context}

### Observations (non-interpretive)
- {objective observation without capability inference}
```

### 3. Competitor Footprint Language Fix

**Replace (lines 148-154):**
```md
**Why this is a bonus, not a blocker:** Competitor distributors already have:
- Customer base in cleaning robotics
- Sales and deployment teams trained on robots
- After-sales service capability
- Market knowledge and relationships
```

**With:**
```md
**Why this is a bonus, not a blocker:** Competitor distributors are often high-value because they:
- Are already selling comparable products in the category (explicit competitor evidence)
- May already have channel motion for robots (distribution language, partner programs, pricing pages)
- Are typically open to multi-brand portfolios (if the site explicitly mentions multiple brands)

> Note: These are general patterns — do not claim capabilities about a specific company unless explicitly stated.
```

### 4. Channel Capability Bonus (Facts-Only)

**Replace current section with:**
```md
## Channel Capability Bonus (Facts-Only)

Award points **only** when the website explicitly shows these signals:

| Signal Type | Examples of Explicit Evidence |
|------------|-------------------------------|
| After-sales support | "Service", "Repair", "Spare parts", "Wartung", "Support center", "ticket system" |
| Demo / trial | "Demo", "Vorführung", "Teststellung", "Pilot", "free trial" |
| Multiple brands | Brand pages, logos, "We distribute X, Y, Z" |
| Multiple categories | Separate product categories (e.g., cleaning robots + reception robots + industrial robots) |
| SLA / response times | "SLA", "response within 24h", "Supportzeiten", "Service Level" |

**Scoring:**
- +5 = 1 explicit signal
- +10 = 2 explicit signals
- +20 = 3+ explicit signals **OR** explicit service/repair/training infrastructure page

**Not scored (record as Observation only):**
- Partner portal, warehouse/logistics, quiz — useful signals but not counted for points
```

### 5. Sales Play & Routing Precedence

**Add to Sales Play section:**
```md
### Sales Play (facts-only)
- Cite only explicitly verified evidence.
- Do not include assumptions like "trained teams" or "after-sales capability" unless the site explicitly states training/service/repair.
```

**Add to Route section:**
```md
**Routing precedence:** Competitor footprint Tier 1–2 overrides score-based action.
```

## Acceptance Criteria

- [ ] SKILL.md includes Evidence Policy section
- [ ] Output format has Confidence field
- [ ] Output format has Verified Evidence + Observations sections
- [ ] Competitor footprint language is facts-safe
- [ ] Channel Capability scoring table is explicit
- [ ] Sales Play section includes facts-only reminder
- [ ] Routing precedence is documented
