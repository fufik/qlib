#!/bin/env python
import qbit
from qregister import qregister
import qgate
import numpy as np
def deutsch():
    q = qregister(qbit.qbit_0,qbit.qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = np.array([[1, 1, 1, 1],
                   [1,-1, 1,-1],
                   [1, 1,-1,-1],
                   [1,-1,-1, 1]],dtype=complex)
    
    op = (1/2) * op
    q = qregister(np.matmul(op,q.vector))
    print("2:{}\n=========".format(q.vector))
    eye = np.eye(2,dtype=complex)
    opnot = np.array([[0,1],[1,0]],dtype=complex)
    had = np.array([[1,1],[1,-1]],dtype=complex) 
    op = np.kron(eye,eye)
    q = qregister(np.matmul(op,q.vector))
    print("3:{}\n=========".format(q.vector))
    op = np.kron(had,eye)
    q = qregister(np.matmul(op,q.vector))
    print("4:{}\n=========".format(q.vector))
