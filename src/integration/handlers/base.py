from abc import ABC, abstractmethod
from typing import Dict

class IntegrationHandler(ABC):
    def __init__(self):
        self._next_handler = None
        
    def set_next(self, handler):
        print(f"Setting next handler: {handler.__class__.__name__}")
        self._next_handler = handler
        return handler
        
    @abstractmethod
    def handle(self, data: Dict) -> Dict:
        if self._next_handler:
            return self._next_handler.handle(data)
        return data
