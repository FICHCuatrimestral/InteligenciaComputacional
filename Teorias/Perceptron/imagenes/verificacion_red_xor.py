"""Verificacion numerica de la red de 3 neuronas de Milone sobre los 4 patrones del XOR."""
import numpy as np

def signo(z):
    return 1 if z >= 0 else -1

# Orden de los pesos: [w0, w1, w2], con x0 = -1 como entrada de sesgo.
pesos_A = np.array([-1.0, +1.0, +1.0])   # recta x2 = -1 - x1
pesos_B = np.array([+1.0, +1.0, +1.0])   # recta x2 = +1 - x1
# Perceptron C: sus dos entradas son, en el orden del apunte de catedra, (yB, yA)
pesos_C = np.array([+1.0, -1.0, +1.0])   # recta yA = +1 + yB

patrones = [(-1, -1, -1), (-1, +1, +1), (+1, -1, +1), (+1, +1, -1)]

print(f"{'x1':>4}{'x2':>4} | {'vA':>4}{'yA':>4} | {'vB':>4}{'yB':>4} | {'vC':>4}{'y':>4} | {'d':>3}  ok")
print("-" * 56)
todos_correctos = True
for x1, x2, deseada in patrones:
    entrada = np.array([-1.0, x1, x2])
    vA = pesos_A @ entrada; yA = signo(vA)
    vB = pesos_B @ entrada; yB = signo(vB)
    entrada_C = np.array([-1.0, yB, yA])      # (sesgo, yB, yA)
    vC = pesos_C @ entrada_C; y = signo(vC)
    correcto = (y == deseada)
    todos_correctos = todos_correctos and correcto
    print(f"{x1:>4}{x2:>4} | {vA:>4.0f}{yA:>4} | {vB:>4.0f}{yB:>4} | {vC:>4.0f}{y:>4} | {deseada:>3}  {correcto}")

print("-" * 56)
print("La red resuelve el XOR en los 4 patrones:", todos_correctos)

# Comprobacion de que solo importan los cocientes de pesos, no su escala.
print("\nMisma recta A con pesos escalados x7 y desplazados:")
for factor in (1.0, 7.0, 0.25):
    pesos_escalados = factor * pesos_A
    salidas = [signo(pesos_escalados @ np.array([-1.0, a, b]))
               for a, b, _ in patrones]
    print(f"  factor {factor:>5}: pesos {pesos_escalados}  ->  yA = {salidas}")

# Un factor NEGATIVO conserva la recta pero invierte las salidas.
print("\nFactor negativo sobre los pesos de A (misma recta, decision invertida):")
for factor in (+1.0, -1.0):
    pesos_escalados = factor * pesos_A
    salidas = [signo(pesos_escalados @ np.array([-1.0, a, b]))
               for a, b, _ in patrones]
    print(f"  factor {factor:>5}: pesos {pesos_escalados}  ->  yA = {salidas}")
