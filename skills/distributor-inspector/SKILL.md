---
name: distributor-inspector
description: Use when evaluating websites as potential distributors for OrionStar Robotics (cleaning robots). Uses Playwright CLI for navigation. Same extraction/scoring as MCP version. Supports standard (text-only) and deep (image analysis) modes.
arguments:
  url:
    description: The URL of the website to inspect (e.g., "frigosystem.de" or "https://frigosystem.de")
    required: true
    type: string
  mode:
    description: Analysis mode: "standard" (text-only, fast) or "deep" (includes image analysis)
    required: false
    type: string
    default: "standard"
---

# Distributor Inspector (Primary Implementation)

Inspect and score potential distributor websites using Playwright CLI for navigation.

## Overview

This skill is **functionally identical** to `distributor-inspector` (MCP version), but uses `playwright-cli` commands instead of MCP tools for website navigation. Same extraction, same scoring, same report format.

## Prerequisites

```bash
# Install Playwright CLI (one-time)
npm install -g @playwright/cli@latest

# Install shared utilities
cd skills/shared-scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Deep Mode (Image Analysis)

When `mode="deep"` is specified, additional image analysis is performed:

1. **Team Photo Analysis** - Count faces to verify employee count (hard gate validation)
2. **Logo Detection** - Identify competitor brand logos in footer/partners sections
3. **Certification Badges** - Detect ISO, authorized dealer badges
4. **Product Images** - Visual confirmation of product types

**Processing time:** ~90 seconds (vs ~30 seconds standard mode)

**Additional files created in deep mode:**
- `home.png` - Full homepage screenshot
- `team.png` - Team/About page screenshot (if available)

**Image analysis:** The LLM reads screenshot files directly using built-in vision capabilities. See `../shared-references/image-analysis-guide.md` for what to look for.

## Process

### Step 1: Navigate and Capture

**For single URL:**
```bash
# Open browser and navigate
playwright-cli open {url} --persistent -s=inspector

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=inspector
```

**Deep mode:** After snapshot, capture screenshots for image analysis:
- Navigate to team/about page if available
- Capture and save screenshots to files (e.g., `home.png`, `team.png`)
- The LLM will read these image files directly using its vision capabilities

**For batch (persistent session):**
```bash
# Initialize session
playwright-cli open about:blank --persistent -s=inspector

