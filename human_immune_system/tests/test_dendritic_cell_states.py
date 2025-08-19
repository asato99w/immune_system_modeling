import unittest
from ..model import Antigen, AntigenType
from ..model.dendritic_cell import DendriticCell
from ..model.cytokine_environment import CytokineEnvironment


class TestDendriticCellBehaviorChanges(unittest.TestCase):
    """樹状細胞の振る舞い変化テスト（段階的実装）"""
    
    def setUp(self):
        self.env = CytokineEnvironment()
        self.dc = DendriticCell()
        self.env.register_cell(self.dc)
        self.dc.enter_environment(self.env)


class TestStep1BasicActivation(TestDendriticCellBehaviorChanges):
    """Step 1: 基本的な活性化の振る舞い"""
    
    def test_initial_behavior(self):
        """初期状態の振る舞い"""
        self.assertFalse(self.dc.is_activated())
        self.assertFalse(self.dc.is_primed())
    
    def test_pathogen_recognition_changes_behavior(self):
        """病原体認識による振る舞い変化"""
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        # 認識前
        self.assertFalse(self.dc.is_activated())
        
        # 認識後
        self.dc.recognize_pattern(pathogen)
        self.assertTrue(self.dc.is_activated())
        
        # サイトカイン産生を確認
        self.assertGreater(self.env.get_level("IL-12"), 0)


class TestStep2SuppressionBehavior(TestDendriticCellBehaviorChanges):
    """Step 2: 抑制による振る舞い変化"""
    
    def test_suppressive_cytokine_stops_activation(self):
        """抑制性サイトカインが活性化を停止"""
        # まず活性化
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        self.dc.recognize_pattern(pathogen)
        self.assertTrue(self.dc.is_activated())
        
        # IL-10による抑制
        self.env.add_cytokine("IL-10", 20.0)
        
        # 活性化が停止する
        self.assertFalse(self.dc.is_activated())
    
    def test_suppressed_cell_cannot_produce_cytokines(self):
        """抑制された細胞はサイトカイン産生できない"""
        # 活性化してから抑制
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.recognize_pattern(pathogen)
        self.env.add_cytokine("IL-10", 20.0)
        
        # 初期レベルを記録
        initial_il12 = self.env.get_level("IL-12")
        
        # 新たな病原体に暴露
        pathogen2 = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.recognize_pattern(pathogen2)
        
        # サイトカイン産生されない
        self.assertEqual(self.env.get_level("IL-12"), initial_il12)


class TestStep3ExhaustionBehavior(TestDendriticCellBehaviorChanges):
    """Step 3: 疲弊状態の振る舞い"""
    
    def test_strong_suppression_causes_unresponsiveness(self):
        """強い抑制は完全な無反応状態を誘導"""
        # 活性化
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=100.0,
            molecular_signature="LPS"
        )
        self.dc.recognize_pattern(pathogen)
        
        # 強いTGF-β抑制
        self.env.add_cytokine("TGF-beta", 50.0)
        
        # 病原体認識能力自体を失う
        pathogen2 = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        result = self.dc.recognize_pattern(pathogen2)
        self.assertFalse(result)  # 認識自体が失敗
    
    def test_exhausted_cell_ignores_priming_signals(self):
        """疲弊状態では準備シグナルも無視"""
        # 疲弊状態にする
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.recognize_pattern(pathogen)
        self.env.add_cytokine("TGF-beta", 50.0)
        
        # 強いIFN-γでも準備状態にならない
        self.env.add_cytokine("IFN-gamma", 30.0)
        self.assertFalse(self.dc.is_primed())


class TestStep4RecoveryBehavior(TestDendriticCellBehaviorChanges):
    """Step 4: 回復の振る舞い"""
    
    def test_recovery_signal_restores_responsiveness(self):
        """回復シグナルが応答性を回復"""
        # 疲弊状態にする
        pathogen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.recognize_pattern(pathogen)
        self.env.add_cytokine("TGF-beta", 50.0)
        
        # 回復不能を確認
        pathogen2 = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.assertFalse(self.dc.recognize_pattern(pathogen2))
        
        # IL-2による回復
        self.env.add_cytokine("IL-2", 15.0)
        
        # 応答性回復を確認
        pathogen3 = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="flagellin"
        )
        self.assertTrue(self.dc.recognize_pattern(pathogen3))


if __name__ == '__main__':
    unittest.main()