import pytest
import allure
from playwright.sync_api import sync_playwright
from src.main.java.com.framework.utils.config_reader import ConfigReader
from core.utils.browser_utility import BrowserUtility
from core.listeners.test_listener import TestListener
from src.main.java.com.framework.constants.application_constants import ApplicationConstants
import logging
from datetime import datetime
import os

# Configure pytest plugins
pytest_plugins = [
    "core.listeners.test_listener",
    "core.listeners.retry_analyzer"
]


@pytest.fixture(scope="session")
def config():
    """Load configuration for the test session"""
    return ConfigReader()


@pytest.fixture(scope="session")
def browser_utility():
    """Initialize browser utility for UI tests"""
    return BrowserUtility()


@pytest.fixture(scope="function")
def browser_context(browser_utility):
    """Create browser context for each test"""
    with sync_playwright() as playwright:
        context = browser_utility.create_browser_context(playwright)
        yield context
        context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Create page instance for each test"""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(autouse=True)
def setup_test_logging(request):
    """Setup logging for each test"""
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create test-specific log file
    log_file = f"logs/{test_name}_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    yield

    # Cleanup after test
    logging.shutdown()


@pytest.fixture(autouse=True)
def setup_allure_environment():
    """Setup Allure environment properties"""
    allure_results_dir = "reports/allure/allure-results"
    os.makedirs(allure_results_dir, exist_ok=True)

    env_props = f"""{allure_results_dir}/environment.properties"""
    with open(env_props, 'w') as f:
        f.write(f"Environment={ApplicationConstants.ENVIRONMENT}\\n")
        f.write(f"Browser={ApplicationConstants.BROWSER}\\n")
        f.write(f"Base.URL={ApplicationConstants.BASE_URL}\\n")
        f.write(f"Test.Suite={ApplicationConstants.TEST_SUITE}\\n")


def pytest_configure(config):
    """Configure pytest with custom options"""
    config.addinivalue_line("markers", "flaky: mark test as flaky")
    config.addinivalue_line("markers", "timeout: mark test with timeout")


def pytest_runtest_makereport(item, call):
    """Create test report with screenshot on failure"""
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed - take screenshot if UI test
            if hasattr(item, 'funcargs') and 'page' in item.funcargs:
                page = item.funcargs['page']
                screenshot_path = f"screenshots/failed/{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Setup before each test"""
    # Add test metadata to Allure
    allure.dynamic.label("feature", item.parent.name)
    allure.dynamic.label("story", item.name)

    # Set test priority based on markers
    if item.get_closest_marker("critical"):
        allure.dynamic.label("priority", "Critical")
    elif item.get_closest_marker("medium"):
        allure.dynamic.label("priority", "Medium")
    else:
        allure.dynamic.label("priority", "Low")