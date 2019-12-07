import numpy as np
import cmath
from qlib.error import QbitError
import qlib.matrix as mat
class qbit:
    def __init__(self,*prms):
        if len(prms) == 2:
            lower,upper = prms[0],prms[1]
            if round((abs(lower)**2 + abs(upper)**2),5) == 1:
                self.vector = np.array([[upper],[lower]],dtype=complex)
            else:
                raise QbitError("The sum of magnitudes' squares is not 1")
        elif len(prms) is 1:
            if round(np.sum(np.square(np.absolute(prms[0]))),5) == 1:
                self.vector = prms[0]
            else:
                print(prms[0], "\nSum: ",np.sum(prms[0]))
                raise QbitError("Not 1 ")
            self.vector = prms[0]
        else:
            raise QbitError("Wrong amount of arguments")
    
    def op_X(self):
        #opnot = np.array([[0,1],[1,0]],dtype=complex)
        return qbit(np.matmul(mat.X,self.vector))
    
    def op_not(self):
        return self.op_X()
    
    def op_Y(self):
        #opy = np.array([[0,1j],[1j,0]],dtype=complex)
        return qbit(np.mathmul(mat.Y,self.vector))
    
    def op_Z(self):
        #opy = np.array([[1,0],[0,-1]],dtype=complex)
        return qbit(np.mathmul(mat.Z,self.vector))
    
    def op_H(self):
        #oph = np.array([[1,1],[1,-1]],dtype=complex)
        #oph = (1/cmath.sqrt(2)) * oph
        return qbit(np.matmul(mat.H,self.vector))
        
    
    def __eq__(self, other):
        return (self.vector == other.vector).all()
    
    def __mul__(self,other):
        return np.inner(self.vector.transpose(), other.vector.transpose()).item(0)
    
    def __pow__(self,other):
        return np.kron(self.vector,other.vector)
    
    def __repr__(self):
        return "qbit[{},{}]".format(self.vector[0][0],self.vector[1][0])
    
    def __str__(self):
        return "qbit[{},{}]".format(self.vector[0][0],self.vector[1][0])
    
#def cart_prod(x: np.array,y: np.array):
#    i = np.array([np.tile(x.transpose()[0], len(y.transpose()[0])), np.repeat(y.transpose()[0], len(x.transpose()[0]))]).transpose()
#    return np.array([[a[0]*a[1] for a in i]]).transpose()

#def cart_prod(x: np.array,y: np.array):
#    i = np.array([np.tile(y.transpose()[0], len(x.transpose()[0])), np.repeat(x.transpose()[0], #len(y.transpose()[0]))]).transpose()
#    return np.array([[a[0]*a[1] for a in i]]).transpose()


def cart_prod_qbits(*ar):
    ar = list(*ar)
    print(ar)
    base = ar[0].vector
    a = ar[1:]
    for l in a:
        base = np.kron(base,l.vector)
    return base
qbit_0 = qbit(0,1)
qbit_1 = qbit(1,0)
qbit_sp = qbit_0.op_H()
qbit_sn = qbit_1.op_H()
