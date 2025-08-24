import pandas as pd
from db_connector import dbms


def modified_data(ticker):
    file_path = f"data\\{ticker}.NS.csv"
    data = pd.read_csv(file_path).copy()

    # Keep only required columns and rename to match DB
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].rename(
        columns={
            'Open': 'open_price',
            'High': 'high_price',
            'Low': 'low_price',
            'Close': 'close_price',
            'Volume': 'volume',
            'Date': 'on_date'
        }
    )

    # Add ticker
    data['stock_ticker'] = ticker

    # Clean numeric columns for DECIMAL(10,2)
    for col in ['open_price', 'high_price', 'low_price', 'close_price']:
        data[col] = data[col].fillna(0).astype(float).round(2)

    # Volume as integer
    data['volume'] = pd.to_numeric(data['volume'], errors='coerce').fillna(0).astype(int)

    # Ensure valid date format
    data['on_date'] = pd.to_datetime(data['on_date'], errors='coerce').dt.date

    return data


# Load ticker symbols
symbols_df = pd.read_csv("data\\StocksTraded.csv").copy()
symbols = symbols_df['Symbol '].str.strip()

# Connect to DB
conn = dbms()
cursor = conn.cursor()

for symbol in symbols:
    df = modified_data(symbol)

    # Prepare list of tuples for executemany
    rows_to_insert = list(df[['stock_ticker', 'open_price', 'high_price', 'low_price',
                              'close_price', 'volume', 'on_date']].itertuples(index=False, name=None))

    # Skip if no data
    if not rows_to_insert:
        print(f"⚠️ Skipped {symbol} (no valid rows)")
        continue

    cursor.executemany("""
        INSERT INTO historical_data (
            stock_ticker, open_price, high_price, low_price, close_price, volume, on_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows_to_insert)

    conn.commit()
    print(f"✅ Inserted {len(rows_to_insert)} rows for {symbol}")

# Close connection
cursor.close()
conn.close()
