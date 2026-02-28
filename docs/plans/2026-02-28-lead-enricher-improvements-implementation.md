# Lead-Enricher Improvements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve enrichment accuracy by adding email-first search, LinkedIn validation, website priority, and better edge case handling.

**Architecture:** Modify enrich.py to: (1) try direct website before searching, (2) search by email for company domains, (3) validate LinkedIn results with fuzzy matching, (4) verify person=company cases instead of skipping. Add unit and integration tests.

**Tech Stack:** Python 3, pytest, thefuzz, aiohttp (for direct website check)

---

## Task 1: Expand Email ISP List

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py:29-34`

**Step 1: Replace GENERIC_EMAIL_DOMAINS with expanded list**

Find lines 29-34 and replace with:

```python
# Generic email domains (ISPs - skip email-first search)
GENERIC_EMAIL_DOMAINS = {
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

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): expand email ISP list"
```

---

## Task 2: Add Direct Website Check Function

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (insert after imports)

**Step 1: Add aiohttp import**

Add after line 22 (after `from urllib.parse import urlparse`):

```python
import aiohttp
```

**Step 2: Add try_direct_website function**

Insert after `detect_country()` function (after line 132):

```python
async def try_direct_website(domain: str, timeout: float = 5.0) -> tuple[Optional[str], bool]:
    """
    Try to access website directly by domain.

    Returns: (url, success) where url is the final URL after redirects
    """
    if not domain:
        return None, False

    url = f"https://{domain}/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=True,
            ) as response:
                if response.status == 200:
                    return str(response.url), True
    except Exception:
        pass

    return None, False
```

**Step 3: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add direct website check function"
```

---

## Task 3: Add LinkedIn Validation Function

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (insert)

**Step 1: Add validate_linkedin_result function**

Insert after `try_direct_website()` function:

```python
def validate_linkedin_result(
    company_name: str,
    result_url: str,
    result_title: str,
    min_similarity: float = 0.6,
) -> bool:
    """
    Validate that a LinkedIn result matches the company.

    Returns: True if result is valid, False if it should be skipped
    """
    if not company_name or not result_url:
        return False

    company_lower = company_name.lower().strip()

    # Check 1: Company name in title (fuzzy match)
    if result_title:
        similarity = fuzzy_similarity(company_name, result_title)
        if similarity >= min_similarity:
            return True

    # Check 2: Company slug in URL
    # Extract slug from URL (e.g., "reha360" from /company/reha360)
    url_lower = result_url.lower()
    if "linkedin.com/company/" in url_lower:
        # Get the slug part
        parts = url_lower.split("/company/")[-1].split("/")
        if parts:
            slug = parts[0].replace("-", "").replace("_", "")
            company_nospace = company_lower.replace(" ", "").replace("-", "")
            if company_nospace in slug or slug in company_nospace:
                return True

    return False
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add LinkedIn result validation"
```

---

## Task 4: Add Person=Company Check Function

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (insert)

**Step 1: Add person_equals_company function**

Insert after `validate_linkedin_result()` function:

```python
def person_equals_company(full_name: str, company_name: str) -> bool:
    """
    Check if person name equals or is contained in company name.

    Returns: True if they appear to be the same entity
    """
    if not full_name or not company_name:
        return False

    name_lower = full_name.lower().strip()
    company_lower = company_name.lower().strip()

    # Exact match
    if name_lower == company_lower:
        return True

    # Name contained in company (e.g., "Mina" in "Mina GmbH")
    if name_lower in company_lower:
        return True

    # Company contained in name (less common but possible)
    if company_lower in name_lower:
        return True

    return False
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add person=company detection"
```

---

## Task 5: Add Email Search Function

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (insert)

**Step 1: Add search_by_email function**

Insert after `person_equals_company()` function (before `search_company`):

