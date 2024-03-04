import hashlib
from typing import Any
from sage.all import *

#! Схема затемненной подписи Шаума-Педерсена


def preparing_center(p_size: int = 512, q_size: int = 140):
    """Генерация `p`, `q` и `g` в предварительном этапе для центра

    Аргументы:
        p_size (int, optional): размер числа `p` в битах. По умолчанию 512.
        q_size (int, optional): размер числа `q` в битах. По умолчанию 140.

    Возвращает:
        tuple[int, int, int]: числа `p`, `q`, `g`
    """
    p, q = random_prime(2**p_size, lbound=10), random_prime(
        2**q_size, lbound=10
    )
    while (p - 1) % q != 0:
        p, q = random_prime(2**p_size, lbound=10), random_prime(
            2**q_size, lbound=10
        )

    g = randint(2, p - 1)
    while pow(g, q, p) != 1:
        g = randint(2, p - 1)

    return p, q, g


def preparing_signer(p: int, q: int, g: int):
    """Генерация `x` и `h`

    Аргументы:
        p (int): простое число `p`
        q (int): простое число `q`
        g (int): число `g`
    Возвращает:
        tuple[int, int]: числа `x`, `h`
    """
    x = randint(2, q - 1)
    h = pow(g, x, p)

    return x, h


H = hashlib.sha256()
p, q, g = preparing_center(6, 6)
x, h = preparing_signer(p, q, g)
m = 6


def main_actions(
    p: int, q: int, g: int, x: int, h: int, H: Any, m: int
) -> bool:
    """Рабочий этап схемы затемненной подписи Шаума-Педерсена

    Аргументы:
        p (int): простое число от центра
        q (int): простое число от центра
        g (int): число от центра
        x (int): секретный ключ схемы ЦП
        h (int): число от клиента
        H (Any): хэш-функция
        m (int): сообщение
    Возвращает:
        bool: результат проверки подписи
    """
    # ~ 1. Сокрытие подписи (подписывающий) [m,z] -> проверяющему
    z = int(pow(m, x, p))
    # ~ Проверяющий
    s, t, u, v = (randint(3, q - 1) for _ in range(4))
    t = 0
    m_ = pow(m, s, p) * pow(g, t, p)  # m'
    z_ = pow(z, s, p) * pow(h, t, p)  # z'

    # ~ 2. Выбор случайного варианта (подписывающий) [a, b] -> проверяющему
    w = randint(3, q - 1)
    a = int(pow(g, w, p))
    b = int(pow(m, w, p))
    # ~ Проверяющий
    a_ = int(pow(a, u, p)) * int(pow(g, v, p))  # a'
    b_ = int(pow(b, s * u, p) * pow(a, t * u, p) * pow(m_, v, p))  # b'

    # ~ 3. Запрос (проверяющий) с -> подписывающему
    _ = str(m_) + str(z_) + str(a_) + str(b_)
    H.update(_.encode())
    c_ = int(H.hexdigest()[4:], 16) % p  # c'
    c = int(c_ * pow(u, -1, q) % q)

    # ~ 4. Ответ (подписывающий) r -> проверяющему
    r = int(w) + int(c) * int(x)

    # ~ Проверка (проверяющий)
    r_ = (int(u) * int(r) + int(v)) % p

    if (
        pow(int(g), int(r), p) == (a * pow(int(h), int(c), p)) % p
        and pow(int(m), int(r), p) == (b * pow(int(z), int(c), p)) % p
    ):
        return True
    return False


result = main_actions(p, q, g, x, h, H, m)
print(f"Результат проверки (рабочий этап): {result}")
