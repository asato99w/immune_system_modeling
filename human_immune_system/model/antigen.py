from enum import Enum


class AntigenType(Enum):
    VIRAL = "viral"
    BACTERIAL = "bacterial"
    FUNGAL = "fungal"
    PARASITIC = "parasitic"
    SELF = "self"
    TUMOR = "tumor"


class Antigen:
    def __init__(self, antigen_type: AntigenType, concentration: float = 1.0, molecular_signature=None):
        self.antigen_type = antigen_type
        self.concentration = concentration
        self.molecular_signature = molecular_signature
    
    def decay(self, rate: float) -> None:
        self.concentration *= (1 - rate)