from typing import Final, List, Set
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import requests
import io
from PIL import Image
import time
from aiohttp import ClientSession
import aiofiles
from colorama import Fore, init

# Reset text coloring:
init(autoreset=True)

PATH: Final[str] = "C:\\Users\\xptee\\Documents\\Prog\\AstolfoBot\\webscraper\\chromedriver.exe"
options: Options = Options()
# options.add_argument("--headless")
wd: webdriver.Chrome = webdriver.Chrome(service=Service(PATH), options=options)
img_class: Final[str] = "sFlh5c"

def click_accept_cookies_button(wd: webdriver.Chrome) -> None:
    accept_btn: WebElement = wd.find_element(By.ID, "L2AGLb")
    accept_btn.click()

def scroll_down(wd: webdriver.Chrome):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def get_images_from_google(wd: webdriver.Chrome, max_images: int, delay: int, search_term:str) -> Set[str]:
    URL: str = f"https://www.google.com/search?q={search_term}&sca_esv=d7d681b5ae96d960&sca_upv=1&hl=en&sxsrf=ADLYWII_hAmKnNUMYi8CAGUjUJ7uQDazww:1716662791317&source=hp&biw=1920&bih=945&ei=BzJSZsuHELyh5NoPoY-k-AY&iflsig=AL9hbdgAAAAAZlJAF0QPatPymQiT7gtJxVJUgv6iNBOH&ved=0ahUKEwiLp_2eu6mGAxW8EFkFHaEHCW8Q4dUDCA8&uact=5&oq=cats&gs_lp=EgNpbWciBGNhdHMyBBAjGCcyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIqAhQ-QNY_wZwAXgAkAEAmAHlAaABggWqAQUwLjMuMbgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIFoAKPBagCCsICBxAjGCcY6gKYAwWSBwUxLjMuMaAH_hk&sclient=img&udm=2"
    wd.get(URL)
    
    # Clicking the 'Accept all' cookies button:
    try:
        click_accept_cookies_button(wd)
        print("Clicked accept cookies button [get_images_from_google]")
    except Exception as e:
        print(Fore.RED + f"Failed clicking accept cookies button <{e}> [get_images_from_google]")

    image_urls: Set[str] = set()
    thumbnails: List[WebElement] = wd.find_elements(By.CLASS_NAME, "mNsIhb")

    # Scrolling down until we load more images then the max_images:
    while len(thumbnails) < max_images:
        scroll_down(wd)
        thumbnails: List[WebElement] = wd.find_elements(By.CLASS_NAME, "mNsIhb")
        time.sleep(delay)
    
    print(f"Amount of thumbnails loaded: {len(thumbnails)}")

    for i, img in enumerate(thumbnails):
        if i >= max_images:
            break

        try:
            img.click()
            time.sleep(delay)
        except Exception as e:
            print(Fore.YELLOW + "Was unable to click img: " + Fore.WHITE + f"<{img}> [get_images_from_google]")
            continue
        
        try:
            inner_image: WebElement = wd.find_element(By.CLASS_NAME, "iPVvYb")
            src: str = inner_image.get_attribute("src")

            if src and "http" in src:
                image_urls.add(src)
                print(Fore.GREEN + "Image added: " + Fore.WHITE + f"<{inner_image}>")
        except:
            print(Fore.RED + "Image source could not be loaded!")
            continue

    return image_urls

def download_image(path: str, url: str, file_name: str) -> None:
    file_path: str = path + file_name
    
    try:
        image_content: bytes = requests.get(url).content
        image_file: io.BytesIO = io.BytesIO(image_content)
        image: Image = Image.open(image_file)

        with open(file_path, "wb") as file:
            image.save(file, "JPEG")

        print(Fore.GREEN + f"Image downloaded at: <{file_path}> [download_image]")
    except Exception as e:
        print(Fore.RED + f"Failed downloading image at: <{file_path}> [download_image]: {e}")

async def download_image_async(session: ClientSession, path: str, url: str, file_name: str) -> None:
    file_path = path + file_name

    try:
        async with session.get(url) as response:
            if response == 200:
                image_content: bytes = await response.read()
                image_file: io.BytesIO = io.BytesIO(image_content)
                image: Image = Image.open(image_file)

                async with aiofiles.open(file_path, "wb") as file:
                    image.save(file, "JPEG")

                print(f"Image downloaded at: <{file_path}> [download_image_async]")
            else:
                print(f"Failed downliading image at: <{file_path}> [download_image_async]: Response<{response}>")
    except Exception as e:
        print(f"Failed downliading image at: <{file_path}> [download_image_async]: {e}")


urls: Set[str] = get_images_from_google(wd, 150, 0.5, "cats")
wd.quit()

for k, url in enumerate(urls):
    print(url + "\n")
    download_image("imgs\\", url, f"{k}.jpg")

""" 
async def main() -> None:
    for k, url in enumerate(urls):
        print(url + "\n")
        await download_image_async(ClientSession(), "imgs\\", url, f"{k}.jpg")

asyncio.run(main()) 
"""