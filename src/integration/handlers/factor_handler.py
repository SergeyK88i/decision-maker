from typing import Dict
from .base import IntegrationHandler
from ..models.factor import FactorAnalysis
from ..models.statistical import StatisticalModel
from ..utils.calculations import calculate_step_correlations

class FactorHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.factor_analysis = FactorAnalysis()
        self.statistical_model = StatisticalModel()
        
    def handle(self, data: Dict) -> Dict:
        complexity = self.factor_analysis.calculate_multiplier(data['characteristics'])
        trends = self.analyze_trends(data)
        correlations = calculate_step_correlations(data['current_progress']['steps_history'])
        
        data['factor_analysis'] = {
            'complexity': complexity,
            'trends': trends,
            'correlations': correlations,
            'step_complexity': self.calculate_steps_complexity(data)
        }
        return super().handle(data)

    def analyze_trends(self, data: Dict) -> Dict:
        active_steps = data['current_progress']['active_parallel_steps']
        return {
            'execution_trends': {
                step: self.statistical_model.analyze_trends(step) 
                for step in active_steps
            },
            'delay_distribution': {
                step: self.statistical_model.analyze_delay_distribution(step)
                for step in active_steps
            }
        }

    def calculate_steps_complexity(self, data: Dict) -> Dict:
        dependencies = data['current_progress']['steps_dependencies']
        return {
            step: self.factor_analysis.calculate_step_complexity(step, dependencies)
            for step in dependencies.keys()
        }
