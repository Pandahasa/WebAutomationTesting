import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Get a logger for this module, which will be configured by pytest.ini
log = logging.getLogger(__name__)

class BasePage:
    """
    Contains common methods and utilities that will be inherited by all
    Page Object classes.
    """

    def __init__(self, driver):
        """
        The constructor receives the 'driver' fixture from the test
        and initializes the WebDriverWait.
        """
        self.driver = driver
        # Set a standard 10-second explicit wait
        self.wait = WebDriverWait(self.driver, 10)

    def do_click(self, by_locator):
        """
        Waits for an element to be clickable, then clicks it.
        """
        log.info(f"Attempting to click element: {by_locator}")
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
            log.info(f"Successfully clicked element: {by_locator}")
        except TimeoutException:
            log.error(f"Timeout: Element not clickable: {by_locator}", exc_info=True)
            # Re-raise the exception to fail the test
            raise

    def do_send_keys(self, by_locator, text):
        """
        Waits for an element to be clickable (interactable), clears it, then sends keys.
        """
        log.info(f"Attempting to send keys '{text}' to element: {by_locator}")
        try:
            # Wait for element to be clickable (ensures it's interactable)
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.clear()
            element.send_keys(text)
            log.info(f"Successfully sent keys to element: {by_locator}")
        except TimeoutException:
            log.error(f"Timeout: Element not clickable/interactable: {by_locator}", exc_info=True)
            raise

    def get_element_text(self, by_locator):
        """
        Waits for an element to be visible, then returns its text.
        """
        log.info(f"Attempting to get text from element: {by_locator}")
        try:
            element = self.wait.until(EC.visibility_of_element_located(by_locator))
            text = element.text
            log.info(f"Found text '{text}' in element: {by_locator}")
            return text
        except TimeoutException:
            log.error(f"Timeout: Element not visible for text retrieval: {by_locator}", exc_info=True)
            raise

    def is_element_visible(self, by_locator, timeout=10):
        """
        Waits for an element to be visible, returns True/False.
        Allows for a custom timeout.
        """
        log.info(f"Checking visibility of element: {by_locator}")
        try:
            # Use a custom wait if provided, else default
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(by_locator))
            log.info(f"Element is visible: {by_locator}")
            return True
        except TimeoutException:
            log.warning(f"Element not visible after {timeout}s: {by_locator}")
            return False

    def get_page_title(self):
        """
        Returns the title of the current page.
        """
        log.info(f"Getting page title. Current URL: {self.driver.current_url}")
        title = self.driver.title
        log.info(f"Page title is: '{title}'")
        return title
