# Verifica los números que cita Resumenes/01-tp6.md (los resultados de las corridas salen del notebook TP6-v3.ipynb)
import math

def f1(x):
    return -x * math.sin(math.sqrt(abs(x)))

def f2(x, y):
    r2 = x**2 + y**2
    return r2**0.25 * (math.sin(50 * r2**0.1)**2 + 1)

# decodificar con 4 bits en [-512, 512]
entero = int("1010", 2)
x = -512 + entero * 1024 / (2**4 - 1)
print("1010 ->", entero, "-> x =", round(x, 2), " f1 =", round(f1(x), 2), " aptitud =", round(-f1(x), 2))

# resolucion con 20 bits
print("resolucion f1:", 1024 / (2**20 - 1), " f2:", 200 / (2**20 - 1))

# el 0 no es representable en [-100, 100] con 20 bits
m = 2**20 - 1
cerca = min((abs(-100 + k * 200 / m), k) for k in range(524280, 524295))
print("valor mas cercano a 0:", cerca, " f2 ahi:", round(f2(cerca[0], cerca[0]), 5))

# minimo de f1
print("f1(420.9687) =", round(f1(420.9687), 4), " f1(-512) =", round(f1(-512), 2))

# evaluaciones por corrida
print("evaluaciones AG:", 50 * 200 + 50, " gradiente f1:", 1000 * 2, " f2:", 1000 * 4)

# UAR: decir siempre ALL
print("siempre ALL: accuracy train", round(27 / 38, 3), " UAR", (1 + 0) / 2)

# aptitud con beta = 0.2 y 50 candidatos
for k in [2, 3, 4]:
    print("UAR 1 con", k, "genes ->", round(1 - 0.2 * k / 50, 3))
print("costo de un gen:", 0.2 / 50, " un error AML:", round(0.5 / 11, 3), " un error ALL:", round(0.5 / 27, 3))

# test: cuanto mueve un error
print("un error en test AML:", round(0.5 / 14, 3), " ALL:", round(0.5 / 20, 3))
