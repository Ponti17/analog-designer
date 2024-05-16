import numpy as np
from ota import OTA

if __name__ == "__main__":
    ota = OTA()
    ota.itail = 2.24e-6 * 2
    ota.CL = 400e-15
    
    ota.M0.model = "pch_25"
    ota.M1.model = "nch"
    ota.M2.model = "nch"
    ota.M3.model = "pch"
    ota.M4.model = "pch_hvt"
    
    ota.M0.gateL = 1e-6
    ota.M1.gateL = 2e-6
    ota.M2.gateL = 17e-6
    ota.M3.gateL = 2e-6
    ota.M4.gateL = 2e-6

    ota.M0.vdsrc = 0.3
    ota.M1.vdsrc = 0.3
    ota.M2.vdsrc = 0.3
    ota.M3.vdsrc = 0.3
    ota.M4.vdsrc = 0.3
    
    ota.M0.gmoverid = 27
    ota.M1.gmoverid = 22
    ota.M2.gmoverid = 16
    ota.M3.gmoverid = 20
    ota.M4.gmoverid = 18
    
    ota.init()
    
    av = ota.av()
    av_db = 20 * np.log10(av)
    print(av_db)
    
    poles = ota.poles()
    print(poles)
    
    sizes = ota.size()
    print(sizes)