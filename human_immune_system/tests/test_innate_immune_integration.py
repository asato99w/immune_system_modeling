import unittest
from ..model import Antigen, AntigenType
from ..model.innate_immune_system import InnateImmuneSystem
from ..model.dendritic_cell import DendriticCell
from ..model.cytokine_environment import CytokineEnvironment


class TestInnateImmuneIntegration(unittest.TestCase):
    """自然免疫系と樹状細胞の統合テスト"""
    
    def setUp(self):
        """各テストの前に統合環境を準備"""
        self.cytokine_env = CytokineEnvironment()
        self.innate_system = InnateImmuneSystem(self.cytokine_env)
        
        # 樹状細胞を系に追加
        self.dc1 = DendriticCell()
        self.dc2 = DendriticCell()
        self.innate_system.add_dendritic_cell(self.dc1)
        self.innate_system.add_dendritic_cell(self.dc2)
    
    def test_dendritic_cell_integration(self):
        """樹状細胞が自然免疫系に正しく統合される"""
        # 初期状態
        self.assertFalse(self.innate_system.is_activated())
        
        # 病原体による抗原暴露
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        response = self.innate_system.antigen_exposure(pathogen)
        
        self.assertTrue(response)
        self.assertTrue(self.innate_system.is_activated())
    
    def test_coordinated_immune_response(self):
        """協調的な免疫応答"""
        pathogen = Antigen(
            antigen_type=AntigenType.VIRAL,
            concentration=75.0,
            molecular_signature="dsRNA"
        )
        
        self.innate_system.antigen_exposure(pathogen)
        
        # 免疫状態の確認
        status = self.innate_system.get_immune_status()
        
        self.assertTrue(status["system_activated"])
        self.assertGreater(status["active_dcs"], 0)
        self.assertGreater(status["cytokine_levels"].get("IL-12", 0), 0)
    
    def test_dc_communication_via_cytokines(self):
        """サイトカインを介した樹状細胞間コミュニケーション"""
        # 一つの樹状細胞が強く活性化
        strong_pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=100.0,
            molecular_signature="LPS"
        )
        
        # dc1だけに直接暴露（テストのため直接操作）
        self.dc1.recognize_pattern(strong_pathogen)
        
        # dc1のサイトカイン産生によりdc2が準備状態になる
        status = self.innate_system.get_immune_status()
        
        self.assertTrue(self.dc1.is_activated())
        self.assertTrue(self.dc2.is_primed())  # 環境サイトカインにより準備状態
    
    def test_self_antigen_tolerance(self):
        """自己抗原に対する寛容性"""
        self_antigen = Antigen(
            antigen_type=AntigenType.SELF,
            molecular_signature="self_protein"
        )
        
        response = self.innate_system.antigen_exposure(self_antigen)
        
        self.assertFalse(response)
        self.assertFalse(self.innate_system.is_activated())
        
        status = self.innate_system.get_immune_status()
        self.assertEqual(status["active_dcs"], 0)


if __name__ == '__main__':
    unittest.main()