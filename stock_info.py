class StockInfo:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ticker_data = yf.Ticker(ticker)
    
    def get_price(time: str):
        pass

    def get_52_week_high(time: str):
        pass
    def get_52_week_low(time: str):
        pass
    def get_52_week_avg(time: str):
        pass
    def get_last_year_return(time: str):
        pass