"""
test_login.py

Workflow: User Login.
.
"""

from page_objects.login_page import LoginPage

VALID_USERNAME = "Nobi"  
VALID_PASSWORD = "123456"
WRONG_PASS = "123123123"


def test_login_with_valid_credentials(driver, base_url):
    """A registered user should be able to log in successfully."""
    login_page = LoginPage(driver, base_url)
    login_page.load()

    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    assert login_page.is_login_successful(), (
        "Expected a logged-in indicator (Logout link) to appear after login, "
        "but it was not found -- login may have failed, or "
        "USER_INPUT/PASSWORD_INPUT locators still need confirming."
    )


def test_login_with_incorrect_password_shows_error(driver, base_url):
    """Logging in with a valid username but wrong password should show an error."""
    login_page = LoginPage(driver, base_url)
    login_page.load()

    login_page.login(VALID_USERNAME, WRONG_PASS)

    assert not login_page.is_login_successful(), (
        "Login unexpectedly succeeded with an incorrect password."
    )

    error_text = login_page.get_error_message()
    assert error_text.strip() != "", "Error message element was present but empty."