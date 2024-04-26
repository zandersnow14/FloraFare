
import logging
import re

import regex
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

SEASONS_PLANT_REGEX = "(?<=[0-9]*cm\s).*(?=\s[0-9]*cm)"
DOMAIN_REGEX = "(?<=www\.).+?(?=\.)"
IMAGE_URL_REGEX = "(?=www\.).*"
PRICE_REGEX = "[^£]*$"


def get_seasons_stock(web_driver: WebDriver) -> bool:
    """Returns whether the plant is in stock or not."""

    try:
        web_driver.find_element(
            by=By.XPATH, value="//div[@class='wrapper-button']/input[@value='Add to cart']")
        return True

    except:
        return False


def get_seasons_plant_name(web_driver: WebDriver) -> str:
    """Returns the plant name from a PfaS product."""

    # ------- JUST ADD THE ENTIRE TEXT ------------

    logging.info("Getting plant name")

    plant_name = web_driver.find_element(
        by=By.XPATH, value='//h1[@class="product-title"]/span')

    # plant_name = regex.findall(SEASONS_PLANT_REGEX, full_plant_name.text)[0]

    return plant_name.text


def get_seasons_plant_image(web_driver: WebDriver) -> str:
    """Returns the plant image from a PfaS product."""

    logging.info("Getting plant image")

    plant_image = web_driver.find_element(
        by=By.XPATH, value="//a[@class='fancybox']/img")
    image_url = plant_image.get_attribute("src")
    return regex.findall(IMAGE_URL_REGEX, image_url)[0]


def get_seasons_og_price(web_driver: WebDriver) -> float:
    """Gets the original price of a PfaS product."""

    try:
        og_price_text = web_driver.find_element(
            by=By.XPATH, value="//span[@class='compare-price']")
    except:
        og_price_text = web_driver.find_element(
            by=By.XPATH, value="//span[@class='price']")

    og_price = round(
        float(re.findall(PRICE_REGEX, og_price_text.text)[0]), 2)

    return og_price


def get_seasons_current_price(web_driver: WebDriver) -> float:
    """Returns the current price of a PfaS product."""

    logging.info("Getting current price")

    try:
        current_price_text = web_driver.find_element(
            by=By.XPATH, value="//div[@class='prices']/span[@class='price on-sale']")
    except:
        current_price_text = web_driver.find_element(
            by=By.XPATH, value="//div[@class='prices']/span[@class='price']")

    current_price = round(
        float(re.findall(PRICE_REGEX, current_price_text.text)[0]), 2)

    return current_price
