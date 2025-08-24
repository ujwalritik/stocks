import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    data = yf.Ticker(ticker).history(period='max')
    data.to_csv(f'data\\{ticker}.csv')
    print(f"Saved {ticker}.csv with {len(data)} rows")

symbol = pd.read_csv("data\\StocksTraded.csv").copy()
symbol = pd.DataFrame(symbol)
symbol = symbol['Symbol ']

for ticker in symbol:
    get_stock_data(f'{ticker}.NS')
