"""
Base Test class that all test classes should extend
"""
import pytest
import logging
import allure
import os
from typing import Any, Dict, List
from datetime import datetime
from pathlib import Path
from core.utils.config_reader import ConfigReader
from core.utils.browser_utility import BrowserUtility
from core.utils.api_client_utility import APIClientUtility
from core.constants.application_constants import ApplicationConstants


class BaseTest:
    """
    Base test class providing common functionality for all tests
    All test classes should inherit from this class
    """

    def __init__(self):
        """Initialize base test with configuration and utilities"""
        self.config = ConfigReader()
        self.logger = self._setup_logger()
        self.browser_utility = None
        self.api_client = None
        self.test_name = None
        self.test_start_time = None
        self.test_data = {}

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logger for the test class
        Returns: Configured logger instance
        """
        logger = logging.getLogger(self.__class__.__name__)

        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # File handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f"{self.__class__.__name__}_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add handlers
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)

        return logger

    @pytest.fixture(autouse=True)
    def setup_test(self, request):
        """
        Setup method called before each test
        Args:
            request: pytest request fixture
        """
        self.test_name = request.node.name
        self.test_start_time = datetime.now()

        self.logger.info("=" * 80)
        self.logger.info(f"Starting test: {self.test_name}")
        self.logger.info(f"Test class: {self.__class__.__name__}")
        self.logger.info(f"Start time: {self.test_start_time}")
        self.logger.info("=" * 80)

        # Add test information to Allure
        allure.dynamic.title(self.test_name)
        allure.dynamic.description(f"Test: {self.test_name}")
        allure.dynamic.label("framework", "Hybrid Automation Framework")
        allure.dynamic.label("test_class", self.__class__.__name__)

        # Add environment info to Allure
        self._add_allure_environment_info()

        yield

        # Teardown after test
        self.cleanup_test()

    def _add_allure_environment_info(self):
        """Add environment information to Allure report"""
        try:
            with allure.step("Test Environment Information"):
                allure.attach(
                    f"Environment: {ApplicationConstants.ENVIRONMENT}\n"
                    f"Browser: {ApplicationConstants.BROWSER}\n"
                    f"Base URL: {ApplicationConstants.BASE_URL}\n"
                    f"API Base URL: {ApplicationConstants.API_BASE_URL}",
                    name="Environment Info",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            self.logger.warning(f"Could not add environment info to Allure: {e}")

    def setup_browser(self, browser_type: str = None, headless: bool = None):
        """
        Setup browser for UI tests
        Args:
            browser_type: Browser type (chrome, firefox, safari, edge)
            headless: Run browser in headless mode
        """
        try:
            if not self.browser_utility:
                self.browser_utility = BrowserUtility()

            # Override with parameters if provided
            if headless is not None:
                self.config.config.set('browser', 'headless', str(headless))

            self.browser_utility.initialize_browser(browser_type)
            self.browser_utility.create_browser_context()
            self.browser_utility.create_page()

            self.logger.info(f"Browser setup completed: {browser_type or 'default'}")

            with allure.step(f"Setup browser: {browser_type or 'default'}"):
                pass

        except Exception as e:
            self.logger.error(f"Browser setup failed: {e}")
            raise

    def setup_api_client(self, base_url: str = None):
        """
        Setup API client for API tests
        Args:
            base_url: Override default API base URL
        """
        try:
            if not self.api_client:
                self.api_client = APIClientUtility()

            # Override base URL if provided
            if base_url:
                self.api_client.base_url = base_url

            self.logger.info(f"API client setup completed: {self.api_client.base_url}")

            with allure.step(f"Setup API client: {self.api_client.base_url}"):
                pass

        except Exception as e:
            self.logger.error(f"API client setup failed: {e}")
            raise

    def cleanup_test(self):
        """Cleanup method called after each test"""
        test_end_time = datetime.now()
        test_duration = (test_end_time - self.test_start_time).total_seconds()

        self.logger.info("=" * 80)
        self.logger.info(f"Test completed: {self.test_name}")
        self.logger.info(f"Duration: {test_duration:.2f} seconds")
        self.logger.info("=" * 80)

        # Close browser if initialized
        if self.browser_utility:
            try:
                self.browser_utility.close_browser()
                self.logger.info("Browser closed successfully")
            except Exception as e:
                self.logger.warning(f"Error closing browser: {e}")

        # Log test duration to Allure
        with allure.step(f"Test Duration: {test_duration:.2f}s"):
            pass

    def take_screenshot(self, description: str = "Screenshot"):
        """
        Take screenshot and attach to Allure report
        Args:
            description: Description for the screenshot
        """
        if self.browser_utility and self.browser_utility.page:
            try:
                screenshot_path = self.browser_utility.take_screenshot(
                    filename=f"{self.test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )

                # Attach to Allure
                allure.attach.file(
                    screenshot_path,
                    name=description,
                    attachment_type=allure.attachment_type.PNG
                )

                self.logger.info(f"Screenshot captured: {description}")

            except Exception as e:
                self.logger.error(f"Failed to take screenshot: {e}")
        else:
            self.logger.warning("Browser not initialized, cannot take screenshot")

    def log_test_step(self, step_description: str):
        """
        Log test step with Allure
        Args:
            step_description: Description of the test step
        """
        self.logger.info(f"TEST STEP: {step_description}")
        with allure.step(step_description):
            pass

    def attach_text_to_report(self, text: str, name: str = "Additional Info"):
        """
        Attach text to Allure report
        Args:
            text: Text to attach
            name: Name of the attachment
        """
        allure.attach(
            text,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )

    def attach_json_to_report(self, data: Dict, name: str = "JSON Data"):
        """
        Attach JSON data to Allure report
        Args:
            data: Dictionary to attach
            name: Name of the attachment
        """
        import json
        allure.attach(
            json.dumps(data, indent=2),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )

    # ========================================================================
    # ASSERTION METHODS
    # ========================================================================

    def assert_equals(self, actual: Any, expected: Any, message: str = ""):
        """
        Assert that two values are equal
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        try:
            assert actual == expected, \
                f"{message}. Expected: '{expected}', Actual: '{actual}'"

            self.logger.info(f"✓ Assertion passed: {actual} == {expected}")

            with allure.step(f"Assert equals: {actual} == {expected}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_not_equals(self, actual: Any, expected: Any, message: str = ""):
        """
        Assert that two values are not equal
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        try:
            assert actual != expected, \
                f"{message}. Both values are: '{actual}'"

            self.logger.info(f"✓ Assertion passed: {actual} != {expected}")

            with allure.step(f"Assert not equals: {actual} != {expected}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_true(self, condition: bool, message: str = ""):
        """
        Assert that condition is true
        Args:
            condition: Boolean condition
            message: Custom assertion message
        """
        try:
            assert condition is True, \
                f"{message}. Condition evaluated to False"

            self.logger.info(f"✓ Assertion passed: Condition is True")

            with allure.step(f"Assert True: {message}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_false(self, condition: bool, message: str = ""):
        """
        Assert that condition is false
        Args:
            condition: Boolean condition
            message: Custom assertion message
        """
        try:
            assert condition is False, \
                f"{message}. Condition evaluated to True"

            self.logger.info(f"✓ Assertion passed: Condition is False")

            with allure.step(f"Assert False: {message}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_in(self, item: Any, container: Any, message: str = ""):
        """
        Assert that item is in container
        Args:
            item: Item to check
            container: Container (list, string, dict, etc.)
            message: Custom assertion message
        """
        try:
            assert item in container, \
                f"{message}. '{item}' not found in '{container}'"

            self.logger.info(f"✓ Assertion passed: '{item}' in container")

            with allure.step(f"Assert '{item}' in container"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_not_in(self, item: Any, container: Any, message: str = ""):
        """
        Assert that item is not in container
        Args:
            item: Item to check
            container: Container (list, string, dict, etc.)
            message: Custom assertion message
        """
        try:
            assert item not in container, \
                f"{message}. '{item}' found in '{container}'"

            self.logger.info(f"✓ Assertion passed: '{item}' not in container")

            with allure.step(f"Assert '{item}' not in container"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_is_none(self, value: Any, message: str = ""):
        """
        Assert that value is None
        Args:
            value: Value to check
            message: Custom assertion message
        """
        try:
            assert value is None, \
                f"{message}. Value is not None: '{value}'"

            self.logger.info(f"✓ Assertion passed: Value is None")

            with allure.step("Assert value is None"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_is_not_none(self, value: Any, message: str = ""):
        """
        Assert that value is not None
        Args:
            value: Value to check
            message: Custom assertion message
        """
        try:
            assert value is not None, \
                f"{message}. Value is None"

            self.logger.info(f"✓ Assertion passed: Value is not None")

            with allure.step("Assert value is not None"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_greater_than(self, actual: Any, expected: Any, message: str = ""):
        """
        Assert that actual is greater than expected
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        try:
            assert actual > expected, \
                f"{message}. {actual} is not greater than {expected}"

            self.logger.info(f"✓ Assertion passed: {actual} > {expected}")

            with allure.step(f"Assert {actual} > {expected}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_less_than(self, actual: Any, expected: Any, message: str = ""):
        """
        Assert that actual is less than expected
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        try:
            assert actual < expected, \
                f"{message}. {actual} is not less than {expected}"

            self.logger.info(f"✓ Assertion passed: {actual} < {expected}")

            with allure.step(f"Assert {actual} < {expected}"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_contains(self, text: str, substring: str, message: str = ""):
        """
        Assert that text contains substring
        Args:
            text: Text to search in
            substring: Substring to find
            message: Custom assertion message
        """
        try:
            assert substring in text, \
                f"{message}. '{substring}' not found in '{text}'"

            self.logger.info(f"✓ Assertion passed: Text contains '{substring}'")

            with allure.step(f"Assert text contains '{substring}'"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_list_equals(self, actual: List, expected: List, message: str = ""):
        """
        Assert that two lists are equal
        Args:
            actual: Actual list
            expected: Expected list
            message: Custom assertion message
        """
        try:
            assert actual == expected, \
                f"{message}. Lists are not equal.\nExpected: {expected}\nActual: {actual}"

            self.logger.info(f"✓ Assertion passed: Lists are equal")

            with allure.step("Assert lists are equal"):
                pass

        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def soft_assert_equals(self, actual: Any, expected: Any, message: str = ""):
        """
        Soft assertion - logs failure but doesn't stop execution
        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        try:
            assert actual == expected, \
                f"{message}. Expected: '{expected}', Actual: '{actual}'"
            self.logger.info(f"✓ Soft assertion passed: {actual} == {expected}")
        except AssertionError as e:
            self.logger.warning(f"⚠ Soft assertion failed: {e}")
            # Don't raise, just log

    # ========================================================================
    # WAIT METHODS
    # ========================================================================

    def wait_for_condition(self, condition_func, timeout: int = 30,
                           poll_frequency: float = 0.5, message: str = ""):
        """
        Wait for a condition to become true
        Args:
            condition_func: Function that returns boolean
            timeout: Maximum wait time in seconds
            poll_frequency: How often to check condition
            message: Custom message for timeout
        Returns:
            True if condition met, raises TimeoutError otherwise
        """
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    self.logger.info(f"✓ Condition met: {message}")
                    return True
            except Exception as e:
                self.logger.debug(f"Condition check failed: {e}")

            time.sleep(poll_frequency)

        error_msg = f"Timeout waiting for condition: {message}"
        self.logger.error(error_msg)
        self.take_screenshot("Wait_Timeout")
        raise TimeoutError(error_msg)