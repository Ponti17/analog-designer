import numpy as np
from ota import OTA

if __name__ == "__main__":
    ota = OTA()
    ota.itail = 1e-6
    ota.M1.model = "nch"
    ota.M3.model = "nch_25"
    ota.M7.model = "nch_25"
    ota.M1.gateL = 20e-6
    ota.M3.gateL = 20e-6
    ota.M7.gateL = 20e-6
    ota.M1.vdsrc = 0.6
    ota.M3.vdsrc = 0.6
    ota.M7.vdsrc = 0.6
    ota.M1.gmoverid = 20
    ota.M3.gmoverid = 20
    ota.M7.gmoverid = 20
    
    ota.init()
    av = ota.av()
    av_db = 20 * np.log10(av)
    print(av_db)