```python
async def search_by_email(
    email: str,
    country_code: str = "DE",
    num_results: int = 5,
) -> dict:
    """
    Search for exact email address to find associated websites.

    Returns dict with results or error.
    """
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {"error": "brightdata-sdk not installed", "success": False}

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {"error": str(e), "success": False}

    query = f'"{email}"'

    location_map = {
        "DE": "Germany", "AT": "Austria", "CH": "Switzerland",
        "FR": "France", "ES": "Spain",
    }
    location = location_map.get(country_code, "Germany")

    try:
        async with BrightDataClient(
            token=api_key,
            validate_token=False,
            auto_create_zones=False,
        ) as client:
            results = await client.search.google(
                query=query,
                location=location,
                language="de" if country_code in ("DE", "AT", "CH") else "en",
                num_results=num_results,
            )

            if not results.success:
                return {"error": f"Search failed: {results.error}", "success": False}

            mapped = []
            for item in results.data:
                mapped.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                })

            return {
                "success": True,
                "query": query,
                "results": mapped
            }

    except Exception as e:
        return {"error": str(e), "success": False}
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add email search function"
```

---

## Task 6: Update enrich_lead with New Logic

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py:380-454`

**Step 1: Replace enrich_lead function**

Replace the entire `enrich_lead` function (lines 380-454) with:

```python
async def enrich_lead(
    lead: dict,
    min_confidence: float = 0.8,
) -> dict:
    """
    Enrich a single lead with website and LinkedIn info.

    Returns enriched lead dict.
    """
    result = lead.copy()

    # Initialize new fields
    result["website"] = ""
    result["website_confidence"] = 0.0
    result["company_linkedin"] = ""
    result["person_linkedin"] = ""
    result["person_verified"] = ""
    result["employee_count"] = ""
    result["industry"] = ""
    result["country"] = detect_country(lead)
    result["notes"] = ""

    company_name = lead.get("company_name", "").strip()
    full_name = lead.get("full_name", "").strip()
    email = lead.get("work_email", "").strip()
    email_domain = extract_email_domain(email)
    is_generic_email = is_generic_email_domain(email_domain) if email_domain else True

    # Check for generic company name
    generic_names = ["selbstständigkeit", "selbstständig", "self-employed",
                     "freelancer", "privat", "private"]
    if company_name.lower() in generic_names:
        result["notes"] = "Generic company name, verify manually"
        return result

    # Check if person name equals company name
    person_is_company = person_equals_company(full_name, company_name)

    # Strategy 1: Try direct website from email domain (non-generic emails only)
    website_found = False
    if not is_generic_email and email_domain:
        direct_url, success = await try_direct_website(email_domain)
        if success:
            result["website"] = direct_url
            result["website_confidence"] = 0.7  # Good confidence from direct access
            website_found = True

    # Strategy 2: Search by email (non-generic emails only)
    if not website_found and not is_generic_email and email:
        email_search = await search_by_email(email, result["country"])
        if email_search.get("success"):
            email_results = email_search.get("results", [])
            if email_results:
                # Look for website in email search results
                for item in email_results:
                    url = item.get("url", "")
                    # Skip social media
                    if any(d in url for d in ["linkedin.com", "facebook.com", "instagram.com"]):
                        continue
                    # Check if email domain matches
                    if email_domain and extract_domain(url) == email_domain:
                        result["website"] = url
                        result["website_confidence"] = 0.8  # High confidence - email search + domain match
                        website_found = True
                        break

    # Strategy 3: Search by company name (fallback)
    if not website_found:
        search_result = await search_company(company_name, result["country"])

        if search_result.get("success"):
            search_results = search_result.get("results", [])
            if search_results:
                best_url, confidence, candidates = find_best_website(lead, search_results, min_confidence)
                result["website"] = best_url or ""
                result["website_confidence"] = confidence

                # Handle confidence levels
                if confidence < min_confidence and confidence >= 0.5:
                    top_candidates = candidates[:3]
                    candidate_urls = [c["url"] for c in top_candidates]
                    result["notes"] = f"Medium confidence. Candidates: {', '.join(candidate_urls)}"
                elif confidence < 0.5:
                    result["notes"] = f"Low confidence match ({confidence:.2f}). Manual review needed."
        else:
            result["notes"] = f"Search error: {search_result.get('error', 'Unknown')}"

    # Handle person=company case
    if person_is_company and not is_generic_email:
        # Can verify via email domain
        pass  # Already handled above
    elif person_is_company and is_generic_email:
        # Cannot verify - flag for manual review
        if not result["notes"]:
            result["notes"] = "Person name equals company name with generic email. Verify manually."

    # Search for LinkedIn profiles (with validation)
    if company_name:
        linkedin_company = await search_linkedin_company(company_name, result["country"])
        if linkedin_company.get("success") and linkedin_company.get("url"):
            # Validate LinkedIn result
            if validate_linkedin_result(company_name, linkedin_company["url"], linkedin_company.get("title", "")):
                result["company_linkedin"] = linkedin_company["url"]
            # If validation fails, don't set company_linkedin (leave empty)

    if full_name and company_name:
        linkedin_person = await search_linkedin_person(full_name, company_name, result["country"])
        if linkedin_person.get("success") and linkedin_person.get("url"):
            result["person_linkedin"] = linkedin_person["url"]
            result["person_verified"] = "true"  # Found on LinkedIn with company

    return result
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): update enrich_lead with new logic"
```

---

## Task 7: Update search_linkedin_company with Validation

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py:254-302`

