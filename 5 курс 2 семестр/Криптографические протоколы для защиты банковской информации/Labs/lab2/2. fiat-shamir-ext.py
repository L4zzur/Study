from sage.all import *
from random import randint

#! Усовершенствованный вариант протокола аутентификации Фиата - Шамира


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
def preparing_challenger(n: int, k: int = 5) -> tuple[list[int], list[int]]:
    """Генерация набора `s` и строки `v` в предварительном этапе для претендента \\
    `(s, n) = 1` и `1 <= s <= n-1`, `v_i = s_i^2 (mod n)`

    Args:
        n (int): модуль схемы
        k (int, optional): количество чисел в строке `v`. По умолчанию 5.

    Returns:
        tuple[list[int], list[int]]: набор `s` и строка `v`
    """
    s = []  # Секретный ключ претендета

    while len(s) < k:
        s_i = randint(2, n - 1)
        if gcd(s_i, n) == 1:
            s.append(s_i)

    v = [s_i**2 % n for s_i in s]  # Открытый ключ претендета

    return s, v


s, v = preparing_challenger(n)
print(f"Предварительный этап центра: набор s и строка v сгенерированы.")


# ? Рабочий этап
def main_actions(s: list[int], v: list[int], n: int, k: int = 5, t: int = 4) -> bool:
    """Рабочий этап усовершенствованного протокола Фиата-Шамира

    Аргументы:
        s (list[int]): набор случайных чисел `s`
        v (list[int]): набор случайных чисел `v`
        k (int, optional): количество чисел в строке `v`. По умолчанию 5.
        t (int, optional): Количество проходов. По умолчанию 4.

    Возвращает:
        bool: True, если аутентификация пройдена, False - иначе.
    """
    for i in range(t):
        # ~ Шаг 1. Претендент
        r = randint(2, n - 1)
        x = (r**2) % n

        # ~ Шаг 2. Проверяющий центр
        e = [randint(0, 1) for i in range(k)]

        # ~ Шаг 3. Претендент
        y = r
        for i in range(k):
            y *= (s[i] ** e[i]) % n
        y %= n

        # ~ Шаг 4. Проверяющий центр
        y_2 = x
        for i in range(k):
            y_2 *= (v[i] ** e[i]) % n
        y_2 %= n

        if (y**2 % n) != y_2:
            return False
    return True


result = main_actions(s, v, n)
print(f"Результат проверки (рабочий этап): {result}")
