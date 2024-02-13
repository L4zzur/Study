"""
# Задание 4
Построить систему электронных платежей банка Б для параметров $$Р=41, Q=67, Е=71, F(m)=7^m (\bmod 2747),$$ вычислив параметр $D$ системы.
Сформировать оплату покупки в 2 у.е., формируя две банкноты по 1 у.е., для первой банкноты задав $m=57$ и $r=80$, а для второй — $m=125$, а затемняющий множитель $r=408$.
"""

from sage.all import *

## Начальные данные
P, Q, E = 41, 67, 71
base, mod = 7, 2747

# Данные для банкнот (m, r)
data = [
    (57, 80),
    (125, 408),
]

## Построение системы
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


def create_note(m: int, r: int) -> tuple[int, int] | None:
    """Формирование банкноты

    Аргументы:
        m (int): номер банкноты
        r (int): затемняющий множитель

    Возвращает:
        tuple[int, int] | None: данные банкноты или `None`, если банкнота уже использована
    """
    if m in Z:
        return None
    # Покупатель
    x = f(m) * pow(r, E, N) % N
    # Банк
    y = pow(x, D, N)
    # Покупатель
    s = y * inverse_mod(r, N) % N

    # Добавляем номер банкноты в регистр
    Z.append(m)

    return m, s


def get_scheme() -> tuple[int, int, int, int, int]:
    """Получение параметров построенной системы

    Returns:
        tuple[int, int, int, int, int, int]: `P`, `Q`, `N`, `E`, `D`
    """
    Z.append(data[0][0])
    Z.append(data[1][0])
    return P, Q, N, E, D


if __name__ == "__main__":
    for m, r in data:
        note = create_note(m, r)
        print(f"Данные: {m = }, {r = }\nПолученная банкнота: {note}\n")
