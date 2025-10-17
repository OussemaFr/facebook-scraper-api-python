# Path: facebook-scraper-python/examples/advanced_usage.py

"""
Advanced usage examples for Facebook Scraper SDK.

This includes batch processing, retry logic, and more complex scenarios.
"""

import os
import time
from typing import Any, Dict, List

from facebook_scraper_sdk import FacebookScraperClient, FacebookScraperError, RateLimitError

API_KEY = os.getenv("RAPIDAPI_KEY")


def example_batch_processing():
    """Process multiple pages with progress tracking."""
    print("\n" + "=" * 50)
    print("Batch Processing Example")
    print("=" * 50)

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/EngenSA",
        "https://www.facebook.com/Microsoft",
        "https://www.facebook.com/Google",
    ]

    results = []

    with FacebookScraperClient(api_key=API_KEY) as client:
        for i, page_url in enumerate(pages, 1):
            try:
                print(f"Processing {i}/{len(pages)}: {page_url}")
                result = client.get_page_details(link=page_url)
                results.append({"url": page_url, "success": True, "data": result})
                print(f"  ✓ Success")
            except FacebookScraperError as e:
                print(f"  ✗ Error: {e}")
                results.append({"url": page_url, "success": False, "error": str(e)})

    # Summary
    successful = sum(1 for r in results if r["success"])
    print(
        f"\nProcessed {len(pages)} pages: {successful} successful, {len(pages) - successful} failed"
    )

    return results


def example_retry_logic():
    """Example with automatic retry on rate limit."""
    print("\n" + "=" * 50)
    print("Retry Logic Example")
    print("=" * 50)

    def fetch_with_retry(client, page_url, max_retries=3, backoff=2):
        """Fetch page details with exponential backoff retry."""
        for attempt in range(max_retries):
            try:
                result = client.get_page_details(link=page_url)
                print(f"✓ Success on attempt {attempt + 1}")
                return result
            except RateLimitError:
                if attempt < max_retries - 1:
                    wait_time = backoff**attempt
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached")
                    raise
            except FacebookScraperError as e:
                print(f"✗ Error: {e}")
                raise

    with FacebookScraperClient(api_key=API_KEY) as client:
        result = fetch_with_retry(client, "https://www.facebook.com/MazdaItalia")
        print(f"Result: {result}")


def example_data_extraction():
    """Extract specific data fields from multiple pages."""
    print("\n" + "=" * 50)
    print("Data Extraction Example")
    print("=" * 50)

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/EngenSA",
    ]

    extracted_data = []

    with FacebookScraperClient(api_key=API_KEY) as client:
        for page_url in pages:
            try:
                result = client.get_page_details(link=page_url, exact_followers_count=True)

                # Extract only the fields we care about
                extracted = {
                    "url": page_url,
                    "name": result.get("name", "Unknown"),
                    "followers": result.get("followers", 0),
                    "likes": result.get("likes", 0),
                    "verified": result.get("verified", False),
                }
                extracted_data.append(extracted)

                print(f"✓ {extracted['name']}: {extracted['followers']:,} followers")

            except FacebookScraperError as e:
                print(f"✗ {page_url}: {e}")

    return extracted_data


def example_comparison():
    """Compare multiple Facebook pages."""
    print("\n" + "=" * 50)
    print("Page Comparison Example")
    print("=" * 50)

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/EngenSA",
    ]

    with FacebookScraperClient(api_key=API_KEY) as client:
        page_data = []

        for page_url in pages:
            try:
                result = client.get_page_details(link=page_url, exact_followers_count=True)
                page_data.append(
                    {
                        "name": result.get("name", "Unknown"),
                        "followers": result.get("followers", 0),
                        "url": page_url,
                    }
                )
            except FacebookScraperError:
                continue

        if page_data:
            # Sort by followers
            page_data.sort(key=lambda x: x["followers"], reverse=True)

            print("\nPage Rankings by Followers:")
            for i, page in enumerate(page_data, 1):
                print(f"{i}. {page['name']}: {page['followers']:,} followers")


def example_error_recovery():
    """Handle errors gracefully and continue processing."""
    print("\n" + "=" * 50)
    print("Error Recovery Example")
    print("=" * 50)

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/InvalidPageThatDoesNotExist12345",
        "https://www.facebook.com/EngenSA",
    ]

    successful = []
    failed = []

    with FacebookScraperClient(api_key=API_KEY) as client:
        for page_url in pages:
            try:
                result = client.get_page_id(page_url)
                successful.append(page_url)
                print(f"✓ {page_url}")
            except FacebookScraperError as e:
                failed.append((page_url, str(e)))
                print(f"✗ {page_url}: {e}")

    print(f"\nSummary: {len(successful)} successful, {len(failed)} failed")
    if failed:
        print("\nFailed pages:")
        for url, error in failed:
            print(f"  - {url}: {error}")


def example_custom_processing():
    """Custom data processing pipeline."""
    print("\n" + "=" * 50)
    print("Custom Processing Pipeline Example")
    print("=" * 50)

    def process_page(client, url):
        """Process a single page and return formatted data."""
        try:
            # Get page details
            details = client.get_page_details(
                link=url, exact_followers_count=True, show_verified_badge=True
            )

            # Calculate engagement rate (if we have the data)
            followers = details.get("followers", 0)
            likes = details.get("likes", 0)
            engagement = (likes / followers * 100) if followers > 0 else 0

            return {
                "name": details.get("name"),
                "followers": followers,
                "likes": likes,
                "engagement_rate": round(engagement, 2),
                "verified": details.get("verified", False),
                "status": "success",
            }
        except FacebookScraperError as e:
            return {"name": url, "status": "error", "error": str(e)}

    pages = [
        "https://www.facebook.com/MazdaItalia",
        "https://www.facebook.com/EngenSA",
    ]

    with FacebookScraperClient(api_key=API_KEY) as client:
        results = [process_page(client, url) for url in pages]

    # Display results
    for result in results:
        if result["status"] == "success":
            print(f"\n{result['name']}:")
            print(f"  Followers: {result['followers']:,}")
            print(f"  Likes: {result['likes']:,}")
            print(f"  Engagement Rate: {result['engagement_rate']}%")
            print(f"  Verified: {'Yes' if result['verified'] else 'No'}")
        else:
            print(f"\n{result['name']}: Error - {result['error']}")


if __name__ == "__main__":
    print("\n" + "#" * 50)
    print("# Facebook Scraper SDK - Advanced Examples")
    print("#" * 50)

    if not API_KEY:
        print("Error: Please set RAPIDAPI_KEY environment variable")
        exit(1)

    try:
        example_batch_processing()
        example_retry_logic()
        example_data_extraction()
        example_comparison()
        example_error_recovery()
        example_custom_processing()

        print("\n" + "=" * 50)
        print("All advanced examples completed!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
