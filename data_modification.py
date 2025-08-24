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

    rows_to_insert = list(data[['Symbol ', 'LTP ', 'Volume (Lakhs)']].itertuples(index=False, name=None))
    query_ = """
        insert into live_data(ticker, ltp, volume) values(?,?,?)
    """

    cursor.executemany(query_, rows_to_insert)
    conn.commit()
    # Close connection
    cursor.close()
    conn.close()

