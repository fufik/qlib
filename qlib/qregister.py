from math      import log
import qbit
import numpy as np
from error import QregisterError
class qregister:
    def __init__(self,*qbits):
        if type(qbits[0]) is np.ndarray: #from a vector
            self.vector = qbits[0]
            self._length = int(log(len(qbits[0]),2))
        elif type(qbits[0]) is qbit.qbit:
            self.qbits = list(qbits)
            self._length = len(self.qbits)
            self.vector = qbit.cart_prod_qbits(qbits)
        else:
             raise QregisterError("Wrong parameter types")
    
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
    
    def __mul__(self,other):
        return self.vector * other.vector
    
    def __pow__(self,other):
        return np.kron(self.vector,other.vector)
    
    def __len__(self):
        return self._length
    

