"""
Base Test class that all test classes should extend
Provides common functionality for test setup, teardown, and assertions

File: framework/base/base_test.py
Author: Automation Team
Description: Base class for all test classes with comprehensive setup, teardown,
             assertions, and reporting capabilities.
"""

import pytest
import logging
import allure
import os
from typing import Any, Dict, List, Callable
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

    Features:
    - Automatic setup and teardown
    - Browser initialization for UI tests
    - API client initialization for API tests
    - Comprehensive assertion methods
    - Screenshot capture on failure
    - Test step logging
    - Allure report integration
    - Test data management
    - Retry mechanism support
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
        self.soft_assertions = []

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logger for the test class

        Returns:
            Configured logger instance
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

    # ========================================================================
    # PYTEST FIXTURES
    # ========================================================================

    @pytest.fixture(autouse=True)
    def setup_test(self, request):
        """
        Setup method called before each test (pytest fixture)

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

        # Clear soft assertions for each test
        self.soft_assertions = []

        yield

        # Check soft assertions
        self._verify_soft_assertions()

        # Teardown after test
        self.cleanup_test()

    def _add_allure_environment_info(self):
        """Add environment information to Allure report"""
        try:
            with allure.step("Test Environment Information"):
                env_info = (
                    f"Environment: {ApplicationConstants.ENVIRONMENT}\n"
                    f"Browser: {ApplicationConstants.BROWSER}\n"
                    f"Base URL: {ApplicationConstants.BASE_URL}\n"
                    f"API Base URL: {ApplicationConstants.API_BASE_URL}\n"
                    f"Python Version: {os.sys.version.split()[0]}"
                )
                allure.attach(
                    env_info,
                    name="Environment Info",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            self.logger.warning(f"Could not add environment info to Allure: {e}")

    # ========================================================================
    # SETUP METHODS
    # ========================================================================

    def setup_browser(self, browser_type: str = None, headless: bool = None):
        """
        Setup browser for UI tests

        Args:
            browser_type: Browser type (chrome, firefox, safari, edge)
            headless: Run browser in headless mode

        Example:
            self.setup_browser()
            self.setup_browser(browser_type="firefox", headless=True)
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
            self.take_screenshot("Browser_Setup_Failed")
            raise

    def setup_api_client(self, base_url: str = None):
        """
        Setup API client for API tests

        Args:
            base_url: Override default API base URL

        Example:
            self.setup_api_client()
            self.setup_api_client(base_url="https://custom-api.com")
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

    def setup_test_data(self, data: Dict[str, Any]):
        """
        Setup test data for the test

        Args:
            data: Test data dictionary

        Example:
            self.setup_test_data({"username": "test@example.com", "password": "pass123"})
        """
        self.test_data = data
        self.logger.info(f"Test data setup: {list(data.keys())}")

    # ========================================================================
    # CLEANUP METHODS
    # ========================================================================

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

    # ========================================================================
    # SCREENSHOT METHODS
    # ========================================================================

    def take_screenshot(self, description: str = "Screenshot"):
        """
        Take screenshot and attach to Allure report

        Args:
            description: Description for the screenshot

        Example:
            self.take_screenshot("Login Page")
            self.take_screenshot("After Button Click")
        """
        if self.browser_utility and self.browser_utility.page:
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{self.test_name}_{description}_{timestamp}.png"
                screenshot_path = self.browser_utility.take_screenshot(filename=filename)

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

    def take_screenshot_on_failure(self):
        """Take screenshot when test fails (called automatically)"""
        self.take_screenshot("Test_Failure")

    # ========================================================================
    # LOGGING AND REPORTING METHODS
    # ========================================================================

    def log_test_step(self, step_description: str):
        """
        Log test step with Allure

        Args:
            step_description: Description of the test step

        Example:
            self.log_test_step("Step 1: Navigate to login page")
            self.log_test_step("Step 2: Enter credentials")
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

        Example:
            self.attach_text_to_report("User ID: 12345", "User Information")
        """
        allure.attach(
            text,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
        self.logger.debug(f"Attached text to report: {name}")

    def attach_json_to_report(self, data: Dict, name: str = "JSON Data"):
        """
        Attach JSON data to Allure report

        Args:
            data: Dictionary to attach
            name: Name of the attachment

        Example:
            self.attach_json_to_report({"user": "john", "age": 30}, "User Data")
        """
        import json
        allure.attach(
            json.dumps(data, indent=2),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )
        self.logger.debug(f"Attached JSON to report: {name}")

    def attach_file_to_report(self, file_path: str, name: str = "File"):
        """
        Attach file to Allure report

        Args:
            file_path: Path to file
            name: Name of the attachment

        Example:
            self.attach_file_to_report("test_data/sample.pdf", "Sample Document")
        """
        try:
            allure.attach.file(
                file_path,
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )
            self.logger.debug(f"Attached file to report: {name}")
        except Exception as e:
            self.logger.error(f"Failed to attach file: {e}")

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

        Example:
            self.assert_equals(page_title, "Home", "Page title should be Home")
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

        Example:
            self.assert_not_equals(status_code, 404, "Should not return 404")
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

        Example:
            self.assert_true(user.is_logged_in(), "User should be logged in")
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

        Example:
            self.assert_false(error_displayed, "No error should be displayed")
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

        Example:
            self.assert_in("apple", fruits_list, "Apple should be in the list")
            self.assert_in("error", error_message, "Message should contain 'error'")
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

        Example:
            self.assert_not_in("inactive", status_list, "Inactive should not be present")
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

        Example:
            self.assert_is_none(error, "Error should be None")
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

        Example:
            self.assert_is_not_none(user_id, "User ID should not be None")
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

        Example:
            self.assert_greater_than(score, 50, "Score should be greater than 50")
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

        Example:
            self.assert_less_than(response_time, 2.0, "Response time should be under 2s")
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

    def assert_greater_or_equal(self, actual: Any, expected: Any, message: str = ""):
        """Assert that actual is greater than or equal to expected"""
        try:
            assert actual >= expected, \
                f"{message}. {actual} is not greater than or equal to {expected}"
            self.logger.info(f"✓ Assertion passed: {actual} >= {expected}")
        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_less_or_equal(self, actual: Any, expected: Any, message: str = ""):
        """Assert that actual is less than or equal to expected"""
        try:
            assert actual <= expected, \
                f"{message}. {actual} is not less than or equal to {expected}"
            self.logger.info(f"✓ Assertion passed: {actual} <= {expected}")
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

        Example:
            self.assert_contains(page_content, "Welcome", "Page should contain Welcome")
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

    def assert_starts_with(self, text: str, prefix: str, message: str = ""):
        """Assert that text starts with prefix"""
        try:
            assert text.startswith(prefix), \
                f"{message}. Text '{text}' does not start with '{prefix}'"
            self.logger.info(f"✓ Assertion passed: Text starts with '{prefix}'")
        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_ends_with(self, text: str, suffix: str, message: str = ""):
        """Assert that text ends with suffix"""
        try:
            assert text.endswith(suffix), \
                f"{message}. Text '{text}' does not end with '{suffix}'"
            self.logger.info(f"✓ Assertion passed: Text ends with '{suffix}'")
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

        Example:
            self.assert_list_equals([1,2,3], [1,2,3], "Lists should match")
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

    def assert_dict_equals(self, actual: Dict, expected: Dict, message: str = ""):
        """Assert that two dictionaries are equal"""
        try:
            assert actual == expected, \
                f"{message}. Dictionaries are not equal.\nExpected: {expected}\nActual: {actual}"
            self.logger.info(f"✓ Assertion passed: Dictionaries are equal")
        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    def assert_length(self, container: Any, expected_length: int, message: str = ""):
        """
        Assert container has expected length

        Args:
            container: Container (list, string, etc.)
            expected_length: Expected length
            message: Custom assertion message

        Example:
            self.assert_length(user_list, 10, "Should have 10 users")
        """
        try:
            actual_length = len(container)
            assert actual_length == expected_length, \
                f"{message}. Expected length {expected_length}, got {actual_length}"
            self.logger.info(f"✓ Assertion passed: Length is {expected_length}")
        except AssertionError as e:
            self.logger.error(f"✗ Assertion failed: {e}")
            self.take_screenshot("Assertion_Failed")
            raise

    # ========================================================================
    # SOFT ASSERTION METHODS
    # ========================================================================

    def soft_assert_equals(self, actual: Any, expected: Any, message: str = ""):
        """
        Soft assertion - logs failure but doesn't stop execution

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message

        Example:
            self.soft_assert_equals(color, "red", "Color should be red")
        """
        try:
            assert actual == expected, \
                f"{message}. Expected: '{expected}', Actual: '{actual}'"
            self.logger.info(f"✓ Soft assertion passed: {actual} == {expected}")
        except AssertionError as e:
            error_msg = f"Soft assertion failed: {e}"
            self.logger.warning(f"⚠ {error_msg}")
            self.soft_assertions.append(error_msg)
            self.take_screenshot("Soft_Assertion_Failed")

    def soft_assert_true(self, condition: bool, message: str = ""):
        """Soft assert that condition is true"""
        try:
            assert condition is True, f"{message}. Condition evaluated to False"
            self.logger.info(f"✓ Soft assertion passed: Condition is True")
        except AssertionError as e:
            error_msg = f"Soft assertion failed: {e}"
            self.logger.warning(f"⚠ {error_msg}")
            self.soft_assertions.append(error_msg)
            self.take_screenshot("Soft_Assertion_Failed")

    def _verify_soft_assertions(self):
        """Verify all soft assertions at the end of test"""
        if self.soft_assertions:
            error_summary = "\n".join([f"  - {error}" for error in self.soft_assertions])
            self.logger.error(f"Test had {len(self.soft_assertions)} soft assertion failures:\n{error_summary}")
            raise AssertionError(f"Test had {len(self.soft_assertions)} soft assertion failures:\n{error_summary}")

    # ========================================================================
    # WAIT AND RETRY METHODS
    # ========================================================================

    def wait_for_condition(self, condition_func: Callable, timeout: int = 30,
                           poll_frequency: float = 0.5, message: str = "") -> bool:
        """
        Wait for a condition to become true

        Args:
            condition_func: Function that returns boolean
            timeout: Maximum wait time in seconds
            poll_frequency: How often to check condition
            message: Custom message for timeout

        Returns:
            True if condition met

        Raises:
            TimeoutError: If condition not met within timeout

        Example:
            self.wait_for_condition(
                lambda: self.page.is_element_visible("div.content"),
                timeout=10,
                message="Waiting for content to be visible"
            )
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

    def retry_on_exception(self, func: Callable, max_attempts: int = 3,
                           delay: int = 2, exceptions: tuple = (Exception,)) -> Any:
        """
        Retry function on exception

        Args:
            func: Function to execute
            max_attempts: Maximum number of attempts
            delay: Delay between attempts
            exceptions: Tuple of exceptions to catch

        Returns:
            Function result

        Example:
            result = self.retry_on_exception(
                lambda: api_client.get_user(user_id),
                max_attempts=3,
                delay=1
            )
        """
        import time

        for attempt in range(1, max_attempts + 1):
            try:
                return func()
            except exceptions as e:
                if attempt == max_attempts:
                    self.logger.error(f"All {max_attempts} attempts failed")
                    raise
                self.logger.warning(f"Attempt {attempt} failed: {e}. Retrying...")
                time.sleep(delay)

# ============================================================================
# END OF BASE TEST CLASS
# ============================================================================