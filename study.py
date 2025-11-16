import random

import yfinance as yf
import pandas as pd

def get_return(ticker_name: str, length: str):
    sp500_index = yf.Ticker(ticker_name)
    sp500_data = sp500_index.history(period=length)
    price = sp500_data['Close'].tolist()
    return  (price[-1] - price[0]) / price[0]

if __name__ == "__main__":
    print("hello world")
    length = '1y'
    sp500_tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].tolist()
    sp500 = get_return("^GSPC", length)
    print("^GSPC", sp500)
    count = 0
    res = []
    for ticker in sp500_tickers[:]:
        try:
            rate = get_return(ticker, length)
            if rate >= sp500:
                count += 1
                print(ticker, rate)
            res.append([rate, ticker])
        except Exception as e:
            print("error", e)
    print("over sp500 ", count)
    pick_count = 0
    avg_list = []
    for _ in range(100):
        pick = []
        for _ in range(10):
            pick.append(random.choice(res))
        avg = sum([i[0] for i in pick]) / len(pick)
        if avg > sp500:
            print(pick, avg)
            pick_count += 1
        avg_list.append(avg)
    print("pick over ^GSPC", pick_count / 100)
    print(sorted(avg_list, reverse=True))

