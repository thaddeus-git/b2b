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
