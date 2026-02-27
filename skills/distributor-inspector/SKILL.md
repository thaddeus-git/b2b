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

# Configure Bright Data SERP API (required for LinkedIn lookup)
# Run from the distributor-inspector skill directory:
python3 scripts/setup.py
# Then edit ~/.claude/distributor-inspector/config.json and add your Bright Data API key
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

**Image analysis delegation:** `references/image-analyzer.md`

## Process

### Step 1: Navigate and Capture

**For single URL:**
```bash
# Open browser and navigate
playwright-cli open {url} --persistent -s=inspector

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=inspector

# Deep mode: Capture screenshots for image analysis
if mode == "deep":
  playwright-cli screenshot -s=inspector --full-page home.png
  playwright-cli goto {url}/team -s=inspector 2>/dev/null || playwright-cli goto {url}/about -s=inspector 2>/dev/null
  playwright-cli screenshot -s=inspector --full-page team.png
```

**For batch (persistent session):**
```bash
# Initialize session
playwright-cli open about:blank --persistent -s=inspector

# For each URL:
playwright-cli goto {url} -s=inspector
playwright-cli snapshot -s=inspector

# Deep mode: capture screenshots after each snapshot
if mode == "deep":
  playwright-cli screenshot -s=inspector --full-page home.png
  playwright-cli goto {url}/team -s=inspector 2>/dev/null || playwright-cli goto {url}/about -s=inspector 2>/dev/null
  playwright-cli screenshot -s=inspector --full-page team.png
```

### Step 2: Extract Company Profile

**Delegate to:** `references/company-profiler.md`

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

**Delegate to:** `references/image-analyzer.md`

From captured screenshots (`home.png`, `team.png`):
1. **Team photos** - Count faces, estimate employee count
2. **Brand logos** - Detect Pudu, Gausium, LionsBot, Tennant, etc.
3. **Certifications** - Detect ISO badges, "Authorized Dealer" badges

Add findings to the report under "### Deep Mode Analysis" section.

**If no images captured or analysis fails:** Include "Not analyzed (image capture failed)" in Deep Mode Analysis section.

### Step 3: Extract Contact Information

