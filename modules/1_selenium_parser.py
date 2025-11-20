"""
Parser brain.com.ua using Selenium.
Searches for Apple iPhone 15 128GB Black,
collects complete information about the product, and saves it to a PostgreSQL database.
"""

from load_django import *
from parser_app.models import Product

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random
from time import sleep
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     filename="parser.log",
#     encoding="utf-8",
# )

# ---------------- LOGGING CONFIG ----------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = logging.FileHandler("parser.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# ------------------------------------------------

def quit_driver(driver):
    """Quit the WebDriver instance."""
    if driver:
        try:
            driver.quit()
            logging.info("WebDriver has been closed successfully.")
        except Exception as e:
            logging.error(f"Error occurred while closing WebDriver: {e}")
    else:
        logging.warning("WebDriver instance is None; nothing to quit.")


def get_url(driver, url):
    """Navigate to the specified URL."""
    try:
        driver.get(url)
        logging.info(f"Navigated to URL: {url}")
    except Exception as e:
        logging.error(f"Failed to load URL {url}: {e}")
    sleep(random.uniform(2, 6))


def search_product(driver, product_name):
    wait = WebDriverWait(driver, 10)

    try:
        search_input = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'header-bottom-in')]//input[@class='quick-search-input']",
                )
            )
        )
        search_input.clear()
        search_input.send_keys(product_name)
        logging.info(f"Searching for product: {product_name}")
        sleep(random.uniform(1, 3))

        search_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@type='submit' and @class='qsr-submit' and @value='Знайти']",
                )
            )
        )
        search_button.click()
        sleep(random.uniform(1, 4))
        logging.info(f"Searched for product: {product_name}")
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error during product search: {e}")


if __name__ == "__main__":
    options = uc.ChromeOptions()
    
    # stealth mode
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    # anti-detect + shutdowns
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=Autoupgrade")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-background-networking")

    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": "uk-UA,uk,en-US,en",
        },
    )

    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=131)
        driver.maximize_window()
        get_url(driver, "https://brain.com.ua/")
        search_product(driver, "Apple iPhone 15 128GB Black")
        input("Press Enter to close the browser...")
        quit_driver(driver)

    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        quit_driver(driver)
