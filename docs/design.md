# Distributor Inspection System - Design Summary

## Overview

A Claude skill that inspects potential distributor websites for OrionStar Robotics, evaluates them against ICP criteria, and outputs structured scoring with niche market categorization.

## Core Workflow

```
URL → Skill → Digest → Tags → Score → Action
```

## Files Created

| File | Purpose | Editable |
|------|---------|----------|
| `config/keywords.md` | Product/service keywords by target industry | ✅ Yes |
| `config/tags.md` | Niche market tag taxonomy | ✅ Yes |
| `skills/distributor-inspector.md` | Main skill definition | Reference only |
| `CLAUDE.md` | Project documentation | ✅ Yes |
| `human_input/competing brands & SKUs.md` | Competitor brands to detect | ✅ Yes |

## Tag Format

`{primary-product-category}-{business-model}`

**Primary Product Categories:**
- cleaning-equipment, cleaning-supplies, facility-management, cleaning-services, robotics, industrial-equipment, hospitality-supplies, general-merchandise

**Business Models:**
- distributor, wholesaler, retailer, service-provider, system-integrator, manufacturer

**Special Tags:**
- competitor-robot-distributor → Route to sales team
- pure-2c-retail → Exclude

## Scoring

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL gate |
| Required: No competitor focus | PASS/FAIL gate |
| Bonus: Cleaning equipment | +30 to +90 |

| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude |
| (any) + competitor tag | — | route-to-sales |

## Output Format

```json
{
  "url": "https://example.com",
  "digest": { ... },
  "tags": ["tag1", "tag2"],
  "scoring": { ... },
  "key_signals": [ ... ],
  "action": "standard"
}
```

## Next Steps

1. ✅ Design complete
2. ⏳ Implement skill as executable code
3. ⏳ Test on example websites
4. ⏳ Refine keywords and tags based on results
