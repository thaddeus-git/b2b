#!/usr/bin/env python3
"""
Shared utilities for Bright Data API integration.

Used by:
- lead-enricher/scripts/enrich.py
- distributor-inspector/scripts/search.py
"""

import json
import os
from pathlib import Path
from typing import Optional

# Country code to location name mapping
LOCATION_MAP = {
    # Europe
    "DE": "Germany", "AT": "Austria", "CH": "Switzerland",
    "FR": "France", "ES": "Spain", "NL": "Netherlands",
    "BE": "Belgium", "IT": "Italy", "PL": "Poland",
    "CZ": "Czech Republic", "PT": "Portugal", "IE": "Ireland",
    "SE": "Sweden", "NO": "Norway", "DK": "Denmark", "FI": "Finland",
    "GR": "Greece", "RU": "Russia",
    # North America
    "US": "United States", "CA": "Canada", "MX": "Mexico",
    # South America
    "BR": "Brazil", "AR": "Argentina", "CL": "Chile", "CO": "Colombia", "PE": "Peru",
    # Asia-Pacific
    "JP": "Japan", "KR": "South Korea", "CN": "China", "IN": "India",
    "AU": "Australia", "NZ": "New Zealand", "SG": "Singapore",
    "MY": "Malaysia", "TH": "Thailand", "VN": "Vietnam", "ID": "Indonesia",
    "PH": "Philippines", "HK": "Hong Kong", "TW": "Taiwan",
    # Middle East & Africa
    "AE": "United Arab Emirates", "SA": "Saudi Arabia", "IL": "Israel", "TR": "Turkey",
    "EG": "Egypt", "NG": "Nigeria", "KE": "Kenya", "ZA": "South Africa",
}


def get_api_key(config_subdir: str = "lead-enricher") -> str:
    """
    Get Bright Data API key from environment or config file.

    Args:
        config_subdir: Subdirectory name under ~/.claude/ for config file

    Priority:
        1. BRIGHTDATA_SERP_API_KEY environment variable
        2. ~/.claude/{config_subdir}/config.json

    Returns:
        API key string

    Raises:
        ValueError: If API key not found
    """
    # Check environment variable first
    api_key = os.environ.get("BRIGHTDATA_SERP_API_KEY", "")
    if api_key:
        return api_key

    # Fallback to config file
    config_file = Path.home() / ".claude" / config_subdir / "config.json"
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key", "")
                if api_key:
                    return api_key
        except (json.JSONDecodeError, IOError):
            pass

    raise ValueError(
        f"API key not found. Set BRIGHTDATA_SERP_API_KEY or edit {config_file}"
    )


async def create_client(api_key: str):
    """
    Create a Bright Data client with standard settings.

    Args:
        api_key: Bright Data API key

    Returns:
        BrightDataClient instance (async context manager)
    """
    from brightdata import BrightDataClient

    return BrightDataClient(
        token=api_key,
        validate_token=False,
        auto_create_zones=False,
    )


def country_to_location(country_code: str) -> str:
    """
    Convert country code to location name for Bright Data API.

    Args:
        country_code: 2-letter country code (e.g., "DE", "US")

    Returns:
        Location name (e.g., "Germany", "United States")
    """
    return LOCATION_MAP.get(country_code.upper(), country_code)
