# Channel Partner Inspector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a new `channel-partner-inspector` skill to evaluate companies with client relationships in target segments, plus restructure shared resources to eliminate duplication.

**Architecture:** New skill follows same pattern as distributor-inspector (Playwright CLI → snapshot → extract → score → route). Introduces `_shared/` directory for common resources. Cross-routing between all three inspector skills.

**Tech Stack:** Playwright CLI, Markdown skill files, Python scripts (Bright Data SERP)

---

## Phase 1: Create Shared Resources Directory

### Task 1.1: Create _shared directory structure

**Files:**
- Create: `skills/_shared/` directory

**Step 1: Create directory**

```bash
mkdir -p /Users/thaddeus/skills/b2b/skills/_shared
```

**Step 2: Verify directory exists**

Run: `ls -la /Users/thaddeus/skills/b2b/skills/_shared`
Expected: Directory listing (empty)

**Step 3: Commit**

```bash
git add skills/_shared/.gitkeep 2>/dev/null || true
git commit --allow-empty -m "feat: create _shared directory for shared skill resources"
```

---

### Task 1.2: Create target-segments.md

**Files:**
- Create: `skills/_shared/target-segments.md`

**Step 1: Write target-segments.md**

```markdown
# Target Segments for Cleaning Robot End-Users

> **Purpose:** Define target customer segments for OrionStar cleaning robots
> **Used by:** distributor-inspector, ka-inspector, channel-partner-inspector

---

## High-Priority Segments

### Healthcare

**Sub-segments:**
- Hospitals (general, academic, regional)
- Medical centers / clinics
- Outpatient facilities
- Urgent care centers
- Long-term care / nursing homes

**Cleaning robot potential:** HIGH
- Large floor areas
- 24/7 operations
- Hygiene requirements
- Labor cost pressure

**Detection keywords:**
- Hospital, medical center, clinic, healthcare system
- Patient rooms, operating rooms, common areas

---

### Retail

**Sub-segments:**
- Supermarkets / grocery stores
- Drug stores / pharmacies
- Department stores
- Shopping malls
- Convenience store chains

**Cleaning robot potential:** HIGH
- Many locations (scale)
- Consistent floor layouts
- Public-facing (cleanliness matters)
- Night cleaning windows

**Detection keywords:**
- Store, retail, supermarket, pharmacy, chain, locations

---

### Hospitality

**Sub-segments:**
- Hotels / resorts
- Casinos
- Convention centers
- Event venues

**Cleaning robot potential:** HIGH
- Guest areas (lobbies, hallways)
- Public spaces
- 24/7 operations
- Brand/image requirements

**Detection keywords:**
- Hotel, resort, casino, hospitality, guest, rooms

---

### Property / Facility Management

**Sub-segments:**
- Commercial property management
- Facility management companies
- Building services
- IFM (Integrated Facility Management)

**Cleaning robot potential:** HIGH
- Multiple buildings under management
- Centralized procurement
- Service contracts
- Cost optimization focus

**Detection keywords:**
- Property management, facility management, FM, building services

---

## Medium-Priority Segments

### Logistics / Warehousing

**Sub-segments:**
- Distribution centers
- Fulfillment centers
- Warehouses
- Cross-dock facilities

**Cleaning robot potential:** MEDIUM
- Large floor areas
- Less public-facing
- Operational focus

**Detection keywords:**
- Warehouse, distribution, fulfillment, logistics, DC

---

### Education

**Sub-segments:**
- Universities / colleges
- School districts
- Research facilities

**Cleaning robot potential:** MEDIUM
- Campus facilities
- Budget constraints
- Seasonal operations

**Detection keywords:**
- University, college, school, campus, education

---

### Government / Public Sector

**Sub-segments:**
- Municipal buildings
- Government offices
- Public transportation hubs
- Airports

**Cleaning robot potential:** MEDIUM
- Public spaces
- Procurement complexity
- Budget cycles

**Detection keywords:**
- Government, municipal, public, city, state, federal

---

## Segment Detection for Channel Partners

When evaluating channel partners, check if their clients fall into these segments:

| Segment | Priority | Client Examples |
|---------|----------|-----------------|
| Healthcare | HIGH | OHSU, Keck Medicine, Kaiser |
| Retail | HIGH | Walmart, Target, CVS, Walgreens |
| Hospitality | HIGH | Marriott, Hilton, MGM |
| Property/FM | HIGH | JLL, CBRE, Cushman & Wakefield |
| Logistics | MEDIUM | Amazon, FedEx, UPS |
| Education | MEDIUM | State universities, community colleges |
| Government | MEDIUM | City of X, State of Y |

---

## Cross-Segment Opportunities

Some channel partners serve multiple segments:

| Partner Type | Segments Served | Opportunity |
|--------------|-----------------|-------------|
| Healthcare IT | Healthcare | High - direct access to facilities |
| Retail POS | Retail | High - many locations |
| Property management software | Property/FM | High - centralized decision-making |
| Building automation | Multiple | Medium - facility integration |
```

