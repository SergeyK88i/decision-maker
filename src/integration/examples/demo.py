import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)
from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget
from src.integration.utils.calculations import get_standard_time


def run_demo():
    # Создаём тестовый источник
    source_data = {
        'characteristics': {
            'data_volume': 0,       # средний объем (1.2)
            'api_complexity': 0,    # сложный API (1.6)
            'data_quality': 0       # высокое качество (1.0)
        },
        'current_progress': {
            # шаги, которые можно выполнять параллельно
            'available_parallel_steps': ['step3', 'step4'], 
            # текущий активный шаг
            'active_parallel_steps': ['step3','step4'],     
            'steps_time': {
                'step3': 6 ,
                'step4': 1 ,
            },        
            'steps_history': {
                'step1': 3,         
                'step2': 4          
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
        },
    }
    # Получаем прогноз
    predictor = IntegrationPredictor()

    # Получаем текущий шаг из активных шагов
    active_steps = source_data['current_progress']['active_parallel_steps']
    current_step = max(int(''.join(filter(str.isdigit, step))) for step in active_steps)


    # Получаем все шаги из dependencies
    all_steps = source_data['current_progress']['steps_dependencies'].keys()
    
    # Считаем общее ожидаемое время
    total_expected = sum(predictor.statistical_model.calculate_metrics(step)['mean'] for step in all_steps)
    total_standard = sum(get_standard_time(step) for step in all_steps)
    

     # Получаем начальный прогноз
    initial = predictor.initial_estimate(source_data)
    print(f"""
    Начальный прогноз:
    - Ожидаемое время: {initial['initial_estimate']:.1f} дней
    - Стандартное время: {initial['standard_time']} дней

    Общий прогноз всех шагов:
    - Ожидаемое время всех шагов: {total_expected:.1f} дней
    - Стандартное время всех шагов: {total_standard} дней
    """)

    prediction = predictor.predict_completion(source_data)
    print(f"predictor: {predictor}")
    print(f"Прогноз: {prediction}")

    # Проверяем цель
    target = IntegrationTarget()
    result = target.calculate_target(
        prediction['estimated_days'],
        source_data['current_progress']['steps_history'],
        current_step
    )

    print(f"""
    Прогноз интеграции:
    - Ожидаемое время: {prediction['estimated_days']:.1f} дней
    - Статус: {prediction['warning_status']}
    - Сложность: {prediction['complexity_factor']:.2f}
    - Вероятность уложиться в срок: {result['completion_rate']*100:.1f}%
    """)
    print(f"""
    Прогноз интеграции:
    - Затрачено времени: {result['historical_time']:.1f} дней
    - Текущие шаги в работе: {prediction['estimated_days']:.1f} дней
    - Осталось на будущие шаги: {result['remaining_time']:.1f} дней
    - Общее время загрузки: {result['total_time']:.1f} дней
    - Целевое время: {target.target_days} дней
    - Вероятность уложиться в срок: {result['completion_rate']:.1f}%
    """)


    print(f"Результат: {result}")

if __name__ == '__main__':
    run_demo()
