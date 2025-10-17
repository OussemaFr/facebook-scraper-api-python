# Path: facebook-scraper-python/facebook_scraper_sdk/exceptions.py

"""Custom exceptions for Facebook Scraper SDK."""


class FacebookScraperError(Exception):
    """
    Base exception for Facebook Scraper SDK.

    All other SDK exceptions inherit from this class.

    Attributes:
        message (str): Error message
        status_code (int, optional): HTTP status code
        error_code (str, optional): API error code
        response (str, optional): Raw response from the API

    Example:
        >>> try:
        ...     client.get_page_id("invalid")
        ... except FacebookScraperError as e:
        ...     print(f"Error: {e.message}")
        ...     print(f"Code: {e.error_code}")
        ...     print(f"Status: {e.status_code}")
    """

    def __init__(self, message, status_code=None, error_code=None, response=None):
        """
        Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code (optional)
            error_code: API-specific error code (optional)
            response: Raw API response (optional)
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.response = response

    def __str__(self):
        """String representation of the error."""
        if self.status_code and self.error_code:
            return f"{self.message} (Status: {self.status_code}, Code: {self.error_code})"
        elif self.status_code:
            return f"{self.message} (Status Code: {self.status_code})"
        return self.message


class AuthenticationError(FacebookScraperError):
    """
    Raised when API key is invalid or missing.

    HTTP Status: 403, 401

    Common causes:
    - Invalid RapidAPI key
    - Missing API key
    - Expired API subscription

    Solution:
        Get your API key from: https://rapidapi.com/oussemaf/api/facebook-scraper-api4

    Example:
        >>> try:
        ...     client = FacebookScraperClient(api_key="invalid-key")
        ...     client.get_page_id("https://facebook.com/page")
        ... except AuthenticationError:
        ...     print("Get your API key from RapidAPI")
    """

    pass


class ValidationError(FacebookScraperError):
    """
    Raised when request parameters are invalid.

    HTTP Status: 202

    Common Error Codes:
    - INVALID_PAGE_URL: Invalid Facebook page URL
    - INVALID_GROUP_URL: Invalid Facebook group URL
    - INVALID_POST_URL: Invalid Facebook post URL
    - INVALID_DATE_FORMAT: Invalid date format (use YYYY-MM-DD)
    - MISSING_REQUIRED_FIELDS: Required parameters missing
    - FUTURE_DATE_NOT_ALLOWED: Cannot fetch future dates
    - INVALID_FACEBOOK_ID: ID must contain only digits
    - INVALID_SORT_BY: Invalid sort_by value
    - INVALID_INPUT_TYPE: Invalid input type

    Example:
        >>> try:
        ...     client.get_page_details()  # Missing both link and profile_id
        ... except ValidationError as e:
        ...     print(f"Validation error: {e.error_code}")
    """

    pass


class PrivateContentError(FacebookScraperError):
    """
    Raised when content is private or requires authentication.

    HTTP Status: 203

    Common Error Codes:
    - PRIVATE_PAGE: The Facebook page is private
    - PRIVATE_GROUP: The Facebook group is private
    - PRIVATE_CONTENT: Content is private (dynamic source_type)
    - PROFILE_NOT_FOUND: Facebook profile could not be retrieved
    - GROUP_ID_NOT_FOUND: Group ID could not be extracted

    Example:
        >>> try:
        ...     client.get_page_details(link="https://facebook.com/private-page")
        ... except PrivateContentError as e:
        ...     print(f"Content is private: {e.error_code}")
    """

    pass


class CookiesError(FacebookScraperError):
    """
    Raised when there are cookie-related issues.

    HTTP Status: 203

    Common Error Codes:
    - COOKIES_EXPIRED: User cookies are expired
    - MISSING_COOKIES: Required cookies are missing
    - EXPIRED_COOKIES: General cookie expiration error

    Note:
        Some endpoints require valid Facebook cookies for access.

    Example:
        >>> try:
        ...     client.get_private_content()
        ... except CookiesError as e:
        ...     print(f"Cookie issue: {e.error_code}")
    """

    pass


class ContentError(FacebookScraperError):
    """
    Raised when content cannot be fetched or parsed.

    HTTP Status: 206

    Common Error Codes:
    - FAILED_TO_FETCH_LISTING_DETAILS: Could not retrieve marketplace listing
    - RETRY_ERROR: Something went wrong, retry recommended

    Solution:
        Retry the request after a short delay.

    Example:
        >>> try:
        ...     client.get_listing_details(listing_id)
        ... except ContentError as e:
        ...     print(f"Fetch failed: {e.error_code}, retrying...")
        ...     time.sleep(2)
        ...     client.get_listing_details(listing_id)
    """

    pass


class UnparsableContentError(FacebookScraperError):
    """
    Raised when content contains inappropriate or unparsable data.

    HTTP Status: 208

    Error Code:
    - UNPARSABLE_CONTENT: Data contains inappropriate content or keywords

    Cause:
        The content at the provided link contains inappropriate keywords
        or cannot be parsed by the API.

    Example:
        >>> try:
        ...     client.get_page_details(link="https://facebook.com/flagged-content")
        ... except UnparsableContentError as e:
        ...     print(f"Content unparsable: {e.error_code}")
    """

    pass


class RateLimitError(FacebookScraperError):
    """
    Raised when rate limit is exceeded.

    HTTP Status: 429

    Solution:
        Wait before making additional requests. Consider implementing
        exponential backoff retry logic.

    Example:
        >>> import time
        >>> try:
        ...     client.get_page_id(url)
        ... except RateLimitError:
        ...     time.sleep(60)  # Wait 60 seconds
        ...     client.get_page_id(url)  # Retry
    """

    pass


class NotFoundError(FacebookScraperError):
    """
    Raised when resource is not found.

    HTTP Status: 404

    Common causes:
    - Invalid endpoint URL
    - Resource has been deleted
    - Incorrect resource ID

    Example:
        >>> try:
        ...     client.get_page_details(link="https://facebook.com/deleted-page")
        ... except NotFoundError:
        ...     print("Page not found or has been deleted")
    """

    pass
