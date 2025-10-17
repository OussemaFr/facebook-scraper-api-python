# Facebook Scraper SDK - Python

[![PyPI version](https://badge.fury.io/py/facebook-scraper-sdk.svg)](https://badge.fury.io/py/facebook-scraper-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/facebook-scraper-sdk.svg)](https://pypi.org/project/facebook-scraper-sdk/)
[![CI](https://github.com/yourusername/facebook-scraper-python/workflows/CI/badge.svg)](https://github.com/yourusername/facebook-scraper-python/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for **Facebook Scraper API** via RapidAPI.

## ✨ Features

- 🚀 Simple & intuitive API
- 📘 Full type hints
- 🛡️ Comprehensive error handling with specific error codes
- 🔄 Context manager support
- ⚡ Efficient session reuse
- ✅ 95%+ test coverage

## 📦 Installation

```bash
pip install facebook-scraper-sdk
```

## 🔑 Getting Your API Key

1. Visit [Facebook Scraper API on RapidAPI](https://rapidapi.com/oussemaf/api/facebook-scraper-api4)
2. Click "Subscribe to Test"
3. Choose a pricing plan (free tier available)
4. Copy your API key from the dashboard

## 🚀 Quick Start

```python
from facebook_scraper_sdk import FacebookScraperClient

# Initialize client with your RapidAPI key
client = FacebookScraperClient(api_key="your-rapidapi-key")

# Get page ID
page_id = client.get_page_id("https://www.facebook.com/MazdaItalia")
print(page_id)

# Get page details
details = client.get_page_details(
    link="https://www.facebook.com/EngenSA",
    exact_followers_count=True
)
print(f"Page: {details['name']}, Followers: {details['followers']}")

client.close()
```

### Using Context Manager (Recommended)

```python
with FacebookScraperClient(api_key="your-rapidapi-key") as client:
    result = client.get_page_id("https://www.facebook.com/MazdaItalia")
    print(result)
# Session automatically closed
```

## 📖 API Reference

### Initialize Client

```python
FacebookScraperClient(api_key: str, timeout: int = 30)
```

**Parameters:**
- `api_key` (str, required): Your RapidAPI key from https://rapidapi.com/oussemaf/api/facebook-scraper-api4
- `timeout` (int, optional): Request timeout in seconds (default: 30)

**Raises:**
- `AuthenticationError`: If API key is empty or None

---

### Get Page ID

```python
client.get_page_id(link: str) -> Dict[str, Any]
```

Extract the Facebook page ID from a page URL.

**Parameters:**
- `link` (str, required): Facebook page URL

**Returns:**
- Dictionary containing page ID information

**Raises:**
- `ValidationError`: If link is empty or invalid format (HTTP 202)
- `PrivateContentError`: If page is private (HTTP 203)
- `AuthenticationError`: If API token is invalid (HTTP 403)

**Example:**
```python
result = client.get_page_id("https://www.facebook.com/MazdaItalia")
# {'page_id': '123456789', 'username': 'MazdaItalia'}
```

---

### Get Page Details

```python
client.get_page_details(
    link: Optional[str] = None,
    profile_id: Optional[str] = None,
    exact_followers_count: bool = True,
    show_verified_badge: bool = False
) -> Dict[str, Any]
```

Retrieve comprehensive information about a Facebook page.

**Parameters:**
- `link` (str, optional): Facebook page URL (takes priority over profile_id)
- `profile_id` (str, optional): Facebook profile ID
- `exact_followers_count` (bool, optional): Return exact follower count (default: True)
- `show_verified_badge` (bool, optional): Include verified badge info (default: False)

**Returns:**
- Dictionary containing comprehensive page details

**Raises:**
- `ValidationError`: If neither link nor profile_id is provided (HTTP 202)
- `PrivateContentError`: If page is private (HTTP 203)
- `CookiesError`: If cookies are expired or missing (HTTP 203)
- `ContentError`: If content fetch fails (HTTP 206)
- `UnparsableContentError`: If content is inappropriate (HTTP 208)
- `AuthenticationError`: If API token is invalid (HTTP 403)

**Note:** If both `link` and `profile_id` are provided, `link` takes priority.

**Example:**
```python
result = client.get_page_details(
    link="https://www.facebook.com/EngenSA",
    exact_followers_count=True,
    show_verified_badge=True
)
```

## 🛡️ Error Handling

The SDK provides specific exceptions for different error scenarios with detailed error codes:

```python
from facebook_scraper_sdk import (
    FacebookScraperClient,
    AuthenticationError,      # HTTP 403 - Invalid token
    ValidationError,          # HTTP 202 - Invalid parameters
    PrivateContentError,      # HTTP 203 - Private content
    CookiesError,            # HTTP 203 - Cookie issues
    ContentError,            # HTTP 206 - Fetch failures
    UnparsableContentError,  # HTTP 208 - Inappropriate content
    RateLimitError,          # HTTP 429 - Rate limit exceeded
    NotFoundError,           # HTTP 404 - Not found
    FacebookScraperError     # Base exception
)

try:
    with FacebookScraperClient(api_key="your-key") as client:
        result = client.get_page_details(link="https://www.facebook.com/SomePage")
except AuthenticationError as e:
    print(f"Invalid API key: {e.error_code}")
    print("Get your key from: https://rapidapi.com/oussemaf/api/facebook-scraper-api4")
except ValidationError as e:
    print(f"Invalid parameters: {e.message} (Code: {e.error_code})")
except PrivateContentError as e:
    print(f"Content is private: {e.error_code}")
except CookiesError as e:
    print(f"Cookie issue: {e.error_code}")
except ContentError as e:
    print(f"Fetch failed: {e.error_code}")
except UnparsableContentError as e:
    print(f"Content unparsable: {e.error_code}")
except RateLimitError:
    print("Rate limit exceeded - please wait before retrying")
except NotFoundError:
    print("Page not found")
except FacebookScraperError as e:
    print(f"API error: {e}")
```

### Common Error Codes

**HTTP 202 - Validation Errors:**
- `INVALID_PAGE_URL` - Invalid Facebook page URL
- `INVALID_GROUP_URL` - Invalid Facebook group URL
- `INVALID_POST_URL` - Invalid Facebook post URL
- `INVALID_DATE_FORMAT` - Invalid date format (use YYYY-MM-DD)
- `MISSING_REQUIRED_FIELDS` - Required parameters missing
- `FUTURE_DATE_NOT_ALLOWED` - Cannot fetch future dates
- And more...

**HTTP 203 - Private Content / Cookies:**
- `PRIVATE_PAGE` - Page is private
- `PRIVATE_GROUP` - Group is private
- `PRIVATE_CONTENT` - Content is private
- `PROFILE_NOT_FOUND` - Profile not found
- `COOKIES_EXPIRED` - User cookies expired
- `MISSING_COOKIES` - Required cookies missing

**HTTP 206 - Content Errors:**
- `FAILED_TO_FETCH_LISTING_DETAILS` - Could not retrieve listing
- `RETRY_ERROR` - Temporary error, retry recommended

**HTTP 208 - Content Issues:**
- `UNPARSABLE_CONTENT` - Content contains inappropriate keywords

**HTTP 403:**
- Invalid API token

## 🎯 Usage Examples

### Basic Usage

```python
from facebook_scraper_sdk import FacebookScraperClient

with FacebookScraperClient(api_key="your-key") as client:
    # Get page ID
    page = client.get_page_id("https://www.facebook.com/MazdaItalia")
    print(f"Page ID: {page['page_id']}")
    
    # Get page details
    details = client.get_page_details(link="https://www.facebook.com/EngenSA")
    print(f"{details['name']} has {details['followers']} followers")
```

### Batch Processing

```python
pages = [
    "https://www.facebook.com/MazdaItalia",
    "https://www.facebook.com/EngenSA",
]

with FacebookScraperClient(api_key="your-key") as client:
    for page_url in pages:
        try:
            details = client.get_page_details(link=page_url)
            print(f"✓ {details['name']}: {details['followers']} followers")
        except FacebookScraperError as e:
            print(f"✗ {page_url}: {e.message} ({e.error_code})")
```

### Using Profile ID

```python
with FacebookScraperClient(api_key="your-key") as client:
    # First get the profile ID
    result = client.get_page_id("https://www.facebook.com/MazdaItalia")
    profile_id = result['page_id']
    
    # Then use profile_id for subsequent requests
    details = client.get_page_details(profile_id=profile_id)
    print(details)
```

## 📚 Advanced Examples

For more advanced examples including retry logic, batch processing, and data extraction, see the [examples](examples/) directory:

- [`basic_usage.py`](examples/basic_usage.py) - Basic usage patterns
- [`advanced_usage.py`](examples/advanced_usage.py) - Advanced patterns and best practices

## 📋 Requirements

- Python 3.7+
- requests >= 2.25.0

## 🧪 Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/facebook-scraper-python.git
cd facebook-scraper-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Code quality
black facebook_scraper_sdk/
flake8 facebook_scraper_sdk/
mypy facebook_scraper_sdk/
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI**: https://pypi.org/project/facebook-scraper-sdk/
- **GitHub**: https://github.com/yourusername/facebook-scraper-python
- **Issues**: https://github.com/yourusername/facebook-scraper-python/issues
- **RapidAPI**: https://rapidapi.com/oussemaf/api/facebook-scraper-api4
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## 💬 Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/facebook-scraper-python/issues)
- 🔑 Get API Key: https://rapidapi.com/oussemaf/api/facebook-scraper-api4

## 🌟 Related SDKs

- [JavaScript/TypeScript SDK](https://github.com/yourusername/facebook-scraper-js)

---

**Get your API key**: https://rapidapi.com/oussemaf/api/facebook-scraper-api4