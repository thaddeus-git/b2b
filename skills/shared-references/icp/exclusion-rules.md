# Exclusion Rules - Distributor Qualification

> **Purpose:** Define companies that should NOT be pursued as distributors
> **Updated:** 2026-02-27

---

## Overview

Exclusion rules prevent wasted sales effort on companies that cannot succeed as distributors. These are **hard filters** - if a company matches an exclusion criterion, it should be routed to `exclude` regardless of other positive signals.

---

## Exclusion 1: Renovation/Decoration Companies

### ICP Rationale
"装修类公司：核心是装修服务，与机器人业务相关性弱，转化差"

Core business is construction/renovation - weak relevance to robotics, poor conversion rates.

### Detection Keywords

**German:**
- "Renovierung", "Sanierung", "Bau"
- "Innenarchitektur", "Raumgestaltung"
- "Malerbetrieb", "Fliesenleger"
- "Fertigbau", "Trockenbau"

**English:**
- "Renovation", "remodeling"
- "Construction", "building"
- "Interior design" (if no facility management)
- "Painting", "flooring" (installation only)

**French:**
- "Rénovation", "rénovation bâtiment"
- "Travaux", "chantier"
- "Architecture d'intérieur"
- "Peinture", "carrelage"

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| Service focus | "We renovate", "we build", "we design" |
| Project type | Residential/commercial construction |
| No equipment sales | Only materials + labor, no product catalog |
| Trade focus | Construction trades (painter, carpenter, etc.) |

### Exception (Do NOT Exclude)

If company ALSO sells cleaning equipment or facility management equipment → Score normally

**Example:** A renovation company that also sells commercial cleaning machines to their clients → NOT excluded

---

## Exclusion 2: Pure B2C Retail (No ToB Channels)

### ICP Rationale
"纯 2C 零售导向：无 ToB 渠道与 B2B 交付能力的代理商"

Companies that only sell to consumers lack the B2B relationships and sales processes needed for robot distribution.

### Detection Keywords (B2C-only signals)

| Signal | Detection Method |
|--------|------------------|
| Shopping cart | "Add to cart", "checkout", online store for consumers |
| Consumer pricing | Single-unit pricing, no volume/tier pricing |
| No B2B section | No "Become a dealer", "Wholesale", or "Trade" pages |
| Product focus | Home robot vacuums ONLY (iRobot, Roborock consumer line) |
| No business info | No company registration, tax ID, or trade account options |
| Marketing language | "For your home", "family", "household" |

### Detection Keywords (B2B signals - if ANY present, NOT excluded)

| Signal | Detection Method |
|--------|------------------|
| B2B page | "Business customers", "B2B", "Wholesale" |
| Commercial products | Commercial scrubbers, sweepers, industrial vacuums |
| Volume pricing | Tier pricing, bulk discounts, quote requests |
| Trade accounts | Business registration, tax ID required |
| Facility management | Products for property management, janitorial |

### Decision Logic

```
IF (pure-2c-retail tag) AND (NO commercial product signals):
  → EXCLUDE
IF (pure-2c-retail tag) BUT (HAS commercial product signals):
  → Score normally (valid prospect with mixed business)
```

### Examples

**EXCLUDE:**
- Online shop selling only iRobot/Roborock/Xiaomi home vacuums
- Consumer electronics store with no B2B division
- "Robot vacuum shop" with only home models

**NOT EXCLUDE (Score Normally):**
- Home vacuum shop that ALSO sells commercial floor scrubbers
- Retail store with "Business customers" section and bulk pricing
- "Professional cleaning equipment" + consumer products

---

## Exclusion 3: Too Small / No Team

### ICP Rationale
"规模过小或无团队：人员规模 <20 且无交付/售后团队的'皮包公司'"

Companies with < 20 employees and no delivery/after-sales teams cannot support robot distribution.

### Detection Keywords

