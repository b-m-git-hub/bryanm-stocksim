import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, date

today = date.today()
yesterday = today - timedelta(days=1)

ticker = "^GSPC"
start_date = "2025-11-03"
end_date = "2025-11-04"
auto_start_date = yesterday
auto_end_date = today

sp500_data = yf.download(ticker, start=start_date, end=end_date, interval="1m")
#sp500_data = yf.download(ticker, start=auto_start_date, end=auto_end_date, interval="1m")

if sp500_data.empty:
    print("Empty data set")

csv_filename = f"data/S&P500 on {start_date}.csv"
#csv_filename = f"data/S&P500 on {yesterday.isoformat()}.csv"

sp500_data.to_csv(csv_filename)

print(f"Daily OHLC data for {ticker} saved to {csv_filename}")