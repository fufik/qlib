from qregister import qregister
from qbit      import qbit
import qbit
import numpy as np

def op_cnot(qrin: qregister):
    if len(qrin)!= 2:
        raise QbitError("CNOT input is not 2 qbit in length ")
    
    op = np.array([[1,0,0,0],
                   [0,1,0,0],
                   [0,0,0,1],
                   [0,0,1,0]],dtype=complex)
    return qregister(np.matmul(op,qrin.vector))


def op_ccnot(qrin: qregister):
    if len(qrin)!= 3:
        raise QbitError("CCNOT input is not 3 qbit in length ")
    
    op = np.arrray([[1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0],
                    [0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,1,0]],dtype=complex)
    return qregister(np.matmul(op,qrin.vector))
    #return qregister(qrin[0],qrin[1],qrin[2].op_not()) \
    #    if qrin[0] == qbit.qbit_1 and qrin[1] == qbit.qbit_1 \
    #    else qregister(qrin[0],qrin[1],qrin[2]) 

def swap2(qrin: qregister):
    if len(qrin)!= 2:
        raise QbitError("SWAP2 input is not 2 qbit in length ")
    op = np.array([[1,0,0,0],
                   [0,0,1,0],
                   [0,1,0,0],
                   [0,0,0,1]],dtype=complex)
    return qregister(np.matmul(op,qrin.vector))

def swap3(qrin: qregister):
    if len(qrin)!= 3:
        raise QbitError("SWAP3 input is not 2 qbit in length ")
    op = np.arrray([[1,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0],
                    [0,0,1,0,0,0,0,0],
                    [0,0,0,0,0,0,1,0],
                    [0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,1,0,0],
                    [0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,0,1]],dtype=complex)
    return qregister(np.matmul(op,qrin.vector))
#
#def op_ncnot(qrin: qregister):
#    
#    op = np.identity(len(qrin)+1,dtype=complex)
#    return np.matmul(op,qrin.vector)
