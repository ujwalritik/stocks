import yfinance as yf
import pandas as pd
import pyodbc as db


def dbms():
    return db.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=MSI;'
        'DATABASE=Stock;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )


def get_stock_data(ticker, time):
    value = yf.Ticker(f'{ticker}.NS').history(period=time).reset_index()
    value['Symbol'] = ticker
    return value

symbol = pd.read_csv("..\\data\\StocksTraded.csv").copy()
symbol = symbol['Symbol ']

t = '1d'
conn = dbms()
cursor = conn.cursor()
for s in symbol:
    if t.upper() == 'MAX':
        data = get_stock_data(s, t)
        data = data[['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Date']]
        data['Symbol'] = data['Symbol'].astype(str)
        cols = ['Open', 'High', 'Low', 'Close']
        for col in cols:
            data[col] = data[col].fillna(0).astype(float).round(2)
        data['Volume'] = data['Volume'].fillna(0).astype(int)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        rows = list(data[['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Date']]
                    .itertuples(index=False, name=None))
        if not rows:
            continue
        query = '''insert into historical_data(stock_ticker, open_price, high_price, low_price, close_price, volume, on_date)
         values(?,?,?,?,?,?,?)
        '''
        cursor.executemany(query, rows)
        conn.commit()
        print(f'✅ {s} data has been uploaded for time period {t.upper()}')

    elif t.upper() == '1D':
        data = get_stock_data(s, t)
        data = data[['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Date']]
        data['Symbol'] = data['Symbol'].astype(str)
        cols = ['Open', 'High', 'Low', 'Close']
        for col in cols:
            data[col] = data[col].fillna(0).astype(float).round(2)
        data['Volume'] = data['Volume'].fillna(0).astype(int)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        rows = list(data[['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume', 'Date']]
                    .itertuples(index=False, name=None))
        if not rows:
            continue
        query = '''insert into toady_stock(stock_ticker, open_price, high_price, low_price, close_price, volume, on_date)
                 values(?,?,?,?,?,?,?)
                '''
        cursor.executemany(query, rows)
        conn.commit()
        print(f'✅ {s} data has been uploaded for time period {t.upper()}')
    else:
        break

cursor.close()
conn.close()