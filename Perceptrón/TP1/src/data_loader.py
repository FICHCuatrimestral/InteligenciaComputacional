"""
data_loader.py

Lectura de patrones de entrenamiento/prueba para el perceptrón simple.

Formato esperado del archivo CSV: cada fila es
    x1, x2, ..., xN, y_d
es decir, N columnas de entrada seguidas de la salida deseada.

La convención de la cátedra usa la "entrada extendida": se agrega una
columna x0 = -1 al principio, de forma que el umbral u se trata como
un peso más (w0 = u), en vez de un caso especial. Ver ecuación (2) y (3)
del apunte de Perceptrón simple.
"""

import numpy as np


def cargar_patrones(ruta_archivo, valor_entrada_bias=-1.0):
    """
    Carga un archivo de patrones en formato CSV separado por comas.

    Parámetros
    ----------
    ruta_archivo : str
        Ruta al archivo CSV (por ejemplo "Dataset/OR_trn.csv").
    valor_entrada_bias : float
        Valor de la entrada extendida x0. La cátedra usa -1 (con w0 = u).
        Si en algún momento necesitás la convención de Haykin (x0 = +1,
        w0 = b), simplemente llamá a la función con valor_entrada_bias=1.0.

    Retorna
    -------
    entradas : np.ndarray de forma (cantidad_patrones, N + 1)
        Matriz de entradas, con la primera columna igual a valor_entrada_bias.
    salidas_deseadas : np.ndarray de forma (cantidad_patrones,)
        Vector de salidas deseadas (y_d).
    """
    datos = np.loadtxt(ruta_archivo, delimiter=",")

    # Si el archivo tiene un solo patrón, np.loadtxt devuelve un vector
    # 1D en vez de una matriz de una sola fila. Lo normalizamos.
    if datos.ndim == 1:
        datos = datos.reshape(1, -1)

    entradas_originales = datos[:, :-1]   # todas las columnas menos la última
    salidas_deseadas = datos[:, -1]       # la última columna: salida deseada

    cantidad_patrones = entradas_originales.shape[0]
    columna_bias = np.full((cantidad_patrones, 1), valor_entrada_bias)

    entradas = np.hstack([columna_bias, entradas_originales])
    return entradas, salidas_deseadas


if __name__ == "__main__":
    # Prueba rápida y manual del loader.
    import sys

    ruta = sys.argv[1] if len(sys.argv) > 1 else "../Dataset/OR_trn.csv"
    entradas, salidas_deseadas = cargar_patrones(ruta)
    print(f"Archivo: {ruta}")
    print(f"Cantidad de patrones: {entradas.shape[0]}")
    print(f"Cantidad de entradas (con x0): {entradas.shape[1]}")
    print("Primeras 3 filas de entradas:\n", entradas[:3])
    print("Primeras 3 salidas deseadas:\n", salidas_deseadas[:3])
