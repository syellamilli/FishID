import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import copy
import unicodedata
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.request import urlopen
import signal
from contextlib import contextmanager



class TimeoutException(Exception): pass



@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        
        
        
        
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def clean_query(value):
    return value.replace("&", "and")
        
        
        
def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: .001):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    query = clean_query(query)
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    
    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements(by=By.CSS_SELECTOR, value="img.Q4LuWd")
        number_results = len(thumbnail_results)

        #print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements(by=By.CSS_SELECTOR, value='img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))


            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                #print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            #print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(.1)
            load_more_button = wd.find_elements(by=By.CSS_SELECTOR, value='.mye4qd')
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
                
            if len(thumbnail_results) == results_start:
                #print("No more results")
                return image_urls
            results_start = len(thumbnail_results)
            continue
    return image_urls



def persist_image(folder_path:str,url:str, counter):
    try:
        with time_limit(3):
            image_formats = ("image/png", "image/jpeg", "image/gif")
            site = urlopen(url)
            meta = site.info()
            image_type = meta["content-type"]
            if image_type in image_formats:
                image_content = requests.get(url).content
    except Exception as e:
        #print(f"ERROR - Could not download {url} - {e}")
        return

    try:
        filename = slugify(url.split('/')[-1].split('.')[0])[:254]
        if image_type == "image/jpeg":
            f = open(os.path.join(folder_path, filename + ".jpg"), 'wb')
        elif image_type == "image/png":
            f = open(os.path.join(folder_path, filename + ".png"), 'wb')
        elif image_type == "image/gif":
            f = open(os.path.join(folder_path, filename + ".gif"), 'wb')
        else:
            raise ValueError
        f.write(image_content)
        f.close()
        #print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        #print(f"ERROR - Could not save {url} - {e}")
        return
    
        
        
def search_and_download( search_term: str, save_folder, driver, target_path='/media/shivaram/SharedVolum/Projects/FishID/scraped_images/', number_images=10):
    target_folder = os.path.join(target_path, save_folder)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    else:
        return

    res = fetch_image_urls(search_term, number_images, wd=driver, sleep_between_interactions=0.001)
       
    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1