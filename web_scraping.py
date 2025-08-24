import datetime
import time
import threading
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_modification import add_to_database

# Selenium setup
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

driver.get("https://www.nseindia.com/get-quotes/equity?symbol=KOTAKBANK")

# Wait and click "Home"
home = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "link_0"))
)
home.click()

# Click "All Stock"
all_stock = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href='/market-data/stocks-traded']"))
)
driver.execute_script("window.scrollBy(0, 500);")
all_stock.click()
reset_time = datetime.datetime(2025, 8, 25, 4, 30, 0)
print("Now initiating")
# Function to handle clicking "Stocks Traded"
first = True
def open_stocks_traded():
    while datetime.datetime.now() < reset_time:
        try:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
            driver.refresh()

            download_bt = driver.find_element(By.ID, "StocksTraded-download")
            time.sleep(5)
            """WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.ID, "StocksTraded-download"))
            )"""
            print(datetime.datetime.now())
            download_bt.click()

            print("Stocks Traded link clicked and download triggered.")
            # time.sleep(0)

            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            add_to_database()
            open_stocks_traded()

        except Exception as e:
            print("Retrying Stocks Traded link...", e)
            time.sleep(2)

# Start thread
thread1 = threading.Thread(target=open_stocks_traded)
thread1.start()
thread1.join()

print("Clicked element in headless mode.")
driver.quit()
