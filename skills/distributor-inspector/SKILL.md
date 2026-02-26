---
name: distributor-inspector
description: Use when evaluating websites as potential distributors for OrientStar Robotics (cleaning robots). Uses Playwright CLI for navigation. Same extraction/scoring as MCP version.
---

# Distributor Inspector (Primary Implementation)

Inspect and score potential distributor websites using Playwright CLI for navigation.

## Overview

This skill is **functionally identical** to `distributor-inspector` (MCP version), but uses `playwright-cli` commands instead of MCP tools for website navigation. Same extraction, same scoring, same report format.

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
playwright-cli open {url} --persistent -s=inspector

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=inspector
```

**For batch (persistent session):**
```bash
# Initialize session
playwright-cli open about:blank --persistent -s=inspector

# For each URL:
playwright-cli goto {url} -s=inspector
playwright-cli snapshot -s=inspector
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

If LinkedIn not found on website, use the Skill tool to invoke `google-search`:
```
Search: "{company_name} linkedin" in detected country/language
```

Report: URL if found, or "Not found (searched)"

### Step 4: Categorize

**Delegate to:** `references/tags.md`

Apply tags using format: `{category}-{business-model}`

Multiple tags allowed per company.

**Special tags:**
- `competitor-robot-distributor` - Sells Pudu/Gausium/LionsBot/etc.
- `pure-2c-retail` - B2C only (check for commercial products exception)
- `cleaning-services-provider` - Contract cleaning services
- `hospitality-service-provider` - Hotel chains, hospitality groups

### Step 5: Score

**Delegate to:** `references/scoring-rules.md`

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL (informational) |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

**Total capped at 100**

**Commercial Products Pre-Check:**

Before scoring, check if company has commercial products:
- If tagged `pure-2c-retail` AND NO commercial products → Route to `exclude`
- If tagged `pure-2c-retail` BUT has commercial products → Score normally

Commercial product signals: cleaning equipment, facility management, janitorial supplies, robotics/automation, B2B/wholesale.

### Step 6: Route

| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90+ | PASS gate | prioritize |
| B | 70-89 | PASS gate | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |
| — | — | Tier 1-2 competitor | route-to-sales |
| — | — | cleaning-services-provider | service-provider-prospect |
| — | — | hospitality-service-provider | route-to-ka |

**Special routing (overrides score):**
- Tagged `pure-2c-retail` with NO commercial products: `exclude`
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

## Output Format

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
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

### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | {pass/fail with reason} | — |
| Customer overlap bonus | {level with evidence} | +{bonus} |
| Cleaning equipment bonus | {level with evidence} | +{bonus} |
| Competitor footprint bonus | {tier with evidence} | +{bonus} |
| Channel capability bonus | {signals detected} | +{bonus} |
| **Total** | (capped at 100) | **{total}** |

### Sales Play (if applicable)

{play_name}: {play_description}

### Summary

{2-3 sentence summary}
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

| File | Purpose |
|------|---------|
| `references/keywords.md` | Product/service keywords by industry |
| `references/tags.md` | Niche market tag taxonomy |
| `references/competing-brands.md` | Competitor brands to detect |
| `references/company-profiler.md` | Company profile extraction |
| `references/contact-extractor.md` | Contact information extraction |
| `references/scoring-rules.md` | Scoring rules and bonus calculations |

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
