#!/usr/bin/env python3
"""
Unified SERP search script using Bright Data API.

Consolidates search functionality from:
- distributor-inspector/scripts/search.py
- lead-enricher/scripts/enrich.py

API Key Configuration:
  1. Set BRIGHTDATA_SERP_API_KEY environment variable, or
  2. Edit ~/.claude/{skill_name}/config.json and add your API key

Requirements:
  - brightdata-sdk (pip install brightdata-sdk)

Usage Examples:

  # General web search
  python3 serp_search.py "cleaning robot distributor France" "FR" "fr" "20"

  # LinkedIn company search
  python3 serp_search.py --linkedin-company "Acme Corp" "DE" "de" "10"

  # LinkedIn person search
  python3 serp_search.py --linkedin-person "John Doe" "Acme Corp" "DE"

  # Batch search (JSON queries)
  python3 serp_search.py --batch '["query1", "query2"]' "US" "en" "10"

Output:
  JSON to stdout with results or error
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from brightdata_utils import get_api_key, country_to_location


def ensure_sdk_installed():
    """Ensure brightdata-sdk is installed."""
    try:
        import brightdata
    except ImportError:
        print(
            json.dumps(
                {
                    "error": "brightdata-sdk not installed. Run: pip install brightdata-sdk",
                    "success": False,
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)


async def search_google(
    query: str,
    country_code: str = "US",
    language: str = "en",
    num_results: int = 20,
    skill_name: str = "lead-enricher",
) -> dict:
    """
    Search Google using Bright Data SERP API.

    Args:
        query: Search query string
        country_code: 2-letter country code (default: US)
        language: Language code (default: en)
        num_results: Number of results to return (default: 20)
        skill_name: Skill name for config lookup (default: lead-enricher)

    Returns:
        Dict with search results or error
    """
    try:
        from brightdata import BrightDataClient
    except ImportError:
        return {
            "error": "brightdata-sdk not installed. Run: pip install brightdata-sdk",
            "success": False,
            "query": query,
        }

    try:
        api_key = get_api_key(skill_name)
    except ValueError as e:
        return {"error": str(e), "success": False, "query": query}

    location = country_to_location(country_code)

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
                    "query": query,
                }

            mapped_results = []
            for item in results.data:
                mapped_results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("description", ""),
                    }
                )

            return {
                "success": True,
                "query": query,
                "country": country_code,
                "language": language,
                "count": len(mapped_results),
                "results": mapped_results,
            }

    except Exception as e:
        return {"error": str(e), "success": False, "query": query}


async def search_linkedin_company(
    company_name: str,
    country_code: str = "DE",
    language: str = "en",
    num_results: int = 10,
    skill_name: str = "lead-enricher",
) -> dict:
    """
    Search for company's LinkedIn page.

    Args:
        company_name: Company name to search for
        country_code: 2-letter country code
        language: Language code
        num_results: Number of results to return
        skill_name: Skill name for config lookup

    Returns:
        Dict with LinkedIn URL or error
    """
    query = f'"{company_name}" site:linkedin.com/company'
    result = await search_google(query, country_code, language, num_results, skill_name)

    if not result.get("success"):
        return result

    for item in result.get("results", []):
        url = item.get("url", "")
        if "linkedin.com/company" in url:
            return {
                "success": True,
                "company_name": company_name,
                "linkedin_url": url,
                "title": item.get("title", ""),
            }

    return {
        "success": True,
        "company_name": company_name,
        "linkedin_url": None,
        "message": "No LinkedIn company page found",
    }


async def search_linkedin_person(
    full_name: str,
    company_name: str,
    country_code: str = "DE",
    language: str = "en",
    skill_name: str = "lead-enricher",
) -> dict:
    """
    Search for person's LinkedIn profile.

    Args:
        full_name: Person's full name
        company_name: Company name
        country_code: 2-letter country code
        language: Language code
        skill_name: Skill name for config lookup

    Returns:
        Dict with LinkedIn URL or error
    """
    query = f'"{full_name}" "{company_name}" site:linkedin.com/in'
    result = await search_google(query, country_code, language, 5, skill_name)

    if not result.get("success"):
        return result

    for item in result.get("results", []):
        url = item.get("url", "")
        if "linkedin.com/in" in url:
            return {
                "success": True,
                "full_name": full_name,
                "company_name": company_name,
                "linkedin_url": url,
                "title": item.get("title", ""),
            }

    return {
        "success": True,
        "full_name": full_name,
        "company_name": company_name,
        "linkedin_url": None,
        "message": "No LinkedIn person profile found",
    }


async def search_batch(
    queries: list[str],
    country_code: str = "US",
    language: str = "en",
    num_results: int = 20,
    skill_name: str = "lead-enricher",
) -> dict:
    """
    Search multiple queries in parallel.

    Args:
        queries: List of search queries
        country_code: 2-letter country code (default: US)
        language: Language code (default: en)
        num_results: Number of results per query (default: 20)
        skill_name: Skill name for config lookup

    Returns:
        Dict with all search results
    """
    tasks = [
        search_google(q, country_code, language, num_results, skill_name)
        for q in queries
    ]
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
    parser = argparse.ArgumentParser(
        description="Unified SERP search using Bright Data API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # General web search
  %(prog)s "cleaning robot distributor" "FR" "fr" "20"

  # LinkedIn company search
  %(prog)s --linkedin-company "Acme Corp" "DE" "de" "10"

  # LinkedIn person search
  %(prog)s --linkedin-person "John Doe" "Acme Corp" "DE"

  # Batch search
  %(prog)s --batch '["query1", "query2"]' "US" "en" "10"
        """,
    )

    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "country", nargs="?", default="US", help="Country code (default: US)"
    )
    parser.add_argument(
        "language", nargs="?", default="en", help="Language code (default: en)"
    )
    parser.add_argument(
        "num_results",
        nargs="?",
        type=int,
        default=20,
        help="Number of results (default: 20)",
    )

    parser.add_argument(
        "--batch", metavar="QUERIES_JSON", help="Batch mode: JSON array of queries"
    )
    parser.add_argument(
        "--linkedin-company",
        metavar="COMPANY_NAME",
        help="Search for LinkedIn company page",
    )
    parser.add_argument(
        "--linkedin-person",
        nargs=2,
        metavar=("FULL_NAME", "COMPANY_NAME"),
        help="Search for LinkedIn person profile",
    )
    parser.add_argument(
        "--skill",
        default="lead-enricher",
        help="Skill name for config lookup (default: lead-enricher)",
    )

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        try:
            queries = json.loads(args.batch)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON for queries", "success": False}))
            sys.exit(1)

        result = await search_batch(
            queries, args.country, args.language, args.num_results, args.skill
        )
        print(json.dumps(result, indent=2))
        return

    # LinkedIn company search
    if args.linkedin_company:
        result = await search_linkedin_company(
            args.linkedin_company,
            args.country,
            args.language,
            args.num_results,
            args.skill,
        )
        print(json.dumps(result, indent=2))
        return

    # LinkedIn person search
    if args.linkedin_person:
        full_name, company_name = args.linkedin_person
        result = await search_linkedin_person(
            full_name, company_name, args.country, args.language, args.skill
        )
        print(json.dumps(result, indent=2))
        return

    # General web search
    if not args.query:
        print(
            json.dumps(
                {
                    "error": "Usage: serp_search.py <query> [country] [language] [num_results]",
                    "example": 'python serp_search.py "cleaning robot distributor" "FR" "fr" "20"',
                }
            )
        )
        sys.exit(1)

    result = await search_google(
        args.query, args.country, args.language, args.num_results, args.skill
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    ensure_sdk_installed()
    asyncio.run(main())
