"""
entrenar_or.py

Ejercicio 1 - Perceptrón simple aplicado al problema OR.

Entrena un perceptrón con el archivo OR_trn.csv y lo prueba con OR_tst.csv
(un archivo que el perceptrón nunca vio durante el entrenamiento).

Para ver el efecto de la tasa de aprendizaje, este script entrena varias
veces con distintos valores y compara los resultados.
"""

from pathlib import Path

from src.data_loader import cargar_patrones
from src.perceptron import Perceptron

# ---------------------------------------------------------------------------
# Rutas de los archivos, calculadas a partir de la ubicación de ESTE
# archivo (no de la carpeta desde donde se ejecute el script). Así el
# script funciona sin importar si lo corrés parado en TP1/, desde VSCode
# con otra carpeta raíz abierta, o con doble clic.
# ---------------------------------------------------------------------------
DIRECTORIO_BASE = Path(__file__).resolve().parent
DIRECTORIO_DATASET = DIRECTORIO_BASE / "Dataset"

archivo_entrenamiento = DIRECTORIO_DATASET / "OR_trn.csv"
archivo_prueba = DIRECTORIO_DATASET / "OR_tst.csv"

for archivo in (archivo_entrenamiento, archivo_prueba):
    if not archivo.exists():
        raise FileNotFoundError(
            f"No encontré el archivo {archivo}. "
            f"Verificá que exista la carpeta Dataset/ junto a este script "
            f"(debería estar en: {DIRECTORIO_DATASET})."
        )

# ---------------------------------------------------------------------------
# Parámetros configurables del ejercicio 1
# ---------------------------------------------------------------------------
tasas_aprendizaje_a_probar = [0.01, 0.1, 1.0]
maximo_epocas = 100
criterio_de_corte = "cero_errores"   # o "max_epocas"
semilla = 42                          # fija para poder comparar en igualdad de condiciones

# ---------------------------------------------------------------------------
# Carga de datos (una sola vez, se reusa en cada corrida)
# ---------------------------------------------------------------------------
entradas_entrenamiento, salidas_deseadas_entrenamiento = cargar_patrones(archivo_entrenamiento)
entradas_prueba, salidas_deseadas_prueba = cargar_patrones(archivo_prueba)

cantidad_entradas = entradas_entrenamiento.shape[1] - 1  # -1 porque descontamos x0

print(f"Entrenamiento: {entradas_entrenamiento.shape[0]} patrones "
      f"({cantidad_entradas} entradas + bias)")
print(f"Prueba: {entradas_prueba.shape[0]} patrones\n")

# ---------------------------------------------------------------------------
# Entrenar y probar con cada tasa de aprendizaje
# ---------------------------------------------------------------------------
for tasa_aprendizaje in tasas_aprendizaje_a_probar:
    print(f"=== tasa_aprendizaje = {tasa_aprendizaje} ===")

    perceptron = Perceptron(cantidad_entradas, tasa_aprendizaje=tasa_aprendizaje, semilla=semilla)

    errores_por_epoca = perceptron.entrenar(
        entradas_entrenamiento,
        salidas_deseadas_entrenamiento,
        maximo_epocas=maximo_epocas,
        criterio_de_corte=criterio_de_corte,
        mostrar_progreso=True,
    )

    porcentaje_aciertos, cantidad_errores_prueba = perceptron.probar(
        entradas_prueba, salidas_deseadas_prueba
    )

    print(f"  -> Épocas necesarias: {len(errores_por_epoca)}")
    print(f"  -> Pesos finales: {perceptron.pesos}")
    print(f"  -> Test: {porcentaje_aciertos:.2f}% de aciertos "
          f"({cantidad_errores_prueba} errores sobre {len(salidas_deseadas_prueba)} patrones)")
    print()
