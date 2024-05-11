from transistor import MosDevice

if __name__ == "__main__":
    M1 = MosDevice()
    M1.set_model("nch")
    M1.set_id(1e-6)
    M1.set_gateL(10e-6)
    M1.set_vdsrc(0.6)
    M1.set_gmoverid(20.0)
    
    print(M1.gmro())
    print(M1.ft())