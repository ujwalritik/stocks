import datetime
import time

from pywinauto.timings import wait_until
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyodbc as db
import pandas as pd
import os

def dbms():
    conn = db.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=MSI;'
        'DATABASE=Stock;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    return conn

def add_to_database():
    conn = dbms()
    cursor = conn.cursor()
    data = pd.read_csv('C:\\Users\\ritik\\Downloads\\StocksTraded.csv')
    os.remove('C:\\Users\\ritik\\Downloads\\StocksTraded.csv')
    data = data[['Symbol ', 'LTP ', 'Volume (Lakhs)']]
    data['LTP '] = data[['LTP ']].fillna(0).astype(float).round(2)
    data['Volume (Lakhs)'] = data['Volume (Lakhs)'] * 100000
    data['Volume (Lakhs)'] = data[['Volume (Lakhs)']].fillna(0).astype(int).round(0)

    rows_to_insert = data[['Symbol ', 'LTP ', 'Volume (Lakhs)']].values.tolist()
    query_ = """
        insert into live_data(ticker, ltp, volume) values(?,?,?)
    """
    time.sleep(10)
    cursor.executemany(query_, rows_to_insert)
    time.sleep(10)
    conn.commit()
    print('✅')

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

reset_time = datetime.datetime(2025, 8, 25, 15, 30, 0)

def open_stocks_traded():
    while datetime.datetime.now() < reset_time:
        try:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            download_bt = driver.find_element(By.ID, "StocksTraded-download")
            time.sleep(7)
            download_bt.click()
            add_to_database()
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()
            open_stocks_traded()
        except Exception as e:
            time.sleep(2)

open_stocks_traded()
driver.quit()