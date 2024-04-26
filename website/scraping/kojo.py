
import logging
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

PRICE_REGEX = "[^£]*$"
VARIANT_REGEX = "(?<=variant\=).*"


def get_kojo_stock(web_driver: WebDriver, choice: str) -> bool:
    """Finds the stock availability."""

    label = web_driver.find_element(
        by=By.XPATH, value=f'//div[@data-value="{choice.split()[0]}"]/label')

    label_class = label.get_attribute("class")

    if "disabled" in label_class:
        return False
    return True


def get_webpage(url: str, options: Options) -> WebDriver:
    """Returns a web driver at the given URL."""

    driver = webdriver.Chrome(options=options)

    logging.info("Getting URL")

    driver.get(url)
    return driver


def get_kojo_variant_id(url: str) -> str | None:
    """Returns the variant ID if it exists."""

    logging.info("Retrieving variant ID")

    try:
        return re.findall(VARIANT_REGEX, url)[0]
    except IndexError:
        return None


def get_kojo_og_price(web_driver: WebDriver) -> float:
    """Returns the original price of a plant."""

    prices = web_driver.find_elements(by=By.CLASS_NAME, value="product__price")
    prices = [round(float(re.findall(PRICE_REGEX, p.text)[0]), 2)
              for p in prices if p.text != '']

    return max(prices)


def get_kojo_current_price(web_driver: WebDriver) -> float:
    """Returns the current price of a plant."""

    logging.info("Getting plant price")

    prices = web_driver.find_elements(by=By.CLASS_NAME, value="product__price")
    prices = [round(float(re.findall(PRICE_REGEX, p.text)[0]), 2)
              for p in prices if p.text != '']

    return min(prices)


def get_kojo_plant_name(web_driver: WebDriver) -> str:
    """Returns the name of a plant."""

    logging.info("Getting plant name")

    plant_name = web_driver.find_element(
        by=By.CLASS_NAME, value="product-single__title")

    return plant_name.text.title()


def get_kojo_plant_size(web_driver: WebDriver, variant: str) -> str:
    """Returns the size of the plant."""

    logging.info("Getting plant size")

    if variant:
        size = web_driver.find_element(
            by=By.CSS_SELECTOR, value=f"label[data_meta_id='{variant}']")
    else:
        size = web_driver.find_element(
            by=By.CLASS_NAME, value="variant__button-label")
    return size.text


def get_kojo_image(web_driver: WebDriver) -> str:
    """Returns the image URL for a plant."""

    logging.info("Getting plant image")

    image = web_driver.find_element(
        by=By.CLASS_NAME, value="photoswipe__image")
    return image.get_attribute("data-photoswipe-src")[2:]



def get_kojo_size_page(web_driver: WebDriver, choice: str) -> None:
    """Gets on the page with the chosen size."""

    web_driver.find_element(
        by=By.XPATH, value=f'//div[@data-value="{choice.split()[0]}"]/label').click()
