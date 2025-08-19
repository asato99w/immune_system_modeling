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
        self._antigen_type = antigen_type
        self._concentration = concentration
        self._molecular_signature = molecular_signature
    
    @property
    def antigen_type(self) -> AntigenType:
        return self._antigen_type
    
    @property
    def concentration(self) -> float:
        return self._concentration
    
    @property
    def molecular_signature(self):
        return self._molecular_signature
    
    def decay(self, rate: float) -> None:
        self._concentration *= (1 - rate)