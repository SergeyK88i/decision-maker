import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)
from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget

def run_demo():
    # Создаём тестовый источник
    source_data = {
        'characteristics': {
            'data_volume': 1,
            'api_complexity': 2,
            'data_quality': 0
        },
        'current_progress': {
            'step': 'step2',
            'days_spent': 4
        }
    }

    # Получаем прогноз
    predictor = IntegrationPredictor()
    prediction = predictor.predict_completion(source_data)

    # Проверяем цель
    target = IntegrationTarget()
    result = target.calculate_target(prediction['estimated_days'])

    print(f"""
    Прогноз интеграции:
    - Ожидаемое время: {prediction['estimated_days']:.1f} дней
    - Статус: {prediction['warning_status']}
    - Сложность: {prediction['complexity_factor']:.2f}
    - Вероятность уложиться в срок: {result['completion_rate']*100:.1f}%
    """)

if __name__ == '__main__':
    run_demo()
