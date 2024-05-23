import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from tabulate import tabulate
from utils import Utils
from transistor import MosDevice

# Full input-swing folded cascode
# P. 390 Razavi

class FoldedCascode:
    def __init__(self) -> None:
        self.utils = Utils()
        # Closed loop gain
        self.cl_gain: float = 0.0
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
        # 2nd stage NMOS
        self.M6 = MosDevice()
        # 2nd stage PMOS
        self.M7 = MosDevice()
        # Miller capacitor
        self.Cc:float           = 0.0
        # Output stage currnet
        self.iout: float        = 0.0
        # Input pair tail current
        self.itail: float       = 0.0
        # 1st stage gm
        self.gm_1st: float      = 0.0
        # 1st stage output resistance
        self.rout_1st: float    = 0.0
        # 2nd stage gm
        self.gm_2nd: float      = 0.0
        # 2nd stage output resistance
        self.rout_2nd: float    = 0.0
        # 1st stage gain
        self.av_1st: float      = 0.0
        # 2nd stage gain
        self.av_2nd: float      = 0.0
        # 2nd stage load capacitor
        self.CL: float          = 0.0
        # Dominant miller pole
        self.fp1: float     = 0.0
        # Output pole
        self.fp2: float     = 0.0
        # 1st stage mirror pole
        self.fp3: float     = 0.0

        self.twostage: bool = False
        
    def init(self) -> None:
        self.M0.set_id(self.itail/2)
        self.M1.set_id(self.itail/2)
        self.M2.set_id(self.itail)
        self.M3.set_id(self.itail/2)
        self.M4.set_id(self.itail)
        self.M5.set_id(self.itail/2)
        if self.twostage:
            self.M6.set_id(self.iout)
            self.M7.set_id(self.iout)

        self.__calculate()
            
    def __calculate(self) -> None:
        # Assume worst case GM
        self.gm_1st = min(self.M0.gm(), self.M1.gm())
        pmos_ro_1st = self.utils.cascode(self.M4.ro(), self.M5.ro(), self.M5.gm())
        nmos_ro_1st = self.utils.cascode(self.M2.ro(), self.M3.ro(), self.M3.gm())
        self.rout_1st = self.utils.parallel([pmos_ro_1st, nmos_ro_1st])
        self.av_1st = self.rout_1st * self.gm_1st

        if self.twostage:
            self.gm_2nd   = self.M6.gm()
            self.rout_2nd = self.utils.parallel([self.M6.ro(), self.M7.ro()])
            self.av_2nd   = self.rout_2nd * self.gm_2nd
            self.fp1 = (1 / (2 * np.pi * self.Cc * (1 + self.av_2nd) * self.rout_1st))
            self.fp2 = (self.M6.gm() / (2 * np.pi * self.CL))
            self.fp3 = (self.M2.gm() / (2 * np.pi * self.M2.cgs()))
            self.fp4 = (self.M3.gm() / (2 * np.pi * 3 * self.M1.cgs()))
        else:
            self.fp1 = 1 / (2 * np.pi * self.rout_1st * self.CL)
            self.fp2 = self.M2.gm() / (2 * np.pi * self.M2.cgs())
        
    def av(self) -> float:
        if self.twostage:
            return self.av_1st * self.av_2nd
        else:
            return self.av_1st
    
    def rout(self) -> float:
        if self.twostage:
            return self.rout_2nd
        else:
            return self.rout_1st
    
    def poles(self) -> list[float]:
        if self.twostage:
            return [self.fp1, self.fp2, self.fp3, self.fp4]
        else:
            return [self.fp1, self.fp2]
    
    def size(self) -> dict[str, str]:
        W0 = str("{:.2e}".format(np.abs(float(self.M0.w_val))))
        W1 = str("{:.2e}".format(np.abs(float(self.M1.w_val))))
        W2 = str("{:.2e}".format(np.abs(float(self.M2.w_val))))
        W3 = str("{:.2e}".format(np.abs(float(self.M3.w_val))))
        W4 = str("{:.2e}".format(np.abs(float(self.M4.w_val))))
        W5 = str("{:.2e}".format(np.abs(float(self.M5.w_val))))
        if self.twostage:
            W6 = str("{:.2e}".format(np.abs(float(self.M6.w_val))))
            W7 = str("{:.2e}".format(np.abs(float(self.M7.w_val))))
            return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5, "W6": W6, "W7": W7}
        else:
            return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4, "W5": W5}
    
    def characterize(self, latex: bool) -> None:
        av   = np.round(20*np.log10(self.av()), 2)
        poles = self.poles()
        sizes = self.size()
        power = (self.itail * 4) * 1.2 # Assuming 1.2 VDD
        
        poles_formatted = []
        for pole in poles:
            poles_formatted.append(str("{:.2e}".format(pole)))
        
        if self.twostage:
            av1  = np.round(20*np.log10(self.av_1st), 2)
            av2  = np.round(20*np.log10(self.av_2nd), 2)
            table = [["1st Stage Gain"  , av1   , "Dominant Pole"   , poles[0]  , "M0", sizes["W0"], self.M0.gateL],
                    ["2nd Stage Gain"   , av2   , "Output Pole"     , poles[1]  , "M1", sizes["W1"], self.M1.gateL],
                    ["Total Gain"       , av    , "Mirror Pole"     , poles[2]  , "M2", sizes["W2"], self.M2.gateL],
                    [None              , None   , "Cascode Pole"    , poles[3]  , "M3", sizes["W3"], self.M3.gateL],
                    [None              , None   , None              , None      , "M4", sizes["W4"], self.M4.gateL],
                    [None              , None   , None              , None      , "M5", sizes["W5"], self.M5.gateL],
                    [None              , None   , None              , None      , "M6", sizes["W6"], self.M5.gateL],
                    [None              , None   , None              , None      , "M7", sizes["W7"], self.M5.gateL]]
        else:
            table = [["1st Stage Gain" , av    , "Output Pole" , poles[0]  , "M0", sizes["W0"], self.M0.gateL],
                    [None              , None  , "Mirror Pole" , poles[1]  , "M1", sizes["W1"], self.M1.gateL],
                    [None              , None  , None          , None      , "M2", sizes["W2"], self.M2.gateL],
                    [None              , None  , None          , None      , "M3", sizes["W3"], self.M3.gateL],
                    [None              , None  , None          , None      , "M4", sizes["W4"], self.M4.gateL],
                    [None              , None  , None          , None      , "M5", sizes["W5"], self.M5.gateL]]
        
        if latex:
            format = "latex"
        else:
            format = "fancy_outline"
        print(tabulate(table, headers=["Gain", "dB", "Pole", "Hz", "Device", "Width", "Length"], tablefmt=format, floatfmt=".2e"))
        print("Power Consumption: {:.2e} W".format(power))
        
    def bode(self) -> None:
        if not self.twostage:
            return
        poles = self.poles()
        p1 = poles[0]
        p2 = poles[1]
        p3 = poles[2]
        den3 = [1, p1+p2+p3, p1*p2+p3*p1+p2*p3, p1*p2*p3]
        K = den3[-1] * self.av()
        
        w = np.logspace(1, 9, 1000)
        sys = sp.signal.TransferFunction([K], den3)
        w, mag, phase = sp.signal.bode(sys, w)

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)

        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Magnitude [dB]')
        ax.semilogx(w, mag)

        ax2 = ax.twinx()
        ax2.semilogx(w, phase, color="red")
        ax2.set_ylabel('Phase [deg]')
        ax.grid()

        for i in range(0, len(mag)):
            if mag[i] < self.cl_gain:
                print("Phase Margin: {}".format(180+phase[i]))
                break

        plt.title("Gain (Blue), Phase (Red)")
        fig.tight_layout()
        plt.show()