import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)

from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget
from src.integration.agent.smart_agent import IntegrationSmartAgent
from src.integration.agent.ml_predictor import MLPredictor

def run_demo():
    # Создаем ML предиктор для умного анализа
    ml_predictor = MLPredictor()
    
    # Тестовые данные
    source_data = {
        'characteristics': {
            'data_volume': 2,        # Большой объем данных
            'api_complexity': 2,     # Сложный API
            'data_quality': 1        # Среднее качество
        },
        'current_progress': {
            'step': 'step3',
            'days_spent': 4,
            'steps_history': {
                'step1': 4,         # факт выполнения
                'step2': 9          # факт выполнения
            },
            'available_parallel_steps': ['step2', 'step3'],         # шаги, которые можно выполнять параллельно
            'active_parallel_steps': ['step2','step3'],              # шаги, которые сейчас выполняются параллельно
            'steps_time': {
                'step2': 3,
                'step3': 10                                  # время только активного шага
            },
            'steps_dependencies': {
                'step1': [],
                'step2': ['step1'],
                'step3': ['step1'],
                'step4': ['step2', 'step3'],
                'step5': ['step4'],
                'step6': ['step4'],
                'step7': ['step5', 'step6']
            }
        }
    }
    # Получаем стандартный прогноз
    predictor = IntegrationPredictor()
    prediction = predictor.predict_completion(source_data)

    # Получаем умный анализ
    features = ml_predictor.extract_features(source_data)
    patterns = ml_predictor.analyze_patterns(source_data)
    # Получаем текущий шаг из source_data
    current_step = int(source_data['current_progress']['step'].replace('step', ''))

    impact = ml_predictor.calculate_impact(patterns[0], current_step)

    # Создаем агента для комплексного анализа
    agent = IntegrationSmartAgent()
    analysis = agent.analyze_integration(source_data)
    action = agent.redistribute_resources(analysis['prediction'])

    print(f"""
    Умный анализ интеграции:
    1. Характеристики:
       - Объем данных: {features['data_volume'][0]} (высокий)
       - Сложность API: {features['api_complexity'][0]} (сложный)
       - Качество данных: {features['data_quality'][0]} (среднее)

    2. Риски:
       - Уровень риска: {patterns[0]['risk_level']:.2f}
       - Тип риска: {patterns[0]['risk_type']}
       - Вероятность: {patterns[0]['probability']:.2f}

    3. Влияние:
       - На сроки: {impact['schedule_impact']:.1f} дней задержки
       - На ресурсы: {impact['resource_impact']:.1f}x нагрузка
       - На качество: {impact['quality_impact']:.1f}x риск ошибок

    4. Рекомендации агента:
       - Прогноз: {analysis['prediction']}
       - Риски: {analysis['risks']}
       - Статус ресурсов: {analysis['resource_status']}
       - Действия: {analysis['recommendations']}
       - Выбранное действие: {action}
    """)

if __name__ == '__main__':
    run_demo()
