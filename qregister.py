from math      import log
import qbit
import numpy as np
class qregister:
    def __init__(self,*qbits):
        if type(qbits[0]) is not qbit.qbit: #from a vector
            self.vector = qbits[0]
            self._length = int(log(len(qbits[0]),2))
        else:
            self.qbits = list(qbits)
            self._length = len(self.qbits)
            self.vector = qbit.cart_prod_qbits(qbits)
    
    def __getitem__(self,key):
        return self.qbits[key]
    
    def __setitem__(self,key,value):
        if key >= self._length:
            raise QregisterError("Out of bounds")
        if type(value) is qbit.qbit:
            self.qbits[key] = value
            self.vector = qbit.cart_prod_qbits(self.qbits)
        else:
            raise QregisterError("The value is not qbit")
    
    def __len__(self):
        return self._length

