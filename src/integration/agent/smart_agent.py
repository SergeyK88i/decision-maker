from typing import Dict, List
from enum import Enum
from .rules import decide_resource_allocation
from .resource_manager import ResourceManager, Resource
from .ml_predictor import MLPredictor
from ..predictor import IntegrationPredictor
from ..handlers import *

class Action(Enum):
    ASSIGN_SENIOR_DEVELOPER = "assign_senior"
    SCALE_INFRASTRUCTURE = "scale_infra"
    CONTINUE_MONITORING = "continue"

class IntegrationSmartAgent:
    def __init__(self):
        # Инициализация обработчиков
        self.ml_handler = MLPredictorHandler()
        self.statistical_handler = StatisticalHandler()
        self.factor_handler = FactorHandler()
        self.warning_handler = WarningHandler()
        self.predictor_handler = PredictorHandler()
        self.target_handler = TargetHandler()
        
        # Построение цепочки
        print("Инициализация цепочки обработчиков")
        # Правильное построение цепочки
        self.ml_handler.set_next(self.statistical_handler)
        self.statistical_handler.set_next(self.factor_handler)
        self.factor_handler.set_next(self.warning_handler)
        self.warning_handler.set_next(self.predictor_handler)
        self.predictor_handler.set_next(self.target_handler)
        print("Цепочка обработчиков построена")
        
        # Дополнительные компоненты
        self.resource_manager = ResourceManager()
        self.ml_model = MLPredictor()

    def analyze_integration(self, source_data: Dict) -> Dict:
        # Запуск цепочки обработки
        print("\nЗапуск цепочки обработки")
        print(f"Первый обработчик: {self.ml_handler.__class__.__name__}")
        chain_result = self.ml_handler.handle(source_data)
        print("\nРезультат цепочки обработчиков:", chain_result)
        # Анализ результатов и генерация рекомендаций
        risks = chain_result.get('ml_analysis', [])
        resources = self.resource_manager.get_current_allocation()
        critical_steps = self.identify_critical_steps(chain_result)
        
        # Формируем финальный результат
        return {
            'ml_analysis': chain_result.get('ml_analysis', []),
            'statistical_analysis': chain_result.get('statistical_analysis', {}),
            'factor_analysis': chain_result.get('factor_analysis', {}),
            'warning_status': chain_result.get('warning_status', ''),
            'prediction': chain_result.get('prediction', {}),
            'completion_probability': chain_result.get('completion_probability', 0),
            'risks': chain_result.get('risks', []),
            'resource_status': self.resource_manager.get_current_allocation(),
            'recommendations': self.generate_recommendations(
                chain_result.get('prediction', {}),
                chain_result.get('risks', []),
                self.resource_manager.get_current_allocation(),
                self.identify_critical_steps(chain_result)
            )
        }

    def identify_critical_steps(self, prediction: Dict) -> List[str]:
        critical_steps = []
        active_steps = prediction.get('source_data', {}).get('current_progress', {}).get('active_parallel_steps', [])
        
        for step in active_steps:
            metrics = self.get_step_metrics(step)
            if metrics['risk_level'] > 0.7:
                critical_steps.append({
                    'step': step,
                    'risk_level': metrics['risk_level'],
                    'expected_delay': metrics['delay'],
                    'required_skills': self.resource_manager.get_step_requirements(step)
                })
        
        return critical_steps

    def get_step_metrics(self, step: str) -> Dict:
        current_step_num = int(step.replace('step', ''))
        base_risk = 0.5
        risk_level = base_risk + (current_step_num * 0.1)
        
        return {
            'risk_level': risk_level,
            'delay': max(0, current_step_num - 1)
        }

    def generate_recommendations(self, prediction: Dict, risks: List[Dict], 
                               resources: Dict, critical_steps: List[str]) -> List[str]:
        recommendations = []
        
        if prediction.get('warning_status') == 'red':
            recommendations.append("Требуется немедленное вмешательство")
            
        for risk in risks:
            for step in prediction.get('source_data', {}).get('current_progress', {}).get('active_parallel_steps', []):
                recommendations.extend(self.ml_model.suggest_mitigation(risk, step))

        return recommendations
