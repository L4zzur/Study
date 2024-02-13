"""
# Задание 2
При построении системы аутентификации Шнорра были выбраны параметры системы $t=3$, $p=53$, $q=13$. Проверить, что можно завершить построение системы, выбрав при этом значение $g=16$. По данному открытому ключу $y$ вычислить закрытый ключ $x$ пользователя А. Провести расчеты для
$$y_1=36;$$
$$y_2=42;$$
$$y_3=13.$$
"""

from typing import Generator

from sage.all import *


def preparing_x(t: int, p: int, q: int, g: int, y: int) -> int:
    """Построение системы по известным параметрам `t`, `p`, `q`, `g` и открытом ключу `y`

    Аргументы:
        t (int): параметр безопасности
        p (int): простое число
        q (int): простое число, `q >= 2^t`
        g (int): первообразный корень по модулю p
        y (int): открытый ключ


    Возвращает:
        int: `x`
    """

    for _x in range(p):
        if (y * pow(g, _x, p) % p) == 1:
            x = _x
            break

    return x


def get_schnorr_scheme() -> Generator[int, None, None]:
    """Получение параметров построенных систем

    Yields:
        Generator[int, None, None]: `t`, `p`, `q`, `g`, `x`, `y`
    """
    t, p, q, g = 3, 53, 13, 16
    for y in input_data:
        x = preparing_x(t, p, q, g, y)
        yield t, p, q, g, x, y


data = [36, 42, 13]


if __name__ == "__main__":

    t, p, q = 3, 53, 13
    g = 16
    for i in range(len(data)):
        y = data[i]
        x = preparing_x(t, p, q, g, y)
        print(f"Закрытый ключ пользователя А{i + 1}: {x = }")
