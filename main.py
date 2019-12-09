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
    q = bases(q)
    return q

def deutschn(n):
    args = list()
    for i in range(n):
        args.append(qbit_0)
    q = qregister(*args,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = matrix.gen(matrix.H,n+1)
    q = qregister(np.matmul(op,q.vector))
    print("2:{}\n=========".format(q.vector))
    op = matrix.gen(matrix.EYE,n+1)
    q = qregister(np.matmul(op,q.vector))
    print("3:{}\n=========".format(q.vector))
    op = np.kron(matrix.gen(matrix.H,n),matrix.EYE)
    q = qregister(np.matmul(op,q.vector))
    print("4:{}\n=========".format(q.vector))
    q = bases(q)
    return q

def fourier(): #Quantum Fourier transform algorithm
    q = qregister(qbit_0,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = np.kron(matrix.H,matrix.EYE)
    q = qregister(np.matmul(op,q.vector))
    print("2:{}\n=========".format(q.vector))
    q = qgate.swap2(q)
    op = matrix.genpshiftF(2,2)
    q = qregister(np.matmul(op,q.vector))
    print("3:{}\n=========".format(q.vector))
    op = np.kron(matrix.H,matrix.EYE)
    q = qregister(np.matmul(op,q.vector))
    print("4:{}\n=========".format(q.vector))
    return q


