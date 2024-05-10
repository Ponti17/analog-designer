import numpy as np

# A class for containing gm/id relevant parameters.
# ---
# Before the model can be used, gm/id, gmro, id and ft MUST be set.
# After setting needed parameters the caps can be initialized by calling init_caps.
# ---
# All relevant MOS parameters can be accessed by calling the corresponding function.

class MosDevice:
    def __init__(self) -> None:
        self.gmid_val: float    = 0.0
        self.gmro_val: float    = 0.0
        self.id_val: float      = 0.0
        self.ft_val: float      = 0.0
        self.model: str         = ""
        self.caps = {
            "cgg": 0.0,
            "cgd": 0.0,
            "cdd": 0.0,
            "cdb": 0.0,
            "cgs": 0.0
        }
    def init_caps(self) -> None:
        cgg = self.gm() / (2*np.pi*self.ft())
        for cap in self.caps:
            match cap:
                case "cgg":
                    self.caps[cap] = cgg
                case "cgd":
                    self.caps[cap] = 0.24*cgg
                case "cdd":
                    self.caps[cap] = 0.6*cgg
                case "cdb":
                    self.caps[cap] = self.caps["cdd"] - self.caps["cgd"]
                case "cgs":
                    # actually cgs + cgb
                    # neglect cgb
                    self.caps[cap] = self.caps["cgg"] - self.caps["cgd"]
    def cgg(self) -> float:
        return self.caps["cgg"]
    def cgd(self) -> float:
        return self.caps["cgd"]
    def cdd(self) -> float:
        return self.caps["cdd"]
    def cdb(self) -> float:
        return self.caps["cdb"]
    def cgs(self) -> float:
        return self.caps["cgs"]
    def gmid(self) -> float:
        return self.gmid_val
    def gmro(self) -> float:
        return self.gmro_val
    def id(self) -> float:
        return self.id_val
    def ft(self) -> float:
        return self.ft_val
    def gm(self) -> float:
        return self.gmid_val * self.id_val
    def ro(self) -> float:
        return self.gmro_val / self.gm()