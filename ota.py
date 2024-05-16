import numpy as np
from utils import Utils
from transistor import MosDevice

# Three-mirror OTA
# "A Low-Power, Low-Noise CMOS Amplifier for Neural Recording Applications"
# Reid R. Harrison

class OTA:
    def __init__(self) -> None:
        self.utils = Utils()
        
        # Input PMOS
        self.M0 = MosDevice()
        
        # NMOS Mirror
        self.M1 = MosDevice()
        
        # NMOS Cascode
        self.M2 = MosDevice()
        
        # PMOS Mirror
        self.M3 = MosDevice()
        
        # PMOS Cascode
        self.M4 = MosDevice()
        
        self.itail: float       = 0.0
        self.GM_val: float      = 0.0
        self.rout_val: float    = 0.0
        self.CL: float          = 0.0
        
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
        
        self.__calculate()
            
    def __calculate(self) -> None:
        self.GM_val = self.M0.gm()
        nmos_ro = self.utils.cascode(self.M1.ro(), self.M2.ro(), self.M2.gm())
        pmos_ro = self.utils.cascode(self.M3.ro(), self.M4.ro(), self.M4.gm())
        self.rout_val = self.utils.parallel([nmos_ro, pmos_ro])
        
        self.fp1 = 1 / (2 * np.pi * self.rout_val * self.CL)
        self.fp2 = self.M1.gm() / (4 * np.pi * self.M1.cgg())
        self.fp3 = self.M1.gm() / (4 * np.pi * self.M1.cgg())
        self.fp4 = self.M3.gm() / (4 * np.pi * self.M3.cgg())
        
        self.av_val = self.rout_val * self.M0.gm()
        
    def av(self) -> float:
        return self.rout_val * self.GM_val
    
    def rout(self) -> float:
        return self.rout_val
    
    def poles(self) -> list[float]:
        return [self.fp1, self.fp2, self.fp3, self.fp4]
    
    def GM(self) -> float:
        return self.GM_val
    
    def size(self) -> dict[str, str]:
        W0 = str("{:.2e}".format(float(self.M0.w_val)))
        W1 = str("{:.2e}".format(float(self.M1.w_val)))
        W2 = str("{:.2e}".format(float(self.M2.w_val)))
        W3 = str("{:.2e}".format(float(self.M3.w_val)))
        W4 = str("{:.2e}".format(float(self.M4.w_val)))
        return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4}