""" 
    GOOGLE IMAGE DOWNLOADER
    
    - Basically opens the chrome webdriver searches for the given search term on google images
    and tries downloading the specified amount of images or downloads a random image.

    - Functions from here are also used in the discord WaifuBot.
"""

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
from requests.exceptions import Timeout

# COOKIES FORM TYPE
from cookies_from_type import CookiesFormType

# MISC
from io import BytesIO
import sys
import os
from PIL import Image, UnidentifiedImageError
from colorama import Fore, init
import random
import time

"""
CURRENT ISSUES:
    - NSFW images cannot be downloaded because of censoring reasons.
"""

def fill_out_cookies_form(webdriver: Chrome, delay: int) -> CookiesFormType:
    # Attempting the first version:
    try:
        reject_all_cookies_button: WebElement = WebDriverWait(webdriver, delay).until(EC.element_to_be_clickable((By.ID, "W0wltc")))
        reject_all_cookies_button.click()
        print(Fore.GREEN + "Reject all cookies button (v1) was clicked successfully!")
        return CookiesFormType.BASIC_COOKIES_POPUP
    except WebDriverException as e:
        print(Fore.RED + f"First attempt failed at clicking reject all cookies button: <{e.__class__.__name__}>")
    
    # Attempting the second version (here we have to accept the cookies):
    try:
        accept_all_cookies_button_v2: WebElement = WebDriverWait(webdriver, delay).until(
            EC.element_to_be_clickable(webdriver.find_elements(By.TAG_NAME, "button")[1])
        )
        accept_all_cookies_button_v2.click()
        print(Fore.GREEN + "Accept all cookies button (v2) was clicked successfully!")
        return CookiesFormType.BEFORE_YOU_PROCEED_COOKIE_FROM
    except (WebDriverException, IndexError) as e:
        print(Fore.RED + f"Both attempts failed at clicking reject all cookies button: <{e.__class__.__name__}>")
        return CookiesFormType.NO_COOKIES

def scroll_down_on_page(webdriver: Chrome) -> None:
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def download_image(url: str, path: str, file_name: str) -> None:
    print(f"\nImage URL: {url}")
    file_path = path + file_name

    try:
        image_request = requests.get(url, timeout=5)
        image_request.raise_for_status()

        image_content: bytes = image_request.content
        image_file_in_memory: BytesIO = BytesIO(image_content)
        image: Image = Image.open(image_file_in_memory)

        with open(file_path, "wb") as file:
            image.save(file, "JPEG")

        print(Fore.GREEN + "Image downloaded at: " + Fore.RESET + f"[{file_path}]")
    except (Timeout, RequestException) as e:
        print(Fore.RED + f"Failed downloading image at [{file_path}]: <{e.__class__.__name__}>")
    except (UnidentifiedImageError, IOError, OSError) as e:
        print(Fore.RED + f"Failed downloading image at [{file_path}]: <{e.__class__.__name__}>")
        
        # Removing corrupted file:
        try:
            os.remove(file_path)
            print(Fore.YELLOW + f"Removed corrupted file at: {file_path}")
        except Exception as e:
            print(f"Error while removing corrupted file at {file_path} <{e.__class__.__name__}>")

def load_image_thumbnails(webdriver: Chrome, form_type: CookiesFormType, delay: int, max_images: int) -> List[WebElement]:
    # Here I implicit wait because sometimes the thumbnails don't load quick enough:
    webdriver.implicitly_wait(delay)
    thumbnails: List[WebElement] = webdriver.find_elements(By.CLASS_NAME, form_type.value[0])

    while len(thumbnails) < max_images and len(thumbnails) > 0:
        scroll_down_on_page(webdriver)
        thumbnails = webdriver.find_elements(By.CLASS_NAME, form_type.value[0])

    return thumbnails

