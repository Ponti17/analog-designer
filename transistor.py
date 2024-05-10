import numpy.typing as npt
import numpy as np

class MosDevice():
    def __init__(self) -> None:
        self.model: str             = ""
        self.gmoverid: np.float32   = 0.0
        self.gmro: np.float32       = 0.0
        self.id: np.float32         = 0.0
        self.ft: np.float32         = 0.0
        self.params: npt.NDArray[np.float32] = np.array([
            self.gmoverid, self.gmro, self.id, self.ft])
        
    def set(self, params: npt.NDArray[np.float32]) -> None:
        self.params = params