from itertools import count

import yfinance as yf
import pandas as pd
from db_connector import dbms

# DB connection
conn = dbms()
cursor = conn.cursor()

def last_day_data(ticker):
    data = yf.Ticker(f"{ticker}.NS").history(period="1D").reset_index()
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    return data


symbols = pd.read_csv('data\\StocksTraded.csv').copy()
symbols = symbols['Symbol ']
# Get latest data
for symbol in symbols:
    data = last_day_data(symbol)
    if data.empty:
        continue
    # Round numeric columns
    for col in ['Open', 'High', 'Low', 'Close']:
        data[col] = data[col].fillna(0).astype(float).round(2)
    data['Volume'] = data['Volume'].fillna(0).astype(int)
    # Extract just the date for the query
    query_date = data['Date'].iloc[0].date()

    query = """INSERT INTO toady_stock(
                stock_ticker, open_price, high_price, low_price, close_price, volume, on_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

    cursor.execute(query, [
        symbol,
        float(data['Open'].iloc[0]),
        float(data['High'].iloc[0]),
        float(data['Low'].iloc[0]),
        float(data['Close'].iloc[0]),
        int(data['Volume'].iloc[0]),
        query_date
    ])
    conn.commit()
    print(f"✅ Inserted {symbol} for {query_date}")


cursor.close()
conn.close()
