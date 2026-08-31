"""
conftest.py

Shared pytest fixtures for all AgriBot test files.

"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from page_objects.login_page import LoginPage


BASE_URL = os.getenv("AGRIBOT_BASE_URL", "https://agribot.sbs")

# Dedicated test account credentials -- override via env vars if needed.
TEST_USERNAME = os.getenv("AGRIBOT_TEST_USERNAME", "nobi")
TEST_PASSWORD = os.getenv("AGRIBOT_TEST_PASSWORD", "123456")


@pytest.fixture
def driver():
    """
    Yields a fresh, logged-OUT Selenium WebDriver instance for each test.

    Setup: launches a Chrome browser (headless by default).
    Teardown: quits the browser after the test completes, pass or fail.
    """
    options = Options()
    if os.getenv("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # The homepage has an autoplaying <video>. Headless Chrome can hang
    # indefinitely on autoplaying video -- forcing autoplay to require a
    # user gesture prevents that hang during automated runs.
    options.add_argument("--autoplay-policy=user-gesture-required")
    options.add_argument("--mute-audio")

    options.page_load_strategy = "eager"

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(2)
    chrome_driver.set_page_load_timeout(30)

    yield chrome_driver

    chrome_driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """
    Same as `driver`, but logs in with the test account BEFORE handing
    control to the test. Use this fixture (instead of `driver`) for any
    test that needs to be already authenticated -- e.g. testing that
    navigation works correctly once logged in.

    This fixture asserts login succeeded as part of its own setup: if
    login fails here, the test using it fails immediately with a clear
    "fixture setup failed" message, rather than a confusing failure
    later inside the actual test logic.
    """
    login_page = LoginPage(driver, BASE_URL)
    login_page.load()
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    assert login_page.is_login_successful(), (
        "logged_in_driver fixture setup failed: could not log in with "
        f"the configured test account ('{TEST_USERNAME}'). Check "
        "AGRIBOT_TEST_USERNAME / AGRIBOT_TEST_PASSWORD."
    )

    return driver


@pytest.fixture
def base_url():
    """Exposes the configured base URL to tests that need it directly."""
    return BASE_URL