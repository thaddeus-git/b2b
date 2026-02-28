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
