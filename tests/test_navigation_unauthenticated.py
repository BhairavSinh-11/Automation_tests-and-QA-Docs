"""
test_navigation_unauthenticated.py

Workflow: Access control for logged-out users.

Since every page now requires login, a logged-out visitor trying to
reach a protected page directly (e.g. /crops) should be redirected to
/login rather than seeing the protected content. This uses `driver`
(logged-out by default) and navigates directly via URL, since the goal
here is to check the ROUTE's own protection -- not the nav bar's click
behavior (which is covered separately once logged in).
"""

from page_objects.home_page import HomePage


def test_crops_page_redirects_to_login_when_logged_out(driver, base_url):
    """Visiting /crops without logging in should redirect to /login."""
    home_page = HomePage(driver, base_url)
    home_page.open("/crops")

    assert "/login" in driver.current_url, (
        f"Expected an unauthenticated visit to /crops to redirect to "
        f"/login, but landed on: {driver.current_url}"
    )


def test_marketplace_page_redirects_to_login_when_logged_out(driver, base_url):
    """Visiting /agrimarket without logging in should redirect to /login."""
    home_page = HomePage(driver, base_url)
    home_page.open("/agrimarket")

    assert "/login" in driver.current_url, (
        f"Expected an unauthenticated visit to /agrimarket to redirect to "
        f"/login, but landed on: {driver.current_url}"
    )


def test_ai_assistant_page_redirects_to_login_when_logged_out(driver, base_url):
    """Visiting /AI without logging in should redirect to /login."""
    home_page = HomePage(driver, base_url)
    home_page.open("/AI")

    assert "/login" in driver.current_url, (
        f"Expected an unauthenticated visit to /AI to redirect to "
        f"/login, but landed on: {driver.current_url}"
    )