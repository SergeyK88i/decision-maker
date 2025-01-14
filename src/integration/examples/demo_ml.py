import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)
from src.integration.predictor import IntegrationPredictor
from src.integration.target import IntegrationTarget
from src.integration.agent.smart_agent import IntegrationSmartAgent
from src.integration.models.factor import FactorAnalysis
from src.integration.models.statistical import StatisticalModel
from src.integration.utils.calculations import calculate_step_correlations, analyze_parallel_risks, get_parallel_risk_status

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
    
    
    # Получаем базовые результаты
    result = agent.analyze_integration(source_data)
    
    # Получаем дополнительные метрики
    # initial = predictor.initial_estimate(source_data)
    # progress = predictor.calculate_progress_estimate(source_data)
    # parallel_risk = analyze_parallel_risks(source_data['current_progress']['active_parallel_steps'], 
    #                                      source_data['current_progress']['steps_dependencies'])
    
    print(f"""
    Комплексный анализ интеграции:
    
    1. ML анализ и риски:
    - Анализ паттернов: {result['ml_analysis']['patterns']}
    - Параллельные риски: {result['ml_analysis']['parallel_risks']}
    - Выявленные риски: {result['ml_analysis']['risks']}
    
    2. Статистика и прогресс:
    - Статистика шагов: {result['statistical_analysis']['steps']}
    - Прогресс: {result['statistical_analysis']['progress']}
    - Baseline метрики: {result['statistical_analysis']['baseline']}
    
    3. Факторы сложности:
    - Общая сложность: {result['factor_analysis']['complexity']}
    - Тренды выполнения: {result['factor_analysis']['trends']}
    - Корреляции шагов: {result['factor_analysis']['correlations']}
    - Сложность шагов: {result['factor_analysis']['step_complexity']}
    
    4. Статус и прогноз:
    - Статус предупреждений: {result['warning_status']}
    - Прогноз выполнения: {result['prediction']}
    - Вероятность завершения: {result['completion_probability']*100:.1f}%
    
    5. Ресурсы и рекомендации:
    - Статус ресурсов: {result['resource_status']}
    - Рекомендации: {result['recommendations']}
    """)

if __name__ == '__main__':
    run_demo()
