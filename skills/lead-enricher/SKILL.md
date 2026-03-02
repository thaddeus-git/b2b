---
name: lead-enricher
description: Use when you have a CSV of leads with names, companies, phones, emails but no websites. Finds company websites, LinkedIn profiles, and verifies person legitimacy using Bright Data SERP API.
arguments:
  csv_path:
    description: Path to UTF-8 CSV file containing leads (tab-delimited)
    required: true
    type: string
  output_path:
    description: Path for enriched CSV output (default: {input}_enriched.csv)
    required: false
    type: string
  min_confidence:
    description: Minimum confidence threshold for auto-accept (default: 0.8)
    required: false
    type: number
    default: 0.8
---

# Lead Enricher

Enrich lead CSVs with website, LinkedIn URLs, company basics, and person verification.

## Overview

This skill takes a CSV of leads (from Facebook/Instagram ads) and enriches each lead with:
- Company website URL (with confidence score)
- Company LinkedIn page
- Person's LinkedIn profile
- Detected country
- Person verification status

## Prerequisites

```bash
# Install dependencies with uv
cd skills/lead-enricher/scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Configure Bright Data SERP API
python3 setup.py
# Then edit ~/.claude/lead-enricher/config.json and add your API key
```

## Input Requirements

- **Format:** CSV (tab-delimited), UTF-8 encoding
- **Required columns:** `full_name`, `company_name`, `work_phone_number`, `work_email`

## Usage

**Enrich a CSV:**
```bash
python3 scripts/enrich.py /path/to/leads.csv
```

**With custom output path:**
```bash
python3 scripts/enrich.py /path/to/leads.csv /path/to/output.csv
```

**With lower confidence threshold:**
```bash
python3 scripts/enrich.py /path/to/leads.csv --min-confidence 0.6
```

**Test API connection:**
```bash
python3 scripts/enrich.py --test
```

## Output

**Files created:**
- `{name}_enriched.csv` - All leads with enrichment data
- `{name}_enriched_review_needed.csv` - Leads needing manual review

**Added columns:**

| Column | Description |
|--------|-------------|
| `website` | Company website URL |
| `website_confidence` | 0.0-1.0 match score |
| `company_linkedin` | Company LinkedIn URL |
| `person_linkedin` | Person's LinkedIn URL |
| `person_verified` | true/false/null |
| `employee_count` | Company size (if found) |
| `industry` | Primary industry (if found) |
| `country` | Detected country |
| `notes` | Review notes |

## Confidence Scoring

**Delegate to:** `references/confidence-scoring.md`

| Signal | Weight |
|--------|--------|
| Email domain matches website | 0.50 |
| Company name similarity | 0.25 |
| Phone number on website | 0.15 |
| Person name on website | 0.10 |

**Thresholds:**
- `>= 0.8`: High confidence, auto-accept
- `0.5-0.79`: Medium confidence, flag for review
- `< 0.5`: Low confidence, candidates in notes

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Generic email (gmail, etc.) | Skip domain match bonus |
| Generic company name | Flag in notes for manual verify |
| SERP API failure | Note error, continue processing |
| No results | Note "No results found" |

## Rate Limiting

- 1 second delay between SERP API calls
- Progress indicator every 10 leads

## Example

**Input:**
```
full_name	company_name	work_phone_number	work_email
Sven Haubert	Reha360	+4951418879605	Office@reha360.de
```

**Output:**
```
full_name	company_name	work_phone_number	work_email	website	website_confidence	company_linkedin	person_linkedin	person_verified	country	notes
Sven Haubert	Reha360	+4951418879605	Office@reha360.de	https://reha360.de	0.95	https://linkedin.com/company/reha360		true	DE
```
