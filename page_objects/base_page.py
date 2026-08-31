"""
base_page.py

Base Page Object class. All page-specific classes (LoginPage, HomePage,
etc.) inherit from this so common Selenium actions (find, click, type,
wait) are written once and reused everywhere -- the Page Object Model
(POM) pattern.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

DEFAULT_TIMEOUT = 10  # seconds to wait for an element before failing


class BasePage:
    """Common functionality shared by every page object."""

    def __init__(self, driver, base_url="https://agribot.sbs"):
        self.driver = driver
        self.base_url = base_url

    def open(self, path=""):
        """Navigate to a given path relative to the base URL."""
        self.driver.get(f"{self.base_url}{path}")

    def _wait(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout)

    def find(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for and return a single element, raising a clear error on failure."""
        try:
            return self._wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException as exc:
            raise NoSuchElementException(
                f"Element {locator} was not found within {timeout}s on {self.driver.current_url}"
            ) from exc

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait until an element is clickable, then click it, with error handling."""
        try:
            element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
            element.click()
        except (TimeoutException, ElementNotInteractableException) as exc:
            raise ElementNotInteractableException(
                f"Could not click element {locator} on {self.driver.current_url}"
            ) from exc

    def type_text(self, locator, text, clear_first=True):
        """Locate a field and type into it, optionally clearing existing content first."""
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        """Return the visible text of an element."""
        return self.find(locator, timeout).text

    def is_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Return True/False instead of raising, useful for optional/error elements."""
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_present(self, locator, timeout=DEFAULT_TIMEOUT):
        """
        Return True/False based on whether an element EXISTS in the page,
        regardless of CSS visibility. Use this instead of is_visible() for
        elements that are intentionally hidden until a hover/click (e.g. a
        dropdown menu item with opacity-0 by default) -- is_visible() would
        correctly report these as not visible even when login/logic worked
        fine, since the element is only ever shown on :hover.
        """
        try:
            self._wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False