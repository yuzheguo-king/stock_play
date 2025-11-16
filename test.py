import yfinance as yf



def get_return_div_reinvest(ticker: str, start: str, end: str)->float:
    return 0.0


data = yf.download("AAPL", start="2020-01-01", end="2021-01-01")
print(data.head())