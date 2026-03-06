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

### Step 2: Scan for Classification Signals

From the snapshot, detect:

**Distributor Signals:**
- Product catalog / shop / e-commerce
- "Distributor", "Reseller", "Partner" language
- Multiple brand logos (footer, partners section)
- B2B pricing, wholesale mentions

**KA End-User Signals:**
- Facility locations (hotels, retail stores, hospitals)
- "Our locations", "Find a store", "Branches"
- Chain/multi-site indicators
- Operates physical properties

**Channel Partner Signals:**
- Client logos/testimonials
- "Who we serve", "Our clients"
- Case studies with named companies
- Service/consulting business model

**Exclusion Signals:**
- Pure B2C retail (no commercial products)
- Renovation/decoration focus
- Individual/freelancer
- Unrelated industry

### Step 3: Classify and Route

**Decision Tree:**

```
1. Sells physical products?
   YES → distributor-inspector
   
2. Operates facilities (hotels, retail, offices, etc.)?
   YES → ka-inspector
   
3. Has client relationships (logos, case studies)?
   YES → channel-partner-inspector
   
4. None of above?
   → exclude or end-client
```

**Confidence Levels:**
- HIGH: Clear signals present
- MEDIUM: Some signals, may need verification
- LOW: Weak signals, manual review suggested

### Step 4: Output Classification Result

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

### Example 4: Excluded

**URL:** home-decoration-shop.de

**Signals:**
- Pure B2C retail
- Home decoration products only
- No commercial/industrial products
- No B2B signals

**Classification:**
- Type: end-client
- Confidence: HIGH
- Route To: exclude
- Reason: Pure B2C retail, no commercial products

## Error Handling

### Navigation Failure

If website cannot be accessed:
```markdown
## {url} - ERROR

**Error:** Navigation failed - {reason}
**Action:** Manual review required
```

### Ambiguous Classification

If signals are mixed or unclear:
```markdown
## {company_name} - AMBIGUOUS

**Confidence:** LOW
**Possible Types:** {list 2-3 possibilities}
**Recommendation:** Manual review or try multiple inspectors
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
