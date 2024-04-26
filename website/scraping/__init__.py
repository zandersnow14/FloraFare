
import logging
from os import environ

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .kojo import *
from .pfas import *

load_dotenv()

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument(f'user-agent={environ["USER_AGENT"]}')


def get_website_name(url: str) -> str:
    """Returns the website name."""

    name = regex.findall(DOMAIN_REGEX, url)[0]

    return name


def get_kojo_sizes(url: str) -> list:
    """Returns a list of the plant sizes."""

    logging.info("Getting sizes")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    sizes = driver.find_elements(
        by=By.CLASS_NAME, value="variant__button-label")
    return [s.text for s in sizes]


def scrape_kojo(url: str, choice: str) -> dict:
    """Scrapes a House of Kojo product page for info."""

    plant_data = dict()

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    get_kojo_size_page(driver, choice)

    plant_name = f"{get_kojo_plant_name(driver)} {choice}"

    plant_data['plant_name'] = plant_name
    plant_data['current_price'] = get_kojo_current_price(driver)
    plant_data['og_price'] = get_kojo_og_price(driver)
    plant_data['image_url'] = get_kojo_image(driver)
    print(plant_data['image_url'])
    plant_data['url'] = url
    plant_data['in_stock'] = get_kojo_stock(driver, choice)

    driver.close()

    return plant_data


def scrape_seasons(url: str) -> dict:
    """Scrapes a Plants for all Seasons product page for info."""

    plant_data = {}

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    plant_name = get_seasons_plant_name(driver)
    current_price = get_seasons_current_price(driver)
    image = get_seasons_plant_image(driver)
    og_price = get_seasons_og_price(driver)
    stock = get_seasons_stock(driver)

    plant_data['plant_name'] = plant_name
    plant_data['url'] = url
    plant_data['image_url'] = image
    plant_data['current_price'] = current_price
    plant_data['og_price'] = og_price
    plant_data['in_stock'] = stock

    driver.close()

    return plant_data
