from typing import Dict
from .base import IntegrationHandler
from ..models.factor import FactorAnalysis

class FactorHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.factor_analysis = FactorAnalysis()
        
    def handle(self, data: Dict) -> Dict:
        complexity = self.factor_analysis.calculate_multiplier(data['characteristics'])
        data['factor_analysis'] = {'complexity': complexity}
        return super().handle(data)
