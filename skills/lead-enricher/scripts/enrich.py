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
import aiohttp

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))
from brightdata_utils import get_api_key, LOCATION_MAP

# Configuration
CONFIG_DIR = Path.home() / ".claude" / "lead-enricher"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Email ISP domains organized by region (for maintainability)
# Combined into GENERIC_EMAIL_DOMAINS for efficient lookup

# Global / Multi-region
GLOBAL_EMAIL_DOMAINS = {
    "gmail.com", "outlook.com", "hotmail.com", "yahoo.com",
    "aol.com", "icloud.com", "mail.com", "live.com", "msn.com",
    "googlemail.com", "ymail.com", "protonmail.com", "zoho.com",
    "fastmail.com",
}

# North America
USA_EMAIL_DOMAINS = {
    "comcast.net", "verizon.net", "att.net", "bellsouth.net",
    "sbcglobal.net", "cox.net", "charter.net", "earthlink.net",
}
CANADA_EMAIL_DOMAINS = {
    "bell.net", "rogers.com", "shaw.ca", "telus.net",
    "sympatico.ca", "videotron.ca", "primus.ca",
}

# Europe
EU_WEST_EMAIL_DOMAINS = {
    # UK
    "btinternet.com", "sky.com", "virginmedia.com", "talktalk.net",
    # Ireland
    "eircom.net", "vodafone.ie",
    # France
    "orange.fr", "wanadoo.fr", "laposte.net", "free.fr", "sfr.fr",
    # Netherlands
    "ziggo.nl", "kpnmail.nl", "planet.nl",
    # Belgium
    "telenet.be", "skynet.be",
}
EU_DACH_EMAIL_DOMAINS = {
    # Germany
    "web.de", "gmx.de", "t-online.de", "online.de", "freenet.de", "1und1.de",
    # Austria
    "gmx.at", "aon.at", "chello.at",
    # Switzerland
    "gmx.ch", "bluewin.ch", "sunrise.ch",
}
EU_SOUTH_EMAIL_DOMAINS = {
    # Spain
    "telefonica.es", "terra.es", "movistar.es", "ono.com",
    # Italy
    "libero.it", "virgilio.it", "tin.it", "alice.it", "tim.it",
    # Portugal
    "sapo.pt", "netcabo.pt", "mail.pt",
}
EU_NORDIC_EMAIL_DOMAINS = {
    # Scandinavia
    "telenor.no", "telia.com", "tele2.se", "bredband.net",
    # Finland
    "luukku.com", "surffi.net", "kolumbus.fi",
    # Denmark
    "mail.dk", "ofir.dk", "get2net.dk",
}
EU_EAST_EMAIL_DOMAINS = {
    # Poland
    "wp.pl", "onet.pl", "interia.pl", "o2.pl",
    # Czech
    "seznam.cz", "centrum.cz", "email.cz",
    # Hungary
    "freemail.hu", "indamail.hu", "citromail.hu",
    # Russia/CIS
    "mail.ru", "yandex.ru", "rambler.ru", "bk.ru",
}

# Asia-Pacific
ASIA_EAST_EMAIL_DOMAINS = {
    # China
    "qq.com", "163.com", "126.com", "sina.com", "sohu.com",
    "aliyun.com", "139.com", "yeah.net",
    # Japan
    "docomo.ne.jp", "softbank.ne.jp", "ezweb.ne.jp",
    "yahoo.co.jp", "goo.ne.jp", "au.com",
    # South Korea
    "naver.com", "daum.net", "hanmail.net", "kakao.com",
}
ASIA_SOUTH_EMAIL_DOMAINS = {
    # India
    "rediffmail.com", "indiainfo.com", "vsnl.com", "airtelmail.in",
    # Pakistan
    "cyber.net.pk", "wol.net.pk",
}
ASIA_SOUTHEAST_EMAIL_DOMAINS = {
    # Singapore
    "singnet.com.sg", "starhub.net.sg", "pacific.net.sg",
    # Malaysia
    "tm.net.my", "streamyx.com", "celcom.net.my",
    # Indonesia
    "telkom.net", "plasa.com", "indosat.net.id",
    # Thailand
    "truemail.co.th", "sanook.com", "csloxinfo.com",
    # Philippines
    "pldtdsl.net", "globe.com.ph",
    # Vietnam
    "vnptmail.vn", "fpt.vn", "viettel.com.vn",
}
OCEANIA_EMAIL_DOMAINS = {
    # Australia
    "bigpond.com", "optusnet.com.au", "iinet.net.au", "tpg.com.au",
    "dodo.com.au", "internode.on.net", "westnet.com.au",
    # New Zealand
    "xtra.co.nz", "vodafone.co.nz", "slingshot.co.nz",
}

