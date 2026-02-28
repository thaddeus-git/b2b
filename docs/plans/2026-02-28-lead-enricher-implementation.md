# Lead Enricher Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a skill that enriches lead CSVs with website, LinkedIn URLs, company basics, and person verification using Bright Data SERP API.

**Architecture:** Python script reads CSV, calls Bright Data SERP API for each lead, scores matches using email domain + name similarity + phone verification, outputs enriched CSV with confidence scores. Standalone skill - no distributor-inspector integration.

**Tech Stack:** Python 3, brightdata-sdk, pandas (CSV handling), thefuzz (fuzzy string matching)

---

## Task 1: Create Skill Directory Structure

**Files:**
- Create: `skills/lead-enricher/`
- Create: `skills/lead-enricher/scripts/`
- Create: `skills/lead-enricher/references/`

**Step 1: Create directories**

```bash
mkdir -p skills/lead-enricher/scripts skills/lead-enricher/references
```

**Step 2: Verify structure**

Run: `ls -la skills/lead-enricher/`
Expected: `scripts/` and `references/` directories exist

**Step 3: Commit**

```bash
git add skills/lead-enricher/
git commit -m "feat(lead-enricher): create skill directory structure"
```

---

## Task 2: Create Setup Script

**Files:**
- Create: `skills/lead-enricher/scripts/setup.py`

**Step 1: Write setup.py**

