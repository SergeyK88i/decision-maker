from typing import Dict
from .base import IntegrationHandler
from ..target import IntegrationTarget

class TargetHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.target = IntegrationTarget()
        
    def handle(self, data: Dict) -> Dict:
        probability = self.target.calculate_completion_probability(data)
        data['completion_probability'] = probability
        return super().handle(data)
