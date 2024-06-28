# DISCORD
from discord import File

# TYPING
from typing import Final

# SELENIUM
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

# COLORAMA
from colorama import Fore, init

# WEBSCRAPER
from scraper import get_random_image_url, download_image, quit_webdriver

# ASYNC
import asyncio
from concurrent.futures import ThreadPoolExecutor

#   CURRENT ISSUES:
#       - No error handling for get_random_image(...)

def get_random_image(search_term: str) -> File:
    # TEXT COLOR RESET:
    init(autoreset=True)

    # CRHOME DRIVER SETUP:
    CHROME_DRIVER_PATH: Final[str] = "C:\\Users\\xptee\\Documents\\Projects\\WaifuBot\\chromedriver.exe"
    driver_options: Options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--disable-gpu")
    driver_services: Service = Service(CHROME_DRIVER_PATH)
    webdriver: Chrome = Chrome(service=driver_services, options=driver_options)

    # Getting the image url:
    image_url: str = get_random_image_url(webdriver, 3, search_term)
    if image_url is None:
        print(Fore.RED + "No image url was extracted!")
        quit_webdriver(webdriver)
        return None # !!! raise NoImageException

    # QUITTING THE WEBDRIVER:
    quit_webdriver(webdriver)

    # Downloading the image:
    download_image(image_url, "src\\imgs\\", "discord_img.jpg")

    return File("src\\imgs\\discord_img.jpg", "discord_img.jpg")

# Async wrapper for get_random_image(...):
async def async_get_random_image(search_term: str) -> File:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, get_random_image, search_term)

    return result

if __name__ == "__main__":
    img: File = get_random_image("cat")
    print(f"\n{img}")