from fpylll import *

N = 7427348605337420439226351301259396736338668628478026364247537354940635099417985194658970761928680925182008511152254688145103860128004202503366474283301612075177785324580367485485658736331441943472952155621639662643715068050809082488144556149444490361655502468281994103450718847571742070878683972591764582106285078065864827820587920185765360247986736413307433316395696422364074349807321647196675748416486392177198614794875770634343
e = 3
c1 = 31006276680299820175476315067101395202225288554778669509438887512651971587918750955037430926079670744122698892139964166907513659086428199
c2 = 31006276680299820175476315067101395282710387433868750322697813786430647302673358518858061044167142934256709846999692381475803695916434083  
m = 5

# Определяем кольцо полиномов R и два полинома
R.<mm, r> = PolynomialRing(ZZ, 2)
poly1 = mm ** 3 - c1
poly2 = (mm + r) ** 3 - c2

# Находим результатант многочленов
resultant_monomial = poly1.resultant(poly2, mm).mod(N)
# Определяем кольцо полиномов R
R.<r> = PolynomialRing(ZZ, 'r')
# Превращаем результатант в полином f
resultant_polynomial = R(resultant_monomial)

n = resultant_monomial.degree()
X = N.nth_root(n, 1)[0] // 2

# Вычисляем размерность матрицы A
dim = n * m

# Создаем список мономов
monomials = list(map(lambda i: r ** i, range(dim)))
# Создаем матрицу A для хранения коэффициентов многочленов
A = IntegerMatrix(dim, dim)
count = 0
# Заполняем матрицу A коэффициентами многочленов
for i in range(m):
    for j in range(n):
        g = N ** (m - i) * (X * r) ** j * resultant_polynomial(X * r) ** i
        for k in range(dim):
            A[count, k] = g.monomial_coefficient(monomials[k])
        count += 1

# Применяем алгоритм LLL к матрице A
LLL.reduction(A)
A = Matrix(ZZ, dim, dim, lambda i, j: A[i][j])

# Извлекаем первую строку матрицы A
polynomial_h = list(A[0])
# Вычисляем веса мономов
weights = list(map(lambda i: X ** i, range(dim)))

# Получаем корни полинома h
polynomial_h = sum(map(lambda i: ZZ(polynomial_h[i] / weights[i]) * monomials[i], range(dim)))
roots = [root for root, _ in polynomial_h.roots() if resultant_polynomial(root).mod(N) == 0]
print("r = ", roots)

# Определяем кольцо полиномов R
R.<mm, r> = PolynomialRing(ZZ, 2)
poly1 = poly1(mm, roots[0])
poly2 = poly2(mm, roots[0])

# Находим секретное сообщение
secret_message = -gcd(poly1, poly2).coefficient({mm: 0})

# Проверяем, что полученное сообщение удовлетворяют условиям
if pow(secret_message, e, N) == c1 and pow(secret_message + roots[0], e, N) == c2:
    print("message =", secret_message)
    print("message' =", secret_message + roots[0])
