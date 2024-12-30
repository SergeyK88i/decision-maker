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
            'data_volume': 1,       # средний объем (1.2)
            'api_complexity': 2,    # сложный API (1.6)
            'data_quality': 0       # высокое качество (1.0)
        },
        'current_progress': {
            'active_parallel_steps': ['step3'],  # текущий активный шаг
            'steps_time': {
                'step3': 10         # время текущего шага
            },        # потрачено дней
            'steps_history': {
                'step1': 4,         # факт выполнения
                'step2': 9          # факт выполнения
            }
        },
    }

    # Получаем прогноз
    predictor = IntegrationPredictor()
    prediction = predictor.predict_completion(source_data)
    print(f"predictor: {predictor}")
    print(f"Прогноз: {prediction}")

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
    print(f"Результат: {result}")

if __name__ == '__main__':
    run_demo()
