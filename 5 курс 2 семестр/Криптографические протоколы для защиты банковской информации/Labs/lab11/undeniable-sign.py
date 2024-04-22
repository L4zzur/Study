from hashlib import sha256

from sage.all import *

#! Стираемая подпись. Стираемая цифровая подпись, подтверждаемая двумя уполномоченными агентами


p_size = 20
hash_func_int = lambda x, n: int(sha256(str(x).encode()).hexdigest(), 16) % n


# ? Параметры
g = None
while g is None:
    p = random_prime(2**p_size, lbound=1000)
    F = GF(p)
    elements = F.some_elements()
    for element in elements:
        if element.multiplicative_order() == p - 1:
            g = element
            break


p1 = random_prime(2 ** (p_size - 1), lbound=1000)
p2 = random_prime(2 ** (p_size - 1), lbound=1000)
a_private = (p1, p2)  # Закрытый ключ a_minus
x = randint(1, p - 1)
eta = pow(g, x, p)
n = p1 * p2
m = randint(1, p - 1)  # сообщение

y = randint(1, p - 1)
x1 = pow(g, y, p)
x2 = pow(eta, y, p)
hash_m = hash_func_int(m, n)
hash_x = hash_func_int(f"{x1}{x2}", n)
x3 = pow((hash_m + hash_x), (1 / 3))

print(
    f"{p = }, {g = }, {a_private = }\n{x = }, {eta = }, {n = }\n"
    f"сообщение {m = }, {y = }\n{hash_m = }\n{hash_x = }\n{x1 = }, {x2 = } {x3 = }\n"
)


# ? Доказательство подлинности <m>^s_a агентом А
print("Доказательство подлинности <m>^s_a агентом А")
# ~ 1. B -> A
u, v = randint(1, p - 1), randint(1, p - 1)
z = pow(g, u, p) * pow(eta, v, p)
print(f"B -> A: {z = }")

# ~ 2. A -> B
w = randint(1, p - 1)
d = pow(g, w, p)
e = pow(z * d, y, p)
print(f"A -> B: ({d = }, {e = })")

# ~ 3. B -> A
print(f"B -> A: ({u = }, {v = })")

# ~ 4. A -> B
check = z == pow(g, u, p) * pow(eta, v, p)
print(f"Проверка z = g^u * eta^v: {check}")
if not check:
    exit()
print(f"A -> B: {w = }")

# ~ 5. B
check1 = pow(g, w, p) == d
check2 = e == pow(x1, u + w, p) * pow(x2, v, p)
check3 = (hash_m + hash_x) == round(x3**3, 0)
print(f"Проверка d = g^w: {check1}")
print(f"Проверка e = x1^(u + w) * x2^v: {check2}")
print(f"Проверка hash_m + hash_x = x3^3: {check3}\n")


# ? Доказательство подлинности <m>^s_a агентом C
print("Доказательство подлинности <m>^s_a агентом C")
# ~ 1. B -> C
u, v = randint(1, p - 1), randint(1, p - 1)
z = pow(g, u, p) * pow(x1, v, p)
print(f"B -> C: {z = }")

# ~ 2. C -> B
w = randint(1, p - 1)
d = pow(g, w, p)
e = pow(z * d, x, p)
print(f"A -> B: ({d = }, {e = })")

# ~ 3. B -> C
print(f"B -> C: ({u = }, {v = })")

# ~ 4. C -> B
check = z == pow(g, u, p) * pow(x1, v, p)
print(f"Проверка z = g^u * eta^v: {check}")
if not check:
    exit()
print(f"A -> B: {w = }")

# ~ 5. B
check1 = pow(g, w, p) == d
check2 = e == pow(eta, u + w, p) * pow(x2, v, p)
check3 = (hash_m + hash_x) == round(x3**3, 0)
print(f"Проверка d = g^w: {check1}")
print(f"Проверка e = x1^(u + w) * x2^v: {check2}")
print(f"Проверка hash_m + hash_x = x3^3: {check3}")
