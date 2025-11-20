"""
Chrome WebDriver configuration for undetected_chromedriver.
"""

import undetected_chromedriver as uc


def get_chrome_options() -> uc.ChromeOptions:
    """
    Configure Chrome options for stealth and anti-detection.

    Returns:
        Configured ChromeOptions instance
    """
    options = uc.ChromeOptions()

    # stealth mode
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")

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

    return options


def create_driver(chrome_version: int) -> uc.Chrome:
    """
    Create and configure Chrome WebDriver instance.

    Args:
        chrome_version: Chrome browser version

    Returns:
        Configured Chrome WebDriver instance
    """
    options = get_chrome_options()
    driver = uc.Chrome(
        options=options, use_subprocess=True, version_main=chrome_version
    )
    driver.maximize_window()
    return driver
