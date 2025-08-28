import unittest
from unittest.mock import Mock
from ....model.antigen import Antigen


class TestAPCInterface(unittest.TestCase):
    """抗原提示細胞（APC）インターフェースのテスト"""
    
    def test_apc_interface_methods(self):
        """APCインターフェースが必要なメソッドを定義していることを確認"""
        from ....model.antigen_presenting_cell import AntigenPresentingCell
        
        # インターフェースが存在することを確認
        self.assertTrue(hasattr(AntigenPresentingCell, 'get_mhc_peptide_complexes'))
        self.assertTrue(hasattr(AntigenPresentingCell, 'get_costimulatory_signals'))
        self.assertTrue(hasattr(AntigenPresentingCell, 'is_activated'))
    
    def test_mock_apc_implementation(self):
        """モックAPCでインターフェースの使用例を確認"""
        # モックAPCを作成
        mock_apc = Mock()
        mock_apc.get_mhc_peptide_complexes.return_value = [("MHC-II", "viral_peptide")]
        mock_apc.get_costimulatory_signals.return_value = {"CD80": 1.0, "CD86": 0.5}
        mock_apc.is_activated.return_value = True
        
        # APCインターフェースとして使用可能
        complexes = mock_apc.get_mhc_peptide_complexes()
        self.assertIn(("MHC-II", "viral_peptide"), complexes)
        
        signals = mock_apc.get_costimulatory_signals()
        self.assertEqual(signals["CD80"], 1.0)
        
        self.assertTrue(mock_apc.is_activated())


class TestMacrophageAsAPC(unittest.TestCase):
    """マクロファージのAPC機能テスト"""
    
    def test_macrophage_implements_apc_interface(self):
        """マクロファージがAPCインターフェースを実装していることを確認"""
        from ....model.macrophage import Macrophage
        
        macrophage = Macrophage()
        
        # APCインターフェースのメソッドを持つ
        self.assertTrue(hasattr(macrophage, 'get_mhc_peptide_complexes'))
        self.assertTrue(hasattr(macrophage, 'get_costimulatory_signals'))
        self.assertTrue(hasattr(macrophage, 'is_activated'))
    
    def test_macrophage_initial_mhc_complexes_empty(self):
        """初期状態のマクロファージはMHC複合体を持たない"""
        from ....model.macrophage import Macrophage
        
        macrophage = Macrophage()
        complexes = macrophage.get_mhc_peptide_complexes()
        self.assertEqual(complexes, [])
    
    def test_macrophage_presents_antigen_after_phagocytosis(self):
        """貪食後にMHC-ペプチド複合体を提示"""
        from ....model.macrophage import Macrophage
        
        macrophage = Macrophage()
        viral_antigen = Antigen("virus", molecular_signature=["viral_RNA"])
        
        # 貪食前は複合体なし
        self.assertEqual(macrophage.get_mhc_peptide_complexes(), [])
        
        # 貪食
        macrophage.phagocytose(viral_antigen)
        
        # 貪食後はMHC-II複合体を提示
        complexes = macrophage.get_mhc_peptide_complexes()
        self.assertGreater(len(complexes), 0)
        self.assertEqual(complexes[0][0], "MHC-II")  # MHCクラスII
        self.assertEqual(complexes[0][1], "virus_peptide")  # ウイルス由来ペプチド
    
    def test_macrophage_costimulatory_signals_increase_with_activation(self):
        """活性化によって共刺激シグナルが増加"""
        from ....model.macrophage import Macrophage
        from ....model.cytokine_environment import CytokineEnvironment
        
        env = CytokineEnvironment()
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        
        # 初期の共刺激シグナルは低い
        initial_signals = macrophage.get_costimulatory_signals()
        self.assertLess(initial_signals.get("CD80", 0), 0.5)
        
        # IFN-γで活性化
        env.add_cytokine("IFN-gamma", 10.0)
        
        # 活性化後の共刺激シグナルは高い
        activated_signals = macrophage.get_costimulatory_signals()
        self.assertGreater(activated_signals.get("CD80", 0), 0.5)
        self.assertGreater(activated_signals.get("CD86", 0), 0.5)


class TestTCellAPCInteraction(unittest.TestCase):
    """T細胞とAPCの相互作用テスト"""
    
    def test_t_cell_can_scan_any_apc(self):
        """T細胞が任意のAPC実装をスキャンできる"""
        from ....model.t_cell import TCell
        
        t_cell = TCell(specificity=("MHC-II", "bacterial_peptide"))
        
        # モックAPCを作成
        mock_apc = Mock()
        mock_apc.get_mhc_peptide_complexes.return_value = [("MHC-II", "bacterial_peptide")]
        mock_apc.get_costimulatory_signals.return_value = {"CD80": 1.0}
        mock_apc.is_activated.return_value = True
        
        # T細胞がAPCをスキャン
        result = t_cell.scan_apc(mock_apc)
        self.assertTrue(result)
        self.assertTrue(t_cell.is_activated())
    
    def test_t_cell_requires_costimulation_for_activation(self):
        """T細胞の活性化には共刺激シグナルが必要"""
        from ....model.t_cell import TCell
        
        t_cell = TCell(specificity=("MHC-II", "viral_peptide"))
        
        # 共刺激シグナルが不十分なAPC
        weak_apc = Mock()
        weak_apc.get_mhc_peptide_complexes.return_value = [("MHC-II", "viral_peptide")]
        weak_apc.get_costimulatory_signals.return_value = {"CD80": 0.1, "CD86": 0.1}
        weak_apc.is_activated.return_value = False
        
        # MHCは一致するが共刺激不足で活性化しない
        result = t_cell.scan_apc(weak_apc)
        self.assertFalse(result)
        self.assertFalse(t_cell.is_activated())
        
        # 十分な共刺激シグナルを持つAPC
        strong_apc = Mock()
        strong_apc.get_mhc_peptide_complexes.return_value = [("MHC-II", "viral_peptide")]
        strong_apc.get_costimulatory_signals.return_value = {"CD80": 1.0, "CD86": 0.8}
        strong_apc.is_activated.return_value = True
        
        # 共刺激十分で活性化
        result = t_cell.scan_apc(strong_apc)
        self.assertTrue(result)
        self.assertTrue(t_cell.is_activated())