**Step 1: Modify search_linkedin_company to validate results**

Replace the function (lines 254-302) with:

```python
async def search_linkedin_company(
    company_name: str,
    country_code: str = "DE",
) -> dict:
    """Search for company's LinkedIn page with validation."""
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {"error": "brightdata-sdk not installed", "success": False}

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {"error": str(e), "success": False}

    query = f'"{company_name}" site:linkedin.com/company'

    location_map = {
        "DE": "Germany", "AT": "Austria", "CH": "Switzerland",
        "FR": "France", "ES": "Spain", "NL": "Netherlands",
    }
    location = location_map.get(country_code, "Germany")

    try:
        async with BrightDataClient(
            token=api_key,
            validate_token=False,
            auto_create_zones=False,
        ) as client:
            results = await client.search.google(
                query=query,
                location=location,
                language="en",
                num_results=10,  # Get more results to find valid one
            )

            if not results.success:
                return {"error": f"Search failed: {results.error}", "success": False}

            # Try each result until we find a valid one
            for item in results.data:
                url = item.get("url", "")
                title = item.get("title", "")
                if "linkedin.com/company" in url:
                    # Validate before returning
                    if validate_linkedin_result(company_name, url, title):
                        return {
                            "success": True,
                            "url": url,
                            "title": title,
                        }

            return {"success": True, "url": None}

    except Exception as e:
        return {"error": str(e), "success": False}
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add validation to LinkedIn company search"
```

---

## Task 8: Create Unit Tests

**Files:**
- Create: `skills/lead-enricher/scripts/tests/__init__.py`
- Create: `skills/lead-enricher/scripts/tests/test_enrich.py`

**Step 1: Create tests directory**

```bash
mkdir -p skills/lead-enricher/scripts/tests
touch skills/lead-enricher/scripts/tests/__init__.py
```

**Step 2: Create test_enrich.py**

