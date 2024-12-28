from typing import Dict

class FactorAnalysis:
    def __init__(self):
        self.factors = {
            'data_volume': {0: 1.0, 1: 1.2, 2: 1.5},
            'api_complexity': {0: 1.0, 1: 1.3, 2: 1.6},
            'data_quality': {0: 1.0, 1: 1.2, 2: 1.4}
        }
    
    def calculate_multiplier(self, characteristics: Dict) -> float:
        multiplier = 1.0
        for factor, value in characteristics.items():
            if factor in self.factors:
                multiplier *= self.factors[factor][value]
        return multiplier
