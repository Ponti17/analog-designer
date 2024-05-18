import numpy.typing as npt
import numpy as np
from _datahandler import DataHandler

class MosDevice():
    def __init__(self) -> None:
        self.__reader = DataHandler()
        self.model: str             = ""
        self.gmoverid: float        = 0.0
        self.id: float              = 0.0
        self.gateL: float           = 0.0
        self.vdsrc: float           = 0.0
        
        self.gmro_val: float        = 0.0
        self.ft_val: float          = 0.0
        self.gmoverid_val: float    = 0.0
        self.idw_val: float         = 0.0
        self.w_val: float           = 0.0
        self.__gmoverid_arr: npt.NDArray[np.float64]
        self.__gmro_arr: npt.NDArray[np.float64]
        self.__ft_arr: npt.NDArray[np.float64]
        self.__idw_arr: npt.NDArray[np.float64]
        
    def set_gmoverid(self, gmid: float) -> None:
        self.gmoverid = gmid
        if self.valid():
            self.__calculate()
        
    def set_id(self, id: float) -> None:
        self.id = id
        if self.valid():
            self.__calculate()
        
    def set_model(self, model: str) -> None:
        self.model = model
        if self.valid():
            self.__calculate()
            
    def set_gateL(self, gateL: float) -> None:
        self.gateL = gateL
        if self.valid():
            self.__calculate()
            
    def set_vdsrc(self, vdsrc: float) -> None:
        self.vdsrc = vdsrc
        if self.valid():
            self.__calculate()
        
    def valid(self) -> bool:
        if self.model != "" and self.gmoverid != 0.0 and self.id != 0.0 and self.gateL != 0.0 and self.vdsrc != 0.0:
            return True
        return False
    
    def __calculate(self) -> None:
        self.__reader.load(self.model)
        self.__gmoverid_arr = self.__reader.get_axis("gmoverid", str(self.vdsrc), str(self.gateL))
        self.__gmro_arr = self.__reader.get_axis("gmro", str(self.vdsrc), str(self.gateL))
        self.__ft_arr = self.__reader.get_axis("ft", str(self.vdsrc), str(self.gateL))
        self.__idw_arr = self.__reader.get_axis("id/w", str(self.vdsrc), str(self.gateL))

        for i in range(len(self.__gmoverid_arr)):
            if self.__gmoverid_arr[i] < self.gmoverid:
                self.gmoverid_val = self.__gmoverid_arr[i]
                self.gmro_val = self.__gmro_arr[i]
                self.ft_val = self.__ft_arr[i]
                self.idw_val = self.__idw_arr[i]
                self.w_val = self.id / self.idw_val
                break
    
    def gmro(self) -> float:
        return self.gmro_val
    
    def ft(self) -> float:
        return self.ft_val
    
    def gm(self) -> float:
        return self.gmoverid_val * self.id
    
    def ro(self) -> float:
        return self.gmro() / self.gm()
    
    def cgg(self) -> float:
        return self.gm() / self.ft() * (1 / (2 * np.pi))
    
    def cgs(self) -> float:
        return self.cgg() * (1/2.5)
    
    def width(self) -> float:
        return self.w_val