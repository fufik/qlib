import numpy as np
import cmath
EYE = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],dtype=complex)
Y = np.array([[0,1j],[1j,0]],dtype=complex)
Z = np.array([[1,0],[0,-1]],dtype=complex)
H = (1/cmath.sqrt(2)) * np.array([[1,1],[1,-1]],dtype=complex)

def gen(matrix,n):
    if n == 1:
        return matrix
    return np.kron(matrix,gen(matrix,n-1))
