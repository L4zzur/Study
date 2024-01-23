from sage.all import *
from random import randint

#! Протокол аутентификации Шнорра 1989


# ? Предварительный этап центра
def preparing_center(p_size: int = 512, q_size: int = 140) -> tuple[int, int, int]:
    """Генерация `p`, `q` и `a` в предварительном этапе для центра

    Аргументы:
        p_size (int, optional): размер числа `p` в битах. По умолчанию 512.
        q_size (int, optional): размер числа `q` в битах. По умолчанию 140.

    Возвращает:
        tuple[int, int, int]: числа `p`, `q`, `n`
    """
    p, q = random_prime(2**p_size, lbound=1000), random_prime(
        2**q_size, lbound=1000
    )
    while (p - 1) % q != 0:
        p, q = random_prime(2**p_size, lbound=1000), random_prime(
            2**q_size, lbound=1000
        )

    a = randint(2, p)
    while (a**q % p) != 1:
        a = randint(2, p)

    return p, q, a


p, q, a = preparing_center(20, 20)

print(
    f"Предварительный этап центра:\n{p = }\n{q = }\n{a = }\n"
    f"Длина p равна {len(bin(p)[2:])} бит\n"
    f"Длина q равна {len(bin(q)[2:])} бит\n"
)


# ? Предварительный этап претендента
def preparing_challenger(p: int, q: int, a: int) -> tuple[int, int]:
    """Генерация `s` и `v` в предварительном этапе для претендента \\
    `s < n` и `v = a^-s (mod p)

    Аргументы:
        n (int): модуль схемы
        a (int): число от центра доверия

    Возвращает:
        tuple[int, int]: числа `s` и `v`
    """
    s = randint(2, q)  # Секретный ключ претендета
    v = pow(a, -s, p)  # Открытый ключ претендета
    return s, v


s, v = preparing_challenger(p, q, a)
print(f"Предварительный этап претендета:\n{v = }\n{s = }\n")


# ? Рабочий этап
def main_actions(p: int, q: int, a: int, v: int, s: int, t: int = 72) -> bool:
    """Рабочий этап протокола Шнорра

    Аргументы:
        p (int): простое число от центра
        q (int): простое число от центра
        a (int): число от центра
        v (int): открытый ключ претендента
        s (int): закрытый ключ претендента
        t (int, optional): длина `t` в битах. По умолчанию 72.

    Возвращает:
        bool: True, если аутентификация пройдена, False - иначе
    """

    # ~ Шаг 1. Претендент
    r = randint(2, q - 1)
    x = a**r % p

    # ~ Шаг 2. Проверяющий центр
    e = randint(0, 2**t - 1)

    # ~ Шаг 3. Претендент
    y = (r + s * e) % q

    # ~ Шаг 4. Проверяющий центр
    if x == (a**y) * (v**e) % p:
        return True
    return False


result = main_actions(p, q, a, v, s, t=5)
print(f"Результат проверки (рабочий этап): {result}")
