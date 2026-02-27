---
name: ka-inspector
description: Use when evaluating websites as potential KA (Key Account) end customers for OrionStar Robotics cleaning robots. Identifies companies that BUY and USE robots directly. Uses Playwright CLI for navigation. Supports standard (text-only) and deep (image analysis) modes.
arguments:
  url:
    description: The URL of the website to inspect (e.g., "metro.de" or "https://metro.de")
    required: true
    type: string
  mode:
    description: Analysis mode: "standard" (text-only, fast) or "deep" (includes image analysis)
    required: false
    type: string
    default: "standard"
---

# KA Inspector (Key Account End Customer)

Inspect and score potential KA end customer websites for direct sales of cleaning robots.

## Overview

This skill evaluates companies as **direct customers** (end users) for OrionStar cleaning robots. Unlike the distributor-inspector which targets RESELLERS, this skill targets companies that would BUY and USE the robots themselves.

**Target:** Companies with facilities that need cleaning (retail chains, hotels, warehouses, hospitals, property management)

**Output:** Scored report with pilot-readiness assessment and recommended action.

## Prerequisites

```bash
# Install Playwright CLI (one-time)
npm install -g @playwright/cli@latest
```

## Deep Mode (Image Analysis)

When `mode="deep"` is specified, additional image analysis is performed:

1. **Facility Photos** - Verify facility type and scale (retail stores, hotels, offices, warehouses)
2. **Location Count** - Visual confirmation of multi-site presence from location pages
3. **Brand/Partnership Logos** - Identify technology partners, certifications, industry associations
4. **Digital Systems** - Detect IoT, building management system mentions in imagery

**Processing time:** ~90 seconds (vs ~30 seconds standard mode)

**Additional files created in deep mode:**
- `home.png` - Full homepage screenshot
- `locations.png` - Locations/About page screenshot (if available)

**Image analysis delegation:** `references/image-analyzer.md`

## Process

### Step 1: Navigate and Capture

**For single URL:**
```bash
playwright-cli open {url} --persistent -s=ka-inspector
playwright-cli snapshot -s=ka-inspector

# Deep mode: Capture screenshots for image analysis
if mode == "deep":
  playwright-cli screenshot -s=ka-inspector --full-page home.png
  playwright-cli goto {url}/locations -s=ka-inspector 2>/dev/null || playwright-cli goto {url}/about -s=ka-inspector 2>/dev/null
  playwright-cli screenshot -s=ka-inspector --full-page locations.png
```

**For batch (persistent session):**
```bash
playwright-cli open about:blank --persistent -s=ka-inspector
playwright-cli goto {url} -s=ka-inspector
playwright-cli snapshot -s=ka-inspector

# Deep mode: capture screenshots after each snapshot
if mode == "deep":
  playwright-cli screenshot -s=ka-inspector --full-page home.png
  playwright-cli goto {url}/locations -s=ka-inspector 2>/dev/null || playwright-cli goto {url}/about -s=ka-inspector 2>/dev/null
  playwright-cli screenshot -s=ka-inspector --full-page locations.png
```

### Step 2: Extract Company Profile

From the snapshot YAML, extract:

| Field | Description | Where to Find |
|-------|-------------|---------------|
| Company name | Legal/company name | Page title, header, About, Impressum |
| Industry | Primary business sector | Products, services, About |
| Facilities | Owned/managed properties | Locations, portfolio, sites |
| Geography | Countries/regions covered | Locations, branches, coverage |
| Scale | Company size indicators | "X employees", "Y locations", revenue |
| Budget signals | Procurement/function indicators | Careers (hiring), CapEx mentions, investor relations |
| Contacts | Decision-maker info | Leadership, management, facilities team |

### Step 2.5: Analyze Images (Deep Mode Only)

**Only if mode="deep":**

**Delegate to:** `references/image-analyzer.md`

From captured screenshots (`home.png`, `locations.png`):
1. **Facility photos** - Verify facility type (retail stores, hotels, offices, warehouses, hospitals)
2. **Location count** - Count locations from location page or map visualization
3. **Partnership/certification logos** - Detect technology partners, industry certifications, associations

Add findings to the report under "### Deep Mode Analysis" section.

**If no images captured or analysis fails:** Include "Not analyzed (image capture failed)" in Deep Mode Analysis section.

### Step 3: Extract Contact Information

Extract:
- Phone numbers (all formats)
- Email addresses
- Physical addresses (HQ, facilities)
- LinkedIn company page
- Key decision-makers (Facilities Manager, Operations Director, Property Manager)

### Step 4: Check Hard Gates

**Delegate to:** `references/icp-sales/hard-gates.md`

