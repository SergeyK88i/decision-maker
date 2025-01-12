import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)

from src.integration.agent.smart_agent import IntegrationSmartAgent


def run_demo():
    source_data = {
        'characteristics': {
            'data_volume': 0,
            'api_complexity': 0,
            'data_quality': 0
        },
        'current_progress': {
            'active_parallel_steps': ['step3', 'step4'],
            'steps_time': {
                'step3': 3,
                'step4': 1,
            },
            'steps_history': {
                'step1': 3,
                'step2': 1
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
    
    agent = IntegrationSmartAgent()
    result = agent.analyze_integration(source_data)
    
    # Добавим отладочный вывод
    print("Полученный результат:", result)
    
    # Добавим проверку наличия ключей
    ml_analysis = result.get('ml_analysis', 'Нет данных')
    statistical_analysis = result.get('statistical_analysis', 'Нет данных')
    print(ml_analysis)
    print('statistical_analysis',statistical_analysis)
    print(f"""
    Комплексный анализ интеграции:
    
    1. ML анализ и риски:
    - Анализ паттернов: {result['ml_analysis']}
    - Выявленные риски: {result['risks']}
    
    2. Статистика и прогресс:
    - Статистический анализ: {result['statistical_analysis']}
    - Прогресс выполнения: {result['prediction'].get('completion_percent', 0):.1f}%
    
    3. Факторы сложности:
    - Факторный анализ: {result['factor_analysis']}
    - Общая сложность: {result['prediction'].get('complexity_factor', 0):.2f}
    
    4. Статус и прогноз:
    - Статус предупреждений: {result['warning_status']}
    - Ожидаемое время: {result['prediction'].get('estimated_days', 0):.1f} дней
    - Вероятность завершения: {result['completion_probability']*100:.1f}%
    
    5. Ресурсы и рекомендации:
    - Статус ресурсов: {result['resource_status']}
    - Рекомендации: {result['recommendations']}
    """)

if __name__ == '__main__':
    run_demo()
