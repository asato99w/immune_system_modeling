import unittest
from ....model import Antigen, AntigenType


class TestAntigen(unittest.TestCase):
    """統合されたAntigenクラステスト"""
    
    def test_antigen_creation_with_type_and_concentration(self):
        """抗原タイプと濃度での作成"""
        antigen = Antigen(antigen_type=AntigenType.VIRAL, concentration=100.0)
        
        self.assertEqual(antigen.antigen_type, AntigenType.VIRAL)
        self.assertEqual(antigen.concentration, 100.0)
        self.assertIsNone(antigen.molecular_signature)
    
    def test_antigen_creation_with_molecular_signature(self):
        """分子シグネチャ付きで作成"""
        antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        self.assertEqual(antigen.antigen_type, AntigenType.BACTERIAL)
        self.assertEqual(antigen.concentration, 50.0)
        self.assertEqual(antigen.molecular_signature, "LPS")
    
    def test_antigen_creation_with_multiple_signatures(self):
        """複数の分子シグネチャ付きで作成"""
        antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=75.0,
            molecular_signature=["LPS", "flagellin"]
        )
        
        self.assertEqual(antigen.molecular_signature, ["LPS", "flagellin"])
    
    def test_antigen_default_concentration(self):
        """デフォルト濃度"""
        antigen = Antigen(antigen_type=AntigenType.FUNGAL)
        
        self.assertEqual(antigen.concentration, 1.0)
        self.assertIsNone(antigen.molecular_signature)
    
    def test_antigen_decay(self):
        """抗原の減衰"""
        antigen = Antigen(antigen_type=AntigenType.VIRAL, concentration=100.0)
        initial_concentration = antigen.concentration
        
        antigen.decay(rate=0.1)
        
        self.assertLess(antigen.concentration, initial_concentration)
        self.assertAlmostEqual(antigen.concentration, 90.0)
    
    def test_all_antigen_types(self):
        """すべての抗原タイプの作成"""
        types = [
            AntigenType.VIRAL,
            AntigenType.BACTERIAL,
            AntigenType.FUNGAL,
            AntigenType.PARASITIC,
            AntigenType.SELF,
            AntigenType.TUMOR
        ]
        
        for antigen_type in types:
            antigen = Antigen(antigen_type=antigen_type)
            self.assertEqual(antigen.antigen_type, antigen_type)


if __name__ == '__main__':
    unittest.main()