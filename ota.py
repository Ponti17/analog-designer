import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from tabulate import tabulate
from utils import Utils
from transistor import MosDevice

# Three-mirror OTA
# "A Low-Power, Low-Noise CMOS Amplifier for Neural Recording Applications"
# Reid R. Harrison

class OTA:
    def __init__(self) -> None:
        self.utils = Utils()
        
        # Closed loop gain
        self.cl_gain: float = 0.0
        
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
        
        self.fp1 = (1 / (2 * np.pi * self.rout_val * self.CL))
        self.fp2 = (self.M1.gm() / (8 * np.pi * self.M1.cgs()))
        self.fp3 = (self.M1.gm() / (8 * np.pi * self.M1.cgs()))
        self.fp4 = (self.M3.gm() / (8 * np.pi * self.M3.cgs()))
        
        self.av_val = self.rout_val * self.M0.gm()
        
    def characterize(self, latex: bool) -> None:
        av  = np.round(20*np.log10(self.av()), 2)
        poles = self.poles()
        sizes = self.size()
        power = (self.itail*2) * 1.2 # Assuming 1.2 VDD
        
        poles_formatted = []
        for pole in poles:
            poles_formatted.append(str("{:.2e}".format(pole)))
            
        table = [["Total Gain",     av,  "Dominant Pole",       poles[0], "M0", sizes["W0"], self.M0.gateL],
                 [None,             None,"Mirror Pole NMOS 1",  poles[1], "M1", sizes["W1"], self.M1.gateL],
                 [None,             None,"Mirror Pole NMOS 2",  poles[2], "M2", sizes["W2"], self.M2.gateL],
                 [None,             None,"Mirror Pole PMOS 1",  poles[3], "M3", sizes["W3"], self.M3.gateL],
                 [None, None, None, None,                                 "M4", sizes["W4"], self.M4.gateL]]
        
        if latex:
            format = "latex"
        else:
            format = "fancy_outline"
        print(tabulate(table, headers=["Gain", "dB", "Pole", "Hz", "Device", "Width", "Length"], tablefmt=format, floatfmt=".2e"))
        print("Power Consumption: {:.2e} W".format(power))
        
    def av(self) -> float:
        return self.rout_val * self.GM_val
    
    def rout(self) -> float:
        return self.rout_val
    
    def poles(self) -> list[float]:
        return [self.fp1, self.fp2, self.fp3, self.fp4]
    
    def GM(self) -> float:
        return self.GM_val
    
    def size(self) -> dict[str, str]:
        W0 = str("{:.2e}".format(np.abs(float(self.M0.w_val))))
        W1 = str("{:.2e}".format(np.abs(float(self.M1.w_val))))
        W2 = str("{:.2e}".format(np.abs(float(self.M2.w_val))))
        W3 = str("{:.2e}".format(np.abs(float(self.M3.w_val))))
        W4 = str("{:.2e}".format(np.abs(float(self.M4.w_val))))
        return {"W0": W0, "W1": W1, "W2": W2, "W3": W3, "W4": W4}
    
    def bode(self) -> None:
        poles = self.poles()
        p1 = poles[0]
        p2 = poles[1]
        p3 = poles[2]
        p4 = poles[3]
        den4 = [1, p1+p2+p3+p4, p1*p2+p1*p3+p1*p4+p2*p3+p2*p4+p3*p4, p1*p2*p3+p1*p2*p4+p1*p3*p4+p2*p3*p4, p1*p2*p3*p4]
        K = den4[-1] * self.av()
        
        sys = sp.signal.TransferFunction([K], den4)
        w, mag, phase = sp.signal.bode(sys)

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