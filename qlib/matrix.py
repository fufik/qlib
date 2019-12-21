import sympy as sp
import cmath
import math
EYE = sp.eye(2)
X = sp.Matrix([[0,1],[1,0]])
Y = sp.Matrix([[0,-1j],[1j,0]])
Z = sp.Matrix([[1,0],[0,-1]])
H = (1/cmath.sqrt(2)) * sp.Matrix([[1,1],[1,-1]])

def genpshift(angle,n):
    a = sp.eye(2**n)
    a[2**n-1,2**n-1] = cmath.exp(angle*1j) 
    return a

def genpshiftF(m,n):
    a = sp.eye(2**n)
    a[2**n-1,2**n-1] = cmath.exp(2*math.pi*1j/2*m) 
    return a

def gen(matrix,n):
    if type(matrix) is str:
        if matrix == "cnot":
            a = sp.eye(2**n)
            a[2**n - 2,2**n -2] = 0
            a[2**n - 1,2**n -1] = 0
            a[2**n - 2,2**n -1] = 1
            a[2**n - 1,2**n -2] = 1
            return a
    if n == 1:
        return matrix
    return sp.Matrix(sp.kronecker_product(matrix,gen(matrix,n-1)))


