"""
Module for collecting product data using Selenium.
"""

import random
from time import sleep
import logging
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains


def get_product_title(wait):
    """Extract product title."""
    try:
        title = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='main-right-block ']//h1[@class='desktop-only-title']",
                )
            )
        )
        title_text = title.text.strip()
        logging.info(f"Product title found: {title_text}")
        return title_text
    except NoSuchElementException:
        logging.error("Product title not found.")
        return None


def get_product_price(wait):
    """Extract product regular price."""
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
        price_float = float(price)
        logging.info(f"Price found: {price_float}")
        return price_float
    except NoSuchElementException:
        logging.error("Price not found.")
        return None


def get_product_photos(wait):
    """Extract all product photos."""
    try:
        photo_elements = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='product-block-right']//div[@class='slick-track']//img",
                )
            )
        )
        photos = []
        for img in photo_elements:
            src = img.get_attribute("src")
            if src:
                photos.append(src)
        logging.info(f"Added {len(photos)} photos.")
        return photos
    except NoSuchElementException:
        logging.info("No photos found.")
        return []


def get_review_count(wait):
    """Extract review count."""
    try:
        review_count = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='title']//a[@class='forbid-click reviews-count']//span",
                )
            )
        )
        count = int(review_count.text.strip())
        logging.info(f"Review count found: {count}")
        return count
    except NoSuchElementException:
        logging.error("Review count not found.")
        return None


def get_product_code(wait):
    """Extract product code."""
    try:
        code = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='title']//span[@class='br-pr-code-val']",
                )
            )
        )
        code_text = code.text.strip()
        logging.info(f"Product code found: {code_text}")
        return code_text
    except NoSuchElementException:
        logging.error("Product code not found.")
        return None


def scroll_to_characteristics(driver):
    """Scroll down to characteristics section."""
    try:
        ActionChains(driver).scroll_by_amount(0, 700).perform()
        sleep(random.uniform(2, 5))
        logging.info("Scrolled to amount 700")
    except Exception:
        ActionChains(driver).scroll_by_amount(0, 1000).perform()
        sleep(random.uniform(1, 4))
        logging.info("Scrolled to amount 1000")


def expand_all_characteristics(wait):
    """Click button to show all characteristics."""
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
        logging.info("Clicked 'show all characteristics' button")
        sleep(random.uniform(2, 5))
        return True
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Navigation error to all characteristics: {e}")
        return False


def scroll_after_expand(driver):
    """Scroll down after expanding characteristics."""
    try:
        ActionChains(driver).scroll_by_amount(0, 1000).perform()
        sleep(random.uniform(2, 5))
        logging.info("Scrolled to amount 1000 after expand")
    except Exception:
        ActionChains(driver).scroll_by_amount(0, 1500).perform()
        sleep(random.uniform(1, 4))
        logging.info("Scrolled to amount 1500 after expand")


def parse_specification_row(row):
    """Parse a single specification row to extract key-value pair."""
    try:
        spans = row.find_elements(By.XPATH, ".//span")
        if len(spans) < 2:
            return None, None
        
        key = spans[0].text.strip()
        values = []
        
        for span in spans[1:]:
            # Check for links inside the span
            links = span.find_elements(By.XPATH, ".//a")
            if links:
                values.extend([link.text.strip() for link in links])
            else:
                text = span.text.strip()
                if text:
                    values.append(text)
        
        # Set value to dictionary
        value = ", ".join(values) if values else None
        return key, value
    except Exception as e:
        logging.warning(f"Error parsing specification row: {e}")
        return None, None


def parse_specification_detail(detail):
    """Parse a single specification detail block."""
    specs = {}
    try:
        title_section = detail.find_element(By.XPATH, ".//h3").text.strip()
        specs[title_section] = {}
        
        rows = detail.find_elements(By.XPATH, ".//div")
        for row in rows:
            key, value = parse_specification_row(row)
            if key:
                specs[title_section][key] = value
        
        return specs
    except NoSuchElementException:
        logging.warning("Section title (h3) not found in detail block")
        return {}


def get_product_specifications(wait):
    """Extract all product specifications."""
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
                    detail_specs = parse_specification_detail(detail)
                    specs_dict.update(detail_specs)
                    
                logging.info(f"Collected details for specification section.")
            except NoSuchElementException:
                logging.error("Specification details not found.")
                continue
        
        logging.info(f"Collected {len(specs_dict)} specification sections.")
        return specs_dict
        
    except NoSuchElementException:
        logging.error("Specifications not found.")
        return {}


def extract_specific_specs(specifications):
    """Extract specific specifications from the full specs dictionary."""
    specific_data = {}
    
    try:
        specific_data["manufacturer"] = specifications.get("Інші", {}).get("Виробник")
    except Exception as e:
        logging.warning(f"Could not extract manufacturer: {e}")
        specific_data["manufacturer"] = None
    
    try:
        specific_data["memory"] = specifications.get("Функції пам'яті", {}).get("Вбудована пам'ять")
    except Exception as e:
        logging.warning(f"Could not extract memory: {e}")
        specific_data["memory"] = None
    
    try:
        specific_data["color"] = specifications.get("Фізичні характеристики", {}).get("Колір")
    except Exception as e:
        logging.warning(f"Could not extract color: {e}")
        specific_data["color"] = None
    
    try:
        specific_data["screen_diagonal"] = specifications.get("Дисплей", {}).get("Діагональ екрану")
    except Exception as e:
        logging.warning(f"Could not extract screen diagonal: {e}")
        specific_data["screen_diagonal"] = None
    
    try:
        specific_data["screen_resolution"] = specifications.get("Дисплей", {}).get("Роздільна здатність екрану")
    except Exception as e:
        logging.warning(f"Could not extract screen resolution: {e}")
        specific_data["screen_resolution"] = None
    
    return specific_data


def collect_product_data(driver):
    """Collect product data from the product page."""
    wait = WebDriverWait(driver, 10)
    logging.info("Start collecting product data...")
    
    product_data = {}
    
    # Basic product information
    product_data["title"] = get_product_title(wait)
    product_data["regular_price"] = get_product_price(wait)
    product_data["sale_price"] = None
    product_data["photos"] = get_product_photos(wait)
    product_data["review_count"] = get_review_count(wait)
    product_data["code"] = get_product_code(wait)
    
    # Scroll and expand characteristics
    scroll_to_characteristics(driver)
    expand_all_characteristics(wait)
    scroll_after_expand(driver)
    
    # Collect specifications
    product_data["specifications"] = get_product_specifications(wait)
    
    # Extract specific specifications
    specific_specs = extract_specific_specs(product_data["specifications"])
    product_data.update(specific_specs)
    
    print(product_data)
    return product_data