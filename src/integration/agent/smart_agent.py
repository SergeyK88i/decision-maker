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
        
    def analyze_integration(self, source_data: str) -> Dict:
        # source_data = self.history_db.get_source_data(source_id)
         # Временно заменим получение данных из БД на тестовые данные
        # source_data = {
        #     'characteristics': {
        #         'data_volume': 1,
        #         'api_complexity': 2,
        #         'data_quality': 0
        #     },
        #     'current_progress': {
        #         'step': 'step2',
        #         'days_spent': 4
        #     }
        # }
        prediction = self.predictor.predict_completion(source_data)
        prediction['source_data'] = source_data  # Добавляем source_data в prediction

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

    def get_step_metrics(self, step: str) -> Dict:
        # Динамический расчет метрик для шага на основе текущих данных
        current_step_num = int(step.replace('step', ''))
        base_risk = 0.5  # базовый риск
        
        # Увеличиваем риск для более поздних шагов
        risk_level = base_risk + (current_step_num * 0.1)
        
        return {
            'risk_level': risk_level,
            'delay': max(0, current_step_num - 1)  # Потенциальная задержка растет с номером шага
        }

    def identify_critical_steps(self, prediction: Dict) -> List[str]:
        critical_steps = []
        current_step = prediction['source_data']['current_progress']['step']
        current_step_num = int(current_step.replace('step', ''))

        # Анализируем только текущий и будущие шаги
        for step_num in range(current_step_num, 8):
            step = f'step{step_num}'
            metrics = self.get_step_metrics(step)
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

        # Получаем текущий шаг из source_data
        current_step = int(prediction['source_data']['current_progress']['step'].replace('step', ''))

        if prediction['warning_status'] == 'red':
            recommendations.append("Требуется немедленное вмешательство")
        for risk in risks:
            recommendations.extend(self.ml_model.suggest_mitigation(risk, current_step))
        if critical_steps:
            recommendations.append(f"Особое внимание шагам: {', '.join([s['step'] for s in critical_steps])}")
        return recommendations
