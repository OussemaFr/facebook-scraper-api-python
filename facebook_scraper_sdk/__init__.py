# Path: facebook-scraper-python/facebook_scraper_sdk/__init__.py

"""
Facebook Scraper API SDK

Official Python SDK for Facebook Scraper API via RapidAPI.
"""

from .__version__ import __author__, __author_email__, __license__, __version__
from .client import FacebookScraperClient
from .exceptions import (
    AuthenticationError,
    ContentError,
    CookiesError,
    FacebookScraperError,
    NotFoundError,
    PrivateContentError,
    RateLimitError,
    UnparsableContentError,
    ValidationError,
)
from .retry import RateLimiter, retry_with_backoff

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    # Client
    "FacebookScraperClient",
    # Exceptions
    "FacebookScraperError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "PrivateContentError",
    "CookiesError",
    "ContentError",
    "UnparsableContentError",
    # Utilities
    "retry_with_backoff",
    "RateLimiter",
]
