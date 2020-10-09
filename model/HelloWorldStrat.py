import datetime
import numpy as np

from src.StrategyABC import Strategy 
from src.Events import MarketEvent
from src.Events import SignalEvent

class HelloWorldStrat(Strategy):
    def __init__(self, bar_handler, events):
        self.bar_handler = bar_handler
        self.event = events
        
        self.short_window = 100
        self.long_window = 300
        self.bought = self.calculate_initial_bought()

    def calculate_initial_bought(self):
        bought = {symbol: "FLAT" for symbol in self.bar_handler.symbol_list}
        return bought
    
    def _calculate_signals(self, event):
        if isinstance(event, MarketEvent):
            for symbol in self.bar_handler.symbol_list:
                bars = self.bar_handler.get_latest_bar_values(symbol, 'adj_close', N=self.long_window)
                # print(f"data: {bars[:100]}")
                bar_datetime = self.bar_handler.get_latest_bar_datetime(symbol)
                if bars is not None and bars != []:
                    try:
                        short_sma = np.mean(bars[:self.short_window])
                        long_sma = np.mean(bars[:self.long_window])

                        dt = datetime.datetime.utcnow()
                        signal_type = ""
                        strength = 1.0

                        if short_sma > long_sma and self.bought[symbol] == "FLAT":
                            signal_type = "LONG"
                            signal = SignalEvent(symbol, dt, signal_type, strength)
                            self.event.put(signal)
                            self.bought[symbol] =  "LONG"

                        elif short_sma < long_sma and self.bought[symbol] == "LONG":
                            signal_type = "EXIT"
                            signal = SignalEvent(symbol, dt, signal_type, strength)
                            self.event.put(signal)
                            self.bought[symbol] = "FLAT"                               
                    except IndexError:
                        pass


# unit test
if __name__ == "__main__":
    l = ['GEL','FURY','FUGUE']
    bought = {symbol: "OUT" for symbol in l}
    print(bought)