def get_image_urls(webdriver: Chrome, delay: int, search_term: str, max_images: int) -> Set[str]:
    URL: str = f"https://www.google.com/search?q={search_term}&sca_esv=d7d681b5ae96d960&sca_upv=1&hl=en&sxsrf=ADLYWII_hAmKnNUMYi8CAGUjUJ7uQDazww:1716662791317&source=hp&biw=1920&bih=945&ei=BzJSZsuHELyh5NoPoY-k-AY&iflsig=AL9hbdgAAAAAZlJAF0QPatPymQiT7gtJxVJUgv6iNBOH&ved=0ahUKEwiLp_2eu6mGAxW8EFkFHaEHCW8Q4dUDCA8&uact=5&oq=cats&gs_lp=EgNpbWciBGNhdHMyBBAjGCcyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIqAhQ-QNY_wZwAXgAkAEAmAHlAaABggWqAQUwLjMuMbgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIFoAKPBagCCsICBxAjGCcY6gKYAwWSBwUxLjMuMaAH_hk&sclient=img&udm=2"
    webdriver.get(URL)

    # Filling out cookies form:
    form_type: CookiesFormType = fill_out_cookies_form(webdriver, delay)

    if form_type == CookiesFormType.NO_COOKIES:
        print(Fore.YELLOW + "Cookie information form was not found")

    # Loading the thumbnails
    thumbnails: List[WebElement] = load_image_thumbnails(webdriver, form_type, delay, max_images)

    if len(thumbnails) == 0:
        print(Fore.YELLOW + "No thumbnails were found. [ABORTING]")
        return None
    else:
        print(f"Loaded thumbnails: {len(thumbnails)}")

    # Collecting the urls:
    urls: Set[str] = set()

    for i, thumbnail in enumerate(thumbnails):
        if i >= max_images:
            break
        
        # Clicking the thumbnail:
        try:
            clickable_thumbnail: WebElement = WebDriverWait(webdriver, delay).until(EC.element_to_be_clickable(thumbnail))
            clickable_thumbnail.click()
            print(Fore.GREEN + "Thumbnail clicked: " + Fore.RESET + thumbnail.id)
        except WebDriverException as e:
            print(Fore.YELLOW + "Unable to click thumbnail: " + Fore.RESET + f"<{e.__class__.__name__}>")
            continue
        
        # Searching for inner image:
        try:
            image: WebElement = WebDriverWait(webdriver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, "iPVvYb")))
            src: str = image.get_attribute("src")

            if src and "http" in src:
                urls.add(src)
                print(Fore.GREEN + "Image URL added: " + Fore.RESET + str(image))
        except WebDriverException as e:
            print(Fore.RED + "Inner image not found!" + Fore.RESET + f"<{e.__class__.__name__}>")
            continue

    return urls

""" NOT IMPLEMENTED """
def get_random_image_url(webdriver: Chrome, delay: int, search_term: str) -> str:
    raise NotImplementedError

def main() -> None:
    start:float = time.time()

    # TEXT COLOR RESET:
    init(autoreset=True)

    # CRHOME DRIVER SETUP:
    CHROME_DRIVER_PATH: Final[str] = "C:\\Users\\xptee\\Documents\\Prog\\AstolfoBot\\webscraper\\chromedriver.exe"
    driver_options: Options = Options()
    driver_services: Service = Service(CHROME_DRIVER_PATH)
    webdriver: Chrome = Chrome(service=driver_services, options=driver_options)
    search_term: str = sys.argv[1]
    max_images: int = int(sys.argv[2])

    # Getting the image urls:
    urls: Set[str] = get_image_urls(webdriver, 3, search_term, max_images)

    # QUITTING THE WEBDRIVER:
    try:
        webdriver.quit()
        print(Fore.GREEN + "Quit the webdriver successfully! [main]")
    except WebDriverException as e:
        print(Fore.RED + "Error while quitting webdriver!" + Fore.WHITE + e.__class__.__name__)
        return

    # Downloading the images:
    if urls is not None:
        for i, url in enumerate(urls):
            download_image(url, "imgs\\cats\\", f"{search_term}{i}.jpg")
    else:
        print(Fore.YELLOW + "No image urls were loaded. [ABORTING]")

    end: float = time.time()
    n: int = len(os.listdir('imgs\\cats'))

    print(f"Time spent downloading: {end - start}; Number of images downloaded: {n}")

if __name__ == "__main__":
    main()