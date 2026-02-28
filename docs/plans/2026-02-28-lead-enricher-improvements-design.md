# Lead-Enricher Improvements Design

**Date:** 2026-02-28
**Status:** Approved

## Problem Statement

Testing revealed issues with the enrichment logic:

1. **LinkedIn returns wrong results** - "Reha360" search returned "sankompatentsocks"
2. **Generic names get wrong results** - "Mina / Mina" returned Spotify artist
3. **No website priority** - Searches before trying obvious domain
4. **No email ISP filtering** - Wastes API calls on gmail/outlook emails

## Solution

### 1. Website Discovery Priority

**For company emails (non-ISP domains):**

```
1. Extract domain from email (e.g., alibaba-inc.com)
2. Try direct website: https://{domain}/
   - If accessible (200 OK) → use as website (confidence: 0.7)
3. If not accessible → search for company name
   - May find different domain (alibaba-inc.com → alibaba.com)
```

### 2. Email-First Search

**For company emails:**

```
Search query: "office@reha360.de"

Expected results:
- Company website (if email listed on contact page)
- Directories/profiles containing the email
- Nothing (if email is private)

Confidence boost:
- If website found via email search: +0.3 to confidence
```

### 3. LinkedIn Result Validation

**Validation rules:**

| Check | Implementation |
|-------|----------------|
| Company name in title | `fuzzy_similarity(company_name, title) >= 0.6` |
| URL contains company slug | `slugify(company_name) in url.lower()` |
| Skip if both fail | Return "Not found" instead of wrong result |

**Example:**
```
Query: "Reha360" site:linkedin.com/company
Result: https://linkedin.com/company/sankompatentsocks
Title: "Sankom Patent Socks - LinkedIn"
Validation: fuzzy_similarity("Reha360", "Sankom Patent Socks") = 0.15 ❌
Result: SKIP, return "Not found"
```

### 4. Person = Company Verification

**When COMPANY_NAME equals or contains PERSON_NAME:**

| Scenario | Email Type | Action |
|----------|------------|--------|
| Email domain matches company | Non-generic (e.g., mina@mina.com) | ✅ Proceed, high confidence |
| Person LinkedIn shows company | LinkedIn profile has company in title | ✅ Proceed, verified |
| Cannot verify | Generic email (gmail, etc.) | ⚠️ Flag for manual review |

**Key principle:** Don't skip entirely - try to verify first. Flag if unverified.

### 5. Email ISP List

**Skip email-first search for these domains:**

```python
EMAIL_ISP_DOMAINS = {
    # Global
    "gmail.com", "outlook.com", "hotmail.com", "yahoo.com",
    "aol.com", "icloud.com", "mail.com", "live.com", "msn.com",
    "googlemail.com", "ymail.com", "protonmail.com", "zoho.com",
    "fastmail.com",

    # German/DACH
    "web.de", "gmx.de", "gmx.at", "gmx.ch", "t-online.de",
    "online.de", "freenet.de", "1und1.de",

    # French
    "orange.fr", "wanadoo.fr", "laposte.net", "free.fr",

    # Spanish
    "telefonica.es", "terra.es",

    # Chinese
    "qq.com", "163.com", "126.com", "sina.com", "sohu.com",
}
```

## Test Plan

### Unit Tests

| Test | Input | Expected |
|------|-------|----------|
| Email domain match | email=@reha360.de, url=reha360.de | +0.5 score |
| Email domain mismatch | email=@reha360.de, url=other.com | +0.0 score |
| Generic email | email=@gmail.com, url=any.com | +0.0 (skip domain bonus) |
| Fuzzy name match | "Reha360 GmbH" vs "Reha360" | High similarity |
| Phone in snippet | phone=+49123, snippet has +49123 | +0.15 score |
| LinkedIn validation pass | "Reha360" vs "Reha360 GmbH" | Accept |
| LinkedIn validation fail | "Reha360" vs "Sankom Patent Socks" | Skip |

### Integration Tests

| Lead | Expected Website | Expected Confidence |
|------|------------------|---------------------|
| Reha360 / office@reha360.de | reha360.de | ≥ 0.5 |
| SAUBERHAFT / .at email | sauberhaft.at | ≥ 0.5 |
| Selbstständigkeit / gmail | (none) | 0.0 + flag |
| Mina / Mina / gmail | (none or verified) | flag if unverified |

## Files to Modify

| File | Change |
|------|--------|
| `scripts/enrich.py` | Add validation logic, website priority, email-first search |
| `scripts/tests/test_enrich.py` | New: Unit tests |
| `scripts/tests/test_integration.py` | New: Integration tests |

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Website discovery | Try direct domain first | Faster, saves API calls |
| LinkedIn validation | Fuzzy match >= 0.6 | Catches wrong results like "sankompatentsocks" |
| Person=Company | Try to verify, don't skip | May be valid (e.g., "Apple") |
| Email ISP list | Comprehensive global + regional | Avoids wasted searches on personal emails |
