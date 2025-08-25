# 📈 Stock Data Fetcher

This project allows you to **fetch and store stock market data** using:

- **[yfinance](https://pypi.org/project/yfinance/)** → For historical or daily stock data.
- **Web Scraping** → For live stock data (LTP & Volume) directly from market websites.

The fetched data is stored in a **SQL Server database** for further analysis and reporting.

---

## 🚀 Features

- **Historical/Daily Data**  
  - Uses `yfinance` to get Open, High, Low, Close, Volume, and Date for NSE-listed stocks.  
  - Supports fetching data for a specific day or over a range of dates.
  
- **Live Data**  
  - Web scraping to get the **latest price (LTP)** and **current volume**.  
  - Automatically converts volume from *Lakhs* to actual numbers.

- **Database Integration**  
  - Inserts fetched data into SQL Server tables:
    - `historical_data` → Historical/Daily data.
    - `live_data` → Real-time scraped data.
  - Automatically formats numeric and date values for SQL compatibility.

---

# 📂 Project Structure

📁 project_root<br />
│-- 📂 data # Contains CSV files for symbols<br />
│ │-- StocksTraded.csv<br />
│ │-- <TICKER>.NS.csv<br />
│<br />
│-- 📁 Yfinance<br />
│ │-- db_connector.py # SQL Server connection handler<br />
│ │-- data_modify.py # Fetching and modifying data from csv and uploading in SQL Server<br />
│ │-- todays_data.py # Fething and Uploading last trading day data<br />
│ │-- historical_data.py # Fetching and saving data into csv files<br />
|<br />
│-- 📁 Web_scraping<br />
│ │-- data_modification # Modifying data & uploading it in database<br />
│ │-- web_scraping # Scrape data from NSE official website<br />
│<br />
│-- README.md # Project documentation<br />
│-- LICENSE # Apache 2.0 Licence<br />
