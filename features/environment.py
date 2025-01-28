import os
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from icecream import ic

from utilities import ConfigReader


def get_config_value(section, key, env_var=None, default=None):
    """Helper function to get a config value from environment or configuration file."""
    # First, check if the environment variable exists
    if env_var:
        value = os.getenv(env_var, default)
        if value is not None:
            # ic(f"Found value from environment variable: {value}")
            return value  # Return the environment variable value if it exists

    # If the environment variable isn't set or not provided, check the configuration file
    value = ConfigReader.read_configuration(section, key)
    # if value is not None:
    #     ic(f"Read value from config file: {value}")
    # else:
    #     ic(f"Using default value: {default}")
    return value if value is not None else default  # Return from config file or default if not found


def setup_browser_options(browser, headless, maximized, fullscreen):
    """Returns the browser options based on the browser name."""
    options = None

    # ic(f"Setting up options for {browser} browser")

    if browser.lower() == "chrome":
        options = ChromeOptions()
        # Disable automation info bar by setting preferences
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-notifications")  # Disable Web Push Notification

    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        options.set_preference("dom.push.enabled", False)  # Disable web push notifications

    elif browser.lower() == "edge":
        options = EdgeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-notifications")  # Disable Web Push Notification

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Apply headless mode first
    if headless:
        # ic("Running headless browser")
        options.add_argument("--headless")

    # Apply window size arguments only if not headless
    if not headless:
        # if maximized and fullscreen:
        #     ic("Error: Both 'maximized' and 'fullscreen' cannot be enabled at the same time.")
        #     raise ValueError("Both 'maximized' and 'fullscreen' cannot be enabled at the same time.")
        if maximized:
            # ic("Maximizing browser window")
            options.add_argument("--start-maximized")
        if fullscreen:
            # ic("Starting browser in fullscreen mode")
            options.add_argument("--start-fullscreen")

    # Debug output for the options being applied
    # ic(f"Options created: {options.arguments}")
    return options


def initialize_webdriver(browser, options):
    """Initialize and return the WebDriver instance."""
    # ic(f"Initializing {browser} WebDriver with options: {options.arguments}")

    if browser.lower() == "chrome":
        return webdriver.Chrome(service=ChromeService(), options=options)
    elif browser.lower() == "firefox":
        return webdriver.Firefox(service=FirefoxService(), options=options)
    elif browser.lower() == "edge":
        return webdriver.Edge(service=EdgeService(), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")


def before_scenario(context, driver):
    """Setup the WebDriver before running the scenario."""
    # Retrieve browser settings from environment or configuration file
    browser = get_config_value("basic info", "browser", "browser")
    headless = get_config_value("basic info", "headless", "headless") == "true"
    maximized = get_config_value("basic info", "maximized", "maximized") == "true"
    fullscreen = get_config_value("basic info", "fullscreen", "fullscreen") == "true"
    base_url = get_config_value("basic info", "url", "url")

    # Set base_url in context
    context.base_url = base_url

    # Setup browser options
    options = setup_browser_options(browser, headless, maximized, fullscreen)

    # Initialize the WebDriver with the options
    # ic(f"Initializing WebDriver for {browser} browser with options: {options.arguments}")
    context.driver = initialize_webdriver(browser, options)

    # Open the base URL
    # context.driver.get(base_url)


def after_scenario(context, driver):
    """Quit the WebDriver after the scenario has run."""
    if context.driver:
        context.driver.quit()


def after_step(context, step):
    """Take a screenshot on step failure and attach it to Allure."""
    if step.status == "failed":
        scenario_title = context.scenario.name if hasattr(context, 'scenario') else 'Scenario_Failed'
        screenshot = context.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Scenario: {scenario_title} failed", attachment_type=AttachmentType.PNG)
