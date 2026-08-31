"""
test_registration.py

Workflow: New User Registration.

Covers a valid registration (happy path), a mismatched-password
validation error, and an already-taken username (negative path, using
the known test account "nobi" from test_login.py).
"""

import uuid
from page_objects.registration_page import RegistrationPage

EXISTING_USERNAME = "nobi"  # confirmed to already exist (used in test_login.py)


def _unique_suffix():
    return uuid.uuid4().hex[:8]


def test_register_with_valid_new_details(driver, base_url):
    """A new user with a unique username/email should register successfully."""
    reg_page = RegistrationPage(driver, base_url)
    reg_page.load()

    suffix = _unique_suffix()
    reg_page.register(
        username=f"qa_test_{suffix}",
        email=f"qa.test.{suffix}@example.com",
        password="StrongPass123!",
    )

    redirected_away = not reg_page.is_still_on_register_page()
    success_message_shown = reg_page.is_present(reg_page.SUCCESS_MESSAGE, timeout=5)

    assert redirected_away or success_message_shown, (
        "Expected either a redirect away from /register or a visible "
        f"success message after valid registration. Still on: {driver.current_url}"
    )


def test_register_with_mismatched_passwords_shows_error(driver, base_url):
    """Password and Confirm Password not matching should be rejected."""
    reg_page = RegistrationPage(driver, base_url)
    reg_page.load()

    suffix = _unique_suffix()
    reg_page.register(
        username=f"qa_mismatch_{suffix}",
        email=f"qa.mismatch.{suffix}@example.com",
        password="StrongPass123!",
        confirm_password="ADifferentPass456!",
    )

    assert reg_page.is_still_on_register_page(), (
        "Expected to remain on /register after a password mismatch, "
        f"but landed on: {driver.current_url}"
    )
    assert reg_page.has_field_error() or reg_page.is_present(
        reg_page.ERROR_MESSAGE, timeout=5
    ), "Expected a visible validation error for mismatched passwords."


def test_register_with_existing_username_is_rejected(driver, base_url):
    """Registering with a username that's already taken should be blocked."""
    reg_page = RegistrationPage(driver, base_url)
    reg_page.load()

    suffix = _unique_suffix()
    reg_page.register(
        username=EXISTING_USERNAME,
        email=f"qa.duplicate.{suffix}@example.com",
        password="StrongPass123!",
    )

    assert reg_page.is_still_on_register_page(), (
        "Expected to remain on /register when the username is already taken, "
        f"but landed on: {driver.current_url}"
    )
    assert reg_page.has_field_error() or reg_page.is_present(
        reg_page.ERROR_MESSAGE, timeout=5
    ), "Expected a visible error for an already-taken username."