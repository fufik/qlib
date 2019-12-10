from qlib.qregister import qregister
from qlib.qbit      import *
import numpy as np
from qlib.error import QoperatorError
import qlib.matrix as ma
class qoperator:
    def __init__(self,matrix:np.ndarray):
        if type(matrix) is not np.ndarray:
            raise QoperatorError("argument must be of type numpy.ndarray")
        self.matrix = matrix
    
    def __add__(self,other):
        if type(other) is qoperator:
            return qoperator(self.matrix + other.matrix)
        elif type(other) is np.ndarray:
            return qoperator(self.matrix + other)

    def __matmul__(self,other):
        if type(other) is qoperator:
            return qoperator(np.matmul(self.matrix,other.matrix))
        elif type(other) is qregister:
            return qregister(np.matmul(self.matrix,other.vector))
        elif type(other) is qbit:
           return qbit(np.matmul(self.matrix,other.vector))
        elif type(other) is np.ndarray:
            return qoperator(self @ other)

    def __mul__(self,other):
        if type(other) is qoperator:
            return qoperator(np.kron(self.matrix,other.matrix))
        elif type(other) is qregister:
            return qregister(np.kron(self.matrix,other.vector))
        elif type(other) is qbit:
            return qbit(np.kron(self.matrix,other.vector))
        elif type(other) is np.ndarray:
            return qoperator(np.kron(self.matrix, other))
    
    def __pow__(self,other):
        if type(other) is not int:
            raise TypeError(f"unsupported operand type for **: '{type(other)}'")
        if n ==0:
            return qoperator(np.array([[1]],dtype=complex)) #does NOTHING on matmul! :)

        n = self
        for i in range(1,other):
            n = n * self #kronecker product
        return n

    def __repr__(self):
        return "qoperator: {}".format(self.matrix)

    def __str__(self):
        return "qoperator: {}".format(self.matrix)



op_I = qoperator(ma.EYE)
op_H = qoperator(ma.H)
op_X = qoperator(ma.X)
op_Y = qoperator(ma.Y)
op_Z = qoperator(ma.Z)
op_CNOT = qoperator(np.array([[1,0,0,0],
                              [0,1,0,0],
                              [0,0,0,1],
                              [0,0,1,0]],dtype=complex))
op_CCNOT = qoperator(np.array([[1,0,0,0,0,0,0,0],
                               [0,1,0,0,0,0,0,0],
                               [0,0,1,0,0,0,0,0],
                               [0,0,0,1,0,0,0,0],
                               [0,0,0,0,1,0,0,0],
                               [0,0,0,0,0,1,0,0],
                               [0,0,0,0,0,0,0,1],
                               [0,0,0,0,0,0,1,0]],dtype=complex))

op_SWAP2 = qoperator(np.array([[1,0,0,0],
                               [0,0,1,0],
                               [0,1,0,0],
                               [0,0,0,1]],dtype=complex))
op_SWAP3 = qoperator(np.array([[1,0,0,0,0,0,0,0],
                               [0,0,0,0,1,0,0,0],
                               [0,0,1,0,0,0,0,0],
                               [0,0,0,0,0,0,1,0],
                               [0,1,0,0,0,0,0,0],
                               [0,0,0,0,0,1,0,0],
                               [0,0,0,1,0,0,0,0],
                               [0,0,0,0,0,0,0,1]],dtype=complex))
