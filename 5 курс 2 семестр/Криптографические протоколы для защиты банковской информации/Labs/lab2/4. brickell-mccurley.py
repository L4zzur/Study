from sage.all import *
from random import randint

#! Протокол аутентификации Брикелла - Мак-Карли 1990-1991


# ? Предварительный этап центра
def preparing_center(
    p_size: int = 512, q_size: int = 512, k: int = 140
) -> tuple[int, int, int, int]:
    """Генерация `p`, `q`, `w` и `a` в предварительном этапе для центра

    Аргументы:
        p_size (int, optional): размер числа `p` в битах. По умолчанию 512.
        q_size (int, optional): размер числа `q` в битах. По умолчанию 512.
        k (int, optional): размер числа `k` в битах. По умолчанию 140.

    Возвращает:
        tuple[int, int, int, int]: числа `p`, `q`, `w`, `a`
    """
    p = random_prime(2**p_size)
    q = random_prime(2**q_size, lbound=2**k)
    w = random_prime(2**q_size, lbound=2**k)

    while (p - 1) % (q * w) != 0 or (p - 1) % q**2 == 0:
        p = next_prime(p)

    a = randint(2, p)
    while (a**q % p) != 1:
        a = randint(2, p)

    return p, q, w, a


p, q, w, a = preparing_center(p_size=10, q_size=10, k=5)
print(
    f"Предварительный этап центра:\n{p = }\n{q = }\n{w = }\n{a = }\n"
    f"Длина p равна {len(bin(p)[2:])} бит\n"
    f"Длина q равна {len(bin(q)[2:])} бит\n"
)


# ? Предварительный этап претендента
def preparing_challenger(p: int, a: int) -> tuple[int, int]:
    """Генерация `a`, `s` и `v` в предварительном этапе для претендента

    Аргументы:
        p (int): открытое простое число центра

    Возвращает:
        tuple[int, int]: числа `s`, `v`
    """

    s = randint(2, p)  # Секретный ключ претендета
    v = pow(a, -s, p)  # Открытый ключ претендета

    return s, v


s, v = preparing_challenger(p, a)
print(f"Предварительный этап претендета:\n{a = }\n{v = }\n{s = }\n")


# ? Рабочий этап
def main_actions(p: int, a: int, s: int, v: int, t: int = 72) -> bool:
    """Рабочий этап протокола Брикелла - Мак-Карли

    Аргументы:
        p (int): открытое простое число центра
        a (int): число от центра доверия
        s (int): секретный ключ претендента
        v (int): открытый ключ претендента
        t (int, optional): длина `t` в битах. По умолчанию 72.

    Возвращает:
        bool: True, если аутентификация пройдена, False - иначе.
    """
    # ~ Шаг 1. Претендент
    r = randint(2, p)
    x = a**r % p

    # ~ Шаг 2. Проверяющий центр
    e = randint(0, 2**t - 1)

    # ~ Шаг 3. Претендент
    y = (r + s * e) % (p - 1)

    # ~ Шаг 4. Проверяющий центр
    if x == (a**y) * (v**e) % p:
        return True
    return False


result = main_actions(p, a, s, v, t=5)
print(f"Результат проверки (рабочий этап): {result}")
