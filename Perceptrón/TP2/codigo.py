import pandas as pd
import numpy as np

datos = pd.read_csv("Dataset/XOR_trn.csv", header = None)
X = datos.iloc[:, 0:2].values
yd = datos.iloc[:, 2].values

alpha = 0.1
capas = [2,2,3,1]

w = []
b = []

for i in range(len(capas)-1):
    w.append(np.random.uniform(-0.5, 0.5, (capas[i], capas[i+1])))
    b.append(np.random.uniform(-0.5, 0.5, capas[i+1]))



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

        a = X[i]

        # propagacion
        activaciones = [a]

        for j in range(len(capas)-1):
            salida = np.dot(a, w[j]) + b[j]
            a = sigmoide(salida)
            activaciones.append(a)

        error = yd[i] - a


        # retro propagacion
        deltas = [None] * (len(capas)-1)

        # ultima capa
        deltas[-1] = error * derivada_sigmoide(activaciones[-1])

        # capas anteriores
        for j in range(len(deltas)-2, -1, -1):
            deltas[j] = derivada_sigmoide(activaciones[j+1]) * np.dot(w[j+1], deltas[j+1])


        # actualizacion pesos
        for j in range(len(w)):

            w[j] = w[j] + alpha * np.outer(activaciones[j],deltas[j])

            b[j] = b[j] + alpha * deltas[j]


        # Contar errores ---------------------------------

        if np.any(abs(error) > 0.1):

            errores = errores + 1

    if errores == 0: break

print('epocas', epocas)


# test -------------------------------------------------

datos = pd.read_csv("Dataset/XOR_tst.csv", header = None)
X = datos.iloc[:, 0:2].values
yd = datos.iloc[:, 2].values

C = 0

for i in range(len(X)):

    a = X[i]
    for j in range(len(capas)-1):
        salida = np.dot(a, w[j]) + b[j]
        a = sigmoide(salida)
  

    if a >= 0:
        y = 1
    else:
        y = -1


    if y == yd[i]:
        C = C + 1


print('aciertos',C)
print(C / len(X) * 100, '%')