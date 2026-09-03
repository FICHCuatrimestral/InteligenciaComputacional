import pandas as pd
import numpy as np
from graficos import dispersion
from graficos import curvas

#carga de datos-------------------------------------
archivo = "iris81"
entradas = 4
salidas = 3
alpha = 0.1
capas = [entradas,4,4,salidas]

#funciones------------------------------------------
def sigmoide(v):
    return 2 / (1 + np.exp(-v)) - 1

def derivada_sigmoide(y):
    return 0.5 * (1 - y**2)

#definiciones---------------------------------------

positivos = []
negativos = []
incorrectos = []

print('Tasa:', alpha)
print('Estructura: ',end="")
for i in range(len(capas)):
    print(capas[i],end=" ")
print()

w = []
b = []

for i in range(len(capas)-1):
    w.append(np.random.uniform(-0.5, 0.5, (capas[i], capas[i+1])))
    b.append(np.random.uniform(-0.5, 0.5, capas[i+1]))


# train ---------------------------------------
datos = pd.read_csv(archivo + "_trn.csv", header=None)
X = datos.iloc[:, 0:entradas].values
yd = datos.iloc[:, entradas:entradas+salidas].values

errores_cuadraticos = []
cant_errores = []
epocas = 0

for epoca in range(1000):

    errores = 0
    error_cuadratico = 0

    for i in range(len(X)):

        a = X[i]

        # propagacion
        activaciones = [a]

        for j in range(len(capas)-1):
            salida = np.dot(a, w[j]) + b[j]
            a = sigmoide(salida)
            activaciones.append(a)

        error = yd[i] - a
        error_cuadratico = error_cuadratico + np.sum(error ** 2)


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

    epocas = epocas + 1
    errores_cuadraticos.append(error_cuadratico)
    cant_errores.append(errores)
    if errores == 0: break


print('Epocas:', epocas)


# test -------------------------------------------------

datos = pd.read_csv(archivo + "_tst.csv", header=None)
X = datos.iloc[:, 0:entradas].values
yd = datos.iloc[:, entradas:entradas+salidas].values

C = 0

for i in range(len(X)):

    a = X[i]

    #propagacion
    for j in range(len(capas)-1):
        salida = np.dot(a, w[j]) + b[j]
        a = sigmoide(salida)
  

    # clasificacion-----------------------

    # 1 salida-------------
    if len(a) == 1:

        if a[0] >= 0:
            y = 1
        else:
            y = -1

        if y == yd[i][0]:
            C = C + 1
            if yd[i][0] == 1:
                positivos.append(X[i])
            else:
                negativos.append(X[i])
        else:
            incorrectos.append(X[i])

    # +2 salidas-------------
    else:
        y = np.full(len(a), -1)
        y[np.argmax(a)] = 1

        if np.array_equal(y, yd[i]):
            C = C + 1
 


print('Aciertos:',C)
print(C / len(X) * 100, '%')

if salidas == 1:
    dispersion(positivos,negativos,incorrectos)
else:
    curvas(errores_cuadraticos, cant_errores)
