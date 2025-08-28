import unittest
from ...model.macrophage import Macrophage
from ...model.t_cell import TCell
from ...model.antigen import Antigen
from ...model.cytokine_environment import CytokineEnvironment


class TestMacrophageTCellInteraction(unittest.TestCase):
    """マクロファージとT細胞の相互作用の統合テスト"""
    
    def test_t_cell_scans_macrophage_as_apc(self):
        """T細胞がマクロファージをAPCとしてスキャンできる"""
        # 環境を準備
        env = CytokineEnvironment()
        
        # マクロファージを作成
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        
        # 細菌抗原を貪食
        bacterial_antigen = Antigen("bacteria", molecular_signature=["LPS"])
        macrophage.phagocytose(bacterial_antigen)
        
        # T細胞を作成（細菌ペプチドに特異的）
        t_cell = TCell(specificity=("MHC-II", "bacteria_peptide"))
        
        # T細胞がマクロファージをスキャン
        result = t_cell.scan_apc(macrophage)
        
        # MHCは一致するが、共刺激不足で活性化しない（マクロファージ未活性化）
        self.assertFalse(result)
        self.assertFalse(t_cell.is_activated())
        
        # マクロファージを活性化
        env.add_cytokine("IFN-gamma", 10.0)
        
        # 別のT細胞で再度スキャン
        t_cell2 = TCell(specificity=("MHC-II", "bacteria_peptide"))
        result2 = t_cell2.scan_apc(macrophage)
        
        # 活性化マクロファージは十分な共刺激を持つ
        self.assertTrue(result2)
        self.assertTrue(t_cell2.is_activated())
    
    def test_positive_feedback_loop(self):
        """Th1細胞とマクロファージの正のフィードバックループ"""
        # 環境を準備
        env = CytokineEnvironment()
        
        # マクロファージを作成
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        
        # ウイルス抗原を貪食
        viral_antigen = Antigen("virus", molecular_signature=["dsRNA"])
        macrophage.phagocytose(viral_antigen)
        
        # マクロファージを強く活性化（IL-12産生のため75以上必要）
        env.add_cytokine("IFN-gamma", 15.0)
        
        # T細胞を作成して活性化
        t_cell = TCell(specificity=("MHC-II", "virus_peptide"))
        t_cell.enter_environment(env)
        result = t_cell.scan_apc(macrophage)
        self.assertTrue(result)
        
        # 活性化マクロファージがIL-12を産生
        initial_il12 = env.get_level("IL-12")
        macrophage.produce_cytokines()
        
        # 複数のマクロファージが存在する場合を想定して追加のIL-12
        macrophage.produce_cytokines()  # 2回目の産生
        
        il12_after = env.get_level("IL-12")
        self.assertGreater(il12_after, initial_il12)
        
        # IL-12レベルが分化に十分か確認（閾値は5.0）
        self.assertGreaterEqual(il12_after, 5.0, f"IL-12 level {il12_after} is not enough for Th1 differentiation")
        
        # IL-12によりT細胞がTh1に分化
        t_cell.differentiate()
        self.assertEqual(t_cell.get_differentiation_type(), "Th1")
        
        # Th1細胞がIFN-γを産生
        initial_ifn = env.get_level("IFN-gamma")
        t_cell.produce_cytokines()
        self.assertGreater(env.get_level("IFN-gamma"), initial_ifn)
        
        # IFN-γによりマクロファージが最大活性化を維持
        final_activation = macrophage.get_activation_level()
        # マクロファージは既に高度に活性化されている
        self.assertGreaterEqual(final_activation, 75)  # IL-12産生レベル
    
    def test_multiple_t_cells_scan_same_macrophage(self):
        """複数のT細胞が同じマクロファージをスキャン"""
        env = CytokineEnvironment()
        
        # マクロファージを準備
        macrophage = Macrophage()
        macrophage.enter_environment(env)
        
        # 複数の抗原を貪食
        bacterial_antigen = Antigen("bacteria", molecular_signature=["LPS"])
        viral_antigen = Antigen("virus", molecular_signature=["dsRNA"])
        macrophage.phagocytose(bacterial_antigen)
        macrophage.phagocytose(viral_antigen)
        
        # マクロファージを活性化
        env.add_cytokine("IFN-gamma", 10.0)
        
        # 異なる特異性を持つT細胞
        t_cell_bacterial = TCell(specificity=("MHC-II", "bacteria_peptide"))
        t_cell_viral = TCell(specificity=("MHC-II", "virus_peptide"))
        t_cell_nonspecific = TCell(specificity=("MHC-II", "fungal_peptide"))
        
        # それぞれがスキャン
        self.assertTrue(t_cell_bacterial.scan_apc(macrophage))
        self.assertTrue(t_cell_viral.scan_apc(macrophage))
        self.assertFalse(t_cell_nonspecific.scan_apc(macrophage))
        
        # 特異的T細胞のみ活性化
        self.assertTrue(t_cell_bacterial.is_activated())
        self.assertTrue(t_cell_viral.is_activated())
        self.assertFalse(t_cell_nonspecific.is_activated())
    
    def test_macrophage_antigen_processing_diversity(self):
        """マクロファージが異なる抗原を処理して提示"""
        macrophage = Macrophage()
        
        # 様々な抗原を貪食
        antigens = [
            Antigen("bacteria", molecular_signature=["LPS"]),
            Antigen("virus", molecular_signature=["dsRNA"]),
            Antigen("parasite"),
        ]
        
        for antigen in antigens:
            macrophage.phagocytose(antigen)
        
        # 各抗原のペプチドがMHC-IIに載る
        complexes = macrophage.get_mhc_peptide_complexes()
        self.assertEqual(len(complexes), 3)
        
        # すべてMHCクラスII
        for mhc_type, peptide in complexes:
            self.assertEqual(mhc_type, "MHC-II")
        
        # 異なるペプチドが提示されている
        peptides = [peptide for _, peptide in complexes]
        self.assertIn("bacteria_peptide", peptides)
        self.assertIn("virus_peptide", peptides)
        self.assertIn("parasite_peptide", peptides)