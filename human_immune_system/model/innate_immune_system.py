from .antigen import Antigen, AntigenType


class InnateImmuneSystem:
    def __init__(self, cytokine_environment):
        self._non_threatening_types = {AntigenType.SELF}
        self._known_pamps = {
            'LPS',           # 細菌のリポ多糖
            'dsRNA',         # ウイルスの二本鎖RNA
            'flagellin',     # 細菌のフラジェリン
            'peptidoglycan', # 細菌の細胞壁成分
            'beta_glucan',   # 真菌の細胞壁成分
        }
        self._environment = cytokine_environment
        self._dendritic_cells = []
        self._is_activated = False
    
    def recognize_pattern(self, antigen: Antigen) -> bool:
        """
        パターン認識受容体による分子パターンの認識
        分子シグネチャに基づく厳密な認識のみを行う
        """
        if not antigen:
            return False
        
        # 分子シグネチャに基づく認識のみ（生物学的に正確）
        return self._recognize_known_pamps(antigen)
    
    def _recognize_known_pamps(self, antigen: Antigen) -> bool:
        """
        既知のPAMPsシグネチャを認識する
        """
        if not antigen or not antigen.molecular_signature:
            return False
        
        # 単一のシグネチャの場合
        if isinstance(antigen.molecular_signature, str):
            return antigen.molecular_signature in self._known_pamps
        
        # 複数のシグネチャの場合
        if isinstance(antigen.molecular_signature, list):
            return any(sig in self._known_pamps for sig in antigen.molecular_signature)
        
        return False
    
    def add_dendritic_cell(self, dc):
        """樹状細胞を系に追加"""
        self._dendritic_cells.append(dc)
        self._environment.register_cell(dc)
        dc.enter_environment(self._environment)
    
    def antigen_exposure(self, antigen: Antigen) -> bool:
        """抗原暴露時の統合応答"""
        if not antigen:
            return False
        
        # 自然免疫のパターン認識
        pattern_recognized = self.recognize_pattern(antigen)
        
        # 全樹状細胞での並列認識
        dc_responses = []
        for dc in self._dendritic_cells:
            if dc.recognize_pattern(antigen):
                dc_responses.append(dc)
        
        # 統合的な活性化判定
        if pattern_recognized or dc_responses:
            self._is_activated = True
            return True
        return False
    
    def is_activated(self) -> bool:
        """自然免疫系の活性化状態"""
        return self._is_activated
    
    def get_immune_status(self) -> dict:
        """統合された免疫状態"""
        return {
            "system_activated": self._is_activated,
            "active_dcs": len([dc for dc in self._dendritic_cells if dc.is_activated()]),
            "primed_dcs": len([dc for dc in self._dendritic_cells if dc.is_primed()]),
            "cytokine_levels": self._environment._levels.copy()
        }
    
