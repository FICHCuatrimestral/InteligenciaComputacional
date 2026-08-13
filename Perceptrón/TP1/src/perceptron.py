"""
perceptron.py

Clase Perceptron: implementa el perceptrón simple con activación signo
y la regla de aprendizaje por corrección de error (ecuación 13 del
apunte de cátedra):

    pesos(n+1) = pesos(n) + (tasa_aprendizaje/2) * [salida_deseada(n) - salida(n)] * patron(n)

Se asume que las entradas ya vienen con la columna extendida x0
(ver data_loader.py), así que el vector de pesos tiene tamaño
cantidad_entradas + 1 y no hay que tratar el bias como caso especial
en ningún lado.
"""

import numpy as np


class Perceptron:
    def __init__(self, cantidad_entradas, tasa_aprendizaje=0.1, semilla=None):
        """
        Parámetros
        ----------
        cantidad_entradas : int
            Cantidad de entradas SIN contar la entrada extendida x0
            (por ejemplo, 2 para el problema OR). Internamente el
            vector de pesos tendrá tamaño cantidad_entradas + 1.
        tasa_aprendizaje : float
            Qué tan grande es cada corrección de los pesos (llamada
            "eta" en el apunte). Cuanto más grande, más rápido se mueven
            los pesos en cada patrón mal clasificado; cuanto más chica,
            más lento pero más "suave".
        semilla : int o None
            Semilla para la inicialización aleatoria de pesos. Sirve
            solo para debuggear con resultados reproducibles; en el
            uso normal se deja en None (pesos iniciales distintos cada vez).
        """
        generador_aleatorio = np.random.default_rng(semilla)
        # Pesos iniciales aleatorios pequeños en [-0.5, 0.5], como indica
        # la diapositiva de la cátedra: w(1) in [-0.5, 0.5].
        self.pesos = generador_aleatorio.uniform(-0.5, 0.5, size=cantidad_entradas + 1)
        self.tasa_aprendizaje = tasa_aprendizaje

    @staticmethod
    def funcion_signo(nivel_activacion):
        """+1 si nivel_activacion >= 0, -1 en caso contrario (sgn(0)=+1)."""
        return np.where(nivel_activacion >= 0, 1.0, -1.0)

    def calcular_salida(self, patron):
        """Calcula y = sgn(pesos . patron) para UN solo patrón (incluye x0)."""
        nivel_activacion = np.dot(self.pesos, patron)
        return self.funcion_signo(nivel_activacion)

    def predecir(self, entradas):
        """Calcula y = sgn(pesos . patron) para TODA una matriz de patrones."""
        nivel_activacion = entradas @ self.pesos
        return self.funcion_signo(nivel_activacion)

    def _entrenar_una_epoca(self, entradas, salidas_deseadas):
        """
        Recorre todo el conjunto de entrenamiento una vez (una época),
        aplicando la regla de corrección de error patrón por patrón.

        Retorna la cantidad de patrones mal clasificados en esta época
        (antes de corregirlos), que es lo que se usa para el criterio
        de finalización "cero errores".
        """
        cantidad_errores = 0
        for patron, salida_deseada in zip(entradas, salidas_deseadas):
            salida_obtenida = self.calcular_salida(patron)
            if salida_obtenida != salida_deseada:
                cantidad_errores += 1
                correccion = (self.tasa_aprendizaje / 2) * (salida_deseada - salida_obtenida)
                self.pesos = self.pesos + correccion * patron
        return cantidad_errores

    def entrenar(self, entradas, salidas_deseadas, maximo_epocas=100,
                 criterio_de_corte="cero_errores", mostrar_progreso=False):
        """
        Entrena el perceptrón hasta cumplir el criterio de finalización
        elegido o alcanzar maximo_epocas.

        Parámetros
        ----------
        entradas, salidas_deseadas : arrays devueltos por data_loader.cargar_patrones
        maximo_epocas : int
            Número máximo de épocas (obligatorio: si el problema no es
            linealmente separable, "cero_errores" nunca se cumple).
        criterio_de_corte : str
            "cero_errores" -> corta apenas una época entera no tiene errores.
            "max_epocas"   -> siempre entrena las maximo_epocas completas
                              (útil para comparar/graficar la convergencia).
        mostrar_progreso : bool
            Si True, imprime la cantidad de errores en cada época.

        Retorna
        -------
        errores_por_epoca : list[int]
            Cantidad de errores en cada época, en orden.
        """
        errores_por_epoca = []

        for numero_epoca in range(1, maximo_epocas + 1):
            cantidad_errores = self._entrenar_una_epoca(entradas, salidas_deseadas)
            errores_por_epoca.append(cantidad_errores)

            if mostrar_progreso:
                print(f"  Época {numero_epoca}: {cantidad_errores} errores "
                      f"(tasa_aprendizaje={self.tasa_aprendizaje})")

            if criterio_de_corte == "cero_errores" and cantidad_errores == 0:
                break

        return errores_por_epoca

    def probar(self, entradas, salidas_deseadas):
        """
        Prueba el perceptrón ya entrenado sobre un conjunto de datos
        (típicamente uno que nunca vio durante el entrenamiento).

        Retorna
        -------
        porcentaje_aciertos : float
            Porcentaje de patrones bien clasificados (0 a 100).
        cantidad_errores : int
            Cantidad de patrones mal clasificados.
        """
        salidas_obtenidas = self.predecir(entradas)
        cantidad_aciertos = np.sum(salidas_obtenidas == salidas_deseadas)
        cantidad_errores = len(salidas_deseadas) - cantidad_aciertos
        porcentaje_aciertos = 100.0 * cantidad_aciertos / len(salidas_deseadas)
        return porcentaje_aciertos, cantidad_errores
