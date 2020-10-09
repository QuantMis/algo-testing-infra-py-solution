import queue
import time
import pprint

from src.Events import MarketEvent
from src.Events import SignalEvent
from src.Events import OrderEvent
from src.Events import FillEvent

class BacktestEngine:
    def __init__(self,
                data_dir,
                symbol_list,
                initial_capital,
                heartbeat,
                start_date,
                data_handler,
                execution_handler,
                portfolio,
                strategy):
                
    
        self.data_dir = data_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat
        self.start_date = start_date

        self.data_handler_cls = data_handler
        self.execution_handler_cls = execution_handler
        self.portfolio_cls = portfolio
        self.strategy_cls = strategy

        self.events = queue.Queue()
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

        self._generate_handler_instances()

    def _generate_handler_instances(self):
        self.data_handler = self.data_handler_cls(self.events,self.data_dir,self.symbol_list)
        self.strategy = self.strategy_cls(self.data_handler, self.events)
        self.portfolio = self.portfolio_cls(self.data_handler, self.events, self.start_date, self.initial_capital)
        self.execution_handler = self.execution_handler_cls(self.events)
    
    def _run_backtest(self):
        i = 0
        while True:
            i += 1;
            # print(i)
            if self.data_handler.continue_backtest==True:
                self.data_handler.update_bars()
            else:
                break

            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if isinstance(event, MarketEvent):
                            self.strategy._calculate_signals(event)
                            self.portfolio.update_timeindex(event) # breakpoint
                        
                        elif isinstance(event, SignalEvent):
                            self.signals += 1
                            self.portfolio.update_signal(event)
                        
                        elif isinstance(event, OrderEvent):
                            self.orders += 1
                            self.execution_handler.execute_order(event)
                        
                        elif isinstance(event, FillEvent):
                            self.fills += 1
                            self.portfolio.update_fill(event)
        
        time.sleep(self.heartbeat)

    def _output_performance(self):
        self.portfolio.create_equity_curve_dataframe()
        stats = self.portfolio.output_summary_stats()
        pprint.pprint(stats)
        print(f"Signals: {self.signals}")
        print(f"Orders: {self.orders}")
        print(f"Fills: {self.fills}")

    def simulate_trading(self):
        self._run_backtest()
        self._output_performance()



