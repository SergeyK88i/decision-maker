from typing import Dict
from .resource_manager import Resource
from enum import Enum

class Action(Enum):
    ASSIGN_SENIOR_DEVELOPER = "assign_senior"
    SCALE_INFRASTRUCTURE = "scale_infra"
    CONTINUE_MONITORING = "continue"

def decide_resource_allocation(prediction: Dict, available_resources: Dict) -> Action:
    risk_level = prediction.get('risk_level', 0)
    
    if risk_level > 0.7:
        if available_resources.get('senior_developers', 0) > 0:
            return Action.ASSIGN_SENIOR_DEVELOPER
        elif prediction.get('bottleneck') == 'performance':
            return Action.SCALE_INFRASTRUCTURE
    return Action.CONTINUE_MONITORING
