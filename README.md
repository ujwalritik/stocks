⚠️⚠️ *Project is in primary development phase* ⚠️⚠️

📈 Stock Data Fetcher
Overview
Stock Data Fetcher is a Python-based solution for fetching and storing both historical and live stock market data. It leverages yfinance for easy access to daily OHLCV data and efficient web scraping to capture live Last Traded Price (LTP) and Volume directly from official market websites. All collected data is automatically formatted and inserted into a SQL Server database, empowering comprehensive analysis and reporting workflows.

Features
Historical/Daily Data:
Fetches Open, High, Low, Close, Volume, and Date for NSE-listed stocks using yfinance. Supports flexible querying for single days or date ranges.

Live Data Acquisition:
Uses web scraping to obtain real-time LTP and current volume. Volumes in lakh units are intelligently converted to absolute values.

SQL Server Integration:
Inserts both historical and live data into dedicated tables:

historical_data for daily/archival records

live_data for current, scraped data
Automatically formats all numeric and date values for compatibility.

Project Structure
text
project_root
│-- data/
│   ├── StocksTraded.csv
│   └── .NS.csv
│
│-- Yfinance/
│   ├── db_connector.py        # SQL Server connection handler
│   ├── data_modify.py         # Data fetching & upload logic
│   ├── todays_data.py         # Daily data capture
│   └── historical_data.py     # Bulk historical data management
│
│-- Web_scraping/
│   ├── data_modification/     # Parsing and DB upload scripts
│   └── web_scraping/          # Scrapers for NSE and market sites
│
│-- README.md                  # Project documentation
│-- LICENSE                    # Apache 2.0 License
Branches
Branch	Purpose/Focus
main	Stable default; consolidated features
backend	Database handling and server logic
frontend	UI scripts, dashboards, web views
news	Stock news and headline integrations
optimized	Performance tuning, faster algorithms
sql	Advanced SQL queries, procedures
Develop and test new features in relevant branches before merging to main.

Setup Instructions
Clone the repository:

bash
git clone https://github.com/your-username/Stock-Data-Fetcher.git
cd Stock-Data-Fetcher
Install dependencies:

Python 3.x, yfinance, pandas, BeautifulSoup, requests, pyodbc

Configure SQL Server:

Edit Yfinance/db_connector.py to enter your SQL connection parameters.

Run Fetchers:

Historical:
python Yfinance/historical_data.py

Daily Data:
python Yfinance/todays_data.py

Live Data Scraping:
python Web_scraping/web_scraping/main.py

Review Data:

All records are stored in your configured SQL Server for easy querying and reporting.

License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

Contributing
Issues, suggestions, and pull requests are welcome! Please raise issues in the appropriate branch for focused development.
