# Channel Partner Inspector - Design Document

> **Created:** 2026-03-03
> **Status:** Approved
> **Related:** distributor-inspector, ka-inspector

---

## Overview

### Purpose

Evaluate companies as potential **channel partners** - companies that don't distribute physical products but have relationships with end-users in target segments.

### Problem Statement

Current skills only handle two types:
- **Distributors** - Buy and resell physical products
- **Key Accounts (KA)** - Buy and use directly

But there's a third type that gets excluded incorrectly:
- **Channel Partners** - Have client relationships with potential end-users, but sell different products (software, services, etc.)

Example: Valer (healthcare IT company) has deep relationships with hospitals (OHSU, Keck Medicine) that need cleaning robots, but gets excluded because they sell SaaS, not physical products.

### Solution

Create a new `channel-partner-inspector` skill that:
1. Detects client overlap with target segments
2. Scores based on relationship depth, not logistics capability
3. Provides cross-routing to/from existing skills

---

## Skill Design

### Target Profile

| Type | What they sell | What they have | Value |
|------|---------------|----------------|-------|
| Software companies | POS, EHR, property management systems | Client relationships | Warm introductions |
| Service providers | Consulting, FM services | Trusted advisor status | Credibility |
| Industry associations | Membership, certifications | Network access | Market reach |
| Technology vendors | IoT, building systems | Existing integrations | Bundle opportunities |

### Target Client Segments

| Segment | Examples | Cleaning Robot Potential |
|---------|----------|-------------------------|
| Healthcare | Hospitals, medical centers, clinics | HIGH - large facilities, 24/7 |
| Retail | Chains, supermarkets, drug stores | HIGH - many locations |
| Hospitality | Hotels, resorts, casinos | HIGH - guest areas |
| Property/FM | Property management, facility management | HIGH - multiple buildings |
| Logistics | Distribution centers, fulfillment | MEDIUM - large floors |
| Education | Universities, schools | MEDIUM - campuses |
| Government | Public buildings, municipal | MEDIUM - varied |

---

## Hard Gates

### Primary Gate: Client Overlap

| Gate | Requirement | Detection |
|------|-------------|-----------|
| **Client Overlap** | Has named clients in target segments | Client logos, case studies, testimonials, "who we serve" |

**Detection Sources:**
- Client logos in footer/homepage
- Case studies / success stories
- Testimonials with company names
- "Who we serve" / "Our clients" pages
- Named references in content

**Gate Result:**
- **PASS** → Named clients in target segments → Continue scoring
- **FAIL** → No client overlap → Exclude or cross-route

---

## Scoring Criteria

### Base Score
- **60 points** if client overlap gate passes

### Bonus Scoring

| Component | Max Points | Criteria |
|-----------|------------|----------|
| **Client Quantity** | +20 | 1-10: +5, 11-50: +10, 51-200: +15, 200+: +20 |
| **Client Quality (KA)** | +15 | Named enterprise/recognizable brands |
| **Sales Capability** | +10 | Has sales/BD/account managers |
| **Trust/Relationship Depth** | +10 | Long-term clients, case studies, "partnership" language |
| **Geographic Reach** | +10 | Multi-region/multi-state/international clients |
| **Industry Expertise** | +5 | Specialized in target industry |
| **Partnership History** | +5 | Previous co-marketing, integrations, referrals |
| **Financial Stability** | +5 | PE backed, profitable, 5+ years established |

**Total Cap:** 100 points

### Grades & Actions

| Score | Grade | Action |
|-------|-------|--------|
| 80-100 | A | `prioritize` - Strong partner, route to BD |
| 60-79 | B | `standard` - Viable partner, explore |
| 40-59 | C | `explore` - Potential, nurture |
| <40 | D/F | `exclude` - Not a fit |

---

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

---

## Cross-Routing Design

### FROM distributor-inspector

**Trigger:** Company fails hard gates (no physical distribution) BUT has client overlap

