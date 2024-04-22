from sage.all import *

#! Стираемая подпись. Протокол ГОСТ стираемой ЭП

p_size = 20

# ? Параметры
p = random_prime(2**p_size, lbound=1000)
factor_p = factor(p - 1)
q = factor_p[len(factor_p) - 1][0]
g = randint(2, p)
while pow(g, q, p) != 1:
    g = randint(2, p)
print(f"{p = }, {q = }, {g = }")

m = randint(1, q)  # сообщение
x1, x2 = randint(1, q), randint(1, q)
a_private = (x1, x2)  # Закрытый ключ a_minus
g1, g2 = pow(g, x1, p), pow(g, x2, p)
a_public = (g1, g2)  # Открытый ключ a_plus
u = randint(1, q)
s1 = pow(g, u, p)
s2 = (x1 * s1 + m * x2 * u) % q
m_s_a = (s1, s2)
print(f"{m = }, {a_private = }, {a_public = }, {m_s_a = }\n")

# ? 1. Протокол подтверждения подлинности <m>^s_a
# ? Доказательство утверждения (z1, z2) = <m>^s_a
print("1. Протокол подтверждения подлинности <m>^s_a")
# ~ 1. B -> A
u, v = randint(1, q), randint(1, q)
z1, z2 = randint(1, q), randint(1, q)
y = pow(z1, u, p) * pow(g, v, p) % p
print(f"B -> A: {y = }")

# ~ 2. A -> B
w = randint(1, q)
h1 = y * pow(g, w, p) % p
h2 = pow(h1, x2, p)
print(f"A -> B: ({h1 = }, {h2 = })")

# ~ 3. B -> A
print(f"B -> A: ({u = }, {v = })")

# ~ 4. A
check = y == pow(z1, u, p) * pow(g, v, p) % p
print(f"Проверка y = z1^u * g^v: {check}")
if not check:
    exit()
print(f"A -> B: {w = }")

# ~ 5. B
#! Неправильный вариант, для опровержения
gamma = randint(1, p)
# ! Правильный вариант
gamma = int(pow(z1, x2, p))

check1 = h1 == pow(z1, u, p) * pow(g, v + w, p) % p
check2 = h2 == pow(gamma, u, p) * pow(g2, v + w, p) % p

print(f"Проверка h1 = z1^u * g^(v + w): {check1}")
print(f"Проверка h2 = gamma^u * g^(v + w): {check2}")
if not (check1 and check2):
    print(f"Проверки не пройдены. (z1, z2) != <m>^s_a\n")

    # ? 2. Протокол опровержения подлинности <m>^s_a
    # ? Доказательство утверждения (z1, z2) != <m>^s_a
    print("2. Протокол опровержения подлинности <m>^s_a")
    # ~ 1. B -> A
    i = randint(0, 1)
    v = randint(1, q)
    if i == 0:
        y1 = pow(g, v, p)
        y2 = pow(g2, v, p)
    else:
        y1 = pow(z1, v, p)
        y2 = pow(gamma, v, p)
    w = randint(2, q)
    r = randint(1, p)
    print(f"B -> A: {i = }, {v = }, {y1 = }, {y2 = }, {w = }, {r = }")

    # ~ 2. A -> B
    check = pow(y1, x2, p) == y2
    j = 0 if check else 1
    print(f"A -> B: {j = }")

    # ~ 3. B -> A
    print(f"B -> A: {v = }")

    # ~ 4. A
    check = (y1 == pow(g, v, p) and y2 == pow(g2, v, p)) or (
        y1 == pow(z1, v, p) and y2 == pow(gamma, v, p)
    )
    if not check:
        exit()

    # ~ 5. A -> B
    print(f"A -> B: {r = }")

    # ~ 6. B
    check = i == j
    print(f"Проверка: {check}")
