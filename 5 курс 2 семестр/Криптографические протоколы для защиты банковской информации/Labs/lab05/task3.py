"""
# Задание 3
Провести аутентификацию по протоколу Шнорра в случае систем, построенных в задачах 1 и 2, производя выбор параметра $k$ за А, параметра $e$ за Б, вычисляя $s$ за А и проверяя равенство $$r=g^sy^e (\bmod p)$$
"""

from itertools import chain
from random import randint

from sage.all import *
from task1 import get_schnorr_scheme as get_schnorr_scheme_1
from task2 import get_schnorr_scheme as get_schnorr_scheme_2


def auth_scheme_1():
    schemes = chain(get_schnorr_scheme_1(), get_schnorr_scheme_2())
    for t, p, q, g, x, y in schemes:
        print(f"Система с параметрами {t = } {p = } {q = } {g = }")
        print(f"Открытый ключ пользователя А: {x = }")
        print(f"Открытый ключ пользователя А: {y = }")
        # Пользователь А
        k = randint(0, q - 1)
        r = pow(g, k, p)  # Отправляет в банк Б
        # Банк Б
        e = randint(0, 2**t - 1)  # Отправляет пользователю А
        # Пользователь А
        s = (k + x * e) % q  # Отправляет в банк Б
        # Банк Б
        if r == pow(g, s, p) * pow(y, e, p) % p:
            print("Аутентификация прошла успешно\n")
        else:
            print("Аутентификация провалена\n")


auth_scheme_1()
