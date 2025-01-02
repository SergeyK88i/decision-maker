from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Resource:
    id: str
    type: str
    skill_level: int
    availability: float
    current_project: Optional[str] = None

class ResourceManager:
    def __init__(self):
        self.resources = {}
        self.assignments = {}
        
    def find_available(self) -> List[Resource]:
        return [r for r in self.resources.values() if r.availability > 0.3]
    
    def assign_senior(self, resources: List[Resource]) -> bool:
        senior = next((r for r in resources if r.skill_level > 7), None)
        if senior:
            senior.availability -= 0.5
            return True
        return False

    def get_current_allocation(self) -> Dict:
        current_allocation = {}
        for resource_id, resource in self.resources.items():
            current_allocation[resource_id] = {
                'type': resource.type,
                'skill_level': resource.skill_level,
                'availability': resource.availability,
                'current_project': resource.current_project
            }
        return current_allocation

    def optimize_allocation(self, available: List[Resource], 
                          critical_steps: List[str]) -> Dict:
        optimization_plan = {}
        
        for step in critical_steps:
            required_skills = self.get_step_requirements(step)
            best_match = self.find_best_resource(available, required_skills)
            
            if best_match:
                optimization_plan[step] = {
                    'resource': best_match,
                    'allocation': self.calculate_optimal_allocation(step, best_match)
                }
                
        return optimization_plan
    
    def get_step_requirements(self, step: str) -> Dict:
        requirements = {
            'step1': {'min_skill': 5, 'preferred_type': 'analyst'},
            'step2': {'min_skill': 7, 'preferred_type': 'developer'},
            'step3': {'min_skill': 6, 'preferred_type': 'developer'},
            'step4': {'min_skill': 6, 'preferred_type': 'developer'}
        }
        return requirements.get(step, {'min_skill': 5, 'preferred_type': 'any'})