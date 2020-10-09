from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def _calculate_signals(self):
        raise NotImplementedError("Should Implement _calculate_signals")