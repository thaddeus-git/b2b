#!/usr/bin/env python3
"""Unit tests for brightdata_utils.py."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from brightdata_utils import get_api_key, country_to_location, LOCATION_MAP


class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_env_variable_takes_priority(self, tmp_path, monkeypatch):
        """Environment variable should take priority over config files."""
        # Set env variable
        monkeypatch.setenv("BRIGHTDATA_SERP_API_KEY", "env_test_key")

        # Create a config file (should be ignored)
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"brightdata_api_key": "file_test_key"}))

        with patch.object(Path, "home", return_value=tmp_path):
            result = get_api_key()

        assert result == "env_test_key"

    def test_shared_config_used_when_no_env(self, tmp_path, monkeypatch):
        """Shared config should be used when no env variable."""
        # Ensure no env variable
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        # Create shared config
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        config_file = claude_dir / "config.json"
        config_file.write_text(json.dumps({"brightdata_api_key": "shared_key"}))

        with patch.object(Path, "home", return_value=tmp_path):
            result = get_api_key()

        assert result == "shared_key"

    def test_skill_config_fallback(self, tmp_path, monkeypatch):
        """Skill-specific config should be fallback when no shared config."""
        # Ensure no env variable
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        # Create skill-specific config
        claude_dir = tmp_path / ".claude"
        skill_dir = claude_dir / "test-skill"
        skill_dir.mkdir(parents=True)
        config_file = skill_dir / "config.json"
        config_file.write_text(json.dumps({"api_key": "skill_key"}))

        with patch.object(Path, "home", return_value=tmp_path):
            result = get_api_key("test-skill")

        assert result == "skill_key"

    def test_returns_empty_when_no_config(self, tmp_path, monkeypatch):
        """Should return empty string when no config found."""
        # Ensure no env variable
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        # No config files exist
        with patch.object(Path, "home", return_value=tmp_path):
            result = get_api_key()

        assert result == ""

    def test_handles_malformed_json(self, tmp_path, monkeypatch):
        """Should handle malformed JSON gracefully."""
        monkeypatch.delenv("BRIGHTDATA_SERP_API_KEY", raising=False)

        # Create malformed config
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        config_file = claude_dir / "config.json"
        config_file.write_text("{ invalid json }")

        with patch.object(Path, "home", return_value=tmp_path):
            result = get_api_key()

        assert result == ""


class TestCountryToLocation:
    """Tests for country_to_location function."""

    def test_known_country_codes(self):
        """Test known country codes return correct locations."""
        assert country_to_location("DE") == "Germany"
        assert country_to_location("US") == "United States"
        assert country_to_location("FR") == "France"
        assert country_to_location("GB") == "United Kingdom"  # If in map
        assert country_to_location("AE") == "United Arab Emirates"

    def test_case_insensitive(self):
        """Country codes should be case insensitive."""
        assert country_to_location("de") == "Germany"
        assert country_to_location("De") == "Germany"
        assert country_to_location("dE") == "Germany"
        assert country_to_location("DE") == "Germany"

    def test_unknown_code_returns_input(self):
        """Unknown country codes should return the input."""
        assert country_to_location("XX") == "XX"
        assert country_to_location("ZZ") == "ZZ"

    def test_all_location_map_entries_valid(self):
        """All entries in LOCATION_MAP should have valid values."""
        for code, location in LOCATION_MAP.items():
            assert len(code) == 2, f"Country code {code} should be 2 characters"
            assert isinstance(location, str), f"Location for {code} should be string"
            assert len(location) > 0, f"Location for {code} should not be empty"


class TestLocationMapCompleteness:
    """Tests for LOCATION_MAP completeness."""

    def test_tier1_countries_present(self):
        """Tier 1 countries should be in the map."""
        tier1 = ["DE", "FR", "IT", "UK", "HU"]
        for country in tier1:
            # UK uses GB as code
            code = "GB" if country == "UK" else country
            assert code in LOCATION_MAP, f"Tier 1 country {country} missing from LOCATION_MAP"

    def test_tier2_countries_present(self):
        """Tier 2 countries should be in the map."""
        tier2 = ["AT", "NL", "BE", "ES", "SE", "PL", "IE", "SG", "TH", "MY", "AU", "NZ", "AE", "US", "CA"]
        for country in tier2:
            assert country in LOCATION_MAP, f"Tier 2 country {country} missing from LOCATION_MAP"