**Delegate to:** `references/contact-extractor.md`

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
python3 scripts/search.py "{company_name} linkedin" "{country}" "{language}" "5"
```

Parse the JSON output and extract the LinkedIn URL from the first matching result.

If the script fails (missing dependency, API key error, etc.), report "Not found (searched)" and continue.

### Step 4: Categorize

**Delegate to:** `references/tags.md`

Apply tags using format: `{category}-{business-model}`

Multiple tags allowed per company.

**Special tags:**
- `competitor-robot-distributor` - Sells Pudu/Gausium/LionsBot/etc.
- `pure-2c-retail` - B2C only (check for commercial products exception)
- `cleaning-services-provider` - Contract cleaning services
- `hospitality-service-provider` - Hotel chains, hospitality groups

### Step 4.5: Classify Company Scale (NEW - CRITICAL)

**Delegate to:** `references/smb-classifier.md`

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

**Delegate to:** `references/icp-sales/hard-gates.md` and `references/icp-skill/gate-translation.md`

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

**Delegate to:** `references/icp-skill/scoring-matrix.md`

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
- France (FR): Competitor footprint +10 bonus
- Spain (ES): After-sales maturity +10 bonus
- Germany (DE): System integration +10 bonus

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

## Output Format

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Classification:** {SMB | MID-MARKET | KA}
**Action:** {action}
**Play:** {play} (optional - only if competitor footprint detected)

### Company Profile

**Products:**
{list of products}

**Services:**
{list of services}

**Brands:**
{brands carried}

**Geography:**
{geographic coverage}

**Team:**
{team info}

**SLA:**
{SLA mentions or "None detected"}

### Deep Mode Analysis (if mode="deep")

**Team Photos:**
{analysis results or "Not analyzed (standard mode)"}

**Logo Detection:**
{analysis results or "Not analyzed (standard mode)"}

**Certifications:**
{analysis results or "Not analyzed (standard mode)"}

### Contact

**Phone:** {phone}
**Email:** {email}
**Headquarters:** {city}, {region}, {country}
**Address:** {full address or "Not found"}
**Additional Locations:** {count} offices/branches (list if found) or "Single location"
**WhatsApp:** {whatsapp_number or "Not found"}
**Website:** {main website or "Same as URL"}
**LinkedIn:** {linkedin_url or "Not found (searched)"}
**Additional Channels:** {youtube, twitter, facebook, instagram, etc. or "None detected"}

### Key Signals

{bullet list of notable signals}

### Classification

| Criterion | Value | Signal |
|-----------|-------|--------|
| Employees | {count or "Unknown"} | {SMB/MID-MARKET/KA signal} |
| Locations | {count} | {SMB/MID-MARKET/KA signal} |
| Structure | {description} | {SMB/MID-MARKET/KA signal} |

**Classification:** {SMB | MID-MARKET | KA}
**Confidence:** {HIGH | MEDIUM | LOW}
**Score Cap:** {50 | 75 | 100}
**Rationale:** {brief explanation of classification decision}

### Hard Gates Evaluation

| Gate | Result | Evidence |
|------|--------|----------|
| Company Size (20-500 emp) | {PASS/FAIL/UNCLEAR} | {evidence} |
| Team Capability (3 functions) | {PASS/FAIL/UNCLEAR} | {evidence} |
| SLA Capability | {PASS/FAIL/UNCLEAR} | {evidence} |
| PoC Capability | {PASS/FAIL/UNCLEAR} | {evidence} |
| Market Coverage | {PASS/FAIL/UNCLEAR} | {evidence} |
| Price Discipline | {PASS/FAIL/UNCLEAR} | {evidence} |

**Gate Result:** {ALL_PASS / SOME_FAIL (1-2) / MOST_FAIL (3+)} → {Eligible for A/B / Capped at 50 / Exclude}

### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Base score | {qualified/partial/unqualified} | {base} |
| Cleaning equipment | {level with evidence} | +{bonus} |
| Competitor footprint | {tier with evidence} | +{bonus} |
| Distribution network | {signals} | +{bonus} |
| System integration | {signals} | +{bonus} |
| FM/property customers | {categories} | +{bonus} |
| After-sales maturity | {signals} | +{bonus} |
| Demo capability | {signals} | +{bonus} |
| Marketing investment | {signals} | +{bonus} |
| Customer overlap | {categories} | +{bonus} |
| Country adjustment | {country} | +{adjustment} |
| **Raw Total** | | **{raw_total}** |
| **Cap Applied** | ({classification} + {gate_result}) | **{cap}** |
| **Final Score** | (capped at {cap}) | **{total}** |

### Sales Play (if applicable)

{play_name}: {play_description}

### Summary

{2-3 sentence summary}

### ⚠️ Manual Review Suggested (if applicable)

**Only include this section if:** Company routes to `exclude` BUT has named enterprise clients in target segments.

```markdown
**Named Enterprise Clients:**
- {Client Name} ({segment}) - Target segment
- {Client Name} ({segment}) - Target segment

**Potential Value:** This company has relationships with enterprises in your target segments. Consider manual outreach to explore referral partnership opportunities.

**Gate Failure Summary:** Excluded due to: {failed gates}
```

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

## Configuration Files

### ICP Reference Files (New Structure)

| File | Purpose |
|------|---------|
| `references/icp-summary.md` | Quick reference for sales team + AI |
| `references/icp-sales/hard-gates.md` | Hard qualification gates |
| `references/icp-sales/bonus-criteria.md` | Bonus criteria from sales ICP |
| `references/icp-sales/target-industries.md` | Target industry list |
| `references/icp-sales/exclusion-rules.md` | Exclusion criteria |
| `references/icp-sales/country-strategies.md` | FR/ES/DE/HU/CH/GR strategies |
| `references/icp-skill/gate-translation.md` | How AI interprets each gate |
| `references/icp-skill/scoring-matrix.md` | Complete bonus scoring matrix |
| `references/icp-skill/customer-overlap-rules.md` | Explicit customer overlap scoring |

### Legacy Files (Preserved)

| File | Purpose |
|------|---------|
| `references/tags.md` | Niche market tag taxonomy |
| `references/scoring-rules.md` | Legacy scoring rules (superseded) |
| `references/keywords.md` | Product/service keywords by industry |
| `references/competing-brands.md` | Competitor brands to detect |
| `references/company-profiler.md` | Company profile extraction |
| `references/contact-extractor.md` | Contact information extraction |

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
