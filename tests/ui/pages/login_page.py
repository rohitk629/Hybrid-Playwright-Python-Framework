"""
Login Page Object Model
"""
from core.base.base_page import BasePage
from core.base.base_test import BaseTest
import allure


class LoginPage(BasePage):
    """Login page object for SauceDemo"""

    # Locators for SauceDemo
    USERNAME_INPUT = "#Input_Email"
    PASSWORD_INPUT = "#Input_Password"
    LOGIN_BUTTON = "//*[@id='LoginForm']/div[3]/div[2]/button/span"
    ERROR_MESSAGE = "//div[@class='feedback-message-text']"
    INVENTORY_CONTAINER = "#inventory_container"

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        """Enter username"""
        self.enter_text(self.USERNAME_INPUT, username, True,  15000)

    @allure.step("Enter password")
    def enter_password(self, password: str):
        """Enter password"""
        self.enter_text(self.PASSWORD_INPUT, password)

    @allure.step("Click login button")
    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Login with credentials")
    def login(self, username: str, password: str):
        """Perform login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    @allure.step("Check if user is logged in")
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_element_visible(self.INVENTORY_CONTAINER, timeout=5000)

