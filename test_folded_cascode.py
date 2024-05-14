import numpy as np
from folded_cascode import FoldedCascode

if __name__ == "__main__":
    fd = FoldedCascode()
    fd.itail = 5.5e-6
    fd.M0.model = "nch_25"
    fd.M1.model = "pch_25"
    fd.M2.model = "nch"
    fd.M3.model = "nch"
    fd.M4.model = "pch_25"
    fd.M5.model = "pch"
    
    fd.M0.gateL = 1e-6
    fd.M1.gateL = 1e-6
    fd.M2.gateL = 2e-6
    fd.M3.gateL = 1e-6
    fd.M4.gateL = 5e-6
    fd.M5.gateL = 10e-6
    
    fd.M0.vdsrc = 0.3
    fd.M1.vdsrc = 0.3
    fd.M2.vdsrc = 0.3
    fd.M3.vdsrc = 0.3
    fd.M4.vdsrc = 0.3
    fd.M5.vdsrc = 0.3
    
    fd.M0.gmoverid = 26
    fd.M1.gmoverid = 26
    fd.M2.gmoverid = 20
    fd.M3.gmoverid = 20
    fd.M4.gmoverid = 15
    fd.M5.gmoverid = 12
    
    fd.init()
    av = fd.av()
    av_db = 20 * np.log10(av)
    print(av_db)