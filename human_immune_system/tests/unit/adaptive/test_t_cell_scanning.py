import unittest
from ....model import Antigen, AntigenType
from ....model.dendritic_cell import DendriticCell
from ....model.t_cell import TCell


class TestTCellScanning(unittest.TestCase):
    """T細胞のMHC-ペプチド複合体スキャン機能のテスト"""
    
    def setUp(self):
        self.dc = DendriticCell()
    
    def test_t_cell_with_specificity(self):
        """T細胞は特定のMHC-ペプチド複合体に特異性を持つ"""
        # 特異性を持つT細胞を作成
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        
        # 特異性を確認
        self.assertEqual(t_cell.get_specificity(), ("MHC-II", "viral_peptide_1"))
    
    def test_scan_finds_matching_complex(self):
        """スキャンで一致する複合体を見つけると活性化"""
        # ウイルス抗原を貪食
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.phagocytose(viral_antigen)
        
        # viral_peptide_1に特異的なT細胞
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        
        # スキャン前は未活性
        self.assertFalse(t_cell.is_activated())
        
        # スキャンで複合体を認識
        recognized = t_cell.scan_dendritic_cell(self.dc)
        
        self.assertTrue(recognized)
        self.assertTrue(t_cell.is_activated())
    
    def test_scan_does_not_find_non_matching_complex(self):
        """一致しない複合体では活性化しない"""
        # 細菌抗原を貪食
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        self.dc.phagocytose(bacterial_antigen)
        
        # viral_peptide_1に特異的なT細胞（細菌ペプチドは認識しない）
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        
        # スキャンしても認識しない
        recognized = t_cell.scan_dendritic_cell(self.dc)
        
        self.assertFalse(recognized)
        self.assertFalse(t_cell.is_activated())
    
    def test_scan_empty_mhc_complexes(self):
        """MHC複合体がない樹状細胞では活性化しない"""
        # 貪食していない樹状細胞
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        
        recognized = t_cell.scan_dendritic_cell(self.dc)
        
        self.assertFalse(recognized)
        self.assertFalse(t_cell.is_activated())
    
    def test_activated_t_cell_remains_activated(self):
        """一度活性化したT細胞は活性化状態を維持"""
        # ウイルス抗原を貪食
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        self.dc.phagocytose(viral_antigen)
        
        t_cell = TCell(specificity=("MHC-II", "viral_peptide_1"))
        
        # 最初のスキャンで活性化
        t_cell.scan_dendritic_cell(self.dc)
        self.assertTrue(t_cell.is_activated())
        
        # 空の樹状細胞をスキャンしても活性化状態維持
        empty_dc = DendriticCell()
        t_cell.scan_dendritic_cell(empty_dc)
        self.assertTrue(t_cell.is_activated())


if __name__ == '__main__':
    unittest.main()