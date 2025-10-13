"""
Login Step Definitions for BDD
"""
from behave import given, when, then
from tests.ui.pages.login_page import LoginPage
from core.utils.browser_utility import BrowserUtility
from core.utils.config_reader import ConfigReader



@given('I am on the login page')
def step_impl(context):
    """Navigate to login page"""
    config = ConfigReader()
    context.browser_utility = BrowserUtility()
    context.browser_utility.initialize_browser()
    context.browser_utility.create_browser_context()
    context.browser_utility.create_page()

    context.login_page = LoginPage(context.browser_utility)
    login_url = config.get_property("app.base.url") + "/login"
    context.login_page.navigate_to(login_url)

@when('I enter username "{username}"')
def step_impl(context, username):
    """Enter username"""
    context.login_page.enter_username(username)

@when('I enter password "{password}"')
def step_impl(context, password):
    """Enter password"""
    context.login_page.enter_password(password)

@when('I click the login button')
def step_impl(context):
    """Click login button"""
    context.login_page.click_login_button()

@then('I should be logged in successfully')
def step_impl(context):
    """Verify user is logged in"""
    assert context.login_page.is_logged_in(), "User should be logged in"


@then('I should see the dashboard')
def step_impl(context):
    """Verify dashboard is displayed"""
    current_url = context.login_page.get_current_url()
    assert "/dashboard" in current_url, "Should be redirected to dashboard"

@then('I should see an error message "{message}"')
def step_impl(context, message):
    """Verify error message"""
    error_msg = context.login_page.get_error_message()
    assert message in error_msg, f"Expected '{message}' in error message, got '{error_msg}'"

@then('I should remain on the login page')
def step_impl(context):
    """Verify still on login page"""
    current_url = context.login_page.get_current_url()
    assert "/login" in current_url, "Should remain on login page"

@then('I should see "{result}"')
def step_impl(context, result):
    pass
