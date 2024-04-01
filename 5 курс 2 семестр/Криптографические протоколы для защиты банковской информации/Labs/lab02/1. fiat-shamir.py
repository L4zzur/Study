from random import randint

from sage.all import *

#! Протокол аутентификации Фиата - Шамира 1986


# ? Предварительный этап центра с учетом длины 1024 бит и упрощения вычислений n = (4 * p + 3) * (4 * q + 3)
def preparing_center(size_n: int = 1024) -> tuple[int, int, int]:
    """Генерация `p`, `q` и `n` в предварительном этапе для центра

    Аргументы:
        size_n (int, optional): размер числа `n`. По умолчанию 1024.

    Возвращает:
        tuple[int, int, int]: числа `p`, `q`, `n`
    """
    p = random_prime(2 ** (size_n // 2))
    q = next_prime(p)
    n = (4 * p + 3) * (4 * q + 3)

    return p, q, n


p, q, n = preparing_center()

print(
    f"Предварительный этап центра:\n{p = }\n{q = }\n{n = }\nДлина n равна {len(bin(n)[2:])} бит\n"
)


# ? Предварительный этап претендента
def preparing_challenger(n: int) -> tuple[int, int]:
    """Генерация `s` и `v` в предварительном этапе для претендента \\
    `(s, n) = 1` и `1 <= s <= n-1`

    Аргументы:
        n (int): известный модуль схемы

    Возвращает:
        tuple[int, int]: числа `s` и `v`
    """
    s = randint(2, n - 1)  # Секретный ключ претендета
    while gcd(s, n) != 1:
        s = randint(2, n - 1)

    v = pow(s, 2, n)  # Открытый ключ претендета
    return s, v


s, v = preparing_challenger(n)

print(f"Предварительный этап претендета:\n{v = }\n{s = }\n")


# ? Рабочий этап
def main_actions(n: int, v: int, t: int = 1000) -> bool:
    """Рабочий этап протокола Фиата-Шамира

    Аргументы:
        n (int): известный модуль схемы
        v (int): открытый ключ претендета
        t (int, optional): параметр безопасности протокола. По умолчанию 1000.

    Возвращает:
        bool: True, если аутентификация пройдена, False - иначе.
    """
    checks = 0
    for i in range(t):
        # ~ Шаг 1. Претендент
        r = randint(2, n - 1)
        x = pow(r, 2, n)

        # ~ Шаг 2. Проверяющий центр
        e = randint(0, 1)

        # ~ Шаг 3. Претендет
        if e == 0:
            y = r
        else:
            y = (r * s) % n

        # ~ Шаг 4. Проверяющий центр
        if y != 0:
            if (pow(y, 2, n)) == (x * pow(v, e, n) % n):
                checks += 1

    return t == checks


result = main_actions(n, v)
print(f"Результат проверки (рабочий этап): {result}")
