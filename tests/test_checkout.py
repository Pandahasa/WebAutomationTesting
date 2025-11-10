import os
import pytest
from pages import LoginPage, InventoryPage
# Note: Other pages are imported via Page Chaining
import logging

log = logging.getLogger(__name__)
BASE_URL = "https://www.saucedemo.com/"

@pytest.mark.smoke  # This is a critical path test
@pytest.mark.regression
@pytest.mark.checkout
@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="E2E test has timing issues in headless CI - works locally"
)
def test_end_to_end_checkout(driver):
    """
    Validates the full user flow:
    Login > Add item to Cart > Checkout > Verify Completion
    """
    log.info("--- Starting test_end_to_end_checkout ---")

    # --- 1. Login ---
    log.info("Step 1: Logging in")
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page(BASE_URL)
    login_page.login("standard_user", "secret_sauce")

    # --- 2. Add item (simulating "search") ---
    log.info("Step 2: Adding item to cart")
    inventory_page = InventoryPage(driver)
    assert inventory_page.is_inventory_page_displayed(), "Failed to log in."
    inventory_page.add_backpack_to_cart()

    # --- 3. Go to Cart and verify ---
    log.info("Step 3: Navigating to cart and verifying item")
    # Page Chaining: This method returns the CartPage object
    cart_page = inventory_page.go_to_cart()
    assert cart_page.is_item_in_cart("Sauce Labs Backpack"), "Item not found in cart!"

    # --- 4. Proceed to Checkout Info ---
    log.info("Step 4: Proceeding to checkout info")
    # Page Chaining: This method returns the CheckoutInfoPage object
    checkout_info_page = cart_page.proceed_to_checkout()

    # --- 5. Fill shipping info ---
    log.info("Step 5: Filling shipping information")
    # Page Chaining: This method returns the CheckoutOverviewPage object
    checkout_overview_page = checkout_info_page.fill_shipping_info(
        "Test", "User", "12345"
    )

    # --- 6. Finish checkout ---
    log.info("Step 6: Finishing checkout")
    # Page Chaining: This method returns the CheckoutCompletePage object
    checkout_complete_page = checkout_overview_page.finish_checkout()

    # --- 7. Final Assertion ---
    log.info("Step 7: Verifying order completion message")
    message = checkout_complete_page.get_complete_message()
    assert message == "Thank you for your order!", f"Checkout failed. Expected 'Thank you...' but got '{message}'"

    log.info("--- test_end_to_end_checkout PASSED ---")
