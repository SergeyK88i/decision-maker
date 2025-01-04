from typing import Dict
import math
from .utils.calculations import get_standard_time
from .models.statistical import StatisticalModel
from .models.factor import FactorAnalysis
from .utils.calculations import calculate_step_correlations, get_standard_time, analyze_parallel_risks


class IntegrationTarget:
    def __init__(self):
        self.target_days = 30
        self.statistical_model = StatisticalModel()
        self.factor_analysis = FactorAnalysis()

    def calculate_completion_probability(self, source_data: Dict) -> float:
        steps_history = source_data['current_progress']['steps_history']
        steps_time = source_data['current_progress'].get('steps_time', {})
        dependencies = source_data['current_progress']['steps_dependencies']
        
        # Рассчитываем total_time
        historical_time = sum(steps_history.values())
        stats = self.statistical_model.calculate_metrics(f'step{max(int(step[-1]) for step in steps_history)}')
        current_time = sum(steps_time.values())
        remaining_steps_time = sum(get_standard_time(f'step{i}') for i in range(len(steps_history) + 1, 8))
        
        total_time = (
            historical_time * 1.0 +
            current_time * (1 + stats['std']) +
            remaining_steps_time * 1.2
        )
        
        # Базовый расчет по времени
        time_factor = (self.target_days - total_time) / self.target_days
        
        # Анализ трендов для оставшихся шагов
        remaining_steps = set(dependencies.keys()) - set(steps_history.keys())
        trends = [
            self.statistical_model.analyze_trends(step)
            for step in remaining_steps
        ]
        
        # Учитываем сложность оставшихся шагов
        complexities = [
            self.factor_analysis.calculate_step_complexity(step, dependencies)
            for step in remaining_steps
        ]
        
        # Корреляции между шагами
        correlations = calculate_step_correlations(steps_history)
        
        # Добавляем анализ параллельных рисков
        parallel_risk = analyze_parallel_risks(
            source_data['current_progress'].get('active_parallel_steps', []),
            dependencies
        )
        # Анализ распределения задержек
        delay_distributions = [
            self.statistical_model.analyze_delay_distribution(step)
            for step in remaining_steps
        ]
        delay_risk = sum(d['high_delay_prob'] for d in delay_distributions) / len(delay_distributions) if delay_distributions else 0

        # Обновляем итоговый расчет
        completion_rate = (time_factor * 
            (1 - sum(t['trend_factor'] for t in trends) / len(trends)) /
            (sum(complexities) / len(complexities)) *
            (1 - sum(correlations.values()) / len(correlations) if correlations else 1) /
            parallel_risk *
            (1 - delay_risk)
        )
        
        return min(0.9, max(0, completion_rate))


    def calculate_target(self, actual_days: float, steps_history: Dict, current_step: int) -> Dict:
        # История выполненных шагов
        historical_time = sum(steps_history.values())

        # Получаем статистику для текущего шага
        stats = self.statistical_model.calculate_metrics(f'step{current_step}')

        # Текущее время из actual_days
        current_time = actual_days - historical_time

        # Считаем оставшееся время на невыполненные шаги
        remaining_steps_time = sum(get_standard_time(f'step{i}') for i in range(current_step + 1, 8))

        # Анализируем историю выполнения
        delays = []
        for step, time in steps_history.items():
            standard = get_standard_time(step)
            delay = time / standard
            delays.append(delay)

        # Средний процент задержек
        avg_delay = sum(delays) / len(delays) if delays else 1.0
    
        # Прогноз с учетом истории
        # predicted_days = actual_days * avg_delay
        predicted_days = actual_days


        # Общий прогноз времени
        total_time = (
            historical_time * 1.0 +  # Фактическое время - точное
            current_time * (1 + stats['std']) +  # Текущее время + погрешность
            remaining_steps_time * 1.2  # Будущее время с запасом
        )


        # Если уже превысили целевое время - вероятность 0
        if total_time > self.target_days:
            completion_rate = 0
        else:
            # Вероятность уложиться в срок
            # Чем больше запас по времени, тем выше вероятность
                buffer = (self.target_days - total_time) / self.target_days
                completion_rate = min(0.9, buffer)  # Нормализуем до 100%        
            
        return {
            'on_time': predicted_days <= self.target_days,
            'deviation_days': predicted_days - self.target_days,
            'completion_rate': completion_rate,
            'historical_delay': avg_delay,
            'remaining_time': remaining_steps_time,
            'historical_time': historical_time,
            'total_time': total_time
        }
