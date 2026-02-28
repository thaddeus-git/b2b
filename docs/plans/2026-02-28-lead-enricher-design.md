# Lead Enricher Skill Design

**Date:** 2026-02-28
**Status:** Approved

## Overview

A skill to enrich lead CSVs with website, LinkedIn URLs, company basics, and person verification using Bright Data SERP API.

## Problem Statement

Leads from Facebook/Instagram ads contain only basic contact info:
- `full_name`
- `company_name`
- `work_phone_number`
- `work_email`

We need to:
1. Find the company website
2. Find LinkedIn profiles (company + person)
3. Verify the person is legitimate
4. Get company basics (size, industry, country)

## Solution

### Skill Structure

```
skills/
└── lead-enricher/
    ├── SKILL.md                    # Main skill definition
    ├── scripts/
    │   ├── setup.py                # Configure Bright Data API
    │   └── enrich.py               # Core enrichment logic
    └── references/
        └── confidence-scoring.md   # Scoring algorithm details
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `csv_path` | Yes | - | Path to UTF-8 CSV file |
| `output_path` | No | `{name}_enriched.csv` | Output path |
| `min_confidence` | No | 0.8 | Threshold for auto-accept |

### Input Requirements

- **Encoding:** UTF-8 (required)
- **Required columns:** `full_name`, `company_name`, `work_phone_number`, `work_email`

### Output Columns (Added)

| Column | Description |
|--------|-------------|
| `website` | Company website URL |
| `website_confidence` | 0.0-1.0 match score |
| `company_linkedin` | Company LinkedIn URL |
| `person_linkedin` | Person's LinkedIn URL |
| `person_verified` | true/false/null |
| `employee_count` | Company size |
| `industry` | Primary industry |
| `country` | Detected country |
| `notes` | Review notes for ambiguous cases |

### Output Files

| File | Content |
|------|---------|
| `{name}_enriched.csv` | All leads with enrichment data |
| `{name}_review_needed.csv` | Low-confidence matches (< 0.8) |

## Confidence Scoring Algorithm

```python
def score_match(lead, candidate_website):
    score = 0.0

    # Email domain match (strongest signal)
    if email_domain_matches(candidate_website):
        score += 0.5

    # Company name similarity (fuzzy match)
    score += fuzzy_similarity(lead.company_name, website_title) * 0.25

    # Phone number found on website
    if lead.phone in website_content:
        score += 0.15

    # Person name found on website (About/Team page)
    if lead.full_name in website_team_page:
        score += 0.10

    return min(score, 1.0)
```

### Threshold Behavior

| Score | Action |
|-------|--------|
| >= 0.8 | Auto-accept, `person_verified=true` if name found |
| 0.5-0.79 | Include but flag for manual review with `notes` |
| < 0.5 | Leave blank, add candidate URLs to `notes` |

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Email domain is generic (gmail, outlook) | Skip domain match bonus |
| Company name is generic ("Selbstständigkeit") | Flag in `notes` |
| Multiple candidates with similar scores | Include top 3 in `notes` |
| SERP API failure | Retry once, then `website_error=true` |
| No results found | Leave blank, `notes="No results"` |
| Person name not found | `person_verified=null` |
| Person name found but wrong company | `person_verified=false` |

### Rate Limiting

- 1 second delay between SERP API calls
- Progress indicator every 10 leads
- Errors logged to `{name}_errors.log`

## Data Flow

```
Input CSV (leads)
       │
       ▼
   enrich.py
   (SERP search)
       │
       ▼
 Enriched CSV
 + confidence
       │
       ├─► {name}_enriched.csv (all leads)
       │
       └─► {name}_review_needed.csv (low confidence)
```

## Integration with Other Skills

This skill is **standalone**. After enrichment:

1. Review `_review_needed.csv` manually
2. (Optional) Run `distributor-inspector` on enriched websites separately

## Prerequisites

```bash
# Configure Bright Data SERP API
cd skills/lead-enricher
python3 scripts/setup.py
# Edit ~/.claude/lead-enricher/config.json with API key
```

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Search API | Bright Data SERP | Reuses existing infrastructure |
| Output format | CSV only | Easier for batch processing |
| Integration | Standalone | Keeps skills focused and composable |
| Confidence threshold | 0.8 | Balances accuracy vs coverage |
| CSV encoding | UTF-8 required | Standard format, avoids encoding issues |
