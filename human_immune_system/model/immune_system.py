from .antigen import Antigen
from .innate_immune_system import InnateImmuneSystem
from .cytokine_environment import CytokineEnvironment


class ImmuneSystem:
    def __init__(self):
        self._cytokine_environment = CytokineEnvironment()
        self._innate_system = InnateImmuneSystem(self._cytokine_environment)
    
    def antigen_exposure(self, antigen: Antigen):
        """統合型の抗原暴露（樹状細胞も含む）"""
        return self._innate_system.antigen_exposure(antigen)
    
    def is_activated(self):
        return self._innate_system.is_activated()
    
    def get_innate_system(self):
        """自然免疫系へのアクセス"""
        return self._innate_system
    
    def get_cytokine_environment(self):
        """サイトカイン環境へのアクセス"""
        return self._cytokine_environment
