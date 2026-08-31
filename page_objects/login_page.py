"""
login_page.py

Page Object for the AgriBot Login page (https://agribot.sbs/login).

"""

from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class LoginPage(BasePage):
    USER_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn")

    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    FIELD_ERROR = (By.CLASS_NAME, "field-error")

    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/forgotpass']")
    CREATE_ACCOUNT_LINK = (By.PARTIAL_LINK_TEXT, "Create an account")
    GOOGLE_LOGIN_LINK = (By.CSS_SELECTOR, ".google-btn")

    # Hidden until :hover on the profile dropdown -- check PRESENCE, not visibility
    LOGGED_IN_INDICATOR = (By.CSS_SELECTOR, "a[href='/logout']")

    def load(self):
        self.open("/login")
        return self

    def login(self, username, password):
        """Fill the login form and submit it."""
        self.type_text(self.USER_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Return the error text shown after a failed login attempt."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_successful(self):
        """
        Confirms login worked by checking the Logout link EXISTS in the
        navbar -- using is_present() rather than is_visible(), since this
        link is only shown on :hover and would otherwise never register
        as visible right after login.
        """
        return self.is_present(self.LOGGED_IN_INDICATOR, timeout=8)