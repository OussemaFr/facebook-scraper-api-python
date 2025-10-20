# Path: facebook-scraper-python/tests/test_retry.py

"""Tests for retry logic and rate limiting."""

import time
from unittest.mock import Mock, patch

import pytest

from facebook_scraper_sdk import RateLimiter, RateLimitError, retry_with_backoff


class TestRetryWithBackoff:
    """Test retry_with_backoff decorator."""

    def test_retry_on_rate_limit_error(self):
        """Test that function retries on RateLimitError."""
        mock_func = Mock(
            side_effect=[
                RateLimitError("Rate limit"),
                RateLimitError("Rate limit"),
                {"success": True},
            ]
        )

        @retry_with_backoff(max_retries=3, backoff_factor=0.1)
        def test_func():
            return mock_func()

        result = test_func()

        assert result == {"success": True}
        assert mock_func.call_count == 3

    def test_raises_after_max_retries(self):
        """Test that exception is raised after max retries."""
        mock_func = Mock(side_effect=RateLimitError("Rate limit"))

        @retry_with_backoff(max_retries=2, backoff_factor=0.1)
        def test_func():
            return mock_func()

        with pytest.raises(RateLimitError):
            test_func()

        assert mock_func.call_count == 2

    def test_no_retry_on_other_exceptions(self):
        """Test that other exceptions are not retried."""
        mock_func = Mock(side_effect=ValueError("Some error"))

        @retry_with_backoff(max_retries=3, backoff_factor=0.1)
        def test_func():
            return mock_func()

        with pytest.raises(ValueError):
            test_func()

        assert mock_func.call_count == 1

    def test_exponential_backoff(self):
        """Test that backoff time increases exponentially."""
        call_times = []

        def mock_func():
            call_times.append(time.time())
            if len(call_times) < 3:
                raise RateLimitError("Rate limit")
            return {"success": True}

        @retry_with_backoff(max_retries=3, backoff_factor=0.1)
        def test_func():
            return mock_func()

        result = test_func()

        assert result == {"success": True}
        assert len(call_times) == 3

        # Check that delays are approximately exponential
        # With backoff_factor=0.1:
        # First retry (attempt 0): 0.1 * (2^0) = 0.1s
        # Second retry (attempt 1): 0.1 * (2^1) = 0.2s
        if len(call_times) >= 3:
            delay1 = call_times[1] - call_times[0]
            delay2 = call_times[2] - call_times[1]

            # Allow for some timing variance
            assert 0.08 < delay1 < 0.15  # ~0.1s with tolerance
            assert 0.15 < delay2 < 0.25  # ~0.2s with tolerance

            # Second delay should be roughly double the first
            assert delay2 > delay1


class TestRateLimiter:
    """Test RateLimiter class."""

    def test_allows_requests_within_limit(self):
        """Test that requests are allowed when under limit."""
        limiter = RateLimiter(max_requests=5, time_window=1)

        # Should allow 5 requests without waiting
        for _ in range(5):
            start = time.time()
            limiter.wait_if_needed()
            elapsed = time.time() - start
            assert elapsed < 0.1  # Should be instant

    def test_enforces_rate_limit(self):
        """Test that rate limit is enforced."""
        limiter = RateLimiter(max_requests=2, time_window=1)

        # First 2 requests should be instant
        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Third request should wait
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start

        # Should have waited approximately 1 second
        assert elapsed >= 0.9

    def test_resets_after_time_window(self):
        """Test that counter resets after time window."""
        limiter = RateLimiter(max_requests=2, time_window=0.5)

        # Use up the limit
        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Wait for time window to pass
        time.sleep(0.6)

        # Should be allowed again without waiting
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start

        assert elapsed < 0.1
