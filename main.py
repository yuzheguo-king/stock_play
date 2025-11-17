
import utils
import stock_info
import threading
import pickle

FILE_NAME = "sp500_stock_info.pkl"

def save_data(ticker_list: list):
    data_dict = {}
    for ticker in ticker_list:
        info = stock_info.StockInfo(ticker)
        if info is not None:
            data_dict[ticker] = info
            print(f"Initialized data for {ticker}")

    with open(FILE_NAME, 'wb') as f:
        pickle.dump(data_dict, f)
    

def init_data(ticker_list: list, res_dict: dict)->dict:
    data_dict = {}
    for ticker in ticker_list:
        info = stock_info.StockInfo(ticker)
        if info is not None:
            data_dict[ticker] = info
            print(f"Initialized data for {ticker}")
    res_dict = res_dict | data_dict
    print(res_dict.keys())
    return res_dict

if __name__ == "__main__":
    print("starting to calculate stock info")
    sp500_tickers = utils.StockUtils.get_sp500_company_tickers()

    save_data(sp500_tickers[:3])

    with open(FILE_NAME, 'rb') as f:
        data_dict = pickle.load(f)
    print(data_dict.values())

    # time = "2025-11-08"
    # low_price_stocks = utils.StockUtils.filter_low_price_stock(time, sp500_tickers)
    # print("Stocks with price below 52-week average:")
    # print(low_price_stocks)
    # growth_stocks = utils.StockUtils.filter_growth_stock(time, sp500_tickers)
    # print("Stocks with 1-year return above S&P 500:")