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
        
        # パターン認識により免疫系が活性化
        self.immune_system.antigen_exposure(bacterial_antigen)
        self.assertTrue(self.immune_system.is_activated())
        
        # 未知のパターンでは活性化しない
        unknown_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="unknown"
        )
        
        immune_system2 = ImmuneSystem()
        immune_system2.antigen_exposure(unknown_antigen)
        self.assertFalse(immune_system2.is_activated())
    
    def test_immune_system_with_dendritic_cells(self):
        """免疫系に樹状細胞を追加した統合テスト"""
        from ..model.dendritic_cell import DendriticCell
        
        # 樹状細胞を追加
        dc1 = DendriticCell()
        dc2 = DendriticCell()
        innate_system = self.immune_system.get_innate_system()
        innate_system.add_dendritic_cell(dc1)
        innate_system.add_dendritic_cell(dc2)
        
        # 病原体による暴露
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=60.0,
            molecular_signature="LPS"
        )
        
        self.immune_system.antigen_exposure(pathogen)
        
        # 統合状態の確認
        self.assertTrue(self.immune_system.is_activated())
        status = innate_system.get_immune_status()
        self.assertTrue(status["system_activated"])
        self.assertGreater(status["active_dcs"], 0)


if __name__ == '__main__':
    unittest.main()