**Step 2: Verify file created**

Run: `head -20 /Users/thaddeus/skills/b2b/skills/_shared/target-segments.md`
Expected: First 20 lines of the file

**Step 3: Commit**

```bash
git add skills/_shared/target-segments.md
git commit -m "feat(shared): add target-segments.md defining customer segments"
```

---

### Task 1.3: Move country-strategies.md to _shared

**Files:**
- Move: `skills/distributor-inspector/references/icp-sales/country-strategies.md` → `skills/_shared/country-strategies.md`
- Modify: `skills/distributor-inspector/SKILL.md` (update reference)

**Step 1: Copy country-strategies.md to _shared**

```bash
cp /Users/thaddeus/skills/b2b/skills/distributor-inspector/references/icp-sales/country-strategies.md /Users/thaddeus/skills/b2b/skills/_shared/country-strategies.md
```

**Step 2: Verify copy**

Run: `head -10 /Users/thaddeus/skills/b2b/skills/_shared/country-strategies.md`
Expected: Shows "Global Markets: 35+ countries"

**Step 3: Update distributor-inspector SKILL.md reference**

Find: `references/icp-sales/country-strategies.md`
Replace with: `../_shared/country-strategies.md`

**Step 4: Commit**

```bash
git add skills/_shared/country-strategies.md skills/distributor-inspector/SKILL.md
git commit -m "feat(shared): move country-strategies.md to _shared directory"
```

---

## Phase 2: Create channel-partner-inspector Skill

### Task 2.1: Create skill directory structure

**Files:**
- Create: `skills/channel-partner-inspector/` directory
- Create: `skills/channel-partner-inspector/references/` directory

**Step 1: Create directories**

```bash
mkdir -p /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/references
```

**Step 2: Verify**

Run: `ls -la /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/`
Expected: Directory with `references/` subdirectory

---

### Task 2.2: Create SKILL.md

**Files:**
- Create: `skills/channel-partner-inspector/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
---
name: channel-partner-inspector
description: Use when evaluating websites as potential channel partners for OrionStar Robotics. Identifies companies with client relationships in target segments (healthcare, retail, hospitality, property/FM). These companies don't distribute physical products but can provide warm introductions to end-users. Uses Playwright CLI for navigation.
arguments:
  url:
    description: The URL of the website to inspect (e.g., "valer.health" or "https://valer.health")
    required: true
    type: string
  mode:
    description: Analysis mode: "standard" (text-only, fast) or "deep" (includes image analysis)
    required: false
    type: string
    default: "standard"
---

# Channel Partner Inspector

Inspect and score potential channel partner websites - companies with client relationships in target segments.

## Overview

This skill evaluates companies as **channel partners** - they don't distribute physical products but have relationships with potential end-users for OrionStar cleaning robots.

**Target:** Software companies, service providers, consultants, associations with clients in healthcare, retail, hospitality, property/FM, etc.

**Output:** Scored report with partnership recommendation and suggested approach.

## Prerequisites

```bash
# Install Playwright CLI (one-time)
npm install -g @playwright/cli@latest
```

## Process

### Step 1: Navigate and Capture

**For single URL:**
```bash
# Open browser and navigate
playwright-cli open {url} --persistent -s=cp-inspector

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=cp-inspector
```

**For batch (persistent session):**
```bash
# Initialize session
playwright-cli open about:blank --persistent -s=cp-inspector

