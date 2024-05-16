import numpy as np
from utils import Utils
from transistor import MosDevice

# Full input-swing folded cascode
# P. 390 Razavi

class FoldedCascode:
    def __init__(self) -> None:
        self.utils = Utils()
        # input NMOS
        self.M0 = MosDevice()
        # input PMOS
        self.M1 = MosDevice()
        # NMOS Mirror
        self.M2 = MosDevice()
        # NMOS Mirror Cascode
        self.M3 = MosDevice()
        # PMOS CCS
        self.M4 = MosDevice()
        # PMOS CCS Cascode
        self.M5 = MosDevice()
        
        self.itail: float       = 0.0
        self.GM_val: float      = 0.0
        self.rout_val: float    = 0.0
        self.CL: float          = 0.0
        
        # Output Pole
        self.fp1: float     = 0.0
        # NMOS Mirror Pole
        self.fp2: float     = 0.0
        # NMOS Mirror Zero
        self.fz1: float     = 0.0
        
    def init(self) -> None:
        self.M0.set_id(self.itail/2)
        self.M1.set_id(self.itail/2)
        self.M2.set_id(self.itail)
        self.M3.set_id(self.itail/2)
        self.M4.set_id(self.itail)
        self.M5.set_id(self.itail/2)

        self.__calculate()
            
    def __calculate(self) -> None:
        # Assume worst case GM
        self.GM_val = min(self.M0.gm(), self.M1.gm())
        nmos_ro = self.utils.cascode(self.M2.ro(), self.M3.ro(), self.M3.gm())
        pmos_ro = self.utils.cascode(self.M4.ro(), self.M5.ro(), self.M5.gm())
        self.rout_val = self.utils.parallel([nmos_ro, pmos_ro])
        
        nmos_mirror_cap = 2*(self.M2.gm() / (2*np.pi*self.M2.ft()))
        
        self.fp1 = 1 / (2 * np.pi * self.rout_val * self.CL)
        self.fp2 = self.M2.gm() / (2 * np.pi * nmos_mirror_cap)
        self.fz1 = 2 * self.M2.gm() / (2 * np.pi * nmos_mirror_cap)
        
    def av(self) -> float:
        return self.rout_val * self.GM_val
    
    def rout(self) -> float:
        return self.rout_val
    
    def poles(self) -> list[float]:
        return [self.fp1, self.fp2]
    
    def zeros(self) -> list[float]:
        return [self.fz1]

    def GM(self) -> float:
        return self.GM_val