#!/usr/bin/env python3
"""Unit tests for serp_search.py."""

import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import modules
import brightdata_utils
import serp_search


class TestSearchGoogle:
    """Tests for search_google function."""

    @pytest.mark.asyncio
    async def test_successful_search(self):
        """Test successful Google search returns results."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = [
            {"title": "Result 1", "url": "https://example.com/1", "description": "Desc 1"},
            {"title": "Result 2", "url": "https://example.com/2", "description": "Desc 2"},
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_google("test query", "US", "en", 10)

        assert result["success"] is True
        assert result["query"] == "test query"
        assert result["country"] == "US"
        assert result["count"] == 2
        assert len(result["results"]) == 2
        assert result["results"][0]["title"] == "Result 1"

    @pytest.mark.asyncio
    async def test_search_failure(self):
        """Test search failure returns error."""
        mock_results = MagicMock()
        mock_results.success = False
        mock_results.error = "API rate limit exceeded"

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_google("test query", "US", "en", 10)

        assert result["success"] is False
        assert "rate limit" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_missing_api_key(self):
        """Test missing API key returns error."""
        with patch.object(serp_search, "get_api_key", return_value=""):
            result = await serp_search.search_google("test query", "US", "en", 10)

        assert result["success"] is False
        assert "error" in result


class TestSearchLinkedinCompany:
    """Tests for search_linkedin_company function."""

    @pytest.mark.asyncio
    async def test_finds_linkedin_company_page(self):
        """Test finding LinkedIn company page."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = [
            {"title": "Acme Corp | LinkedIn", "url": "https://linkedin.com/company/acme-corp", "description": ""},
            {"title": "Other Result", "url": "https://example.com", "description": ""},
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_linkedin_company("Acme Corp", "US", "en", 10)

        assert result["success"] is True
        assert result["linkedin_url"] == "https://linkedin.com/company/acme-corp"
        assert result["company_name"] == "Acme Corp"

    @pytest.mark.asyncio
    async def test_no_linkedin_page_found(self):
        """Test when no LinkedIn page is found."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = [
            {"title": "Some Other Result", "url": "https://example.com", "description": ""},
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_linkedin_company("Unknown Company", "US", "en", 10)

        assert result["success"] is True
        assert result["linkedin_url"] is None
        assert "No LinkedIn company page found" in result["message"]


class TestSearchLinkedinPerson:
    """Tests for search_linkedin_person function."""

    @pytest.mark.asyncio
    async def test_finds_person_profile(self):
        """Test finding LinkedIn person profile."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = [
            {"title": "John Doe - CEO at Acme | LinkedIn", "url": "https://linkedin.com/in/john-doe-123", "description": ""},
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_linkedin_person("John Doe", "Acme", "US", "en")

        assert result["success"] is True
        assert result["linkedin_url"] == "https://linkedin.com/in/john-doe-123"
        assert result["full_name"] == "John Doe"

    @pytest.mark.asyncio
    async def test_no_person_profile_found(self):
        """Test when no person profile is found."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = []

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_linkedin_person("Unknown Person", "Unknown Co", "US", "en")

        assert result["success"] is True
        assert result["linkedin_url"] is None


class TestSearchBatch:
    """Tests for search_batch function."""

    @pytest.mark.asyncio
    async def test_batch_search_multiple_queries(self):
        """Test batch search with multiple queries."""
        mock_results = MagicMock()
        mock_results.success = True
        mock_results.data = [{"title": "Result", "url": "https://example.com", "description": ""}]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.search.google = AsyncMock(return_value=mock_results)

        with patch.object(serp_search, "get_api_key", return_value="test_key"):
            with patch("brightdata.BrightDataClient", return_value=mock_client):
                result = await serp_search.search_batch(
                    ["query 1", "query 2", "query 3"],
                    "US",
                    "en",
                    10
                )

        assert result["success"] is True
        assert result["total_queries"] == 3
        assert len(result["results_by_query"]) == 3


class TestCountryToLocationDelegation:
    """Tests for country_to_location delegation in serp_search."""

    def test_delegates_to_utils(self):
        """serp_search should delegate to brightdata_utils."""
        # Both should return same results
        assert serp_search.country_to_location("DE") == brightdata_utils.country_to_location("DE")
        assert serp_search.country_to_location("US") == brightdata_utils.country_to_location("US")
        assert serp_search.country_to_location("XX") == brightdata_utils.country_to_location("XX")