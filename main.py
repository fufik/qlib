#!/bin/env python
from qlib import *
import numpy as np

def deutsch():
    q = qregister(qbit_0,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = qoperator(matrix.gen(matrix.H,2))
    q = op @ q
    print("2:{}\n=========".format(q.vector))
    op = qoperator(matrix.gen(matrix.EYE,2))
    q = op @ q
    print("3:{}\n=========".format(q.vector))
    op = qoperator(np.kron(matrix.H,matrix.EYE))
    q = op @ q 
    print("4:{}\n=========".format(q.vector))
    q = bases(q)
    return q

def deutschn(n):
    args = list()
    for i in range(n):
        args.append(qbit_0)
    q = qregister(*args,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = qoperator(matrix.gen(matrix.H,n+1))
    q = op @ q
    print("2:{}\n=========".format(q.vector))
    op = qoperator(matrix.gen(matrix.EYE,n+1))
    q = op @ q
    print("3:{}\n=========".format(q.vector))
    op = qoperator(np.kron(matrix.gen(matrix.H,n),matrix.EYE))
    q = op @ q
    print("4:{}\n=========".format(q.vector))
    q = bases(q)
    return q

def fourier(): #Quantum Fourier transform algorithm
    q = qregister(qbit_0,qbit_1)
    print("1:{}\n=========".format(q.vector))
    op = op_H * op_I
    q = op @ q
    print("2:{}\n=========".format(q.vector))
    op_R = qoperator(matrix.genpshiftF(2,1))
    op = op_I * (qbit_0 @ qbit_0) + op_R * (qbit_1 @ qbit_1) 
    q = op @ q
    print("3:{}\n=========".format(q.vector))
    op = op_I * op_H
    q = op @ q
    print("4:{}\n=========".format(q.vector))
    q = qgate.swap2(q)
    print("5:{}\n=========".format(q.vector))
    return q


