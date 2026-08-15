import numpy as np


def cargar_patrones(ruta):
    datos = np.loadtxt(ruta, delimiter=",")
    entradas = datos[:, :-1]
    salidas_deseadas = datos[:, -1]
    return entradas, salidas_deseadas