| Gate | Requirement | Detection |
|------|-------------|-----------|
| **Budget** | Has procurement/facility management function | Careers (hiring), organizational structure, procurement pages |
| **Contact** | Has on-site contact (facilities/operations/IT) | Team pages, facility management mentions |
| **Pilot Timeline** | Can launch quickly (no long renovation) | Project timeline mentions, "quick deployment" language |

**Gate Logic:**
- **ALL PASS** → Eligible for pilot-ready status
- **1 FAIL** → Route to `nurture`
- **2+ FAIL** → Route to `exclude`

### Step 5: Score

**Delegate to:** `references/icp-skill/scoring-matrix.md`

| Component | Max Points |
|-----------|------------|
| Base score (has budget + contact) | 50 |
| Multi-site potential | +30 |
| Digital maturity | +20 |
| Pilot KPI clarity | +20 |
| Cross-team coordination | +15 |

**Total capped at 100**

### Step 6: Route

| Grade | Score | Action |
|-------|-------|--------|
| A | 80-100 | `pilot-ready` (prioritize) |
| B | 60-79 | `pilot-ready` (standard) |
| C | 40-59 | `nurture` |
| D/F | <40 | `exclude` |

---

## Output Format

```markdown
---
{Company Name} - {Grade} ({score}/100)

URL: {url}
Country: {country}
Industry: {industry}
Action: {action}

---

### Company Profile

**Industry:** {primary_business}

**Facilities:**
- {facility_type_1}: {count} locations
- {facility_type_2}: {count} locations

**Scale:**
- Employees: {count} (if found)
- Revenue: {amount} (if found)
- Locations: {count}

**Geography:**
- HQ: {location}
- Coverage: {regions}

---

### Contact

- **Phone:** {phone}
- **Email:** {email}
- **Headquarters:** {address}
- **LinkedIn:** {url}

---

### Deep Mode Analysis (if mode="deep")

**Facility Photos:**
{analysis results or "Not analyzed (standard mode)"}

**Location Count:**
{analysis results or "Not analyzed (standard mode)"}

**Partnerships/Certifications:**
{analysis results or "Not analyzed (standard mode)"}

---

### Hard Gates Evaluation

| Gate | Result | Evidence |
|------|--------|----------|
| Budget/Procurement | {PASS/FAIL/UNCLEAR} | {evidence} |
| On-site Contact | {PASS/FAIL/UNCLEAR} | {evidence} |
| Pilot Timeline | {PASS/FAIL/UNCLEAR} | {evidence} |

**Gate Result:** {ALL_PASS / SOME_FAIL / MOST_FAIL}

---

### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Base score | {qualified/partial} | {base} |
| Multi-site potential | {details} | +{bonus} |
| Digital maturity | {details} | +{bonus} |
| Pilot KPI | {details} | +{bonus} |
| Cross-team coordination | {details} | +{bonus} |
| **Total** | | **{total}** |

---

### Summary

{2-3 sentence summary of the company and why they are/aren't a good KA prospect}
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `references/icp-summary.md` | Quick reference |
| `references/icp-sales/hard-gates.md` | Hard qualification gates |
| `references/icp-sales/bonus-criteria.md` | Bonus criteria |
| `references/icp-sales/target-industries.md` | Target industry list |
| `references/icp-sales/exclusion-rules.md` | Exclusion criteria |
| `references/icp-sales/country-strategies.md` | Country priorities |
| `references/icp-skill/gate-translation.md` | AI detection logic |
| `references/icp-skill/scoring-matrix.md` | Complete scoring |
| `references/icp-skill/site-potential-rules.md` | Multi-site evaluation |

---

## Example Usage

```bash
# Single URL - Standard mode (text-only, fast)
playwright-cli open https://metro.de --persistent -s=ka-inspector
playwright-cli snapshot -s=ka-inspector

# Single URL - Deep mode (includes image analysis)
playwright-cli open https://metro.de --persistent -s=ka-inspector
playwright-cli snapshot -s=ka-inspector
# Claude will automatically capture screenshots and analyze images

# Batch - Standard mode
playwright-cli open about:blank --persistent -s=ka-inspector
playwright-cli goto https://example-retail.com -s=ka-inspector
playwright-cli snapshot -s=ka-inspector

# Batch - Deep mode
playwright-cli open about:blank --persistent -s=ka-inspector
playwright-cli goto https://example-retail.com -s=ka-inspector
playwright-cli snapshot -s=ka-inspector
# Claude will automatically capture screenshots after each snapshot
```

---

## Key Differences from Distributor Inspector

| Aspect | Distributor Inspector | KA Inspector |
|--------|----------------------|--------------|
| **Target** | RESELLERS | END CUSTOMERS |
| **Hard Gates** | 6 (team, SLA, etc.) | 3 (budget, contact, timeline) |
| **Bonus Focus** | Channel capability | Multi-site potential |
| **Output Actions** | `prioritize`/`standard`/`explore`/`exclude` | `pilot-ready`/`nurture`/`exclude` |