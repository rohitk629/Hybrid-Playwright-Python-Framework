import pytest
import allure
from playwright.sync_api import sync_playwright
from core.utils.config_reader import ConfigReader
from core.utils.browser_utility import BrowserUtility
from core.constants.application_constants import ApplicationConstants
import logging
from datetime import datetime
import os


# Configure pytest plugins
# pytest_plugins = []


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
        browser = playwright.chromium.launch(headless=ApplicationConstants.HEADLESS)
        context = browser.new_context(
            viewport={'width': ApplicationConstants.VIEWPORT_WIDTH,
                      'height': ApplicationConstants.VIEWPORT_HEIGHT}
        )
        yield context
        context.close()
        browser.close()


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

    # Create logs directory
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create test-specific log file
    log_file = f"{log_dir}/{test_name}_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )

    yield

    # Cleanup after test
    logging.shutdown()


@pytest.fixture(autouse=True)
def setup_allure_environment():
    """Setup Allure environment properties"""
    allure_results_dir = "reports/allure/allure-results"
    os.makedirs(allure_results_dir, exist_ok=True)

    env_props = f"{allure_results_dir}/environment.properties"
    with open(env_props, 'w') as f:
        f.write(f"Environment={ApplicationConstants.ENVIRONMENT}\n")
        f.write(f"Browser={ApplicationConstants.BROWSER}\n")
        f.write(f"Base.URL={ApplicationConstants.BASE_URL}\n")


def pytest_configure(config):
    """Configure pytest with custom options"""
    # Add custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "ui: mark test as UI test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "critical: mark test as critical priority")
    config.addinivalue_line("markers", "medium: mark test as medium priority")
    config.addinivalue_line("markers", "low: mark test as low priority")

    # Create reports directory structure
    reports_dirs = [
        "reports/pytest",
        "reports/behave",
        "reports/allure/allure-results",
        "reports/allure/allure-report",
        "logs",
        "screenshots/failed"
    ]

    for directory in reports_dirs:
        os.makedirs(directory, exist_ok=True)

    # Override HTML report path if specified in command line
    # This ensures HTML reports always go to reports folder
    html_path = config.getoption('--html', default=None)
    if html_path and not html_path.startswith('reports/'):
        # If HTML path doesn't start with reports/, prepend it
        new_html_path = f"reports/pytest/{os.path.basename(html_path)}"
        config.option.htmlpath = new_html_path
        # Update the actual option
        if hasattr(config.option, 'htmlpath'):
            config.option.htmlpath = new_html_path

    # Handle pytest-json-report plugin if installed
    # Ensure output.json goes to reports folder
    try:
        if hasattr(config.option, 'json_report_file'):
            if not config.option.json_report_file:
                config.option.json_report_file = 'reports/pytest/report.json'
            elif not config.option.json_report_file.startswith('reports/'):
                config.option.json_report_file = f"reports/pytest/{os.path.basename(config.option.json_report_file)}"
    except (AttributeError, TypeError):
        pass  # pytest-json-report not installed


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Create test report with screenshot on failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Test failed - take screenshot if UI test
        if hasattr(item, 'funcargs') and 'page' in item.funcargs:
            try:
                page = item.funcargs['page']
                screenshot_dir = "screenshots/failed"
                os.makedirs(screenshot_dir, exist_ok=True)

                screenshot_path = f"{screenshot_dir}/{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=screenshot_path)

                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")


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


def pytest_sessionfinish(session, exitstatus):
    """
    Hook that runs after all tests complete
    Clean up any misplaced report files
    """
    # List of files that should not be in root directory
    root_report_files = [
        'pytest-html-report.html',
        'output.json',
        'report.json',
        'test-results.json',
        'results.json'
    ]

    # Move any misplaced report files to reports folder
    for filename in root_report_files:
        if os.path.exists(filename):
            try:
                target_path = f"reports/pytest/{filename}"
                # Move the file
                if os.path.exists(target_path):
                    os.remove(target_path)
                os.rename(filename, target_path)
                print(f"\n✓ Moved {filename} to reports/pytest/")
            except Exception as e:
                print(f"\n⚠ Could not move {filename}: {e}")
