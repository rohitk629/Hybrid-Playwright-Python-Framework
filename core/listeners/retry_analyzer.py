"""
Retry Analyzer for flaky tests
"""
import pytest
import logging
from typing import Dict


class RetryAnalyzer:
    """Retry analyzer for flaky tests"""

    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.retry_counts: Dict[str, int] = {}
        self.logger = logging.getLogger(__name__)

    def should_retry(self, test_name: str) -> bool:
        """Check if test should be retried"""
        if test_name not in self.retry_counts:
            self.retry_counts[test_name] = 0

        if self.retry_counts[test_name] < self.max_retries:
            self.retry_counts[test_name] += 1
            self.logger.info(f"Retrying test: {test_name} (Attempt {self.retry_counts[test_name]})")
            return True

        return False

    def reset_retry_count(self, test_name: str):
        """Reset retry count for test"""
        if test_name in self.retry_counts:
            del self.retry_counts[test_name]


# Configure pytest for retry
def pytest_configure(config):
    """Configure pytest with retry plugin"""
    config.addinivalue_line(
        "markers", "flaky: mark test to automatically retry on failure"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    """Hook to implement retry logic"""
    if item.get_closest_marker("flaky"):
        retry_analyzer = RetryAnalyzer()

        for attempt in range(retry_analyzer.max_retries + 1):
            try:
                item.ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)
                item.ihook.pytest_runtest_setup(item=item)
                item.ihook.pytest_runtest_call(item=item)
                item.ihook.pytest_runtest_teardown(item=item, nextitem=nextitem)
                item.ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)
                return True
            except Exception as e:
                if attempt < retry_analyzer.max_retries:
                    logging.warning(f"Test failed, retrying... (Attempt {attempt + 1})")
                    continue
                else:
                    raise
    return None