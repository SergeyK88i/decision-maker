from typing import Dict
from .base import IntegrationHandler
from ..predictor import IntegrationPredictor

class PredictorHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.predictor = IntegrationPredictor()
        
    def handle(self, data: Dict) -> Dict:
        prediction = self.predictor.predict_completion(data)
        data['prediction'] = prediction
        return super().handle(data)