| Signal | Detection Method |
|--------|------------------|
| Solo/family business | "Owner-operated", "family business", "einzelunternehmen" |
| No team page | No "Our team", "Team", "Über uns" section |
| < 5 employees | Team page shows 1-4 people |
| No department structure | All-in-one "we do everything" |
| Virtual business | "Virtual office", no physical address |

### Decision Logic

```
IF (employees < 20) AND (no sales team) AND (no service team):
  → EXCLUDE
IF (employees < 20) BUT (has specialized capability, high revenue):
  → SOFT_PASS, flag for manual review
```

### Examples

**EXCLUDE:**
- "3-person family team" with no service department
- Solo consultant with "network of partners"
- Virtual business with no physical location

**NOT EXCLUDE:**
- 15-person company with dedicated sales + service teams
- 10-person company with €10M+ revenue (specialized, high-value)

---

## Exclusion 4: No Key Decision-Makers Identified

### ICP Rationale
"无明确关键决策人触达路径的公司"

Cannot identify sales or technical leadership - no clear path to decision-makers.

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| No named contacts | Only "info@company.com" with no names |
| No leadership page | No "Management", "Leadership", "Geschäftsführung" |
| Generic contact only | Only contact form, no direct contact info |
| No sales contact | No sales team or sales contact information |

### Decision Logic

```
IF (no named contacts) AND (no leadership page) AND (no sales contact):
  → EXCLUDE
IF (some contacts but limited):
  → Flag for manual research (LinkedIn, etc.)
```

---

## Exclusion 5: Free Sample Seekers

### ICP Rationale
"只要免费样机：不愿为演示/试用投入...往往缺乏真实投入与执行力"

Companies unwilling to invest in demos/trials lack real commitment.

### Detection Signals

| Signal | Detection Method |
|--------|------------------|
| "Free sample" language | "Free demo", "free trial" demands |
| No demo policy | No mention of demo purchase or trial program |
| Price-focused | Heavy emphasis on "free", "no cost" |

### Note
This is typically detected during **sales qualification calls**, not website analysis. Flag companies that explicitly demand free equipment.

---

## Exclusion Decision Tree

```
Is company a renovation/decoration business?
├─ YES → Does it ALSO sell cleaning equipment?
│   ├─ YES → NOT excluded, score normally
│   └─ NO → EXCLUDE
└─ NO → Continue

Is company pure B2C retail?
├─ YES → Does it have commercial products or B2B division?
│   ├─ YES → NOT excluded, score normally
│   └─ NO → EXCLUDE
└─ NO → Continue

Does company have < 20 employees AND no team structure?
├─ YES → EXCLUDE
└─ NO → Continue

Are there no key decision-makers identifiable?
├─ YES → EXCLUDE (or flag for manual research)
└─ NO → Continue

Is company a free sample seeker? (detected in conversation)
├─ YES → EXCLUDE
└─ NO → PASS all exclusions, proceed to scoring
```

---

## Exclusion vs. Low Score

| Situation | Action | Rationale |
|-----------|--------|-----------|
| Pure B2C, no commercial products | EXCLUDE | Wrong business model |
| Renovation company, no equipment | EXCLUDE | Wrong industry |
| < 20 employees, no team | EXCLUDE | Cannot deliver/support |
| Low customer overlap | LOW SCORE (not exclude) | Weak fit, but not disqualified |
| No competitor footprint | LOW SCORE (not exclude) | Missing bonus, not a disqualifier |
| Single location, no branches | LOW SCORE (not exclude) | Limited coverage, but may still work |

---

## Routing for Excluded Companies

| Exclusion Reason | Route To | Notes |
|------------------|----------|-------|
| Pure B2C retail | `exclude` | May revisit if they add B2B division |
| Renovation/decoration | `exclude` | Wrong industry entirely |
| Too small / no team | `exclude` | Cannot support distribution |
| No decision-makers | `exclude` | May revisit after research |
| Free sample seeker | `exclude` | Cultural fit issue |

**Note:** Excluded companies should be clearly marked in reports so sales team understands why.
