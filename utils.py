#%%
import yfinance as yf
from stock_info import StockInfo
import pandas as pd
from datetime import date, datetime, timedelta
from typing import Iterable, Optional, Union, Set, List


class StockUtils:
    """Utility class for stock analysis and data filtering operations."""

    @staticmethod
    def filter_low_price_stock(time: str, cand: List[str]) -> List[str]:
        """
        Filter stocks with price below their 52-week average.

        Parameters:
        - time: date string for the specific time period
        - cand: list of stock tickers to filter

        Returns:
        - list of tickers with price < 52-week average
        """
        res = []
        for ticker in cand:
            info = StockInfo(ticker)
            if info.get_price(time) < info.get_52_week_avg(time):
                res.append(ticker)
        return res

    @staticmethod
    def filter_growth_stock(time: str, cand: List[str]) -> List[str]:
        """
        Filter stocks with higher 1-year return than S&P 500 (VOO).

        Parameters:
        - time: date string for the specific time period
        - cand: list of stock tickers to filter

        Returns:
        - list of tickers with 1-year return > S&P 500 return
        """
        res = []
        sp500 = StockInfo("VOO")
        for ticker in cand:
            info = StockInfo(ticker)
            if info.get_last_year_return(time) > sp500.get_last_year_return(time):
                res.append(ticker)
        return res

    @staticmethod
    def get_sp500_company_tickers() -> List[str]:
        """
        Retrieve list of S&P 500 company tickers from CSV file.

        Returns:
        - list of stock tickers
        """
        return pd.read_csv("sp500_list.csv")["Symbol"].to_list()