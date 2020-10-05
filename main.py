import os
from datetime import datetime

from src.Engine import BacktestEngine
from src.DataHandler import CsvHandler
from src.ExecutionHandler import SimpleHandler
from src.Portfolio import Portfolio

from model.Scalper import Scalper

if __name__ == "__main__":
    data_dir = os.getcwd + "/data"
    symbol = ['ETHUSDT']
    initial_capital = 100.0
    start_date = datetime(2010,1,1)
    hearbeat = 0.0

    run = BacktestEngine(data_dir,
                         symbol_list,
                         initial_capital,
                         heartbeat,
                         start_data,
                         CsvHandler,
                         SimpleHandler,
                         Portfolio,
                         Scalper)

    run.simulate_trading()



    
