from enum import Enum
from .antigen import Antigen, AntigenType


class DendriticCellState(Enum):
    """
    樹状細胞の生物学的状態
    実際の免疫系における状態遷移を反映
    """
    RESTING = "resting"      # 静止状態：初期状態、通常の監視活動
    PRIMED = "primed"        # 準備状態：環境シグナル（IFN-γ等）による警戒態勢
    ACTIVATED = "activated"  # 活性化状態：病原体認識による完全活性化
    SUPPRESSED = "suppressed"  # 抑制状態：IL-10による一時的無反応
    EXHAUSTED = "exhausted"  # 疲弊状態：TGF-βによる完全無反応


# サイトカイン応答の閾値
CYTOKINE_THRESHOLDS = {
    "priming": {
        "IFN-gamma": 5.0,
        "TNF-alpha": 15.0,
    },
    "suppression": {
        "IL-10": 10.0,
    },
    "exhaustion": {
        "TGF-beta": 30.0,
    },
    "recovery": {
        "IL-2": 10.0,
    }
}


class DendriticCell:
    """
    樹状細胞：免疫系の警報細胞
    ラルフ・スタインマンによって発見された、パターン認識と警報発信の専門細胞
    """
    
    def __init__(self):
        self._state = DendriticCellState.RESTING
        self._recognized_patterns = []
        self._environment = None  # 所属する環境
        
        # PAMPs認識能力（InnateImmuneSystemと同様）
        self._known_pamps = {
            'LPS',           # 細菌のリポ多糖
            'dsRNA',         # ウイルスの二本鎖RNA
            'flagellin',     # 細菌のフラジェリン
            'peptidoglycan', # 細菌の細胞壁成分
            'beta_glucan',   # 真菌の細胞壁成分
        }
        self._non_threatening_types = {AntigenType.SELF}
    
    def recognize_pattern(self, antigen: Antigen) -> bool:
        """
        パターン認識受容体による抗原認識
        認識に成功すると自動的にシグナル処理を開始
        """
        if not antigen:
            return False
        
        # 疲弊状態や抑制状態では認識不能
        if self._state in [DendriticCellState.EXHAUSTED, DendriticCellState.SUPPRESSED]:
            return False
        
        # 自己抗原は認識するが活性化はしない
        if antigen.antigen_type in self._non_threatening_types:
            return False
        
        # 分子シグネチャに基づく認識のみ（生物学的に正確）
        recognized = self._recognize_known_pamps(antigen)
        
        # 認識した抗原を記録し、自動的にシグナル処理
        if recognized:
            self._recognized_patterns.append(antigen)
            self._process_signals()  # 自律的に処理開始
        
        return recognized
    
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
    
    def _is_suppressed(self) -> bool:
        """
        抑制状態かどうかを判定
        環境中の抑制性サイトカインレベルをチェック
        """
        if not self._environment:
            return False
        
        # IL-10による抑制
        il10_level = self._environment.get_level("IL-10")
        if il10_level > 10.0:
            return True
        
        return False
    
    def _process_signals(self):
        """
        認識したパターンに基づいてシグナル処理
        活性化とサイトカイン産生の決定
        処理後はパターンをクリア（一度の処理で消費）
        """
        if not self._recognized_patterns:
            return
        
        # 脅威レベルの計算
        total_threat_level = 0.0
        for antigen in self._recognized_patterns:
            threat_level = antigen.concentration / 10.0  # 濃度を0-10スケールに正規化
            
            # 特定のPAMPsは強い応答を誘導
            if hasattr(antigen, 'molecular_signature'):
                if antigen.molecular_signature == "LPS":
                    threat_level *= 2.0  # LPSは強力な活性化因子
                elif antigen.molecular_signature == "dsRNA":
                    threat_level *= 1.5  # ウイルスRNAも強い応答
            
            total_threat_level += threat_level
        
        # 活性化の決定
        if total_threat_level > 0:
            # 準備状態かどうかを事前にチェック（活性化前の状態）
            was_primed = (self._state == DendriticCellState.PRIMED)
            self._state = DendriticCellState.ACTIVATED
            
            # 環境にサイトカインを産生
            if self._environment:
                cytokine_production = min(total_threat_level, 10.0)  # 最大値を10に制限
                
                # 準備状態からの活性化では産生量が増幅（プライミング効果）
                amplification = 2.0 if was_primed else 1.0
                
                self._environment.add_cytokine("IL-12", cytokine_production * 2.0 * amplification)     # Th1誘導
                self._environment.add_cytokine("TNF-alpha", cytokine_production * 1.5 * amplification)  # 炎症促進
                self._environment.add_cytokine("IL-6", cytokine_production * 1.8 * amplification)      # 急性期応答
        
        # 処理済みのパターンをクリア（次の認識に備える）
        self._recognized_patterns.clear()
    
    def is_activated(self) -> bool:
        """
        樹状細胞の活性化状態を返す
        """
        return self._state == DendriticCellState.ACTIVATED
    
    def enter_environment(self, environment):
        """環境に参加"""
        self._environment = environment
    
    def on_cytokine_changed(self, cytokine_name: str, level: float):
        """
        環境中のサイトカイン変化に反応
        """
        # TGF-βによる疲弊状態誘導（最優先でチェック）
        if cytokine_name == "TGF-beta" and level > CYTOKINE_THRESHOLDS["exhaustion"]["TGF-beta"]:
            self._state = DendriticCellState.EXHAUSTED
            return  # 疲弊状態では他のシグナルを無視
        
        # IL-2による疲弊状態からの回復（疲弊状態でも処理される）
        if (cytokine_name == "IL-2" and 
            level > CYTOKINE_THRESHOLDS["recovery"]["IL-2"] and 
            self._state == DendriticCellState.EXHAUSTED):
            self._state = DendriticCellState.RESTING
            return
        
        # 疲弊状態では他のシグナルに反応しない
        if self._state == DendriticCellState.EXHAUSTED:
            return
        
        # IL-10による抑制状態
        if cytokine_name == "IL-10" and level > CYTOKINE_THRESHOLDS["suppression"]["IL-10"]:
            self._state = DendriticCellState.SUPPRESSED
            return
        
        # IFN-γによる準備状態
        if (cytokine_name == "IFN-gamma" and 
            level > CYTOKINE_THRESHOLDS["priming"]["IFN-gamma"] and
            self._state == DendriticCellState.RESTING):
            self._state = DendriticCellState.PRIMED
        
        # TNF-αによる準備状態
        if (cytokine_name == "TNF-alpha" and 
            level >= CYTOKINE_THRESHOLDS["priming"]["TNF-alpha"] and
            self._state == DendriticCellState.RESTING):
            self._state = DendriticCellState.PRIMED
    
    def is_primed(self) -> bool:
        """準備状態を返す"""
        return self._state == DendriticCellState.PRIMED