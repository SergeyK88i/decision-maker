from typing import Dict, List
from enum import Enum
from .rules import decide_resource_allocation
from .resource_manager import ResourceManager, Resource
from .ml_predictor import MLPredictor
# from .historical_db import HistoricalDatabase
from ..predictor import IntegrationPredictor


class Action(Enum):
    ASSIGN_SENIOR_DEVELOPER = "assign_senior"
    SCALE_INFRASTRUCTURE = "scale_infra"
    CONTINUE_MONITORING = "continue"

class IntegrationSmartAgent:
    def __init__(self):
        self.predictor = IntegrationPredictor()
        self.resource_manager = ResourceManager()
        self.ml_model = MLPredictor()
        # self.history_db = HistoricalDatabase()
        
    def analyze_integration(self, source_id: str) -> Dict:
        # source_data = self.history_db.get_source_data(source_id)
         # Временно заменим получение данных из БД на тестовые данные
        source_data = {
            'characteristics': {
                'data_volume': 1,
                'api_complexity': 2,
                'data_quality': 0
            },
            'current_progress': {
                'step': 'step2',
                'days_spent': 4
            }
        }
        prediction = self.predictor.predict_completion(source_data)
        risks = self.detect_risks(source_data)
        resources = self.resource_manager.get_current_allocation()
        critical_steps = self.identify_critical_steps(prediction)
        
        return {
            'prediction': prediction,
            'risks': risks,
            'resource_status': resources,
            'recommendations': self.generate_recommendations(
                prediction, risks, resources, critical_steps
            )
        }
    
    def redistribute_resources(self, prediction: Dict) -> Action:
        """
        Перераспределяет ресурсы при критической ситуации.
        Если статус warning_status = 'red', ищет доступные ресурсы,
        определяет необходимое действие и выполняет его.
        """
        if prediction['warning_status'] == 'red':
            available = self.resource_manager.find_available()
            action = decide_resource_allocation(prediction, available)
            return self.execute_action(action, available)
        return Action.CONTINUE_MONITORING

    def execute_action(self, action: Action, available_resources: List[Resource]) -> Action:
        """
        Выполняет выбранное действие по перераспределению ресурсов
        """
        if action == Action.ASSIGN_SENIOR_DEVELOPER:
            success = self.resource_manager.assign_senior(available_resources)
            return action if success else Action.CONTINUE_MONITORING
        elif action == Action.SCALE_INFRASTRUCTURE:
            # Логика масштабирования инфраструктуры
            return action
        return Action.CONTINUE_MONITORING

    def identify_critical_steps(self, prediction: Dict) -> List[str]:
        critical_steps = []
        # Добавить метрики шагов по умолчанию, если они отсутствуют
        step_metrics = {
            'step1': {'risk_level': 0.5, 'delay': 0},
            'step2': {'risk_level': 0.8, 'delay': 2},
            'step3': {'risk_level': 0.6, 'delay': 1}
        }
        for step, metrics in step_metrics.items():
            if metrics['risk_level'] > 0.7:
                critical_steps.append({
                    'step': step,
                    'risk_level': metrics['risk_level'],
                    'expected_delay': metrics['delay'],
                    'required_skills': self.resource_manager.get_step_requirements(step)
                })
            
        return sorted(critical_steps, key=lambda x: x['risk_level'], reverse=True)
        # for step, metrics in prediction['step_metrics'].items():
        #     if metrics['risk_level'] > 0.7:
        #         critical_steps.append({
        #             'step': step,
        #             'risk_level': metrics['risk_level'],
        #             'expected_delay': metrics['delay'],
        #             'required_skills': self.resource_manager.get_step_requirements(step)
        #         })
                
        # return sorted(critical_steps, 
                    #  key=lambda x: x['risk_level'], 
                    #  reverse=True)

    

    def detect_risks(self, source_data: Dict) -> List[Dict]:
        patterns = self.ml_model.analyze_patterns(source_data)
        return [p for p in patterns if p['risk_level'] > 0.7]
    
    def generate_recommendations(self, prediction: Dict, risks: List[Dict], 
                               resources: Dict, critical_steps: List[str]) -> List[str]:
        recommendations = []
        if prediction['warning_status'] == 'red':
            recommendations.append("Требуется немедленное вмешательство")
        for risk in risks:
            recommendations.extend(self.ml_model.suggest_mitigation(risk))
        if critical_steps:
            recommendations.append(f"Особое внимание шагам: {', '.join([s['step'] for s in critical_steps])}")
        return recommendations
