"""
Login Test Cases - Fixed and Working
"""

import pytest
import allure
from core.base.base_test import BaseTest
from tests.ui.pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("Login")
class TestLogin(BaseTest):
    """Login test cases"""


    @pytest.fixture(autouse=True)
    def setup_login_test(self, setup_test):
        """Setup for login tests - depends on setup_test"""
        # Initialize instance variables here (replacing __init__)
        self.setup_browser()
        self.login_page = LoginPage(self.browser_utility)
        login_url = "https://qos214.sk.bluecross.ca/IdPLogin/LoginMemberWeb"
        self.login_page.navigate_to(login_url)
        yield
        # Additional teardown if needed

    @allure.title("Test successful login")
    @allure.description("Verify user can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_successful_login(self):
        """Test successful login"""
        self.log_test_step("Step 1: Enter valid username")
        self.login_page.enter_username("jcastro@gmail.com")

        self.log_test_step("Step 2: Enter valid password")
        self.login_page.enter_password("SBCqatester2024!")

        self.log_test_step("Step 3: Click login button")
        self.login_page.click_login_button()

        self.log_test_step("Step 4: Verify successful login")
        self.login_page.wait_for_page_load(timeout=100000)
        current_url = self.login_page.get_current_url()
        self.assert_in("Home", current_url,
                      "Should be redirected to home page")

    @allure.title("Test login with invalid credentials")
    @allure.description("Verify error message for invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        self.log_test_step("Step 1: Enter invalid username")
        self.login_page.enter_username("invalid_user")

        self.log_test_step("Step 2: Enter invalid password")
        self.login_page.enter_password("wrong_password")

        self.log_test_step("Step 3: Click login button")
        self.login_page.click_login_button()

        self.log_test_step("Step 4: Verify error message")
        error_visible = self.login_page.is_element_visible(
            self.login_page.ERROR_MESSAGE,
            timeout=5000
        )
        # self.assert_contains(error_visible, " Invalid username or password.")
        self.assert_contains(self.login_page.get_error_message(),
                             "Invalid username or password.")

