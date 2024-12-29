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
                'data_volume': 2,        # Большой объем
                'api_complexity': 2,     # Сложный API
                'data_quality': 0,       # Низкое качество
                'current_step': 2,       # Шаг 2
                'days_spent': 8,         # Потрачено дней
                'completion_time': 45    # Итоговое время
            },
            {   
                'data_volume': 1,        # Средний объем
                'api_complexity': 1,     # Средний API
                'data_quality': 1,       # Среднее качество
                'current_step': 2,
                'days_spent': 5,
                'completion_time': 25
            },
            {
                'data_volume': 0,        # Малый объем
                'api_complexity': 0,     # Простой API
                'data_quality': 2,       # Высокое качество
                'current_step': 2,
                'days_spent': 4,
                'completion_time': 20
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
            # Нормализуем предсказание в вероятность от 0 до 1
            normalized_prob = min(pred / 30.0, 1.0)  # 30 дней - целевое время
            patterns.append({
                'risk_level': float(pred),
                'risk_type': 'schedule_risk' if pred > 0.7 else 'normal',
                'probability': normalized_prob
            })
        return patterns

    def train(self, historical_data: List[Dict]) -> None:
        X = pd.DataFrame(historical_data)[self.feature_columns]
        y = pd.DataFrame(historical_data)['completion_time']
        self.model.fit(X, y)
        
    def estimate_delay(self, risk_pattern: Dict, current_step: int) -> float:
        # Получаем оставшиеся шаги
        remaining_steps = 7 - current_step
        # Среднее время на шаг из settings
        avg_step_time = 5  
        # Максимальная возможная задержка для оставшихся шагов
        max_delay = remaining_steps * avg_step_time
        return risk_pattern['probability'] * max_delay

    def estimate_resource_needs(self, risk_pattern: Dict, current_step: int) -> float:
        # Получаем оставшиеся шаги
        remaining_steps = 7 - current_step
        # Среднее время на шаг из settings
        avg_step_time = 5  
        # Максимальная возможная задержка для оставшихся шагов
        max_delay = remaining_steps * avg_step_time
        return risk_pattern['probability'] * max_delay

    def estimate_quality_risk(self, risk_pattern: Dict) -> float:
        return risk_pattern['probability'] * 0.9

    def calculate_impact(self, risk_pattern: Dict, current_step: int) -> Dict:
        return {
            'schedule_impact': self.estimate_delay(risk_pattern, current_step),
            'resource_impact': self.estimate_resource_needs(risk_pattern, current_step),
            'quality_impact': self.estimate_quality_risk(risk_pattern)
        }
    
    def suggest_mitigation(self, risk_pattern: Dict, current_step: int) -> List[str]:
        impact = self.calculate_impact(risk_pattern, current_step)
        mitigations = []
        
        if impact['schedule_impact'] > 5:
            mitigations.append("Добавить опытных разработчиков")
        if impact['resource_impact'] > 0.7:
            mitigations.append("Оптимизировать распределение ресурсов")
        if impact['quality_impact'] > 0.8:
            mitigations.append("Усилить контроль качества")
            
        return mitigations
