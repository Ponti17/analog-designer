import numpy as np
from twostage import TwoStage

if __name__ == "__main__":
    # M0 = PMOS input
    # M1 = NMOS Mirror
    # M2 = NMOS Mirror Cascode
    # M3 = NMOS 2nd stage
    # M4 = PMOS 2nd stage load
    ts = TwoStage()
    ts.itail    = 7.7e-6
    ts.iout     = 21e-6
    ts.CL       = 500e-15
    ts.Cc       = 150e-15
    ts.cl_gain  = 20*np.log10(20)
    
    ts.M0.model = "pch_25"
    ts.M1.model = "nch"
    ts.M2.model = "nch"
    ts.M3.model = "nch_25"
    ts.M4.model = "pch_25"
    
    ts.M0.gateL = 1e-6
    ts.M1.gateL = 10e-6
    ts.M2.gateL = 2e-6
    ts.M3.gateL = 5e-6
    ts.M4.gateL = 5e-6

    ts.M0.vdsrc = 0.5
    ts.M1.vdsrc = 0.3
    ts.M2.vdsrc = 0.3
    ts.M3.vdsrc = 0.6
    ts.M4.vdsrc = 0.6
    
    ts.M0.gmoverid = 27
    ts.M1.gmoverid = 15
    ts.M2.gmoverid = 15
    ts.M3.gmoverid = 15
    ts.M4.gmoverid = 15
    
    ts.init()
    
    av = ts.av()
    av_db = 20 * np.log10(av)
    print(av_db)
    
    poles = ts.poles()
    print(poles)
    
    sizes = ts.size()
    print(sizes)
    
    ts.bode()