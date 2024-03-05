# Пример из лекции
from sage.all import *

if __name__ == "__main__":
    p, g, x, y = 23, 5, 7, pow(5, 7, 23)
    message = 5

    h = 3

    assert h < p

    k = 5
    while gcd(k, p - 1) != 1:
        k = randint(1, p - 1)

    r = pow(g, k, p)
    print(f"{r=}")
    u = (h - x * r) % (p - 1)
    print(f"{u=}")

    s = (inverse_mod(k, p - 1) * u) % (p - 1)
    print(f"{s=}")

    print(pow(y, r, p) * pow(r, s, p) % p)
    print(pow(g, h, p))
    if pow(y, r, p) * pow(r, s, p) % p == pow(g, h, p):
        print("OK")
    else:
        print("NOT OK")
