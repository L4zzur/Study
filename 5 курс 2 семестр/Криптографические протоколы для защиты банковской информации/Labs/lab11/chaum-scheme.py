from sage.all import *

#! Стираемая подпись. Схема Шаума


p_size = 20

# ? Параметры
p = random_prime(2**p_size, lbound=1000)
g = GF(p).multiplicative_generator()
print(f"{p = }, {g = }")

# ? Предположения
m = randint(1, p - 1)  # сообщение
a_private = randint(1, p - 1)  # Закрытый ключ a_minus
a_public = pow(g, a_private, p)  # Открытый ключ a_plus
print(f"{m = }, {a_private = }, {a_public = }\n")
m_s_a = pow(m, a_private, p)

#! Неправильный вариант, для опровержения
z = randint(1, p - 1)
# ! Правильный вариант
z = pow(m, a_private, p)

# ? 1. Протокол подтверждения подлинности <m>^s_a
# ? Доказательство утверждения z = m^x (mod p)
print("1. Протокол подтверждения подлинности <m>^s_a")
# ~ 1. B -> A
u, v = randint(1, p - 1), randint(1, p - 1)
y = pow(m, u, p) * pow(g, v, p) % p
print(f"B -> A: {y = }")

# ~ 2. A -> B
w = randint(1, p - 1)
h1 = y * pow(g, w, p) % p
h2 = pow(h1, a_private, p)
print(f"A -> B: ({h1 = }, {h2 = })")

# ~ 3. B -> A
print(f"B -> A: ({u = }, {v = })")

# ~ 4. A
check = y == pow(m, u, p) * pow(g, v, p) % p
print(f"Проверка y = m^u * g^v: {check}")
if not check:
    exit()
print(f"A -> B: {w = }")

# ~ 5. B
check_1 = h1 == y * pow(g, w, p) % p
check_2 = h2 == pow(z, u, p) * pow(a_public, v + w, p)
print(f"Проверка h1 = y * g^w: {check_1}")
print(f"Проверка h2 = z^u * a_plus^(v + w): {check_2}")

if not (check_1 and check_2):
    print(f"Проверки не пройдены. z != m^x\n")

    # ? 2. Протокол опровержения подлинности <m>^s_a
    # ? Доказательство утверждения z != m^x (mod p)
    print(f"2. Протокол опровержения подлинности <m>^s_a")
    k = randint(2, 50)
    print(f"{k = }")

    # ~ 1. B -> A
    u, v = randint(1, k), randint(1, p - 1)
    y1 = pow(m, u, p) * pow(g, v, p) % p
    y2 = pow(z, u, p) * pow(a_public, v, p) % p
    print(f"B -> A: {u = }, {v = }, {y1 = }, {y2 = }")

    # ~ 2. A -> B
    r = randint(1, p - 1)
    left = pow(y1, a_private, p) / y2 % p
    right = m_s_a / z % p
    for w in range(0, k):
        if left == pow(right, w, p):
            break
    print(f"A -> B: {w = }, сообщение = {pow(w, r, p)}")

    # ~ 3. B -> A
    print(f"B -> A: {v = }")

    # ~ 4. A
    check1 = y1 == pow(m, w, p) * pow(g, v, p) % p
    check2 = y2 == pow(z, w, p) * pow(a_public, v, p) % p

    print(f"Проверка y1 = m^w * g^v: {check1}")
    print(f"Проверка y2 = z^w * a_plus^v: {check2}")

    # ~ 5. A -> B
    print(f"A -> B: {r = }")

    # ~ 6. B
    check = w == u
    print(f"Проверка w = u: {check}")
