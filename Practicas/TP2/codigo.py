from pathlib import Path
import pandas as pd
import numpy as np

DIRECTORIO_DATASET = Path(__file__).resolve().parent / "Dataset"

# lo unico que cambio respecto de su codigo: los dos nombres de archivo
tr = pd.read_csv(DIRECTORIO_DATASET / "concent_trn.csv", header=None)
X  = tr.iloc[:, 0:2].values
yd = tr.iloc[:, 2].values

alpha = 0.1

# la arquitectura, de entrada a salida:
#   [2, 2, 1]      -> una capa oculta de 2   (lo que habia antes)
#   [2, 8, 1]      -> una capa oculta de 8
#   [2, 8, 6, 1]   -> dos capas ocultas, de 8 y de 6
CAPAS = [2, 8, 1]

n = len(CAPAS) - 1        # capas de conexiones

W = []
b = []
for k in range(n):
    W.append(np.random.uniform(-0.5, 0.5, (CAPAS[k], CAPAS[k + 1])))
    b.append(np.random.uniform(-0.5, 0.5, CAPAS[k + 1]))

def sigmoide(v):
    return 2 / (1 + np.exp(-v)) - 1

def derivada_sigmoide(y):
    return 0.5 * (1 - y**2)

# train ---------------------------------------
epocas = 0
for epoca in range(200):
    epocas = epocas + 1
    errores = 0
    for i in range(len(X)):
        entrada = X[i]

        # propagacion
        a = [entrada]
        for k in range(n):
            z = np.dot(a[k], W[k]) + b[k]
            a.append(sigmoide(z))
        y = a[-1][0]

        error = yd[i] - y

        # retro propagacion
        delta = [None] * n
        delta[-1] = error * derivada_sigmoide(a[-1])
        for k in range(n - 2, -1, -1):
            delta[k] = derivada_sigmoide(a[k + 1]) * np.dot(W[k + 1], delta[k + 1])

        # actualizacion pesos
        for k in range(n):
            W[k] = W[k] + alpha * np.outer(a[k], delta[k])
            b[k] = b[k] + alpha * delta[k]

        if abs(error) > 0.1:
            errores = errores + 1
    if errores == 0: break

# test -------------------------------------------------
te = pd.read_csv(DIRECTORIO_DATASET / "concent_tst.csv", header=None)
X_test  = te.iloc[:, 0:2].values
yd_test = te.iloc[:, 2].values

C = 0
for i in range(len(X_test)):
    a = X_test[i]
    for k in range(n):
        a = sigmoide(np.dot(a, W[k]) + b[k])
    y = a[0]
    y = 1 if y >= 0 else -1
    if y == yd_test[i]:
        C = C + 1

piso = 100 * (yd_test > 0).mean()

print("arquitectura:", CAPAS)
print("épocas:", epocas, "de 1000")
print("aciertos:", C, "de", len(X_test))
print("%:", 100 * C / len(X_test))
print("piso (contestar siempre la clase mayoritaria):", round(piso, 2), "%")