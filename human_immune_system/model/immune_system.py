from .antigen import Antigen
from .innate_immune_system import InnateImmuneSystem


class ImmuneSystem:
    def __init__(self):
        self.immune_activation = False
        self.innate_system = InnateImmuneSystem()
    
    def antigen_exposure(self, antigen: Antigen):
        if antigen and self.innate_system.recognize_pattern(antigen):
            self.immune_activation = True
    
    def is_activated(self):
        return self.immune_activation
