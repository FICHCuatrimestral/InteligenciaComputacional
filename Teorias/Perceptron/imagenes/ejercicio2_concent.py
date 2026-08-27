import numpy as np
from matplotlib import pyplot as plt
from clase_mlp import PerceptronMulticapa

CARPETA = "/mnt/user-data/uploads/InteligenciaComputacional/Practicas/TP2/Dataset/"
FACTOR_DE_ESCALA = 4.0
CENTRO_DE_LOS_DATOS = 0.5


def cargar_patrones(ruta):
    datos = np.loadtxt(ruta, delimiter=",")
    return datos[:, :-1], datos[:, -1]


def normalizar(entradas):
    return (entradas - CENTRO_DE_LOS_DATOS) * FACTOR_DE_ESCALA


entradas_entrenamiento, deseadas_entrenamiento = cargar_patrones(CARPETA + "concent_trn.csv")
entradas_prueba, deseadas_prueba = cargar_patrones(CARPETA + "concent_tst.csv")

red = PerceptronMulticapa([2, 8, 1], tasa_aprendizaje=0.1, semilla=0)
red.entrenar(normalizar(entradas_entrenamiento), deseadas_entrenamiento,
             maximo_epocas=60, tolerancia=0.1)

porcentaje_aciertos, cantidad_errores = red.probar(normalizar(entradas_prueba), deseadas_prueba)
print(f"aciertos en prueba: {porcentaje_aciertos:.2f}%  ({cantidad_errores} errores de "
      f"{len(deseadas_prueba)})")

# ------------------------------------------------------------------ figura
SUPERFICIE, TINTA = "#fcfcfb", "#52514e"
COLOR_INTERIOR, COLOR_EXTERIOR = "#eb6834", "#2a78d6"

predicciones = np.where(red.predecir(normalizar(entradas_prueba))[:, 0] >= 0, 1.0, -1.0)
acertados = predicciones == deseadas_prueba

resolucion = 320
malla_x1, malla_x2 = np.meshgrid(np.linspace(0, 1, resolucion),
                                 np.linspace(0, 1, resolucion))
puntos_malla = np.column_stack([malla_x1.ravel(), malla_x2.ravel()])
region = np.where(red.predecir(normalizar(puntos_malla))[:, 0] >= 0, 1.0, -1.0)
region = region.reshape(malla_x1.shape)

figura, (izquierda, derecha) = plt.subplots(1, 2, figsize=(10.6, 5.1))
for ax in (izquierda, derecha):
    ax.set_aspect("equal"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$", rotation=0, labelpad=12)
    ax.grid(True, color="#e6e5e0", linewidth=0.7); ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)

for clase, color, marcador, etiqueta in ((-1, COLOR_INTERIOR, "s", "clase $-1$ (interior)"),
                                         (1, COLOR_EXTERIOR, "o", "clase $+1$ (exterior)")):
    seleccion = deseadas_prueba == clase
    izquierda.scatter(entradas_prueba[seleccion, 0], entradas_prueba[seleccion, 1],
                      s=9, c=color, marker=marcador, label=etiqueta, linewidths=0)
izquierda.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=TINTA)
izquierda.set_title("Clases reales del conjunto de prueba", fontweight="bold", fontsize=11.5)

derecha.contourf(malla_x1, malla_x2, region, levels=[-1.5, 0, 1.5],
                 colors=[COLOR_INTERIOR, COLOR_EXTERIOR], alpha=0.16)
derecha.contour(malla_x1, malla_x2, region, levels=[0], colors=["#4a3aa7"], linewidths=2.0)
for clase, color, marcador in ((-1, COLOR_INTERIOR, "s"), (1, COLOR_EXTERIOR, "o")):
    seleccion = (predicciones == clase) & acertados
    derecha.scatter(entradas_prueba[seleccion, 0], entradas_prueba[seleccion, 1],
                    s=9, c=color, marker=marcador, linewidths=0)
derecha.scatter(entradas_prueba[~acertados, 0], entradas_prueba[~acertados, 1],
                s=42, facecolor="none", edgecolor="#0b0b0b", linewidths=1.3,
                label=f"mal clasificados ({cantidad_errores})")
derecha.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=TINTA)
derecha.set_title(f"Región aprendida — red $[2,8,1]$, {porcentaje_aciertos:.1f}%",
                  fontweight="bold", fontsize=11.5)

figura.tight_layout()
figura.savefig("/home/claude/figuras/25-concent-region.png", dpi=185, facecolor=SUPERFICIE)
print("figura guardada")
