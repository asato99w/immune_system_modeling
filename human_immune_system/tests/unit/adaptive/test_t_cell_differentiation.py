import unittest
from ....model.t_cell import TCell
from ....model.cytokine_environment import CytokineEnvironment
from ....model.dendritic_cell import DendriticCell
from ....model import Antigen, AntigenType


class TestTCellDifferentiation(unittest.TestCase):
    """T細胞の分化機能テスト"""
    
    def setUp(self):
        self.env = CytokineEnvironment()
        self.dc = DendriticCell()
        self.dc.enter_environment(self.env)
        self.env.register_cell(self.dc)
    
    def test_initial_differentiation_state(self):
        """初期状態では未分化"""
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        self.assertIsNone(t_cell.get_differentiation_type())
    
    def test_th1_differentiation_with_il12(self):
        """IL-12環境でTh1に分化"""
        # ウイルス抗原を貪食（IL-12産生を誘導）
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.phagocytose(viral_antigen)
        
        # T細胞を環境に登録して活性化
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        
        # 活性化（樹状細胞のMHC-ペプチド複合体を認識）
        t_cell.scan_dendritic_cell(self.dc)
        self.assertTrue(t_cell.is_activated())
        
        # 樹状細胞を活性化してIL-12産生
        self.dc.recognize_pattern(viral_antigen)
        
        # IL-12が十分にある環境でTh1に分化
        self.env.add_cytokine("IL-12", 10.0)
        t_cell.differentiate()
        
        self.assertEqual(t_cell.get_differentiation_type(), "Th1")
    
    def test_th2_differentiation_with_il4(self):
        """IL-4環境でTh2に分化"""
        # T細胞を準備
        t_cell = TCell(specificity=("MHC-II", "bacterial_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        
        # 活性化のため細菌抗原を貪食
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.phagocytose(bacterial_antigen)
        t_cell.scan_dendritic_cell(self.dc)
        
        # IL-4優勢環境でTh2に分化
        self.env.add_cytokine("IL-4", 8.0)
        t_cell.differentiate()
        
        self.assertEqual(t_cell.get_differentiation_type(), "Th2")
    
    def test_no_differentiation_without_activation(self):
        """未活性化T細胞は分化しない"""
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        
        # 活性化せずにサイトカイン環境を作る
        self.env.add_cytokine("IL-12", 10.0)
        
        # 分化を試みる
        t_cell.differentiate()
        
        # 未活性化なので分化しない
        self.assertIsNone(t_cell.get_differentiation_type())
    
    def test_th1_produces_ifn_gamma(self):
        """Th1細胞はIFN-γを産生"""
        # T細胞を活性化してTh1に分化
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.phagocytose(viral_antigen)
        
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        t_cell.scan_dendritic_cell(self.dc)
        
        self.env.add_cytokine("IL-12", 10.0)
        t_cell.differentiate()
        
        # Th1がサイトカインを産生
        initial_ifn = self.env.get_level("IFN-gamma")
        t_cell.produce_cytokines()
        final_ifn = self.env.get_level("IFN-gamma")
        
        self.assertGreater(final_ifn, initial_ifn)
    
    def test_th2_produces_il4(self):
        """Th2細胞はIL-4を産生"""
        # T細胞を活性化してTh2に分化
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.phagocytose(bacterial_antigen)
        
        t_cell = TCell(specificity=("MHC-II", "bacterial_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        t_cell.scan_dendritic_cell(self.dc)
        
        self.env.add_cytokine("IL-4", 8.0)
        t_cell.differentiate()
        
        # Th2がサイトカインを産生
        initial_il4 = self.env.get_level("IL-4")
        t_cell.produce_cytokines()
        final_il4 = self.env.get_level("IL-4")
        
        self.assertGreater(final_il4, initial_il4)
    
    def test_differentiation_is_permanent(self):
        """一度分化したら変更されない"""
        # Th1に分化
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.phagocytose(viral_antigen)
        
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        self.env.register_cell(t_cell)
        t_cell.enter_environment(self.env)
        t_cell.scan_dendritic_cell(self.dc)
        
        self.env.add_cytokine("IL-12", 10.0)
        t_cell.differentiate()
        self.assertEqual(t_cell.get_differentiation_type(), "Th1")
        
        # IL-4を追加しても変わらない
        self.env.add_cytokine("IL-4", 20.0)
        t_cell.differentiate()
        self.assertEqual(t_cell.get_differentiation_type(), "Th1")


if __name__ == '__main__':
    unittest.main()