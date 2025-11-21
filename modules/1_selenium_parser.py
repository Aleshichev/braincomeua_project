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
import re
import pandas as pd

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains

# config imports
from config.driver_config import create_driver
from config.logger_config import setup_logging


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
            logging.info(
                f"Clicked product button successfully on attempt {attempt + 1}"
            )
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


def collect_product_data(driver):
    """Collect product data from the product page."""
    wait = WebDriverWait(driver, 10)
    logging.info("Start collecting product data...")
    product_data = {}

    # Product title
    try:
        title = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='main-right-block ']//h1[@class='desktop-only-title']",
                )
            )
        )
        product_data["title"] = title.text.strip()
        logging.info(f"Product title found: {product_data['title']}")
    except NoSuchElementException:
        product_data["title"] = None
        logging.error("Product title not found.")

    # Original price
    try:
        regular_price = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='br-pr-price main-price-block']//div[@class='price-wrapper']",
                )
            )
        )
        price = regular_price.text.strip().replace("\n", "")
        price = re.sub(r"[^\d.]", "", price)
        price = price.replace(",", ".")
        product_data["regular_price"] = float(price)
        logging.info(f"Price found: {product_data['regular_price']}")
    except NoSuchElementException:
        product_data["regular_price"] = None
        logging.error("Price not found.")

    # Sale price
    product_data["sale_price"] = None

    # All photos
    try:
        photo_elements = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='product-block-right']//div[@class='slick-track']//img",
                )
            )
        )
        product_data["photos"] = []
        for img in photo_elements:
            src = img.get_attribute("src")
            if src:
                product_data["photos"].append(src)
        logging.info(f"Added {len(product_data['photos'])} photos.")
    except NoSuchElementException:
        product_data["photos"] = []
        logging.info("No photos found.")

    # Review count
    try:
        review_count = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='title']//a[@class='forbid-click reviews-count']//span",
                )
            )
        )
        product_data["review_count"] = int(review_count.text.strip())
        logging.info(f"Review count found: {product_data['review_count']}")
    except NoSuchElementException:
        product_data["review_count"] = None
        logging.error("Review count not found.")

    # Code of the product
    try:
        code = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='title']//span[@class='br-pr-code-val']",
                )
            )
        )
        product_data["code"] = code.text.strip()
        logging.info(f"Product code found: {product_data['code']}")
    except NoSuchElementException:
        product_data["code"] = None
        logging.error("Product code not found.")

    # Scroll to all characteristics

    try:
        ActionChains(driver).scroll_by_amount(0, 700).perform()
        sleep(random.uniform(2, 5))
        logging.info("Scrolled to amount 700")
    except:
        ActionChains(driver).scroll_by_amount(0, 1000).perform()
        sleep(random.uniform(1, 4))

    # Click to show all characteristics
    try:
        all_characteristics = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@id='br-characteristics']//button[@class='br-prs-button']",
                )
            )
        )
        all_characteristics.click()
        logging.info("Click to all characteristics")
        sleep(random.uniform(2, 5))
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Navigation error to all characteristics: {e}")

    # Scroll
    try:
        ActionChains(driver).scroll_by_amount(0, 1000).perform()
        sleep(random.uniform(2, 5))
        logging.info("Scrolled to amount 1000")
    except:
        ActionChains(driver).scroll_by_amount(0, 1500).perform()
        sleep(random.uniform(1, 4))

    # Extract color, memory, manufacturer from title
    parts = title.text.strip().split()
    product_data["color"] = parts[-2]
    product_data["memory"] = parts[-3]
    product_data["manufacturer"] = parts[2]

    logging.info(
        f"Extracted color: {product_data['color']}, memory: {product_data['memory']}, manufacturer: {product_data['manufacturer']}"
    )

    # Collect specifications
    try:
        specifications = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='br-wrap-block br-elem-block']",
                )
            )
        )
        specs_dict = {}
        for spec in specifications:
            try:
                details = spec.find_elements(
                    By.XPATH, ".//div[@class='br-pr-chr-item']"
                )
                for detail in details:
                    try:
                        title_section = detail.find_element(
                            By.XPATH, ".//h3"
                        ).text.strip()
                        specs_dict[title_section] = {}
                        rows = detail.find_elements(By.XPATH, ".//div")
                        for row in rows:
                            try:
                                spans = row.find_elements(By.XPATH, ".//span")
                                if len(spans) >= 2:
                                    key = spans[0].text.strip()
                                values = []
                                for span in spans[1:]:
                                    # Check for links inside the span
                                    links = span.find_elements(By.XPATH, ".//a")
                                    if links:
                                        values.extend(
                                            [link.text.strip() for link in links]
                                        )
                                    else:
                                        text = span.text.strip()
                                        if text:
                                            values.append(text)

                                # Set value to dictionary
                                value = ", ".join(values) if values else None
                                if key:
                                    specs_dict[title_section][key] = value
                            except NoSuchElementException:
                                logging.warning(
                                    "Section title (h3) not found in detail block"
                                )
                                continue
                        logging.info(
                            f"Collected {len(specs_dict)} specification sections."
                        )
                    except NoSuchElementException:
                        logging.error("Specification details not found.")
                        continue
                logging.info(f"Collected  details for specification.")
            except NoSuchElementException:
                specs_dict["details"] = {}
                logging.error("Specification details not found.")

        product_data["specifications"] = specs_dict
        logging.info(f"Collected {len(specs_dict)} specifications.")

        # for spec in specifications:
        #     try:
        #         key = spec.find_element(By.XPATH, ".//td[1]").text.strip()
        #         value = spec.find_element(By.XPATH, ".//td[2]").text.strip()
        #         specs_dict[key] = value
        #     except NoSuchElementException:
        #         continue
        # product_data["specifications"] = specs_dict
        # logging.info(f"Collected {len(specs_dict)} specifications.")
    except NoSuchElementException:
        product_data["specifications"] = {}
        logging.error("Specifications not found.")

    # get manufacturer, memory, color, screen diagonal, screen resolution from specifications
    manufacturer = product_data["specifications"]["Інші"]["Виробник"]
    product_data["manufacturer"] = manufacturer

    memory = product_data["specifications"]["Функції пам'яті"]["Вбудована пам'ять"]
    product_data["memory"] = memory

    color = product_data["specifications"]["Фізичні характеристики"]["Колір"]
    product_data["color"] = color

    screen_diagonal = product_data["specifications"]["Дисплей"]["Діагональ екрану"]
    product_data["screen_diagonal"] = screen_diagonal

    screen_resolution = product_data["specifications"]["Дисплей"][
        "Роздільна здатність екрану"
    ]
    product_data["screen_resolution"] = screen_resolution

    print(product_data)
    # Save to database
    try:
        product = Product.objects.create(**product_data)
        logging.info(f"Product saved to database with ID: {product.id}")
    except Exception as e:
        logging.error(f"Failed to save product to database: {e}")


# Export from db to csv
def export_to_csv():
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
        # get_url(driver, "https://brain.com.ua/")
        # search_product(driver, "Apple iPhone 15 128GB Black")
        # got_to_first_product(driver)
        # collect_product_data(driver)
        export_to_csv()

        # Wait for product listings to load
        input("Press Enter to close the browser...")
        quit_driver(driver)

    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        quit_driver(driver)
