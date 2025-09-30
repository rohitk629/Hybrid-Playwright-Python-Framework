"""
Application Constants
Centralized configuration constants for the automation framework

File: framework/constants/application_constants.py
Author: Automation Team
Description: Contains all application-level constants loaded from configuration files.
             Provides easy access to framework settings throughout the codebase.
"""

import os
from pathlib import Path
from core.utils.config_reader import ConfigReader


class ApplicationConstants:
    """
    Application level constants
    All constants are loaded from config files and can be overridden by environment variables
    """

    # Initialize config reader
    config = ConfigReader()

    # ========================================================================
    # ENVIRONMENT CONFIGURATION
    # ========================================================================

    # Current environment (dev, qa, staging, prod)
    ENVIRONMENT = os.getenv('TEST_ENV') or config.get_property("app.environment", "qa")

    # Application name and version
    APPLICATION_NAME = config.get_property("app.application.name", "Hybrid Automation Framework")
    VERSION = config.get_property("app.version", "1.0.0")

    # Debug mode
    DEBUG_MODE = config.get_bool_property("app.debug.mode", False)

    # ========================================================================
    # APPLICATION URLS
    # ========================================================================

    # Base URL for application under test
    BASE_URL = os.getenv('BASE_URL') or config.get_property("app.base.url", "https://www.saucedemo.com")

    # API Base URL
    API_BASE_URL = os.getenv('API_BASE_URL') or config.get_property("api.base.url", "https://reqres.in/api")

    # Login URL (derived from base URL)
    LOGIN_URL = f"{BASE_URL}/login" if BASE_URL else None

    # Dashboard URL
    DASHBOARD_URL = f"{BASE_URL}/dashboard" if BASE_URL else None

    # ========================================================================
    # BROWSER CONFIGURATION
    # ========================================================================

    # Browser type (chrome, firefox, safari, edge)
    BROWSER = os.getenv('BROWSER') or config.get_property("browser.type", "chrome")

    # Headless mode
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true' or \
               config.get_bool_property("browser.headless", False)

    # Window maximize
    WINDOW_MAXIMIZE = config.get_bool_property("browser.window.maximize", True)

    # Accept insecure certificates
    ACCEPT_INSECURE_CERTS = config.get_bool_property("browser.accept.insecure.certs", True)

    # Download path
    DOWNLOAD_PATH = config.get_property("browser.download.path", "downloads/")

    # Viewport size
    VIEWPORT_WIDTH = config.get_int_property("browser.viewport.width", 1920)
    VIEWPORT_HEIGHT = config.get_int_property("browser.viewport.height", 1080)

    # ========================================================================
    # TIMEOUT CONFIGURATION
    # ========================================================================

    # Application timeout
    APP_TIMEOUT = config.get_int_property("app.timeout", 30)

    # Browser timeouts (in milliseconds)
    IMPLICIT_WAIT = config.get_int_property("browser.implicit.wait", 10) * 1000
    EXPLICIT_WAIT = config.get_int_property("browser.explicit.wait", 30) * 1000
    PAGE_LOAD_TIMEOUT = config.get_int_property("browser.page.load.timeout", 60) * 1000

    # API timeout (in seconds)
    API_TIMEOUT = config.get_int_property("api.timeout", 30)
    API_CONNECTION_TIMEOUT = config.get_int_property("api.connection.timeout", 30)
    API_READ_TIMEOUT = config.get_int_property("api.read.timeout", 30)

    # ========================================================================
    # API CONFIGURATION
    # ========================================================================

    # API retry count
    API_RETRY_COUNT = config.get_int_property("api.retry.count", 3)

    # API content type
    API_CONTENT_TYPE = config.get_property("api.content.type", "application/json")

    # API accept header
    API_ACCEPT = config.get_property("api.accept", "application/json")

    # Verify SSL
    API_VERIFY_SSL = config.get_bool_property("api.verify.ssl", True)

    # ========================================================================
    # TEST CONFIGURATION
    # ========================================================================

    # Test suite name
    TEST_SUITE = config.get_property("test.suite", "Hybrid Automation Framework")

    # Parallel execution count
    PARALLEL_COUNT = config.get_int_property("test.parallel.count", 4)

    # Retry count for failed tests
    RETRY_COUNT = config.get_int_property("test.retry.count", 2)

    # Data provider type (excel, csv, json)
    DATA_PROVIDER_TYPE = config.get_property("test.data.provider.type", "excel")

    # Screenshot settings
    SCREENSHOT_ON_FAILURE = config.get_bool_property("test.screenshot.on.failure", True)
    SCREENSHOT_ON_SUCCESS = config.get_bool_property("test.screenshot.on.success", False)
    TAKE_SCREENSHOT_FOR_PASSED_TESTS = config.get_bool_property(
        "test.take.screenshot.for.passed.tests", False
    )
    TAKE_SCREENSHOT_FOR_FAILED_TESTS = config.get_bool_property(
        "test.take.screenshot.for.failed.tests", True
    )

    # Video recording
    VIDEO_RECORDING = config.get_bool_property("test.video.recording", False)

    # Assertion mode
    SOFT_ASSERT = config.get_bool_property("test.soft.assert", False)
    HARD_ASSERT = config.get_bool_property("test.hard.assert", True)

    # ========================================================================
    # REPORTING CONFIGURATION
    # ========================================================================

    # Allure reporting
    ALLURE_ENABLED = config.get_bool_property("report.allure.enabled", True)
    ALLURE_RESULTS_DIR = config.get_property(
        "report.allure.results.directory",
        "reports/allure/allure-results"
    )
    ALLURE_REPORT_DIR = config.get_property(
        "report.allure.report.directory",
        "reports/allure/allure-report"
    )

    # Extent reporting
    EXTENT_ENABLED = config.get_bool_property("report.extent.enabled", True)
    EXTENT_REPORT_PATH = config.get_property(
        "report.extent.report.path",
        "reports/extent/extent-report.html"
    )

    # Pytest HTML reporting
    PYTEST_HTML_ENABLED = config.get_bool_property("report.pytest.html.enabled", True)
    PYTEST_REPORT_PATH = config.get_property(
        "report.pytest.report.path",
        "reports/pytest/pytest-report.html"
    )

    # Screenshot in report
    SCREENSHOT_ENABLED = config.get_bool_property("report.screenshot.enabled", True)

    # Output directory
    OUTPUT_DIRECTORY = config.get_property("report.output.directory", "reports")

    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================

    # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL = config.get_property("logging.level", "INFO")

    # Log file path
    LOG_FILE_PATH = config.get_property("logging.file.path", "logs/automation.log")

    # Console logging
    CONSOLE_LOGGING_ENABLED = config.get_bool_property("logging.console.enabled", True)

    # File logging
    FILE_LOGGING_ENABLED = config.get_bool_property("logging.file.enabled", True)

    # Log format
    LOG_FORMAT = config.get_property(
        "logging.format",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Log date format
    LOG_DATE_FORMAT = config.get_property("logging.date.format", "%Y-%m-%d %H:%M:%S")

    # Max log file size
    LOG_MAX_FILE_SIZE = config.get_property("logging.max.file.size", "10MB")

    # Log backup count
    LOG_BACKUP_COUNT = config.get_int_property("logging.backup.count", 5)

    # ========================================================================
    # PATH CONFIGURATION
    # ========================================================================

    # Project root path
    PROJECT_ROOT = Path(__file__).parent.parent.parent

    # Framework path
    FRAMEWORK_PATH = PROJECT_ROOT / "framework"

    # Tests path
    TESTS_PATH = PROJECT_ROOT / "tests"

    # Config path
    CONFIG_PATH = PROJECT_ROOT / "config"

    # Test data path
    TEST_DATA_PATH = PROJECT_ROOT / "test_data"
    EXCEL_DATA_PATH = TEST_DATA_PATH / "excel"
    CSV_DATA_PATH = TEST_DATA_PATH / "csv"
    JSON_DATA_PATH = TEST_DATA_PATH / "json"
    XML_DATA_PATH = TEST_DATA_PATH / "xml"

    # Resources path
    RESOURCES_PATH = PROJECT_ROOT / "resources"
    DRIVERS_PATH = RESOURCES_PATH / "drivers"
    TEMPLATES_PATH = RESOURCES_PATH / "templates"

    # Output paths
    SCREENSHOTS_PATH = PROJECT_ROOT / "screenshots"
    SCREENSHOTS_PASSED_PATH = SCREENSHOTS_PATH / "passed"
    SCREENSHOTS_FAILED_PATH = SCREENSHOTS_PATH / "failed"

    LOGS_PATH = PROJECT_ROOT / "logs"

    REPORTS_PATH = PROJECT_ROOT / "reports"
    ALLURE_REPORTS_PATH = REPORTS_PATH / "allure"
    EXTENT_REPORTS_PATH = REPORTS_PATH / "extent"
    PYTEST_REPORTS_PATH = REPORTS_PATH / "pytest"

    DOWNLOADS_PATH = PROJECT_ROOT / "downloads"

    # ========================================================================
    # DATABASE CONFIGURATION (Optional)
    # ========================================================================

    # Database enabled
    DB_ENABLED = config.get_bool_property("database.enabled", False)

    # Database connection details
    DB_HOST = config.get_property("database.host", "localhost")
    DB_PORT = config.get_int_property("database.port", 5432)
    DB_NAME = config.get_property("database.name", "test_db")
    DB_USERNAME = config.get_property("database.username", "testuser")
    DB_PASSWORD = config.get_property("database.password", "testpass")
    DB_DRIVER = config.get_property("database.driver", "postgresql")
    DB_POOL_SIZE = config.get_int_property("database.pool.size", 5)
    DB_CONNECTION_TIMEOUT = config.get_int_property("database.connection.timeout", 30)

    # ========================================================================
    # EMAIL CONFIGURATION (Optional)
    # ========================================================================

    # Email enabled
    EMAIL_ENABLED = config.get_bool_property("email.enabled", False)

    # SMTP configuration
    SMTP_HOST = config.get_property("email.smtp.host", "smtp.gmail.com")
    SMTP_PORT = config.get_int_property("email.smtp.port", 587)

    # Sender details
    SENDER_EMAIL = config.get_property("email.sender.email", "automation@example.com")
    SENDER_PASSWORD = config.get_property("email.sender.password", "")

    # Recipients
    RECIPIENT_EMAILS = config.get_list_property("email.recipient.emails", ",")

    # Email subject prefix
    EMAIL_SUBJECT_PREFIX = config.get_property("email.subject.prefix", "[Automation Report]")

    # Send conditions
    SEND_EMAIL_ON_FAILURE = config.get_bool_property("email.send.on.failure", True)
    SEND_EMAIL_ON_SUCCESS = config.get_bool_property("email.send.on.success", False)

    # ========================================================================
    # SLACK CONFIGURATION (Optional)
    # ========================================================================

    # Slack enabled
    SLACK_ENABLED = config.get_bool_property("slack.enabled", False)

    # Slack webhook URL
    SLACK_WEBHOOK_URL = config.get_property("slack.webhook.url", "")

    # Slack channel
    SLACK_CHANNEL = config.get_property("slack.channel", "#automation-reports")

    # Slack username
    SLACK_USERNAME = config.get_property("slack.username", "Automation Bot")

    # Send conditions
    SEND_SLACK_ON_FAILURE = config.get_bool_property("slack.send.on.failure", True)
    SEND_SLACK_ON_SUCCESS = config.get_bool_property("slack.send.on.success", False)

    # ========================================================================
    # PERFORMANCE CONFIGURATION
    # ========================================================================

    # Response time thresholds (in milliseconds)
    RESPONSE_TIME_THRESHOLD = config.get_int_property("performance.response.time.threshold", 5000)
    API_RESPONSE_TIME_THRESHOLD = config.get_int_property(
        "performance.api.response.time.threshold", 3000
    )
    PAGE_LOAD_TIME_THRESHOLD = config.get_int_property(
        "performance.page.load.time.threshold", 10000
    )

    # ========================================================================
    # PROXY CONFIGURATION (Optional)
    # ========================================================================

    # Proxy enabled
    PROXY_ENABLED = config.get_bool_property("proxy.enabled", False)

    # Proxy details
    PROXY_HOST = config.get_property("proxy.host", "")
    PROXY_PORT = config.get_int_property("proxy.port", 8080)
    PROXY_USERNAME = config.get_property("proxy.username", "")
    PROXY_PASSWORD = config.get_property("proxy.password", "")
    PROXY_BYPASS_LIST = config.get_list_property("proxy.bypass.list", ",")

    # ========================================================================
    # SECURITY CONFIGURATION
    # ========================================================================

    # Encrypt sensitive data
    ENCRYPT_SENSITIVE_DATA = config.get_bool_property("security.encrypt.sensitive.data", True)

    # Mask passwords in logs
    MASK_PASSWORDS_IN_LOGS = config.get_bool_property("security.mask.passwords.in.logs", True)

    # Mask API keys in logs
    MASK_API_KEYS_IN_LOGS = config.get_bool_property("security.mask.api.keys.in.logs", True)

    # ========================================================================
    # CI/CD CONFIGURATION
    # ========================================================================

    # Run mode (local, ci, docker)
    RUN_MODE = os.getenv('RUN_MODE') or config.get_property("ci_cd.run.mode", "local")

    # Headless in CI
    HEADLESS_IN_CI = config.get_bool_property("ci_cd.headless.in.ci", True)

    # Parallel tests in CI
    PARALLEL_TESTS_IN_CI = config.get_int_property("ci_cd.parallel.tests.in.ci", 8)

    # Generate reports in CI
    GENERATE_REPORTS_IN_CI = config.get_bool_property("ci_cd.generate.reports.in.ci", True)

    # ========================================================================
    # SELENIUM GRID CONFIGURATION (Optional)
    # ========================================================================

    # Selenium Grid enabled
    SELENIUM_GRID_ENABLED = config.get_bool_property("selenium_grid.enabled", False)

    # Grid hub URL
    GRID_HUB_URL = config.get_property(
        "selenium_grid.hub.url",
        "http://localhost:4444/wd/hub"
    )

    # Grid browser configuration
    GRID_BROWSER_NAME = config.get_property("selenium_grid.browser.name", "chrome")
    GRID_BROWSER_VERSION = config.get_property("selenium_grid.browser.version", "latest")
    GRID_PLATFORM_NAME = config.get_property("selenium_grid.platform.name", "WINDOWS")

    # ========================================================================
    # FEATURE FLAGS (Optional)
    # ========================================================================

    # Enable experimental features
    ENABLE_EXPERIMENTAL_FEATURES = config.get_bool_property("feature_flags.enable.experimental", False)

    # Enable new login flow
    ENABLE_NEW_LOGIN_FLOW = config.get_bool_property("feature_flags.enable.new.login.flow", False)

    # Enable beta features
    ENABLE_BETA_FEATURES = config.get_bool_property("feature_flags.enable.beta.features", False)

    # ========================================================================
    # MOBILE CONFIGURATION (Optional - for future use)
    # ========================================================================

    # Mobile testing enabled
    MOBILE_TESTING_ENABLED = config.get_bool_property("mobile.enabled", False)

    # Platform (Android, iOS)
    MOBILE_PLATFORM = config.get_property("mobile.platform", "Android")

    # Device name
    MOBILE_DEVICE_NAME = config.get_property("mobile.device.name", "")

    # Platform version
    MOBILE_PLATFORM_VERSION = config.get_property("mobile.platform.version", "")

    # App path
    MOBILE_APP_PATH = config.get_property("mobile.app.path", "")

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @classmethod
    def is_headless_mode(cls) -> bool:
        """Check if running in headless mode"""
        return cls.HEADLESS or (cls.RUN_MODE == 'ci' and cls.HEADLESS_IN_CI)

    @classmethod
    def get_parallel_count(cls) -> int:
        """Get parallel execution count based on run mode"""
        if cls.RUN_MODE == 'ci':
            return cls.PARALLEL_TESTS_IN_CI
        return cls.PARALLEL_COUNT

    @classmethod
    def is_ci_mode(cls) -> bool:
        """Check if running in CI mode"""
        return cls.RUN_MODE == 'ci'

    @classmethod
    def should_take_screenshot(cls, test_passed: bool) -> bool:
        """Determine if screenshot should be taken based on test result"""
        if test_passed:
            return cls.SCREENSHOT_ON_SUCCESS or cls.TAKE_SCREENSHOT_FOR_PASSED_TESTS
        else:
            return cls.SCREENSHOT_ON_FAILURE or cls.TAKE_SCREENSHOT_FOR_FAILED_TESTS

    @classmethod
    def get_browser_config(cls) -> dict:
        """Get browser configuration as dictionary"""
        return {
            "browser": cls.BROWSER,
            "headless": cls.is_headless_mode(),
            "maximize": cls.WINDOW_MAXIMIZE,
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT
            },
            "accept_insecure_certs": cls.ACCEPT_INSECURE_CERTS,
            "download_path": cls.DOWNLOAD_PATH
        }

    @classmethod
    def get_api_config(cls) -> dict:
        """Get API configuration as dictionary"""
        return {
            "base_url": cls.API_BASE_URL,
            "timeout": cls.API_TIMEOUT,
            "retry_count": cls.API_RETRY_COUNT,
            "content_type": cls.API_CONTENT_TYPE,
            "verify_ssl": cls.API_VERIFY_SSL
        }

    @classmethod
    def get_report_config(cls) -> dict:
        """Get reporting configuration as dictionary"""
        return {
            "allure_enabled": cls.ALLURE_ENABLED,
            "extent_enabled": cls.EXTENT_ENABLED,
            "pytest_html_enabled": cls.PYTEST_HTML_ENABLED,
            "screenshot_enabled": cls.SCREENSHOT_ENABLED,
            "output_directory": cls.OUTPUT_DIRECTORY
        }

    @classmethod
    def print_configuration(cls):
        """Print all configuration values (for debugging)"""
        print("\n" + "=" * 80)
        print("APPLICATION CONSTANTS CONFIGURATION")
        print("=" * 80)

        print(f"\nEnvironment: {cls.ENVIRONMENT}")
        print(f"Application: {cls.APPLICATION_NAME} v{cls.VERSION}")
        print(f"Base URL: {cls.BASE_URL}")
        print(f"API URL: {cls.API_BASE_URL}")

        print(f"\nBrowser Configuration:")
        print(f"  Browser: {cls.BROWSER}")
        print(f"  Headless: {cls.is_headless_mode()}")
        print(f"  Viewport: {cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}")

        print(f"\nTest Configuration:")
        print(f"  Parallel Count: {cls.get_parallel_count()}")
        print(f"  Retry Count: {cls.RETRY_COUNT}")
        print(f"  Screenshot on Failure: {cls.SCREENSHOT_ON_FAILURE}")

        print(f"\nReporting:")
        print(f"  Allure: {cls.ALLURE_ENABLED}")
        print(f"  Extent: {cls.EXTENT_ENABLED}")
        print(f"  Output Dir: {cls.OUTPUT_DIRECTORY}")

        print(f"\nLogging:")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Log File: {cls.LOG_FILE_PATH}")

        print("=" * 80 + "\n")

    @classmethod
    def validate_configuration(cls) -> bool:
        """Validate required configuration values are set"""
        errors = []

        if not cls.BASE_URL:
            errors.append("BASE_URL is not set")

        if not cls.API_BASE_URL:
            errors.append("API_BASE_URL is not set")

        if cls.BROWSER not in ['chrome', 'firefox', 'safari', 'edge']:
            errors.append(f"Invalid BROWSER value: {cls.BROWSER}")

        if cls.LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            errors.append(f"Invalid LOG_LEVEL value: {cls.LOG_LEVEL}")

        if errors:
            print("Configuration Validation Errors:")
            for error in errors:
                print(f"  - {error}")
            return False

        return True


# ============================================================================
# MODULE LEVEL FUNCTIONS
# ============================================================================

def get_config_value(key: str, default=None):
    """
    Get configuration value by key

    Args:
        key: Configuration key in format "section.property"
        default: Default value if not found

    Returns:
        Configuration value

    Example:
        timeout = get_config_value("app.timeout", 30)
    """
    config = ConfigReader()
    return config.get_property(key, default)


def is_environment(env_name: str) -> bool:
    """
    Check if current environment matches given name

    Args:
        env_name: Environment name to check

    Returns:
        True if matches

    Example:
        if is_environment("qa"):
            print("Running in QA environment")
    """
    return ApplicationConstants.ENVIRONMENT.lower() == env_name.lower()


def print_all_constants():
    """Print all application constants"""
    ApplicationConstants.print_configuration()


# ============================================================================
# AUTO-VALIDATION ON IMPORT
# ============================================================================

# Validate configuration when module is imported
if __name__ != "__main__":
    if not ApplicationConstants.validate_configuration():
        print("⚠ Warning: Configuration validation failed. Please check config files.")

# ============================================================================
# END OF APPLICATION CONSTANTS
# ============================================================================