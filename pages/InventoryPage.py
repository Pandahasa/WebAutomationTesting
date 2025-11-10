import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.BasePage import BasePage

log = logging.getLogger(__name__)

class InventoryPage(BasePage):
    """
    Page Object for the main Inventory/Product Page.
    """

    # --- Locators ---
    PAGE_TITLE = (By.CLASS_NAME, "title")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_FROM_CART_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        super().__init__(driver)
        log.info("InventoryPage initialized.")

    # --- Verification Methods ---

    def is_inventory_page_displayed(self):
        """
        Verifies the user is on the inventory page by checking for the title.
        """
        log.info("Checking if inventory page is displayed.")
        return self.is_element_visible(self.PAGE_TITLE)

    def get_page_title_text(self):
        return self.get_element_text(self.PAGE_TITLE)

    # --- High-Level Action Methods ---

    def add_backpack_to_cart(self):
        """
        Simulates the "search and select" by adding a specific item.
        """
        log.info("Adding 'Sauce Labs Backpack' to cart.")
        self.do_click(self.ADD_TO_CART_BACKPACK)
        # Verify the "Remove" button appears and cart badge updates
        self.wait.until(EC.visibility_of_element_located(self.REMOVE_FROM_CART_BACKPACK))
        self.wait.until(EC.visibility_of_element_located(self.SHOPPING_CART_BADGE))

    def go_to_cart(self):
        """
        Navigates to the shopping cart.
        """
        log.info("Navigating to shopping cart.")
        self.do_click(self.SHOPPING_CART_LINK)

        # --- Page Chaining ---
        # This action navigates to a new page.
        # We import the next Page Object and return an instance of it.
        # This makes test scripts fluent and logical.
        from pages.CheckoutFlowPage import CartPage
        return CartPage(self.driver)
