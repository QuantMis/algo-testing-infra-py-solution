import os
from datetime import datetime

from src.Engine import BacktestEngine
from src.DataHandler import CsvHandler
from src.ExecutionHandler import SimpleExecutionHandler
from src.Portfolio import Portfolio
from src.Visualize import Visualize

from model.HelloWorldStrat import HelloWorldStrat

if __name__ == "__main__":
    data_dir = os.getcwd() + "/data"
    symbol_list = ['AAPL','GOOG']
    initial_capital = 100.0
    start_date = datetime(2010,1,1)
    heartbeat = 0.0

    run = BacktestEngine(data_dir,
                         symbol_list,
                         initial_capital,
                         heartbeat,
                         start_date,
                         CsvHandler,
                         SimpleExecutionHandler,
                         Portfolio,
                         HelloWorldStrat)

    run.simulate_trading()
    Visualize(data_dir)




    
