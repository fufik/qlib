import numpy as np
import cmath
import math
EYE = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],dtype=complex)
Y = np.array([[0,1j],[1j,0]],dtype=complex)
Z = np.array([[1,0],[0,-1]],dtype=complex)
H = (1/cmath.sqrt(2)) * np.array([[1,1],[1,-1]],dtype=complex)

def genpshift(angle,n):
    a = np.eye(2**n,dtype=complex)
    a[2**n-1][2**n-1] = cmath.exp(angle*1j) 
    return a

def genpshiftF(m,n):
    a = np.eye(2**n,dtype=complex)
    a[2**n-1][2**n-1] = cmath.exp(2*math.pi*1j/2*m) 
    return a

def gen(matrix,n):
    if type(matrix) is str:
        if matrix == "cnot":
            a = np.eye(2**n,dtype=complex)
            a[2**n - 2][2**n -2] = 0
            a[2**n - 1][2**n -1] = 0
            a[2**n - 2][2**n -1] = 1
            a[2**n - 1][2**n -2] = 1
            return a
    if n == 1:
        return matrix
    return np.kron(matrix,gen(matrix,n-1))