**Detection:**
```
IF gate_result == "MOST_FAIL" AND has_named_clients_in_target_segments:
    ADD "⚠️ Channel Partner Potential" section
    SUGGEST: "Re-inspect with channel-partner-inspector"
```

**Output Addition:**
```markdown
### ⚠️ Channel Partner Potential

This company does not qualify as a traditional distributor, but has **client overlap** with target segments:

**Detected Clients:** OHSU (Healthcare), Keck Medicine USC (Healthcare)

**Recommendation:** Re-inspect with `channel-partner-inspector` to evaluate as a referral partner.
```

### FROM ka-inspector

**Trigger:** Company doesn't operate facilities BUT has client overlap

**Detection:**
```
IF no_facilities_operated AND has_named_clients_in_target_segments:
    ADD "⚠️ Channel Partner Potential" section
    SUGGEST: "Re-inspect with channel-partner-inspector"
```

### TO distributor-inspector

**Trigger:** Channel partner also sells physical products

### TO ka-inspector

**Trigger:** Channel partner also operates facilities themselves

---

## File Structure

### Proposed Unified Structure

```
skills/
├── _shared/                          # SHARED across all skills
│   ├── country-strategies.md         # All markets (35+ countries)
│   ├── target-segments.md            # Healthcare, retail, hospitality, etc.
│   ├── exclusion-rules.md            # Universal exclusions
│   ├── competing-brands.md           # Competitor brands
│   ├── tags.md                       # Tag taxonomy
│   └── keywords.md                   # Product/service keywords
│
├── distributor-inspector/
│   ├── SKILL.md
│   ├── references/
│   │   ├── hard-gates.md             # Physical distribution gates
│   │   ├── scoring-matrix.md         # Distributor scoring
│   │   ├── company-profiler.md
│   │   └── contact-extractor.md
│   └── scripts/
│
├── ka-inspector/
│   ├── SKILL.md
│   ├── references/
│   │   ├── hard-gates.md             # Facility ownership gates
│   │   ├── scoring-matrix.md         # KA scoring
│   │   └── site-potential-rules.md
│   └── scripts/
│
├── channel-partner-inspector/        # NEW
│   ├── SKILL.md
│   ├── references/
│   │   ├── hard-gates.md             # Client overlap gate
│   │   ├── scoring-matrix.md         # Channel partner scoring
│   │   └── client-detection.md       # How to extract client lists
│   └── scripts/
│
└── lead-enricher/
    ├── SKILL.md
    └── references/
```

### Key Principles

1. **`_shared/`** = One source of truth for shared resources
2. **Each skill owns its logic** = hard-gates, scoring-matrix are skill-specific
3. **Cross-routing in SKILL.md** = Each skill defines when to route elsewhere
4. **No duplication** = Shared files referenced, not copied

---

## Implementation Tasks

### Phase 1: Restructure Shared Resources
1. Create `skills/_shared/` directory
2. Consolidate `country-strategies.md` (use updated global version)
3. Create `target-segments.md` from existing content
4. Move shared files, update references in existing skills

### Phase 2: Create channel-partner-inspector
1. Create skill directory structure
2. Write `SKILL.md` with full process
3. Create reference files:
   - `hard-gates.md` - Client overlap detection
   - `scoring-matrix.md` - Channel partner scoring
   - `client-detection.md` - How to extract client lists

### Phase 3: Add Cross-Routing
1. Update `distributor-inspector/SKILL.md` with channel partner routing
2. Update `ka-inspector/SKILL.md` with channel partner routing
3. Update `channel-partner-inspector/SKILL.md` with reverse routing

### Phase 4: Testing
1. Test Valer.health with all three skills
2. Verify cross-routing suggestions appear correctly
3. Verify scoring produces expected results

---

## Success Criteria

1. **Valer.health** routes correctly:
   - distributor-inspector → excludes but suggests channel-partner-inspector
   - channel-partner-inspector → scores 70-85 based on hospital clients

2. **No duplication:** Shared files exist in one place only

3. **Consistent updates:** Changing `country-strategies.md` affects all skills

4. **Clear cross-routing:** Each skill explicitly defines when to route elsewhere
