import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest_html
from datetime import datetime
import logging

# Get a logger for this module
log = logging.getLogger(__name__)

# Hook to add custom command-line options
def pytest_addoption(parser):
    """
    Adds custom command-line options to pytest.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Specify the browser to run tests on: 'chrome' or 'firefox'. Default: 'chrome'"
    )
    parser.addoption(
        "--headless",
        action="store_true",  # This makes it a flag, e.g., 'pytest --headless'
        default=False,
        help="Run browser in headless mode (no GUI)"
    )


# --- The central driver fixture ---
@pytest.fixture(scope="function")
def driver(request):
    """
    A pytest fixture that manages the Selenium WebDriver lifecycle for a test.
    """
    # --- 1. Get browser and headless options from command-line
    browser_name = request.config.getoption("--browser").lower()
    is_headless = request.config.getoption("--headless")

    driver_instance = None

    # --- 2. Initialize the browser specified
    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        if is_headless:
            chrome_options.add_argument("--headless")
            # Arguments required for running headless in CI/Docker environments
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

        # Use webdriver-manager to automatically handle the driver binary
        service = ChromeService(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        if is_headless:
            firefox_options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=firefox_options)

    else:
        # If an unsupported browser is specified, raise an error
        raise pytest.UsageError(f"--browser='{browser_name}' is not supported. Use 'chrome' or 'firefox'.")

    # --- 3. Configure common driver properties
    driver_instance.implicitly_wait(10)  # Implicitly wait for elements
    driver_instance.maximize_window()

    log.info(f"WebDriver initialized: {browser_name}, headless={is_headless}")

    # --- 4. Yield the driver to the test function
    # The 'yield' keyword passes the driver_instance to the test
    yield driver_instance

    # --- 5. Teardown (runs after the test completes)
    # This 'quit()' is guaranteed to run, even if the test fails
    log.info("WebDriver teardown: Closing browser")
    driver_instance.quit()


# --- Hook for adding screenshots to HTML report on failure ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook runs for every test. It captures the test outcome
    and adds screenshots to the report if the test fails.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Clear 'extras' on report setup
    if report.when == "setup":
        report.extras = []

    # We only want to add extras when the test 'call' has failed
    if report.when == "call" and report.failed:
        log.error(f"Test '{item.name}' FAILED. Capturing screenshot.")

        # 'item' is the test function. We can access its fixtures.
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]

            try:
                # --- Create reports/screenshots directory if it doesn't exist
                screenshot_dir = os.path.join("reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)

                # --- Generate a unique screenshot name
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                test_name = item.name.replace('[', '-').replace(']', '')  # Clean parameterized names
                screenshot_file = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")

                # --- Save the screenshot
                driver.save_screenshot(screenshot_file)
                log.info(f"Screenshot saved: {screenshot_file}")

                # --- Add screenshot to the HTML report ---
                # Create relative path for the HTML report
                relative_path = os.path.join("screenshots", f"{test_name}_{timestamp}.png")

                # Create an <img> tag
                html = f'<div><img src="{relative_path}" alt="Screenshot" style="width:600px;" onclick="window.open(this.src)" align="right"/></div>'

                report.extras.append(pytest_html.extras.html(html))

            except Exception as e:
                log.warning(f"Could not take screenshot for failed test {item.name}: {e}")
