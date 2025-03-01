from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import uuid
import time
import os


async def scrape(url):
    download_root = os.path.join(os.getcwd(), "downloads")
    download_folder = f'{download_root}/{uuid.uuid4()}'
    os.makedirs(download_folder, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    driver = webdriver.Remote(
        options=chrome_options,
        command_executor="http://selenium-hub:4444/wd/hub",
    )

    driver.get('https://snapinst.app/')

    input_el = driver.find_element(
        By.CSS_SELECTOR, 'input[id="url"]')

    input_el.send_keys(url)

    download_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="btn-submit"]'))
    )

    download_btn.click()

    close_model_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="close-modal"]'))
    )

    close_model_btn.click()

    download_video_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="download"]/div[1]/div/div/div[2]/div'))
    )

    download_video_btn.click()

    time.sleep(7.5)
    driver.quit()
    return download_folder
