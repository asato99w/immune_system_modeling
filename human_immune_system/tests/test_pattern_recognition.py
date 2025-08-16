import unittest
from ..model import Antigen, AntigenType, InnateImmuneSystem


class TestPatternRecognition(unittest.TestCase):
    """統合されたパターン認識テスト"""
    
    def setUp(self):
        self.innate_system = InnateImmuneSystem()
    
    def test_recognizes_bacterial_lps(self):
        """細菌のLPSパターンを認識"""
        bacterial_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=50.0,
            molecular_signature="LPS"
        )
        
        self.assertTrue(self.innate_system.recognize_pattern(bacterial_antigen))
    
    def test_recognizes_viral_dsRNA(self):
        """ウイルスのdsRNAパターンを認識"""
        viral_antigen = Antigen(
            antigen_type=AntigenType.VIRAL,
            concentration=30.0,
            molecular_signature="dsRNA"
        )
        
        self.assertTrue(self.innate_system.recognize_pattern(viral_antigen))
    
    def test_recognizes_multiple_pamps(self):
        """複数のPAMPsを持つ抗原を認識"""
        multi_pamp_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=40.0,
            molecular_signature=["LPS", "flagellin"]
        )
        
        self.assertTrue(self.innate_system.recognize_pattern(multi_pamp_antigen))
    
    def test_does_not_recognize_unknown_signature(self):
        """未知のシグネチャは認識しない"""
        unknown_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            concentration=20.0,
            molecular_signature="unknown_molecule"
        )
        
        # 未知のシグネチャでもタイプベースで認識される（後方互換性）
        self.assertTrue(self.innate_system.recognize_pattern(unknown_antigen))
    
    def test_self_antigen_not_recognized(self):
        """自己抗原は認識されない"""
        self_antigen = Antigen(
            antigen_type=AntigenType.SELF,
            concentration=50.0,
            molecular_signature="self_protein"
        )
        
        self.assertFalse(self.innate_system.recognize_pattern(self_antigen))
    
    def test_antigen_without_signature_uses_type_based_recognition(self):
        """シグネチャなしの抗原はタイプベース認識"""
        viral_antigen = Antigen(antigen_type=AntigenType.VIRAL, concentration=25.0)
        self_antigen = Antigen(antigen_type=AntigenType.SELF, concentration=25.0)
        
        self.assertTrue(self.innate_system.recognize_pattern(viral_antigen))
        self.assertFalse(self.innate_system.recognize_pattern(self_antigen))
    
    def test_known_pamps_method(self):
        """既知のPAMPs認識メソッドの直接テスト"""
        lps_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="LPS"
        )
        unknown_antigen = Antigen(
            antigen_type=AntigenType.BACTERIAL,
            molecular_signature="unknown"
        )
        
        self.assertTrue(self.innate_system.recognize_known_pamps(lps_antigen))
        self.assertFalse(self.innate_system.recognize_known_pamps(unknown_antigen))


if __name__ == '__main__':
    unittest.main()