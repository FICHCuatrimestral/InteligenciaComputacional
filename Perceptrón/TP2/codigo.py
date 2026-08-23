import pandas as pd
import numpy as np

datos = pd.read_csv("XOR_trn.csv", header = None)
X = datos.iloc[:, 0:2].values
yd = datos.iloc[:, 2].values

alpha = 0.1

W1 = np.random.uniform(-0.5, 0.5, (2, 2))
b1 = np.random.uniform(-0.5, 0.5, 2)

W2 = np.random.uniform(-0.5, 0.5, (2, 1))
b2 = np.random.uniform(-0.5, 0.5, 1)

def sigmoide(v):
    return 2 / (1 + np.exp(-v)) - 1

def derivada_sigmoide(y):
    return 0.5 * (1 - y**2)



# train ---------------------------------------
epocas = 0

for epoca in range(1000):
    epocas = epocas + 1
    errores = 0

    for i in range(len(X)):

        entrada = X[i]

        # propagacion
        z1 = np.dot(entrada, W1) + b1
        a1 = sigmoide(z1)

        z2 = np.dot(a1, W2) + b2
        y = sigmoide(z2)[0]

        error = yd[i] - y



        # retro propagacion
        delta2 = error * derivada_sigmoide(y)

        delta1 = derivada_sigmoide(a1)* (W2.flatten() * delta2)



        # actualizacion pesos
        W2 = W2 + alpha * np.outer(a1, delta2)

        b2 = b2 + alpha * delta2

        W1 = W1 + alpha * np.outer(entrada, delta1)

        b1 = b1 + alpha * delta1

        if abs(error) > 0.1:
            errores = errores + 1

    if errores == 0: break

print(epocas )


# test -------------------------------------------------

datos = pd.read_csv("XOR_tst.csv", header = None)
X = datos.iloc[:, 0:2].values
yd = datos.iloc[:, 2].values

C = 0

for i in range(len(X)):

    z1 = np.dot(X[i], W1) + b1
    a1 = sigmoide(z1)

    z2 = np.dot(a1, W2) + b2
    y = sigmoide(z2)[0]

    if y >= 0:
        y = 1
    else:
        y = -1


    if y == yd[i]:
        C = C + 1


print(C)
print("%:", C / len(X))
print(len(X))