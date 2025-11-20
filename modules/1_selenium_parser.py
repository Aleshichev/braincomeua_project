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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
            EC.presence_of_element_located((By.XPATH, "//input[@class='quick-search-input']"))
        )
        search_input.clear()
        search_input.send_keys(product_name)
        sleep(random.uniform(1, 3))
        
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='search-button-first-form']")))
        search_button.click()
        sleep(random.uniform(1, 4))
        logging.info(f"Searched for product: {product_name}")
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error during product search: {e}")
        
    
    
if __name__ == "__main__":
    options = uc.ChromeOptions()
    
    # Add options to reduce detection
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=131)
        driver.maximize_window()
        get_url(driver, "https://brain.com.ua/")
        search_product(driver, "Apple iPhone 15 128GB Black")
        
        input("Press Enter to close the browser...")
        quit_driver(driver)
        
    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        logging.info("Try updating undetected-chromedriver: pip install undetected-chromedriver --upgrade")