from typing import Dict, List
import numpy as np

class StatisticalModel:
    def __init__(self):
        # Исторические данные по времени выполнения шагов
        self.historical_data = {
            # дни выполнения шага 1
            'step1': [3, 4, 3, 5, 3, 4],
            'step2': [7, 8, 9, 7, 8, 10],
            'step3': [5, 6, 5, 7, 5, 6],
            'step4': [5, 6, 5, 7, 5, 6],
            'step5': [1, 2, 1, 2, 1, 2],
            'step6': [8, 9, 8, 10, 8, 9],
            'step7': [1, 2, 1, 2, 1, 2]
        }

    def calculate_metrics(self, step: str) -> Dict:
        data = self.historical_data[step]
        return {
            # Вычисляет среднее значение (арифметическое) элементов в массиве data.
            'mean': np.mean(data),
            # Находит медиану элементов в массиве data. 
            # Медиана — это значение, которое делит набор данных на две равные части, то есть половина значений меньше медианы, а другая половина — больше.
            'median': np.median(data),
            # Вычисляет стандартное отклонение элементов в массиве data. 
            # Стандартное отклонение показывает, насколько значения в наборе данных разбросаны относительно среднего значения.
            'std': np.std(data)
        }
    def analyze_trends(self, step: str) -> Dict:
        data = self.historical_data[step]
        # Анализ последних 3 значений для тренда
        recent_trend = data[-3:]
        trend_factor = sum(y - x for x, y in zip(recent_trend, recent_trend[1:])) / len(recent_trend)
        
        return {
            'trend_factor': trend_factor,
            'std': np.std(data),
            'delay_probability': len([x for x in data if x > np.mean(data)]) / len(data)
        }

