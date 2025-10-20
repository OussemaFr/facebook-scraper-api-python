# Path: facebook-scraper-python/tests/test_integration.py

"""
Integration tests against real API.

These tests require a valid API key set in RAPIDAPI_KEY environment variable.
Run with: pytest tests/test_integration.py -v -m integration

Skip with: pytest tests/ -v -m "not integration"
"""

import os

import pytest

from facebook_scraper_sdk import AuthenticationError, FacebookScraperClient, ValidationError


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("RAPIDAPI_KEY"), reason="No API key set")
class TestRealAPIIntegration:
    """Integration tests against real API."""

    @pytest.fixture
    def client(self):
        """Create client with real API key."""
        api_key = os.getenv("RAPIDAPI_KEY")
        return FacebookScraperClient(api_key=api_key)

    def test_get_page_id_facebook_official(self, client):
        """Test getting Facebook's official page ID."""
        result = client.get_page_id("https://www.facebook.com/facebook")

        assert "page_id" in result or "id" in result
        assert result is not None

    def test_get_page_details_facebook_official(self, client):
        """Test getting Facebook's official page details."""
        result = client.get_page_details(
            link="https://www.facebook.com/facebook", exact_followers_count=True
        )

        assert result is not None
        # Facebook page should have a name
        assert "name" in result or "title" in result

    def test_invalid_url_raises_validation_error(self, client):
        """Test that invalid URL raises ValidationError."""
        with pytest.raises(ValidationError):
            client.get_page_id("not-a-valid-url")

    def test_context_manager_works(self):
        """Test client works with context manager."""
        api_key = os.getenv("RAPIDAPI_KEY")

        with FacebookScraperClient(api_key=api_key) as client:
            result = client.get_page_id("https://www.facebook.com/facebook")
            assert result is not None


@pytest.mark.integration
class TestInvalidAuthentication:
    """Test authentication failures."""

    def test_invalid_api_key_raises_auth_error(self):
        """Test that invalid API key raises AuthenticationError."""
        client = FacebookScraperClient(api_key="invalid-key-12345")

        with pytest.raises(AuthenticationError):
            client.get_page_id("https://www.facebook.com/facebook")
