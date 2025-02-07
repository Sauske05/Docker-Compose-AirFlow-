import pandas as pd
import yfinance as yf
import mysql.connector
import os
#database connection
DB_HOST = 'my-mysql'
DB_USER = 'arun'
DB_PASSWORD = 'root'
DB_NAME = 'yfinance'
def extract():
    data = yf.download("AAPL", period = "1d", interval = "1m")
    #print(data)

    df = pd.DataFrame(data)

    df.columns = df.columns.droplevel(1)

    df.index.name = None

    df = df.reset_index()
    df = df.rename_axis(None, axis=1)
    df = df.rename(columns={"index": "Datetime"})
    df = df.drop(columns=['Datetime'])
    return df

def transform(df):
    return df


def load(df):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

        cursor = conn.cursor()
        # Create the database if it doesn't exist
        database_name = 'yfinance'
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' is ready.")
        cursor.execute(f"USE {database_name}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS finance (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                close float,
                high float,
                low float, 
                open float, 
                volume float
            )
        """)

        for _, row in df.iterrows():
            cursor.execute(
                '''INSERT INTO finance (close, high, low, open, volume) 
                VALUES (%s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE 
                close = VALUES(close),
                high = VALUES(high),
                low = VALUES(low),
                open = VALUES(open),
                volume = VALUES(volume)''',
                (float(row["Close"]), float(row["High"]), float(row["Low"]), float(row["Open"]), float(row["Volume"])))

        conn.commit()
        print("Data loaded into MySQL.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

    

def etl_pipeline():
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    etl_pipeline()