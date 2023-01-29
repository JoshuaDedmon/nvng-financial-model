import requests
import pandas as pd
from lxml import html
import yfinance as yf

headers= {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) \
    Gecko/20100101 Firefox/87.0",
    "Accept": "text/html, application/xhtml+xml, application/xml; q = 0.9, \
    image/webp,*/*; q = 0.8",
    "Accept-Language": "en-US, en; q = 0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age = 0"
}

ticker = input("Enter a stock ticker: ")

urls = {}
urls["income annually"] = \
f"https://stockanalysis.com/stocks/{ticker}/financials/"

response = requests.get(urls["income annually"], headers = headers)
    
# Just in case. 
eps = None

try:
    stock = yf.Ticker(ticker)
    closing_price = \
    stock.history(start = "2020-12-25", end = "2020-12-31")["Close"].values[0]
    print(f"\n{ticker} had a stock price of ${closing_price:.2f} \
    at the end of 2020.")
except:
    print("I apologize, we don't seem to have that ticker on file.")

if response.status_code != 200:
    print("I apologize, we don't seem to have that ticker on file.")
else:
    tree = html.fromstring(response.content)
    table = tree.xpath("//table[@class = 'w-full whitespace-nowrap']")
    df = pd.read_html(html.tostring(table[0]))[0]
    eps = df.loc[df["Year"] == "EPS (Diluted)"]
    eps = float(eps["2020"].iloc[0])
    print(f"\n{ticker} had an EPS of {eps} at the end of 2020.")
    
if closing_price and eps:
    pe_ratio = closing_price / eps
    print(f"\n{ticker} had a P/E ratio of {pe_ratio:.2f} at the end of 2020.")
else:
    print("I apologize, we don't seem to have that ticker on file.")
