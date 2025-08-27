import unittest
from ....model import Antigen, AntigenType
from ....model.dendritic_cell import DendriticCell


class TestDendriticCellPhagocytosis(unittest.TestCase):
    """樹状細胞の貪食とMHC提示機能のテスト"""
    
    def test_initial_mhc_complexes_empty(self):
        """初期状態ではMHC-ペプチド複合体リストは空"""
        dc = DendriticCell()
        complexes = dc.get_mhc_peptide_complexes()
        self.assertEqual(len(complexes), 0)
    
    def test_phagocytosis_creates_mhc_peptide_complexes(self):
        """貪食によりMHC-ペプチド複合体が生成される"""
        dc = DendriticCell()
        
        # ウイルス抗原を貪食
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        dc.phagocytose(viral_antigen)
        
        # MHC-ペプチド複合体が生成される
        complexes = dc.get_mhc_peptide_complexes()
        self.assertGreater(len(complexes), 0)
        
        # 複合体の構造を確認（MHCタイプ, ペプチド）
        first_complex = complexes[0]
        self.assertEqual(len(first_complex), 2)  # タプル
        mhc_type, peptide = first_complex
        self.assertIsNotNone(mhc_type)
        self.assertIsNotNone(peptide)
    
    def test_different_antigens_produce_different_peptides(self):
        """異なる抗原から異なるペプチドが生成される"""
        dc = DendriticCell()
        
        # ウイルス抗原
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            molecular_signature="dsRNA"
        )
        dc.phagocytose(viral_antigen)
        viral_complexes = dc.get_mhc_peptide_complexes()
        
        # 細菌抗原
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        dc.phagocytose(bacterial_antigen)
        all_complexes = dc.get_mhc_peptide_complexes()
        
        # 両方の抗原由来のペプチドが存在
        self.assertGreater(len(all_complexes), len(viral_complexes))
    
    def test_mhc_class_ii_for_extracellular_antigens(self):
        """細胞外抗原はMHCクラスIIで提示される"""
        dc = DendriticCell()
        
        # 細菌抗原（細胞外）
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        dc.phagocytose(bacterial_antigen)
        
        complexes = dc.get_mhc_peptide_complexes()
        mhc_type, peptide = complexes[0]
        
        # MHCクラスIIで提示（簡略化：HLA-DRなど）
        self.assertIn("MHC-II", mhc_type)


if __name__ == '__main__':
    unittest.main()