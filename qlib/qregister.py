from math      import log, sqrt
from qlib import *
import numpy as np
from qlib.error import QregisterError
from collections import deque as deq
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
    
    def __repr__(self):
        return "qregister: {}".format(self.vector.transpose())
    
    def __str__(self):
        return "qregister: {}".format(self.vector.transpose())
    
    
def legmeasure(qrin:qregister):
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
    
def legbases(qrin:qregister):
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
    
def _binfill(size:int):
    def b2q(n):
        return qbit_0 if n == 0b0 else qbit_1
    
    states = list()
    up_lim = 2 ** size
    for x in range(0,up_lim):
        print(f"{x} is {x:b} in binary")
        arg = deq()
        n = x
        for f in range(size):           #parsing each number into an array of bits
            arg.appendleft(b2q(n%2))    #thus converting every bit into a basic qbit
            n = n>>1                    
        print(arg)
        q = qregister(*arg)
        states.append(q)
    return states
    
    
def bases(qrin: qregister):
    d = sqrt(abs(qrin * qrin))
    states = _binfill(len(qrin))
    probs = list()
    for n,i in enumerate(states):
        a = (i*qrin)
        b = (abs(a)/d)**2
        #print("Pr:",b)
        probs.append(round(b,5))
    r = list(filter(lambda x: x[0] != 0.0,zip(probs,states)))
    return r
    
def measure(qrin: qregister):
    q = bases(qrin)
    q = list(zip(*q))
    probs = q[0]
    states = q[1]
    res = np.random.choice(len(states),1,p=probs).item(0)
    return states[res]
