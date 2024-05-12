from transistor import MosDevice

class OTA:
    def __init__(self) -> None:
        self.M1 = MosDevice()
        self.M3 = MosDevice()
        self.M7 = MosDevice()
        
        self.itail: float   = 0.0
        self.av_val: float      = 0.0
        self.rout_val: float    = 0.0
        
        # Output Pole
        self.fp1: float     = 0.0
        # NMOS Mirror Pole
        self.fp2: float     = 0.0
        # NMOS Mirror Pole
        self.fp3: float     = 0.0
        # PMOS Mirror Pole
        self.fp4: float     = 0.0
        
    def init(self) -> None:
        self.M1.set_id(self.itail/2)
        self.M3.set_id(self.itail/2)
        self.M7.set_id(self.itail/2)
        if self.M1.valid() and self.M3.valid() and self.M7.valid():
            self.__calculate()
            
    def __parallel(self, R1: float, R2: float) -> float:
        return R1 * R2 / (R1 + R2)
            
    def __calculate(self) -> None:
        self.rout_val = self.__parallel(self.M3.ro(), self.M7.ro())
        self.av_val = self.rout_val * self.M1.gm()
        
    def av(self) -> float:
        return self.av_val
    
    def rout(self) -> float:
        return self.rout_val