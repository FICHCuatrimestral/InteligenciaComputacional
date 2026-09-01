import numpy as np


def cargar_patrones(ruta, n_salidas=1):
    """Lee un CSV sin encabezado donde las ultimas `n_salidas` columnas son la salida deseada.

    Devuelve (entradas, salidas_deseadas). Con n_salidas=1 la salida sale como vector
    de una dimension; con n_salidas>1, como matriz de (cantidad_de_patrones, n_salidas).
    """
    datos = np.loadtxt(ruta, delimiter=",")
    entradas = datos[:, :-n_salidas]
    salidas_deseadas = datos[:, -n_salidas:]
    if n_salidas == 1:
        salidas_deseadas = salidas_deseadas[:, 0]
    return entradas, salidas_deseadas


def armar_arquitectura(cantidad_entradas, neuronas_ocultas, cantidad_salidas):
    """Arma la lista que espera PerceptronMulticapa a partir de sus tres partes.

    armar_arquitectura(2, [4], 1)      -> [2, 4, 1]     una capa oculta de 4
    armar_arquitectura(2, [8, 6], 1)   -> [2, 8, 6, 1]  dos capas ocultas
    armar_arquitectura(4, [], 3)       -> [4, 3]        sin capa oculta
    """
    return [cantidad_entradas] + list(neuronas_ocultas) + [cantidad_salidas]
