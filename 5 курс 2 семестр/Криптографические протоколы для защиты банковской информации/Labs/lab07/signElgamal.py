from sage.all import *

#! Задание 1
#! Реализация электронной подписи на базе шифра Эль-Гамаля


# ? Предварительный этап клиента
def preparing_client(
    p: int | None, g: int | None, x: int | None, size_p: int = 1024
) -> tuple[int, int, int, int]:
    """Генерация `p`, `g`, `x`, `y` в предварительном этапе для клиента

    Аргументы:
        size_p (int, optional): размер числа `p`. По умолчанию 1024.

    Возвращает:
        tuple[int, int, int, int]: числа `p`, `g`, `x`, `y`
    """
    # ~ Открытые данные
    if not p:
        p = random_prime(2**size_p)
    if not g:
        g = primitive_root(p)  # первообразный корень по модулю p
        # различные степени g являются различными числами по модулю p

    # ~ Секретный ключ
    if not x:
        x = randint(2, p - 1)

    # ~ Открытый ключ
    y = pow(g, x, p)

    return p, g, x, y


def create_sign(
    p: int, g: int, x: int, k: int | None, hash_func: callable, message: int
) -> tuple[int, int, int]:
    """Генерация подписи

    Аргументы:
        p (int): простое число
        x (int): секретный ключ
        hash_func (callable): хеш-функция
        message (int): сообщение

    Возвращает:
        tuple[int, int, int]: подпись (m, r, s)
    """

    h = hash_func(message)

    assert h < p

    if not k:
        k = randint(1, p - 1)
        while gcd(k, p - 1) != 1:
            k = randint(1, p - 1)

    r = pow(g, k, p)
    u = (h - x * r) % (p - 1)

    s = (inverse_mod(k, p - 1) * u) % (p - 1)

    return message, r, s


def verify_sign(
    p: int, g: int, y: int, sign: tuple[int, int, int], hash_func: callable
) -> bool:
    """Проверка подписи

    Аргументы:
        y (int): открытый ключ
        sign (tuple[int, int, int]): подпись (m, r, s)
        hash_func (callable): хеш-функция
        message (int): сообщение

    Возвращает:
        bool: результат проверки
    """
    message, r, s = sign
    h = hash_func(message)
    if pow(y, r, p) * pow(r, s, p) % p == pow(g, h, p):
        return True
    return False


if __name__ == "__main__":
    hash_func = lambda m: m
    p, g, x, y = preparing_client(20)

    message = 12345
    sign = create_sign(p, g, x, hash_func, message)
    print(f"Подпись: {sign}")

    result = verify_sign(y, sign, hash_func, message)
    print(f"Результат проверки подписи: {result}")
