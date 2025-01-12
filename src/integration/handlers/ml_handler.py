from typing import Dict
from .base import IntegrationHandler
from ..agent.ml_predictor import MLPredictor

class MLPredictorHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.ml_predictor = MLPredictor()
        
    def handle(self, data: Dict) -> Dict:
        patterns = self.ml_predictor.analyze_patterns(data)
        data['ml_analysis'] = patterns
        return super().handle(data)
