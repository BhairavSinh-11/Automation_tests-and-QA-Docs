"""
registration_page.py

Page Object for the AgriBot Registration page (https://agribot.sbs/register).


"""

from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class RegistrationPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirmPassword")  # capital P, confirmed
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".register-btn")

    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    FIELD_ERROR = (By.CLASS_NAME, "field-error")

    def load(self):
        self.open("/register")
        return self

    def register(self, username, email, password, confirm_password=None):
        """
        Fill out and submit the registration form.

        `confirm_password` defaults to matching `password` -- pass a
        different value explicitly to test the mismatch/validation case.
        """
        if confirm_password is None:
            confirm_password = password

        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.click(self.SUBMIT_BUTTON)

    def is_still_on_register_page(self):
        """True if the form submission did NOT navigate away (e.g. a
        validation error kept us on /register)."""
        return "/register" in self.driver.current_url

    def has_field_error(self):
        return self.is_present(self.FIELD_ERROR, timeout=5)

    def get_field_error(self):
        """Return validation error text (e.g. weak password, duplicate email)."""
        return self.get_text(self.FIELD_ERROR)

    def has_flash_message(self):
        """True if either a success or error flash banner is showing."""
        return self.is_present(self.SUCCESS_MESSAGE, timeout=3) or self.is_present(
            self.ERROR_MESSAGE, timeout=3
        )