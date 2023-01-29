import pandas as pd
import matplotlib.pyplot as plt

df_excel = \
pd.read_excel("C:\\Users\\Joshua\\Documents\\tickers_pe_ratios.xlsx", \
sheet_name="Sheet1")

pe_ratios = df_excel[(df_excel["P/E Ratio"] > -200) & \
(df_excel["P/E Ratio"] < 200)]["P/E Ratio"]

plt.hist(pe_ratios, bins = 20)
plt.xlabel("P/E Ratio")
plt.ylabel("Frequency")
plt.title("Distribution of P/E Ratios for S&P 500 Stocks in 2020")
plt.show()

print(f"Mean: {pe_ratios.mean()}")
print(f"Standard Deviation: {pe_ratios.std()}")

df_excel['diff'] = abs(df_excel['P/E Ratio'] - 26.81299628058758) # Mean

df_excel_2 = df_excel.sort_values(by=['diff'])

ticker_symbols = df_excel_2["Ticker"].head(10)

goldilocks_stocks = ticker_symbols.tolist()
print(goldilocks_stocks)
