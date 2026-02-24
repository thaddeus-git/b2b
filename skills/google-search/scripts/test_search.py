#!/usr/bin/env python3
"""
Test script for google-search skill.

Tests:
1. SDK installation
2. API key validation
3. Single search
4. Batch search
5. Error handling

Usage:
  BRIGHTDATA_SERP_API_KEY="xxx" python scripts/test_search.py
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path


# Add skill directory to path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir / "scripts"))
from search import search_google, search_batch, get_api_key, ensure_sdk_installed


class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []

    def add_pass(self, name):
        self.passed.append(name)
        print(f"  ✅ {name}")

    def add_fail(self, name, reason):
        self.failed.append((name, reason))
        print(f"  ❌ {name}: {reason}")

    def summary(self):
        print(f"\n=== Test Summary ===")
        print(f"Passed: {len(self.passed)}")
        print(f"Failed: {len(self.failed)}")
        return len(self.failed) == 0


async def test_sdk_installation(results):
    """Test SDK is installed."""
    print("\n--- Testing SDK Installation ---")
    try:
        ensure_sdk_installed()
        import brightdata
        results.add_pass("SDK installed")
    except Exception as e:
        results.add_fail("SDK installation", str(e))


async def test_api_key_validation(results):
    """Test API key is set."""
    print("\n--- Testing API Key Validation ---")
    try:
        api_key = get_api_key()
        if api_key:
            results.add_pass(f"API key set (length: {len(api_key)})")
        else:
            results.add_fail("API key", "Empty API key")
    except ValueError as e:
        results.add_fail("API key", str(e))


async def test_single_search(results):
    """Test single search."""
    print("\n--- Testing Single Search ---")
    try:
        result = await search_google("test query", "US", "en", 5)
        if result.get("success"):
            results.add_pass(f"Single search (found {result.get('count')} results)")
        else:
            results.add_fail("Single search", result.get("error", "Unknown error"))
    except Exception as e:
        results.add_fail("Single search", str(e))


async def test_batch_search(results):
    """Test batch search."""
    print("\n--- Testing Batch Search ---")
    try:
        queries = ["test query 1", "test query 2"]
        result = await search_batch(queries, "US", "en", 5)
        if result.get("success"):
            results.add_pass(f"Batch search ({len(queries)} queries)")
        else:
            results.add_fail("Batch search", result.get("error", "Unknown error"))
    except Exception as e:
        results.add_fail("Batch search", str(e))


async def test_error_handling(results):
    """Test error handling."""
    print("\n--- Testing Error Handling ---")
    try:
        # Empty query should fail gracefully
        result = await search_google("", "US", "en", 5)
        if not result.get("success"):
            results.add_pass("Error handling - empty query")
        else:
            results.add_fail("Error handling", "Empty query should fail")
    except Exception as e:
        results.add_fail("Error handling", str(e))


async def test_cli_single_search(results):
    """Test CLI single search."""
    print("\n--- Testing CLI Single Search ---")
    try:
        result = subprocess.run(
            [sys.executable, str(skill_dir / "scripts" / "search.py"), "test", "US", "en", "3"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = json.loads(result.stdout)
        if output.get("success"):
            results.add_pass(f"CLI single search (found {output.get('count')} results)")
        else:
            results.add_fail("CLI single search", output.get("error", "Unknown error"))
    except subprocess.TimeoutExpired:
        results.add_fail("CLI single search", "Timeout")
    except Exception as e:
        results.add_fail("CLI single search", str(e))


async def test_cli_batch_search(results):
    """Test CLI batch search."""
    print("\n--- Testing CLI Batch Search ---")
    try:
        result = subprocess.run(
            [sys.executable, str(skill_dir / "scripts" / "search.py"), "--batch", '["test1", "test2"]', "US", "en", "3"],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = json.loads(result.stdout)
        if output.get("success"):
            results.add_pass(f"CLI batch search ({output.get('total_queries')} queries)")
        else:
            results.add_fail("CLI batch search", output.get("error", "Unknown error"))
    except subprocess.TimeoutExpired:
        results.add_fail("CLI batch search", "Timeout")
    except Exception as e:
        results.add_fail("CLI batch search", str(e))


async def main():
    """Run all tests."""
    print("=" * 50)
    print("Google Search Skill Tests")
    print("=" * 50)

    results = TestResults()

    # Always run SDK test first
    await test_sdk_installation(results)

    # Check if API key is set (env var or config file)
    try:
        api_key = get_api_key()
    except ValueError:
        print("\n⚠️  API key not found")
        print("   Set BRIGHTDATA_SERP_API_KEY or edit ~/.claude/google-search/config.json")
        results.summary()
        return 1

    # Run all tests
    await test_api_key_validation(results)
    await test_single_search(results)
    await test_batch_search(results)
    await test_error_handling(results)
    await test_cli_single_search(results)
    await test_cli_batch_search(results)

    # Summary
    all_passed = results.summary()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
