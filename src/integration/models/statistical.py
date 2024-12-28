from typing import Dict, List
import numpy as np

class StatisticalModel:
    def __init__(self):
        self.historical_data = {
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
            'mean': np.mean(data),
            'median': np.median(data),
            'std': np.std(data)
        }
