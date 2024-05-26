# TYPING
from typing import Final, List, Set

# SELENIUM
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

# REQUESTS
import requests
from requests import RequestException

# MISC
from io import BytesIO
import time
from PIL import Image, UnidentifiedImageError
from colorama import Fore, init

def click_reject_cookies_btn(webdriver: Chrome, delay: int) -> None:
    try:
        # Attempting the first version:
        try:
            reject_all_cookies_button: WebElement = WebDriverWait(webdriver, delay).until(EC.element_to_be_clickable((By.ID, "W0wltc")))
            reject_all_cookies_button.click()
            print(Fore.GREEN + "Reject all cookies button (v1) was clicked successfully!")
            return
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(Fore.RED + f"First attempt failed at clicking reject all cookies button: <{e.__class__.__name__}>")

        # Attempting the second version:
        reject_all_cookies_button_v2: WebElement = WebDriverWait(webdriver, delay).until(
            EC.element_to_be_clickable(webdriver.find_elements(By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-k8QpJ")[0])
        )
        reject_all_cookies_button_v2.click()

        print(Fore.GREEN + "Reject all cookies button (v2) was clicked successfully!")
        return
    except (NoSuchElementException, TimeoutException, WebDriverException, IndexError) as e:
        print(Fore.RED + f"Both attempts failed at clicking reject all cookies button: <{e.__class__.__name__}>")

def download_image(url: str, path: str, file_name: str) -> None:
    file_path = path + file_name

    try:
        image_content: bytes = requests.get(url).content
        image_file_int_memory: BytesIO = BytesIO(image_content)
        image: Image = Image.open(image_file_int_memory)

        with open(file_path, "wb") as file:
            image.save(file, "JPEG")

        print(Fore.GREEN + f"Image downloaded at: [{file_path}]")
    except (RequestException, UnidentifiedImageError, IOError, OSError) as e:
        print(Fore.RED + f"Failed downloading image at [{file_path}]: <{e.__class__.__name__}>")

def get_image_urls(webdriver: Chrome, delay: int, search_term: str) -> None:
    URL: str = f"https://www.google.com/search?q={search_term}&sca_esv=d7d681b5ae96d960&sca_upv=1&hl=en&sxsrf=ADLYWII_hAmKnNUMYi8CAGUjUJ7uQDazww:1716662791317&source=hp&biw=1920&bih=945&ei=BzJSZsuHELyh5NoPoY-k-AY&iflsig=AL9hbdgAAAAAZlJAF0QPatPymQiT7gtJxVJUgv6iNBOH&ved=0ahUKEwiLp_2eu6mGAxW8EFkFHaEHCW8Q4dUDCA8&uact=5&oq=cats&gs_lp=EgNpbWciBGNhdHMyBBAjGCcyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIqAhQ-QNY_wZwAXgAkAEAmAHlAaABggWqAQUwLjMuMbgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIFoAKPBagCCsICBxAjGCcY6gKYAwWSBwUxLjMuMaAH_hk&sclient=img&udm=2"
    webdriver.get(URL)

    # Clicking reject all cookies button:
    click_reject_cookies_btn(webdriver, delay)

    

def main() -> None:
    # TEXT COLOR RESET:
    init(autoreset=True)

    # CRHOME DRIVER SETUP:
    CHROME_DRIVER_PATH: Final[str] = "C:\\Users\\xptee\\Documents\\Prog\\AstolfoBot\\webscraper\\chromedriver.exe"
    driver_options: Options = Options()
    driver_services: Service = Service(CHROME_DRIVER_PATH)
    webdriver: Chrome = Chrome(service=driver_services, options=driver_options)

    get_image_urls(webdriver, 1, "astolfo")

    # QUITTING THE WEBDRIVER:
    try:
        webdriver.quit()
        print(Fore.GREEN + "Quit the webdriver successfully!")
    except WebDriverException as e:
        print(Fore.RED + "Error while quitting webdriver!" + Fore.WHITE + e)

if __name__ == "__main__":
    main()