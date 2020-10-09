import pandas as pd
import os

from src.MetricHandler import create_sharpe_ratio
from src.MetricHandler import create_drawdowns 
from src.Events import SignalEvent
from src.Events import OrderEvent
from src.Events import FillEvent

class Portfolio:
    def __init__(self, data_handler, events, start_date, initial_capital):
        self.events = events 
        self.bar_handler = data_handler
        self.start_date = start_date
        self.initial_capital = initial_capital
        self.equity_curve = pd.DataFrame()

        # overall position
        # ================
        self.all_positions = self.init_all_positions()
        self.all_holdings = self.init_all_holdings()
        
        # instantaneous position
        # ================
        self.current_positions = {symbol:0 for symbol in self.bar_handler.symbol_list}
        self.current_holdings = self.init_current_holdings()

        # print(f"H: {self.all_holdings},h: {self.current_holdings}")
        # print(f"P: {self.all_positions},p {self.current_positions}")

    def init_all_positions(self):
        positions = {symbol:0 for symbol in self.bar_handler.symbol_list}
        positions["datetime"] = self.start_date
        return [positions]
    
    def init_all_holdings(self):
        holdings = {symbol:0.0 for symbol in self.bar_handler.symbol_list}
        holdings["datetime"] = self.start_date
        holdings["cash"] = self.initial_capital
        holdings["commission"] = 0.0
        holdings["total"] = self.initial_capital
        return [holdings]
    
    def init_current_holdings(self):
        holdings = {symbol:0.0 for symbol in self.bar_handler.symbol_list}
        holdings["cash"] = self.initial_capital
        holdings["comission"] = 0.0
        holdings["total"] = self.initial_capital
        return holdings
    
    def update_timeindex(self, events):
        # new MarketEvent
        latest_datetime = self.bar_handler.get_latest_bar_datetime(self.bar_handler.symbol_list[0])
        
        # positions updt (cur && all)    
        # ==========================
        positions = {symbol:self.current_positions[symbol] for symbol in self.bar_handler.symbol_list}
        positions["datetime"] = latest_datetime
        self.all_positions.append(positions)

        # holdings updt (cur && all)
        # ==========================
        holdings = {symbol:0.0 for symbol in self.bar_handler.symbol_list}
        holdings["datetime"] = latest_datetime
        holdings["cash"] = self.current_holdings["cash"]
        holdings["comission"]  = self.current_holdings["comission"]
        holdings["total"] = self.current_holdings["cash"]

        for symbol in self.bar_handler.symbol_list:
            market_value = self.current_positions[symbol]*self.bar_handler.get_latest_bar_value(symbol, "adj_close")
            holdings["total"]+=market_value

        self.all_holdings.append(holdings)
     
    def update_signal(self, event):
         if isinstance(event, SignalEvent):
             order_event = self.generate_naive_order(event)
             self.events.put(order_event)
    
    def generate_naive_order(self, signalObject):
        signal = signalObject
        order = None
        symbol = signal.symbol
        direction  = signal.signal_type
        strength = signal.strength
        order_qty  = 100 
        order_type = "MKT"  
        
        # TO DO: sizing function
        # ======================
        # pass margin parameters from main 
        # qty = sizing_function(current price, margin)

        current_qty = self.current_positions[symbol]

        if direction == "LONG" and current_qty == 0:
            order = OrderEvent(symbol, order_type, order_qty, "LONG")
        if direction == "EXIT" and current_qty > 0:
            order = OrderEvent(symbol, order_type, order_qty, "SELL")
        if direction == "SHORT" and current_qty == 0:
            order = OrderEvent(symbol, order_type, order_qty, "SHORT")
        if direction == "EXIT" and current_qty < 0:
            order = OrderEvent(symbol, order_type, order_qty, "COVER")
        return order

    def update_fill(self, event):
        if isinstance(event, FillEvent):
            self.update_current_positions_after_fill(event)
            self.update_current_holdings_after_fill(event)

    def update_current_positions_after_fill(self, fillObject):
        fill = fillObject
        fill_direction = 0
        if fill.direction == "LONG":
            fill_direction = 1
        if fill.direction == "SELL":
            fill_direction = -1
        if fill.direction == "SHORT":
            fill_direction = -1
        if fill.direction == "COVER":
            fill_direction = 1
        self.current_positions[fill.symbol]+=fill_direction*fill.quantity
    
    def update_current_holdings_after_fill(self, fillObject):
        fill = fillObject
        fill_direction = 0
        if fill.direction == "LONG":
            fill_direction = 1
        if fill.direction == "SELL":
            fill_direction = -1
        if fill.direction == "SHORT":
            fill_direction = -1
        if fill.direction == "COVER":
            fill_direction = 1
        fill_cost = self.bar_handler.get_latest_bar_value(fill.symbol, "adj_close")*fill.quantity*fill_direction
        self.current_holdings[fill.symbol]+=fill_cost
        self.current_holdings["comission"]+= fill.comission
        self.current_holdings["cash"]-= (fill_cost+fill.comission)
        self.current_holdings["total"]-= (fill_cost+fill.comission)
    
    def create_equity_curve_dataframe(self):
        equity_curve = pd.DataFrame(self.all_holdings)
        equity_curve.set_index("datetime",inplace=True)
        equity_curve["returns"] = equity_curve["total"].pct_change()
        equity_curve["equity_curve"] = (1.0 + equity_curve["returns"]).cumprod()
        self.equity_curve = equity_curve

    def output_summary_stats(self):
        stats = {}
        total_return = self.equity_curve["equity_curve"][-1]
        returns = self.equity_curve["returns"]
        pnl = self.equity_curve["equity_curve"]
        sharpe_ratio = create_sharpe_ratio(returns, periods=252*60*6.5)
        drawdown, max_dd, max_dd_duration = create_drawdowns(pnl)
        # print(f"max_dd:{max_dd}")
        self.equity_curve["drawdown"] = drawdown
        stats["Return"] = (total_return - 1)*100.0
        stats["Sharpe"] = sharpe_ratio
        stats["Drawdown"] = max_dd*100
        stats["Drawdown Period"] = max_dd_duration
        data_dir = os.getcwd()+"/data/equity.csv"
        print(data_dir)
        self.equity_curve.to_csv(data_dir)
        return stats
        