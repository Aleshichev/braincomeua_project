"""
Module for collecting product data using Selenium.
"""

import random
from time import sleep
import logging
import re

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains


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
    return product_data
