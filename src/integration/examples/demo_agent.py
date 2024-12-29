import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)

from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget
from src.integration.agent.smart_agent import IntegrationSmartAgent
from src.integration.agent.resource_manager import ResourceManager

def run_demo():
    
    
    # Тестовый источник
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

    # Инициализация агента
    agent = IntegrationSmartAgent()

     # Получаем прогноз
    predictor = IntegrationPredictor()
    prediction = predictor.predict_completion(source_data)
    
    # Проверяем цель
    target = IntegrationTarget()
    result = target.calculate_target(prediction['estimated_days'])
    
    # Получаем анализ от агента
    analysis = agent.analyze_integration(source_data)
    
    # Проверяем необходимость перераспределения ресурсов
    action = agent.redistribute_resources(analysis['prediction'])
    
    print(f"""
    Анализ интеграции:
    - Прогноз: {analysis['prediction']}
    - Риски: {analysis['risks']}
    - Статус ресурсов: {analysis['resource_status']}
    - Рекомендуемые действия: {analysis['recommendations']}
    - Выбранное действие: {action}
    """)

if __name__ == '__main__':
    run_demo()
