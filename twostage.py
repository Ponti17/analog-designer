import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from tabulate import tabulate
from utils import Utils
from transistor import MosDevice

# Two Stage Amplifier
# Kenneth Martin p. 243

class TwoStage:
    def __init__(self) -> None:
        self.utils = Utils()
        # Closed loop gain
        self.cl_gain: float = 0.0
        # Input PMOS
        self.M0 = MosDevice()
        # NMOS Mirror
        self.M1 = MosDevice()
        # NMOS Mirror Cascode
        self.M2 = MosDevice()
        # NMOS 2nd stage
        self.M3 = MosDevice()
        # PMOS 2nd stage load
        self.M4 = MosDevice()
        # Input Cascode
        self.M5 = MosDevice()
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
        
        self.cascode_mirror: bool = False
        self.cascode_input: bool  = False
        
    def init(self) -> None:
        self.M0.set_id(self.itail/2)
        self.M1.set_id(self.itail/2)
        self.M2.set_id(self.itail/2)
        self.M3.set_id(self.iout)
        self.M4.set_id(self.iout)
        self.M5.set_id(self.itail/2)
        
        self.__calculate()
            
    def __calculate(self) -> None:
        self.gm_1st = self.M0.gm()
        self.gm_2nd = self.M3.gm()
        
        if self.cascode_input:
            pmos_ro_1st     = self.utils.cascode(self.M1.ro(), self.M5.ro(), self.M5.gm())
        else:
            pmos_ro_1st     = self.M0.ro()
        if self.cascode_mirror:
            mirror_ro_1st   = self.utils.cascode(self.M1.ro(), self.M2.ro(), self.M2.gm())
        else:
            mirror_ro_1st   = self.M1.ro()
        self.rout_1st   = self.utils.parallel([pmos_ro_1st, mirror_ro_1st])
        self.av_1st     = self.rout_1st * self.gm_1st

        self.rout_2nd   = self.utils.parallel([self.M3.ro(), self.M4.ro()])
        self.av_2nd     = self.rout_2nd * self.gm_2nd
        
        self.fp1 = (1 / (2 * np.pi * self.Cc * (1 + self.av_2nd) * self.rout_1st))
        self.fp2 = (self.M3.gm() / (2 * np.pi * (self.CL + self.M3.cgg())))
        self.fp3 = (self.M1.gm() / (2 * np.pi * 0.5 * self.M1.cgs()))
        
    def av(self) -> float:
        return self.av_1st * self.av_2nd
    
    def rout(self) -> float:
        return self.rout_2nd
    
    def poles(self) -> list[float]:
        return [self.fp1, self.fp2, self.fp3]
    
    def size(self) -> dict[str, str]:
        W0 = str("{:.2e}".format(np.abs(float(self.M0.w_val))))
        W1 = str("{:.2e}".format(np.abs(float(self.M1.w_val))))
        W2 = str("{:.2e}".format(np.abs(float(self.M2.w_val))))
        W3 = str("{:.2e}".format(np.abs(float(self.M3.w_val))))
        W4 = str("{:.2e}".format(np.abs(float(self.M4.w_val))))
        return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4}
    
    def characterize(self, latex: bool) -> None:
        av1 = np.round(20*np.log10(self.av_1st), 2)
        av2 = np.round(20*np.log10(self.av_2nd), 2)
        av  = np.round(20*np.log10(self.av()), 2)
        poles = self.poles()
        sizes = self.size()
        power = (self.itail + self.iout) * 1.2 # Assuming 1.2 VDD
        
        poles_formatted = []
        for pole in poles:
            poles_formatted.append(str("{:.2e}".format(pole)))
            
        table = [["1st Stage Gain", av1, "Dominant Pole",   poles[0], "M0", sizes["W0"], self.M0.gateL],
                 ["2nd Stage Gain", av2, "Output Pole",     poles[1], "M1", sizes["W1"], self.M1.gateL],
                 ["Total Gain",     av,  "Mirror Pole",     poles[2], "M2", sizes["W2"], self.M2.gateL],
                 [None, None, None, None,                             "M3", sizes["W3"], self.M3.gateL],
                 [None, None, None, None,                             "M4", sizes["W4"], self.M4.gateL]]
        
        if latex:
            format = "latex"
        else:
            format = "fancy_outline"
        print(tabulate(table, headers=["Gain", "dB", "Pole", "Hz", "Device", "Width", "Length"], tablefmt=format, floatfmt=".2e"))
        print("Power Consumption: {:.2e} W".format(power))
    
    def bode(self) -> None:
        poles = self.poles()
        p1 = poles[0]
        p2 = poles[1]
        p3 = poles[2]
        den3 = [1, p1+p2+p3, p1*p2+p3*p1+p2*p3, p1*p2*p3]
        K = den3[-1] * self.av()
        
        w = np.logspace(0, 8, 1000)
        sys = sp.signal.TransferFunction([K], den3)
        w, mag, phase = sp.signal.bode(sys, w)

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)

        ax.set_xlim(1, 1e8)
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