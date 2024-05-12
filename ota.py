from transistor import MosDevice

class OTA:
    def __init__(self):
        self.M1 = MosDevice()
        self.M3 = MosDevice()
        self.M7 = MosDevice()
        
        self.id: float = 0.0
        
    def init(self) -> None:
        if self.M1.valid() and self.M3.valid() and self.M7.valid():
            self.__calculate()
            
    def __calculate(self) -> None:
        pass