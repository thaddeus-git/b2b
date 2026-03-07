---
name: lead-classifier
description: Quickly classify lead type from basic website info. Routes to correct inspector skill. Run BEFORE detailed inspection. Output: recommended inspector or exclude reason.
arguments:
  url:
    description: The URL of the website to classify (e.g., "company.com" or "https://company.com")
    required: true
    type: string
---

# Lead Classifier

Quickly determine lead type to route efficiently to the correct inspector skill.

## Overview

This skill performs a **30-second classification** to determine what type of lead this is, then routes to the appropriate inspector skill. This saves time by avoiding trial-and-error with multiple inspectors.

**Use BEFORE:**
- distributor-inspector
- ka-inspector
- channel-partner-inspector

## Prerequisites

```bash
# Install Playwright CLI (one-time)
npm install -g @playwright/cli@latest
```

## Process

### Step 1: Navigate and Capture

```bash
# Open browser and navigate
playwright-cli open {url} --persistent -s=classifier

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=classifier
```

### Step 2: Pre-Classification Exclusion Gates

**Before detailed analysis, check for quick exclusions:**

| Condition | Action | Reason |
|-----------|--------|--------|
| Website under construction | **exclude** | Insufficient information to classify |
| 403 Forbidden / bot blocked | **flag for manual** | Cannot access content |
| Domain not found / DNS error | **exclude** | Invalid lead |
| Timeout after 2 retries | **flag for manual** | Site performance issue |
| Personal email domain only (gmail, web.de, etc.) | **exclude** | Individual, not company |

**Output for quick exclusions:**
```markdown
## {url} - EXCLUDED

**Reason:** {under-construction / 403-error / invalid-domain / timeout}
**Action:** {Manual review recommended / Remove from list}
```

### Step 3: Check Industry Relevance

**Target industries for OrionStar cleaning robots:**
- ✅ Cleaning equipment / janitorial supplies
- ✅ Facility management / property management
- ✅ Hospitality (hotels, resorts, casinos)
- ✅ Retail (chains, supermarkets, malls)
- ✅ Healthcare (hospitals, clinics)
- ✅ Logistics (warehouses, distribution centers)
- ✅ Commercial real estate / offices

**Irrelevant industries (early exclude):**
- ❌ Construction / renovation (unless FM-related)
- ❌ Financial services / banking
- ❌ Legal / accounting
- ❌ Education (unless large campus FM)
- ❌ Pure software / IT services (no physical operations)
- ❌ Manufacturing (unless logistics/warehouse focus)

**Relevance decision:**
```
IF industry is target OR could be channel partner serving target industries
  → Continue to Step 4
ELSE
  → exclude with reason "Industry not relevant"
```

**Edge case - Service providers:**
If company provides services (security, HVAC, cleaning, IT) but doesn't sell products or operate facilities:
- Check for **client overlap** with target industries
- If clients include hospitality/retail/healthcare/FM → route to **channel-partner-inspector**
- If no client overlap → **exclude** (not relevant)

### Step 4: Scan for Classification Signals

From the snapshot, detect:

**Distributor Signals:**
- Product catalog / shop / e-commerce
- "Distributor", "Reseller", "Partner" language
- Multiple brand logos (footer, partners section)
- B2B pricing, wholesale mentions
- Shopping cart / checkout functionality

**KA End-User Signals:**
- Facility locations (hotels, retail stores, hospitals)
- "Our locations", "Find a store", "Branches"
- Chain/multi-site indicators
- Operates physical properties
- Booking/reservation system (for hospitality)

**Channel Partner Signals:**
- Client logos/testimonials
- "Who we serve", "Our clients"
- Case studies with named companies
- Service/consulting business model
- "Solutions provider", "Systems integrator" language

**Service Provider Signals (NEW):**
- Offers services, not products (security, HVAC, IT, consulting)
- "Dienstleistungen", "Services" prominent
- No product catalog or shop
- Project-based work descriptions
- Team page shows technicians/consultants, not sales

**Exclusion Signals:**
- Pure B2C retail (no commercial products)
- Renovation/decoration focus
- Individual/freelancer
- Unrelated industry
- No business contact info (only personal email)

### Step 5: Classify and Route

**Decision Tree (Updated):**

```
1. Quick exclusion triggered?
   YES → exclude with reason

2. Industry relevant OR has client overlap?
   NO → exclude "not relevant"

3. Sells physical products?
   YES → distributor-inspector

4. Operates facilities (hotels, retail, offices, etc.)?
   YES → ka-inspector

5. Has client relationships in target industries?
   YES → channel-partner-inspector

6. Service provider with NO client overlap?
   → exclude "not relevant"

7. None of above?
   → exclude "unclear business model"
```

**Confidence Levels:**
- HIGH: Clear signals present, unambiguous classification
- MEDIUM: Some signals present, may need verification
- LOW: Weak or mixed signals, manual review suggested

