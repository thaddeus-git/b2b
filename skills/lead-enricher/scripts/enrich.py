#!/usr/bin/env python3
"""
Lead enrichment script using Bright Data SERP API.

Usage:
  python3 scripts/enrich.py <input_csv> [output_csv] [--min-confidence 0.8]

Example:
  python3 scripts/enrich.py leads.csv leads_enriched.csv
"""

import argparse
import asyncio
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