# For each URL:
playwright-cli goto {url} -s=cp-inspector
playwright-cli snapshot -s=cp-inspector
```

### Step 2: Extract Company Profile

From the snapshot YAML, extract:
- Company name (page title, headers)
- Products/Services (what they sell)
- Target market (who they serve)
- Named clients (logos, case studies, testimonials)
- Geography (where they/their clients operate)
- Team (sales, BD, account managers)

### Step 3: Detect Client Overlap (PRIMARY GATE)

**Delegate to:** `references/client-detection.md`

Look for named clients in these target segments:

| Segment | Priority | Examples |
|---------|----------|----------|
| Healthcare | HIGH | Hospitals, medical centers, clinics |
| Retail | HIGH | Chains, supermarkets, drug stores |
| Hospitality | HIGH | Hotels, resorts, casinos |
| Property/FM | HIGH | Property management, FM companies |
| Logistics | MEDIUM | Distribution centers, warehouses |
| Education | MEDIUM | Universities, schools |
| Government | MEDIUM | Public buildings, municipal |

**Detection sources:**
- Client logos in footer/homepage
- Case studies / success stories
- Testimonials with company names
- "Who we serve" / "Our clients" pages
- Named references in content

**Gate Result:**
- **PASS** → Named clients in target segments → Continue scoring
- **FAIL** → No client overlap → Route to `exclude` or cross-route

### Step 4: Score Channel Partner Potential

**Delegate to:** `references/scoring-matrix.md`

**Base Score:** 60 points if client overlap gate passes

**Bonus Scoring:**

| Component | Max Points | Criteria |
|-----------|------------|----------|
| Client Quantity | +20 | 1-10: +5, 11-50: +10, 51-200: +15, 200+: +20 |
| Client Quality (KA) | +15 | Named enterprise/recognizable brands |
| Sales Capability | +10 | Has sales/BD/account managers |
| Trust/Relationship Depth | +10 | Long-term clients, case studies, "partnership" language |
| Geographic Reach | +10 | Multi-region/multi-state/international clients |
| Industry Expertise | +5 | Specialized in target industry |
| Partnership History | +5 | Previous co-marketing, integrations, referrals |
| Financial Stability | +5 | PE backed, profitable, 5+ years established |

**Total Cap:** 100 points

### Step 5: Determine Action

| Score | Grade | Action |
|-------|-------|--------|
| 80-100 | A | `prioritize` - Strong partner, route to BD |
| 60-79 | B | `standard` - Viable partner, explore |
| 40-59 | C | `explore` - Potential, nurture |
| <40 | D/F | `exclude` - Not a fit |

### Step 6: Cross-Route if Applicable

**Route to `distributor-inspector` if:**
- Company also sells physical products
- Has distribution capability (warehouse, logistics)

**Route to `ka-inspector` if:**
- Company operates facilities themselves
- Could be an end-user

## Output Format

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country}
**Type:** Channel Partner
**Client Segments:** {healthcare, retail, hospitality, etc.}
**Action:** {prioritize/standard/explore/exclude}

### Company Profile

**Products/Services:**
{what they sell}

**Target Market:**
{who they serve}

**Named Clients:**
{list with segment tags}

### Channel Partner Assessment

| Criterion | Value | Points |
|-----------|-------|--------|
| Client Overlap Gate | {PASS/FAIL} | - |
| Client Quantity | {count} | +{points} |
| Client Quality | {KA names} | +{points} |
| Sales Capability | {evidence} | +{points} |
| Trust/Relationship | {evidence} | +{points} |
| Geographic Reach | {regions} | +{points} |
| Industry Expertise | {specialization} | +{points} |
| Partnership History | {evidence} | +{points} |
| **Total** | | **{score}** |

### Recommended Approach

**Partnership Type:** {referral / co-marketing / integration / bundle}
**Target Contact:** {CEO / BD / Partnerships}
**Suggested Pitch:** {customized based on client base}

### Cross-Routing Suggestion (if applicable)

{If sells physical products → distributor-inspector}
{If operates facilities → ka-inspector}
```

## Cross-Routing FROM Other Skills

**From `distributor-inspector`:**
If company fails hard gates BUT has client overlap, suggest re-inspecting with this skill.

**From `ka-inspector`:**
If company doesn't operate facilities BUT has client overlap, suggest re-inspecting with this skill.

## Configuration Files

| File | Purpose |
|------|---------|
| `references/hard-gates.md` | Client overlap gate definition |
| `references/scoring-matrix.md` | Complete bonus scoring matrix |
| `references/client-detection.md` | How to detect and categorize clients |
| `../_shared/target-segments.md` | Target segment definitions |
| `../_shared/country-strategies.md` | Country-specific strategies |
```

**Step 2: Verify file created**

Run: `head -30 /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/SKILL.md`
Expected: YAML frontmatter and first sections

**Step 3: Commit**

```bash
git add skills/channel-partner-inspector/SKILL.md
git commit -m "feat(channel-partner): add SKILL.md with inspection process"
```

---

### Task 2.3: Create hard-gates.md

**Files:**
- Create: `skills/channel-partner-inspector/references/hard-gates.md`

**Step 1: Write hard-gates.md**

```markdown
# Hard Gates - Channel Partner Inspector

