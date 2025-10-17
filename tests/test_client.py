# Path: facebook-scraper-python/tests/test_client.py

"""Comprehensive tests for FacebookScraperClient."""

from unittest.mock import Mock, patch

import pytest

from facebook_scraper_sdk import (
    AuthenticationError,
    FacebookScraperClient,
    FacebookScraperError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class TestClientInitialization:
    """Test client initialization scenarios."""

    def test_init_without_api_key(self):
        """Test that client raises error without API key."""
        with pytest.raises(AuthenticationError, match="API key is required"):
            FacebookScraperClient(api_key="")

    def test_init_with_none_api_key(self):
        """Test that client raises error with None API key."""
        with pytest.raises(AuthenticationError):
            FacebookScraperClient(api_key=None)

    def test_init_with_valid_api_key(self):
        """Test successful initialization with valid API key."""
        client = FacebookScraperClient(api_key="test-key-123")
        assert client.api_key == "test-key-123"
        assert client.timeout == 30

    def test_init_with_custom_timeout(self):
        """Test initialization with custom timeout."""
        client = FacebookScraperClient(api_key="test-key", timeout=60)
        assert client.timeout == 60

    def test_session_headers_are_set(self):
        """Test that session headers are properly configured."""
        client = FacebookScraperClient(api_key="test-key")
        assert "x-rapidapi-key" in client.session.headers
        assert client.session.headers["x-rapidapi-key"] == "test-key"
        assert client.session.headers["x-rapidapi-host"] == "facebook-scraper-api4.p.rapidapi.com"

    def test_base_url_is_set(self):
        """Test that BASE_URL is correctly set."""
        assert FacebookScraperClient.BASE_URL == "https://facebook-scraper-api4.p.rapidapi.com"


class TestGetPageId:
    """Test get_page_id method."""

    @patch("requests.Session.get")
    def test_get_page_id_success(self, mock_get):
        """Test successful page ID retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"page_id": "12345", "username": "MazdaItalia"}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        result = client.get_page_id("https://www.facebook.com/MazdaItalia")

        assert result == {"page_id": "12345", "username": "MazdaItalia"}
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "link" in call_args[1]["params"]

    def test_get_page_id_without_link(self):
        """Test that empty link raises ValidationError."""
        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(ValidationError, match="Link parameter is required"):
            client.get_page_id("")

    def test_get_page_id_with_none_link(self):
        """Test that None link raises ValidationError."""
        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(ValidationError):
            client.get_page_id(None)

    @patch("requests.Session.get")
    def test_get_page_id_authentication_error(self, mock_get):
        """Test handling of 401 authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="invalid-key")
        with pytest.raises(AuthenticationError, match="Invalid API key"):
            client.get_page_id("https://www.facebook.com/TestPage")

    @patch("requests.Session.get")
    def test_get_page_id_rate_limit_error(self, mock_get):
        """Test handling of 429 rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            client.get_page_id("https://www.facebook.com/TestPage")

    @patch("requests.Session.get")
    def test_get_page_id_not_found_error(self, mock_get):
        """Test handling of 404 not found error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Page not found"
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(NotFoundError, match="Resource not found"):
            client.get_page_id("https://www.facebook.com/NonExistent")

    @patch("requests.Session.get")
    def test_get_page_id_validation_error(self, mock_get):
        """Test handling of 400 validation error."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(ValidationError, match="Invalid request parameters"):
            client.get_page_id("https://www.facebook.com/TestPage")


class TestGetPageDetails:
    """Test get_page_details method."""

    @patch("requests.Session.get")
    def test_get_page_details_with_link(self, mock_get):
        """Test successful page details retrieval with link."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Test Page",
            "followers": 10000,
            "likes": 9500,
        }
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        result = client.get_page_details(link="https://www.facebook.com/TestPage")

        assert result["name"] == "Test Page"
        assert result["followers"] == 10000

    @patch("requests.Session.get")
    def test_get_page_details_with_profile_id(self, mock_get):
        """Test successful page details retrieval with profile_id."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Test Page", "followers": 10000}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        result = client.get_page_details(profile_id="12345")

        assert result["name"] == "Test Page"
        call_args = mock_get.call_args
        assert "profile_id" in call_args[1]["params"]

    @patch("requests.Session.get")
    def test_get_page_details_link_takes_priority(self, mock_get):
        """Test that link takes priority over profile_id."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Test Page"}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        client.get_page_details(link="https://www.facebook.com/TestPage", profile_id="12345")

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert "link" in params
        assert "profile_id" not in params

    def test_get_page_details_without_params(self):
        """Test that missing both link and profile_id raises error."""
        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(ValidationError, match="Either 'link' or 'profile_id' must be provided"):
            client.get_page_details()

    @patch("requests.Session.get")
    def test_get_page_details_with_boolean_params(self, mock_get):
        """Test that boolean parameters are correctly formatted."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Test Page"}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        client.get_page_details(
            link="https://www.facebook.com/TestPage",
            exact_followers_count=False,
            show_verified_badge=True,
        )

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["exact_followers_count"] == "false"
        assert params["show_verified_badge"] == "true"

    @patch("requests.Session.get")
    def test_get_page_details_default_params(self, mock_get):
        """Test default boolean parameter values."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Test Page"}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        client.get_page_details(link="https://www.facebook.com/TestPage")

        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["exact_followers_count"] == "true"
        assert params["show_verified_badge"] == "false"


