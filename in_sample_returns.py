import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

file_path = "C:\\Users\\Joshua\\Documents\\tickers_pe_ratios.xlsx"
df = pd.read_excel(file_path, sheet_name = "Sheet1")
tickers = list(map(str, df["TickerTen"].tolist()))
weights = df["Weight"].tolist()

individual_returns = []

max_iterations = 10

for i, ticker in enumerate(tickers):
    if i >= max_iterations:
        break
    data = yf.download(ticker, start = "2021-01-01", end = "2021-12-31")
    if data.empty:
        print(f"No data available for {ticker}.")
        continue
    return_ = (data["Adj Close"].iloc[-1] - data["Adj Close"].iloc[0]) / \
    data["Adj Close"].iloc[0]
    individual_returns.append(return_)

for ticker, return_, weight in zip(tickers, individual_returns, weights):
    print(f"{ticker}: {return_:.2%}")

portfolio_return = 0
initial_investment = 1000
for return_, weight in zip(individual_returns, weights):
    portfolio_return += return_ * weight * initial_investment

portfolio_return = portfolio_return + 1000

print(f"\nCumulative Portfolio Return (assuming $1000 investment): \
${portfolio_return:.2f}")

data = yf.download("^GSPC", start = "2021-01-01", end = "2021-12-31")

sp500_2021_return = (data["Close"][-1] / data["Close"][0]) - 1

x = [1, 12]
y = [1000, 1000 * (1 + sp500_2021_return)]

x2 = [1, 12]
y2 = [1000, portfolio_return]

plt.plot(x2, y2)
plt.plot(x, y)

plt.title("NVNG Model vs. S&P 500 for 2021")
plt.xlabel("Months")
plt.ylabel("Investment Value")

plt.legend(["NVNG Model (EOY = $1,406.11)", "S&P 500 (EOY = $1,291.32)"])

plt.xticks(range(1,13))

plt.show()
