from sage.all import *


# Проверять работу своей функции orderBSGS() с помощью встроенной функции order():
def test_orderBSGS(i):
    q = Primes().next(2 ^ (16 * i) + 1)
    a = ZZ.random_element(1, q - 1)
    b = ZZ.random_element(1, q - 1)
    F = GF(q)
    E = EllipticCurve(F, [a, b])
    return orderBSGS(a, b, q) == E.order()


def orderPoint(q, E, P):
    # Step 1
    Q = (q + 1) * P

    # Step 2
    m = ceil(q ^ (1 / 4))
    L_j = set()
    L_jP = set()
    L = []
    M = 0

    z = E(0)
    for j in range(0, m + 1):
        L.append(z)
        L_j.add(z[0])
        L_jP.add(z[1])
        z += P

    # Step 3
    double_Mp = 2 * m * P
    check = Q - m * double_Mp

    for k in range(-m, m + 1):
        if check[0] in L_j:
            if check[1] in L_jP:
                j = L.index(check)
                M = q + 1 + 2 * m * k - j
                break
            elif -check[1] in L_jP:
                j = L.index(-check)
                M = q + 1 + 2 * m * k + j
                break
        check += double_Mp

    # Step 4
    while True:
        M = int(M)
        fctr = factor(M)
        for pi in fctr:
            if (M // pi[0]) * P == E(0):
                M = M // pi[0]
                break
        else:
            break

    return M


def orderBSGS(a, b, q):
    """
    TESTS::
        sage: [test_orderBSGS(i) for i in range(1,5)]
        [True, True, True, True]
    """
    E = EllipticCurve(GF(q), [a, b])
    # Step 1
    L = 1

    # Step 2
    P = E.random_point()
    # Step 2
    r = orderPoint(q, E, P)
    # Step 3
    L = lcm(L, r)
    # Step 4
    if L >= 4 * ceil(sqrt(q)) and L < q + 1 - 2 * ceil(sqrt(q)):
        m = (q + 1 + 2 * ceil(sqrt(q))) // L
        return m * L
    return L
