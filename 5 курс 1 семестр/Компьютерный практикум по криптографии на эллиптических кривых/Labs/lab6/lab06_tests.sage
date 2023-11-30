from random import randint
import time
from sage.all import *


def test_Prove_prime(p):
    Cert = Prove_prime(p)
    return Check_prime(p, Cert) == "Accept"


def Check_prime(p, Cert):
    p_0 = p
    for (a, b), L, p_i in Cert:
        assert p_0 % 2
        assert p_0 % 3
        assert gcd(4 * a ^ 3 + 27 * b ^ 2, p_0)
        assert p_i > (sqrt(sqrt(p_0)) + 1) ^ 2
        assert str(L) != "(0 : 1 : 0)"
        assert str(p_i * L) == "(0 : 1 : 0)"
        p_0 = p_i
    return "Accept"


def MillerRabin(n, a):
    """
    Тест Миллера-Рабина определяет,
    является ли число n составным или
    возможно простым
    """
    # ? Step 1
    q = n - 1
    k = 0
    while q % 2 == 0:
        k += 1
        q //= 2
    # ? Step 2
    a = pow(a, q, n)
    # ? Step 3
    if a == 1 % n:
        return True
    # ? Step 4
    for _ in range(k - 1):
        # ? Step 5
        if a == n - 1:
            return True
        # ? Step 6
        a = a ^ 2 % n
    # ? Step 7
    return False


def gen_curve(p):
    while True:
        # ? Step 1
        a, b = randint(1, p - 1), randint(1, p - 1)
        E = EllipticCurve(GF(p), [a, b])

        d = 4 * a ^ 3 + 27 * b ^ 2
        ord_E = E.order()

        # ? Step 2
        if ord_E % 2 == 0 and gcd(d, p) == 1:
            q = ord_E // 2
            if q % 2 == 0 or q % 3 == 0 or MillerRabin(p, q) == False:
                continue
            return a, b, q


def find_point(p, q, a, b):
    """
    Получаем на вход p,q,A,B
    На выход возвращаем найденную точку L порядка q
    """
    E = EllipticCurve(GF(p), [a, b])
    inf_point = E(0, 1, 0)
    while True:
        # ? Step 1
        x = GF(p).random_element()
        y = (x ^ 3 + a * x + b) % p
        if y.is_square():
            # ? Step 2
            y = y.sqrt()
            L = E(x, y)
            # ? Step 3
            if q * L != inf_point:
                continue
            # ? Step 4
            return L


def Prove_prime(p):
    """
    TESTS::
        sage: test_Prove_prime(1000003)
        True

        sage: test_Prove_prime(100000000003)
        True
    """

    LB = 2 ^ 6
    # ? Step 1
    i = 0
    p_i = p
    C = []
    lgp = log(p) ^ (log(log(p)))
    # ? Step 2
    while p_i > p // 5:
        # ? Step 2.1
        a, b, p_i_1 = gen_curve(p_i)
        # ? Step 2.2
        L_i = find_point(p_i, p_i_1, a, b)
        # ? Step 2.3
        i += 1
        # ? Step 2.4
        if i >= lgp or p_i % 3 == 0 or p_i % 3 == 0 or not is_prime(p_i_1):
            continue
        C += [((a, b), L_i, p_i_1)]
        p_i = p_i_1
    return C