# Middle East & Africa
MIDDLE_EAST_EMAIL_DOMAINS = {
    # UAE/Gulf
    "etisalat.ae", "du.ae", "eim.ae",
    # Saudi Arabia
    "stc.com.sa", "mobily.com.sa",
    # Israel
    "walla.co.il", "netvision.net.il", "012.net.il",
    # Turkey
    "turkcell.com.tr", "ttmail.com", "superonline.com",
    # Egypt
    "te.eg", "link.net", "tedata.net",
}
AFRICA_EMAIL_DOMAINS = {
    # South Africa
    "telkomsa.net", "vodamail.co.za", "mweb.co.za",
    "iafrica.com", "webmail.co.za", "absamail.co.za",
    # Kenya
    "safaricom.co.ke", "kenyaweb.com",
    # Nigeria
    "yahoo.com.ng", "gmail.com.ng",
}

# Latin America
LATIN_AMERICA_EMAIL_DOMAINS = {
    # Brazil
    "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br",
    # Mexico
    "prodigy.net.mx", "terra.com.mx", "hotmail.com.mx",
    # Argentina
    "arnet.com.ar", "ciudad.com.ar", "fibertel.com.ar",
    # Chile
    "vtr.net", "terra.cl", "entel.cl",
    # Colombia
    "etb.net.co", "une.net.co", "tigo.com.co",
    # Peru
    "speedy.com.pe", "infonegocio.net.pe",
}

# Combined set for efficient lookup
GENERIC_EMAIL_DOMAINS = (
    GLOBAL_EMAIL_DOMAINS |
    USA_EMAIL_DOMAINS |
    CANADA_EMAIL_DOMAINS |
    EU_WEST_EMAIL_DOMAINS |
    EU_DACH_EMAIL_DOMAINS |
    EU_SOUTH_EMAIL_DOMAINS |
    EU_NORDIC_EMAIL_DOMAINS |
    EU_EAST_EMAIL_DOMAINS |
    ASIA_EAST_EMAIL_DOMAINS |
    ASIA_SOUTH_EMAIL_DOMAINS |
    ASIA_SOUTHEAST_EMAIL_DOMAINS |
    OCEANIA_EMAIL_DOMAINS |
    MIDDLE_EAST_EMAIL_DOMAINS |
    AFRICA_EMAIL_DOMAINS |
    LATIN_AMERICA_EMAIL_DOMAINS
)


# get_api_key is now imported from shared.brightdata_utils


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


def extract_linkedin_company_data(html: str) -> dict:
    """
    Extract employee count and industry from LinkedIn company page HTML.

    Returns dict with employee_count, industry, followers.
    """
    import json as json_module

    result = {
        "employee_count": None,
        "industry": None,
        "followers": None,
    }

    # 1. Extract from JSON-LD structured data (most reliable for employee count)
    ld_json_match = re.search(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE
    )
    if ld_json_match:
        try:
            data = json_module.loads(ld_json_match.group(1))

            # Handle @graph structure (nested)
            if isinstance(data, dict) and "@graph" in data:
                for item in data["@graph"]:
                    if isinstance(item, dict) and item.get("@type") == "Organization":
                        data = item
                        break

            # Handle array structure
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Organization":
                        data = item
                        break

            if isinstance(data, dict) and "numberOfEmployees" in data:
                emp = data["numberOfEmployees"]
                if isinstance(emp, dict) and "value" in emp:
                    result["employee_count"] = str(emp["value"])
                elif isinstance(emp, (int, str)):
                    result["employee_count"] = str(emp)
        except json_module.JSONDecodeError:
            pass

    # 2. Extract followers from meta description
    followers_match = re.search(
        r'(\d[\d,\.]*)\s*followers?\s+on\s+LinkedIn',
        html, re.IGNORECASE
    )
    if followers_match:
        result["followers"] = followers_match.group(1).replace(",", "").replace(".", "")

    # 3. Extract industry from about-us section
    industry_match = re.search(
        r'about-us__industry[^>]*>.*?<dd[^>]*>([^<]+)</dd>',
        html, re.DOTALL | re.IGNORECASE
    )
    if industry_match:
        result["industry"] = industry_match.group(1).strip()

    return result


