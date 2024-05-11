import numpy.typing as npt
import numpy as np

class MosDevice():
    def __init__(self) -> None:
        self.model: str             = ""
        self.gmoverid: float        = 0.0
        self.gmro: float            = 0.0
        self.id: float              = 0.0
        self.ft: float              = 0.0