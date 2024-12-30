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

    def analyze_parallel_steps(self, source_data: Dict) -> Dict:
        current_progress = source_data['current_progress']
        dependencies = current_progress['steps_dependencies']
        steps_history = current_progress['steps_history']
    
        # Определяем доступные для параллельного выполнения шаги
        available_parallel = [
            step for step in dependencies 
            if all(dep in steps_history for dep in dependencies[step])
        ]
    
        # Получаем активные параллельные шаги
        active_parallel = current_progress.get('active_parallel_steps', [])
    
        # Находим шаги, которые можно начать выполнять параллельно
        potential_parallel = [
            step for step in available_parallel 
            if step not in active_parallel
        ]
    
        return {
            'available_parallel': available_parallel,
            'active_parallel': active_parallel,
            'potential_parallel': potential_parallel
        }
        
    def analyze_integration(self, source_data: str) -> Dict:
        prediction = self.predictor.predict_completion(source_data)
        prediction = {
            'estimated_days': prediction['estimated_days'],
            'warning_status': prediction['warning_status'],
            'complexity_factor': prediction['complexity_factor'],
            'statistical_data': prediction['statistical_data'],
            'source_data': source_data
        }

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
        active_steps = prediction['source_data']['current_progress']['active_parallel_steps']
        
        for step in active_steps:
            metrics = self.get_step_metrics(step)
            # Анализируем только текущий и будущие шаги
            if metrics['risk_level'] > 0.7:
                critical_steps.append({
                    'step': step,
                    'risk_level': metrics['risk_level'],
                    'expected_delay': metrics['delay'],
                    'required_skills': self.resource_manager.get_step_requirements(step)
                })
        
        return critical_steps
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
        active_steps = prediction['source_data']['current_progress']['active_parallel_steps']
        parallel_steps = prediction['source_data']['current_progress'].get('parallel_steps', [])
        dependencies = prediction['source_data']['current_progress']['steps_dependencies']
        steps_history = prediction['source_data']['current_progress']['steps_history']

        if prediction['warning_status'] == 'red':
            recommendations.append("Требуется немедленное вмешательство")
        for risk in risks:
            for step in active_steps:
                recommendations.extend(self.ml_model.suggest_mitigation(risk, step))

        recommendations.append(f"Особое внимание текущим шагам: {', '.join(active_steps)}")
        # Анализ возможности параллельного выполнения
        available_steps = [step for step in dependencies 
                        if all(dep in steps_history for dep in dependencies[step])]
        
        if available_steps:
            recommendations.append(f"Возможно параллельное выполнение шагов: {', '.join(available_steps)}")
        
        if parallel_steps:
            recommendations.append(f"Текущие параллельные шаги: {', '.join(parallel_steps)}")

        return recommendations