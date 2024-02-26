from typing import Any
from sage.all import *
import hashlib
from uuid import uuid4

#! Задание параметров и подготовка к совместной ЦП Брикелла-Ли-Якоби


def preparing(
    k: int, p_size: int = 2**20, l_size: int = 1000
) -> tuple[int, Any, int, int, str, list[int], list[int]]:
    """Генерация `p`, `Z`, `g`, `l`, `S` и `V` в предварительном этапе для посредника I.

    Аргументы:
        k (int): количество агентов
        p_size (int, optional): размер простого числа `p`. По умолчанию 2**20.
        l_size (int, optional): размер большого числа `l`. По умолчанию 1000.

    Возвращает:
        tuple[Any, int, int, int, str, list[int], list[int]]: `Z`, числа `p`, `g`, `l` и списки `S` и `V`
    """
    p = random_prime(p_size**2, lbound=p_size)  # Простое число

    Z = Integers(p)  # Z^*_p
    g = Z.multiplicative_generator()  # Элемент порядка р-1

    l = randrange(l_size, 2 * l_size)  # Большое число из N

    S = [[randint(3, 10) for j in range(l)] for i in range(k)]
    V = [[int(pow(g, -S[i][j], p)) for j in range(l)] for i in range(k)]

    return Z, p, g, l, S, V


hash_func = hashlib.sha256()  # Хеш-функция
k = 7  # количество агентов
message = uuid4()  # Случайное сообщение

Z, p, g, l, S, V = preparing(k=k)


def main_actions(
    Z: Any,
    k: int,
    p: int,
    g: int,
    l: int,
    S: list[int],
    V: list[int],
    hash_func: Any,
    message: str,
) -> tuple[bool, int, int]:
    """Основной этап работы с совместной ЦП

    Аргументы:
        Z (Any): Integers
        k (int): количество агентов
        p (int): простое число
        g (int): элемент порядка р-1
        l (int): большое число
        S (list[int]): список `S`
        V (list[int]): список `V`
        hash_func (hashlib._Hash): хеш-функция
        message (str): сообщение

    Возвращает:
        tuple[bool, int, int]: результат проверки, `check`, `y`
    """
    # ~ A_i -> I (Агенты -> Посредник)
    X = [Z.random_element() for _ in range(k)]
    Y = [int(pow(g, X[i], p)) for i in range(k)]

    # ~ I -> A_i (Посредник -> Агенты)
    y = int(Z(prod(Y)))

    # ~ A_i -> I (Агенты -> Посредник)
    m = "".join([str(message), str(y), *map(str, range(k))])

    hash_func.update(m.encode())
    h = int(hash_func.hexdigest(), 16)
    b = list(map(int, bin(pow(g, h, p))[2:].zfill(l)))

    Z_ = [
        int((X[i] + sum([S[i][j] for j in range(l) if b[j] == 1])))
        for i in range(k)
    ]

    # ~ I -> A_i (Посредник -> Агенты)
    z = int((sum(Z_)))

    check = pow(g, z, p) * prod(
        [prod([V[i][j] for j in range(l) if b[j] == 1]) for i in range(k)]
    )

    # * Проверка
    if check == y:
        return True, check, y
    return False, check, y


result, c, y = main_actions(
    Z=Z, k=k, p=p, g=g, l=l, S=S, V=V, hash_func=hash_func, message=message
)
print(f"Результат проверки (рабочий этап): {result}\n{c = }\n{y = }")