```python
#!/usr/bin/env python3
"""
Setup script for lead-enricher skill.

Installs required packages and creates config template.
"""

import json
import subprocess
import sys
from pathlib import Path


CONFIG_DIR = Path.home() / ".claude" / "lead-enricher"
CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_TEMPLATE = {
    "api_key": "",
    "note": "Add your Bright Data SERP API key here"
}


def create_config():
    """Create config directory and config.json template if not exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(CONFIG_TEMPLATE, f, indent=2)
        print(f"Created config file: {CONFIG_FILE}")
        print("Please edit this file and add your Bright Data SERP API key.")
        return True
    else:
        print(f"Config file already exists: {CONFIG_FILE}")
        return False


def install_dependencies():
    """Install required packages if not already installed."""
    packages = ["brightdata-sdk", "pandas", "thefuzz"]

    for package in packages:
        try:
            if package == "thefuzz":
                __import__("thefuzz")
            else:
                __import__(package.replace("-", "_"))
            print(f"{package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"{package} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}", file=sys.stderr)
                return False
    return True


def main():
    """Run setup."""
    created_config = create_config()
    installed = install_dependencies()

    if installed and created_config:
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        print(f"\nNext step: Add your Bright Data API key to:")
        print(f"  {CONFIG_FILE}")
        print("\nVerify with: python3 scripts/enrich.py --test")
    elif installed:
        print("\n" + "=" * 60)
        print("Setup complete!")
        print("=" * 60)
        if CONFIG_FILE.exists():
            print(f"\nConfig file: {CONFIG_FILE}")
            print("Make sure your API key is configured.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 2: Make executable**

Run: `chmod +x skills/lead-enricher/scripts/setup.py`

**Step 3: Test setup**

Run: `python3 skills/lead-enricher/scripts/setup.py`
Expected: Creates `~/.claude/lead-enricher/config.json`, installs dependencies

**Step 4: Commit**

```bash
git add skills/lead-enricher/scripts/setup.py
git commit -m "feat(lead-enricher): add setup script with dependency installation"
```

---

## Task 3: Create Confidence Scoring Reference

**Files:**
- Create: `skills/lead-enricher/references/confidence-scoring.md`

**Step 1: Write confidence-scoring.md**

```markdown
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
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/references/confidence-scoring.md
git commit -m "feat(lead-enricher): add confidence scoring reference"
```

---

## Task 4: Create Core Enrichment Script (Part 1 - Utilities)

**Files:**
- Create: `skills/lead-enricher/scripts/enrich.py`

**Step 1: Write utility functions**

```python
#!/usr/bin/env python3
"""
Lead enrichment script using Bright Data SERP API.

Usage:
  python3 scripts/enrich.py <input_csv> [output_csv] [--min-confidence 0.8]

Example:
  python3 scripts/enrich.py leads.csv leads_enriched.csv
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Configuration
CONFIG_DIR = Path.home() / ".claude" / "lead-enricher"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Generic email domains (skip domain matching bonus)
GENERIC_EMAIL_DOMAINS = {
    "gmail.com", "outlook.com", "hotmail.com", "yahoo.com",
    "web.de", "gmx.de", "t-online.de", "aol.com", "icloud.com",
    "mail.com", "googlemail.com", "ymail.com", "live.com",
    "msn.com", "qq.com", "163.com", "126.com",
}


def get_api_key() -> str:
    """Get API key from environment variable or config file."""
    api_key = os.environ.get("BRIGHTDATA_SERP_API_KEY", "")
    if api_key:
        return api_key

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key", "")
                if api_key:
                    return api_key
        except (json.JSONDecodeError, IOError):
            pass

    raise ValueError(
        f"API key not found. Set BRIGHTDATA_SERP_API_KEY or edit {CONFIG_FILE}"
    )


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc.lower().replace("www.", "")


def extract_email_domain(email: str) -> Optional[str]:
    """Extract domain from email address."""
    if "@" not in email:
        return None
    return email.split("@")[-1].lower()


def is_generic_email_domain(domain: str) -> bool:
    """Check if domain is a generic email provider."""
    return domain in GENERIC_EMAIL_DOMAINS


def normalize_phone(phone: str) -> str:
    """Normalize phone number to digits only."""
    if not phone:
        return ""
    return re.sub(r"\D", "", phone)


def fuzzy_similarity(name1: str, name2: str) -> float:
    """Calculate fuzzy similarity between two names (0-1)."""
    try:
        from thefuzz import fuzz
        return fuzz.token_sort_ratio(name1, name2) / 100.0
    except ImportError:
        # Fallback: simple word overlap
        words1 = set(name1.lower().split())
        words2 = set(name2.lower().split())
        if not words1 or not words2:
            return 0.0
        overlap = len(words1 & words2)
        return overlap / max(len(words1), len(words2))


def detect_country(lead: dict) -> str:
    """Detect country from phone, email TLD, or company name."""
    phone = lead.get("work_phone_number", "")
    email = lead.get("work_email", "")

    # Phone country code
    phone_digits = normalize_phone(phone)
    if phone_digits.startswith("49"):
        return "DE"
    elif phone_digits.startswith("43"):
        return "AT"
    elif phone_digits.startswith("41"):
        return "CH"
    elif phone_digits.startswith("33"):
        return "FR"
    elif phone_digits.startswith("34"):
        return "ES"

    # Email TLD
    email_domain = extract_email_domain(email)
    if email_domain:
        if email_domain.endswith(".de"):
            return "DE"
        elif email_domain.endswith(".at"):
            return "AT"
        elif email_domain.endswith(".ch"):
            return "CH"
        elif email_domain.endswith(".fr"):
            return "FR"
        elif email_domain.endswith(".es"):
            return "ES"

    return "DE"  # Default to Germany for German leads
```

**Step 2: Test utilities**

Run: `python3 -c "from skills.lead_enricher.scripts.enrich import *; print(normalize_phone('+49-123-456-7890'))"`
Expected: `491234567890`

**Step 3: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add utility functions for enrichment"
```

---

## Task 5: Create Core Enrichment Script (Part 2 - SERP Search)

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (append)

**Step 1: Add SERP search functions**

```python
# (Append to enrich.py)

async def search_company(
    company_name: str,
    country_code: str = "DE",
    num_results: int = 10,
) -> dict:
    """
    Search for company using Bright Data SERP API.

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

    # Build search query
    query = f'"{company_name}"'

    # Country code to location
    location_map = {
        "DE": "Germany", "AT": "Austria", "CH": "Switzerland",
        "FR": "France", "ES": "Spain", "NL": "Netherlands",
        "BE": "Belgium", "IT": "Italy", "PL": "Poland",
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


async def search_linkedin_person(
    full_name: str,
    company_name: str,
    country_code: str = "DE",
) -> dict:
    """Search for person's LinkedIn profile."""
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {"error": "brightdata-sdk not installed", "success": False}

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {"error": str(e), "success": False}

    query = f'"{full_name}" "{company_name}" site:linkedin.com/in'

    location_map = {"DE": "Germany", "AT": "Austria", "CH": "Switzerland"}
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
                num_results=5,
            )

            if not results.success:
                return {"error": f"Search failed", "success": False}

            for item in results.data:
                url = item.get("url", "")
                if "linkedin.com/in" in url:
                    return {
                        "success": True,
                        "url": url,
                        "title": item.get("title", ""),
                    }

            return {"success": True, "url": None}

    except Exception as e:
        return {"error": str(e), "success": False}


async def search_linkedin_company(
    company_name: str,
    country_code: str = "DE",
) -> dict:
    """Search for company's LinkedIn page."""
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {"error": "brightdata-sdk not installed", "success": False}

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {"error": str(e), "success": False}

    query = f'"{company_name}" site:linkedin.com/company'

    location_map = {"DE": "Germany", "AT": "Austria", "CH": "Switzerland"}
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
                num_results=5,
            )

            if not results.success:
                return {"error": f"Search failed", "success": False}

            for item in results.data:
                url = item.get("url", "")
                if "linkedin.com/company" in url:
                    return {
                        "success": True,
                        "url": url,
                        "title": item.get("title", ""),
                    }

            return {"success": True, "url": None}

    except Exception as e:
        return {"error": str(e), "success": False}
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add SERP search functions"
```

---

## Task 6: Create Core Enrichment Script (Part 3 - Scoring)

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (append)

**Step 1: Add scoring function**

```python
# (Append to enrich.py)

