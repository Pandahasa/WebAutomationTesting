import logging
from selenium.webdriver.common.by import By
from utils.BasePage import BasePage

# Get a logger
log = logging.getLogger(__name__)

class LoginPage(BasePage):
    """
    Page Object for the Saucedemo Login Page.
    """

    # --- Locators ---
    # We define locators as class-level tuples
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        """
        Pass the driver to the BasePage's constructor
        """
        super().__init__(driver)
        log.info("LoginPage initialized.")

    # --- High-Level Action Methods ---

    def navigate_to_login_page(self, url):
        """
        Navigates the driver to the provided login URL.
        """
        log.info(f"Navigating to login page: {url}")
        self.driver.get(url)

    def login(self, username, password):
        """
        Performs a full login action by filling fields and clicking submit.
        This method uses the inherited 'do_send_keys' and 'do_click'.
        """
        log.info(f"Attempting login with user: {username}")
        try:
            self.do_send_keys(self.USERNAME_INPUT, username)
            self.do_send_keys(self.PASSWORD_INPUT, password)
            self.do_click(self.LOGIN_BUTTON)
            log.info("Login form submitted.")
        except Exception as e:
            log.error(f"Error during login: {e}", exc_info=True)
            raise

    def get_error_message(self):
        """
        Gets the text of the login error message.
        Returns None if the message is not visible.
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=3):
            return self.get_element_text(self.ERROR_MESSAGE)
        log.warning("Login error message element not found.")
        return None
