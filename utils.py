import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

class Utils:
    def __init__(self) -> None:
        pass
    
    def parallel(self, res: list[float]) -> float:
        parallel_r: float = 0
        for r in res:
            if r == 0:
                return 0
            parallel_r += 1/r
        return 1/parallel_r
    
    def cascode(self, rO1: float, rO2: float, gm2: float) -> float:
        return (1 + gm2 * rO2) * rO1 + rO2
    
    def bode(self, H: sp.signal.TransferFunction) -> None:
        w, mag, phase = sp.signal.bode(H)
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.semilogx(w, mag)
        plt.subplot(2, 1, 2)
        plt.semilogx(w, phase)
        plt.show()