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
import pandas as pd

# import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC

# config imports
from config.driver_config import create_driver
from config.logger_config import setup_logging

# utils imports
from utils.collect_products import collect_product_data
from utils.search_product import search_product, go_to_first_product


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


def save_to_database(product_data):
    """Save product data to the database."""
    try:
        product = Product.objects.create(**product_data)
        logging.info(f"Product saved to database with ID: {product.id}")
    except Exception as e:
        logging.error(f"Failed to save product to database: {e}")


def export_to_csv():
    """Export all products from the database to a CSV file."""
    try:
        products = Product.objects.all()
        df = pd.DataFrame(list(products.values()))
        df.to_csv("results/products.csv", index=False)
        logging.info("Products exported to CSV successfully.")
    except Exception as e:
        logging.error(f"Failed to export products to CSV: {e}")


if __name__ == "__main__":
    logger = setup_logging()

    logging.info("Starting the parser...")
    try:
        driver = create_driver(chrome_version=131)
        get_url(driver, "https://brain.com.ua/")
        search_product(driver, "Apple iPhone 15 128GB Black")
        go_to_first_product(driver)
        product_data = collect_product_data(driver)
        save_to_database(product_data)
        export_to_csv()

        # Wait for product listings to load
        input("Press Enter to close the browser...")
        quit_driver(driver)

    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        quit_driver(driver)
