#%%
import yfinance as yf
from stock_info import StockInfo
import pandas as pd

def filter_low_price_stock(time, cand: list)->list:
    res = []
    for ticker in cand:
        info = StockInfo(ticker)
        if info.get_price(time) < info.get_52_week_avg(time):
            res.append(ticker)
    return res

def filter_growth_stock(time, cand: list)->list:
    res = []
    sp500 = StockInfo("VOO")
    for ticker in cand:
        info = StockInfo(ticker)
        if info.get_last_year_return(time) > sp500.get_last_year_return(time):
            res.append(ticker)
    return res

def get_sp500_company_tickers()->list:
    return pd.read_csv("sp500_list.csv")["Symbol"].to_list()

#%%
get_sp500_company_tickers()
# %%
