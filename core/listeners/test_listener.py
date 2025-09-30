# src/main/java/com/framework/listeners/test_listener.py
"""
Test Listener for pytest hooks
"""
import pytest
import logging
import allure
from datetime import datetime
import os


class TestListener:
    """Custom test listener for pytest"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Capture screenshot on test completion"""
        outcome = yield
        report = outcome.get_result()

        if self.screenshots_enabled and report.when == "call":
            if hasattr(item, 'funcargs') and 'page' in item.funcargs:
                self._capture_screenshot(item, report)

    def _capture_screenshot(self, item, report):
        """Capture and attach screenshot"""
        try:
            page = item.funcargs['page']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if report.failed:
                folder = "failed"
                status = "FAILED"
            else:
                folder = "passed"
                status = "PASSED"

            screenshot_path = f"screenshots/{folder}/{item.name}_{timestamp}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            page.screenshot(path=screenshot_path, full_page=True)

            allure.attach.file(
                screenshot_path,
                name=f"{status} - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            self.logger.info(f"Screenshot captured: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")