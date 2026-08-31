"""
test_navigation_authenticated.py

Workflow: Top navigation for a LOGGED-IN user.

"""

from page_objects.home_page import HomePage


def test_navigate_to_crops_page_when_logged_in(logged_in_driver, base_url):
    """A logged-in user clicking the Crops nav link should reach the Crops page."""
    home_page = HomePage(logged_in_driver, base_url)
    home_page.load()

    home_page.go_to_crops()

    assert "/crops" in logged_in_driver.current_url, (
        f"Expected to land on the Crops page, got: {logged_in_driver.current_url}"
    )


def test_navigate_to_marketplace_page_when_logged_in(logged_in_driver, base_url):
    """A logged-in user clicking the Marketplace nav link should reach Agrimarket."""
    home_page = HomePage(logged_in_driver, base_url)
    home_page.load()

    home_page.go_to_marketplace()

    assert "/agrimarket" in logged_in_driver.current_url, (
        f"Expected to land on the Marketplace page, got: {logged_in_driver.current_url}"
    )


def test_navigate_to_ai_assistant_page_when_logged_in(logged_in_driver, base_url):
    """A logged-in user clicking the AI Assistant nav link should reach the AI page."""
    home_page = HomePage(logged_in_driver, base_url)
    home_page.load()

    home_page.go_to_ai_assistant()

    assert "/AI" in logged_in_driver.current_url, (
        f"Expected to land on the AI Assistant page, got: {logged_in_driver.current_url}"
    )