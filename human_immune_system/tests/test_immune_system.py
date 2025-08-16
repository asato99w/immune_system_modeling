import unittest
from ..model import ImmuneSystem, Antigen, AntigenType


class TestImmuneSystem(unittest.TestCase):
    """統合された免疫系テスト"""
    
    def setUp(self):
        self.immune_system = ImmuneSystem()
    
    def test_immune_system_activation_by_pathogen(self):
        """病原体による免疫系の活性化"""
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            concentration=50.0,
            molecular_signature="dsRNA"
        )
        
        self.assertFalse(self.immune_system.is_activated())
        
        self.immune_system.antigen_exposure(viral_antigen)
        
        self.assertTrue(self.immune_system.is_activated())
    
    def test_no_activation_by_self_antigen(self):
        """自己抗原では活性化されない"""
        self_antigen = Antigen(
            antigen_type=AntigenType.SELF,
            concentration=50.0,
            molecular_signature="self_protein"
        )
        
        self.immune_system.antigen_exposure(self_antigen)
        
        self.assertFalse(self.immune_system.is_activated())
    
    def test_no_activation_without_antigen(self):
        """抗原なしでは活性化されない"""
        self.immune_system.antigen_exposure(None)
        
        self.assertFalse(self.immune_system.is_activated())
    
    def test_immune_system_uses_innate_pattern_recognition(self):
        """免疫系が自然免疫のパターン認識を使用"""
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        
        # 自然免疫系がパターンを認識すれば免疫系も活性化
        pattern_recognized = self.immune_system.innate_system.recognize_pattern(bacterial_antigen)
        
        self.immune_system.antigen_exposure(bacterial_antigen)
        
        self.assertTrue(pattern_recognized)
        self.assertTrue(self.immune_system.is_activated())


if __name__ == '__main__':
    unittest.main()