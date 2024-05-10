import numpy as np
from transistor import MosDevice

# Two-stage amplifier structure w/ PMOS inputs

class TwoStage():
    def __init__(self) -> None:
        self.M2 = MosDevice()
        self.M4 = MosDevice()
        self.M6 = MosDevice()
        self.M7 = MosDevice()
        
        self.itail: float  = 0.0
        self.vdd: float    = 0.0
        self.CL: float     = 0.0

        