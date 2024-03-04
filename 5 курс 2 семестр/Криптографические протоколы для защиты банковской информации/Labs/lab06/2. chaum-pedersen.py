from sage.all import *

#! Схема цифровой подписи Шаума-Педерсена с сокрытием подписанного сообщения


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


def preparing_signer(p: int, q: int, g: int):
    """Генерация `x` и `h`

    Аргументы:
        p (int): простое число `p`
        q (int): простое число `q`
        g (int): число `g`
    Возвращает:
        tuple[int, int]: числа `x`, `h`
    """
    x = randint(1, q - 1)
    h = pow(g, x, p)

    return x, h


p, q, g = preparing_center(15, 15)
x, h = preparing_signer(p, q, g)
m = randint(100, p - 1)


def main_actions(p: int, q: int, g: int, x: int, h: int, m: int) -> bool:
    """Рабочий этап подписи Шаума-Педерсена с сокрытием подписанного сообщения

    Аргументы:
        p (int): простое число от центра
        q (int): простое число от центра
        g (int): число от центра
        x (int): секретный ключ схемы ЦП
        h (int): число от клиента
        m (int): сообщение
    Возвращает:
        bool: результат проверки подписи
    """
    # ~ 1. Сокрытие подписи (подписывающий) [m,z] -> проверяющему
    z = pow(m, x)

    # ~ 2. Выбор случайного варианта (подписывающий) [a, b] -> проверяющему
    w = randint(2, q - 1)
    a = pow(g, w)
    b = pow(m, w)

    # ~ 3. Запрос (проверяющий) с -> подписывающему
    c = randint(2, q - 1)

    # ~ 4. Ответ (подписывающий) r -> проверяющему
    r = w + c * x

    # ~ Проверка (проверяющий)
    if (pow(g, r, p) == a * pow(h, c, p) % p) and (
        pow(m, r, p) == b * pow(z, c, p) % p
    ):
        return True
    return False


result = main_actions(p, q, g, x, h, m)
print(f"Результат проверки (рабочий этап): {result}")
