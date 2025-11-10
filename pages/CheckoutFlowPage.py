import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.BasePage import BasePage

log = logging.getLogger(__name__)

# --- 1. Cart Page ---

class CartPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        super().__init__(driver)
        log.info("CartPage initialized.")
        # Wait for cart page to be fully loaded
        self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))

    def is_item_in_cart(self, item_name):
        log.info(f"Verifying if '{item_name}' is in cart.")
        try:
            item_text = self.get_element_text(self.ITEM_NAME)
            return item_text == item_name
        except:
            return False

    def proceed_to_checkout(self):
        log.info("Proceeding to checkout step 1.")
        self.do_click(self.CHECKOUT_BUTTON)
        # Page Chaining: Return the next page in the flow
        return CheckoutInfoPage(self.driver)

# --- 2. Checkout Info Page ---

class CheckoutInfoPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def __init__(self, driver):
        super().__init__(driver)
        log.info("CheckoutInfoPage initialized.")
        # Wait for the first form field to be ready before proceeding
        # This helps with headless mode stability
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME_INPUT))

    def fill_shipping_info(self, first, last, code):
        log.info("Filling shipping information.")
        self.do_send_keys(self.FIRST_NAME_INPUT, first)
        self.do_send_keys(self.LAST_NAME_INPUT, last)
        self.do_send_keys(self.POSTAL_CODE_INPUT, code)
        self.do_click(self.CONTINUE_BUTTON)
        # Page Chaining: Return the next page in the flow
        return CheckoutOverviewPage(self.driver)

# --- 3. Checkout Overview Page ---

class CheckoutOverviewPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")

    def __init__(self, driver):
        super().__init__(driver)
        log.info("CheckoutOverviewPage initialized.")
        # Wait for overview page to be fully loaded
        self.wait.until(EC.presence_of_element_located(self.ITEM_TOTAL_LABEL))

    def get_item_total(self):
        return self.get_element_text(self.ITEM_TOTAL_LABEL)

    def finish_checkout(self):
        log.info("Finishing checkout.")
        self.do_click(self.FINISH_BUTTON)
        # Page Chaining: Return the final page in the flow
        return CheckoutCompletePage(self.driver)

# --- 4. Checkout Complete Page ---

class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")

    def __init__(self, driver):
        super().__init__(driver)
        log.info("CheckoutCompletePage initialized.")
        # Wait for complete page to be fully loaded
        self.wait.until(EC.presence_of_element_located(self.COMPLETE_HEADER))

    def get_complete_message(self):
        return self.get_element_text(self.COMPLETE_HEADER)

    def get_complete_text(self):
        return self.get_element_text(self.COMPLETE_TEXT)
