from fpylll import *

FPLLL.set_random_seed(2023)
A = IntegerMatrix(20, 20)
A.randomize("qary", k=10, q=256)
print(A)
B = IntegerMatrix(25, 25)
B.randomize("uniform", bits=13)
print(B)

AGSO = GSO.Mat(A)
print(AGSO.get_mu(1, 0))
_ = AGSO.update_gso()
print(AGSO.get_mu(1, 0))
print(AGSO.get_mu(2, 0))
