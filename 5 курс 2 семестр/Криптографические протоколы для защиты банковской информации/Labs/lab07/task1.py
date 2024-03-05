from signElgamal import verify_sign
from sage.all import *

#! Задание 1
"""
Для указанных открытых ключей ($y$) пользователей системы Эль-Гамаля с общими параметрами $p=23$ и $g=5$ проверить подлинность подписанных сообщений:
1. $y=22$: $(15; 20, 3), (15; 10, 5), (15; 19, 3)$
2. $y=9$: $(5; 19, 17), (7; 17, 8), (6; 17, 8)$
3. $y=10$: $(3; 17, 12), (2; 17, 12), (8; 21, 11)$
4. $y=6$: $(5; 17, 1), (5; 11, 3), (5; 17, 10)$
5. $y=11$: $(15; 7, 1), (10; 15, 3), (15; 7, 16)$
"""

p = 23
g = 5

data = [
    {"y": 22, "signs": [(15, 20, 3), (15, 10, 5), (15, 19, 3)]},
    {"y": 9, "signs": [(5, 19, 17), (7, 17, 8), (6, 17, 8)]},
    {"y": 10, "signs": [(3, 17, 12), (2, 17, 12), (8, 21, 11)]},
    {"y": 6, "signs": [(5, 17, 1), (5, 11, 3), (5, 17, 10)]},
    {"y": 11, "signs": [(15, 7, 1), (10, 15, 3), (15, 7, 16)]},
]

hash_func = lambda m: m

for d in data:
    y = d["y"]
    signs = d["signs"]
    print(f"\nОткрытый ключ: {y}\nПодписи: {signs}")
    for sign in signs:
        print(
            f"Подпись: {sign}. Проверка: {verify_sign(p, g, y, sign, hash_func)}"
        )
