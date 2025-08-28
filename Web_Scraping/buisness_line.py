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

# Open Main Web Page
driver.get("https://www.thehindubusinessline.com/")

news = WebDriverWait(driver, 5).until(
    ec.presence_of_element_located((By.CLASS_NAME, "news-lg-title"))
)
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", news)
time.sleep(2)
news.click()
title = driver.find_element(By.CSS_SELECTOR, "h1.title").text
sub_heading = driver.find_element(By.CLASS_NAME, "sub-title").text
publisher = driver.find_element(By.CLASS_NAME, "story-publisher").text
story = WebDriverWait(driver, 15).until(
        ec.presence_of_element_located((By.CLASS_NAME, "article-main"))
    ).text
# Goes back to main page
driver.back()
# Store Local variable into JSON format
data = {
        "title" : title,
        "sub_heading" : sub_heading,
        "publisher" : publisher,
        "story" : story,
        "timestamp" : datetime.datetime.now().isoformat()
    }
collection.insert_one(data)

# Getting url of all other topics
elements = driver.find_elements(By.CSS_SELECTOR, "h2.title a")
urls = []

# Storing url in a list
for e in elements:
    url = e.get_attribute("href")
    urls.append(url)

#Getting information of url
for u in urls:
    driver.get(u)
    title = driver.find_element(By.CSS_SELECTOR, "h1.title").text
    sub_heading = driver.find_element(By.CLASS_NAME, "sub-title").text
    publisher = driver.find_element(By.CLASS_NAME, "story-publisher").text
    story = WebDriverWait(driver, 15).until(
        ec.presence_of_element_located((By.CLASS_NAME, "article-main"))
    ).text

    data = {
        "title" : title,
        "sub_heading" : sub_heading,
        "publisher" : publisher,
        "story" : story,
        "timestamp" : datetime.datetime.now().isoformat()
    }
    collection.insert_one(data)
driver.quit()
