from abc import ABC, abstractmethod
from datetime import datetime

from src.Events import OrderEvent
from src.Events import FillEvent

class Execution(ABC):
    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError("Should Implement execute_order")

class SimpleExecutionHandler(Execution):
    def __init__(self, events):
        self.events = events

    def execute_order(self, event):
        if isinstance(event,OrderEvent):
            fill_event = FillEvent(datetime.utcnow(), event.symbol, "ARCA", event.quantity, event.direction, None)
            self.events.put(fill_event)