from typing import List, Tuple, Dict
from .antigen import Antigen


class Macrophage:
    """
    マクロファージ：貪食と炎症応答の中心的細胞
    病原体を貪食し、IFN-γにより活性化される
    APCインターフェースを実装し、T細胞に抗原提示を行う
    """
    
    def __init__(self):
        self._activation_level = 0  # 0-100のスケール
        self._environment = None
        self._phagocytosed_count = 0  # 貪食した病原体数
        self._mhc_peptide_complexes = []  # MHC-ペプチド複合体のリスト
        self._processed_antigens = []  # 処理済み抗原のリスト
    
    def is_activated(self) -> bool:
        """活性化状態かどうか（活性化レベル > 50）"""
        return self._activation_level > 50
    
    def get_activation_level(self) -> float:
        """活性化レベルを返す（0-100）"""
        return self._activation_level
    
    def phagocytose(self, antigen: Antigen) -> bool:
        """
        病原体を貪食し、抗原処理を行う
        
        Args:
            antigen: 貪食する抗原
            
        Returns:
            貪食に成功したかどうか
        """
        if not antigen:
            return False
        
        # 貪食成功
        self._phagocytosed_count += 1
        self._processed_antigens.append(antigen)
        
        # 抗原をペプチドに処理してMHCクラスIIに載せる
        self._process_antigen_to_mhc(antigen)
        
        # 貪食により軽度の活性化（最大30）
        activation_boost = min(10, 100 - self._activation_level)
        self._activation_level = min(self._activation_level + activation_boost, 30)
        
        # 活性化時はより効率的な貪食
        if self.is_activated():
            # 追加の活性化ボースト
            self._activation_level = min(self._activation_level + 5, 100)
        
        return True
    
    def _process_antigen_to_mhc(self, antigen: Antigen):
        """
        抗原をペプチドに処理してMHC-II複合体を形成
        
        Args:
            antigen: 処理する抗原
        """
        # 抗原タイプに基づいてペプチドを生成
        peptide = f"{antigen.antigen_type}_peptide"
        
        # MHCクラスII複合体を形成（細胞外抗原の提示）
        mhc_complex = ("MHC-II", peptide)
        
        # 複合体リストに追加（重複を避ける）
        if mhc_complex not in self._mhc_peptide_complexes:
            self._mhc_peptide_complexes.append(mhc_complex)
    
    def enter_environment(self, environment):
        """環境に参加"""
        self._environment = environment
        # オブザーバーとして登録
        environment.register_cell(self)
    
    def on_cytokine_changed(self, cytokine_name: str, level: float):
        """
        環境中のサイトカイン変化に反応
        特にIFN-γによる活性化
        """
        if cytokine_name == "IFN-gamma" and level > 5.0:
            # IFN-γによる強力な活性化
            # レベルに応じた活性化（最大100）
            activation = min(50 + level * 5, 100)
            self._activation_level = max(self._activation_level, activation)
        elif cytokine_name == "IL-10" and level > 10.0:
            # IL-10による抑制
            # 活性化レベルを低下
            suppression = min(level * 2, 50)
            self._activation_level = max(0, self._activation_level - suppression)
    
    def produce_cytokines(self):
        """
        活性化状態に応じてサイトカインを産生
        """
        if not self._environment:
            return
        
        if self.is_activated():
            # 活性化マクロファージはTNF-αとIL-1βを産生
            tnf_amount = self._activation_level / 20.0  # 0-5の範囲
            il1_amount = self._activation_level / 25.0  # 0-4の範囲
            
            self._environment.add_cytokine("TNF-alpha", tnf_amount)
            self._environment.add_cytokine("IL-1beta", il1_amount)
            
            # 高度に活性化されている場合はIL-12も産生（Th1誘導）
            if self._activation_level > 75:
                self._environment.add_cytokine("IL-12", 3.0)
    
    # APCインターフェースの実装
    def get_mhc_peptide_complexes(self) -> List[Tuple[str, str]]:
        """
        MHC-ペプチド複合体のリストを返す
        
        Returns:
            List of (MHC type, peptide) tuples
        """
        return self._mhc_peptide_complexes.copy()
    
    def get_costimulatory_signals(self) -> Dict[str, float]:
        """
        共刺激シグナルのレベルを返す
        活性化レベルに応じてCD80/CD86の発現が増加
        
        Returns:
            Dict of signal name to intensity (0.0 - 1.0)
        """
        if self.is_activated():
            # 活性化マクロファージは強い共刺激シグナルを発現
            cd80_level = min(self._activation_level / 100.0, 1.0)
            cd86_level = min(self._activation_level / 120.0, 0.8)
        else:
            # 非活性化状態では弱い共刺激シグナル
            cd80_level = self._activation_level / 200.0  # 最大0.25
            cd86_level = self._activation_level / 250.0  # 最大0.20
        
        return {
            "CD80": cd80_level,
            "CD86": cd86_level
        }