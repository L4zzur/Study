import hashlib
from random import randint
from uuid import uuid4

from sage.all import *

#! Схема цифровой подписи Шнорра


def preparing_center(p_size: int = 512, q_size: int = 140):
    """Генерация `p`, `q` и `g` в предварительном этапе для центра

    Аргументы:
        p_size (int, optional): размер числа `p` в битах. По умолчанию 512.
        q_size (int, optional): размер числа `q` в битах. По умолчанию 140.

    Возвращает:
        tuple[int, int, int]: числа `p`, `q`, `g`
    """
    p, q = random_prime(2**p_size, lbound=1000), random_prime(
        2**q_size, lbound=1000
    )
    while (p - 1) % q != 0:
        p, q = random_prime(2**p_size, lbound=1000), random_prime(
            2**q_size, lbound=1000
        )

    g = randint(2, p - 1)
    while pow(g, q, p) != 1:
        g = randint(2, p - 1)

    return p, q, g


def preparing_signer(p: int, q: int, g: int) -> tuple[int, int]:
    """Генерация `x` и `h`

    Аргументы:
        p (int): простое число `p`
        q (int): простое число `q`
        g (int): число `g`
    Возвращает:
        tuple[int, int]: числа `x`, `h`
    """
    x = randint(1, q - 1)  # Секретный ключ схемы ЦП
    h = pow(g, x, p)

    return x, h


H = hashlib.sha256()
message = uuid4()
p, q, g = preparing_center(15, 15)
x, h = preparing_signer(p, q, g)


def main_actions(p, q, g, x, h, H, message):
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
    w = randint(2, q - 1)
    a = pow(g, w)
    H.update(f"{message}{a}".encode())
    m = int(H.hexdigest(), 16)
    c = m % q
    r = w + c * x

    if pow(g, r, p) % p == a * pow(h, c, p) % p:
        return True
    return False


result = main_actions(p, q, g, x, h, H, message)
print(f"Результат проверки (рабочий этап): {result}")
