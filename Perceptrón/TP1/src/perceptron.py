import numpy as np


class Perceptron:
    def __init__(self, cantidad_entradas, tasa_aprendizaje=0.1, semilla=None):
        rng = np.random.default_rng(semilla)
        self.pesos = rng.uniform(-0.5, 0.5, cantidad_entradas)
        self.umbral = rng.uniform(-0.5, 0.5)
        self.tasa_aprendizaje = tasa_aprendizaje

    def entrada_neta(self, entradas):
        return np.dot(self.pesos, entradas) - self.umbral

    def activacion(self, suma_ponderada):
        return 1 if suma_ponderada >= 0 else -1

    def predecir(self, entradas):
        return self.activacion(self.entrada_neta(entradas))

    def entrenar_un_patron(self, entradas, salida_deseada):
        salida_obtenida = self.predecir(entradas)
        error = salida_deseada - salida_obtenida
        self.pesos = self.pesos + self.tasa_aprendizaje * error * entradas
        self.umbral = self.umbral - self.tasa_aprendizaje * error

    def entrenar(self, entradas_entrenamiento, salidas_deseadas, maximo_epocas, criterio_de_corte="cero_errores"):
        errores_por_epoca = []
        for epoca in range(maximo_epocas):
            errores_en_esta_epoca = 0
            for entradas, salida_deseada in zip(entradas_entrenamiento, salidas_deseadas):
                salida_antes_de_ajustar = self.predecir(entradas)
                if salida_antes_de_ajustar != salida_deseada:
                    errores_en_esta_epoca += 1
                self.entrenar_un_patron(entradas, salida_deseada)
            errores_por_epoca.append(errores_en_esta_epoca)
            if criterio_de_corte == "cero_errores" and errores_en_esta_epoca == 0:
                break
        return errores_por_epoca

    def probar(self, entradas_prueba, salidas_deseadas_prueba):
        cantidad_patrones = len(salidas_deseadas_prueba)
        cantidad_errores = 0
        for entradas, salida_deseada in zip(entradas_prueba, salidas_deseadas_prueba):
            salida_obtenida = self.predecir(entradas)
            if salida_obtenida != salida_deseada:
                cantidad_errores += 1
        porcentaje_aciertos = 100 * (cantidad_patrones - cantidad_errores) / cantidad_patrones
        return porcentaje_aciertos, cantidad_errores
