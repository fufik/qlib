from math      import log, sqrt
from qlib import *
import numpy as np
from qlib.error import QregisterError
class qregister:
    def __init__(self,*qbits):
        if type(qbits[0]) is np.ndarray: #from a vector
            self.vector = qbits[0]
            self._length = int(log(len(qbits[0]),2))
        elif type(qbits[0]) is qbit:
            self.qbits = list(qbits)
            self._length = len(self.qbits)
            self.vector = cart_prod_qbits(qbits)
        else:
             raise QregisterError("Wrong parameter types")
    
    def __getitem__(self,key):
        return self.qbits[key]
    
    def __setitem__(self,key,value):
        if key >= self._length:
            raise QregisterError("Out of bounds")
        if type(value) is qbit:
            self.qbits[key] = value
            self.vector = cart_prod_qbits(self.qbits)
        else:
            raise QregisterError("The value is not qbit")
    
    def __mul__(self,other):
        return np.inner(self.vector.transpose(), other.vector.transpose()).item(0)
    
    def __pow__(self,other):
        return np.kron(self.vector,other.vector)
    
    def __len__(self):
        return self._length
    
    
    
def measure(qrin:qregister):
    if len(qrin) != 2:
        raise QregisterError("The qregister is not 2 qbits in size")
    d = sqrt(abs(qrin * qrin))
    #print("D: ",d)
    states = list()
    states.append(qregister(qbit_0,qbit_0))
    states.append(qregister(qbit_0,qbit_1))
    states.append(qregister(qbit_1,qbit_0))
    states.append(qregister(qbit_1,qbit_1))
    probs = list()
    for n,i in enumerate(states):
        a = (i*qrin)
        b = (abs(a)/d)**2
        #print("Product: ", a, b)
        probs.append(b)
    res = np.random.choice(len(states),1,p=probs).item(0)
    #print("Result n {}:\n".format(res,states[res]))
    return states[res]
    
def bases(qrin:qregister):
    if len(qrin) != 2:
        raise QregisterError("The qregister is not 2 qbits in size")
    d = sqrt(abs(qrin * qrin))
    #print("D: ",d)
    states = list()
    states.append(qregister(qbit_0,qbit_0))
    states.append(qregister(qbit_0,qbit_1))
    states.append(qregister(qbit_1,qbit_0))
    states.append(qregister(qbit_1,qbit_1))
    probs = list()
    for n,i in enumerate(states):
        a = (i*qrin)
        b = (abs(a)/d)**2
        #print("Pr:",b)
        probs.append(round(b,5))
    r = list(filter(lambda x: x[0] != 0.0,zip(probs,states)))
    #print("R:",r)
    return r
        
