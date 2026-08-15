from pathlib import Path

from src.data_loader import cargar_patrones
from src.perceptron import Perceptron

DIRECTORIO_BASE = Path(__file__).resolve().parent
DIRECTORIO_DATASET = DIRECTORIO_BASE / "Dataset"

archivo_entrenamiento = DIRECTORIO_DATASET / "OR_trn.csv"
archivo_prueba = DIRECTORIO_DATASET / "OR_tst.csv"

entradas_entrenamiento, salidas_deseadas_entrenamiento = cargar_patrones(archivo_entrenamiento)
entradas_prueba, salidas_deseadas_prueba = cargar_patrones(archivo_prueba)

perceptron = Perceptron(
    cantidad_entradas = entradas_entrenamiento.shape[1], 
    tasa_aprendizaje = 0.1, 
    semilla = 42)

errores_por_epoca = perceptron.entrenar(
    entradas_entrenamiento,
    salidas_deseadas_entrenamiento,
    maximo_epocas = 100,
    criterio_de_corte = "cero_errores"
)

porcentaje_aciertos, cantidad_errores_prueba = perceptron.probar(entradas_prueba, salidas_deseadas_prueba)

print(f"Épocas utilizadas: {len(errores_por_epoca)}")
print(f"Errores por época: {errores_por_epoca}")
print(f"Pesos finales: {perceptron.pesos}")
print(f"Umbral final: {perceptron.umbral}")
print(f"Aciertos en prueba: {porcentaje_aciertos:.2f}% ({cantidad_errores_prueba} errores sobre {len(salidas_deseadas_prueba)} patrones)")
