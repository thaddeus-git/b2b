# Scoring Matrix - Channel Partner Inspector

> **Purpose:** Define scoring criteria for channel partner evaluation
> **Related:** `hard-gates.md`, `../_shared/target-segments.md`

---

## Scoring Overview

| Phase | Points | Description |
|-------|--------|-------------|
| Base | 60 | Awarded if client overlap gate passes |
| Bonuses | 0-80 | Additional points for partner quality signals |
| Cap | 100 | Maximum total score |

---

## Base Score

**60 points** - Awarded automatically if client overlap gate passes.

This reflects that any company with clients in target segments has baseline value as a potential channel partner.

---

## Bonus Scoring

### Client Quantity (+20 max)

| Client Count | Points | Rationale |
|--------------|--------|-----------|
| 1-10 | +5 | Limited reach |
| 11-50 | +10 | Moderate network |
| 51-200 | +15 | Strong network |
| 200+ | +20 | Extensive network |

**Detection:**
- Count named clients from case studies, logos, testimonials
- Use lower bound if exact count unclear

### Client Quality / KA Presence (+15 max)

| Quality Level | Points | Criteria |
|---------------|--------|----------|
| No KA clients | +0 | Only SMB/mid-market clients |
| Some KA clients | +10 | 1-3 recognizable enterprise brands |
| Strong KA presence | +15 | 4+ recognizable enterprise brands |

**KA Detection:**
- Healthcare: Major health systems (Kaiser, HCA, etc.)
- Retail: National chains (Walmart, Target, CVS, etc.)
- Hospitality: Major brands (Marriott, Hilton, etc.)
- Property/FM: Large PM companies (JLL, CBRE, etc.)

### Sales Capability (+10 max)

| Level | Points | Evidence |
|-------|--------|----------|
| None detected | +0 | No sales team mentioned |
| Basic | +5 | "Contact sales", sales email |
| Established | +10 | Named sales team, BD team, account managers, sales leadership |

**Detection:**
- Team page with sales roles
- "Sales team", "Business development", "Account manager"
- Sales leadership (VP Sales, Chief Revenue Officer)

### Trust / Relationship Depth (+10 max)

| Level | Points | Evidence |
|-------|--------|----------|
| Transactional | +0 | Product-focused, no relationship signals |
| Moderate | +5 | Some testimonials, client mentions |
| Deep | +10 | Long-term clients, "partnership" language, case studies with depth |

**Detection:**
- "Partnership", "trusted advisor", "strategic relationship"
- Multi-year client relationships mentioned
- Detailed case studies showing deep engagement

### Geographic Reach (+10 max)

| Level | Points | Client Distribution |
|-------|--------|---------------------|
| Local | +0 | Single city/region |
| Regional | +5 | Multi-state or multi-region |
| National/International | +10 | Multiple countries or nationwide |

**Detection:**
- Client locations mentioned
- "Serving clients across [X regions]"
- Office locations as proxy for client reach

### Industry Expertise (+5 max)

| Level | Points | Focus |
|-------|--------|-------|
| General | +0 | Serves multiple industries |
| Specialized | +5 | Focused on ONE target segment |

**Detection:**
- "Healthcare IT", "Retail technology", "PropTech"
- Product/service specifically for one industry

### Partnership History (+5 max)

| Level | Points | Evidence |
|-------|--------|----------|
| None detected | +0 | No partnership mentions |
| Has partnerships | +5 | Integrations, co-marketing, referral programs, channel partners |

**Detection:**
- "Partners" page
- Integration marketplace
- "Referral program", "Channel partner program"
- Co-marketing case studies

### Financial Stability (+5 max)

| Level | Points | Evidence |
|-------|--------|----------|
| Unclear | +0 | No signals |
| Stable | +5 | PE backed, profitable, 5+ years, established brand |

**Detection:**
- "Founded in [year]" (5+ years ago)
- "Backed by [PE firm]"
- "Profitable" mentions
- Established brand recognition

---

## Scoring Example: Valer.health

| Component | Evidence | Points |
|-----------|----------|--------|
| Base | Client overlap gate passed | 60 |
| Client Quantity | 8+ named healthcare clients | +10 |
| Client Quality | OHSU, Keck Medicine (KA) | +10 |
| Sales Capability | CGO mentioned, sales team | +10 |
| Trust/Relationship | "Partnership" language, testimonials | +10 |
| Geographic Reach | Multi-state (US) | +5 |
| Industry Expertise | Healthcare-focused | +5 |
| Partnership History | AccuReg/Optum partnership | +5 |
| Financial Stability | PE backed (Hughes & Co.) | +5 |
| **Total** | | **120 → 100** |

**Final Score: 100/100 (A)**
**Action: prioritize**

---

## Score to Grade Mapping

| Score | Grade | Action |
|-------|-------|--------|
| 80-100 | A | `prioritize` |
| 60-79 | B | `standard` |
| 40-59 | C | `explore` |
| <40 | D/F | `exclude` |
