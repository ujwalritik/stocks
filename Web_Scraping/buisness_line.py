import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from MongoDb_connector import conn
from driver_options import driver_option

def other_news():
    collection = conn()
    driver = driver_option()
    driver.get("https://www.thehindubusinessline.com/")
    time.sleep(2)
    # Getting url of all other topics
    elements = driver.find_elements(By.CSS_SELECTOR, "h2.title a")
    urls = []

    # Storing url in a list
    for e in elements:
        url = e.get_attribute("href")
        urls.append(url)

    # Getting information of url
    for u in urls:
        driver.get(u)
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1.title").text
            sub_heading = driver.find_element(By.CLASS_NAME, "sub-title").text
            publisher = driver.find_element(By.CLASS_NAME, "story-publisher").text
            story = WebDriverWait(driver, 15).until(
                ec.presence_of_element_located((By.CLASS_NAME, "article-main"))
            ).text

            data = {
                "title": title,
                "sub_heading": sub_heading,
                "publisher": publisher,
                "story": story,
                "timestamp": datetime.datetime.now().isoformat()
            }
            collection.insert_one(data)
        except Exception as e:
            print(f"Exception Occured : {e}")