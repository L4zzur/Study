import numpy as np

w = np.exp(-2 * np.pi * 1j / 8)

F_8 = np.matrix(
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, w, w**2, w**3, w**4, w**5, w**6, w**7],
        [1, w**2, w**4, w**6, 1, w**2, w**4, w**6],
        [1, w**3, w**6, w, w**4, w**7, w**2, w**5],
        [1, w**4, 1, w**4, 1, w**4, 1, w**4],
        [1, w**5, w**2, w**7, w**4, w, w**6, w**3],
        [1, w**6, w**4, w**2, 1, w**6, w**4, w**2],
        [1, w**7, w**6, w**5, w**4, w**3, w**2, w],
    ]
)


w_in = [0, 0, 0, 1, 0, 0, 0, 0]

ws = []
for i in range(8):
    print(i, ": ", w**i)
    ws.append(w**i)

res = w_in * F_8
res = res.transpose()
for i in res:
    # print(i[0, 0])
    print(f"w_{ws.index(i[0, 0])}")
