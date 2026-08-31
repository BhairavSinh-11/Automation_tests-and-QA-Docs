# AgriBot Automated Test Suite

Automated Selenium test scripts for **AgriBot** ([agribot.sbs](https://agribot.sbs)),
a smart agriculture platform. Built with **Python, Selenium WebDriver, and pytest**,
following the Page Object Model (POM) design pattern.

## What This Tests

| Workflow | What it checks | Test file |
|---|---|---|
| **Login** | Logging in with valid credentials succeeds; logging in with an incorrect password is correctly rejected with an error | `tests/test_login.py` |
| **Registration** | Creating a new account with valid, unique details succeeds; mismatched passwords are rejected; an already-taken username is rejected | `tests/test_registration.py` |
| **Navigation (logged in)** | A signed-in user can navigate to Crops, Marketplace, and AI Assistant via the nav bar | `tests/test_navigation_authenticated.py` |
| **Access control (logged out)** | A signed-out visitor trying to access protected pages directly is redirected to the login page | `tests/test_navigation_unauthenticated.py` |

**11 test cases** in total, run against the real, live application.

## Project Structure

```
agribot_automation/
├── README.md
├── requirements.txt
├── pytest.ini
├── .gitignore
├── page_objects/           # One class per page — holds locators and actions
│   ├── base_page.py        # Shared helpers used by every page object
│   ├── login_page.py
│   ├── registration_page.py
│   └── home_page.py
└── tests/
    ├── conftest.py          # Shared setup/teardown (browser fixtures)
    ├── test_login.py
    ├── test_registration.py
    ├── test_navigation_authenticated.py
    └── test_navigation_unauthenticated.py
```

Each page has its own file under `page_objects/`, keeping locators and
page actions separate from the test logic in `tests/`. This means UI
changes only require updating the relevant page object, not every test
that touches that page.

## Setup

```bash
pip install -r requirements.txt
```

Selenium 4.6+ manages the ChromeDriver binary automatically — no
separate download needed.

## Configuration

Optional environment variables (defaults shown):

```bash
export AGRIBOT_BASE_URL="https://agribot.sbs"
export HEADLESS=true            # set to false to watch the browser run
export AGRIBOT_TEST_USERNAME="nobi"
export AGRIBOT_TEST_PASSWORD="123456"
```

## Running the Tests

```bash
# Run everything
pytest

# Run one workflow
pytest tests/test_login.py -v

# Run everything and generate an HTML report
pytest --html=report.html --self-contained-html
```

The HTML report includes a screenshot automatically attached to any
test that fails, so failures are easy to diagnose at a glance.

## How It Works

- **Setup/teardown** — a fresh, isolated browser session is created for
  every test and closed afterward automatically, whether the test
  passes or fails.
- **Authenticated tests** use a `logged_in_driver` fixture that signs in
  with a test account before the test runs, so individual tests don't
  need to repeat login steps.
- **Assertions** confirm both the expected success cases and that
  invalid actions (wrong password, mismatched passwords, unauthorized
  access) are properly rejected.