# For each URL:
playwright-cli goto {url} -s=inspector
playwright-cli snapshot -s=inspector
# Deep mode: capture screenshots after each snapshot
```

### Step 2: Extract Company Profile

**Delegate to:** `../shared-references/company-profiler.md`

From the snapshot YAML, extract:
- Company name (page title, headers, Impressum)
- Products (product pages, catalog mentions)
- Services (service offerings, maintenance, support)
- Brands carried (brand logos, "our partners", "distributors of")
- Geography (coverage area, customer locations, HQ address)
- Team (employee count, team structure mentions)
- SLA (response times, service commitments)

### Step 2.5: Analyze Images (Deep Mode Only)

**Only if mode="deep":**

**Delegate to:** `../shared-references/image-analysis-guide.md`

From captured screenshots:
1. **Team photos** - Count faces, estimate employee count
2. **Brand logos** - Detect Pudu, Gausium, LionsBot, Tennant, etc.
3. **Certifications** - Detect ISO badges, "Authorized Dealer" badges

**How image analysis works:** The LLM reads screenshot files directly using built-in vision capabilities. No special image processing tools needed.

Add findings to the report under "### Deep Mode Analysis" section.

**If no images captured or analysis fails:** Include "Not analyzed (image capture failed)" in Deep Mode Analysis section.

### Step 3: Extract Contact Information

**Delegate to:** `../shared-references/contact-extractor.md`

Extract:
- Phone numbers (all formats: +49, 0049, local)
- Email addresses (including obfuscated)
- Physical address (structured address blocks)
- WhatsApp (wa.me links or labeled numbers)
- LinkedIn company page URL
- Additional channels (Facebook, Instagram, YouTube, X)

**Mandatory LinkedIn Search:**

If LinkedIn not found on website, run the search script directly:

```bash
# Run from the distributor-inspector skill directory:
python3 ../shared-scripts/serp_search.py "{company_name} linkedin" "{country}" "{language}" "5"
```

Parse the JSON output and extract the LinkedIn URL from the first matching result.

If the script fails (missing dependency, API key error, etc.), report "Not found (searched)" and continue.

### Step 4: Categorize

**Delegate to:** `../shared-references/tags.md`

Apply tags using format: `{category}-{business-model}`

Multiple tags allowed per company.

**Special tags:**
- `competitor-robot-distributor` - Sells Pudu/Gausium/LionsBot/etc.
- `pure-2c-retail` - B2C only (check for commercial products exception)
- `cleaning-services-provider` - Contract cleaning services
- `hospitality-service-provider` - Hotel chains, hospitality groups

### Step 4.1: Classify Industry

**Delegate to:** `references/industry-taxonomy.md`

Select the most appropriate industry and sub-industry based on:
1. **Primary business** - What products/services do they primarily offer?
2. **Customer type** - Are they an agent/distributor or end user?
3. **Match to taxonomy** - Find the closest match from the Industry Taxonomy

**Format:** `{Industry Chinese} ({Industry English}) → {Sub-industry}`

### Step 4.5: Classify Company Scale (NEW - CRITICAL)

**Delegate to:** `../shared-references/smb-classifier.md`

Before evaluating hard gates, classify the company by scale:

| Classification | Employee Range | Locations | Score Cap | Max Grade |
|----------------|----------------|-----------|-----------|-----------|
| **SMB** | <20 or unknown | Single property | 50 | C |
| **MID-MARKET** | 20-500 | 2-5 branches | 75 | B |
| **KA** | 500+ or sophisticated | 6+ branches | 100 | A |

**SMB Detection Signals:**
- Single property/location (e.g., one hotel, one shop)
- "Family business", "Familienbetrieb", no department structure
- Employee count not stated or <20
- No procurement function visible
- Hospitality single-property pattern (Gasthof, Pension)

**Output:** Add "Classification" section to report with rationale.

---

### Step 4.6: Check Hard Gates (CRITICAL)

**Delegate to:** `../shared-references/icp/hard-gates.md` and `../shared-references/icp/gate-translation.md`

After classification, evaluate all 6 hard gates:

| Gate | Requirement | Detection |
|------|-------------|-----------|
| Company Size | 20-500 employees, ~€10M revenue | About/Impressum, team count, revenue mentions |
| Team Capability | Sales + Deployment + After-sales | Team page, service sections |
| SLA Capability | Quantifiable response times | "24h", "48h", "SLA" mentions |
| PoC Capability | Demo/trial support | "Demo", "showroom", "trial" |
| Market Coverage | 1-3 cities, cross-city service | Multiple locations, service area |
| Price Discipline | MSRP/authorized dealer | Brand partnership language |

**Gate Logic:**

| Classification | Gate Result | Max Score | Eligible Grades |
|----------------|-------------|-----------|-----------------|
| **SMB** | Any | 50 | C / D / F |
| **MID-MARKET** | ALL_PASS | 75 | A / B / C |
| **MID-MARKET** | SOME_FAIL | 50 | C only |
| **MID-MARKET** | MOST_FAIL | 0 | exclude |
| **KA** | ALL_PASS | 100 | A / B / C |
| **KA** | SOME_FAIL | 50 | C only |
| **KA** | MOST_FAIL | 0 | exclude |

- **ALL PASS** → Eligible for A/B grade (subject to classification cap)
- **1-2 FAIL** → Cap max score at 50 (explore tier only)
- **3+ FAIL** → Route to `exclude` regardless of classification

**Document evidence for each gate** in the report.

### Step 5: Score

**Delegate to:** `../shared-references/icp/scoring-matrix.md`

**Scoring Order:**
1. Determine base score from hard gates result
2. Apply classification cap (SMB=50, MID-MARKET=75, KA=100)
3. Calculate bonuses
4. Apply final cap (whichever is lower: classification or gates)

| Component | Max Points | Notes |
|-----------|------------|-------|
| Base score (qualified B2B) | 60 | ALL_PASS gates |
| Base score (partial) | 40 | SOME_FAIL (1-2 gates) |
| Base score (unqualified) | 0 | MOST_FAIL (3+ gates) |
| Cleaning equipment focus | +90 | Core business = +90 |
| Competitor footprint | +90 | Official distributor = +90 |
| Distribution network | +20 | Reseller program |
| System integration capability | +20 | API/customization |
| Existing FM/property customers | +15 | Per category (+5 each) |
| After-sales maturity | +15 | SLA/spare parts/ticketing |
| Demo/showroom capability | +10 | Showroom + demo policy |
| Marketing investment | +10 | Exhibitions/social |
| Customer overlap | +50 | Target segment overlap |

**Total capped at:**
- 100 for KA with ALL_PASS gates
- 75 for MID-MARKET with ALL_PASS gates
- 50 for SMB or ANY with SOME_FAIL gates
- 0 for MOST_FAIL gates (exclude)

**CRITICAL: Do NOT award bonuses for SMB-typical signals:**
- ~~"Has website"~~ → Not digital maturity (must have B2B procurement signals)
- ~~"Family operation"~~ → Not cross-team coordination (must have explicit departments)
- ~~"Facebook page"~~ → Not marketing investment (must have exhibitions/trade budget)
- ~~"Online booking"~~ → Not pilot KPI (must have cleaning/service KPIs)

**Valid Bonus Signals:**

| Bonus | Valid Signals Only |
|-------|-------------------|
| Digital maturity | B2B portal, tender/RFP page, procurement system |
| Cross-team coordination | Org chart, 3+ named departments, team structure page |
| Marketing investment | Trade fair participation, marketing budget mentioned, B2B content |
| Pilot KPI | Cleaning SLA mentions, performance metrics, service KPIs |

**Commercial Products Pre-Check:**

Before scoring, check if company has commercial products:
- If tagged `pure-2c-retail` AND NO commercial products → Route to `exclude`
- If tagged `pure-2c-retail` BUT has commercial products → Score normally

Commercial product signals: cleaning equipment, facility management, janitorial supplies, robotics/automation, B2B/wholesale.

**Country Adjustments:**
- See `../shared-references/country-strategies.md` for full list (35+ countries)
- All countries in the strategy document are TARGET MARKETS - do not exclude based on geography
- Apply region-specific bonuses (IMPORTANT markets: DE, FR, IT, UK, HU get dedicated strategies)

### Step 6: Route

**Final action is determined by:** Classification + Gate Result + Score

| Classification | Gate Result | Score Range | Grade | Action |
|----------------|-------------|-------------|-------|--------|
| **SMB** | Any | 0-50 | C/D/F | nurture or exclude |
| **MID-MARKET** | ALL_PASS | 70-75 | A | prioritize |
| **MID-MARKET** | ALL_PASS | 50-69 | B | standard |
| **MID-MARKET** | ALL_PASS | <50 | C | explore |
| **MID-MARKET** | SOME_FAIL | Any | C | explore |
| **MID-MARKET** | MOST_FAIL | 0 | F | exclude |
| **KA** | ALL_PASS | 90-100 | A | prioritize |
| **KA** | ALL_PASS | 70-89 | B | standard |
| **KA** | ALL_PASS | 50-69 | C | explore |
| **KA** | SOME_FAIL | Any | C | explore |
| **KA** | MOST_FAIL | 0 | F | exclude |

**Special routing (overrides score + classification):**
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider` (chain/hotel group): `route-to-ka`
- Tagged `pure-2c-retail` with NO commercial products: `exclude`
- Tagged `hospitality-single-property` (Gasthof, Pension): `nurture` or `exclude`

