import numpy as np
from ota import OTA

if __name__ == "__main__":
    # M0 Input PMOS
    # M1 NMOS Mirror
    # M2 NMOS Cascode
    # M3 PMOS Mirror
    # M4 PMOS Cascode
    ota = OTA()
    ota.itail = 4.4e-6
    ota.CL = 600e-15
    ota.cl_gain = 20*np.log10(22)
    
    ota.M0.model = "pch_25"
    ota.M1.model = "nch_25"
    ota.M2.model = "nch_25"
    ota.M3.model = "pch_25"
    ota.M4.model = "pch_25"
    
    ota.M0.gateL = 1e-6
    ota.M1.gateL = 10e-6
    ota.M2.gateL = 2e-6
    ota.M3.gateL = 6e-6
    ota.M4.gateL = 2e-6

    ota.M0.vdsrc = 0.3
    ota.M1.vdsrc = 0.3
    ota.M2.vdsrc = 0.3
    ota.M3.vdsrc = 0.3
    ota.M4.vdsrc = 0.3
    
    ota.M0.gmoverid = 27
    ota.M1.gmoverid = 18
    ota.M2.gmoverid = 15
    ota.M3.gmoverid = 18
    ota.M4.gmoverid = 15
    
    ota.init()
    ota.characterize(latex = False)
    
    #ota.bode()