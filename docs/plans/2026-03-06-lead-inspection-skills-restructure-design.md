# Lead Inspection Skills Restructure - Design Document

**Date**: 2026-03-06
**Status**: Approved
**Goal**: Restructure lead inspection skills to follow Agent Skills best practices

---

## Problem Statement

Current structure has several issues:

1. **Duplication** - ICP reference files duplicated across `distributor-inspector` and `ka-inspector`
2. **Two shared directories** - `skills/shared/` (Python) and `skills/_shared/` (markdown)
3. **Deep nesting** - `references/icp-sales/...` violates "one level deep" best practice
4. **Inefficient routing** - Sequential trial of inspector skills wastes time
5. **Redundant scripts** - `search.py` duplicated, `setup.py` scripts unnecessary

---

## Design Goals

1. Follow Agent Skills specification (flat structure, <500 lines per SKILL.md)
2. Eliminate duplication (DRY principle)
3. Improve routing efficiency (classify first, inspect once)
4. Simplify maintenance (single source of truth)
5. Clear separation of concerns

---

## Solution Overview

### 1. New lead-classifier Skill

**Purpose**: Quickly classify lead type and route to correct inspector

**Benefits**:
- 50% time savings (classify in 30s, inspect once in 60s vs trying 3-4 inspectors)
- Clear decision logic
- Prevents unnecessary inspections

**Classification Logic**:
```
Sells products? → distributor-inspector
Operates facilities? → ka-inspector
Has client relationships? → channel-partner-inspector
None of above → exclude or end-client
```

### 2. Consolidated Shared Resources