class TestContextManager:
    """Test context manager functionality."""

    def test_context_manager_usage(self):
        """Test that client works as context manager."""
        with FacebookScraperClient(api_key="test-key") as client:
            assert client.api_key == "test-key"
            assert client.session is not None

    @patch("requests.Session.close")
    def test_context_manager_closes_session(self, mock_close):
        """Test that session is closed when exiting context."""
        with FacebookScraperClient(api_key="test-key") as client:
            pass
        mock_close.assert_called_once()

    def test_manual_close(self):
        """Test manual session close."""
        client = FacebookScraperClient(api_key="test-key")
        with patch.object(client.session, "close") as mock_close:
            client.close()
            mock_close.assert_called_once()


class TestErrorHandling:
    """Test error handling scenarios."""

    @patch("requests.Session.get")
    def test_timeout_error(self, mock_get):
        """Test handling of request timeout."""
        import requests

        mock_get.side_effect = requests.exceptions.Timeout()

        client = FacebookScraperClient(api_key="test-key", timeout=5)
        with pytest.raises(FacebookScraperError, match="timed out after 5 seconds"):
            client.get_page_id("https://www.facebook.com/TestPage")

    @patch("requests.Session.get")
    def test_connection_error(self, mock_get):
        """Test handling of connection error."""
        import requests

        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(FacebookScraperError, match="Request failed"):
            client.get_page_id("https://www.facebook.com/TestPage")

    @patch("requests.Session.get")
    def test_generic_request_error(self, mock_get):
        """Test handling of generic request exception."""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Unknown error")

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(FacebookScraperError, match="Request failed"):
            client.get_page_id("https://www.facebook.com/TestPage")

    @patch("requests.Session.get")
    def test_500_server_error(self, mock_get):
        """Test handling of 500 internal server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")
        with pytest.raises(FacebookScraperError, match="API request failed"):
            client.get_page_id("https://www.facebook.com/TestPage")


class TestExceptionProperties:
    """Test exception class properties."""

    def test_exception_with_status_code(self):
        """Test exception includes status code."""
        error = FacebookScraperError("Test error", status_code=404, response="Not found")
        assert error.status_code == 404
        assert error.response == "Not found"
        assert "404" in str(error)

    def test_exception_without_status_code(self):
        """Test exception without status code."""
        error = FacebookScraperError("Test error")
        assert error.status_code is None
        assert "Test error" in str(error)


class TestRepr:
    """Test string representation."""

    def test_repr_masks_api_key(self):
        """Test that __repr__ masks the API key."""
        client = FacebookScraperClient(api_key="super-secret-key", timeout=45)
        repr_str = repr(client)

        assert "FacebookScraperClient" in repr_str
        assert "super-secret-key" not in repr_str
        assert "***" in repr_str
        assert "45" in repr_str


class TestIntegrationScenarios:
    """Test real-world usage scenarios."""

    @patch("requests.Session.get")
    def test_sequential_requests(self, mock_get):
        """Test making multiple requests in sequence."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"page_id": "12345"}
        mock_get.return_value = mock_response

        client = FacebookScraperClient(api_key="test-key")

        result1 = client.get_page_id("https://www.facebook.com/Page1")
        result2 = client.get_page_id("https://www.facebook.com/Page2")

        assert result1 == {"page_id": "12345"}
        assert result2 == {"page_id": "12345"}
        assert mock_get.call_count == 2

    @patch("requests.Session.get")
    def test_mixed_method_calls(self, mock_get):
        """Test calling different methods on same client."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        with FacebookScraperClient(api_key="test-key") as client:
            client.get_page_id("https://www.facebook.com/Page1")
            client.get_page_details(link="https://www.facebook.com/Page2")

        assert mock_get.call_count == 2
