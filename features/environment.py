"""
Behave Environment Setup
Handles before/after hooks for feature/scenario/step execution
"""
from core.utils.browser_utility import BrowserUtility
from core.utils.api_client_utility import APIClientUtility
from core.utils.config_reader import ConfigReader
import logging
import allure
from datetime import datetime
import os


def before_all(context):
    """Before all features"""
    context.config_reader = ConfigReader()
    context.logger = logging.getLogger(__name__)
    context.logger.info("Starting test execution")

    # Create reports directory
    os.makedirs("reports/allure/allure-results", exist_ok=True)
    os.makedirs("reports/behave", exist_ok=True)


def before_feature(context, feature):
    """Before each feature"""
    context.logger.info(f"Starting feature: {feature.name}")


def before_scenario(context, scenario):
    """Before each scenario"""
    context.logger.info(f"Starting scenario: {scenario.name}")

    # Initialize browser for UI tests
    if 'ui' in scenario.tags:
        context.browser_utility = BrowserUtility()
        context.browser_utility.initialize_browser()
        context.browser_utility.create_browser_context()
        context.browser_utility.create_page()

    # Initialize API client for API tests
    if 'api' in scenario.tags:
        context.api_client = APIClientUtility()


def after_scenario(context, scenario):
    """After each scenario"""
    # Take screenshot on failure for UI tests
    if scenario.status == 'failed' and hasattr(context, 'browser_utility'):
        try:
            screenshot_dir = "screenshots/failed"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{screenshot_dir}/{scenario.name}_{timestamp}.png"

            context.browser_utility.take_screenshot(screenshot_path)

            # Attach to Allure
            allure.attach.file(
                screenshot_path,
                name=f"Failure - {scenario.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            context.logger.error(f"Failed to capture screenshot: {e}")

    # Close browser
    if hasattr(context, 'browser_utility'):
        try:
            context.browser_utility.close_browser()
        except Exception as e:
            context.logger.error(f"Error closing browser: {e}")


def after_feature(context, feature):
    """After each feature"""
    context.logger.info(f"Finished feature: {feature.name}")


def after_all(context):
    """After all features"""
    context.logger.info("Test execution completed")