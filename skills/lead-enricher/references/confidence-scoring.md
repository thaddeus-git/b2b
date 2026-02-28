# Confidence Scoring Algorithm

## Overview

This document describes how to score website matches for lead enrichment.

## Scoring Components

| Signal | Weight | Description |
|--------|--------|-------------|
| Email domain match | 0.50 | Website domain matches email domain |
| Company name similarity | 0.25 | Fuzzy match between company name and website title |
| Phone on website | 0.15 | Lead's phone number found on website |
| Person name on website | 0.10 | Lead's name found on team/about page |

## Algorithm

```python
def score_match(lead, candidate_website):
    score = 0.0

    # Email domain match (strongest signal)
    if email_domain_matches(lead.email, candidate_website.url):
        score += 0.50

    # Company name similarity (fuzzy match, 0-1 scaled)
    similarity = fuzzy_similarity(lead.company_name, candidate_website.title)
    score += similarity * 0.25

    # Phone number found on website
    if normalize_phone(lead.phone) in normalize_phone(candidate_website.content):
        score += 0.15

    # Person name found on website (About/Team page)
    if lead.full_name in candidate_website.team_page_content:
        score += 0.10

    return min(score, 1.0)
```

## Thresholds

| Score | Action |
|-------|--------|
| >= 0.80 | Auto-accept, high confidence |
| 0.50-0.79 | Accept with review flag |
| < 0.50 | Reject, add candidates to notes |

## Email Domain Matching

Extract domain from email and compare to website domain:

```python
def email_domain_matches(email, website_url):
    email_domain = email.split('@')[-1].lower()
    website_domain = extract_domain(website_url).lower()

    # Exact match
    if email_domain == website_domain:
        return True

    # www prefix handling
    if email_domain == website_domain.replace('www.', ''):
        return True

    return False
```

## Generic Email Domains

Skip email domain bonus for generic providers:

- gmail.com, outlook.com, hotmail.com, yahoo.com
- web.de, gmx.de, t-online.de (German providers)
- aol.com, icloud.com, mail.com

## Company Name Similarity

Use fuzzy string matching (Levenshtein distance):

```python
from thefuzz import fuzz

def fuzzy_similarity(name1, name2):
    # Token sort ratio handles word order differences
    # "Wolf Bavaria GmbH" vs "Bavaria Wolf" -> high score
    return fuzz.token_sort_ratio(name1, name2) / 100.0
```

## Phone Normalization

Normalize phone numbers before comparison:

```python
import re

def normalize_phone(phone):
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)

    # Handle country codes
    # +49... -> 49...
    # 0049... -> 49...
    # 0... (local) -> keep as is for now

    return digits
```

## Person Verification

After finding website, check for person's name:

1. Search for exact name on website
2. Check /about, /team, /kontakt, /impresum pages
3. If found: `person_verified = true`
4. If not found: `person_verified = null` (inconclusive)
5. If found but different company context: `person_verified = false`
