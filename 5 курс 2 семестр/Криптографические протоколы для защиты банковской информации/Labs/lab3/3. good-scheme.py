import hashlib
from sage.all import *

#! Третья "хорошая" схема


def preparing_bank(size_n: int = 600) -> tuple[int, int, int, int]:
    """Генерация `P`, `Q`, `N`, `c` и `d` в предварительном этапе для банка.

    Аргументы:
        size_n (int, optional): размер простого числа `N`. По умолчанию 512.

    Возвращает:
        tuple[int, int, int, int]: числа `P`, `Q`, `N`, `c` и `d`
    """
    p = random_prime(2 ** (size_n // 2))
    q = next_prime(p)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    c = random_prime(phi_n)  # Открытая экспонента
    d = pow(c, -1, phi_n)  # Секретная экспонента

    return p, q, n, c, d


# ? Предварительный этап банка
P, Q, N, c, d = preparing_bank()

print(f"Предварительный этап банка:\n{P = }\n{Q = }\n{N = }\n{c = }\n{d = }\n")


# ? Работа с банкнотой: получение (генерация) и оплата в магазине (проверка)
def main_actions(N: int, c: int, d: int) -> bool:
    """Основной этап работы с электронными деньгами

    Аргументы:
        N (int): простое число `P*Q`
        c (int): открытая экспонента
        d (int): секретная экспонента

    Возвращает:
        bool: результат проверки
    """
    # ? Генерация покупателем номера банкноты
    n = randint(2, N - 1)  # Номер банкноты не отправляется в банк
    print(f"Номер банкноты: {n = }")
    f = hashlib.sha3_512()
    f.update(str(n).encode())
    n_hashed = int(f.digest().hex(), 16)
    print(f"Номер банкноты в банк: {n_hashed = }")

    # ? Банк формирует банкноту
    s_f = pow(n_hashed, c, N)  # Отправляется обратно, снимается у.е. со счета

    # ? Покупатель предъявляет банкноту, магазин проверяет
    if pow(s_f, d, N) == n_hashed:
        return True
    return False


result = main_actions(N, c, d)
print(f"Результат проверки (рабочий этап): {result}")
