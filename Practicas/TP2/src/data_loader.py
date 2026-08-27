import numpy as np


def cargar_patrones(ruta, n_salidas=1):
    datos = np.loadtxt(ruta, delimiter=",")
    entradas = datos[:, :-n_salidas]
    salidas_deseadas = datos[:, -n_salidas:]
    if n_salidas == 1:
        salidas_deseadas = salidas_deseadas[:, 0]
    return entradas, salidas_deseadas
