from typing import Protocol, List, Tuple, Dict


class AntigenPresentingCell(Protocol):
    """
    抗原提示細胞（APC）のインターフェース
    
    樹状細胞、マクロファージ、B細胞などが実装する共通インターフェース
    T細胞はこのインターフェースを通じてAPCと相互作用する
    """
    
    def get_mhc_peptide_complexes(self) -> List[Tuple[str, str]]:
        """
        MHC-ペプチド複合体のリストを返す
        
        Returns:
            List of (MHC type, peptide) tuples
            例: [("MHC-II", "viral_peptide")]
        """
        ...
    
    def get_costimulatory_signals(self) -> Dict[str, float]:
        """
        共刺激シグナルのレベルを返す
        
        Returns:
            Dict of signal name to intensity (0.0 - 1.0)
            例: {"CD80": 0.8, "CD86": 0.6}
        """
        ...
    
    def is_activated(self) -> bool:
        """
        APCが活性化状態かどうか
        
        Returns:
            活性化状態の場合True
        """
        ...