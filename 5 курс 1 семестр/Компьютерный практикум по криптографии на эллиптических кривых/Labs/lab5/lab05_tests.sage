from sage.all import *


def find_multiplier(P, Q, a, N):
    inf_point = [0, 1, 0]

    if Q == inf_point:
        return False, P
    if P == inf_point:
        return False, Q

    x1, y1, z1 = P
    x2, y2, z2 = Q

    if x1 == x2 and y1 == -y2:
        return False, inf_point

    d = gcd(x1 - x2, N)
    if d != 1 and d != N:
        return True, d

    if x1 == x2:
        d = gcd(y1 + y2, N)
        if d > 1:
            return True, d
        alpha = ((3 * x1 ^ 2 + a) / (y1 + y2)) % N
    else:
        alpha = ((y2 - y1) / (x2 - x1)) % N

    beta = (y1 - alpha * x1) % N

    x3 = (alpha ^ 2 - x1 - x2) % N
    y3 = (-(alpha * x3 + beta)) % N

    return False, [x3, y3, 1]


def multiply(P, N, a, k):
    inf_point = [0, 1, 0]
    Q = inf_point
    bin_k = [int(i) for i in list(bin(k)[2:])]

    for i in bin_k:
        is_div, Q = find_multiplier(Q, Q, a, N)
        if is_div:
            return is_div, Q
        if i == 1:
            is_div, Q = find_multiplier(P, Q, a, N)
            if is_div:
                return is_div, Q

    if Q == inf_point:
        return False, inf_point
    else:
        return False, Q


def factorECM(N: int):
    """
    TESTS::
      sage: factorECM(100070000190133)
      [10007, 10000000019]

      sage: factorECM(100181800505809010267)
      [5009090003, 20000000089]

      sage: factorECM(6986389896254914969335451)
      [833489857, 8382093480298843]
    """
    while True:
        # Step 1
        a = Integers(N).random_element()
        x = Integers(N).random_element()
        y = Integers(N).random_element()
        b = (y ^ 2 - x ^ 3 - a * x) % N
        _gcd = gcd((4 * a ^ 3 + 27 * b ^ 2) % N, N)

        if _gcd != 1:
            return _gcd

        if _gcd == 1:
            P = [x, y, 1]
            B1 = ceil(exp((1 / sqrt(2)) * log(N) ^ 0.5 * log(log(N)) ^ 0.5))
            B2 = B1

            for p_i in Primes():
                if p_i > B1:
                    break

                e_i = 1
                pe_i = p_i
                while pe_i < B1:
                    is_divisor, P = multiply(P, N, a, pe_i)
                    if is_divisor:
                        return sorted([int(P), N // int(P)])
                    e_i += 1
                    pe_i = p_i ^ e_i
            continue
        if _gcd != N:
            return sorted([int(_gcd), N // int(_gcd)])
