import numpy as np


I = np.matrix(
    [
        [1, 0],
        [0, 1],
    ]
)

H = np.matrix(
    [
        [1, 1],
        [1, -1],
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

I_H = np.tensordot(H, I, 0)
I_H = I_H.transpose((0, 2, 1, 3)).reshape((4, 4))
print(I_H)
res2 = CNOT * I_H
print(res2)
print()


print([1, 0, 0, 0] * res2)
