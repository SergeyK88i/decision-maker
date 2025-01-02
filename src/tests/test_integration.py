import unittest
from integration.predictor import IntegrationPredictor
from integration.target import IntegrationTarget

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.predictor = IntegrationPredictor()
        self.target = IntegrationTarget()
        
    def test_prediction(self):
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
        self.assertIsNotNone(prediction['estimated_days'])
        self.assertIn(prediction['warning_status'], ['green', 'yellow', 'red'])
        
    def test_target_calculation(self):
        result = self.target.calculate_target(35.0)
        self.assertFalse(result['on_time'])
        self.assertEqual(result['deviation_days'], 5.0)

if __name__ == '__main__':
    unittest.main()
