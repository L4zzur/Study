from sage.all import *

#! Задание 1
#! Реализация протокола аутентификации Гиллу-Кискате


# ? Предварительный этап центра
def preparing_center(size_n: int = 1024) -> tuple[int, int, int]:
    """Генерация `p`, `q` и `n` в предварительном этапе для центра

    Аргументы:
        size_n (int, optional): размер числа `n`. По умолчанию 1024.

    Возвращает:
        tuple[int, int, int]: числа `p`, `q`, `n`
    """
    p = random_prime(2 ** (size_n // 2))
    q = next_prime(p)
    n = p * q

    return p, q, n


p, q, n = preparing_center()

print(
    f"Предварительный этап центра:\n{p = }\n{q = }\n{n = }\nДлина n равна {len(bin(n)[2:])} бит\n"
)


# ? Предварительный этап претендента
def preparing_challenger(n: int, l: int = 2) -> tuple[int, int]:
    """Генерация `s` и `v` в предварительном этапе для претендента \\
    `(s, n) = 1` и `1 <= s <= n-1`

    Аргументы:
        n (int): известный модуль схемы
        l (int, optional): выбранная степень. По умолчанию 2.

    Возвращает:
        tuple[int, int]: числа `s` и `v`
    """
    s = randint(2, n - 1)  # Секретный ключ претендета
    while gcd(s, n) != 1:
        s = randint(2, n - 1)
    v = pow(s, -l, n)  # Открытый ключ претендета

    return s, v


l = 15
s, v = preparing_challenger(n, l)

print(f"Предварительный этап претендета:\n{v = }\n{s = }\n")


# ? Рабочий этап
def main_actions(n: int, v: int, l: int = 2) -> bool:
    """Рабочий этап протокола аутентификации Гиллу-Кискате

    Аргументы:
        n (int): известный модуль схемы
        v (int): открытый ключ претендета
        l (int, optional): выбранная степень. По умолчанию 2 (Фиата-Шамира).
        t (int, optional): параметр безопасности протокола. По умолчанию 1000.

    Возвращает:
        bool: True, если аутентификация пройдена, False - иначе.
    """
    assert l >= 2

    # ~ Шаг 1. Претендент
    z = randint(1, n - 1)
    x = pow(z, l, n)
    print(f"Шаг 1. Претендент: {x = }, {z = }")

    # ~ Шаг 2. Проверяющий центр
    e = randint(2, l - 1)
    print(f"Шаг 2. Проверяющий центр: {e = }")

    # ~ Шаг 3. Претендет
    y = z * pow(s, e, n) % n
    print(f"Шаг 3. Претендет: {y = }")

    # ~ Шаг 4. Проверяющий центр
    print(f"Шаг 4. Проверяющий центр: {pow(y, l, n) * pow(v, e, n) % n}")
    if x == pow(y, l, n) * pow(v, e, n) % n:
        return True
    return False


result = main_actions(n, v, l)
print(f"Результат проверки аутентификации: {result}")
