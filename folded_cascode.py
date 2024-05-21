import numpy as np
from tabulate import tabulate
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
        
        self.fp1 = 1 / (2 * np.pi * self.rout_val * self.CL)
        self.fp2 = self.M2.gm() / (2 * np.pi * 2 * self.M2.cgs())
        
    def av(self) -> float:
        return self.rout_val * self.GM_val
    
    def rout(self) -> float:
        return self.rout_val
    
    def poles(self) -> list[float]:
        return [self.fp1, self.fp2]

    def GM(self) -> float:
        return self.GM_val
    
    def size(self) -> dict[str, str]:
        W0 = str("{:.2e}".format(np.abs(float(self.M0.w_val))))
        W1 = str("{:.2e}".format(np.abs(float(self.M1.w_val))))
        W2 = str("{:.2e}".format(np.abs(float(self.M2.w_val))))
        W3 = str("{:.2e}".format(np.abs(float(self.M3.w_val))))
        W4 = str("{:.2e}".format(np.abs(float(self.M4.w_val))))
        W5 = str("{:.2e}".format(np.abs(float(self.M5.w_val))))
        return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5}
    
    def characterize(self, latex: bool) -> None:
        av  = np.round(20*np.log10(self.av()), 2)
        poles = self.poles()
        sizes = self.size()
        power = (self.itail * 4) * 1.2 # Assuming 1.2 VDD
        
        poles_formatted = []
        for pole in poles:
            poles_formatted.append(str("{:.2e}".format(pole)))
            
        table = [["1st Stage Gain"  , av    , "Output Pole" , poles[0]  , "M0", sizes["W0"], self.M0.gateL],
                 [None              , None  , "Mirror Pole" , poles[1]  , "M1", sizes["W1"], self.M1.gateL],
                 [None              , None  , None          , None      , "M2", sizes["W2"], self.M2.gateL],
                 [None              , None  , None          , None      , "M3", sizes["W3"], self.M3.gateL],
                 [None              , None  , None          , None      , "M4", sizes["W4"], self.M4.gateL],
                 [None              , None  , None          , None      , "M4", sizes["W5"], self.M5.gateL]]
        
        if latex:
            format = "latex"
        else:
            format = "fancy_outline"
        print(tabulate(table, headers=["Gain", "dB", "Pole", "Hz", "Device", "Width", "Length"], tablefmt=format, floatfmt=".2e"))
        print("Power Consumption: {:.2e} W".format(power))