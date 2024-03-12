from sage.all import *

#! Реализация протокола обмена подписью между банком и клиентом


def generate_primes(size: int) -> tuple[int, int]:
    """Генерация двух простых чисел от 10^`(size-1)` до 10^`size`

    Аргументы:
        size (int): размер простого числа (от 10^`(size-1)` до 10^`size`)

    Возвращает:
        tuple[int, int]: разные простые числа
    """
    P = random_prime(lbound=10 ** (size - 1), n=10**size)
    Q = next_prime(P)
    return P, Q


def generate_ed(phi_n: int) -> tuple[int, int]:
    """Генерация параметров `e` и `d` для `phi_n`

    Аргументы:
        phi_n (int): функция Эйлера от `n`

    Возвращает:
        tuple[int, int]: параметры `e` и `d`
    """
    e = randint(2, phi_n)
    while gcd(e, phi_n) != 1:
        e = randint(2, phi_n)

    d = pow(e, -1, phi_n)

    return e, d


# Банк
P, Q = generate_primes(5)
N = P * Q
phi_N = (P - 1) * (Q - 1)

E, D = generate_ed(phi_N)

print(f"Параметры банка:\n{P = }, {Q = }, {N = }, {phi_N = }, {E = }, {D = }")

# Клиент А
p, q = generate_primes(3)
n = p * q
phi_n = (p - 1) * (q - 1)
e, d = generate_ed(phi_n)

print(
    f"Параметры клиента:\n{p = }, {q = }, {n = }, {phi_n = }, {e = }, {d = }\n"
)

# Сообщение, пересылка
m = randint(100, 1000)
x = pow(m, d, n)
s = pow(x, E, N)

message = (m, s)
print(f"Сообщение (m, s):\n{message = }\n")

# Проверка банком
y = pow(s, D, N)
z = pow(y, e, n)
print(f"Проверка:\n{z = }\nz == m: {z == m}")
