"""
home_page.py

Page Object for the AgriBot Home page and its top navigation
(https://agribot.sbs/).

"""

from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class HomePage(BasePage):
    # ---- Confirmed navigation paths (from the real site's HTML) ----
    NAV_HOME = (By.CSS_SELECTOR, "nav a[href='/']")
    NAV_CROPS = (By.CSS_SELECTOR, "nav a[href='/crops']")
    NAV_MARKETPLACE = (By.CSS_SELECTOR, "nav a[href='/agrimarket']")
    NAV_AI_ASSISTANT = (By.CSS_SELECTOR, "nav a[href='/AI']")
    NAV_ANNADATA = (By.CSS_SELECTOR, "nav a[href='/annadata']")
    NAV_ABOUT = (By.CSS_SELECTOR, "nav a[href='/about']")
    NAV_LOGIN = (By.CSS_SELECTOR, "nav a[href='/login']")
    NAV_REGISTER = (By.CSS_SELECTOR, "nav a[href='/register']")
    GET_STARTED_BUTTON = (By.XPATH, "//a[contains(text(), 'Get Started')]")
    ASK_AGRIBOT_BUTTON = (By.XPATH, "//a[contains(text(), 'Ask AgriBot')]")

    # ---- TODO: replace with real locators found via Inspect Element ----
    # Elements specific to the Crops page (e.g. a crop search/filter input)
    CROP_SEARCH_INPUT = (By.ID, "TODO-crop-search-input-id")
    CROP_RESULT_CARD = (By.CLASS_NAME, "TODO-crop-result-card-class")

    def load(self):
        self.open("/")
        return self

    def go_to_crops(self):
        self.click(self.NAV_CROPS)

    def go_to_marketplace(self):
        self.click(self.NAV_MARKETPLACE)

    def go_to_ai_assistant(self):
        self.click(self.NAV_AI_ASSISTANT)

    def go_to_annadata(self):
        self.click(self.NAV_ANNADATA)

    def go_to_about(self):
        self.click(self.NAV_ABOUT)

    def click_get_started(self):
        """'Get Started' on the homepage links to /login on the real site."""
        self.click(self.GET_STARTED_BUTTON)