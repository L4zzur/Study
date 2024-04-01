from sage.all import *
from signElgamal import create_sign, preparing_client, verify_sign

#! Задание 3
"""
$$p=31259, g=2$$
Остальные параметры выбираем самостоятельно.
Для тестирования программы рекомендуется использовать подписанное сообщение 
$$(500; 27665, 26022)$$
для открытого ключа пользователя
$$y=16196, h(m)=m$$
Данное сообщение должно признаваться подлинным.
"""

p = 31259
g = 2

sign = (500, 27665, 26022)

y = 16196
hash_func = lambda m: m

x = randint(2, p - 1)
while pow(g, x, p) != y:
    x = randint(2, p - 1)

h = hash_func(sign[0])

while True:
    k = randint(1, p - 1)
    while gcd(k, p - 1) != 1:
        k = randint(1, p - 1)

    r = pow(g, k, p)
    if r == sign[1]:
        break

print(f"{x=}, {k=}")

verify = verify_sign(p=p, g=g, y=y, sign=sign, hash_func=hash_func)
print(f"Подлинность подписи: {verify}")
