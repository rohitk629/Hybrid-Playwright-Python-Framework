"""
Common/Shared Step Definitions
These steps can be reused across multiple feature files
"""
from behave import given, when, then, step
from tests.ui.pages.login_page import LoginPage
from core.utils.browser_utility import BrowserUtility
from core.utils.config_reader import ConfigReader
import allure


# ============== AUTHENTICATION STEPS (Reusable) ==============

@given('I am logged in as a valid user')
@given('I am authenticated')
@given('I have successfully logged in')
def step_login_as_valid_user(context):
    """
    Complete login process - can be reused in any feature
    This step performs the full login workflow
    """
    # Initialize browser if not already done
    if not hasattr(context, 'browser_utility'):
        config = ConfigReader()
        context.browser_utility = BrowserUtility()
        context.browser_utility.initialize_browser()
        context.browser_utility.create_browser_context()
        context.browser_utility.create_page()

        context.login_page = LoginPage(context.browser_utility)
        login_url = config.get_property("app.base.url")
        context.login_page.navigate_to(login_url)

    # Perform login with default credentials
    context.login_page.enter_username("jcastro@gmail.com")
    context.login_page.enter_password("SBCqatester2024!")
    context.login_page.click_login_button()
    context.login_page.wait_for_page_load(timeout=100000)

    # Store login state in context
    context.is_logged_in = True
    context.logged_in_user = "jcastro@gmail.com"


@given('I am logged in with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):
    """
    Login with specific credentials - parametrized version
    """
    if not hasattr(context, 'browser_utility'):
        config = ConfigReader()
        context.browser_utility = BrowserUtility()
        context.browser_utility.initialize_browser()
        context.browser_utility.create_browser_context()
        context.browser_utility.create_page()

        context.login_page = LoginPage(context.browser_utility)
        login_url = config.get_property("app.base.url")
        context.login_page.navigate_to(login_url)

    context.login_page.enter_username(username)
    context.login_page.enter_password(password)
    context.login_page.click_login_button()
    context.login_page.wait_for_page_load(timeout=100000)

    context.is_logged_in = True
    context.logged_in_user = username


# ============== NAVIGATION STEPS (Reusable) ==============

@given('I navigate to "{page_name}" page')
@when('I navigate to "{page_name}" page')
def step_navigate_to_page(context, page_name):
    """Navigate to specific page after login"""
    page_urls = {
        'claims': '/claims',
        'submit claim': '/claims/submit',
        'dashboard': '/dashboard',
        'profile': '/profile',
        'home': '/home'
    }

    base_url = context.config_reader.get_property("app.base.url")
    page_url = base_url + page_urls.get(page_name.lower(), f'/{page_name.lower()}')

    context.browser_utility.page.goto(page_url)


# ============== VERIFICATION STEPS (Reusable) ==============

@then('I should be on the "{page_name}" page')
def step_verify_on_page(context, page_name):
    """Verify current page"""
    current_url = context.browser_utility.page.url
    assert page_name.lower() in current_url.lower(), \
        f"Expected to be on {page_name} page, but current URL is {current_url}"