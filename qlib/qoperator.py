from qlib.qregister import qregister
from qlib.qbit      import *
from qlib.matrix    import *
import sympy as sp
from sympy.matrices.dense import MutableDenseMatrix as MatrixType
from qlib.error import QoperatorError
import qlib.matrix as ma
from collections import deque as deq
class qoperator:
    def __init__(self,matrix: MatrixType):
        if type(matrix) is not MatrixType:
            raise QoperatorError("argument must be of type sympy.<..>.MutableDenseMatrix")
        self.matrix = matrix
    
    def __add__(self,other):
        if type(other) is qoperator:
            return qoperator(self.matrix + other.matrix)
        elif type(other) is MatrixType:
            return qoperator(self.matrix + other)

    def __matmul__(self,other):
        if type(other) is qoperator:
            return qoperator(self.matrix @ other.matrix)
        elif type(other) is qregister:
            return qregister(self.matrix @ other.vector)
        elif type(other) is qbit:
           return qbit(self.matrix @ other.vector)
        elif type(other) is MatrixType:
            return qoperator(self @ other)

    def __mul__(self,other):
        if type(other) is qoperator:
            return qoperator(sp.Matrix(sp.kronecker_product(self.matrix,other.matrix)))
        elif type(other) is qregister:
            return qregister(sp.Matrix(sp.kronecker_product(self.matrix,other.vector)))
        elif type(other) is qbit:
            return qbit(sp.Matrix(sp.kronecker_product(self.matrix,other.vector)))
        elif type(other) is MatrixType:
            return qoperator(sp.Matrix(sp.kronecker_product(self.matrix, other)))
    
    def __pow__(self,other):
        if type(other) is not int:
            raise TypeError(f"unsupported operand type for **: '{type(other)}'")
        if other == 0:
            return qoperator(sp.Matrix([1])) #does NOTHING on matmul! :)

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
op_CNOT = qoperator(sp.Matrix([[1,0,0,0],
                              [0,1,0,0],
                              [0,0,0,1],
                              [0,0,1,0]]))
op_CCNOT = qoperator(sp.Matrix([[1,0,0,0,0,0,0,0],
                               [0,1,0,0,0,0,0,0],
                               [0,0,1,0,0,0,0,0],
                               [0,0,0,1,0,0,0,0],
                               [0,0,0,0,1,0,0,0],
                               [0,0,0,0,0,1,0,0],
                               [0,0,0,0,0,0,0,1],
                               [0,0,0,0,0,0,1,0]]))

op_SWAP2 = qoperator(sp.Matrix([[1,0,0,0],
                               [0,0,1,0],
                               [0,1,0,0],
                               [0,0,0,1]],))
op_SWAP3 = qoperator(sp.Matrix([[1,0,0,0,0,0,0,0],
                               [0,0,0,0,1,0,0,0],
                               [0,0,1,0,0,0,0,0],
                               [0,0,0,0,0,0,1,0],
                               [0,1,0,0,0,0,0,0],
                               [0,0,0,0,0,1,0,0],
                               [0,0,0,1,0,0,0,0],
                               [0,0,0,0,0,0,0,1]]))


def op_R(angle):
    return qoperator(genpshift(angle,1))

def op_RF(coeff):
    return qoperator(genpshiftF(coeff,1))

def op_SWAPN(n):
    def _binfill(size:int):
        def b2q(n):
            return qbit_0 if n == 0b0 else qbit_1

        states = list()
        states_r = list()
        up_lim = 2 ** size
        for x in range(0,up_lim):
            #print(f"{x} is {x:b} in binary")
            arg = deq()
            arg_r = list()
            n = x
            for f in range(size):           #parsing each number into an array of bits
                arg.appendleft(b2q(n%2))
                arg_r.append(b2q(n%2))    #thus converting every bit into a basic qbit
                n = n>>1
            #print(arg)
            q = qregister(*arg)
            states.append(q)
            q = qregister(*arg_r)
            states_r.append(q)
        return states,states_r

    s,sr = _binfill(n)
    rs = list(zip(s,sr))
    op = qoperator(sp.zeros(2**n))
    for i in rs:
        print(i[0])
        print(i[1])
        a = (i[0] @ i[1])
        op = op + a
    return op

