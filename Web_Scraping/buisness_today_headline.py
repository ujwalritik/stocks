import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from MongoDb_connector import conn
from driver_options import driver_option

def headlines():
    collection = conn()
    driver = driver_option()
    # Open Main Web Page
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
        "title": title,
        "sub_heading": sub_heading,
        "publisher": publisher,
        "story": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    collection.insert_one(data)