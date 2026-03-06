# Cross-Routing Decision Matrix

Centralized routing logic for B2B lead inspection skills.

## Overview

This document provides the complete routing decision matrix for determining which inspector skill to use based on company signals detected during lead classification.

## Recommended Workflow

**Best Practice:** Run `lead-classifier` first (30s), then run the recommended inspector (60s).
**Total Time:** 90 seconds vs. 180-240 seconds for trial-and-error (50% faster)

## From lead-classifier

The lead-classifier skill performs initial 30-second classification to route efficiently.

| Signal Detected | Route To | Confidence |
|----------------|----------|------------|
| Sells physical products | distributor-inspector | HIGH |
| Operates facilities (hotels, retail, offices, etc.) | ka-inspector | HIGH |
| Client relationships (logos, case studies, testimonials) | channel-partner-inspector | MEDIUM |
| None of above | exclude or end-client | LOW |

## From distributor-inspector

**Condition:** Company evaluated as potential distributor/reseller

| Result | Route To | Reason |
|--------|----------|--------|
| Fails hard gates BUT has client overlap | channel-partner-inspector | Client relationships valuable despite not qualifying as distributor |
| Operates facilities themselves | ka-inspector | Could be end-user instead of reseller |
| Passes all checks | Final action | prioritize/standard/explore |

**Output Section:**
```markdown
### ⚠️ Channel Partner Potential

This company does not qualify as a traditional distributor, but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.

**Why this matters:** Their clients are potential end-users for cleaning robots. A partnership could provide warm introductions to facility decision-makers.
```

## From ka-inspector

**Condition:** Company evaluated as potential KA end-user

| Result | Route To | Reason |
|--------|----------|--------|
| Doesn't operate facilities BUT has client overlap | channel-partner-inspector | Service provider with clients, not end-user |
| Sells physical products | distributor-inspector | Could be distributor instead of end-user |
| Passes all checks | Final action | pilot-ready/nurture |

**Output Section:**
```markdown
### Channel Partner Potential

This company is not a direct end-user (doesn't operate facilities), but has **client overlap** with target segments:

**Detected Clients:** {list with segments}

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.
```

## From channel-partner-inspector

**Condition:** Company evaluated as potential channel partner

| Result | Route To | Reason |
|--------|----------|--------|
| Also sells physical products | distributor-inspector | Could be both distributor and channel partner |
| Operates facilities | ka-inspector | Could be end-user themselves |
| Passes all checks | Final action | prioritize/standard/explore |

**Cross-Routing Suggestion (in output):**
```markdown
### Cross-Routing Suggestion

**If sells physical products:** Consider re-inspecting with `distributor-inspector` to evaluate as distributor.

**If operates facilities:** Consider re-inspecting with `ka-inspector` to evaluate as end-user.
```

## Complete Routing Decision Tree

```
START: lead-classifier
  │
  ├─→ Sells products? ─YES→ distributor-inspector
  │     │
  │     ├─→ Fails gates + client overlap? ─YES→ channel-partner-inspector
  │     ├─→ Operates facilities? ─YES→ ka-inspector
  │     └─→ Passes checks ─→ Final action
  │
  ├─→ Operates facilities? ─YES→ ka-inspector
  │     │
  │     ├─→ No facilities + client overlap? ─YES→ channel-partner-inspector
  │     ├─→ Sells products? ─YES→ distributor-inspector
  │     └─→ Passes checks ─→ Final action
  │
  ├─→ Client relationships? ─YES→ channel-partner-inspector
  │     │
  │     ├─→ Sells products? ─YES→ distributor-inspector
  │     ├─→ Operates facilities? ─YES→ ka-inspector
  │     └─→ Passes checks ─→ Final action
  │
  └─→ None of above ─→ exclude or end-client
```

## Routing Signals Reference

### distributor-inspector Signals
- Product catalog / shop / e-commerce
- "Distributor", "Reseller", "Partner" language
- Multiple brand logos (footer, partners section)
- B2B pricing, wholesale mentions
- "Authorized Dealer" badges

### ka-inspector Signals
- Facility locations (hotels, retail stores, hospitals)
- "Our locations", "Find a store", "Branches"
- Chain/multi-site indicators
- Operates physical properties
- Facility management mentions

### channel-partner-inspector Signals
- Client logos/testimonials
- "Who we serve", "Our clients"
- Case studies with named companies
- Service/consulting business model
- Solution provider/integrator language

### Exclude Signals
- Pure B2C retail (no commercial products)
- Renovation/decoration focus
- Individual/freelancer
- Unrelated industry
- No B2B signals

## Efficiency Comparison

**Before (Sequential Trial):**
```
Try distributor-inspector (60s) → fail
Try ka-inspector (60s) → fail
Try channel-partner-inspector (60s) → fail
Total: 180-240s
```

**After (Classify First):**
```
Run lead-classifier (30s) → route to ka-inspector
Run ka-inspector (60s) → score
Total: 90s
```

**Result: 50% time savings**

## Implementation in Skills

Each inspector skill should reference this document in their routing section:

```markdown
### Cross-Routing

**See:** `../shared-references/cross-routing.md` for complete routing decision matrix
```

## When to Cross-Route

**Always cross-route when:**
1. Primary classification fails but valuable signal detected
2. Multiple business models present (e.g., sells products AND operates facilities)
3. Client overlap detected with target segments

**Never cross-route when:**
1. Clear exclusion signals present
2. No additional value in alternative classification
3. Company clearly fits one inspector only

## Notes

- Cross-routing is a **recommendation**, not automatic
- Human review may be needed for ambiguous cases
- Some companies may qualify for multiple inspectors (run both)
- Always document routing rationale in output
