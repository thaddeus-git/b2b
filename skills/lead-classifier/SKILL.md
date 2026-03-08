---
name: lead-classifier
description: Quickly classify lead type from basic website info. Outputs industry classification (primary_industry + secondary_industry) and routes to correct inspector skill. Run BEFORE detailed inspection. Ideal for CRM data prep.
arguments:
  url:
    description: The URL of the website to classify (e.g., "company.com" or "https://company.com")
    required: true
    type: string
---

# Lead Classifier

Quickly determine lead type to route efficiently to the correct inspector skill.

## Quick Start (For Agents)

**What this skill does:**
1. Reads a website snapshot
2. Classifies the company into a fixed industry taxonomy
3. Routes to the correct inspector skill
4. Outputs CRM-ready fields

**Input:** URL (e.g., "metro.de" or "https://metro.de")

**Important: Do you have a URL?**

| If you have... | Do this first | Then use lead-classifier |
|----------------|---------------|-------------------------|
| **Website URL** | Nothing - you're ready! | ✅ Run lead-classifier |
| **Company name only** | Run lead-enricher to find website | ✅ Then classify |
| **Email address** | Run lead-enricher to find website | ✅ Then classify |
| **CSV with names, companies, emails** | Run lead-enricher on CSV | ✅ Then classify each URL |
| **Person name + company** | Run lead-enricher to find website + LinkedIn | ✅ Then classify |

**Example workflows:**

```
# Scenario 1: User has URL
User: "Classify metro.de"
→ Run: lead-classifier with url="metro.de"

# Scenario 2: User has company name only
User: "Classify Real Supermarkt GmbH"
→ Run: lead-enricher first (or search for website)
→ Then: lead-classifier with the found URL

# Scenario 3: User has CSV lead list
User: "I have 50 leads in leads.csv"
→ Run: lead-enricher scripts/enrich.py leads.csv
→ Then: lead-classifier on each website URL found
```

**Output:**
```markdown
## Company Name - Classification

**URL:** {url}
**Country:** {detected country}
**Type:** {distributor/ka-end-user/channel-partner}
**Confidence:** {HIGH/MEDIUM/LOW}
**Route To:** {skill-name}

**Industry Classification:**
- Primary Industry: 商超 (Retail)
- Secondary Industry: 商超终端方向-KA

**Next Step:** Run `ka-inspector` skill
```

**CRM Fields (copy these):**
- `primary_industry`: The industry category (Chinese + English)
- `secondary_industry`: The sub-industry (Chinese)
- `lead_type`: Business model (distributor/ka-end-user/channel-partner)

**What this skill does NOT do:**
- Does NOT perform deep evaluation (use inspector skills for that)
- Does NOT insert data into CRM (manual step)
- Does NOT enrich leads with website URLs (use lead-enricher first)

---

## Overview

This skill performs a **30-second classification** to determine:
1. **Lead type**: distributor, ka-end-user, channel-partner, or exclude
2. **Industry classification**: Primary and secondary industry from fixed taxonomy (for CRM)
3. **Routing**: Which inspector skill to run next

**Output fields for CRM:**
- `primary_industry`: Industry category (e.g., `商超 (Retail)`)
- `secondary_industry`: Sub-industry (e.g., `商超终端方向-KA`)
- `lead_type`: Business model classification
- `route_to`: Recommended next action

**Workflow position:**
```
lead-enricher (finds websites)
    ↓
lead-classifier (this skill) → CRM industry fields
    ↓
inspector skills (deep evaluation)
```

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

### Step 5.5: Assign Industry Classification

**After determining the lead type, assign the industry classification from the fixed taxonomy.**

**Delegate to:** `../shared-references/industry-taxonomy.md`

**Confidence Levels:**
- HIGH: Clear signals present, unambiguous classification
- MEDIUM: Some signals present, may need verification
- LOW: Weak or mixed signals, manual review suggested

**When to search LinkedIn for verification:**
- Company size unclear (need to verify 20-500 employees)
- Team structure unknown
- Use: `python3 ../shared-scripts/serp_search.py --linkedin-company "{company_name}" "{country}" "en" "5"`

### Step 6: Output Classification Result

**Handling Missing URL:**

If the user provides company name, email, or person info but NO website URL:

```markdown
**Response:**
"I need a website URL to run lead-classifier.

Based on your input, here's what to do first:

| You provided | Run this first | Then I can classify |
|--------------|----------------|---------------------|
| Company name only | `lead-enricher` or search for website | ✅ |
| Email address | `lead-enricher` (finds website from email domain) | ✅ |
| Person name + company | `lead-enricher` (finds website + LinkedIn) | ✅ |
| CSV with leads | `lead-enricher` batch mode | ✅ |

Would you like me to help run lead-enricher first?"
```

