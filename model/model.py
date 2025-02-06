import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

DB_HOST = 'my-mysql'
DB_USER = 'arun'
DB_PASSWORD = 'root'
DB_NAME = 'yfinance'

def fetch_data():
    """ Fetch data from MySQL database """
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    query = "SELECT high, volume FROM finance"
    df = pd.read_sql(query, conn)
    conn.close()
    
    #df["age_group"] = df["age_group"].apply(lambda x: 1 if x == "Adult" else 0)
    return df

def train_model(df):
    """ Train a simple logistic regression model """
    X = df[["high"]]
    y = df["volume"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    with open("trained_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("Model trained and saved.")

def train_pipeline():
    df = fetch_data()
    train_model(df)

if __name__ == "__main__":
    train_pipeline()
