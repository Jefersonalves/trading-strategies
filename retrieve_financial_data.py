import yfinance as yf

#https://github.com/ranaroussi/yfinance
asset = yf.Ticker("CPLE6.SA")

#valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
data = asset.history(start="2021-09-01", end="2021-09-07", interval='1m')

data = data.reset_index()
data.columns = [c.lower() for c in data.columns]
data = data.rename(columns={'date': 'datetime'})

columns_order = ['datetime','open','high','low','close','volume']
data = data[columns_order]

data.to_csv('asset.csv', index=False)