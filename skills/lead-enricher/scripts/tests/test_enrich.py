#!/usr/bin/env python3
"""Unit tests for lead enrichment functions."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from enrich import (
    extract_domain,
    extract_email_domain,
    is_generic_email_domain,
    normalize_phone,
    fuzzy_similarity,
    validate_linkedin_result,
    person_equals_company,
    score_website_match,
)


class TestExtractDomain:
    def test_full_url(self):
        assert extract_domain("https://www.example.com/path") == "example.com"

    def test_without_protocol(self):
        assert extract_domain("example.com") == "example.com"

    def test_with_www(self):
        assert extract_domain("https://www.example.com") == "example.com"


class TestExtractEmailDomain:
    def test_normal_email(self):
        assert extract_email_domain("user@example.com") == "example.com"

    def test_invalid_email(self):
        assert extract_email_domain("invalid-email") is None

    def test_empty_string(self):
        assert extract_email_domain("") is None


class TestIsGenericEmailDomain:
    def test_gmail(self):
        assert is_generic_email_domain("gmail.com") is True

    def test_company_domain(self):
        assert is_generic_email_domain("reha360.de") is False

    def test_german_isp(self):
        assert is_generic_email_domain("web.de") is True


class TestNormalizePhone:
    def test_with_country_code(self):
        assert normalize_phone("+49-123-456-7890") == "491234567890"

    def test_with_spaces(self):
        assert normalize_phone("0664 1302708") == "06641302708"

    def test_empty(self):
        assert normalize_phone("") == ""


class TestFuzzySimilarity:
    def test_exact_match(self):
        assert fuzzy_similarity("Reha360", "Reha360") >= 0.99

    def test_similar_names(self):
        assert fuzzy_similarity("Reha360 GmbH", "Reha360") >= 0.7

    def test_different_names(self):
        assert fuzzy_similarity("Reha360", "Sankom Patent Socks") < 0.3


class TestValidateLinkedInResult:
    def test_matching_title(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/reha360",
            "Reha360 GmbH | LinkedIn"
        ) is True

    def test_matching_slug(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/reha360",
            ""
        ) is True

    def test_wrong_result(self):
        assert validate_linkedin_result(
            "Reha360",
            "https://linkedin.com/company/sankompatentsocks",
            "Sankom Patent Socks | LinkedIn"
        ) is False

    def test_partial_match(self):
        assert validate_linkedin_result(
            "SAUBERHAFT",
            "https://linkedin.com/company/sauberhaft-ch",
            "Sauberhaft | LinkedIn"
        ) is True


class TestPersonEqualsCompany:
    def test_exact_match(self):
        assert person_equals_company("Mina", "Mina") is True

    def test_name_in_company(self):
        assert person_equals_company("Mina", "Mina GmbH") is True

    def test_different(self):
        assert person_equals_company("Sven Haubert", "Reha360") is False

    def test_empty(self):
        assert person_equals_company("", "Company") is False


class TestScoreWebsiteMatch:
    def test_email_domain_match(self):
        lead = {"company_name": "Reha360", "work_email": "office@reha360.de", "work_phone_number": ""}
        result = {"url": "https://reha360.de", "title": "Reha360", "snippet": ""}
        score = score_website_match(lead, result)
        assert score >= 0.5  # Email domain match

    def test_generic_email_no_bonus(self):
        lead = {"company_name": "Test", "work_email": "user@gmail.com", "work_phone_number": ""}
        result = {"url": "https://test.com", "title": "Test", "snippet": ""}
        score = score_website_match(lead, result)
        assert score < 0.5  # No email domain bonus for generic

    def test_phone_in_snippet(self):
        lead = {"company_name": "Test", "work_email": "", "work_phone_number": "+49-123-456"}
        result = {"url": "https://test.com", "title": "Test", "snippet": "Call us at 49123456"}
        score = score_website_match(lead, result)
        assert score >= 0.15  # Phone bonus