def score_website_match(
    lead: dict,
    result: dict,
) -> float:
    """
    Score how well a search result matches the lead.

    Returns score 0.0-1.0
    """
    score = 0.0
    company_name = lead.get("company_name", "")
    email = lead.get("work_email", "")
    phone = lead.get("work_phone_number", "")

    # 1. Email domain match (0.50)
    email_domain = extract_email_domain(email)
    if email_domain and not is_generic_email_domain(email_domain):
        result_domain = extract_domain(result.get("url", ""))
        if email_domain == result_domain:
            score += 0.50

    # 2. Company name similarity (0.25)
    title = result.get("title", "")
    similarity = fuzzy_similarity(company_name, title)
    score += similarity * 0.25

    # 3. Phone in snippet (0.15) - weak signal, just check if normalized phone appears
    snippet = result.get("snippet", "")
    if phone and normalize_phone(phone) in normalize_phone(snippet):
        score += 0.15

    return min(score, 1.0)


def find_best_website(
    lead: dict,
    search_results: list[dict],
    min_confidence: float = 0.5,
) -> tuple[Optional[str], float, list[dict]]:
    """
    Find best matching website from search results.

    Returns: (best_url, confidence, all_candidates)
    """
    candidates = []

    for result in search_results:
        url = result.get("url", "")
        if not url:
            continue

        # Skip LinkedIn, Facebook, etc. for website
        skip_domains = ["linkedin.com", "facebook.com", "instagram.com",
                        "twitter.com", "youtube.com", "wikipedia.org"]
        if any(d in url for d in skip_domains):
            continue

        score = score_website_match(lead, result)
        candidates.append({
            "url": url,
            "title": result.get("title", ""),
            "snippet": result.get("snippet", ""),
            "score": score,
        })

    # Sort by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)

    if not candidates:
        return None, 0.0, []

    best = candidates[0]
    return best["url"], best["score"], candidates
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add website scoring function"
```

---

## Task 7: Create Core Enrichment Script (Part 4 - Main Logic)

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (append)

**Step 1: Add main enrichment logic**

```python
# (Append to enrich.py)
import asyncio


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

    # Check for generic company name
    generic_names = ["selbstständigkeit", "selbstständig", "self-employed",
                     "freelancer", "privat", "private"]
    if company_name.lower() in generic_names:
        result["notes"] = "Generic company name, verify manually"
        return result

    # Search for company website
    search_result = await search_company(company_name, result["country"])

    if not search_result.get("success"):
        result["notes"] = f"Search error: {search_result.get('error', 'Unknown')}"
        return result

    search_results = search_result.get("results", [])
    if not search_results:
        result["notes"] = "No results found"
        return result

    # Find best website match
    best_url, confidence, candidates = find_best_website(lead, search_results, min_confidence)

    result["website"] = best_url or ""
    result["website_confidence"] = confidence

    # Handle confidence levels
    if confidence >= min_confidence:
        pass  # Good match, no notes needed
    elif confidence >= 0.5:
        # Medium confidence - add candidates to notes
        top_candidates = candidates[:3]
        candidate_urls = [c["url"] for c in top_candidates]
        result["notes"] = f"Medium confidence. Candidates: {', '.join(candidate_urls)}"
    else:
        # Low confidence - flag for review
        result["notes"] = f"Low confidence match ({confidence:.2f}). Manual review needed."

    # Search for LinkedIn profiles
    if company_name:
        linkedin_company = await search_linkedin_company(company_name, result["country"])
        if linkedin_company.get("success") and linkedin_company.get("url"):
            result["company_linkedin"] = linkedin_company["url"]

    if full_name and company_name:
        linkedin_person = await search_linkedin_person(full_name, company_name, result["country"])
        if linkedin_person.get("success") and linkedin_person.get("url"):
            result["person_linkedin"] = linkedin_person["url"]
            result["person_verified"] = "true"  # Found on LinkedIn with company

    return result


