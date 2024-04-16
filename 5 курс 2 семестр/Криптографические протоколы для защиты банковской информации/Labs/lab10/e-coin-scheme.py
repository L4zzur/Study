from hashlib import sha256

from sage.all import *

#! Электронная монета. Схема Якоби

"""
Четыре участника в системе:
1. Центр сертификации (ЦС)
2. Банк (Б)
3. Покупатель (Пк)
4. Продавец (Пр)

Шесть транзакций:
1. Выдача начального сертификата
2. Обновление сертификата
3. Снятие со счета
4. Платеж
5. Депозит
6. Обмен монет

Банк и ЦС используют схему электронной подписи RSA, а клиенты - схему Эль Гамаля.
"""

N_size = 30
hash_func_int = lambda x: int(sha256(str(x).encode()).hexdigest(), 16)

#! Подготовительный этап
# ? Банк
N_b = random_prime(2**N_size, lbound=2 ** (N_size - 1))  # Модуль
e_b = randint(1, N_b)  # Открытая экспонента
d_b = inverse_mod(e_b, N_b)  # Закрытая экспонента
print(f"Подготовительный этап\nБанк: {N_b = }, {e_b = }, {d_b = }")

# ? ЦС
N_c = random_prime(2**N_size, lbound=2 ** (N_size - 1))  # Модуль
e_c = randint(1, N_c)  # Открытая экспонента
d_c = inverse_mod(e_c, N_c)  # Закрытая экспонента
print(f"ЦС: {N_c = }, {e_c = }, {d_c = }")

gamma = randint(30, 50)
p = random_prime(2**N_size, lbound=2 ** (N_size - 1))
alpha = GF(p).multiplicative_generator()  # Элемент порядка р-1
print(f"{gamma = }, {p = }, {alpha = }")

k = 15
S = [int(f"{i + 1}{randint(1, p)}") for i in range(k)]  # Секретные ключи
P = [pow(alpha, int(s), p) for s in S]  # Открытые ключи
print(f"{S = }, {P = }\n")

# ~ 1. Выдача начального сертификата
i = randint(0, k - 1)  # Случайный клиент
x = randint(1, N_c - 1)
null_gamma = "".zfill(gamma)
f = hash_func_int(f"{P[i]}{null_gamma}")
z = (pow(x, e_c, N_c) * f) % N_c

print(f"1. Выдача начального сертификата")
print(f"Клиент №{i}\n{x = }, {null_gamma = }\n{f = }, {z = }")

if any(str(i + 1) == str(s)[0 : len(str(i + 1))] for s in S):
    print("ЦС принимает доказательство")
else:
    print("ЦС не принимает доказательство")
    exit()

z_ = pow(z, d_c, N_c)
cert = pow(f, d_c, N_c)
print(f"Подписанный {z_ = }, сертификат {cert = }\n")

# ~ 2. Обновление сертификата
print("2. Обновление сертификата")
S_i = f"{i + 1}{randint(1, p)}"
P_i_ = pow(alpha, int(S_i), p)

if str(i + 1) == str(S_i)[0 : len(str(i + 1))]:
    print("Вторая проверка с нулевым разглашением принята")
else:
    print("Вторая проверка с нулевым разглашением не принята")
    exit()

f = hash_func_int(f"{P_i_}{null_gamma}")
c_2_ec = (pow(x, e_c, N_c) * f) % N_c
c_2 = pow(c_2_ec, d_c, N_c)
new_cert = (c_2 * inverse_mod(x, N_c)) % N_c
print(f"{f = }\n{c_2_ec = }, {c_2 = }\nНовый сертификат{new_cert = }\n")


# ~ 3. Снятие со счета
print("3. Снятие со счета")
r = randint(1, p)
u = pow(alpha, r, p)
f = hash_func_int(f"{P[i]}{u}{null_gamma}")
w = (pow(x, e_b, N_b) * f) % N_b
print(f"{r = }, {u = }\n{f = }\n{w = }")

if any(str(i + 1) == str(s)[0 : len(str(i + 1))] for s in S):
    print("Третья проверка с нулевым разглашением принята")
else:
    print("Третья проверка с нулевым разглашением не принята")
    exit()

c = pow(f, d_b, N_b)
ecoin = (P[i], u, c)
print(f"Электронная монета (P_i, u, c) = {ecoin}\n")


# ~ 4. Платеж
print("4. Платеж")
m = randint(1, p - 1)
v = (inverse_mod(r, p) * (m - S[i] * u)) % p - 1
print(f"Случайное значение {m = }, подпись {v = }")

# ~ 5. Депозит
registry = set()
print("5. Депозит")
print(
    f"Продавец передает банку: электронную монету = ({ecoin}), запрос {m}, подпись s = ({u}, {v})\n"
)
if ecoin in registry:
    print("Монета была потрачена ранее.")
else:
    print("Монета была успешно потрачена.")
    registry.add(ecoin)


# ~ 6. Снятие со счета
print("6. Снятие со счета")
print(f"Сертификат {cert}, {u = }")
