from transistor import MosDevice
import numpy as np

# Full input-swing folded cascode
# P. 390 Razavi

class FoldedCascode:
    def __init__(self) -> None:
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
        
        self.itail: float   = 0.0
        self.GM_val: float      = 0.0
        self.av_val: float      = 0.0
        self.rout_val: float    = 0.0
        self.CL: float      = 0.0
        
        # Output Pole
        self.fp1: float     = 0.0
        # NMOS Mirror Pole
        self.fp2: float     = 0.0
        # NMOS Mirror Pole
        self.fp3: float     = 0.0
        # PMOS Mirror Pole
        self.fp4: float     = 0.0
        
    def init(self) -> None:
        self.M0.set_id(self.itail/2)
        self.M1.set_id(self.itail/2)
        self.M2.set_id(self.itail/2)
        self.M3.set_id(self.itail/2)
        self.M4.set_id(self.itail/2)
        self.M5.set_id(self.itail/2)

        self.__calculate()
            
    def __parallel(self, R1: float, R2: float) -> float:
        return R1 * R2 / (R1 + R2)
    
    def __cascode(self, rO1: float, rO2: float, gm2: float) -> float:
        return (1 + gm2 * rO2) * rO1 + rO2
            
    def __calculate(self) -> None:
        # Assume worst case GM
        self.GM_val = min(self.M0.gm(), self.M1.gm())
        nmos_ro = self.__cascode(self.M2.ro(), self.M3.ro(), self.M3.gm())
        pmos_ro = self.__cascode(self.M4.ro(), self.M5.ro(), self.M5.gm())
        self.rout_val = self.__parallel(nmos_ro, pmos_ro)
        self.av_val = self.rout_val * self.GM_val
        
        self.fp1 = 1 / (2 * np.pi * self.rout_val * self.CL)
        
    def av(self) -> float:
        return self.av_val
    
    def rout(self) -> float:
        return self.rout_val
    
    def poles(self) -> list[float]:
        return [self.fp1]

    def GM(self) -> float:
        return self.GM_val