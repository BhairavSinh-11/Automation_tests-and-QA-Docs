# AgriBot Automated Test Suite

Week 3 deliverable — Junior QA Analyst (Job Simulation)
Automated Selenium test scripts for **AgriBot** (https://agribot.sbs),
a real, live smart-agriculture web application.

## Overview

This suite automates **4 critical user workflows** across **11 test
cases**, using **Python + Selenium WebDriver + pytest**, following the
Page Object Model (POM) design pattern.

| Workflow | Test file | Tests |
|---|---|---|
| Login (valid + invalid credentials) | `tests/test_login.py` | 2 |
| Registration (valid, mismatched passwords, duplicate username) | `tests/test_registration.py` | 3 |
| Navigation for a logged-in user | `tests/test_navigation_authenticated.py` | 3 |
| Access control for a logged-out user | `tests/test_navigation_unauthenticated.py` | 3 |

Unlike a simulated application, every locator in this suite was
**confirmed against AgriBot's real HTML** (fetched directly and, for
the login/register pages, cross-checked against the actual Jinja
templates) and every test has been **run and passed against the live
site**.

## Project Structure

```
agribot_automation/
├── README.md
├── requirements.txt
├── pytest.ini
├── page_objects/              # Page Object Model — one class per page
│   ├── base_page.py           # Shared helpers: find, click, type, wait,
│   │                          # is_visible, is_present
│   ├── login_page.py
│   ├── registration_page.py
│   └── home_page.py
└── tests/
    ├── conftest.py             # Fixtures: driver, logged_in_driver, base_url
    ├── test_login.py
    ├── test_registration.py
    ├── test_navigation_authenticated.py
    └── test_navigation_unauthenticated.py
```

## Setup

```bash
pip install -r requirements.txt
```

Selenium 4.6+ auto-manages the ChromeDriver binary — no separate
download needed.

## Configuration

Environment variables (all optional, sensible defaults are set):

```bash
export AGRIBOT_BASE_URL="https://agribot.sbs"     # default
export HEADLESS=false                              # watch the browser (default: true)
export AGRIBOT_TEST_USERNAME="nobi"                 # test account
export AGRIBOT_TEST_PASSWORD="123456"               # test account
```

## Running the Tests

```bash
# Everything
pytest

# One workflow at a time
pytest tests/test_login.py -v
pytest tests/test_registration.py -v
pytest tests/test_navigation_authenticated.py -v
pytest tests/test_navigation_unauthenticated.py -v
```

## Setup & Teardown

Handled in `tests/conftest.py` via two fixtures:

- **`driver`** — a fresh, logged-OUT Chrome session per test (setup),
  quit after the test completes regardless of pass/fail (teardown).
- **`logged_in_driver`** — builds on `driver`: logs in with the test
  account as part of its own setup, before the test body runs, so
  authenticated tests don't repeat login steps. If login itself fails,
  the fixture fails immediately with a clear message rather than a
  confusing failure deep inside a test.

## Confirmed Element Locators

These were read directly from AgriBot's real HTML/templates, not
guessed.

### Login (`/login`)

| Element | Locator | Notes |
|---|---|---|
| Username input | `#username` | Flask-WTF default id |
| Password input | `#password` | Flask-WTF default id |
| Sign In button | `.login-btn` | Has icon + separate text node — a plain XPath `contains(text(), 'Sign In')` fails because it only checks the first text node (blank whitespace before the icon). Class selector avoids this entirely. |
| Error message | `.error-message` | |
| Success message | `.success-message` | |
| Field-level error | `.field-error` | |
| Logged-in indicator | `a[href='/logout']` | Sits inside a profile dropdown that's CSS-hidden until `:hover` (`opacity-0 invisible`). Must check **presence**, not visibility — see `is_present()` below. |

### Registration (`/register`)

| Element | Locator | Notes |
|---|---|---|
| Username input | `#username` | |
| Email input | `#email` | |
| Password input | `#password` | |
| Confirm password input | `#confirmPassword` | Capital "P" — case-sensitive |
| Create Account button | `.register-btn` | Same icon+text issue as login button |
| Error / success / field-error | same classes as login page | Shared CSS across both forms |

There is **no separate "name" field** on registration — only username,
email, password, and confirm password.

### Navigation (site-wide)

Nav links use **relative** hrefs (e.g. `href="/agrimarket"`, not the
full URL) and appear multiple times in the DOM — in the visible desktop
nav, the mobile menu (hidden unless toggled), the footer, and some
feature cards. Locators are scoped to `nav a[href='...']` so they match
the first (visible, desktop) copy rather than a hidden duplicate.

**Every page now requires authentication** — a logged-out visitor
hitting `/crops`, `/agrimarket`, or `/AI` directly is redirected to
`/login`, which is exactly what `test_navigation_unauthenticated.py`
verifies.

## Key Fixes Applied During Development

| Problem | Root cause | Fix |
|---|---|---|
| Sign In / Create Account button never clickable | `contains(text(), '...')` XPath only checks the first text node of an element; the icon (`<i>`) creates a second text node, and the visible label was in that second node | Switched to CSS class selectors (`.login-btn`, `.register-btn`) |
| Nav links "not interactable" | Selectors used the full absolute URL (`a[href='https://agribot.sbs/agrimarket']`) but the real HTML uses relative hrefs (`href="/agrimarket"`) | Rewrote selectors to match relative hrefs, scoped to `nav` |
| Login check always failed even on successful login | `is_visible()` on the Logout link correctly reported "not visible", since that link is inside a `:hover`-only dropdown | Added `is_present()` to `base_page.py`, which checks existence regardless of CSS visibility, and used it for the login check |
| Tests hanging for 2+ minutes, then failing with a raw connection timeout | The homepage's autoplaying `<video>` can cause headless Chrome to become unresponsive | Added `--autoplay-policy=user-gesture-required` and `--mute-audio` Chrome options, plus `page_load_strategy = "eager"` and a 30s page load timeout |

## Error Handling in the Scripts

- `base_page.py` wraps Selenium's `find`/`click` calls in try/except,
  raising clear, descriptive errors (locator + current URL) instead of
  raw Selenium tracebacks.
- Negative-path tests assert on the *absence* of success states (e.g.
  "login should NOT succeed"), not just the presence of an error, so a
  silently-broken form can't accidentally pass.
- `logged_in_driver` asserts login succeeded as part of its own setup,
  so a broken login fails fast with a clear fixture-setup message
  rather than a confusing failure inside an unrelated test.

## Known Limitations / Notes for Future Maintenance

- `test_register_with_valid_new_details` creates a **real new account**
  on the live site each run (with a randomly generated unique
  username/email via `uuid`). This is expected and by design, but means
  the user database will accumulate test accounts (`qa_test_...`) over
  time.
- Success detection after registration checks for *either* a redirect
  away from `/register` *or* a visible success message, since the exact
  post-submit behavior wasn't independently confirmed from the template
  alone — tighten this assertion if the real behavior turns out to be
  more specific.
- If AgriBot's real HTML changes, only the locator constants in
  `page_objects/*.py` should need updating — test logic in `tests/*.py`
  should not need to change, by design of the Page Object Model.