# Path: facebook-scraper-python/examples/basic_usage.py

"""
Basic usage examples for Facebook Scraper SDK.

Make sure to set your API key before running:
export RAPIDAPI_KEY="your-api-key-here"
"""

import os

from facebook_scraper_sdk import (
    AuthenticationError,
    FacebookScraperClient,
    FacebookScraperError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

# Get API key from environment variable
API_KEY = os.getenv("RAPIDAPI_KEY")

if not API_KEY:
    print("Error: Please set RAPIDAPI_KEY environment variable")
    print("Example: export RAPIDAPI_KEY='your-key-here'")
    exit(1)


def example_1_get_page_id():
    """Example 1: Get Facebook page ID from URL."""
    print("\n" + "=" * 50)
    print("Example 1: Get Page ID")
    print("=" * 50)

    client = FacebookScraperClient(api_key=API_KEY)

    page_url = "https://www.facebook.com/MazdaItalia"
    result = client.get_page_id(page_url)

    print(f"Page URL: {page_url}")
    print(f"Result: {result}")

    client.close()


def example_2_get_page_details():
    """Example 2: Get detailed page information."""
    print("\n" + "=" * 50)
    print("Example 2: Get Page Details")
    print("=" * 50)

    client = FacebookScraperClient(api_key=API_KEY)

    page_url = "https://www.facebook.com/EngenSA"
    result = client.get_page_details(
        link=page_url, exact_followers_count=True, show_verified_badge=True
    )

    print(f"Page URL: {page_url}")
    print(f"Page Name: {result.get('name', 'N/A')}")
    print(f"Followers: {result.get('followers', 'N/A')}")
    print(f"Likes: {result.get('likes', 'N/A')}")
    print(f"Full Result: {result}")

    client.close()


def example_3_context_manager():
    """Example 3: Using context manager (recommended)."""
    print("\n" + "=" * 50)
    print("Example 3: Context Manager Usage")
    print("=" * 50)

    with FacebookScraperClient(api_key=API_KEY) as client:
        page_url = "https://www.facebook.com/MazdaItalia"
        result = client.get_page_id(page_url)
        print(f"Result: {result}")

    print("Session automatically closed!")


def example_4_error_handling():
    """Example 4: Proper error handling."""
    print("\n" + "=" * 50)
    print("Example 4: Error Handling")
    print("=" * 50)

    try:
        with FacebookScraperClient(api_key=API_KEY) as client:
            # Try to get details without required parameters
            result = client.get_page_details()
    except ValidationError as e:
        print(f"✓ Caught ValidationError: {e}")
    except AuthenticationError as e:
        print(f"✗ Authentication Error: {e}")
    except RateLimitError as e:
        print(f"✗ Rate Limit Error: {e}")
    except NotFoundError as e:
        print(f"✗ Not Found Error: {e}")
    except FacebookScraperError as e:
        print(f"✗ API Error: {e}")


def example_5_multiple_requests():
    """Example 5: Making multiple requests efficiently."""
    print("\n" + "=" * 50)
    print("Example 5: Multiple Requests")
    print("=" * 50)

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/EngenSA",
    ]

    with FacebookScraperClient(api_key=API_KEY) as client:
        for page_url in pages:
            try:
                result = client.get_page_id(page_url)
                print(f"✓ {page_url}: {result.get('page_id', 'Unknown')}")
            except Exception as e:
                print(f"✗ {page_url}: Error - {e}")


def example_6_using_profile_id():
    """Example 6: Using profile ID instead of URL."""
    print("\n" + "=" * 50)
    print("Example 6: Using Profile ID")
    print("=" * 50)

    with FacebookScraperClient(api_key=API_KEY) as client:
        # First get the profile ID from a URL
        page_url = "https://www.facebook.com/MazdaItalia"
        id_result = client.get_page_id(page_url)
        profile_id = id_result.get("page_id")

        print(f"Got profile ID: {profile_id}")

        # Then use the profile ID to get details
        if profile_id:
            details = client.get_page_details(profile_id=profile_id)
            print(f"Page details: {details.get('name', 'Unknown')}")


def example_7_custom_timeout():
    """Example 7: Custom timeout configuration."""
    print("\n" + "=" * 50)
    print("Example 7: Custom Timeout")
    print("=" * 50)

    # Create client with 60 second timeout
    with FacebookScraperClient(api_key=API_KEY, timeout=60) as client:
        print(f"Client timeout set to: {client.timeout} seconds")

        result = client.get_page_id("https://www.facebook.com/MazdaItalia")
        print(f"Result: {result}")


if __name__ == "__main__":
    print("\n" + "#" * 50)
    print("# Facebook Scraper SDK - Basic Usage Examples")
    print("#" * 50)

    try:
        example_1_get_page_id()
        example_2_get_page_details()
        example_3_context_manager()
        example_4_error_handling()
        example_5_multiple_requests()
        example_6_using_profile_id()
        example_7_custom_timeout()

        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
