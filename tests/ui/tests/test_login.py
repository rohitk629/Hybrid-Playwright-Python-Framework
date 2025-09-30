"""
Login Test Cases
"""
import pytest
import allure
from core.base.base_test import BaseTest
from tests.ui.pages.login_page import LoginPage
from core.constants.test_constants import TestConstants
from core.dataproviders.excel_data_provider import ExcelDataProvider


@allure.feature("Authentication")
@allure.story("Login")
class TestLogin(BaseTest):
    """Login test cases"""


    def setup_login_test(self):
        """Setup for login tests"""
        self.setup_browser()
        self.login_page = LoginPage(self.browser_utility)
        self.login_page.navigate_to(self.config.get_property("app.base.url") + "/login")

    @allure.title("Test successful login")
    @allure.description("Verify user can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_successful_login(self):
        """Test successful login"""
        self.log_test_step("Step 1: Enter valid username")
        self.login_page.enter_username(TestConstants.VALID_USERNAME)

        self.log_test_step("Step 2: Enter valid password")
        self.login_page.enter_password(TestConstants.VALID_PASSWORD)

        self.log_test_step("Step 3: Click login button")
        self.login_page.click_login_button()

        self.log_test_step("Step 4: Verify user is logged in")
        self.assert_true(self.login_page.is_logged_in(), "User should be logged in")

    @allure.title("Test login with invalid credentials")
    @allure.description("Verify error message is displayed for invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        self.log_test_step("Step 1: Enter invalid username")
        self.login_page.enter_username(TestConstants.INVALID_USERNAME)

        self.log_test_step("Step 2: Enter invalid password")
        self.login_page.enter_password(TestConstants.INVALID_PASSWORD)

        self.log_test_step("Step 3: Click login button")
        self.login_page.click_login_button()

        self.log_test_step("Step 4: Verify error message is displayed")
        error_message = self.login_page.get_error_message()
        self.assert_equals(error_message, TestConstants.LOGIN_ERROR_MESSAGE,
                           "Error message should be displayed")

    @allure.title("Test login with data from Excel")
    @allure.description("Test login with multiple data sets from Excel")
    @pytest.mark.parametrize("username,password,expected_result",
                             ExcelDataProvider().load_data("test_data/excel/login_data.xlsx"))
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_with_excel_data(self, username, password, expected_result):
        """Test login with data from Excel"""
        self.log_test_step(f"Testing login with username: {username}")
        self.login_page.login(username, password)

        if expected_result == "success":
            self.assert_true(self.login_page.is_logged_in(),
                             f"Login should succeed for {username}")
        else:
            error_message = self.login_page.get_error_message()
            self.assert_true(len(error_message) > 0,
                             f"Error message should be displayed for {username}")