from fpylll import *
import copy

# документация https://readthedocs.org/projects/fpylll/downloads/pdf/latest/
"""
A = IntegerMatrix.random(30, "qary", k=15, bits=30)
#print(A)
dim = A.nrows
#print('dimension:', dim)


M = GSO.Mat(A, float_type="d") #float_type \in {'d', 'dd', 'qd','mpfr'}
print(M.get_r(0,0))
print(M.d) # размерность решетки
print(M.B) # текущий базис решетки
M.update_gso() # вычислить все интересные матрицы (Грам-Шмидт ортогонализацию, mu, ...)
print(M.get_r(1,1))
print(A[0].norm()**2) # норма первого вектра в базисе
print('before:', [M.get_r(i,i) for i in range(dim)]) # выдать все r_ii


L = LLL.Reduction(M, delta=0.99, eta=0.501) # создание объекта LLL
L() # запуск LLL редукции __call__
print('after:', [M.get_r(i,i) for i in range(dim)])
print(A)
"""

A = IntegerMatrix.random(100, "qary", k=50, bits=30)
dim = A.nrows
Ac = copy.deepcopy(A) # копия A
U = IntegerMatrix.identity(dim)
UinvT = IntegerMatrix.identity(dim)

M_transf = GSO.Mat(Ac, float_type="d", U = U, UinvT = UinvT) #U --  матрица преобразования от A к LLL-редцуцированному Ac
print(M_transf.inverse_transform_enabled) # LLL вычисляет в процессе U

L = LLL.Reduction(M_transf, delta=0.99, eta=0.501)
L()
print(A[1])
print(Ac[1])
print((U*A)[1])
