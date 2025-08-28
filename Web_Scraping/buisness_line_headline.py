import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec, wait
from selenium.webdriver.support.ui import WebDriverWait
from MongoDb_connector import conn
from driver_options import driver_option

def headlines():
    collection = conn()
    driver = driver_option()

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
        ec.presence_of_element_located((By.ID, "ControlPara"))
    ).text
    # Goes back to main page
    driver.back()
    # Store Local variable into JSON format
    data = {
        "title": title,
        "sub_heading": sub_heading,
        "publisher": publisher,
        "story": story,
        "timestamp": datetime.datetime.now().isoformat()
    }
    collection.insert_one(data)