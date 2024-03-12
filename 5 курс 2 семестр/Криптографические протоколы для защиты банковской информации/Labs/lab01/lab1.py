from dataclasses import dataclass
from prettytable import PrettyTable
from sage.all import *

#! Реализация алгоритма разложения числа n на простые числа p и q


def generate_ed(phi_n: int) -> tuple[int, int]:
    """Генерация параметров `e` и `d` для `phi_n`

    Аргументы:
        phi_n (int): функция Эйлера от `n`

    Возвращает:
        tuple[int, int]: параметры `e` и `d`
    """
    e = randint(2, phi_n)
    while gcd(e, phi_n) != 1:
        e = randint(2, phi_n)

    d = pow(e, -1, phi_n)

    return e, d


def repres_k(k: int) -> tuple[int, int]:
    """Представление числа `k` в виде `r*2^t`

    Аргументы:
        k (int): число, необходимое представить

    Возвращает:
        tuple[int, int]: числа `r` и `t`
    """
    t = 0
    while k % 2 == 0:
        t += 1
        k //= 2
    return k, t


def factorize_n(e: int, d: int, n: int) -> tuple[int, int]:
    """Функция, реализующая алгоритм факторизации `n` на `p` и `q`

    Аргументы:
        e (int): параметр
        d (int): параметр
        n (int): модуль

    Возвращает:
        tuple[int, int]: числа `p` и `q`
    """
    g_set = set()

    while True:
        g = randint(2, n)
        if g not in g_set:
            g_set.add(g)

            # * Шаг 1
            gcd_g_n = gcd(g, n)
            if gcd_g_n != 1:
                return int(gcd_g_n), int(n // gcd_g_n)

            # * Шаг 2
            k = e * d - 1
            r, t = repres_k(k)

            for _t in range(1, t + 1):
                y = pow(g, r * (2**_t), n)
                if y == n - 1:
                    break
                elif y == 1:
                    continue
                gcd_y_n = gcd(y - 1, n)
                if gcd_g_n != 1:
                    return int(gcd_y_n), int(n // gcd_y_n)


@dataclass
class Pair:
    """Датакласс для хранения пары `n` и `phi_n`"""

    n: int
    phi_n: int


# ? Задание
data = [
    {"n": 201239, "phi_n": 197880},
    {"n": 233977, "phi_n": 231076},
    {"n": 146017, "phi_n": 144900},
    {"n": 182051, "phi_n": 181152},
    {"n": 485789, "phi_n": 484380},
    {"n": 274849, "phi_n": 273220},
    {"n": 170783, "phi_n": 168168},
    {"n": 649237, "phi_n": 647020},
    {"n": 1563769, "phi_n": 1560996},
    {"n": 548257, "phi_n": 546480},
]


columns = ["n", "phi_n", "p", "q", "p*q", "primefactors", "match"]

table = PrettyTable(["n", "phi_n", "p", "q", "p*q", "p_f", "q_f", "match"])
table.align = "r"


for d in data:
    n = d["n"]
    phi_n = d["phi_n"]
    e, d = generate_ed(phi_n)
    p, q = factorize_n(e, d, n)
    p_test, q_test = [f[0] for f in factor(n)]
    match = (p == p_test and q == q_test) or (p == q_test and q == p_test)
    table.add_row([n, phi_n, p, q, p * q, p_test, q_test, match])
print(table)
