"""
Login Page Object Model
"""
from core.base.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Login page object"""

    # Locators
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    LOGOUT_BUTTON = "button#logout"

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str):
        """Enter username"""
        self.enter_text(self.USERNAME_INPUT, username)

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
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Check if user is logged in")
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_element_visible(self.LOGOUT_BUTTON)