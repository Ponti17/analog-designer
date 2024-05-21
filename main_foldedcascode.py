import numpy as np
from folded_cascode import FoldedCascode

if __name__ == "__main__":
    fd = FoldedCascode()
    fd.itail = 570e-9
    fd.CL = 1e-12
    fd.M0.model = "nch_25"
    fd.M1.model = "pch_25"
    fd.M2.model = "nch"
    fd.M3.model = "nch"
    fd.M4.model = "pch"
    fd.M5.model = "pch"
    
    fd.M0.gateL = 1e-6
    fd.M1.gateL = 1e-6
    fd.M2.gateL = 2e-6
    fd.M3.gateL = 1e-6
    fd.M4.gateL = 1e-6
    fd.M5.gateL = 1e-6
    
    fd.M0.vdsrc = 0.3
    fd.M1.vdsrc = 0.3
    fd.M2.vdsrc = 0.3
    fd.M3.vdsrc = 0.3
    fd.M4.vdsrc = 0.3
    fd.M5.vdsrc = 0.3
    
    fd.M0.gmoverid = 27
    fd.M1.gmoverid = 27
    fd.M2.gmoverid = 21
    fd.M3.gmoverid = 21
    fd.M4.gmoverid = 20
    fd.M5.gmoverid = 17
    
    fd.init()
    fd.characterize(latex = False)