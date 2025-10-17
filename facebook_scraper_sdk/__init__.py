# Path: facebook-scraper-python/facebook_scraper_sdk/__init__.py

"""
Facebook Scraper API SDK

Official Python SDK for Facebook Scraper API via RapidAPI.
"""

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

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

__all__ = [
    "FacebookScraperClient",
    "FacebookScraperError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "PrivateContentError",
    "CookiesError",
    "ContentError",
    "UnparsableContentError",
]
