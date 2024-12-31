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
            'data_volume': 0,       # средний объем (1.2)
            'api_complexity': 0,    # сложный API (1.6)
            'data_quality': 0       # высокое качество (1.0)
        },
        'current_progress': {
            'available_parallel_steps': ['step3', 'step4'],
            'active_parallel_steps': ['step3','step4'],  # текущий активный шаг
            'steps_time': {
                'step3': 1 ,
                'step4': 7 ,
            },        
            'steps_history': {
                'step1': 3,         # факт выполнения
                'step2': 12          # факт выполнения
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
    # Получаем текущий шаг из активных шагов
    active_steps = source_data['current_progress']['active_parallel_steps']
    current_step = max(int(''.join(filter(str.isdigit, step))) for step in active_steps)

    # Получаем прогноз
    predictor = IntegrationPredictor()
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
