from prettytable import PrettyTable
from sage.all import *
from signElgamal import create_sign, preparing_client, verify_sign

#! Задание 2
"""
Абоненты некоторой сети применяют подпись Эль-Гамаля с общими параметрами $p=23$ и $g=5$. Для указанных секретных параметров абонентов найти открытый ключ ($y$) и построить подпись для сообщения $m$:
1. $x=11, k=3, m=h=15$
2. $x=10, k=15, m=h=5$
3. $x=3, k=13, m=h=8$
4. $x=18, k=7, m=h=5$
5. $x=9, k=19, m=h=15$
"""

p = 23
g = 5

data = [
    {"x": 11, "k": 3, "m": 15},
    {"x": 10, "k": 15, "m": 5},
    {"x": 3, "k": 13, "m": 8},
    {"x": 18, "k": 7, "m": 5},
    {"x": 9, "k": 19, "m": 15},
]

hash_func = lambda m: m

table = PrettyTable(
    ["p", "g", "Secret x", "k", "Message", " | ", "Public y", "sign", "verify"]
)
table.align = "l"
for d in data:
    x = d["x"]
    k = d["k"]
    m = d["m"]
    p, g, x, y = preparing_client(p=p, g=g, x=x)
    sign = create_sign(p=p, g=g, x=x, k=k, hash_func=hash_func, message=m)
    verify = verify_sign(p=p, g=g, y=y, sign=sign, hash_func=hash_func)
    table.add_row([p, g, x, k, m, " | ", y, sign, verify])
print(table)
