import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client["News"]
collection = db["news_data"]

options = Options()

options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)
driver = webdriver.Edge(options=options)

#Open Main Web Page
driver.get("https://www.businesstoday.in/")

news = WebDriverWait(driver, 5).until(
    ec.presence_of_element_located((By.CSS_SELECTOR, "h2 a"))
)
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", news)
time.sleep(2)
news.click()
title = driver.find_element(By.CLASS_NAME, "storyheading").text
sub_heading = driver.find_element(By.CLASS_NAME, "sab_head_tranlate_sec").text
publisher = driver.find_element(By.CLASS_NAME, "brand_detial_main").text
story = WebDriverWait(driver, 15).until(
        ec.presence_of_element_located((By.CLASS_NAME, "text-formatted"))
    )
paragraphs = story.find_elements(By.TAG_NAME, "p")
content = [p.text for p in paragraphs]

data = {
        "title" : title,
        "sub_heading" : sub_heading,
        "publisher" : publisher,
        "story" : content,
        "timestamp" : datetime.datetime.now().isoformat()
    }
collection.insert_one(data)
print(data)
driver.get("https://www.businesstoday.in/")
time.sleep(3)
ele = driver.find_elements(By.CSS_SELECTOR, "h3 a")
urls = []
for e in ele:
    urls.append(e.get_attribute("href"))
for url in urls:
    driver.get(url)
    try:
        title = driver.find_element(By.CLASS_NAME, "bt_story_heading").text
        sub_heading = driver.find_element(By.CLASS_NAME, "bt_story_header_sub_heading").text
        publisher = driver.find_element(By.CLASS_NAME, "bt_story_profile").text
        story = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "text-formatted"))
            )
        paragraphs = story.find_elements(By.TAG_NAME, "p")
        content = [p.text for p in paragraphs]

        data = {
            "title" : title,
            "sub_heading" : sub_heading,
            "publisher" : publisher,
            "story" : content,
            "timestamp" : datetime.datetime.now().isoformat()
        }
    except:
        title = driver.find_element(By.CLASS_NAME, "storyheading").text
        sub_heading = driver.find_element(By.CLASS_NAME, "sab_head_tranlate_sec").text
        publisher = driver.find_element(By.CLASS_NAME, "brand_detial_main").text
        story = WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "text-formatted"))
        )

        paragraphs = story.find_elements(By.TAG_NAME, "p")
        content = [p.text for p in paragraphs]

        data = {
            "title": title,
            "sub_heading": sub_heading,
            "publisher": publisher,
            "story": content,
            "timestamp": datetime.datetime.now().isoformat()
        }
    print(data)
    collection.insert_one(data)

driver.quit()