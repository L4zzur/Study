import numpy as np


I = np.matrix(
    [
        [1, 0],
        [0, 1],
    ]
)

S = np.matrix(
    [
        [1, 0],
        [0, 1j],
    ]
)
CNOT = np.matrix(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
)


I_S1 = np.tensordot(S, I, 0)
I_S1 = I_S1.transpose((0, 2, 1, 3)).reshape((4, 4))
print(I_S1)
res1 = I_S1 * CNOT
print(res1)
print()

I_S2 = np.tensordot(S, I, 0)
I_S2 = I_S2.transpose((0, 2, 1, 3)).reshape((4, 4))
print(I_S2)
res2 = CNOT * I_S2
print(res2)
print()

print(res1 == res2)
print(I_S1 == I_S2)
