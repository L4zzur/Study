from sage.all import *


def Sum(a, b, q, x1, y1, x2, y2):
    """
    TESTS::
        sage: Sum(3, 10, 11, 4, 3, 1, 5)
        [4, 8]

        sage: Sum(978, 8052, 10007, 5593, 1759, 1298, 1966)
        [3420, 5599]

        sage: Sum(37, 33, 59, 34, 11, 0, infinity)
        [34, 11]

        sage: Sum(17, 29, 59, 42, 14, 42, 45)
        [0, infinity]

        sage: Sum(14, 6, 23, 18, 8, 4, 12)
        Error: the point [4,12] is not on E
    """

    K = GF(q)

    # Проверка на сложение с бесконечно удаленной точкой
    if x1 == 0 and y1 == infinity:
        x3 = x2
        y3 = y2
        return [x3, y3]
    if x2 == 0 and y2 == infinity:
        x3 = x1
        y3 = y1
        return [x3, y3]

    # Проверка, что точка [x1, y1] лежит на кривой E
    if (y1 ^ 2 % q) != ((x1 ^ 3 + a * x1 + b) % q):
        print(f"Error: the point [{x1},{y1}] is not on E")
        return None

    # Проверка, что точка [x2, y2] лежит на кривой E
    if (y2 ^ 2 % q) != ((x2 ^ 3 + a * x2 + b) % q):
        print(f"Error: the point [{x2},{y2}] is not on E")
        return None

    # Случай x1 != x2
    if x1 != x2:
        m = (y2 - y1) / (x2 - x1) % q
        x3 = (m ^ 2 - x1 - x2) % q
        y3 = (m * (x1 - x3) - y1) % q
        return [x3, y3]

    # Случай x1 = x2, y1 != y2 или P1 = P2, y1 = 0
    if ((x1 == x2) and (y1 != y2)) or ((x1 == x2) and (y1 == y2) and (y1 == 0)):
        x3 = 0
        y3 = "infinity"
        print(f"[{x3}, {y3}]")
        return None

    # Случай P1 = P2, y != 0
    if (x1 == x2) and (y1 == y2) and (y1 != 0):
        m = (3 * x1 ^ 2 + a) / (2 * y1) % q
        x3 = (m ^ 2 - 2 * x1) % q
        y3 = (m * (x1 - x3) - y1) % q
        return [x3, y3]


def SumProj(a, b, q, x1, y1, z1, x2, y2, z2):
    """
    TESTS::
        sage: SumProj(57, 1, 59, 18, 29, 1, 5, 23, 1)
        [2,51,1]

        sage: SumProj(49, 41, 59, 57, 42, 1, 1, 0, 1)
        [57,42,1]
    """

    # Бесконечно удаленная точка в проективных координатах
    infinity_p = (0, 1, 0)

    # Проверка на сложение с бесконечно удаленной точкой
    if (x1, y1, z1) == infinity_p:
        x3 = x2
        y3 = y2
        z3 = z2
        print(f"[{x3},{y3},{z3}]")
        return None

    # Проверка на сложение с бесконечно удаленной точкой
    if (x2, y2, z2) == infinity_p:
        x3 = x1
        y3 = y1
        z3 = z1
        print(f"[{x3},{y3},{z3}]")
        return None

    # Проверка, что точка [x1, y1, z1] лежит на кривой E
    if ((y1 ^ 2 * z1) % q) != ((x1 ^ 3 + a * x1 * z1 ^ 2 + b * z1 ^ 3) % q):
        x3 = x2
        y3 = y2
        z3 = z2
        print(f"[{x3},{y3},{z3}]")
        return None

    # Проверка, что точка [x2, y2, z2] лежит на кривой E
    if ((y2 ^ 2 * z2) % q) != ((x2 ^ 3 + a * x2 * z2 ^ 2 + b * z2 ^ 3) % q):
        x3 = x1
        y3 = y1
        z3 = z1
        print(f"[{x3},{y3},{z3}]")
        return None

    u = (y2 * z1 - y1 * z2) % q
    v = (x2 * z1 - x1 * z2) % q
    w = (u ^ 2 * z1 * z2 - v ^ 3 - 2 * v ^ 2 * x1 * z2) % q

    x3 = (v * w) % q
    y3 = (u * (x1 * v ^ 2 * z2 - w) - v ^ 3 * z2 * y1) % q
    z3 = (v ^ 3 * z1 * z2) % q

    print(f"[{x3/z3 % q},{y3/z3 % q},{z3/z3 % q}]")
    return None


def Mul(a, b, q, x1, y1, k):
    """
    TESTS::
        sage: Mul(15, 2, 23, 8, 6, 19)
        [10, 5]

        sage: Mul(16, 27, 37, 19, 30, 24)
        [0, infinity]

        sage: Mul(1596531425664112104, 8469635381684191285, 17364269638771469903, 13402180624743596496, 13385993554720361919, 4872114054757385562)
        [7833260487853357138, 12663396679974011624]
    """

    # Проверка, что точка [x1, y1] лежит на кривой E
    if (y1 ^ 2 % q) != ((x1 ^ 3 + a * x1 + b) % q):
        print(f"Error: the point [{x1},{y1}] is not on E")
        return None

    # Переводим в двоичное представление
    bin_k = [int(i) for i in list(bin(k)[2:])]

    # Создаем объект поля Fq и эллиптической кривой
    K = GF(q)
    E = EllipticCurve(GF(q), [a, b])

    # Переменные, O - нейтральный элемент, P - входная точка
    O = E(0)
    P = E([x1, y1])
    Q = O

    # Перебираем побитово в обратном порядке k
    for i in bin_k:
        Q += Q  # Удвоение точки
        if i == 1:
            Q += P  # Сложение с точкой P, если бит равен 1

    if Q == O:
        print(f"[0, infinity]")
        return None
    else:
        return list(Q)[:2]  # Первые две координаты афинные
