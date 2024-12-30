import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from typing import List, Dict
from ..utils.calculations import load_settings

class MLPredictor:
    def __init__(self):
        self.settings = load_settings()
        self.model = RandomForestRegressor()
        self.feature_columns = [
            'data_volume',
            'api_complexity',
            'data_quality',
            'current_step',
            'days_spent',
            'parallel_steps_count' 
        ]
        # Initial training data
        initial_data = [
            {
                'data_volume': 2,        # Большой объем
                'api_complexity': 2,     # Сложный API
                'data_quality': 0,       # Низкое качество
                'current_step': 2,       # Шаг 2
                'days_spent': 8,         # Потрачено дней
                'completion_time': 45,    # Итоговое время
                'parallel_steps_count': 0
            },
            {   
                'data_volume': 1,        # Средний объем
                'api_complexity': 1,     # Средний API
                'data_quality': 1,       # Среднее качество
                'current_step': 2,
                'days_spent': 5,
                'completion_time': 25,
                'parallel_steps_count': 0
            },
            {
                'data_volume': 0,        # Малый объем
                'api_complexity': 0,     # Простой API
                'data_quality': 2,       # Высокое качество
                'current_step': 2,
                'days_spent': 4,
                'completion_time': 20,
                'parallel_steps_count': 0
            }
        ]
        self.train(initial_data)

    def extract_features(self, source_data: Dict) -> pd.DataFrame:
        active_steps = source_data['current_progress']['active_parallel_steps']
        steps_time = source_data['current_progress'].get('steps_time', {})
    
        features = {
            'data_volume': source_data['characteristics']['data_volume'],
            'api_complexity': source_data['characteristics']['api_complexity'],
            'data_quality': source_data['characteristics']['data_quality'],
            # Берем максимальный номер шага из активных
            'current_step': max(int(''.join(filter(str.isdigit, step))) for step in active_steps),
            # Берем максимальное время из активных шагов
            'days_spent': max(steps_time.get(step, 0) for step in active_steps),
            'parallel_steps_count': len(source_data['current_progress'].get('active_parallel_steps', []))
        }
        return pd.DataFrame([features])

    def analyze_patterns(self, source_data: Dict) -> List[Dict]:
        features = self.extract_features(source_data)
        predictions = self.model.predict(features)
        return self.convert_predictions_to_patterns(predictions)

    def convert_predictions_to_patterns(self, predictions) -> List[Dict]:
        patterns = []
        for pred in predictions:
            # Используем сигмоиду для нормализации вероятности
            normalized_prob = 1 / (1 + np.exp(-0.1 * (pred - 30)))
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
        steps = self.settings['integration']['steps']
        # Преобразуем current_step в число, если это строка
        if isinstance(current_step, str):
            current_step = int(current_step.replace('step', ''))
        
        remaining_steps = {
            k: v for k, v in steps.items() 
            if int(k.replace('step', '')) > current_step
        }
        
        total_remaining_time = sum(remaining_steps.values())
        return risk_pattern['probability'] * total_remaining_time

    def get_step_time(self, step: int) -> int:
        step_key = f'step{step}'
        return self.settings['integration']['steps'][step_key]

    def estimate_resource_needs(self, risk_pattern: Dict, current_step: int) -> float:
        steps = self.settings['integration']['steps']
    
        # Преобразуем current_step в число, если это строка
        if isinstance(current_step, str):
            current_step = int(current_step.replace('step', ''))
            
        remaining_steps = {
            k: v for k, v in steps.items() 
            if int(k.replace('step', '')) > current_step
        }
    
        total_remaining_time = sum(remaining_steps.values())
        return risk_pattern['probability'] * total_remaining_time

    def estimate_quality_risk(self, risk_pattern: Dict) -> float:
        return risk_pattern['probability'] * 0.9

    def calculate_impact(self, risk_pattern: Dict, current_step: int) -> Dict:
        # Получаем веса для текущего шага
        step_weights = {
            'schedule': self.settings['factors']['weights']['data_volume'],
            'resource': self.settings['factors']['weights']['api_complexity'],
            'quality': self.settings['factors']['weights']['data_quality']
        }
        return {
            'schedule_impact': self.estimate_delay(risk_pattern, current_step) * step_weights['schedule'],
            'resource_impact': self.estimate_resource_needs(risk_pattern, current_step) * step_weights['resource'],
            'quality_impact': self.estimate_quality_risk(risk_pattern) * step_weights['quality']
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
