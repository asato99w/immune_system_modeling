from .antigen import Antigen


class Macrophage:
    """
    マクロファージ：貪食と炎症応答の中心的細胞
    病原体を貪食し、IFN-γにより活性化される
    """
    
    def __init__(self):
        self._activation_level = 0  # 0-100のスケール
        self._environment = None
        self._phagocytosed_count = 0  # 貪食した病原体数
    
    def is_activated(self) -> bool:
        """活性化状態かどうか（活性化レベル > 50）"""
        return self._activation_level > 50
    
    def get_activation_level(self) -> float:
        """活性化レベルを返す（0-100）"""
        return self._activation_level
    
    def phagocytose(self, antigen: Antigen) -> bool:
        """
        病原体を貪食
        
        Args:
            antigen: 貪食する抗原
            
        Returns:
            貪食に成功したかどうか
        """
        if not antigen:
            return False
        
        # 貪食成功
        self._phagocytosed_count += 1
        
        # 貪食により軽度の活性化（最大30）
        activation_boost = min(10, 100 - self._activation_level)
        self._activation_level = min(self._activation_level + activation_boost, 30)
        
        # 活性化時はより効率的な貪食
        if self.is_activated():
            # 追加の活性化ボースト
            self._activation_level = min(self._activation_level + 5, 100)
        
        return True
    
    def enter_environment(self, environment):
        """環境に参加"""
        self._environment = environment
    
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