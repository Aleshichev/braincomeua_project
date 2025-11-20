"""
Parser brain.com.ua using Selenium.
Searches for Apple iPhone 15 128GB Black,
collects complete information about the product, and saves it to a PostgreSQL database.
"""

from load_django import *
from parser_app.models import Product

import random
from time import sleep
import logging

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config.driver_config import create_driver

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
    "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
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
    for attempt in range(3):
        try:
            driver.get(url)
            logging.info(f"Navigated to URL after {attempt + 1} attempts: {url}")
            sleep(random.uniform(2, 6))
            return True
        except Exception as e:
            logging.error(f"Failed to load URL {url} after {attempt + 1} attempts: {e}")
            sleep(random.uniform(1, 4))
    raise Exception(f"Not found {url} after 3 attempts")


def search_product(driver, product_name):
    """Search write and click on the product."""
    wait = WebDriverWait(driver, 10)

    for attempt in range(3):
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
            logging.info(
                f"Searching for product: {product_name}, attempt {attempt + 1}"
            )
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
            logging.info(f"Search clicked successfully on attempt {attempt + 1}")
            return True
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Search error (attempt {attempt+1}): {e}")
            sleep(2)
    raise TimeoutException("Search product failed after 3 retries")


def got_to_first_product(driver):
    """Go to first product from the search results."""
    wait = WebDriverWait(driver, 10)

    for attempt in range(3):
        try:
            first_product = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '(//div[@data-stock="1"])[1]//a',
                    )
                )
            )
            first_product.click()
            sleep(random.uniform(2, 5))
            logging.info(f"Navigated to first product page on attempt {attempt + 1}")
            return True
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(
                f"Navigation error to first product (attempt {attempt+1}): {e}"
            )
            sleep(2)
    raise TimeoutException("Navigation to first product failed after 3 retries")


if __name__ == "__main__":
    logging.info("Starting the parser...")
    try:
        driver = create_driver(chrome_version=131)
        get_url(driver, "https://brain.com.ua/")
        search_product(driver, "Apple iPhone 15 128GB Black")
        got_to_first_product(driver)

        # Wait for product listings to load
        input("Press Enter to close the browser...")
        quit_driver(driver)

    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        quit_driver(driver)
