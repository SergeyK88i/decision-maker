from typing import Dict
from .base import IntegrationHandler
from ..models.early_warning import EarlyWarningSystem

class WarningHandler(IntegrationHandler):
    def __init__(self):
        super().__init__()
        self.early_warning = EarlyWarningSystem()
        
    def handle(self, data: Dict) -> Dict:
        status = self.early_warning.check_status(
            data['current_progress']['active_parallel_steps'],
            data['current_progress']['steps_time']
        )
        data['warning_status'] = status
        return super().handle(data)
