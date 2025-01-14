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
        self.resources = {
            'R1': Resource('R1', 'developer', 8, 0.7),
            'R2': Resource('R2', 'developer', 6, 0.5),
            'R3': Resource('R3', 'analyst', 7, 0.8)
        }
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
        return {
            'available_resources': {r.id: r.availability for r in self.resources.values()},
            'utilization': self.calculate_utilization(),
            'bottlenecks': self.identify_bottlenecks(),
            'resource_details': {
                resource_id: {
                    'type': resource.type,
                    'skill_level': resource.skill_level,
                    'availability': resource.availability,
                    'current_project': resource.current_project
                }
                for resource_id, resource in self.resources.items()
            }
        }

    def calculate_utilization(self) -> Dict:
        return {
            resource.id: {
                'total': 1.0,
                'used': 1 - resource.availability,
                'type': resource.type,
                'skill_level': resource.skill_level
            }
            for resource in self.resources.values()
        }

    def identify_bottlenecks(self) -> List[str]:
        bottlenecks = []
        for resource in self.resources.values():
            if resource.availability < 0.1:
                bottlenecks.append(f"Critical utilization of {resource.type} (ID: {resource.id})")
            elif resource.availability < 0.3:
                bottlenecks.append(f"High utilization of {resource.type} (ID: {resource.id})")
        return bottlenecks

    def get_step_requirements(self, step: str) -> Dict:
        requirements = {
            'step1': {'min_skill': 5, 'preferred_type': 'analyst'},
            'step2': {'min_skill': 7, 'preferred_type': 'developer'},
            'step3': {'min_skill': 6, 'preferred_type': 'developer'},
            'step4': {'min_skill': 6, 'preferred_type': 'developer'},
            'step5': {'min_skill': 5, 'preferred_type': 'analyst'},
            'step6': {'min_skill': 7, 'preferred_type': 'developer'},
            'step7': {'min_skill': 6, 'preferred_type': 'developer'}
        }
        return requirements.get(step, {'min_skill': 5, 'preferred_type': 'any'})

    def optimize_allocation(self, available: List[Resource], critical_steps: List[str]) -> Dict:
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

    def find_best_resource(self, available: List[Resource], requirements: Dict) -> Optional[Resource]:
        suitable = [
            r for r in available
            if r.skill_level >= requirements['min_skill'] and
            (r.type == requirements['preferred_type'] or requirements['preferred_type'] == 'any')
        ]
        return max(suitable, key=lambda x: x.skill_level) if suitable else None

    def calculate_optimal_allocation(self, step: str, resource: Resource) -> float:
        base_allocation = 0.5
        if resource.skill_level > 7:
            base_allocation *= 0.8  # Опытные ресурсы работают эффективнее
        return min(resource.availability, base_allocation)
