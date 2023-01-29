import yfinance as yf
import pandas as pd

sp500 = \
pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")\
[0]["Symbol"].tolist()

data = \
yf.download(sp500, start = "2020-12-31", end = "2021-1-1", interval = "1d")

closing_prices = data["Close"]

closing_prices_filled = closing_prices.fillna("NaN")

filepath = "C:\\Users\\Joshua\\Documents\\tickers_pe_ratios.xlsx"
closing_prices_filled.to_excel(filepath, sheet_name = "Sheet1")
