from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .antigen_presenting_cell import AntigenPresentingCell


class TCell:
    """
    T細胞：獲得免疫の中心的細胞
    特定のMHC-ペプチド複合体を認識して活性化し、環境に応じて分化
    """
    
    def __init__(self, specificity=None):
        """
        Args:
            specificity: 認識する(MHCタイプ, ペプチド)のタプル
        """
        self._activated = False
        self._specificity = specificity
        self._differentiation_type = None  # "Th1", "Th2", or None
        self._environment = None
    
    def is_activated(self) -> bool:
        """活性化状態かどうか"""
        return self._activated
    
    def activate(self):
        """T細胞を活性化する"""
        if not self._activated:
            self._activated = True
    
    def get_specificity(self):
        """T細胞が認識するMHC-ペプチド複合体の特異性を返す"""
        return self._specificity
    
    def scan_dendritic_cell(self, dendritic_cell) -> bool:
        """
        樹状細胞のMHC-ペプチド複合体をスキャンして認識を試みる
        
        Args:
            dendritic_cell: スキャン対象の樹状細胞
            
        Returns:
            特異的複合体を認識したかどうか
        """
        if not self._specificity:
            return False
        
        # 樹状細胞が提示している複合体をスキャン
        complexes = dendritic_cell.get_mhc_peptide_complexes()
        
        for complex in complexes:
            if complex == self._specificity:
                # 特異的複合体を認識したら活性化
                self.activate()
                return True
        
        return False
    
    def scan_apc(self, apc: 'AntigenPresentingCell') -> bool:
        """
        抗原提示細胞（APC）のMHC-ペプチド複合体をスキャンして認識を試みる
        共刺激シグナルも考慮して活性化を決定
        
        Args:
            apc: スキャン対象のAPC（樹状細胞、マクロファージなど）
            
        Returns:
            特異的複合体を認識して活性化したかどうか
        """
        if not self._specificity:
            return False
        
        # すでに活性化済みの場合は再活性化しない
        if self._activated:
            return False
        
        # APCが提示している複合体をスキャン
        complexes = apc.get_mhc_peptide_complexes()
        
        # 特異的複合体を探す
        found_match = False
        for complex in complexes:
            if complex == self._specificity:
                found_match = True
                break
        
        if not found_match:
            return False
        
        # 共刺激シグナルを確認（Signal 2）
        costim_signals = apc.get_costimulatory_signals()
        cd80_level = costim_signals.get("CD80", 0)
        cd86_level = costim_signals.get("CD86", 0)
        
        # 共刺激シグナルが十分な場合のみ活性化
        # CD80またはCD86が閾値（0.3）以上必要
        if cd80_level >= 0.3 or cd86_level >= 0.3:
            self.activate()
            return True
        
        return False
    
    def enter_environment(self, environment):
        """環境に参加"""
        self._environment = environment
        # オブザーバーとして登録
        environment.register_cell(self)
    
    def get_differentiation_type(self):
        """分化タイプを返す"""
        return self._differentiation_type
    
    def differentiate(self):
        """
        環境中のサイトカインに基づいて分化
        活性化されたT細胞のみ分化可能
        """
        # 未活性化または既に分化済みなら何もしない
        if not self._activated or self._differentiation_type is not None:
            return
        
        if not self._environment:
            return
        
        # サイトカインレベルを確認
        il12_level = self._environment.get_level("IL-12")
        il4_level = self._environment.get_level("IL-4")
        
        # 優勢なサイトカインに基づいて分化
        if il12_level > il4_level and il12_level >= 5.0:
            # IL-12優勢でTh1に分化
            self._differentiation_type = "Th1"
        elif il4_level > il12_level and il4_level >= 5.0:
            # IL-4優勢でTh2に分化
            self._differentiation_type = "Th2"
    
    def produce_cytokines(self):
        """
        分化タイプに応じたサイトカインを産生
        """
        if not self._environment or not self._differentiation_type:
            return
        
        if self._differentiation_type == "Th1":
            # Th1はIFN-γを産生
            self._environment.add_cytokine("IFN-gamma", 5.0)
        elif self._differentiation_type == "Th2":
            # Th2はIL-4を産生
            self._environment.add_cytokine("IL-4", 3.0)
    
    def on_cytokine_changed(self, cytokine_name: str, level: float):
        """
        環境中のサイトカイン変化に反応
        活性化後の分化誘導に使用
        """
        # 活性化されていて未分化の場合のみ反応
        if self._activated and self._differentiation_type is None:
            # 分化を試みる
            self.differentiate()