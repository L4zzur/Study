from sage.all import *

################
# Для тестирования функции nTorsionPoints(n, a, b, q)
# можно пользоваться встроенной функцией division_points(n).
# E = EllipticCurve(F, [a, b])
# Origin = E(0)
# Origin.division_points(n)
################


def test_nTorsionPoints(n, a, b, q):
    t1 = nTorsionPoints(n, a, b, q)
    F = t1[0][0].parent()
    E = EllipticCurve(F, [F(a), F(b)])
    t2 = [n * E(P) == E(0) for P in t1]
    return [len(set(t1)), len(set(t2)), t2[0]]


def psi(n, a, b, q, _n):
    x, y = var("x y")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        if _n % 2 != 0:
            return 2 * y
        else:
            return 2 * 2 * (x ^ 3 + a * x + b)
    elif n == 3:
        return 3 * x ^ 4 + 6 * a * x ^ 2 + 12 * b * x - a ^ 2
    elif n == 4:
        if _n % 2 != 0:
            return (
                4 * y * (
                    x ^ 6 
                    + 5 * a * x ^ 4 
                    + 20 * b * x ^ 3 
                    - 5 * a ^ 2 * x ^ 2 
                    - 4 * a * b * x 
                    - 8 * b ^ 2 
                    - a ^ 3
                )
            )
        else:
            return (
                4 * 2 * (x ^ 3 + a * x + b) * (
                    x ^ 6 
                    + 5 * a * x ^ 4 
                    + 20 * b * x ^ 3 
                    - 5 * a ^ 2 * x ^ 2 
                    - 4 * a * b * x 
                    - 8 * b ^ 2 
                    - a ^ 3
                )
            )
    elif n % 2 == 1:
        return (
            psi((n - 1) // 2 + 2, a, b, q, _n) * (psi((n - 1) // 2, a, b, q, _n)) ^ 3
            - psi((n - 1) // 2 - 1, a, b, q, _n) * psi((n - 1) // 2 + 1, a, b, q, _n) ^ 3
        )
    else:
        return (
            (2 * y) ^ -1
            * psi(n // 2, a, b, q, _n)
            * (
                psi(n // 2 + 2, a, b, q, _n) * psi(n // 2 - 1, a, b, q, _n) ^ 2
                - psi(n // 2 - 2, a, b, q, _n)  * psi(n // 2 + 1, a, b, q, _n) ^ 2
            ) 
        )


def nTorsion_extension_deg(n, a, b, q):
    """
    TESTS::
        sage: nTorsion_extension_deg(3, 3, 17, 23)
        2

        sage: nTorsion_extension_deg(2, 1, 11, 41)
        1

        sage: nTorsion_extension_deg(5, 2, 21, 53)
        4

        sage: nTorsion_extension_deg(7, 1, 7, 11)
        21
    """
    E = EllipticCurve(GF(q), [a, b])
    x, y = var("x y")

    # * Шаг 1, построение psi_n
    psi_n = psi(n, a, b, q, n)
    for i in range(1, 100):
        psi_n = psi_n.substitution_delayed(y ^ i, (x ^ 3 + a * x + b) ^ (i / 2))

    R.<x> = PolynomialRing(GF(q))
    psi_n = R(psi_n)
    psi_n = psi_n.change_ring(Zmod(q))

    # * Шаг 2, факторизация psi_n
    factor_psi = [f[0] for f in factor(psi_n)]

    # * Шаг 3, нахождение l
    l = lcm([f.degree() for f in factor_psi])

    # * Шаг 4, нахождение f_i т.ч. 2*deg(f_i) не делит l
    for f in factor_psi:
        if l % (2 * f.degree()) != 0:
            f_i = f
            d_i = f.degree()
            break

    # * Шаг 5, нахождение c
    x_i = [root[0] for root in f_i.roots(ring=GF(q ^ d_i))]
    x_i = x_i[0]
    _c = x_i ^ 3 + a * x_i + b
    c = _c.is_square()

    # * Шаг 6, проверка c = -1
    if c == -1:
        return 2 * l

    # * Шаг 7
    d = lcm(Mod(q, n).multiplicative_order(), d_i)
    if d == l or l == n * d:
        return l
    return 2 * l


def nTorsionPoints(n, a, b, q):
    """
    TESTS::
        sage: test_nTorsionPoints(3, 3, 17, 23)
        [9, 1, True]

        sage: test_nTorsionPoints(2, 1, 11, 41)
        [4, 1, True]

        sage: test_nTorsionPoints(5, 2, 21, 53)
        [25, 1, True]

        sage: test_nTorsionPoints(7, 1, 7, 11)
        [49, 1, True]
    """
    E = EllipticCurve(GF(q), [a, b])
    
    points = []

    psi_n = E.division_polynomial(n)
    d = nTorsion_extension_deg(n, a, b, q)

    factor_psi = [f[0] for f in factor(psi_n)]

    for f in factor_psi:
        x = [i[0] for i in f.roots(ring=GF(q ^ d))]
        points += [(x_i, sqrt(x_i ^ 3 + a * x_i + b)) for x_i in x]
    if n != 2:
        points += [(i, -j) for i, j in points]
    points += [(0, 1, 0)]
    return points


# Вопросы:
# 1. Связь между многочленом деления и степенью расширения
# 2. Приложение билинейных отображений (кроме лекции)