> **Purpose:** Define the primary qualification gate for channel partners
> **Related:** `../_shared/target-segments.md`

---

## Primary Gate: Client Overlap

A company qualifies as a channel partner prospect if they have **named clients in target segments**.

### Gate Definition

| Gate | Requirement | Weight |
|------|-------------|--------|
| **Client Overlap** | Has named clients in target segments | PASS/FAIL (blocking) |

### What Counts as Client Evidence

**Strong Evidence (definite client):**
- Client logo with link to case study
- Named testimonial with person's name and company
- Case study / success story with named company
- "Our clients include: [Company A, Company B, ...]"
- Press release mentioning client relationship

**Moderate Evidence (likely client):**
- Client logos without case study links
- "Trusted by [industry] leaders" with logos
- "Who we serve" page with company types

**Weak Evidence (possible client):**
- Industry mentions without specific companies
- "Serving Fortune 500 companies" (no names)

**Minimum for PASS:** At least ONE named client in a target segment

### Target Segments (from _shared/target-segments.md)

| Segment | Priority | Client Types |
|---------|----------|--------------|
| Healthcare | HIGH | Hospitals, medical centers, clinics, health systems |
| Retail | HIGH | Retail chains, supermarkets, drug stores, malls |
| Hospitality | HIGH | Hotels, resorts, casinos, event venues |
| Property/FM | HIGH | Property management, facility management, IFM |
| Logistics | MEDIUM | Warehouses, distribution centers, fulfillment |
| Education | MEDIUM | Universities, colleges, school districts |
| Government | MEDIUM | Municipal, state, federal agencies |

### Gate Evaluation Process

1. **Scan for client evidence:**
   - Check homepage for client logos
   - Look for "Clients", "Case Studies", "Success Stories" pages
   - Check testimonials for company names
   - Search for "our clients", "who we serve", "trusted by"

2. **Categorize each client:**
   - Map client to target segment (Healthcare, Retail, etc.)
   - Note if client is KA (enterprise/recognizable brand)

3. **Determine gate result:**
   - If ANY client in target segment → PASS
   - If NO clients in target segments → FAIL

### Gate Result Impact

| Result | Action |
|--------|--------|
| **PASS** | Continue to scoring (base score: 60) |
| **FAIL** | Route to `exclude` or cross-route to appropriate skill |

---

## Cross-Routing on Gate Fail

If client overlap gate FAILS, check for alternative fits:

| Condition | Route To |
|-----------|----------|
| Sells physical products | `distributor-inspector` |
| Operates facilities | `ka-inspector` |
| Neither | `exclude` (not a prospect)
```

**Step 2: Verify**

Run: `head -20 /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/references/hard-gates.md`

**Step 3: Commit**

```bash
git add skills/channel-partner-inspector/references/hard-gates.md
git commit -m "feat(channel-partner): add hard-gates.md with client overlap gate"
```

---

### Task 2.4: Create scoring-matrix.md

**Files:**
- Create: `skills/channel-partner-inspector/references/scoring-matrix.md`

**Step 1: Write scoring-matrix.md**

```markdown
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
```

**Step 2: Verify**

Run: `head -30 /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/references/scoring-matrix.md`

**Step 3: Commit**

```bash
git add skills/channel-partner-inspector/references/scoring-matrix.md
git commit -m "feat(channel-partner): add scoring-matrix.md with bonus criteria"
```

---

### Task 2.5: Create client-detection.md

**Files:**
- Create: `skills/channel-partner-inspector/references/client-detection.md`

**Step 1: Write client-detection.md**

```markdown
# Client Detection Guide

> **Purpose:** How to extract and categorize client lists from websites
> **Related:** `hard-gates.md`, `../_shared/target-segments.md`

---

## Detection Sources

### Primary Sources (High Confidence)

1. **Client Logos Section**
   - Location: Usually in footer, homepage, or dedicated "Clients" page
   - Detection: Look for logo grids with company names in alt text
   - Signal: "Our clients", "Trusted by", "Who we serve"

