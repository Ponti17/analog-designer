import pandas as pd
import numpy as np
import numpy.typing as npt
import os

class DataHandler:
    def __init__(self) -> None:
        self.df: pd.DataFrame = pd.DataFrame()
        self.model: str = ""
        
    def load(self, model: str) -> None:
        modeldir  =     "models"
        modellist =    {"nch":        "nch_full_sim",
                        "nch_25":     "nch_25_full_sim",
                        "nch_hvt":    "nch_hvt_full_sim",
                        "nch_lvt":    "nch_lvt_full_sim",
                        "pch":        "pch_full_sim",
                        "pch_25":     "pch_25_full_sim",
                        "pch_hvt":    "pch_hvt_full_sim",
                        "pch_lvt":    "pch_lvt_full_sim"}

        try:
            file = os.path.join(modeldir, modellist[model] + ".pkl")
            self.df = pd.read_pickle(file)
            self.model = model
        except:
            print("Invalid model or model not found: {}".format(model))
            exit()
            
    def get_loaded(self) -> str:
        return self.model

    def get_axis(self, ax: str, vdsrc: str, gateL: str) -> npt.NDArray[np.float32]:
        match ax:
            case "gmro":
                return self.__get_gmro(vdsrc, gateL)
            case "id/w":
                return self.__get_idw(vdsrc, gateL)
            case "ft":
                return self.__get_ft(vdsrc, gateL)
            case _:
                return self.__get_simple(ax, vdsrc, gateL)
    
    def __get_simple(self, ax: str, vdsrc: str, gateL: str) -> npt.NDArray[np.float32]:
        # This regex string is a steaming pile of shit, but it essentially ANDs 4 conditions
        regex_str: str = "(?=.*M0:{})(?=.*vds={})(?=.*length={})(?=.*Y)".format(ax, vdsrc, gateL).replace("+", "\\+")
        return self.df.filter(regex=regex_str).to_numpy()
    
    def __get_gmro(self, vdsrc: str, gateL: str) -> npt.NDArray[np.float32]:
        gm:  npt.NDArray[np.float32] = self.__get_simple("gm ", vdsrc, gateL)
        gds: npt.NDArray[np.float32] = self.__get_simple("gds", vdsrc, gateL)
        return gm / gds
    
    def __get_idw(self, vdsrc: str, gateL: str) -> npt.NDArray[np.float32]:
        id: npt.NDArray[np.float32] = self.__get_simple("id ", vdsrc, gateL)
        return id / 1e-6
    
    def __get_ft(self, vdsrc: str, gateL: str) -> npt.NDArray[np.float32]:
        gm:  npt.NDArray[np.float32] = self.__get_simple("gm ", vdsrc, gateL)
        cgg: npt.NDArray[np.float32] = self.__get_simple("cgg ", vdsrc, gateL)
        return gm / (2 * np.pi * cgg)