**Once you have the URL, proceed with classification.**

```markdown
## {company_name} - Classification

**URL:** {url}
**Country:** {detected country}
**Type:** {distributor/ka-end-user/channel-partner/end-client}
**Confidence:** {HIGH/MEDIUM/LOW}
**Route To:** {skill-name or "exclude"}
**Reason:** {1-2 sentence explanation}

**Industry Classification:**
- Primary Industry: {行业 Chinese} ({English})
- Secondary Industry: {Sub-industry Chinese}

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
- Primary Industry: 清洁 (Cleaning)
- Secondary Industry: 清洁代理商 - 机械类

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
- Primary Industry: 酒店 (Hospitality)
- Secondary Industry: 酒店终端方向-KA

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
- Primary Industry: 服务行业 (Services)
- Secondary Industry: 服务代理商

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
- Primary Industry: 弱相关 /不相关 (Unrelated)
- Secondary Industry: 无二级行业
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
- Primary Industry: 弱相关 /不相关 (Unrelated)
- Secondary Industry: 无二级行业
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
- Primary Industry: 弱相关 /不相关 (Unrelated)
- Secondary Industry: 无二级行业
- Reason: Security services, no client overlap with target industries for cleaning robots
- **Note:** If they list clients in hospitality/retail, re-evaluate as channel-partner

### Example 7: Supermarket/Retail (商超)

**URL:** real-supermarket-kette.de

**Signals:**
- "50+ Märkte in Deutschland"
- Online shop with B2B pricing
- Commercial/wholesale section
- Fresh food, groceries, household products

**Classification:**
- Type: ka-end-user
- Confidence: HIGH
- Route To: ka-inspector
- Primary Industry: 商超 (Retail)
- Secondary Industry: 商超终端方向-KA

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

**Complete Workflow:**

```
Step 1: lead-enricher
  └─> Input: CSV with names, companies, emails
  └─> Output: CSV with website URLs, LinkedIn, contacts

Step 2: lead-classifier (this skill)
  └─> Input: URL from enriched CSV
  └─> Output: Industry classification + routing decision

Step 3: Appropriate inspector (distributor/ka/channel-partner)
  └─> Input: URL + classification data
  └─> Output: Scored report with action recommendation

Step 4: CRM insertion (MANUAL - not part of skill set)
  └─> User copies classification output to CRM
  └─> CRM fields: primary_industry, secondary_industry, lead_type, website, etc.
```

**Example Flow:**

```
User: "Classify metro.de"
Claude: [Runs lead-classifier]
Output:
  - Type: ka-end-user
  - Primary Industry: 商超 (Retail)
  - Secondary Industry: 商超终端方向-KA
  - Route To: ka-inspector

User: "Now inspect it"
Claude: [Runs ka-inspector]
Output: Full scored report with action recommendation

User: [Manually copies industry fields to CRM]
```

**Workflow time savings:**
- Before: 3-4 inspection attempts (180-240s)
- After: 1 classification + 1 inspection (90s)
- **50% faster**

**CRM Field Mapping:**

| CRM Field | Source |
|-----------|--------|
| `primary_industry` | lead-classifier output |
| `secondary_industry` | lead-classifier output |
| `website` | lead-enricher output |
| `company_linkedin` | lead-enricher output |
| `lead_type` | lead-classifier output (distributor/ka/channel-partner) |
| `classification_confidence` | lead-classifier output |

## Batch Processing

### Option 1: Individual URL Classification

```bash
# Initialize session
playwright-cli open about:blank --persistent -s=classifier

# For each URL:
playwright-cli goto {url} -s=classifier
playwright-cli snapshot -s=classifier
# Claude classifies and outputs routing decision + industry classification

# Cleanup
playwright-cli close-all -s=classifier
```

### Option 2: CSV Batch Workflow (Recommended for CRM)

```bash
# Step 1: Enrich CSV with lead-enricher
python3 ../lead-enricher/scripts/enrich.py leads.csv leads_enriched.csv

# Step 2: Classify each URL (batch script or manual)
# For each website in leads_enriched.csv:
playwright-cli open {website} --persistent -s=classifier
playwright-cli snapshot -s=classifier
# Claude outputs: primary_industry, secondary_industry, route_to

# Step 3: Consolidate results for CRM
# Combine lead-enricher + lead-classifier outputs
# CRM-ready CSV columns:
#   full_name, company_name, website, company_linkedin,
#   primary_industry, secondary_industry, lead_type, route_to, confidence
```

### Option 3: Persistent Session for High Volume

```bash
# Start persistent session
playwright-cli open about:blank --persistent -s=classifier

# Process URLs in sequence (Claude maintains context)
goto url1 → snapshot → classify → goto url2 → snapshot → classify → ...

# Session preserves learned patterns for faster classification
```