async def scrape_linkedin_company(linkedin_url: str, verbose: bool = False) -> dict:
    """
    Scrape a LinkedIn company page to extract employee count and industry.

    Returns dict with employee_count, industry, followers, or error.
    """
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {"error": "brightdata-sdk not installed", "success": False}

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {"error": str(e), "success": False}

    try:
        async with BrightDataClient(
            token=api_key,
            validate_token=False,
            auto_create_zones=False,
        ) as client:
            if verbose:
                print(f"  [LinkedIn] Scraping company page: {linkedin_url}")

            result = await client.scrape_url(linkedin_url)

            if not result.success:
                return {"error": f"Scrape failed: {result.error}", "success": False}

            data = extract_linkedin_company_data(result.data)

            if verbose:
                emp = data.get("employee_count") or "N/A"
                ind = data.get("industry") or "N/A"
                print(f"  [LinkedIn] Extracted: employees={emp}, industry={ind}")

            return {
                "success": True,
                "employee_count": data.get("employee_count"),
                "industry": data.get("industry"),
                "followers": data.get("followers"),
            }

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
    verbose: bool = False,
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
        if verbose:
            print(f"  [Strategy 1] Trying direct website: https://{email_domain}/")
        direct_url, success = await try_direct_website(email_domain)
        if success:
            result["website"] = direct_url
            result["website_confidence"] = 0.9  # High confidence - exact domain match
            website_found = True
            if verbose:
                print(f"  [Strategy 1] ✅ Direct website found: {direct_url} (confidence: 0.9)")

    # Strategy 2: Search by email (non-generic emails only)
    if not website_found and not is_generic_email and email:
        if verbose:
            print(f"  [Strategy 2] Searching by email: \"{email}\"")
        email_search = await search_by_email(email, result["country"])
        if email_search.get("success"):
            email_results = email_search.get("results", [])
            if verbose:
                print(f"  [Strategy 2] Found {len(email_results)} results")
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
                        result["website_confidence"] = 0.9  # High confidence - email search + exact domain match
                        website_found = True
                        if verbose:
                            print(f"  [Strategy 2] ✅ Domain match found: {url} (confidence: 0.9)")
                        break

    # Strategy 3: Search by company name (fallback)
    if not website_found:
        if verbose:
            print(f"  [Strategy 3] Searching by company name: \"{company_name}\"")
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
        if verbose:
            print(f"  [LinkedIn] Searching for company: \"{company_name}\"")
        linkedin_company = await search_linkedin_company(company_name, result["country"])
        if linkedin_company.get("success") and linkedin_company.get("url"):
            # Validate LinkedIn result
            if validate_linkedin_result(company_name, linkedin_company["url"], linkedin_company.get("title", "")):
                result["company_linkedin"] = linkedin_company["url"]
                if verbose:
                    print(f"  [LinkedIn] ✅ Company page validated: {linkedin_company['url']}")

                # Scrape company page for employee count and industry
                company_data = await scrape_linkedin_company(linkedin_company["url"], verbose)
                if company_data.get("success"):
                    if company_data.get("employee_count"):
                        result["employee_count"] = company_data["employee_count"]
                    if company_data.get("industry"):
                        result["industry"] = company_data["industry"]
            else:
                if verbose:
                    print(f"  [LinkedIn] ⚠️ Result rejected by validation: {linkedin_company['url']}")
        elif verbose:
            print(f"  [LinkedIn] No company page found")

    if full_name and company_name:
        if verbose:
            print(f"  [LinkedIn] Searching for person: \"{full_name}\" at \"{company_name}\"")
        linkedin_person = await search_linkedin_person(full_name, company_name, result["country"])
        if linkedin_person.get("success") and linkedin_person.get("url"):
            result["person_linkedin"] = linkedin_person["url"]
            result["person_verified"] = "true"  # Found on LinkedIn with company
            if verbose:
                print(f"  [LinkedIn] ✅ Person profile found: {linkedin_person['url']}")
        elif verbose:
            print(f"  [LinkedIn] No person profile found")

    return result


async def enrich_csv(
    input_path: str,
    output_path: str,
    min_confidence: float = 0.8,
    verbose: bool = False,
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

        enriched_lead = await enrich_lead(lead, min_confidence, verbose)
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
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress and debugging info"
    )

    args = parser.parse_args()

    if args.test:
        # Test mode - verify API key works
        try:
            api_key = get_api_key()
            print(f"API key configured: ...{api_key[-4:]}")
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
    result = asyncio.run(enrich_csv(args.input_csv, output_path, args.min_confidence, args.verbose))

    if not result.get("success"):
        print(f"Error: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