```python
#!/usr/bin/env python3
"""Unit tests for lead enrichment functions."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from enrich import (
    extract_domain,
    extract_email_domain,
    is_generic_email_domain,
    normalize_phone,
    fuzzy_similarity,
    validate_linkedin_result,
    person_equals_company,
    score_website_match,
)


class TestExtractDomain:
    def test_full_url(self):
        assert extract_domain("https://www.example.com/path") == "example.com"

    def test_without_protocol(self):
        assert extract_domain("example.com") == "example.com"

    def test_with_www(self):
        assert extract_domain("https://www.example.com") == "example.com"


class TestExtractEmailDomain:
    def test_normal_email(self):
        assert extract_email_domain("user@example.com") == "example.com"

    def test_invalid_email(self):
        assert extract_email_domain("invalid-email") is None

    def test_empty_string(self):
        assert extract_email_domain("") is None


class TestIsGenericEmailDomain:
    def test_gmail(self):
        assert is_generic_email_domain("gmail.com") is True

    def test_company_domain(self):
        assert is_generic_email_domain("reha360.de") is False

    def test_german_isp(self):
        assert is_generic_email_domain("web.de") is True


class TestNormalizePhone:
    def test_with_country_code(self):
        assert normalize_phone("+49-123-456-7890") == "491234567890"

    def test_with_spaces(self):
        assert normalize_phone("0664 1302708") == "06641302708"

    def test_empty(self):
        assert normalize_phone("") == ""


class TestFuzzySimilarity:
    def test_exact_match(self):
        assert fuzzy_similarity("Reha360", "Reha360") >= 0.99

    def test_similar_names(self):
        assert fuzzy_similarity("Reha360 GmbH", "Reha360") >= 0.8

    def test_different_names(self):
        assert fuzzy_similarity("Reha360", "Sankom Patent Socks") < 0.3


class TestValidateLinkedInResult:
    def test_matching_title(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/reha360",
            "Reha360 GmbH | LinkedIn"
        ) is True

    def test_matching_slug(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/reha360",
            ""
        ) is True

    def test_wrong_result(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/sankompatentsocks",
            "Sankom Patent Socks | LinkedIn"
        ) is False

    def test_partial_match(self):
        assert validate_linkedin_result(
            "SAUBERHAFT",
            "https://linkedin.com/company/sauberhaft-ch",
            "Sauberhaft | LinkedIn"
        ) is True


class TestPersonEqualsCompany:
    def test_exact_match(self):
        assert person_equals_company("Mina", "Mina") is True

    def test_name_in_company(self):
        assert person_equals_company("Mina", "Mina GmbH") is True

    def test_different(self):
        assert person_equals_company("Sven Haubert", "Reha360") is False

    def test_empty(self):
        assert person_equals_company("", "Company") is False


class TestScoreWebsiteMatch:
    def test_email_domain_match(self):
        lead = {"company_name": "Reha360", "work_email": "office@reha360.de", "work_phone_number": ""}
        result = {"url": "https://reha360.de", "title": "Reha360", "snippet": ""}
        score = score_website_match(lead, result)
        assert score >= 0.5  # Email domain match

    def test_generic_email_no_bonus(self):
        lead = {"company_name": "Test", "work_email": "user@gmail.com", "work_phone_number": ""}
        result = {"url": "https://test.com", "title": "Test", "snippet": ""}
        score = score_website_match(lead, result)
        assert score < 0.5  # No email domain bonus for generic

    def test_phone_in_snippet(self):
        lead = {"company_name": "Test", "work_email": "", "work_phone_number": "+49-123-456"}
        result = {"url": "https://test.com", "title": "Test", "snippet": "Call us at 49123456"}
        score = score_website_match(lead, result)
        assert score >= 0.15  # Phone bonus
```

**Step 3: Run tests**

```bash
cd skills/lead-enricher/scripts && python3 -m pytest tests/test_enrich.py -v
```

**Step 4: Commit**

```bash
git add skills/lead-enricher/scripts/tests/
git commit -m "feat(lead-enricher): add unit tests"
```

---

## Task 9: Run Integration Test

**Files:**
- None (testing only)

**Step 1: Create test CSV with diverse cases**

```bash
cat > /tmp/test_improved_leads.csv << 'EOF'
full_name	company_name	work_phone_number	work_email
Sven Haubert	Reha360	+4951418879605	Office@reha360.de
Mina	Mina	015566468185	minasohrabi1987@gmail.com
Don Erwin	Selbstständigkeit	+4917647628313	rwevogt@gmail.com
Alexander Vystoupil	SAUBERHAFT	+436769611946	Office@sauberhaft.at
EOF
```

**Step 2: Run enrichment**

```bash
python3 skills/lead-enricher/scripts/enrich.py /tmp/test_improved_leads.csv /tmp/test_improved_output.csv --min-confidence 0.5
```

**Step 3: Verify results**

Expected:
- Reha360: website found, LinkedIn validated (not sankompatentsocks)
- Mina: flagged for manual review (person=company, generic email)
- Selbstständigkeit: flagged as generic company name
- SAUBERHAFT: website found, Austrian

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat(lead-enricher): complete improvements with tests"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Expand email ISP list | enrich.py |
| 2 | Add direct website check | enrich.py |
| 3 | Add LinkedIn validation | enrich.py |
| 4 | Add person=company detection | enrich.py |
| 5 | Add email search function | enrich.py |
| 6 | Update enrich_lead logic | enrich.py |
| 7 | Update LinkedIn search with validation | enrich.py |
| 8 | Create unit tests | tests/test_enrich.py |
| 9 | Run integration test | (testing only) |
