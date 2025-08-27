import unittest
from ....model import Antigen, AntigenType
from ....model.macrophage import Macrophage
from ....model.cytokine_environment import CytokineEnvironment


class TestMacrophageBasic(unittest.TestCase):
    """マクロファージの基本機能テスト"""
    
    def test_initial_state(self):
        """初期状態の確認"""
        macrophage = Macrophage()
        self.assertFalse(macrophage.is_activated())
        self.assertEqual(macrophage.get_activation_level(), 0)
    
    def test_phagocytosis(self):
        """貪食機能"""
        macrophage = Macrophage()
        
        # 細菌抗原を貪食
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        
        result = macrophage.phagocytose(bacterial_antigen)
        self.assertTrue(result)
        
        # 貪食により基礎的な活性化
        self.assertTrue(macrophage.get_activation_level() > 0)
    
    def test_activation_by_ifn_gamma(self):
        """IFN-γによる活性化"""
        env = CytokineEnvironment()
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        env.register_cell(macrophage)
        
        # IFN-γを環境に追加
        env.add_cytokine("IFN-gamma", 10.0)
        
        # 活性化を確認
        self.assertTrue(macrophage.is_activated())
        self.assertGreater(macrophage.get_activation_level(), 50)
    
    def test_cytokine_production_when_activated(self):
        """活性化時のサイトカイン産生"""
        env = CytokineEnvironment()
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        env.register_cell(macrophage)
        
        # 活性化
        env.add_cytokine("IFN-gamma", 10.0)
        
        # TNF-α産生を確認
        initial_tnf = env.get_level("TNF-alpha")
        macrophage.produce_cytokines()
        final_tnf = env.get_level("TNF-alpha")
        
        self.assertGreater(final_tnf, initial_tnf)
    
    def test_enhanced_phagocytosis_when_activated(self):
        """活性化時の貪食能力増強"""
        env = CytokineEnvironment()
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        
        # 通常状態での貪食
        result1 = macrophage.phagocytose(bacterial_antigen)
        self.assertTrue(result1)
        initial_level = macrophage.get_activation_level()
        
        # IFN-γで活性化
        env.add_cytokine("IFN-gamma", 10.0)
        env.register_cell(macrophage)
        
        # 活性化状態での貪食（より効率的）
        result2 = macrophage.phagocytose(bacterial_antigen)
        self.assertTrue(result2)
        final_level = macrophage.get_activation_level()
        
        # 活性化により貪食能力が向上
        self.assertGreater(final_level, initial_level)


if __name__ == '__main__':
    unittest.main()