### Step 6.5: Cross-Route to Channel Partner Inspector (NEW)

**Trigger:** Company fails hard gates BUT has client overlap with target segments

**Detection:**
After determining route, check for client overlap:
1. Scan for named clients in target segments (Healthcare, Retail, Hospitality, Property/FM)
2. If clients detected AND route is `exclude` or `explore`:
   - Add "Channel Partner Potential" section to output

**Output Addition:**
```markdown
### ⚠️ Channel Partner Potential

This company does not qualify as a traditional distributor, but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.

**Why this matters:** Their clients are potential end-users for cleaning robots. A partnership could provide warm introductions to facility decision-makers.
```

**See:** `../shared-references/cross-routing.md` for complete routing decision matrix

**Reference:** See `../shared-references/target-segments.md` for target segment definitions.

## Output Format

**Delegate to:** `references/output-format.md`

Use the exact template structure from the output format reference. The report must include:
- Company profile with products, services, brands, geography, team, SLA
- Deep Mode Analysis (if applicable)
- Contact information
- Classification with rationale
- Hard Gates Evaluation
- Scoring Details
- Summary

**Key sections to include:**

| Section | Required |
|---------|----------|
| Company Profile | ✅ Always |
| Contact | ✅ Always |
| Classification | ✅ Always |
| Hard Gates Evaluation | ✅ Always |
| Scoring Details | ✅ Always |
| Deep Mode Analysis | Only if mode="deep" |
| Channel Partner Potential | Only if client overlap detected |
| Sales Play | Only if competitor footprint detected |

## Error Handling

### Navigation Failure

If the website cannot be accessed:
1. Retry navigation once
2. Check if URL is correct and accessible
3. Return error with URL for manual review

