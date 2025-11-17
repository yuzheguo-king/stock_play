#%%
import yfinance as yf
import datetime

class StockInfo:
    def __init__(self, ticker: str):
        try:
            self.ticker = ticker
            self.history_data = yf.Ticker(ticker).history(period="max", interval="1d")
            self.start_time = self.history_data.index[0].strftime("%Y-%m-%d")
            self.end_time = self.history_data.index[-1].strftime("%Y-%m-%d")
            self.dividend_data = self.history_data[self.history_data["Dividends"] > 0][["Dividends", "Close"]]
        except Exception as e:
            print(f"Error initializing StockInfo for {ticker}: {e}")
            return None
    def __convert_to_datetime(self, time: str):
        year, month, day = self.__parse_year_month_day(time)
        return datetime.datetime(year, month, day)
    
    def __parse_year_month_day(self, time: str):
        segs = time.split("-")
        year = int(segs[0])
        month = int(segs[1])
        day = int(segs[2])
        return year, month, day
    # time format "YYYY-MM-DD"
    def get_price(self, time: str):
        datetime_time = self.__convert_to_datetime(time)
        if datetime_time < self.__convert_to_datetime(self.start_time):
            return self.history_data.iloc[0]['Close']
        if datetime_time > self.__convert_to_datetime(self.end_time):
            return self.history_data.iloc[-1]['Close']

        try_count = 7
        while try_count > 0:
            try:
                price = self.history_data.loc[datetime_time.strftime("%Y-%m-%d")]
                return price['Close']
            except Exception as e:
                datetime_time += datetime.timedelta(days=1)
                try_count -= 1
        raise Exception(f"cannot find price for {self.ticker} at {time}")

    def get_52_week_high(self, time: str):
        datetime_time = self.__convert_to_datetime(time)
        start_date = datetime_time - datetime.timedelta(weeks=52)
        data_52_week = self.history_data.loc[start_date.strftime("%Y-%m-%d"):datetime_time.strftime("%Y-%m-%d")]
        return data_52_week['Close'].max()

    def get_52_week_low(self, time: str):
        datetime_time = self.__convert_to_datetime(time)
        start_date = datetime_time - datetime.timedelta(weeks=52)
        data_52_week = self.history_data.loc[start_date.strftime("%Y-%m-%d"):datetime_time.strftime("%Y-%m-%d")]
        return data_52_week['Close'].min()

    def get_52_week_avg(self, time: str):
        return (self.get_52_week_high(time) + self.get_52_week_low(time)) / 2

    def get_return_without_dividend(self, start_time: str, end_time: str):
        start_price = self.get_price(start_time)
        end_price = self.get_price(end_time)
        return (end_price - start_price) / start_price
    
    def get_last_year_return(self, time: str):
        current_price = self.get_price(time)
        last_year_date = datetime.datetime.strptime(time, "%Y-%m-%d") - datetime.timedelta(days=365)
        return self.get_return_without_dividend(last_year_date.strftime("%Y-%m-%d"), time)

    def get_return_with_dividend_reinvested(self, start_time: str, end_time: str):
        initial_shares = 1.0
        shares = self.get_share_increase_with_dividend(start_time, end_time)
        start_price = self.get_price(start_time)
        end_price = self.get_price(end_time)
        return (end_price * shares - start_price * initial_shares) / (start_price * initial_shares)

    def get_share_increase_with_dividend(self, start_time: str, end_time: str):
        datetime_start = self.__convert_to_datetime(start_time)
        datetime_end = self.__convert_to_datetime(end_time)
        data_in_range = self.dividend_data.loc[datetime_start.strftime("%Y-%m-%d"):datetime_end.strftime("%Y-%m-%d")]
        shares = 1.0
        for index, row in data_in_range.iterrows():
            dividend_per_share = row['Dividends']
            close_price = row['Close']
            total_dividend = dividend_per_share * shares
            additional_shares = total_dividend / close_price
            shares += additional_shares
        return shares

# %%

# stock = StockInfo("VOO")
# print(stock.get_price("2025-11-08"))
# print(stock.get_52_week_high("2025-11-08"))
# print(stock.get_52_week_low("2025-11-08"))
# print(stock.get_return_with_dividend_reinvested("2024-11-08", "2025-11-08"))
# print(stock.get_return_without_dividend("2024-11-08", "2025-11-08"))
# print("stock info")
# apple_stock = yf.Ticker("AAPL")
# data = apple_stock.history(period="10y", interval="1d")
# print(data[data["Dividends"] > 0][["Dividends", "Close"]])



# # %%
# end_time = datetime(2025, 11, 16)
# start_time = datetime(2025, 11, 1)
# data = stock.history(perod='max', interval='1d')
# # %%
# data.head(30)
# # %%
# data.loc['2025-11-16']['Close']
# # %%
# stock.history(start=start_time, end=end_time)
# # %%

# %%
