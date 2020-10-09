import pandas as pd
import numpy as np
import os, os.path
from abc import ABC, abstractmethod

from src.Events import MarketEvent

class DataManagement(ABC):
    
    @abstractmethod
    def get_latest_bar(self, symbol):
        raise NotImplementedError("get_latest_bar() not implemented!")
    
    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        raise NotImplementedError("get_latest_bars() not implemented!")
    
    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        raise NotImplementedError("get_latest_bar_datetime() not implemented!")
    
    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
        raise NotImplementedError("get_latest_bar_value() not implemented!")

    @abstractmethod
    def get_latest_bar_values(self, symbol, val_type,N=1):
        raise NotImplementedError("get_latest_bar_values() not implemented!")
    
    @abstractmethod
    def update_bars(self, symbol):
        raise NotImplementedError("update_bars() not implemented!")

class CsvHandler(DataManagement):
    
    def __init__(self, events, data_dir, symbol_list):
        self.events = events
        self.data_dir = data_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self._data_conversion_from_csv_files()
    
    def _data_conversion_from_csv_files(self):
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = pd.io.parsers.read_csv(
                                    os.path.join(self.data_dir, f"{symbol}.csv"),
                                    header=0, index_col=0,
                                    names = ["datetime","open","high","low","close","adj_close","volume"])
            combined_index = self.symbol_data[symbol].index
            self.latest_symbol_data[symbol] = []

        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()                            

    def _get_new_bar(self, symbol):
        for bar in self.symbol_data[symbol]:
            yield bar

    def get_latest_bar(self, symbol):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("Symbol dont exist.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("Symbol dont exist.")
            raise
        else:
            return bars_list[-N]
    
    def get_latest_bar_datetime(self, symbol):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("Symbol dont exist.")
            raise
        else:
            return bars_list[-1][0]
        
    def get_latest_bar_value(self, symbol, val_type):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("Symbol dont exist.")
            raise
        else:
            return getattr(bars_list[-1][1], val_type)
    
    def get_latest_bar_values(self, symbol, val_type, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("Symbol dont exist.")
            raise
        else:
            return [getattr(bar[1],val_type) for bar in bars_list]
                 
    def update_bars(self): 
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())


# unit test 

# def _data_conversion_from_csv_files_test(data_dir, symbol_list, symbol_data, latest_symbol_data):
#     for symbol in symbol_list:
#         symbol_data[symbol] = pd.io.parsers.read_csv(
#                             os.path.join(data_dir, f"{symbol}.csv"),
#                             header=0, index_col=0,
#                             names = ["datetime","open","high","low","close","adj_close","volume"])
#         # print(symbol_data[symbol])
#         combined_index = symbol_data[symbol].index
#         latest_symbol_data = []

#         symbol_data[symbol] = symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()
    
#     for bar in symbol_data['AAPL']:
#         yield bar


if __name__ == "__main__":
    data_dir = "/home/lenovo/Desktop/repo/algo-testing-infra-py-solution/data"
    symbol_list = ['AAPL','GOOG']
    symbol_data = {}
    latest_symbol_data = {}
    bar = _data_conversion_from_csv_files_test(data_dir, symbol_list, symbol_data, latest_symbol_data)
    bar = next(bar)
    latest = []
    latest.append(bar)
    print(latest[-1][1]['open'])
    print(getattr(latest[-1][1],"open"))