**Report format:**
```markdown
## {url} - ERROR

**Error:** Navigation failed - {reason}

**Action:** Manual review required
```

### Empty Snapshot

If the snapshot is empty or missing key information:
1. Try scrolling: `playwright-cli press End -s=inspector`
2. Wait 2 seconds, retry snapshot
3. If still empty, return error for manual review

### Cookie Modal Handling

**Detection Selectors:**
- `[data-testid="cookie-modal"]`, `.cookie-consent`, `#onetrust`, `.cookie-banner`
- Buttons: "Accept all", "Alle akzeptieren", "Tout accepter", "Reject", "Ablehnen"

**Dismissal Priority:**
1. "Accept All" / "Alle akzeptieren" / "Tout accepter"
2. "Reject" / "Ablehnen" / "Tout refuser"
3. Close button (`[aria-label="close"]`, `.close-btn`)
4. "Settings" (last resort)

**If modal dismissal fails:**
- Proceed with available snapshot
- Add warning to output: `**Warning:** Cookie popup present - could not dismiss`

---

## Configuration Files

### ICP Reference Files (Shared Structure)

| File | Purpose |
|------|---------|
| `../shared-references/icp/hard-gates.md` | Hard qualification gates |
| `../shared-references/icp/bonus-criteria.md` | Bonus criteria from sales ICP |
| `../shared-references/icp/target-industries.md` | Target industry list |
| `../shared-references/icp/exclusion-rules.md` | Exclusion criteria |
| `../shared-references/country-strategies.md` | Global strategies (35+ countries) |
| `../shared-references/icp/gate-translation.md` | How AI interprets each gate |
| `../shared-references/icp/scoring-matrix.md` | Complete bonus scoring matrix |
| `../shared-references/icp/customer-overlap-rules.md` | Explicit customer overlap scoring |

### Reference Files (Shared)

| File | Purpose |
|------|---------|
| `../shared-references/tags.md` | Niche market tag taxonomy |
| `../shared-references/keywords.md` | Product/service keywords by industry |
| `../shared-references/competing-brands.md` | Competitor brands to detect |
| `../shared-references/company-profiler.md` | Company profile extraction |
| `../shared-references/contact-extractor.md` | Contact information extraction |
| `../shared-references/smb-classifier.md` | Company scale classification |
| `../shared-references/image-analysis-guide.md` | Image analysis procedures |
| `../shared-references/target-segments.md` | Target segment definitions |
| `../shared-references/cross-routing.md` | Cross-route decision matrix |

### Local Reference Files

| File | Purpose |
|------|---------|
| `references/output-format.md` | Report template structure |
| `references/industry-taxonomy.md` | Industry classification table |
| `references/scoring-rules.md` | Legacy scoring reference |
| `references/icp-summary.md` | Quick ICP reference |
| `references/image-analyzer.md` | Image analysis procedures |

### Local Reference Files

| File | Purpose |
|------|---------|
| `references/output-format.md` | Report template structure |
| `references/industry-taxonomy.md` | Industry classification table |
| `references/scoring-rules.md` | Legacy scoring reference |
| `references/icp-summary.md` | Quick ICP reference |
| `references/image-analyzer.md` | Image analysis procedures |

## Example Usage

**Single URL:**
```bash
# Navigate
playwright-cli open https://lan-security.de --persistent -s=inspector

# Snapshot output appears in Claude's context
playwright-cli snapshot -s=inspector

# Claude extracts, scores, and outputs full report
```

**Batch (optional):**
```bash
# Initialize session once
playwright-cli open about:blank --persistent -s=inspector

# Process each URL
playwright-cli goto https://example1.de -s=inspector
playwright-cli snapshot -s=inspector

playwright-cli goto https://example2.de -s=inspector
playwright-cli snapshot -s=inspector

# Cleanup (optional)
playwright-cli close-all -s=inspector
```

## Comparison: CLI vs MCP

| Aspect | MCP Version | Primary Implementation |
|--------|-------------|-------------|
| Navigation | `browser_navigate` | `playwright-cli goto` |
| Snapshot | `browser_snapshot` | `playwright-cli snapshot` |
| Extraction | Same (Claude reads YAML) | Same (Claude reads YAML) |
| Scoring | Same rules | Same rules |
| Output | Same format | Same format |
| Session | Per-call | Persistent (optional) |

**Use CLI when:**
- Processing multiple URLs in one session
- Need visual monitoring (`playwright-cli show`)
- Prefer CLI-based workflow

**Use MCP when:**
- Single URL inspection
- Prefer MCP tool integration
