import logging
import random
from time import sleep


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

