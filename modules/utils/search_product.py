"""
Module for searching and navigating to products using Selenium.
"""

import logging
import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
            logging.info(
                f"Clicked product button successfully on attempt {attempt + 1}"
            )
            return True
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Search error (attempt {attempt+1}): {e}")
            sleep(2)
    raise TimeoutException("Search product failed after 3 retries")


def go_to_first_product(driver):
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
