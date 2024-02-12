# Лабораторная № 0 к курсу "Криптография на решетках 2023"
>Опубликовано: 23.01.23

**Приём лабораторной:** эта лабораторная не будет проверяться

## Инструкция
1. Установить библиотеку FPyLLL Про FPyLLL можно прочитать здесь
2. Убедитесь в корректной установке библиотеки, запустив сниппет

```python
# https://buildmedia.readthedocs.org/media/pdf/fpylll/latest/fpylll.pdf
from fpylll import *
FPLLL.set_random_seed(2023)
A = IntegerMatrix(20,20)
A.randomize("qary", k=10, q=256)
print(A)
B = IntegerMatrix(25,25)
B.randomize("uniform", bits=13)
print(B)

AGSO = GSO.Mat(A)
print(AGSO.get_mu(1,0))
_ = AGSO.update_gso()
print(AGSO.get_mu(1,0))
print(AGSO.get_mu(2,0))
```