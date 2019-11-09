import numpy as np
import cmath
from error import QbitError
from functools import singledispatch
class qbit:
    def __init__(self,lower,upper):
        if (abs(lower)**2 + abs(upper)**2) == 1:
            self.vector = np.array([[upper],[lower]],dtype=complex)
        else:
            raise QbitError("The sum of magnitudes' squares is not 1")
    
    def op_X(self):
        opnot = np.array([[0,1],[1,0]],dtype=complex)
        return np.matmul(opnot,self.vector)
    
    def op_not(self):
        return op_X(self)
    
    def op_Y(self):
        opy = np.array([[0,j],[j,0]],dtype=complex)
        return np.mathmul(opnot,self.vector)
    
    def op_Z(self):
        opy = np.array([[1,0],[0,-1]],dtype=complex)
        return np.mathmul(opnot,self.vector)
    
#def cart_prod(x: np.array,y: np.array):
#    i = np.array([np.tile(x.transpose()[0], len(y.transpose()[0])), np.repeat(y.transpose()[0], len(x.transpose()[0]))]).transpose()
#    return np.array([[a[0]*a[1] for a in i]]).transpose()

def cart_prod(x: np.array,y: np.array):
    i = np.array([np.tile(y.transpose()[0], len(x.transpose()[0])), np.repeat(x.transpose()[0], len(y.transpose()[0]))]).transpose()
    return np.array([[a[0]*a[1] for a in i]]).transpose()


def cart_prod_qbits(*ar):
    ar = list(*ar)
    print(ar)
    base = ar[0].vector
    a = ar[1:]
    for l in a:
        base = cart_prod(base,l.vector)
    return base
qbit_0 = qbit(0,1)
qbit_1 = qbit(1,0)
