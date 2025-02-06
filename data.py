import yfinance as yf
data = yf.download("AAPL", period = "1d", interval = "1m")
#print(data)

import pandas as pd

df = pd.DataFrame(data)

df.columns = df.columns.droplevel(1)

df.index.name = None

df = df.reset_index()
df = df.rename_axis(None, axis=1)
df = df.rename(columns={"index": "Datetime"})
df = df.drop(columns=['Datetime'])
print(df.columns)
print(df.head())