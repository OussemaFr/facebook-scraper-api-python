# Path: facebook-scraper-python/facebook_scraper_sdk/retry.py

"""Retry logic and rate limiting utilities."""

import functools
import time
from typing import Any, Callable, Tuple, Type

from .exceptions import FacebookScraperError, RateLimitError


def retry_with_backoff(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    retry_on: Tuple[Type[Exception], ...] = (RateLimitError,),
):
    """
    Decorator to retry failed requests with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_factor: Base delay for exponential backoff in seconds (default: 2.0)
        retry_on: Tuple of exceptions to retry on (default: (RateLimitError,))

    Example:
        >>> from facebook_scraper_sdk import FacebookScraperClient, retry_with_backoff
        >>>
        >>> @retry_with_backoff(max_retries=3, backoff_factor=2)
        ... def fetch_page_data(url):
        ...     client = FacebookScraperClient(api_key="your-key")
        ...     return client.get_page_id(url)
        >>>
        >>> # Will retry up to 3 times with exponential backoff on rate limit
        >>> result = fetch_page_data("https://www.facebook.com/page")
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    if attempt == max_retries - 1:
                        # Last attempt, raise the exception
                        raise

                    # Calculate wait time: backoff_factor * (2 ** attempt)
                    # attempt 0: backoff_factor * 1 = backoff_factor
                    # attempt 1: backoff_factor * 2 = backoff_factor * 2
                    # attempt 2: backoff_factor * 4 = backoff_factor * 4
                    wait_time = backoff_factor * (2**attempt)

                    # Log retry attempt if the exception has error details
                    if isinstance(e, FacebookScraperError):
                        error_code = getattr(e, "error_code", None) or "Unknown"
                        print(
                            f"Retry attempt {attempt + 1}/{max_retries} after "
                            f"{wait_time:.1f}s (Error: {error_code})"
                        )

                    time.sleep(wait_time)

            # Final attempt (should not reach here due to raise in loop)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class RateLimiter:
    """
    Simple rate limiter to control request frequency.

    Example:
        >>> from facebook_scraper_sdk import FacebookScraperClient, RateLimiter
        >>>
        >>> limiter = RateLimiter(max_requests=10, time_window=60)  # 10 req/min
        >>> client = FacebookScraperClient(api_key="your-key")
        >>>
        >>> for url in urls:
        ...     limiter.wait_if_needed()
        ...     result = client.get_page_id(url)
    """

    def __init__(self, max_requests: int = 60, time_window: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()

        # Remove old requests outside the time window
        self.requests = [
            req_time for req_time in self.requests if now - req_time < self.time_window
        ]

        # Check if we need to wait
        if len(self.requests) >= self.max_requests:
            oldest_request = min(self.requests)
            wait_time = self.time_window - (now - oldest_request)
            if wait_time > 0:
                time.sleep(wait_time)
                # Clean up again after waiting
                now = time.time()
                self.requests = [
                    req_time for req_time in self.requests if now - req_time < self.time_window
                ]

        # Record this request
        self.requests.append(now)
