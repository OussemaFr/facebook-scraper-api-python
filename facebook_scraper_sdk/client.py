# Path: facebook-scraper-python/facebook_scraper_sdk/client.py

"""Main client for Facebook Scraper API."""

import requests
from typing import Optional, Dict, Any

from .exceptions import (
    FacebookScraperError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    PrivateContentError,
    CookiesError,
    ContentError,
    UnparsableContentError,
)


class FacebookScraperClient:
    """
    Client for interacting with Facebook Scraper API.
    
    Example:
        >>> from facebook_scraper_sdk import FacebookScraperClient
        >>> client = FacebookScraperClient(api_key="your-rapidapi-key")
        >>> page_id = client.get_page_id("https://www.facebook.com/MazdaItalia")
    """

    BASE_URL = "https://facebook-scraper-api4.p.rapidapi.com"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize the Facebook Scraper client.

        Args:
            api_key: Your RapidAPI key
            timeout: Request timeout in seconds (default: 30)

        Raises:
            AuthenticationError: If API key is empty or None
        """
        if not api_key:
            raise AuthenticationError("API key is required")

        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "x-rapidapi-host": "facebook-scraper-api4.p.rapidapi.com",
            "x-rapidapi-key": self.api_key,
        })

    def _parse_error_response(self, response_text: str, status_code: int) -> tuple:
        """
        Parse error response to extract error code and message.
        
        Returns:
            Tuple of (error_code, error_message)
        """
        try:
            import json
            error_data = json.loads(response_text)
            error_code = error_data.get('error_code', '')
            error_message = error_data.get('message', response_text)
            return error_code, error_message
        except:
            return '', response_text

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            # Success
            if response.status_code == 200:
                return response.json()
            
            # Parse error response
            error_code, error_message = self._parse_error_response(response.text, response.status_code)
            
            # HTTP 202 - Validation Errors
            if response.status_code == 202:
                validation_errors = [
                    'INVALID_ENDPOINT_FOR_GROUP', 'INVALID_MARKETPLACE_LINK',
                    'INVALID_MARKETPLACE_LINK_FORMAT', 'INVALID_END_CURSOR',
                    'INVALID_ACTIVE_STATUS', 'INVALID_TIMEZONE',
                    'MISSING_REQUIRED_FIELDS', 'INVALID_PAGE_URL',
                    'INVALID_GROUP_URL', 'INVALID_POST_URL',
                    'INVALID_REELS_URL', 'INVALID_VIDEO_URL',
                    'INVALID_SORT_BY', 'INVALID_FACEBOOK_ID',
                    'INVALID_KEYWORD_ID', 'INVALID_DATE_FORMAT',
                    'FUTURE_DATE_NOT_ALLOWED', 'INVALID_INPUT_TYPE',
                    'INVALID_JSON_COOKIES', 'INVALID_SEARCH_CONDITION',
                    'INVALID_AD_ARCHIVE_ID'
                ]
                raise ValidationError(
                    error_message or "Invalid request parameters",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 203 - Private Content / Cookies Errors
            elif response.status_code == 203:
                cookie_errors = ['COOKIES_EXPIRED', 'MISSING_COOKIES', 'EXPIRED_COOKIES']
                private_errors = ['PRIVATE_PAGE', 'PRIVATE_GROUP', 'PRIVATE_CONTENT', 'PROFILE_NOT_FOUND', 'GROUP_ID_NOT_FOUND']
                
                if error_code in cookie_errors:
                    raise CookiesError(
                        error_message or "Cookie authentication failed",
                        status_code=response.status_code,
                        error_code=error_code,
                        response=response.text,
                    )
                elif error_code in private_errors:
                    raise PrivateContentError(
                        error_message or "Content is private or not accessible",
                        status_code=response.status_code,
                        error_code=error_code,
                        response=response.text,
                    )
                else:
                    raise FacebookScraperError(
                        error_message,
                        status_code=response.status_code,
                        error_code=error_code,
                        response=response.text,
                    )
            
            # HTTP 206 - Content Fetch Errors
            elif response.status_code == 206:
                raise ContentError(
                    error_message or "Failed to fetch content",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 208 - Unparsable Content
            elif response.status_code == 208:
                raise UnparsableContentError(
                    error_message or "Content contains inappropriate or unparsable data",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 403 - Authentication Error (Invalid Token)
            elif response.status_code == 403:
                raise AuthenticationError(
                    "Invalid API token",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 401 - Unauthorized
            elif response.status_code == 401:
                raise AuthenticationError(
                    "Unauthorized - Invalid API key",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 429 - Rate Limit
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # HTTP 404 - Not Found
            elif response.status_code == 404:
                raise NotFoundError(
                    "Resource not found",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
            
            # Generic error
            else:
                raise FacebookScraperError(
                    f"API request failed: {error_message}",
                    status_code=response.status_code,
                    error_code=error_code,
                    response=response.text,
                )
                
        except requests.exceptions.Timeout:
            raise FacebookScraperError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise FacebookScraperError(f"Request failed: {str(e)}")

    def get_page_id(self, link: str) -> Dict[str, Any]:
        """
        Get Facebook page ID from a page link.

        Args:
            link: Facebook page URL

        Returns:
            Dictionary containing page ID information

        Raises:
            ValidationError: If link is empty, None, or invalid format
            PrivateContentError: If the page is private
            AuthenticationError: If API key is invalid (403)

        Example:
            >>> client = FacebookScraperClient("your-api-key")
            >>> result = client.get_page_id("https://www.facebook.com/MazdaItalia")
            >>> print(result)
        """
        if not link:
            raise ValidationError("Link parameter is required")

        params = {"link": link}
        return self._make_request("/get_facebook_page_id", params)

    def get_page_details(
        self,
        link: Optional[str] = None,
        profile_id: Optional[str] = None,
        exact_followers_count: bool = True,
        show_verified_badge: bool = False,
    ) -> Dict[str, Any]:
        """
        Get detailed information about a Facebook page.

        Args:
            link: Facebook page URL (priority if both link and profile_id provided)
            profile_id: Facebook profile ID
            exact_followers_count: Return exact follower count (default: True)
            show_verified_badge: Include verified badge information (default: False)

        Returns:
            Dictionary containing page details

        Raises:
            ValidationError: If neither link nor profile_id is provided, or invalid format
            PrivateContentError: If the page is private
            AuthenticationError: If API key is invalid (403)
            ContentError: If content fetch fails (206)

        Example:
            >>> client = FacebookScraperClient("your-api-key")
            >>> result = client.get_page_details(
            ...     link="https://www.facebook.com/EngenSA",
            ...     exact_followers_count=True
            ... )
        
        Note:
            If both link and profile_id are provided, link takes priority.
        """
        if not link and not profile_id:
            raise ValidationError("Either 'link' or 'profile_id' must be provided")

        params = {
            "exact_followers_count": str(exact_followers_count).lower(),
            "show_verified_badge": str(show_verified_badge).lower(),
        }

        if link:
            params["link"] = link
        elif profile_id:
            params["profile_id"] = profile_id

        return self._make_request("/get_facebook_pages_details_from_link", params)

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self):
        """String representation of the client."""
        return f"FacebookScraperClient(api_key='***', timeout={self.timeout})"