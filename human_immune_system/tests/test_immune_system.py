import unittest
from ..model import ImmuneSystem

class TestAntigenRecognition(unittest.TestCase):
    def test_antigen_exposure_triggers_activation(self):
        immune_system = ImmuneSystem()
        
        self.assertFalse(immune_system.is_activated())
        
        response = immune_system.antigen_exposure("viral_antigen")
        
        self.assertTrue(response)
        self.assertTrue(immune_system.is_activated())


if __name__ == '__main__':
    unittest.main()