2. **Case Studies / Success Stories**
   - Location: `/case-studies`, `/success-stories`, `/customers`
   - Detection: Named company with story details
   - Signal: "Read how [Company] achieved [result]"

3. **Testimonials with Attribution**
   - Location: Homepage, product pages, about page
   - Detection: Quote + person name + company name
   - Signal: "– [Name], [Title], [Company]"

### Secondary Sources (Medium Confidence)

4. **"Who We Serve" Pages**
   - Location: `/who-we-serve`, `/industries`, `/solutions`
   - Detection: Industry pages with named examples
   - Signal: "Serving [industry] leaders like..."

5. **Press Releases / News**
   - Location: `/news`, `/press`, `/blog`
   - Detection: Announcements of client wins
   - Signal: "[Company] selects [Vendor] for..."

6. **Partner/Integration Pages**
   - Location: `/partners`, `/integrations`
   - Detection: Mutual customers mentioned
   - Signal: "Together with [Partner], serving [Client]"

---

## Extraction Process

### Step 1: Scan Homepage

Look for:
- Logo sections (footer, mid-page)
- Testimonial carousels
- "Trusted by N companies" claims
- Client count claims ("Serving 500+ organizations")

### Step 2: Check Common Pages

Navigate to:
- `/clients` or `/customers`
- `/case-studies` or `/success-stories`
- `/who-we-serve` or `/industries`
- `/about` (may list notable clients)

### Step 3: Extract Client Names

For each detected client:
1. Record company name
2. Note detection source (logo, case study, testimonial)
3. Categorize by segment (Healthcare, Retail, etc.)
4. Note if KA (recognizable enterprise brand)

---

## Segment Categorization

### Healthcare

**Keywords:** Hospital, medical center, clinic, health system, healthcare, patient, clinical

**Examples:**
- OHSU (Oregon Health & Sciences University)
- Keck Medicine USC
- Kaiser Permanente
- HCA Healthcare
- Cleveland Clinic

### Retail

**Keywords:** Retail, store, chain, supermarket, pharmacy, grocery, mall

**Examples:**
- Walmart
- Target
- CVS Health
- Walgreens
- Kroger
- Albertsons

### Hospitality

**Keywords:** Hotel, resort, casino, hospitality, guest, lodging, accommodation

**Examples:**
- Marriott International
- Hilton
- MGM Resorts
- Caesars Entertainment
- IHG

### Property / Facility Management

**Keywords:** Property management, facility management, FM, building services, real estate, CRE

**Examples:**
- JLL
- CBRE
- Cushman & Wakefield
- Colliers
- Prologis

### Logistics

**Keywords:** Warehouse, distribution, fulfillment, logistics, supply chain, DC

**Examples:**
- Amazon
- FedEx
- UPS
- DHL
- XPO Logistics

### Education

**Keywords:** University, college, school, campus, education, academic

**Examples:**
- State University systems
- Community college districts
- Private universities

### Government

**Keywords:** Government, municipal, city, state, federal, public sector, agency

**Examples:**
- City of [Name]
- State of [Name]
- GSA
- Department of [X]

---

## Output Format

Extract clients in this format:

```markdown
**Named Clients:**
- OHSU (Healthcare) - KA
- Keck Medicine USC (Healthcare) - KA
- Kern Medical (Healthcare)
- Golden Valley Health Centers (Healthcare)
- Omni Family Health (Healthcare)
```

---

## Client Count Estimation

When exact count unavailable:

| Signal | Estimated Count |
|--------|-----------------|
| "Serving 500+ organizations" | 500+ |
| Logo grid with 20+ logos | 20+ |
| "Fortune 500 clients" | Assume 5-10 |
| "Trusted by industry leaders" | Assume 5-10 |
| No signals | Count extracted names |
```

**Step 2: Verify**

Run: `head -30 /Users/thaddeus/skills/b2b/skills/channel-partner-inspector/references/client-detection.md`

**Step 3: Commit**

```bash
git add skills/channel-partner-inspector/references/client-detection.md
git commit -m "feat(channel-partner): add client-detection.md for extracting client lists"
```

---

## Phase 3: Add Cross-Routing to Existing Skills

### Task 3.1: Add cross-routing to distributor-inspector

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md`

**Step 1: Add cross-routing section after Step 6: Route**

Add this section to SKILL.md after the routing table:

