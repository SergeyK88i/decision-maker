from typing import Dict, List
from .base import IntegrationHandler
from ..agent.ml_predictor import MLPredictor
from ..utils.calculations import analyze_parallel_risks, get_parallel_risk_status

class MLPredictorHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.ml_predictor = MLPredictor()
        
    def handle(self, data: Dict) -> Dict:
        patterns = self.ml_predictor.analyze_patterns(data)
        parallel_risks = self.analyze_parallel_risks(data)
        
        data['ml_analysis'] = {
            'patterns': patterns,
            'parallel_risks': parallel_risks,
            'risks': self.detect_risks(patterns)
        }
        return super().handle(data)

    def analyze_parallel_risks(self, data: Dict) -> Dict:
        risk = analyze_parallel_risks(
            data['current_progress']['active_parallel_steps'],
            data['current_progress']['steps_dependencies']
        )
        return {
            'risk_value': risk,
            'status': get_parallel_risk_status(risk)
        }

    def detect_risks(self, patterns: List[Dict]) -> List[Dict]:
        return [p for p in patterns if p['risk_level'] > 0.7]
