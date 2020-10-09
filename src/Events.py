class Event:
    pass

class MarketEvent(Event):
    def __init__(self):
        self.type = "MARKET"

class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type, strength):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength

class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity, direction):
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
    
    def print_order(self):
        print(f"Order: Symbol: {self.symbol}, Type: {self.order_type}, Qty: {self.quantity}, Direction: {self.direction}")

class FillEvent(Event):
    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=None):
        self.type = "FILL"
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        
        if commission is None:
            self.comission = 0 # self.calculate_commision()
        else:
            self.commission = commission