```markdown
### Step 6.5: Cross-Route to Channel Partner Inspector (NEW)

**Trigger:** Company fails hard gates BUT has client overlap with target segments

**Detection:**
After determining route, check for client overlap:
1. Scan for named clients in target segments (Healthcare, Retail, Hospitality, Property/FM)
2. If clients detected AND route is `exclude` or `explore`:
   - Add "⚠️ Channel Partner Potential" section to output

**Output Addition:**
```markdown
### ⚠️ Channel Partner Potential

This company does not qualify as a traditional distributor, but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.

**Why this matters:** Their clients are potential end-users for cleaning robots. A partnership could provide warm introductions to facility decision-makers.
```

**Reference:** See `../_shared/target-segments.md` for target segment definitions.
```

**Step 2: Verify section added**

Run: `grep -A 10 "Cross-Route to Channel Partner" /Users/thaddeus/skills/b2b/skills/distributor-inspector/SKILL.md`

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat(distributor-inspector): add cross-routing to channel-partner-inspector"
```

---

### Task 3.2: Add cross-routing to ka-inspector

**Files:**
- Modify: `skills/ka-inspector/SKILL.md`

**Step 1: Add cross-routing section**

Find the routing section in ka-inspector/SKILL.md and add:

```markdown
### Cross-Route to Channel Partner Inspector

**Trigger:** Company doesn't operate facilities BUT has client overlap with target segments

**Detection:**
After determining company is not a KA (doesn't operate facilities), check:
1. Does this company have named clients in target segments?
2. If yes, they may be a channel partner rather than end-user

**Output Addition (if triggered):**
```markdown
### ⚠️ Channel Partner Potential

This company is not a direct end-user (doesn't operate facilities), but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.
```
```

**Step 2: Verify**

Run: `grep -A 5 "Channel Partner" /Users/thaddeus/skills/b2b/skills/ka-inspector/SKILL.md`

**Step 3: Commit**

```bash
git add skills/ka-inspector/SKILL.md
git commit -m "feat(ka-inspector): add cross-routing to channel-partner-inspector"
```

---

## Phase 4: Testing

### Task 4.1: Test channel-partner-inspector with Valer.health

**Files:**
- Test: Run `channel-partner-inspector` skill on `https://valer.health/`

**Step 1: Run the skill**

Use the Skill tool with `channel-partner-inspector` on `https://valer.health/`

**Step 2: Verify output**

Expected results:
- Type: Channel Partner
- Client Segments: Healthcare
- Client Overlap Gate: PASS
- Score: 70-100 (A or B grade)
- Action: `prioritize` or `standard`
- Named clients: OHSU, Keck Medicine USC, Kern Medical, etc.

**Step 3: Document results**

If test passes, note in commit. If fails, debug and fix.

---

### Task 4.2: Test cross-routing from distributor-inspector

**Files:**
- Test: Run `distributor-inspector` on `https://valer.health/`

**Step 1: Run distributor-inspector on Valer**

**Step 2: Verify cross-routing appears**

Expected:
- Original route: `exclude` (fails hard gates - no physical distribution)
- Cross-routing section appears: "⚠️ Channel Partner Potential"
- Suggests re-inspecting with `channel-partner-inspector`

---

### Task 4.3: Final commit and summary

**Step 1: Verify all files in place**

```bash
echo "=== _shared ===" && ls skills/_shared/
echo "=== channel-partner-inspector ===" && ls -R skills/channel-partner-inspector/
```

Expected:
```
=== _shared ===
country-strategies.md
target-segments.md

=== channel-partner-inspector ===
SKILL.md
references/
  hard-gates.md
  scoring-matrix.md
  client-detection.md
```

**Step 2: Final commit**

```bash
git add -A
git commit -m "feat: complete channel-partner-inspector implementation

- Add channel-partner-inspector skill with client overlap detection
- Add _shared directory for common resources
- Add cross-routing from distributor-inspector and ka-inspector
- Test with Valer.health - correctly identifies as channel partner"
```

---

## Success Criteria

| Criterion | Verification |
|-----------|--------------|
| Valer scores 70+ as channel partner | Run channel-partner-inspector |
| distributor-inspector cross-routes to channel-partner | Run distributor-inspector on Valer |
| _shared directory exists with target-segments.md | `ls skills/_shared/` |
| No duplicated files | `find skills -name "country-strategies.md"` shows one in _shared |
| All three skills reference _shared | Check SKILL.md files |
