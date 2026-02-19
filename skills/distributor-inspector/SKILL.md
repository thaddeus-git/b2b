---
name: distributor-inspector
description: Use when evaluating websites as potential distributors for OrientStar Robotics (cleaning robots). Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach.
---

# Distributor Inspector

Inspect and score potential distributor websites for OrientStar Robotics (cleaning robot sales).

## Overview

Evaluates websites against ICP criteria, categorizes by niche market using standardized tags, and routes to appropriate action (prioritize/standard/explore/exclude/route-to-sales).

## When to Use

```dot
digraph use_flowchart {
    "Need to evaluate distributor website?" [shape=diamond];
    "Use distributor-inspector" [shape=box];

    "Need to evaluate distributor website?" -> "Use distributor-inspector" [label="yes"];
}
```

**When to use:**
- Evaluating potential distributors from search results
- Qualifying websites for sales outreach
- Identifying competitor distributors (Pudu, Gausium, LionsBot, etc.)
- Categorizing companies by niche market

## Tag Format

`{primary-product-category}-{business-model}`

**Product categories:** cleaning-equipment, cleaning-supplies, facility-management, cleaning-services, robotics, industrial-equipment, hospitality-supplies, general-merchandise

**Business models:** distributor, wholesaler, retailer, service-provider, system-integrator, manufacturer

**Special tags:** competitor-robot-distributor, pure-2c-retail

See `config/tags.md` for complete taxonomy.

## Scoring

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Required: No competitor focus | PASS/FAIL |
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
  "digest": {
    "company_name": "Name",
    "description": "Brief",
    "products_sold": ["..."],
    "services_offered": ["..."],
    "brands_carried": ["..."],
    "geographic_focus": "Country",
    "team_presence": "...",
    "sla_mentions": "..."
  },
  "tags": ["tag1", "tag2"],
  "scoring": {
    "required_checks": {
      "sells_as_expected": true,
      "no_competitor_focus": true
    },
    "cleaning_equipment_bonus": 70,
    "total_score": 78,
    "grade": "B"
  },
  "key_signals": ["...", "..."],
  "action": "standard"
}
```

## Process

1. **Digest**: Fetch website, extract key info (company, products, services, brands, team, SLA)
2. **Categorize**: Apply niche market tags (multiple allowed)
3. **Score**: Run required checks + apply cleaning equipment bonus
4. **Route**: Return action recommendation

## Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment | +30 |
| Moderate | Has product category | +50 |
| Strong | Core offering, multiple products | +70 |
| Dominant | Primary business, extensive catalog | +90 |

## Competitor Detection

Check `human_input/competing brands & SKUs.md` for brands to detect:
- Pudu, Gausium, LionsBot, Tennant, Nilfisk, Kärcher, Adlatus, ICE Cobotics, SoftBank, Avidbots

If competitor products found → apply `competitor-robot-distributor` tag → action: `route-to-sales`

## Configuration Files

| File | Purpose |
|------|---------|
| `config/keywords.md` | Product/service keywords by industry |
| `config/tags.md` | Niche market tag taxonomy |
| `human_input/competing brands & SKUs.md` | Competitor brands to detect |
