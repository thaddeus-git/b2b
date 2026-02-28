#!/usr/bin/env python3
"""
Bright Data SERP API search script for distributor-inspector skill.

API Key Configuration:
  1. Set BRIGHTDATA_SERP_API_KEY environment variable, or
  2. Edit ~/.claude/distributor-inspector/config.json and add your API key

Requirements:
  - brightdata-sdk (auto-installed by setup.py)

Usage (from skill):
  python3 scripts/search.py <query> <country> <language> <num_results>

Example:
  python3 scripts/search.py "best restaurants" "US" "en" "10"
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))
from brightdata_utils import get_api_key as shared_get_api_key, LOCATION_MAP


CONFIG_DIR = Path.home() / ".claude" / "distributor-inspector"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_api_key() -> str:
    """Get API key using shared utility with distributor-inspector config."""
    return shared_get_api_key("distributor-inspector")


def ensure_sdk_installed():
    """Ensure brightdata-sdk is installed."""
    try:
        import brightdata
    except ImportError:
        print(
            json.dumps({
                "error": "brightdata-sdk not installed. Run: pip install brightdata-sdk",
                "success": False
            }),
            file=sys.stderr
        )
        sys.exit(1)


def country_code_to_location(country_code: str) -> str:
    """Convert country code to location name using shared LOCATION_MAP."""
    return LOCATION_MAP.get(country_code.upper(), country_code)


async def search_google(
    query: str,
    country_code: str = "US",
    language: str = "en",
    num_results: int = 20,
) -> dict:
    """
    Search Google using Bright Data SERP API.

    Args:
        query: Search query string
        country_code: 2-letter country code (default: US)
        language: Language code (default: en)
        num_results: Number of results to return (default: 20)

    Returns:
        Dict with search results or error
    """
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {
            "error": "brightdata-sdk not installed. Run: pip install brightdata-sdk",
            "success": False,
            "query": query
        }

    try:
        api_key = get_api_key()
    except ValueError as e:
        return {
            "error": str(e),
            "success": False,
            "query": query
        }

    location = country_code_to_location(country_code)

    try:
        async with BrightDataClient(
            token=api_key,
            validate_token=False,
            auto_create_zones=False,
        ) as client:
            results = await client.search.google(
                query=query,
                location=location,
                language=language,
                num_results=num_results,
            )

            if not results.success:
                return {
                    "error": f"Search failed: {results.error}",
                    "success": False,
                    "query": query
                }

            mapped_results = []
            for item in results.data:
                mapped_results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                })

            return {
                "success": True,
                "query": query,
                "country": country_code,
                "language": language,
                "count": len(mapped_results),
                "results": mapped_results
            }

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "query": query
        }


async def search_batch(
    queries: list[str],
    country_code: str = "US",
    language: str = "en",
    num_results: int = 20,
) -> dict:
    """
    Search multiple queries in parallel.

    Args:
        queries: List of search queries
        country_code: 2-letter country code (default: US)
        language: Language code (default: en)
        num_results: Number of results per query (default: 20)

    Returns:
        Dict with all search results
    """
    tasks = [search_google(q, country_code, language, num_results) for q in queries]
    all_results = await asyncio.gather(*tasks)

    return {
        "success": True,
        "queries": queries,
        "country": country_code,
        "language": language,
        "results_by_query": {q: r for q, r in zip(queries, all_results)},
        "total_queries": len(queries),
    }


async def main():
    """CLI entry point."""
    # Batch mode: --batch <json_queries> <country> <language> <num_results>
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: --batch <queries_json> [country] [language] [num_results]"}))
            sys.exit(1)

        queries_json = sys.argv[2]
        country_code = sys.argv[3] if len(sys.argv) > 3 else "US"
        language = sys.argv[4] if len(sys.argv) > 4 else "en"
        num_results = int(sys.argv[5]) if len(sys.argv) > 5 else 20

        try:
            queries = json.loads(queries_json)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON for queries"}))
            sys.exit(1)

        result = await search_batch(queries, country_code, language, num_results)
        print(json.dumps(result, indent=2))
        return

    # Single query mode: <query> [country] [language] [num_results]
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: search.py <query> [country] [language] [num_results]",
            "example": 'python search.py "best restaurants" "US" "en" "10"'
        }))
        sys.exit(1)

    query = sys.argv[1]
    country_code = sys.argv[2] if len(sys.argv) > 2 else "US"
    language = sys.argv[3] if len(sys.argv) > 3 else "en"
    num_results = int(sys.argv[4]) if len(sys.argv) > 4 else 20

    result = await search_google(query, country_code, language, num_results)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
