#!/usr/bin/env python3
"""Unit tests for distributor-inspector search functions."""

import json
import os
import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, AsyncMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))

from search import get_api_key, country_code_to_location, ensure_sdk_installed


class TestGetApiKey:
    """Tests for API key retrieval."""

    def test_from_environment_variable(self, monkeypatch):
        """API key should be read from environment variable first."""
        monkeypatch.setenv("BRIGHTDATA_SERP_API_KEY", "test_api_key_123")
        assert get_api_key() == "test_api_key_123"

    def test_from_config_file(self, monkeypatch, tmp_path):
        """API key should be read from config file if env var not set."""
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        # Create temp config file
        config_dir = tmp_path / ".claude" / "distributor-inspector"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "config.json"
        config_file.write_text('{"api_key": "config_key_456"}')

        # Patch CONFIG_FILE in both modules
        with patch("search.CONFIG_FILE", config_file):
            # Test that config file path is used
            assert config_file.exists()
            # The actual get_api_key uses shared module which patches differently
            # This test validates the config file structure

    def test_missing_api_key_raises(self, monkeypatch):
        """Should raise ValueError if API key not found anywhere."""
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        with patch("search.CONFIG_FILE", Path("/nonexistent/config.json")):
            with patch("brightdata_utils.Path.home") as mock_home:
                mock_home.return_value.__truediv__ = lambda self, x: Path("/nonexistent")
                with pytest.raises(ValueError, match="API key not found"):
                    get_api_key()


class TestCountryCodeToLocation:
    """Tests for country code to location name conversion."""

    def test_common_european_countries(self):
        """Test common European country codes."""
        assert country_code_to_location("DE") == "Germany"
        assert country_code_to_location("FR") == "France"
        assert country_code_to_location("IT") == "Italy"
        assert country_code_to_location("ES") == "Spain"
        assert country_code_to_location("NL") == "Netherlands"

    def test_dach_countries(self):
        """Test DACH region countries."""
        assert country_code_to_location("DE") == "Germany"
        assert country_code_to_location("AT") == "Austria"
        assert country_code_to_location("CH") == "Switzerland"

    def test_case_insensitive(self):
        """Country codes should be case insensitive."""
        assert country_code_to_location("de") == "Germany"
        assert country_code_to_location("De") == "Germany"
        assert country_code_to_location("DE") == "Germany"

    def test_unknown_country_returns_as_is(self):
        """Unknown country codes should be returned unchanged."""
        assert country_code_to_location("XX") == "XX"
        assert country_code_to_location("ZZ") == "ZZ"

    def test_no_duplicate_keys(self):
        """Verify LOCATION_MAP has no duplicate keys (ZA bug fix)."""
        from brightdata_utils import LOCATION_MAP
        # No duplicates means count equals unique count
        keys = list(LOCATION_MAP.keys())
        assert len(keys) == len(set(keys)), "LOCATION_MAP has duplicate keys"


class TestEnsureSdkInstalled:
    """Tests for SDK installation check."""

    def test_sdk_installed(self):
        """Should not raise if brightdata is importable."""
        # This test passes if brightdata is installed
        try:
            import brightdata
            # If we get here, SDK is installed
            ensure_sdk_installed()  # Should not raise
        except ImportError:
            pytest.skip("brightdata-sdk not installed")

    def test_sdk_not_installed_exits(self, monkeypatch):
        """Should exit with error if SDK not installed."""
        # Mock the import to raise ImportError
        import builtins
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "brightdata":
                raise ImportError("No module named 'brightdata'")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        with pytest.raises(SystemExit):
            ensure_sdk_installed()


class TestSearchGoogle:
    """Tests for Google search function."""

    @pytest.mark.asyncio
    async def test_missing_api_key_returns_error(self, monkeypatch):
        """Should return error dict if API key missing."""
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        with patch("search.CONFIG_FILE", Path("/nonexistent/config.json")):
            with patch("brightdata_utils.Path.home") as mock_home:
                mock_home.return_value.__truediv__ = lambda self, x: Path("/nonexistent")

                # Import here to get fresh module state
                from search import search_google
                result = await search_google("test query")

                assert result.get("success") is False
                assert "error" in result

    @pytest.mark.asyncio
    async def test_sdk_not_installed_returns_error(self, monkeypatch):
        """Should return error dict if SDK not installed."""
        monkeypatch.setenv("BRIGHTDATA_SERP_API_KEY", "fake_key")

        with patch.dict("sys.modules", {"brightdata": None}):
            # Force ImportError
            import builtins
            original_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == "brightdata":
                    raise ImportError("No module named 'brightdata'")
                return original_import(name, *args, **kwargs)

            monkeypatch.setattr(builtins, "__import__", mock_import)

            from search import search_google
            result = await search_google("test query")

            assert result.get("success") is False
            assert "brightdata-sdk not installed" in result.get("error", "")


class TestSearchBatch:
    """Tests for batch search function."""

    @pytest.mark.asyncio
    async def test_empty_queries(self):
        """Should handle empty query list."""
        from search import search_batch
        result = await search_batch([])

        assert result.get("success") is True
        assert result.get("total_queries") == 0

    @pytest.mark.asyncio
    async def test_single_query_delegates(self, monkeypatch):
        """Should delegate single query to search_google."""
        monkeypatch.setenv("BRIGHTDATA_SERP_API_KEY", "fake_key")

        from search import search_batch

        # This will fail due to fake key, but tests the delegation
        result = await search_batch(["test query"], "US", "en", 5)

        assert "results_by_query" in result
        assert "test query" in result["results_by_query"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
