"""
Parser brain.com.ua using Selenium.
Searches for Apple iPhone 15 128GB Black,
collects complete information about the product, and saves it to a PostgreSQL database.
"""

import logging

# config imports
from config.driver_config import create_driver
from config.logger_config import setup_logging
from load_django import *
# import undetected_chromedriver as uc
from utils.get_main_url import get_url
from utils.search_product import go_to_first_product, search_product
from utils.storage import export_to_csv, save_to_database

# utils imports
from utils.collect_data import collect_product_data


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


def main():
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
        quit_driver(driver)

    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        quit_driver(driver)

    logging.info("Parser completed.")


if __name__ == "__main__":
    main()