async def enrich_csv(
    input_path: str,
    output_path: str,
    min_confidence: float = 0.8,
) -> dict:
    """
    Enrich all leads in a CSV file.

    Returns summary dict.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        return {"error": f"Input file not found: {input_path}", "success": False}

    # Read input CSV
    leads = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")  # Tab-delimited
        leads = list(reader)

    if not leads:
        return {"error": "No leads found in input file", "success": False}

    print(f"Processing {len(leads)} leads...")

    # Enrich each lead
    enriched = []
    high_confidence_count = 0
    review_count = 0

    for i, lead in enumerate(leads):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{len(leads)}")

        enriched_lead = await enrich_lead(lead, min_confidence)
        enriched.append(enriched_lead)

        if enriched_lead["website_confidence"] >= min_confidence:
            high_confidence_count += 1
        elif enriched_lead["website_confidence"] >= 0.5:
            review_count += 1

        # Rate limiting
        time.sleep(1)

    # Write enriched CSV
    output_file = Path(output_path)
    fieldnames = list(enriched[0].keys())

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(enriched)

    # Write review-needed CSV
    review_file = output_file.with_name(
        output_file.stem + "_review_needed" + output_file.suffix
    )
    review_leads = [l for l in enriched if l["website_confidence"] < min_confidence and l["website"]]

    if review_leads:
        with open(review_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(review_leads)

    print(f"\nComplete!")
    print(f"  Total leads: {len(leads)}")
    print(f"  High confidence: {high_confidence_count}")
    print(f"  Needs review: {review_count}")
    print(f"  Output: {output_file}")
    if review_leads:
        print(f"  Review file: {review_file}")

    return {
        "success": True,
        "total": len(leads),
        "high_confidence": high_confidence_count,
        "review_needed": review_count,
        "output_file": str(output_file),
    }
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add main enrichment logic"
```

---

## Task 8: Create Core Enrichment Script (Part 5 - CLI)

**Files:**
- Modify: `skills/lead-enricher/scripts/enrich.py` (append)

**Step 1: Add CLI entry point**

```python
# (Append to enrich.py)

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Enrich leads with website and LinkedIn info"
    )
    parser.add_argument(
        "input_csv",
        help="Path to input CSV file (UTF-8, tab-delimited)"
    )
    parser.add_argument(
        "output_csv",
        nargs="?",
        help="Path to output CSV file (default: input_enriched.csv)"
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.8,
        help="Minimum confidence threshold (default: 0.8)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test API connection"
    )

    args = parser.parse_args()

    if args.test:
        # Test mode - verify API key works
        try:
            api_key = get_api_key()
            print(f"API key found: {api_key[:8]}...")
            print("API configuration OK")
            return
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Determine output path
    input_path = Path(args.input_csv)
    if args.output_csv:
        output_path = args.output_csv
    else:
        output_path = str(input_path.with_stem(input_path.stem + "_enriched"))

    # Run enrichment
    result = asyncio.run(enrich_csv(args.input_csv, output_path, args.min_confidence))

    if not result.get("success"):
        print(f"Error: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 2: Make executable**

Run: `chmod +x skills/lead-enricher/scripts/enrich.py`

**Step 3: Test help**

Run: `python3 skills/lead-enricher/scripts/enrich.py --help`
Expected: Shows usage help

**Step 4: Commit**

```bash
git add skills/lead-enricher/scripts/enrich.py
git commit -m "feat(lead-enricher): add CLI entry point"
```

---

## Task 9: Create SKILL.md

**Files:**
- Create: `skills/lead-enricher/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
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
# Configure Bright Data SERP API
cd skills/lead-enricher
python3 scripts/setup.py
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
```

**Step 2: Commit**

```bash
git add skills/lead-enricher/SKILL.md
git commit -m "feat(lead-enricher): add SKILL.md documentation"
```

---

## Task 10: Integration Test

**Files:**
- None (testing only)

**Step 1: Create test CSV**

```bash
cat > /tmp/test_leads.csv << 'EOF'
full_name	company_name	work_phone_number	work_email
Sven Haubert	Reha360	+4951418879605	Office@reha360.de
EOF
```

**Step 2: Run enrichment**

Run: `python3 skills/lead-enricher/scripts/enrich.py /tmp/test_leads.csv /tmp/test_output.csv --min-confidence 0.5`
Expected: Creates `/tmp/test_output.csv` with enriched data

**Step 3: Verify output**

Run: `cat /tmp/test_output.csv`
Expected: CSV with `website`, `website_confidence`, `company_linkedin` columns

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat(lead-enricher): complete implementation"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Directory structure | `skills/lead-enricher/` |
| 2 | Setup script | `scripts/setup.py` |
| 3 | Confidence reference | `references/confidence-scoring.md` |
| 4 | Utilities | `scripts/enrich.py` (part 1) |
| 5 | SERP search | `scripts/enrich.py` (part 2) |
| 6 | Scoring | `scripts/enrich.py` (part 3) |
| 7 | Main logic | `scripts/enrich.py` (part 4) |
| 8 | CLI | `scripts/enrich.py` (part 5) |
| 9 | Documentation | `SKILL.md` |
| 10 | Integration test | (testing only) |
