from hashlib import sha256

from sage.all import *

#! Протокол электронной коммерции (ПЭК, e-commerce protocol, ecp) распознающий жулика

# ? A - покупатель
# ? B - банк
# ? T - продавец

R = set()
k = 3
N = 100

# ~ A -> B
_m = randint(1, N)  # Перевод на определенную сумму
m = [_m for _ in range(k)]  # Все переводы на одинаковую сумму
alpha = [randint(1, N) for _ in range(k)]  # Маскирующие множители
r = [randint(1, N) for _ in range(k)]

beta_1 = [randint(1, N) for _ in range(k)]  # 1-я доля секрета
beta_2 = [randint(1, N) for _ in range(k)]  # 2-я доля секрета

hash_func_int = lambda x: int(sha256(str(x).encode()).hexdigest(), 16)
hashed_beta_1 = [hash_func_int(beta_1[i]) for i in range(k)]
hashed_beta_2 = [hash_func_int(beta_2[i]) for i in range(k)]

lists = list(zip(m, r, hashed_beta_1, hashed_beta_2))
masked_lists = [[alpha[i] * element for element in lists[i]] for i in range(k)]

print(
    f"Перевод: m_i = {_m}\n"
    f"Маскирующие множители: alpha = {alpha}\n"
    f"r = {r}\n"
    f"Доли секрета:\nbeta_1 = {beta_1}\nbeta_2 = {beta_2}\n"
    f"Хешированные доли секрета:\nhashed_beta_1 = {hashed_beta_1}\nhashed_beta_2 = {hashed_beta_2}\n"
    f"Маскированные переводы:\nmasked_lists = {masked_lists}\n"
)

# ~ B -> A
num = randint(0, k - 1)
alpha_B = masked_lists[num]
print(f"Номер перевода: {num}\nМаскированный перевод: {alpha_B}\n")

# ~ A -> T - раскрытие num-го перевода
unmasked_list = [
    masked_lists[num][j] // alpha[num] for j in range(len(masked_lists[num]))
]
print(f"Раскрытый перевод: {unmasked_list}\n")

# ~ T -> A
e = [randint(1, 2) for _ in range(k)]
print(f"e = {e}\n")

# ~ A -> T
alpha_e = [beta_1[i] if e[i] == 1 else beta_2[i] for i in range(k)]
hashed_alpha_e = [hash_func_int(alpha_e[i]) for i in range(k)]
print(f"Хешированный alpha_e = {hashed_alpha_e}\n")

for i in range(k):
    if hashed_alpha_e[i] in (unmasked_list[2], unmasked_list[3]):
        print("Платеж принят\n")
        break
else:
    print("Платеж отклонен\n")
    exit()

# ~ T -> B - депонирование
deposit = [unmasked_list, alpha_e]
print(f"Депонирование: {deposit = }\n")

# ~ B проверять r in R?
r = deposit[0][1]
if r not in R:
    R.add(r)
    print("Принято. ЭБ является законной.")
else:
    print("Отказ. ЭБ является копией.")

print(f"{R = }")