**shared-references/** - All shared markdown documentation:
- `icp/` - Hard gates, bonus criteria, scoring matrices
- `country-strategies.md`, `target-segments.md`
- `cross-routing.md` - Extracted routing logic
- `image-analysis-guide.md` - Consolidated image guidance
- Other reference files

**shared-scripts/** - All shared Python utilities:
- `brightdata_utils.py` - API key management
- `serp_search.py` - Unified SERP search utility

### 3. Flattened Reference Structure

**Before**: `references/icp-sales/hard-gates.md` (nested)
**After**: `../shared-references/icp/hard-gates.md` (flat, shared)

### 4. Eliminated Redundancy

**Removed**:
- Duplicate `icp-sales/` and `icp-skill/` directories
- Duplicate `search.py` scripts
- All `setup.py` scripts (document in SKILL.md instead)
- Duplicate `image-analyzer.md` files

**Consolidated**:
- Single shared config: `~/.claude/config.json`
- Single search utility: `shared-scripts/serp_search.py`
- Single image guide: `shared-references/image-analysis-guide.md`

---

## New Directory Structure

```
skills/
├── lead-classifier/                    # NEW: Routes to correct inspector
│   └── SKILL.md
│
├── shared-references/                  # All shared markdown
│   ├── icp/
│   │   ├── hard-gates.md
│   │   ├── bonus-criteria.md
│   │   ├── target-industries.md
│   │   ├── exclusion-rules.md
│   │   ├── gate-translation.md
│   │   ├── scoring-matrix.md
│   │   ├── customer-overlap-rules.md
│   │   └── site-potential-rules.md
│   ├── country-strategies.md
│   ├── target-segments.md
│   ├── cross-routing.md
│   ├── image-analysis-guide.md
│   ├── company-profiler.md
│   ├── contact-extractor.md
│   ├── competing-brands.md
│   ├── keywords.md
│   ├── tags.md
│   ├── smb-classifier.md
│   └── confidence-scoring.md
│
├── shared-scripts/                     # Python utilities
│   ├── __init__.py
│   ├── brightdata_utils.py
│   ├── serp_search.py
│   └── pyproject.toml
│
├── distributor-inspector/
│   └── SKILL.md
│
├── ka-inspector/
│   └── SKILL.md
│
├── channel-partner-inspector/
│   ├── SKILL.md
│   └── references/
│       ├── client-detection.md
│       └── scoring-matrix.md
│
└── lead-enricher/
    └── SKILL.md
```

---

## Workflow Comparison

### Before (Inefficient)

```
User: "Inspect company.com"
Agent: Run distributor-inspector (60s) → fails
Agent: Run ka-inspector (60s) → fails  
Agent: Run channel-partner-inspector (60s) → fails
Agent: Exclude
Total: 3-4 inspections (180-240s)
```

### After (Efficient)

```
User: "Inspect company.com"
Agent: Run lead-classifier (30s) → "Route to: ka-inspector"
Agent: Run ka-inspector (60s) → Score & route
Total: 1 classification + 1 inspection (90s)
```

**50% time savings**

---

## Migration Plan

### Phase 1: Create Shared Structure
- Create `skills/shared-references/` and `skills/shared-references/icp/`
- Create `skills/shared-scripts/`
- Move `skills/_shared/*` to `skills/shared-references/`
- Rename `skills/shared/` to `skills/shared-scripts/`

### Phase 2: Create lead-classifier Skill
- Create `skills/lead-classifier/SKILL.md`
- Implement classification logic
- Test routing decisions

### Phase 3: Consolidate ICP Files
- Move `distributor-inspector/references/icp-sales/*` to `shared-references/icp/`
- Move `distributor-inspector/references/icp-skill/*` to `shared-references/icp/`
- Delete duplicate `ka-inspector/references/icp-sales/`
- Delete duplicate `ka-inspector/references/icp-skill/`

### Phase 4: Consolidate Scripts
- Create `shared-scripts/serp_search.py` (unified search)
- Update imports in SKILL.md files
- Remove `distributor-inspector/scripts/`
- Remove `lead-enricher/scripts/`

### Phase 5: Update References
- Update all SKILL.md files to reference `../shared-references/...`
- Consolidate image-analyzer files into single guide
- Extract cross-routing logic to `shared-references/cross-routing.md`

### Phase 6: Cleanup & Testing
- Remove empty directories
- Update documentation
- Test each skill independently
- Test classification → inspection workflow
- Update README.md

---

## Detailed Changes

### lead-classifier/SKILL.md

```markdown
---
name: lead-classifier
description: Quickly classify lead type from basic website info. Routes to correct inspector skill. Run BEFORE detailed inspection. Output: recommended inspector or exclude reason.
arguments:
  url:
    description: The URL to classify
    required: true
    type: string
---

# Lead Classifier

Quickly determine lead type to route efficiently.

## Process (30 seconds)

1. Navigate to homepage (playwright-cli)
2. Scan for key signals
3. Classify and route

## Classification Logic

| Signal | Route To | Confidence |
|--------|----------|------------|
| Sells physical products | distributor-inspector | HIGH |
| Operates facilities | ka-inspector | HIGH |
| Client relationships | channel-partner-inspector | MEDIUM |
| None of above | exclude | LOW |

## Output Format

**Company:** {name}
**Type:** {type}
**Route To:** {skill-name}
**Reason:** {explanation}
```

### distributor-inspector/SKILL.md Updates

**Remove**:
- Duplicate `icp-sales/` and `icp-skill/` directories
- `scripts/` directory

**Update References**:
```markdown
### Step 4: Check Hard Gates

**Delegate to:** `../shared-references/icp/hard-gates.md`

### Step 3: Extract Contact Information

**LinkedIn Search:**
```bash
python3 ../shared-scripts/serp_search.py "{company} linkedin" "{country}" "{lang}" "5"
```

### Deep Mode Image Analysis

**See:** `../shared-references/image-analysis-guide.md`
```

### ka-inspector/SKILL.md Updates

**Remove**:
- Entire `references/icp-sales/` directory (duplicate)
- Entire `references/icp-skill/` directory (duplicate)
- `references/image-analyzer.md` (use shared guide)

**Update References**:
```markdown
### Step 4: Check Hard Gates

**Delegate to:** `../shared-references/icp/hard-gates.md`

### Deep Mode Image Analysis

For facility photos and location analysis:
**See:** `../shared-references/image-analysis-guide.md` → "KA End-User Analysis" section
```

### channel-partner-inspector/SKILL.md Updates

**Keep** (unique to this skill):
- `references/client-detection.md`
- `references/scoring-matrix.md`

**Add References**:
```markdown
### Step 3: Detect Client Overlap

**Delegate to:** `references/client-detection.md`

### Cross-Routing

**See:** `../shared-references/cross-routing.md`
```

### lead-enricher/SKILL.md Updates

**Remove**:
- `scripts/` directory

**Update**:
```markdown
## Prerequisites

```bash
# Install shared utilities
cd skills/shared-scripts
uv pip install -e .

# Configure API key in ~/.claude/config.json
{
  "brightdata_api_key": "your-key-here"
}
```

## Usage

```bash
python3 ../shared-scripts/serp_search.py "{company}" "{country}" "{lang}" "10"
```
```

### shared-scripts/serp_search.py

**Purpose**: Unified SERP search utility for all skills

**Usage**:
```bash
# LinkedIn lookup (distributor-inspector)
python3 shared-scripts/serp_search.py "company linkedin" "DE" "de" "5"

# Website search (lead-enricher)
python3 shared-scripts/serp_search.py "company name" "FR" "fr" "10"
```

**Implementation**: Merge logic from `distributor-inspector/scripts/search.py` and `lead-enricher/scripts/enrich.py`

### shared-references/cross-routing.md

**Purpose**: Centralized routing logic

```markdown
# Cross-Routing Decision Matrix

## From lead-classifier
- Sells products → distributor-inspector
- Operates facilities → ka-inspector
- Client relationships → channel-partner-inspector

## From distributor-inspector
- Fails hard gates BUT client overlap → channel-partner-inspector
- Operates facilities → ka-inspector

## From ka-inspector
- Doesn't operate facilities BUT client overlap → channel-partner-inspector
- Sells products → distributor-inspector

## From channel-partner-inspector
- Sells products → distributor-inspector
- Operates facilities → ka-inspector
```

### shared-references/image-analysis-guide.md

**Purpose**: Consolidated image analysis guidance

**Structure**:
```markdown
# Image Analysis Guide

## For Distributor Inspectors
- Team photos: Count faces for employee verification
- Competitor logos: Check footer/partners sections
- Certifications: Detect ISO badges, dealer badges

## For KA Inspectors
- Facility photos: Verify facility type and scale
- Location count: Multi-site presence
- Digital systems: IoT, BMS mentions

## Detection Patterns
[Shared patterns for both]
```

---

## Benefits Summary

### Efficiency
- **50% faster** workflow (classify → inspect vs trial-and-error)
- **Reduced API costs** (fewer SERP API calls)

### Maintainability
- **Single source of truth** for shared logic
- **Update once** applies to all skills
- **Clear separation** of concerns

### Best Practices
- **Flat structure** (follows Agent Skills spec)
- **<500 lines** per SKILL.md
- **One level deep** reference structure
- **DRY principle** throughout

### Developer Experience
- **Easier to understand** (clear organization)
- **Easier to extend** (add new inspector skills)
- **Easier to test** (isolated components)

---

## Risks & Mitigations

### Risk: Breaking existing workflows
**Mitigation**: 
- Test each skill independently before integration
- Maintain backward compatibility during transition
- Git tracks all file moves

### Risk: Confusion about when to use lead-classifier
**Mitigation**:
- Clear description in SKILL.md frontmatter
- Update README with workflow examples
- Document in CLAUDE.md

### Risk: Shared config file conflicts
**Mitigation**:
- Single `~/.claude/config.json` with clear structure
- Document configuration in each SKILL.md
- Provide example config in README

---

## Success Criteria

1. ✅ All skills follow Agent Skills specification
2. ✅ No duplicate ICP files
3. ✅ lead-classifier reduces inspection time by 50%
4. ✅ All references resolve correctly
5. ✅ All skills pass testing
6. ✅ Documentation is clear and complete

---

## Next Steps

1. **Create implementation plan** (using writing-plans skill)
2. **Execute migration** in phases
3. **Test thoroughly** at each phase
4. **Update documentation**
5. **Release as version 2.0.0**

---

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent Skills Best Practices](https://agentskills.io/what-are-skills)
- [Obsidian Skills Example](https://github.com/kepano/obsidian-skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
