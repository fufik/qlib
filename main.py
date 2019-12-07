#!/bin/env python
from qlib import *
import numpy as np

#TODO check it out
def deutsch():
    q = qregister(qbit_0,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = matrix.gen(matrix.H,2)
    q = qregister(np.matmul(op,q.vector))
    print("2:{}\n=========".format(q.vector))
    op = matrix.gen(matrix.EYE,2)
    q = qregister(np.matmul(op,q.vector))
    print("3:{}\n=========".format(q.vector))
    op = np.kron(matrix.H,matrix.EYE)
    q = qregister(np.matmul(op,q.vector))
    print("4:{}\n=========".format(q.vector))
    #q = bases(q)
    return q


