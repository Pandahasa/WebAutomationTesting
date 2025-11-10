import pytest
from pages import LoginPage, InventoryPage
from utils.DataUtils import get_csv_data
import logging

log = logging.getLogger(__name__)

BASE_URL = "https://www.saucedemo.com/"

# --- Data for parameterization ---
# We define our test cases as a list of tuples
# (username, password, expected_result, expected_message)
login_test_data = [
    ("standard_user", "secret_sauce", "success", "Products"),
    ("locked_out_user", "secret_sauce", "failure", "Sorry, this user has been locked out."),
    ("invalid_user", "invalid_pass", "failure", "Username and password do not match"),
]

@pytest.mark.login
@pytest.mark.parametrize(
    "username, password, expected_result, expected_message", login_test_data
)
def test_login_scenarios(driver, username, password, expected_result, expected_message):
    """
    Data-driven test for multiple login scenarios.
    This single function runs 3 times, once for each tuple in 'login_test_data'.
    """
    log.info(f"Testing login with user: {username}, expected: {expected_result}")

    # --- 1. ARRANGE
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page(BASE_URL)

    # --- 2. ACT
    login_page.login(username, password)

    # --- 3. ASSERT
    if expected_result == "success":
        inventory_page = InventoryPage(driver)
        # Use plain assert for powerful failure reporting
        assert inventory_page.is_inventory_page_displayed(), "Login succeeded but inventory page was not shown."
        page_title = inventory_page.get_page_title_text()
        # INTENTIONALLY BROKEN: Expecting wrong title to test CI/CD failure detection
        assert page_title == "WRONG_TITLE", f"Expected page title 'WRONG_TITLE', but got '{page_title}'."
        log.info(f"Login 'success' scenario PASSED for user: {username}")

    else:  # expected_result == "failure"
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Login failed as expected, but no error message was displayed."
        assert expected_message in error_msg, f"Expected error '{expected_message}', but got '{error_msg}'."
        log.info(f"Login 'failure' scenario PASSED (error: {error_msg}).")


# --- Data-driven test using external CSV file ---
login_test_data_from_file = get_csv_data("login_data.csv")

@pytest.mark.login
@pytest.mark.parametrize(
    "username, password, expected_result, expected_message", 
    login_test_data_from_file
)
def test_login_scenarios_from_file(driver, username, password, expected_result, expected_message):
    """
    Data-driven test that reads test cases from login_data.csv
    """
    log.info(f"Testing login (from file) with user: {username}, expected: {expected_result}")

    # --- 1. ARRANGE
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page(BASE_URL)

    # --- 2. ACT
    login_page.login(username, password)

    # --- 3. ASSERT
    if expected_result == "success":
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_inventory_page_displayed(), "Login succeeded but inventory page was not shown."
        page_title = inventory_page.get_page_title_text()
        assert page_title == expected_message, f"Expected page title '{expected_message}', but got '{page_title}'."
        log.info(f"Login 'success' scenario PASSED for user: {username}")

    else:  # expected_result == "failure"
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Login failed as expected, but no error message was displayed."
        assert expected_message in error_msg, f"Expected error '{expected_message}', but got '{error_msg}'."
        log.info(f"Login 'failure' scenario PASSED (error: {error_msg}).")
