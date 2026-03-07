# Output Format Template

Template for distributor inspection reports.

## Report Structure

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Industry:** {Industry Chinese} ({Industry English}) → {Sub-industry}
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

## Error Report Format

When inspection fails:

```markdown
## {url} - ERROR

**Error:** Navigation failed - {reason}

**Action:** Manual review required
```

## Channel Partner Potential Format

When company fails gates but has client overlap:

```markdown
### ⚠️ Channel Partner Potential

This company does not qualify as a traditional distributor, but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.

**Why this matters:** Their clients are potential end-users for cleaning robots. A partnership could provide warm introductions to facility decision-makers.
```