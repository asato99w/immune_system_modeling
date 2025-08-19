import unittest
from ..model import Antigen, AntigenType
from ..model.dendritic_cell import DendriticCell
from ..model.cytokine_environment import CytokineEnvironment


class TestDendriticCellBasic(unittest.TestCase):
    """樹状細胞の基本機能テスト"""
    
    def test_initial_state(self):
        """初期状態の確認"""
        dc = DendriticCell()
        self.assertFalse(dc.is_activated())
        self.assertFalse(dc.is_primed())
    
    def test_pattern_recognition(self):
        """パターン認識機能"""
        dc = DendriticCell()
        
        # 既知のPAMPsを認識
        bacterial = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.assertTrue(dc.recognize_pattern(bacterial))
        
        # 自己抗原は認識しない
        self_antigen = Antigen(
            antigen_type=AntigenType.SELF,
            molecular_signature="self_protein"
        )
        self.assertFalse(dc.recognize_pattern(self_antigen))
    
    def test_activation_by_pathogen(self):
        """病原体認識による活性化"""
        dc = DendriticCell()
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        
        dc.recognize_pattern(pathogen)
        # シグナル処理は自動的に実行される
        self.assertTrue(dc.is_activated())


class TestDendriticCellWithEnvironment(unittest.TestCase):
    """環境内での樹状細胞の振る舞いテスト"""
    
    def setUp(self):
        """各テストの前に環境と細胞を準備"""
        self.env = CytokineEnvironment()
        self.dc = DendriticCell()
        self.env.register_cell(self.dc)
        self.dc.enter_environment(self.env)
    
    def test_cytokine_production(self):
        """活性化による環境へのサイトカイン産生"""
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        self.dc.recognize_pattern(pathogen)
        # シグナル処理は自動的に実行される
        
        self.assertGreater(self.env.get_level("IL-12"), 0)
        self.assertGreater(self.env.get_level("TNF-alpha"), 0)
        self.assertGreater(self.env.get_level("IL-6"), 0)
    
    def test_no_cytokine_for_self_antigen(self):
        """自己抗原ではサイトカイン産生しない"""
        self_antigen = Antigen(
            antigen_type=AntigenType.SELF,
            molecular_signature="self_protein"
        )
        
        self.dc.recognize_pattern(self_antigen)
        # 自己抗原では活性化されない
        
        self.assertFalse(self.dc.is_activated())
        self.assertEqual(self.env.get_level("IL-12"), 0)
    
    def test_concentration_dependent_response(self):
        """濃度依存的なサイトカイン産生"""
        env_low = CytokineEnvironment()
        env_high = CytokineEnvironment()
        dc_low = DendriticCell()
        dc_high = DendriticCell()
        
        dc_low.enter_environment(env_low)
        dc_high.enter_environment(env_high)
        
        # 低濃度と高濃度の抗原
        low_threat = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=1.0,
            molecular_signature="LPS"
        )
        high_threat = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=100.0,
            molecular_signature="LPS"
        )
        
        dc_low.recognize_pattern(low_threat)
        # 低濃度抗原による自動処理
        
        dc_high.recognize_pattern(high_threat)
        # 高濃度抗原による自動処理
        
        self.assertGreater(
            env_high.get_level("IL-12"),
            env_low.get_level("IL-12")
        )
    
    def test_response_to_environmental_cytokines(self):
        """環境サイトカインへの応答"""
        # IFN-γによる準備状態の誘導
        self.env.add_cytokine("IFN-gamma", 10.0)
        self.assertTrue(self.dc.is_primed())
        
        # TNF-αによる準備状態の誘導
        dc2 = DendriticCell()
        env2 = CytokineEnvironment()
        env2.register_cell(dc2)
        dc2.enter_environment(env2)
        
        env2.add_cytokine("TNF-alpha", 15.0)
        self.assertTrue(dc2.is_primed())


class TestPrimingBehavior(unittest.TestCase):
    """準備状態による振る舞いの変化をテスト"""
    
    def test_primed_cell_produces_more_cytokines(self):
        """準備状態の細胞はより多くのサイトカインを産生"""
        # 通常の細胞
        env_normal = CytokineEnvironment()
        dc_normal = DendriticCell()
        dc_normal.enter_environment(env_normal)
        
        # 準備状態の細胞
        env_primed = CytokineEnvironment()
        dc_primed = DendriticCell()
        env_primed.register_cell(dc_primed)
        dc_primed.enter_environment(env_primed)
        
        # IFN-γで準備状態にする
        env_primed.add_cytokine("IFN-gamma", 10.0)
        self.assertTrue(dc_primed.is_primed())
        
        # 同じ抗原で刺激
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        dc_normal.recognize_pattern(pathogen)
        dc_primed.recognize_pattern(pathogen)
        
        # 準備状態の細胞の方が多くサイトカインを産生
        normal_il12 = env_normal.get_level("IL-12")
        primed_il12 = env_primed.get_level("IL-12")
        
        self.assertGreater(primed_il12, normal_il12)
        self.assertGreater(primed_il12, normal_il12 * 1.5)


class TestCellCommunication(unittest.TestCase):
    """細胞間コミュニケーションのテスト"""
    
    def test_cytokine_mediated_communication(self):
        """サイトカインを介した細胞間通信"""
        env = CytokineEnvironment()
        dc1 = DendriticCell()
        dc2 = DendriticCell()
        
        # 両細胞を環境に登録
        env.register_cell(dc1)
        env.register_cell(dc2)
        dc1.enter_environment(env)
        dc2.enter_environment(env)
        
        # dc1が病原体を認識してサイトカイン産生
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=100.0,
            molecular_signature="LPS"
        )
        dc1.recognize_pattern(pathogen)
        
        # dc2が環境変化により準備状態になる
        self.assertTrue(dc2.is_primed())
        self.assertTrue(dc1.is_activated())


if __name__ == '__main__':
    unittest.main()