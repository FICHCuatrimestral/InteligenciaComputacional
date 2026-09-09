"""Comprobacion de la derivada de la sigmoide simetrica usada en back-propagation."""
import numpy as np

def sigmoide_simetrica(v, b=1.0):
    return 2.0 / (1.0 + np.exp(-b * v)) - 1.0

def derivada_numerica(v, b=1.0, h=1e-6):
    return (sigmoide_simetrica(v + h, b) - sigmoide_simetrica(v - h, b)) / (2 * h)

def formula_correcta(y, b=1.0):
    return 0.5 * b * (1.0 + y) * (1.0 - y)

def formula_con_signo_invertido(y, b=1.0):
    return 0.5 * b * (1.0 + y) * (y - 1.0)

print(f"{'v':>6} {'y':>9} {'num.':>10} {'1/2(1+y)(1-y)':>15} {'1/2(1+y)(y-1)':>15}")
print("-" * 60)
for v in (-3.0, -1.0, -0.25, 0.0, 0.25, 1.0, 3.0):
    y = sigmoide_simetrica(v)
    print(f"{v:>6.2f} {y:>9.4f} {derivada_numerica(v):>10.5f} "
          f"{formula_correcta(y):>15.5f} {formula_con_signo_invertido(y):>15.5f}")

valores = np.linspace(-8, 8, 4001)
salidas = sigmoide_simetrica(valores)
error_correcta = np.max(np.abs(derivada_numerica(valores) - formula_correcta(salidas)))
print(f"\nMaximo error de 1/2(1+y)(1-y) frente a la derivada numerica: {error_correcta:.3e}")
print("La derivada de una funcion creciente es siempre positiva:",
      bool(np.all(formula_correcta(salidas) > 0)))
print("La version 1/2(1+y)(y-1) da siempre negativa:",
      bool(np.all(formula_con_signo_invertido(salidas) < 0)))

# El parametro b sobrevive a la derivada aunque las diapositivas lo omitan (usan b=1).
print("\nCon b distinto de 1:")
for b in (0.5, 1.0, 2.0):
    v = 0.7
    y = sigmoide_simetrica(v, b)
    print(f"  b={b:>4}: numerica={derivada_numerica(v, b):.6f}  "
          f"(b/2)(1+y)(1-y)={formula_correcta(y, b):.6f}  "
          f"sin el b={formula_correcta(y, 1.0):.6f}")
