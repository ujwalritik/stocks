import pyodbc as db

def dbms():
    conn = db.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=MSI;'
        'DATABASE=Stock;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    return conn


