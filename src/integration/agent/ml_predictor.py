import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from typing import List, Dict

class MLPredictor:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.feature_columns = [
            'data_volume',
            'api_complexity',
            'data_quality',
            'current_step',
            'days_spent'
        ]
        # Initial training data
        initial_data = [
            {
                'data_volume': 1,
                'api_complexity': 2,
                'data_quality': 0,
                'current_step': 2,
                'days_spent': 4,
                'completion_time': 10
            },
            {
                'data_volume': 2,
                'api_complexity': 1,
                'data_quality': 1,
                'current_step': 3,
                'days_spent': 6,
                'completion_time': 15
            }
        ]
        self.train(initial_data)

    def extract_features(self, source_data: Dict) -> pd.DataFrame:
        features = {
            'data_volume': source_data['characteristics']['data_volume'],
            'api_complexity': source_data['characteristics']['api_complexity'],
            'data_quality': source_data['characteristics']['data_quality'],
            'current_step': int(source_data['current_progress']['step'].replace('step', '')),
            'days_spent': source_data['current_progress']['days_spent']
        }
        return pd.DataFrame([features])

    def analyze_patterns(self, source_data: Dict) -> List[Dict]:
        features = self.extract_features(source_data)
        predictions = self.model.predict(features)
        return self.convert_predictions_to_patterns(predictions)

    def convert_predictions_to_patterns(self, predictions) -> List[Dict]:
        patterns = []
        for pred in predictions:
            patterns.append({
                'risk_level': float(pred),
                'risk_type': 'schedule_risk' if pred > 0.7 else 'normal',
                'probability': float(pred)
            })
        return patterns

    def train(self, historical_data: List[Dict]) -> None:
        X = pd.DataFrame(historical_data)[self.feature_columns]
        y = pd.DataFrame(historical_data)['completion_time']
        self.model.fit(X, y)
        
    def estimate_delay(self, risk_pattern: Dict) -> float:
        return risk_pattern['probability'] * 10

    def estimate_resource_needs(self, risk_pattern: Dict) -> float:
        return risk_pattern['probability'] * 0.8

    def estimate_quality_risk(self, risk_pattern: Dict) -> float:
        return risk_pattern['probability'] * 0.9

    def calculate_impact(self, risk_pattern: Dict) -> Dict:
        return {
            'schedule_impact': self.estimate_delay(risk_pattern),
            'resource_impact': self.estimate_resource_needs(risk_pattern),
            'quality_impact': self.estimate_quality_risk(risk_pattern)
        }
    
    def suggest_mitigation(self, risk_pattern: Dict) -> List[str]:
        impact = self.calculate_impact(risk_pattern)
        mitigations = []
        
        if impact['schedule_impact'] > 5:
            mitigations.append("Добавить опытных разработчиков")
        if impact['resource_impact'] > 0.7:
            mitigations.append("Оптимизировать распределение ресурсов")
        if impact['quality_impact'] > 0.8:
            mitigations.append("Усилить контроль качества")
            
        return mitigations
