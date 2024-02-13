"""
# Задание 6
Построить систему электронных платежей банка Б для параметров $$Р=23, Q=37, Е=53, F(m)=5^m (\bmod 851),$$ вычислив параметр $D$ системы.
Сформировать оплату покупки в 2 у.е., формируя две банкноты по 1 у.е., для первой банкноты задав $m=73$, а для второй — $m=351$, а затемняющий множитель $r$ выбрать самим.
"""

from random import randint

from sage.all import *

## Начальные данные
P, Q, E = 23, 37, 53
base, mod = 5, 851
# Номера банкнот
data = [
    73,
    351,
]

# Построение системы
N = P * Q
phi_N = (P - 1) * (Q - 1)
D = pow(E, -1, phi_N)

# Региcтр номеров использованных банкнот
Z = []


def f(m: int, base: int = base, mod: int = mod) -> int:
    """Односторонняя функция, которая не сохраняет произведения

    Аргументы:
        m (int): номер банкноты
        base (int, optional): основание. По умолчанию `base`.
        mod (int, optional): модуль. По умолчанию `mod`.

    Возвращает:
        int: результат функции f(`m`) = `_base`^`m` (mod `_mod`)
    """
    return pow(base, m, mod)


def create_note(m: int) -> tuple[int, int] | None:
    """Формирование банкноты

    Аргументы:
        m (int): номер банкноты

    Возвращает:
        tuple[int, int] | None: данные банкноты или `None`, если банкнота уже использована
    """
    if m in Z:
        return None
    # Покупатель
    r = Zmod(N).random_element()
    try:
        pow(r, -1, N)
    except:
        r = Zmod(N).random_element()
    x = f(m) * pow(r, E, N) % N
    # Банк
    y = pow(x, D, N)
    # Покупатель
    s = y * pow(r, -1, N) % N

    # Добавляем номер банкноты в регистр
    Z.append(m)

    return m, s


def get_scheme() -> tuple[int, int, int, int, int]:
    """Получение параметров построенной системы

    Returns:
        tuple[int, int, int, int, int, int]: `P`, `Q`, `N`, `E`, `D`
    """
    Z.append(data[0])
    Z.append(data[1])
    return P, Q, N, E, D


if __name__ == "__main__":
    for m in data:
        note = create_note(m)
        print(f"Данные: {m = }\nПолученная банкнота: {note}\n")
