from .antigen import Antigen, AntigenType


class InnateImmuneSystem:
    def __init__(self):
        self.non_threatening_types = {AntigenType.SELF}
        self.known_pamps = {
            'LPS',           # 細菌のリポ多糖
            'dsRNA',         # ウイルスの二本鎖RNA
            'flagellin',     # 細菌のフラジェリン
            'peptidoglycan', # 細菌の細胞壁成分
            'beta_glucan',   # 真菌の細胞壁成分
        }
    
    def recognize_pattern(self, antigen: Antigen) -> bool:
        """
        パターン認識受容体による分子パターンの認識
        molecular_signatureがあればそれを優先、なければantigen_typeで判定
        """
        if not antigen:
            return False
        
        # molecular_signatureがあればPAMPs認識を試行
        if hasattr(antigen, 'molecular_signature') and antigen.molecular_signature:
            if self.recognize_known_pamps(antigen):
                return True
        
        # 従来のタイプベース認識（後方互換性）
        return antigen.antigen_type not in self.non_threatening_types
    
    def recognize_known_pamps(self, antigen: Antigen) -> bool:
        """
        既知のPAMPsシグネチャを認識する
        """
        if not antigen or not antigen.molecular_signature:
            return False
        
        # 単一のシグネチャの場合
        if isinstance(antigen.molecular_signature, str):
            return antigen.molecular_signature in self.known_pamps
        
        # 複数のシグネチャの場合
        if isinstance(antigen.molecular_signature, list):
            return any(sig in self.known_pamps for sig in antigen.molecular_signature)
        
        return False
    
