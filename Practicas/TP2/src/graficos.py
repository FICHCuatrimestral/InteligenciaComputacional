import numpy as np
from IPython.display import Image, display
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def _propagar_con_pesos(entradas, pesos, umbrales):
    activacion = entradas
    for W, b in zip(pesos, umbrales):
        entrada_neta = activacion @ W + b
        activacion = 2 / (1 + np.exp(-entrada_neta)) - 1
    return activacion


def _predecir_con_pesos(entradas, pesos, umbrales):
    salida = _propagar_con_pesos(entradas, pesos, umbrales)
    return np.where(salida[:, 0] >= 0, 1, -1)


def _graficar_patrones(ax, entradas, salidas):
    positivos = entradas[salidas == 1]
    negativos = entradas[salidas == -1]
    ax.scatter(positivos[:, 0], positivos[:, 1], c="tab:blue", s=15, label="Clase +1",
               edgecolors="k", linewidths=0.3)
    ax.scatter(negativos[:, 0], negativos[:, 1], c="tab:red", s=15, label="Clase -1",
               edgecolors="k", linewidths=0.3)


def _rango_ejes(entradas, margen=0.5):
    x1_rango = (entradas[:, 0].min() - margen, entradas[:, 0].max() + margen)
    x2_rango = (entradas[:, 1].min() - margen, entradas[:, 1].max() + margen)
    return x1_rango, x2_rango


def _grilla(x1_rango, x2_rango, resolucion):
    x1 = np.linspace(*x1_rango, resolucion)
    x2 = np.linspace(*x2_rango, resolucion)
    return np.meshgrid(x1, x2)


def _dibujar_region(ax, malla_x1, malla_x2, pesos, umbrales):
    puntos = np.column_stack([malla_x1.ravel(), malla_x2.ravel()])
    clases = _predecir_con_pesos(puntos, pesos, umbrales).reshape(malla_x1.shape)
    ax.contourf(malla_x1, malla_x2, clases, levels=[-1.5, 0, 1.5],
                colors=["#f4b6b6", "#b6c8f4"], alpha=0.6)


def _mismo_estado(historial, indice_a, indice_b):
    pesos_a, umbrales_a = historial[indice_a]
    pesos_b, umbrales_b = historial[indice_b]
    return (all(np.array_equal(a, b) for a, b in zip(pesos_a, pesos_b))
            and all(np.array_equal(a, b) for a, b in zip(umbrales_a, umbrales_b)))


def _checkpoints_sin_duplicados(historial, cantidad_checkpoints):
    cantidad = min(cantidad_checkpoints, len(historial))
    candidatos = np.unique(np.linspace(0, len(historial) - 1, cantidad).astype(int))

    indices = []
    for posicion, indice in enumerate(candidatos):
        es_ultimo = posicion == len(candidatos) - 1
        if not es_ultimo and _mismo_estado(historial, indice, candidatos[posicion + 1]):
            continue
        indices.append(indice)
    return indices


def graficar_y_animar_regiones(
    casos, ruta_gif, cantidad_checkpoints=6, fps=5, cantidad_frames_max=30, dpi=100,
    resolucion=120,
):
    """Grilla 2×2: por cada caso (columna) un panel estático con la región de decisión final
    arriba y uno animado, época a época, abajo, en una sola figura guardada como un único GIF.

    `casos` es una lista de tuplas (entradas, salidas, historial, titulo), donde `historial`
    es la lista de (pesos, umbrales) que devuelve `PerceptronMulticapa.entrenar`. Igual que en
    TP1, si el entrenamiento más largo supera `cantidad_frames_max` épocas se muestrea un
    subconjunto parejo en vez de una época por frame, para que el GIF no crezca sin límite.
    """
    columnas = len(casos)
    fig, ejes = plt.subplots(2, columnas, figsize=(5.0 * columnas, 5.0 * 2), squeeze=False)

    info_animacion = []
    for columna, (entradas, salidas, historial, titulo) in enumerate(casos):
        x1_rango, x2_rango = _rango_ejes(entradas)
        malla_x1, malla_x2 = _grilla(x1_rango, x2_rango, resolucion)

        ax_estatico = ejes[0][columna]
        indices = _checkpoints_sin_duplicados(historial, cantidad_checkpoints)
        indice_final = indices[-1]
        pesos_final, umbrales_final = historial[indice_final]
        _dibujar_region(ax_estatico, malla_x1, malla_x2, pesos_final, umbrales_final)
        _graficar_patrones(ax_estatico, entradas, salidas)
        ax_estatico.set_xlim(*x1_rango)
        ax_estatico.set_ylim(*x2_rango)
        ax_estatico.set_xlabel("x₁")
        ax_estatico.set_ylabel("x₂")
        ax_estatico.set_title(f"{titulo} — región final (época {indice_final})")
        ax_estatico.legend(loc="upper right", fontsize=8)

        ax_animado = ejes[1][columna]
        ax_animado.set_xlim(*x1_rango)
        ax_animado.set_ylim(*x2_rango)
        info_animacion.append(
            (ax_animado, malla_x1, malla_x2, entradas, salidas, historial, titulo, x1_rango, x2_rango)
        )

    fig.tight_layout()

    epoca_maxima = max(len(historial) - 1 for _, _, historial, _ in casos)
    cantidad_frames = min(cantidad_frames_max, epoca_maxima + 1)
    epocas_objetivo = np.unique(np.linspace(0, epoca_maxima, cantidad_frames).astype(int))

    def actualizar(indice_frame):
        epoca_objetivo = epocas_objetivo[indice_frame]
        for (ax, malla_x1, malla_x2, entradas, salidas, historial, titulo,
             x1_rango, x2_rango) in info_animacion:
            indice_caso = min(epoca_objetivo, len(historial) - 1)
            pesos, umbrales = historial[indice_caso]
            ax.clear()
            _dibujar_region(ax, malla_x1, malla_x2, pesos, umbrales)
            _graficar_patrones(ax, entradas, salidas)
            ax.set_xlim(*x1_rango)
            ax.set_ylim(*x2_rango)
            ax.set_xlabel("x₁")
            ax.set_ylabel("x₂")
            ax.set_title(f"{titulo} — animado, época {indice_caso} de {len(historial) - 1}")
        return []

    animacion = FuncAnimation(fig, actualizar, frames=len(epocas_objetivo), blit=False)
    ruta_gif.parent.mkdir(parents=True, exist_ok=True)
    animacion.save(ruta_gif, writer=PillowWriter(fps=fps), dpi=dpi)
    plt.close(fig)

    display(Image(filename=str(ruta_gif)))
