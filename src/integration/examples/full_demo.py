import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)

from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget
from src.integration.agent import IntegrationSmartAgent

# demo.py + demo_agent.py
def run_demo():
    # Создаём тестовый источник
    source_data = {
        'characteristics': {
            'data_volume': 1,    # средний объем (1.2)
            'api_complexity': 2, # сложный API (1.6)
            'data_quality': 0    # высокое качество (1.0)
        },
        'current_progress': {
            'step': 'step3',     # текущий шаг
            'days_spent': 4      # потрачено дней
        }
    }

    # Базовый прогноз
    predictor = IntegrationPredictor()
    prediction = predictor.predict_completion(source_data)
    
    # Проверяем цель
    target = IntegrationTarget()
    result = target.calculate_target(prediction['estimated_days'])
    
    # Анализ агента
    agent = IntegrationSmartAgent()
    analysis = agent.analyze_integration('source_123')
    action = agent.redistribute_resources(analysis['prediction'])

    print(f"""
    Базовый прогноз:
    - Ожидаемое время: {prediction['estimated_days']:.1f} дней
    - Статус: {prediction['warning_status']}
    - Сложность: {prediction['complexity_factor']:.2f}
    - Вероятность уложиться в срок: {result['completion_rate']*100:.1f}%
    
    Анализ агента:
    - Риски: {analysis['risks']}
    - Статус ресурсов: {analysis['resource_status']}
    - Рекомендуемые действия: {analysis['recommendations']}
    - Выбранное действие: {action}
    """)

if __name__ == '__main__':
    run_demo()