**When to search LinkedIn for verification:**
- Company size unclear (need to verify 20-500 employees)
- Team structure unknown
- Use: `python3 ../shared-scripts/serp_search.py --linkedin-company "{company_name}" "{country}" "en" "5"`

### Step 6: Output Classification Result

```markdown
## {company_name} - Classification

**URL:** {url}
**Type:** {distributor/ka-end-user/channel-partner/end-client}
**Confidence:** {HIGH/MEDIUM/LOW}
**Route To:** {skill-name or "exclude"}
**Reason:** {1-2 sentence explanation}

**Signals Detected:**
- {signal 1}
- {signal 2}
- {signal 3}

**Next Step:** Run `{skill-name}` skill for detailed inspection.
```

## Classification Examples

### Example 1: Distributor

**URL:** cleaning-equipment-de.de

**Signals:**
- Product catalog with multiple brands
- "Authorized distributor" badges
- B2B pricing visible
- Partner logos in footer

**Classification:**
- Type: distributor
- Confidence: HIGH
- Route To: distributor-inspector

### Example 2: KA End-User

**URL:** metro-hotel-chain.de

**Signals:**
- "25 locations across Germany"
- Hotel chain with multiple properties
- Facility management mentions
- No product sales

**Classification:**
- Type: ka-end-user
- Confidence: HIGH
- Route To: ka-inspector

### Example 3: Channel Partner

**URL:** facility-management-consulting.de

**Signals:**
- Client logos (Siemens, BMW, etc.)
- Case studies section
- "Who we serve" with industries
- Service-based business

**Classification:**
- Type: channel-partner
- Confidence: MEDIUM
- Route To: channel-partner-inspector

### Example 4: Excluded (Industry Not Relevant)

**URL:** frigosystem.de (HVAC/refrigeration service)

**Signals:**
- Service company (Kälte-Klima-Service)
- No product catalog
- ~7 employees (SMB)
- Industry: HVAC/refrigeration

**Classification:**
- Type: service-provider
- Confidence: HIGH
- Route To: exclude
- Reason: HVAC service company, no cleaning equipment, no client overlap with target industries

### Example 5: Excluded (Under Construction)

**URL:** philipps-neumuenster.de

**Signals:**
- "Unsere Webseite befindet sich im Aufbau"
- Minimal content
- No product/service information

**Classification:**
- Type: under-construction
- Confidence: HIGH
- Route To: exclude
- Reason: Website under construction, insufficient information

### Example 6: Excluded (Service Provider, No Client Overlap)

**URL:** bos-franken.de (Security services)

**Signals:**
- Security services company
- Multiple locations
- ISO certified
- No product sales
- No visible client overlap with hospitality/retail/healthcare

**Classification:**
- Type: service-provider
- Confidence: MEDIUM
- Route To: exclude
- Reason: Security services, no client overlap with target industries for cleaning robots
- **Note:** If they list clients in hospitality/retail, re-evaluate as channel-partner

## Error Handling

### Navigation Errors

| Error | Action | Output |
|-------|--------|--------|
| 403 Forbidden | Flag for manual review | `**Error:** 403 - Bot detection triggered` |
| Timeout | Retry once, then flag | `**Error:** Timeout after 2 attempts` |
| DNS failure | Exclude | `**Error:** Domain not found` |
| SSL certificate error | Exclude | `**Error:** SSL certificate invalid` |

**Output format for errors:**
```markdown
## {url} - ERROR

**Error:** {error_type} - {details}
**Action:** {Manual review required / Exclude from list}
```

### Ambiguous Classification

If signals are mixed or unclear:
```markdown
## {company_name} - AMBIGUOUS

**Confidence:** LOW
**Possible Types:** {list 2-3 possibilities}
**Recommendation:** Manual review or try multiple inspectors
```

### Known Issues

**403 Bot Detection:**
Some large websites (e.g., metro.de, amazon.de) block headless browsers. Workarounds:
- Try with different user-agent: `playwright-cli open {url} --user-agent="Mozilla/5.0..."`
- Flag for manual review if automated access fails
- Consider using residential proxies for high-value targets

**Cookie Modals:**
Always check for and dismiss cookie modals before capturing snapshot:
```bash
# Common cookie button selectors
[data-testid="cookie-accept"], .cookie-accept, #onetrust-accept-btn
```

## Integration with Other Skills

**After classification, invoke the appropriate skill:**

```
User: "Inspect cleaning-equipment-de.de"
Claude: [Runs lead-classifier]
Output: "Route to: distributor-inspector"
Claude: [Runs distributor-inspector]
Output: Full scored report
```

**Workflow time savings:**
- Before: 3-4 inspection attempts (180-240s)
- After: 1 classification + 1 inspection (90s)
- **50% faster**

## Batch Processing

For multiple URLs:

```bash
# Initialize session
playwright-cli open about:blank --persistent -s=classifier

# For each URL:
playwright-cli goto {url} -s=classifier
playwright-cli snapshot -s=classifier
# Claude classifies and outputs routing decision

# Cleanup
playwright-cli close-all -s=classifier
```
