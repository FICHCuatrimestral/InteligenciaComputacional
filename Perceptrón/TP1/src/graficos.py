import numpy as np
from IPython.display import Image, display
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def _graficar_patrones(ax, entradas, salidas):
    positivos = entradas[salidas == 1]
    negativos = entradas[salidas == -1]
    ax.scatter(positivos[:, 0], positivos[:, 1], c="tab:blue", s=15, label="Clase +1")
    ax.scatter(negativos[:, 0], negativos[:, 1], c="tab:red", s=15, label="Clase -1")


def _puntos_recta(pesos, umbral, x1_rango):
    w1, w2 = pesos
    if abs(w2) < 1e-9:
        return None
    x1 = np.array(x1_rango)
    x2 = (umbral - w1 * x1) / w2
    return x1, x2


def _rango_ejes(entradas, margen=0.5):
    x1_rango = (entradas[:, 0].min() - margen, entradas[:, 0].max() + margen)
    x2_rango = (entradas[:, 1].min() - margen, entradas[:, 1].max() + margen)
    return x1_rango, x2_rango


def _mismo_estado(historial_pesos, indice_a, indice_b):
    pesos_a, umbral_a = historial_pesos[indice_a]
    pesos_b, umbral_b = historial_pesos[indice_b]
    return np.array_equal(pesos_a, pesos_b) and umbral_a == umbral_b


def _checkpoints_sin_duplicados(historial_pesos, cantidad_checkpoints):
    cantidad = min(cantidad_checkpoints, len(historial_pesos))
    candidatos = np.unique(np.linspace(0, len(historial_pesos) - 1, cantidad).astype(int))

    # Una vez que el perceptrón converge, los pesos quedan congelados (punto fijo): si dos
    # checkpoints consecutivos caen en el mismo estado, la recta del primero queda tapada por
    # la del segundo. Nos quedamos solo con el último de cada tramo de estados repetidos.
    indices = []
    for posicion, indice in enumerate(candidatos):
        es_ultimo = posicion == len(candidatos) - 1
        if not es_ultimo and _mismo_estado(historial_pesos, indice, candidatos[posicion + 1]):
            continue
        indices.append(indice)
    return indices


def graficar_y_animar_entrenamientos(
    casos, ruta_gif, cantidad_checkpoints=6, fps=5, cantidad_frames_max=30, dpi=100
):
    """Grilla 2×2: por cada caso (columna) un panel estático de checkpoints arriba y uno
    animado, época a época, abajo. Los cuatro paneles quedan en una sola figura, guardada
    como un único GIF (el panel animado es el único que cambia entre frames).

    `casos` es una lista de tuplas (entradas, salidas, historial_pesos, titulo). Cuando el
    entrenamiento más largo tiene más de `cantidad_frames_max` épocas, se muestrea un
    subconjunto parejo en vez de una época por frame, para que el GIF no crezca sin límite
    (relevante para GitHub, que no renderiza notebooks con outputs muy pesados).
    """
    columnas = len(casos)
    fig, ejes = plt.subplots(2, columnas, figsize=(5.0 * columnas, 5.0 * 2), squeeze=False)

    lineas = []
    for columna, (entradas, salidas, historial_pesos, titulo) in enumerate(casos):
        x1_rango, x2_rango = _rango_ejes(entradas)

        ax_estatico = ejes[0][columna]
        _graficar_patrones(ax_estatico, entradas, salidas)
        indices = _checkpoints_sin_duplicados(historial_pesos, cantidad_checkpoints)
        colores = plt.cm.viridis(np.linspace(0, 1, len(indices)))
        for color, indice in zip(colores, indices):
            pesos, umbral = historial_pesos[indice]
            recta = _puntos_recta(pesos, umbral, x1_rango)
            if recta is not None:
                ax_estatico.plot(*recta, color=color, linewidth=2, label=f"Época {indice}")
        ax_estatico.set_xlim(*x1_rango)
        ax_estatico.set_ylim(*x2_rango)
        ax_estatico.set_xlabel("x₁")
        ax_estatico.set_ylabel("x₂")
        ax_estatico.set_title(f"{titulo} — checkpoints")
        ax_estatico.grid(True, linestyle="--", alpha=0.4)
        ax_estatico.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=8)

        ax_animado = ejes[1][columna]
        _graficar_patrones(ax_animado, entradas, salidas)
        linea, = ax_animado.plot([], [], color="black", linewidth=2, label="Recta de separación")
        ax_animado.set_xlim(*x1_rango)
        ax_animado.set_ylim(*x2_rango)
        ax_animado.set_xlabel("x₁")
        ax_animado.set_ylabel("x₂")
        ax_animado.grid(True, linestyle="--", alpha=0.4)
        ax_animado.legend(loc="upper right", fontsize=8)
        lineas.append((ax_animado, linea, x1_rango, historial_pesos, titulo))

    fig.tight_layout()

    epoca_maxima = max(len(historial_pesos) - 1 for _, _, _, historial_pesos, _ in lineas)
    cantidad_frames = min(cantidad_frames_max, epoca_maxima + 1)
    epocas_objetivo = np.unique(np.linspace(0, epoca_maxima, cantidad_frames).astype(int))

    def actualizar(indice_frame):
        epoca_objetivo = epocas_objetivo[indice_frame]
        artistas = []
        for ax, linea, x1_rango, historial_pesos, titulo in lineas:
            indice_caso = min(epoca_objetivo, len(historial_pesos) - 1)
            pesos, umbral = historial_pesos[indice_caso]
            recta = _puntos_recta(pesos, umbral, x1_rango)
            if recta is not None:
                linea.set_data(*recta)
            ax.set_title(f"{titulo} — animado, época {indice_caso} de {len(historial_pesos) - 1}")
            artistas.append(linea)
        return artistas

    animacion = FuncAnimation(fig, actualizar, frames=len(epocas_objetivo), blit=False)
    ruta_gif.parent.mkdir(parents=True, exist_ok=True)
    animacion.save(ruta_gif, writer=PillowWriter(fps=fps), dpi=dpi)
    plt.close(fig)

    display(Image(filename=str(ruta_gif)))
