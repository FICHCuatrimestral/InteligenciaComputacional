"""Figuras del apunte de mapas auto-organizativos.

Genera todos los PNG que referencia ../Resumenes/01-mapas-autoorganizativos.md.
Todas las simulaciones son reales: los numeros que aparecen en el apunte salen
de estas corridas.

    python3 graficos_som.py
"""

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle, FancyArrowPatch

DIRECTORIO_SALIDA = os.path.dirname(os.path.abspath(__file__))

COLOR_DATOS = "#8a8f98"
COLOR_PESOS = "#d1495b"
COLOR_GANADORA = "#d1495b"
COLOR_VECINA = "#2a78d6"
COLOR_INACTIVA = "#c8ccd2"
COLOR_MALLA = "#2a78d6"
COLOR_ACENTO = "#1baf7a"
COLOR_NARANJA = "#eb6834"

plt.rcParams.update(
    {
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.grid": True,
        "grid.alpha": 0.30,
        "grid.linestyle": ":",
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    }
)


def guardar(figura, nombre_archivo):
    ruta_completa = os.path.join(DIRECTORIO_SALIDA, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print("generado:", nombre_archivo)


def apagar_grilla(ejes):
    ejes.grid(False)
    ejes.set_xticks([])
    ejes.set_yticks([])
    for lado in ejes.spines.values():
        lado.set_visible(False)


# ---------------------------------------------------------------------------
# 1. Arquitectura del SOM
# ---------------------------------------------------------------------------


def figura_01_arquitectura():
    figura, (ejes_mapa, ejes_neurona) = plt.subplots(1, 2, figsize=(11.0, 4.4))

    # --- panel izquierdo: el plano de neuronas y las conexiones ---
    cantidad_filas, cantidad_columnas = 6, 8
    posiciones_x, posiciones_y = [], []
    for fila in range(cantidad_filas):
        for columna in range(cantidad_columnas):
            posiciones_x.append(columna * 0.62 + fila * 0.30)
            posiciones_y.append(fila * 0.42)
    ejes_mapa.scatter(
        posiciones_x, posiciones_y, s=190, c=COLOR_INACTIVA,
        edgecolors="#6f7681", zorder=3,
    )

    etiquetas_entrada = [r"$x_1$", r"$x_2$", r"$\vdots$", r"$x_N$"]
    alturas_entrada = [2.35, 1.85, 1.35, 0.85]
    indice_neurona_destacada = 0 * cantidad_columnas + 5
    x_destacada = posiciones_x[indice_neurona_destacada]
    y_destacada = posiciones_y[indice_neurona_destacada]

    for etiqueta, altura in zip(etiquetas_entrada, alturas_entrada):
        ejes_mapa.text(-1.60, altura, etiqueta, fontsize=11, va="center", ha="right")
        if etiqueta != r"$\vdots$":
            ejes_mapa.plot([-1.45, x_destacada], [altura, y_destacada],
                           color="#4a4f57", lw=0.8, zorder=1)
            ejes_mapa.scatter([-1.45], [altura], s=22, c="#4a4f57", zorder=3)

    ejes_mapa.scatter([x_destacada], [y_destacada], s=210, c="black", zorder=4)
    ejes_mapa.text(x_destacada + 0.15, y_destacada - 0.42,
                   r"neurona $j$", fontsize=10)
    ejes_mapa.text(1.2, 3.15,
                   r"$\mathbf{w}_j = (w_{j1},\,w_{j2},\,\ldots,\,w_{jN})$",
                   fontsize=10, color=COLOR_PESOS)
    ejes_mapa.set_title("Una sola capa, ordenada en un plano;\n"
                        "cada entrada llega a TODAS las neuronas")
    ejes_mapa.set_xlim(-3.0, 6.6)
    ejes_mapa.set_ylim(-0.8, 3.5)
    apagar_grilla(ejes_mapa)

    # --- panel derecho: la competencia ---
    apagar_grilla(ejes_neurona)
    ejes_neurona.set_title("La salida: gana la neurona cuyo $\\mathbf{w}_j$\n"
                           "está más cerca de $\\mathbf{x}$")
    ejes_neurona.set_xlim(0, 10)
    ejes_neurona.set_ylim(0, 10)

    centros = {
        1: (2.2, 7.6), 2: (5.6, 8.4), 3: (8.2, 6.6),
        4: (2.6, 3.4), 5: (6.4, 4.0), 6: (8.6, 2.0),
    }
    punto_entrada = (5.2, 6.0)
    distancias = {
        indice: np.hypot(centro[0] - punto_entrada[0], centro[1] - punto_entrada[1])
        for indice, centro in centros.items()
    }
    indice_ganadora = min(distancias, key=distancias.get)

    for indice, centro in centros.items():
        es_ganadora = indice == indice_ganadora
        ejes_neurona.add_patch(
            Circle(centro, 0.55, facecolor=COLOR_GANADORA if es_ganadora else COLOR_INACTIVA,
                   edgecolor="#5a6068", zorder=3)
        )
        ejes_neurona.text(centro[0], centro[1], f"$\\mathbf{{w}}_{indice}$",
                          ha="center", va="center", fontsize=9,
                          color="white" if es_ganadora else "#33383f", zorder=4)
        ejes_neurona.plot([punto_entrada[0], centro[0]], [punto_entrada[1], centro[1]],
                          color=COLOR_GANADORA if es_ganadora else "#b6bcc4",
                          lw=2.0 if es_ganadora else 0.9,
                          ls="-" if es_ganadora else "--", zorder=2)
        ejes_neurona.text(
            (punto_entrada[0] + centro[0]) / 2 + 0.1,
            (punto_entrada[1] + centro[1]) / 2 + 0.18,
            f"{distancias[indice]:.1f}", fontsize=7.5,
            color=COLOR_GANADORA if es_ganadora else "#8a8f98",
        )

    ejes_neurona.scatter(*punto_entrada, s=90, c="black", marker="X", zorder=5)
    ejes_neurona.text(punto_entrada[0] - 0.2, punto_entrada[1] - 0.75,
                      r"$\mathbf{x}(n)$", fontsize=11, ha="center")
    ejes_neurona.text(
        0.4, 0.6,
        r"$j^*(n) = \arg\min_j \|\mathbf{x}(n) - \mathbf{w}_j(n)\|$",
        fontsize=11,
    )
    guardar(figura, "01-arquitectura.png")


# ---------------------------------------------------------------------------
# 2. Vecindades
# ---------------------------------------------------------------------------


def figura_02_vecindades():
    figura, ejes = plt.subplots(1, 4, figsize=(12.5, 3.3))

    # lineal, radio 1
    for indice in range(7):
        distancia = abs(indice - 3)
        color = COLOR_GANADORA if distancia == 0 else (COLOR_VECINA if distancia <= 1 else COLOR_INACTIVA)
        ejes[0].add_patch(Circle((indice, 0), 0.42, facecolor=color, edgecolor="#5a6068"))
    ejes[0].set_xlim(-0.8, 6.8)
    ejes[0].set_ylim(-3.8, 3.8)
    ejes[0].set_title(r"Lineal, $\Lambda_G = 1$")

    # cuadrada radio 1 y radio 2
    for panel, radio in ((1, 1), (2, 2)):
        for fila in range(7):
            for columna in range(7):
                distancia = max(abs(fila - 3), abs(columna - 3))
                color = COLOR_GANADORA if distancia == 0 else (
                    COLOR_VECINA if distancia <= radio else COLOR_INACTIVA)
                ejes[panel].add_patch(
                    Circle((columna, -fila), 0.42, facecolor=color, edgecolor="#5a6068")
                )
        ejes[panel].set_xlim(-0.8, 6.8)
        ejes[panel].set_ylim(-6.8, 0.8)
        ejes[panel].set_title(rf"Cuadrada, $\Lambda_G = {radio}$")

    # hexagonal radio 1
    radio_hexagono = 0.55
    paso_horizontal = np.sqrt(3) * radio_hexagono
    paso_vertical = 1.5 * radio_hexagono
    for fila in range(-2, 3):
        for columna in range(-2, 3):
            x = columna * paso_horizontal + (fila % 2) * paso_horizontal / 2
            y = fila * paso_vertical
            distancia = np.hypot(x, y)
            color = COLOR_GANADORA if distancia < 0.05 else (
                COLOR_VECINA if distancia < paso_horizontal * 1.05 else COLOR_INACTIVA)
            ejes[3].add_patch(
                RegularPolygon((x, y), numVertices=6, radius=radio_hexagono,
                               orientation=0, facecolor=color, edgecolor="#5a6068")
            )
    ejes[3].set_xlim(-2.8, 2.8)
    ejes[3].set_ylim(-2.8, 2.8)
    ejes[3].set_title(r"Hexagonal, $\Lambda_G = 1$")

    for eje in ejes:
        eje.set_aspect("equal")
        apagar_grilla(eje)
    figura.suptitle("Rojo: la ganadora. Azul: las que también se actualizan.", y=0.02,
                    fontsize=9, color="#52514e")
    guardar(figura, "02-vecindades.png")


# ---------------------------------------------------------------------------
# 3. Funciones de excitación/inhibición lateral
# ---------------------------------------------------------------------------


def figura_03_funciones_laterales():
    distancia = np.linspace(-6, 6, 1200)
    beta = 1.0

    uniforme = np.where(np.abs(distancia) <= 2, beta, 0.0)
    sigma = 1.5
    gaussiana = beta * np.exp(-(distancia ** 2) / (2 * sigma ** 2))
    sombrero = beta * (
        1.6 * np.exp(-(distancia ** 2) / (2 * 0.9 ** 2))
        - 0.7 * np.exp(-(distancia ** 2) / (2 * 2.4 ** 2))
    )

    figura, ejes = plt.subplots(1, 3, figsize=(12.0, 3.4), sharey=True)
    datos = [
        (uniforme, r"Uniforme (rectangular), $\Lambda_G = 2$", COLOR_VECINA),
        (gaussiana, rf"Gaussiana, $\sigma = {sigma}$", COLOR_ACENTO),
        (sombrero, "Sombrero mejicano", COLOR_NARANJA),
    ]
    for eje, (curva, titulo, color) in zip(ejes, datos):
        eje.plot(distancia, curva, color=color, lw=2.2)
        eje.axhline(0, color="#4a4f57", lw=0.9)
        eje.axvline(0, color="#4a4f57", lw=0.9, ls=":")
        eje.set_title(titulo)
        eje.set_xlabel(r"$G - i$   (distancia a la ganadora, en neuronas)")
        eje.set_xlim(-6, 6)
        eje.set_xticks(range(-6, 7, 2))
        eje.set_ylim(-0.65, 1.75)
        eje.grid(True, alpha=0.30, ls=":")
    ejes[0].set_ylabel(r"$h_{G,i}$")
    ejes[2].fill_between(distancia, sombrero, 0, where=sombrero < 0,
                         color=COLOR_NARANJA, alpha=0.18)
    ejes[2].annotate("zona de inhibición", xy=(2.3, -0.22), xytext=(3.0, -0.55),
                     fontsize=8, color=COLOR_NARANJA,
                     arrowprops=dict(arrowstyle="->", color=COLOR_NARANJA, lw=0.9))
    guardar(figura, "03-funciones-laterales.png")


# ---------------------------------------------------------------------------
# Motor de SOM (el mismo que se usa en todas las simulaciones)
# ---------------------------------------------------------------------------


def entrenar_som(
    patrones,
    forma_del_mapa,
    cantidad_de_epocas,
    tasa_inicial,
    tasa_final,
    radio_inicial,
    radio_final,
    semilla,
    pesos_iniciales=None,
    instantes_a_guardar=(),
):
    """SOM cuadrado con vecindad uniforme (la variante de la cátedra)."""
    generador = np.random.default_rng(semilla)
    cantidad_filas, cantidad_columnas = forma_del_mapa
    cantidad_neuronas = cantidad_filas * cantidad_columnas
    dimension = patrones.shape[1]

    if pesos_iniciales is None:
        pesos = generador.uniform(-0.5, 0.5, size=(cantidad_neuronas, dimension))
    else:
        pesos = pesos_iniciales.copy()

    coordenadas = np.array(
        [(fila, columna) for fila in range(cantidad_filas) for columna in range(cantidad_columnas)],
        dtype=float,
    )
    fotogramas = {}
    if 0 in instantes_a_guardar:
        fotogramas[0] = pesos.copy()

    for epoca in range(cantidad_de_epocas):
        avance = epoca / max(cantidad_de_epocas - 1, 1)
        tasa = tasa_inicial + (tasa_final - tasa_inicial) * avance
        radio = radio_inicial + (radio_final - radio_inicial) * avance
        orden = generador.permutation(len(patrones))
        for indice in orden:
            patron = patrones[indice]
            indice_ganadora = int(np.argmin(np.sum((pesos - patron) ** 2, axis=1)))
            distancia_en_el_mapa = np.max(
                np.abs(coordenadas - coordenadas[indice_ganadora]), axis=1
            )
            en_la_vecindad = distancia_en_el_mapa <= radio
            pesos[en_la_vecindad] += tasa * (patron - pesos[en_la_vecindad])
        if (epoca + 1) in instantes_a_guardar:
            fotogramas[epoca + 1] = pesos.copy()

    return pesos, fotogramas


# ---------------------------------------------------------------------------
# 4. Ejemplo 1 — R1 -> R1, dos neuronas
# ---------------------------------------------------------------------------


def figura_04_ejemplo_r1():
    generador = np.random.default_rng(7)
    grupo_izquierdo = generador.normal(-1.0, 0.18, 200)
    grupo_derecho = generador.normal(+1.0, 0.18, 200)
    patrones = np.concatenate([grupo_izquierdo, grupo_derecho]).reshape(-1, 1)

    pesos = np.array([[-0.32], [0.41]])
    tasa = 0.05
    historia = [pesos.flatten().copy()]
    orden = generador.permutation(len(patrones))
    for indice in orden:
        patron = patrones[indice]
        indice_ganadora = int(np.argmin(np.abs(pesos.flatten() - patron[0])))
        pesos[indice_ganadora] += tasa * (patron - pesos[indice_ganadora])
        historia.append(pesos.flatten().copy())
    historia = np.array(historia)

    figura, (ejes_recta, ejes_traza) = plt.subplots(
        2, 1, figsize=(10.0, 5.4), gridspec_kw={"height_ratios": [1, 1.5]}
    )

    ejes_recta.scatter(patrones.flatten(), np.zeros(len(patrones)), s=14,
                       c=COLOR_DATOS, alpha=0.55, label="patrones de entrenamiento")
    ejes_recta.scatter(historia[0], [0.28, 0.28], s=110, marker="v",
                       c=COLOR_VECINA, zorder=4, label="pesos iniciales")
    ejes_recta.scatter(historia[-1], [0.28, 0.28], s=130, marker="v",
                       c=COLOR_PESOS, zorder=5, label="pesos finales")
    for valor_inicial, valor_final in zip(historia[0], historia[-1]):
        ejes_recta.annotate(
            "", xy=(valor_final, 0.20), xytext=(valor_inicial, 0.20),
            arrowprops=dict(arrowstyle="->", color="#4a4f57", lw=1.2, ls=":"),
        )
    ejes_recta.set_ylim(-0.18, 0.5)
    ejes_recta.set_yticks([])
    ejes_recta.set_xlabel(r"$x$   (y también $w$: viven en la misma recta)")
    ejes_recta.set_title(r"Ejemplo 1: $\mathbb{R}^1 \to \mathbb{R}^1$, dos neuronas, sin entorno")
    ejes_recta.legend(loc="upper center", ncol=3, fontsize=8, framealpha=0.9)
    ejes_recta.grid(True, axis="x", alpha=0.3, ls=":")

    ejes_traza.plot(historia[:, 0], color=COLOR_PESOS, lw=1.6, label=r"$w_1$")
    ejes_traza.plot(historia[:, 1], color=COLOR_VECINA, lw=1.6, label=r"$w_2$")
    ejes_traza.axhline(grupo_izquierdo.mean(), color=COLOR_PESOS, ls="--", lw=1.0,
                       label=f"media del grupo izquierdo = {grupo_izquierdo.mean():.3f}")
    ejes_traza.axhline(grupo_derecho.mean(), color=COLOR_VECINA, ls="--", lw=1.0,
                       label=f"media del grupo derecho = {grupo_derecho.mean():.3f}")
    ejes_traza.set_xlabel("iteración $n$ (un patrón por iteración)")
    ejes_traza.set_ylabel("valor del peso")
    ejes_traza.set_title("Cada peso termina en la media de su grupo, sin que nadie se lo diga")
    ejes_traza.legend(fontsize=8, loc="center right")
    ejes_traza.grid(True, alpha=0.3, ls=":")

    figura.tight_layout()
    guardar(figura, "04-ejemplo-r1.png")
    return historia[-1], grupo_izquierdo.mean(), grupo_derecho.mean()


# ---------------------------------------------------------------------------
# 5. Ejemplo 2 y 3 — R2, cuatro neuronas, con y sin entorno
# ---------------------------------------------------------------------------


def generar_cuatro_grupos(generador):
    centros = np.array([[-1.0, 1.0], [1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]])
    patrones = np.concatenate(
        [centro + generador.normal(0, 0.22, size=(120, 2)) for centro in centros]
    )
    return patrones, centros


def figura_05_ejemplo_r2_sin_entorno():
    generador = np.random.default_rng(3)
    patrones, centros = generar_cuatro_grupos(generador)
    pesos_iniciales = generador.uniform(-0.5, 0.5, size=(4, 2))

    pesos_finales, _ = entrenar_som(
        patrones, (1, 4), cantidad_de_epocas=60,
        tasa_inicial=0.30, tasa_final=0.01,
        radio_inicial=0.0, radio_final=0.0, semilla=11,
        pesos_iniciales=pesos_iniciales,
    )

    figura, ejes = plt.subplots(figsize=(6.0, 5.4))
    ejes.scatter(patrones[:, 0], patrones[:, 1], s=12, c=COLOR_DATOS, alpha=0.45,
                 label="patrones")
    ejes.scatter(pesos_iniciales[:, 0], pesos_iniciales[:, 1], s=110, marker="o",
                 facecolor="white", edgecolor=COLOR_VECINA, lw=2, zorder=4,
                 label="pesos iniciales")
    ejes.scatter(pesos_finales[:, 0], pesos_finales[:, 1], s=140, marker="*",
                 c=COLOR_PESOS, zorder=5, label="pesos finales")
    for inicial, final in zip(pesos_iniciales, pesos_finales):
        ejes.annotate("", xy=final, xytext=inicial,
                      arrowprops=dict(arrowstyle="->", color="#4a4f57", lw=1.0, ls=":"))
    for centro in centros:
        ejes.scatter(*centro, s=60, marker="+", c="black", zorder=3)
    ejes.set_xlabel("$x_1$, $w_{j1}$")
    ejes.set_ylabel("$x_2$, $w_{j2}$")
    ejes.set_title("Ejemplo 3: $\\mathbb{R}^2 \\to$ 4 neuronas sin entorno\n"
                   "(cada peso cae en el centro de un grupo: es $k$-medias en línea)")
    ejes.legend(fontsize=8, loc="upper left")
    ejes.set_aspect("equal")
    ejes.grid(True, alpha=0.3, ls=":")
    guardar(figura, "05-ejemplo-r2-sin-entorno.png")

    errores = [
        np.min(np.linalg.norm(centros - peso, axis=1)) for peso in pesos_finales
    ]
    return float(np.max(errores))


def figura_06_efecto_del_entorno():
    """El ejemplo de la clase 005: dos neuronas vecinas se mueven juntas."""
    generador = np.random.default_rng(5)
    grupo_arriba_izquierda = np.array([-1.1, 1.0]) + generador.normal(0, 0.20, (120, 2))
    grupo_arriba_derecha = np.array([1.1, 1.0]) + generador.normal(0, 0.20, (120, 2))
    grupo_abajo = np.array([0.0, -1.2]) + generador.normal(0, 0.20, (120, 2))
    patrones = np.concatenate([grupo_arriba_izquierda, grupo_arriba_derecha, grupo_abajo])

    pesos_iniciales = np.array([[-0.35, -0.15], [0.30, 0.05], [0.05, -0.40], [-0.20, 0.35]])

    _, fotogramas_con = entrenar_som(
        patrones, (2, 2), cantidad_de_epocas=80,
        tasa_inicial=0.35, tasa_final=0.02,
        radio_inicial=1.0, radio_final=0.0, semilla=21,
        pesos_iniciales=pesos_iniciales, instantes_a_guardar=(0, 10, 80),
    )
    _, fotogramas_sin = entrenar_som(
        patrones, (2, 2), cantidad_de_epocas=80,
        tasa_inicial=0.35, tasa_final=0.02,
        radio_inicial=0.0, radio_final=0.0, semilla=21,
        pesos_iniciales=pesos_iniciales, instantes_a_guardar=(0, 10, 80),
    )

    # aristas de la malla 2x2: indices 0,1 arriba; 2,3 abajo
    aristas = [(0, 1), (0, 2), (1, 3), (2, 3)]

    figura, ejes = plt.subplots(1, 4, figsize=(15.0, 4.0))
    paneles = [
        (fotogramas_con[0], "Inicio (idéntico en los dos casos)"),
        (fotogramas_sin[80], r"Sin entorno ($\Lambda_G = 0$ siempre)"),
        (fotogramas_con[80], r"Con entorno ($\Lambda_G: 1 \to 0$)"),
    ]
    for eje, (pesos, titulo) in zip(ejes, paneles):
        eje.scatter(patrones[:, 0], patrones[:, 1], s=10, c=COLOR_DATOS, alpha=0.35)
        for origen, destino in aristas:
            eje.plot([pesos[origen, 0], pesos[destino, 0]],
                     [pesos[origen, 1], pesos[destino, 1]],
                     color=COLOR_MALLA, lw=1.4, zorder=3)
        eje.scatter(pesos[:, 0], pesos[:, 1], s=110, c=COLOR_PESOS, zorder=4)
        for indice, peso in enumerate(pesos):
            eje.text(peso[0] + 0.09, peso[1] + 0.09, str(indice + 1), fontsize=10,
                     color=COLOR_PESOS, fontweight="bold")
        eje.set_title(titulo, fontsize=9.5)
        eje.set_xlim(-2.0, 2.0)
        eje.set_ylim(-2.0, 2.0)
        eje.set_aspect("equal")
        eje.set_xlabel("$x_1$")
        eje.grid(True, alpha=0.3, ls=":")
    ejes[0].set_ylabel("$x_2$")

    # --- barrido de semillas sobre un mapa 6x6: ¿el entorno ordena de verdad? ---
    generador_uniforme = np.random.default_rng(2)
    patrones_uniformes = generador_uniforme.uniform(-1, 1, size=(1500, 2))
    forma_grande = (6, 6)

    def distancias_del_mapa(pesos_planos):
        malla = pesos_planos.reshape(forma_grande[0], forma_grande[1], 2)
        entre_vecinas = []
        for fila in range(forma_grande[0]):
            for columna in range(forma_grande[1] - 1):
                entre_vecinas.append(np.linalg.norm(malla[fila, columna] - malla[fila, columna + 1]))
        for columna in range(forma_grande[1]):
            for fila in range(forma_grande[0] - 1):
                entre_vecinas.append(np.linalg.norm(malla[fila, columna] - malla[fila + 1, columna]))
        entre_todas = [
            np.linalg.norm(pesos_planos[i] - pesos_planos[j])
            for i in range(len(pesos_planos))
            for j in range(i + 1, len(pesos_planos))
        ]
        return np.mean(entre_vecinas), np.mean(entre_todas)

    resumen = {}
    for etiqueta, radio in (("sin entorno", 0.0), ("con entorno", 3.0)):
        medidas = []
        for semilla in range(8):
            pesos_barrido, _ = entrenar_som(
                patrones_uniformes, forma_grande, cantidad_de_epocas=40,
                tasa_inicial=0.6, tasa_final=0.02,
                radio_inicial=radio, radio_final=0.0, semilla=300 + semilla,
            )
            medidas.append(distancias_del_mapa(pesos_barrido))
        resumen[etiqueta] = np.mean(np.array(medidas), axis=0)

    posiciones = np.arange(2)
    ancho = 0.36
    ejes[3].bar(posiciones - ancho / 2, resumen["sin entorno"], ancho,
                color=COLOR_INACTIVA, edgecolor="#5a6068", label="sin entorno")
    ejes[3].bar(posiciones + ancho / 2, resumen["con entorno"], ancho,
                color=COLOR_MALLA, alpha=0.85, label="con entorno")
    ejes[3].set_xticks(posiciones)
    ejes[3].set_xticklabels(["neuronas VECINAS\nen el mapa", "un par CUALQUIERA\nde neuronas"])
    ejes[3].set_ylabel(r"$\|\mathbf{w}_a - \mathbf{w}_b\|$ promedio")
    ejes[3].set_title("Mapa $6\\times 6$, 8 inicializaciones", fontsize=9.5)
    ejes[3].legend(fontsize=8)
    ejes[3].grid(True, axis="y", alpha=0.3, ls=":")
    ejes[3].set_aspect("auto")
    for indice, clave in enumerate(["sin entorno", "con entorno"]):
        for columna in range(2):
            valor = resumen[clave][columna]
            ejes[3].text(columna + (indice - 0.5) * ancho, valor + 0.02,
                         f"{valor:.2f}", ha="center", fontsize=8)

    figura.tight_layout()
    guardar(figura, "06-efecto-del-entorno.png")
    return resumen


# ---------------------------------------------------------------------------
# 7. El despliegue del pañuelo
# ---------------------------------------------------------------------------


def figura_07_despliegue():
    generador = np.random.default_rng(2)
    patrones = generador.uniform(-1, 1, size=(3000, 2))
    forma = (8, 8)

    instantes = (0, 3, 12, 60)
    _, fotogramas = entrenar_som(
        patrones, forma, cantidad_de_epocas=60,
        tasa_inicial=0.60, tasa_final=0.02,
        radio_inicial=4.0, radio_final=0.0, semilla=17,
        instantes_a_guardar=instantes,
    )

    figura, ejes = plt.subplots(1, 4, figsize=(13.0, 3.6))
    titulos = {
        0: "época 0 — inicio al azar\n(pesos en $[-0{,}5;\\,0{,}5]$)",
        3: "época 3 — ordenamiento global\n($\\Lambda_G \\approx 4$)",
        12: "época 12 — transición\n($\\Lambda_G \\approx 3$)",
        60: "época 60 — ajuste fino\n($\\Lambda_G = 0$)",
    }
    for eje, epoca in zip(ejes, instantes):
        pesos = fotogramas[epoca].reshape(forma[0], forma[1], 2)
        eje.scatter(patrones[:400, 0], patrones[:400, 1], s=5, c=COLOR_DATOS, alpha=0.25)
        for fila in range(forma[0]):
            eje.plot(pesos[fila, :, 0], pesos[fila, :, 1], color=COLOR_MALLA, lw=1.0)
        for columna in range(forma[1]):
            eje.plot(pesos[:, columna, 0], pesos[:, columna, 1], color=COLOR_MALLA, lw=1.0)
        eje.scatter(pesos[..., 0], pesos[..., 1], s=8, c=COLOR_PESOS, zorder=4)
        eje.set_title(titulos[epoca], fontsize=9)
        eje.set_xlim(-1.25, 1.25)
        eje.set_ylim(-1.25, 1.25)
        eje.set_aspect("equal")
        eje.grid(True, alpha=0.25, ls=":")
    ejes[0].set_ylabel("$x_2$")
    for eje in ejes:
        eje.set_xlabel("$x_1$")
    guardar(figura, "07-despliegue.png")


def figura_08_sin_ordenamiento():
    """La misma corrida pero arrancando con entorno chico: la malla queda anudada."""
    generador = np.random.default_rng(2)
    patrones = generador.uniform(-1, 1, size=(3000, 2))
    forma = (8, 8)

    resultados = {}
    for etiqueta, radio_inicial in (("con etapa de ordenamiento", 4.0),
                                    ("sin etapa de ordenamiento", 0.0)):
        pesos, _ = entrenar_som(
            patrones, forma, cantidad_de_epocas=60,
            tasa_inicial=0.60, tasa_final=0.02,
            radio_inicial=radio_inicial, radio_final=0.0, semilla=17,
        )
        resultados[etiqueta] = pesos

    def contar_cruces(pesos_planos):
        """Cantidad de pares de aristas de la malla que se cruzan."""
        pesos = pesos_planos.reshape(forma[0], forma[1], 2)
        segmentos = []
        for fila in range(forma[0]):
            for columna in range(forma[1] - 1):
                segmentos.append((pesos[fila, columna], pesos[fila, columna + 1]))
        for columna in range(forma[1]):
            for fila in range(forma[0] - 1):
                segmentos.append((pesos[fila, columna], pesos[fila + 1, columna]))

        def orientacion(a, b, c):
            return np.sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))

        total = 0
        for i in range(len(segmentos)):
            a, b = segmentos[i]
            for j in range(i + 1, len(segmentos)):
                c, d = segmentos[j]
                if (np.allclose(a, c) or np.allclose(a, d)
                        or np.allclose(b, c) or np.allclose(b, d)):
                    continue
                if (orientacion(a, b, c) != orientacion(a, b, d)
                        and orientacion(c, d, a) != orientacion(c, d, b)):
                    total += 1
        return total

    figura, ejes = plt.subplots(1, 2, figsize=(9.0, 4.4))
    conteos = {}
    for eje, (etiqueta, pesos_planos) in zip(ejes, resultados.items()):
        pesos = pesos_planos.reshape(forma[0], forma[1], 2)
        cruces = contar_cruces(pesos_planos)
        conteos[etiqueta] = cruces
        eje.scatter(patrones[:400, 0], patrones[:400, 1], s=5, c=COLOR_DATOS, alpha=0.25)
        for fila in range(forma[0]):
            eje.plot(pesos[fila, :, 0], pesos[fila, :, 1], color=COLOR_MALLA, lw=1.0)
        for columna in range(forma[1]):
            eje.plot(pesos[:, columna, 0], pesos[:, columna, 1], color=COLOR_MALLA, lw=1.0)
        eje.scatter(pesos[..., 0], pesos[..., 1], s=10, c=COLOR_PESOS, zorder=4)
        eje.set_title(f"{etiqueta}\ncruces de la malla: {cruces}")
        eje.set_xlim(-1.25, 1.25)
        eje.set_ylim(-1.25, 1.25)
        eje.set_aspect("equal")
        eje.set_xlabel("$x_1$")
        eje.grid(True, alpha=0.25, ls=":")
    ejes[0].set_ylabel("$x_2$")
    guardar(figura, "08-sin-ordenamiento.png")
    return conteos


# ---------------------------------------------------------------------------
# 9. Las tres etapas: cómo varían eta y Lambda
# ---------------------------------------------------------------------------


def figura_09_etapas():
    epocas = np.arange(0, 5000)
    tasa = np.empty_like(epocas, dtype=float)
    radio = np.empty_like(epocas, dtype=float)

    fin_ordenamiento, fin_transicion = 1000, 2000
    radio_inicial = 5

    for epoca in epocas:
        if epoca < fin_ordenamiento:
            tasa[epoca] = 0.9
            radio[epoca] = radio_inicial
        elif epoca < fin_transicion:
            avance = (epoca - fin_ordenamiento) / (fin_transicion - fin_ordenamiento)
            tasa[epoca] = 0.9 + (0.1 - 0.9) * avance
            radio[epoca] = np.ceil(radio_inicial + (1 - radio_inicial) * avance)
        else:
            tasa[epoca] = 0.1
            radio[epoca] = 0.0

    figura, (ejes_tasa, ejes_radio) = plt.subplots(2, 1, figsize=(9.5, 5.2), sharex=True)

    ejes_tasa.plot(epocas, tasa, color=COLOR_PESOS, lw=2.0, label="lineal")
    tasa_exponencial = np.where(
        epocas < fin_ordenamiento, 0.9,
        np.where(epocas < fin_transicion,
                 0.9 * (0.1 / 0.9) ** ((epocas - fin_ordenamiento) / (fin_transicion - fin_ordenamiento)),
                 0.1),
    )
    ejes_tasa.plot(epocas, tasa_exponencial, color=COLOR_ACENTO, lw=1.6, ls="--",
                   label="exponencial")
    ejes_tasa.set_ylabel(r"$\eta(n)$")
    ejes_tasa.set_ylim(0, 1.0)
    ejes_tasa.legend(fontsize=8, loc="upper right")

    ejes_radio.step(epocas, radio, color=COLOR_VECINA, lw=2.0, where="post")
    ejes_radio.set_ylabel(r"$\Lambda_G(n)$")
    ejes_radio.set_xlabel("época")
    ejes_radio.set_ylim(-0.4, 6)
    ejes_radio.set_yticks(range(0, 6))

    nombres = [
        (0, fin_ordenamiento, "1. Ordenamiento global", "#2a78d6"),
        (fin_ordenamiento, fin_transicion, "2. Transición", "#eb6834"),
        (fin_transicion, 5000, "3. Ajuste fino (convergencia)", "#1baf7a"),
    ]
    for eje in (ejes_tasa, ejes_radio):
        for inicio, fin, _, color in nombres:
            eje.axvspan(inicio, fin, color=color, alpha=0.07)
            eje.axvline(fin, color="#b6bcc4", lw=0.8, ls=":")
        eje.grid(True, alpha=0.3, ls=":")
    for inicio, fin, nombre, color in nombres:
        ejes_tasa.text((inicio + fin) / 2, 0.93, nombre, ha="center", fontsize=8.5,
                       color=color, fontweight="bold")
    ejes_tasa.set_title("Las tres etapas, con un mapa de $10 \\times 10$ como ejemplo")
    figura.tight_layout()
    guardar(figura, "09-etapas.png")


# ---------------------------------------------------------------------------
# 10. Etiquetado y clasificación
# ---------------------------------------------------------------------------


def figura_10_etiquetado():
    generador = np.random.default_rng(41)
    centros = np.array([[-1.2, 1.0], [1.3, 0.9], [0.0, -1.3]])
    patrones, clases = [], []
    for indice, centro in enumerate(centros):
        patrones.append(centro + generador.normal(0, 0.38, size=(200, 2)))
        clases.append(np.full(200, indice))
    patrones = np.concatenate(patrones)
    clases = np.concatenate(clases)

    permutacion = generador.permutation(len(patrones))
    patrones, clases = patrones[permutacion], clases[permutacion]
    corte = int(0.7 * len(patrones))
    patrones_entrenamiento, clases_entrenamiento = patrones[:corte], clases[:corte]
    patrones_prueba, clases_prueba = patrones[corte:], clases[corte:]

    forma = (6, 6)
    pesos, _ = entrenar_som(
        patrones_entrenamiento, forma, cantidad_de_epocas=120,
        tasa_inicial=0.6, tasa_final=0.02,
        radio_inicial=3.0, radio_final=0.0, semilla=9,
    )

    # etiquetado por clase mayoritaria
    conteos = np.zeros((forma[0] * forma[1], len(centros)))
    for patron, clase in zip(patrones_entrenamiento, clases_entrenamiento):
        ganadora = int(np.argmin(np.sum((pesos - patron) ** 2, axis=1)))
        conteos[ganadora, clase] += 1
    etiquetas = np.where(conteos.sum(axis=1) > 0, conteos.argmax(axis=1), -1)

    aciertos = 0
    for patron, clase in zip(patrones_prueba, clases_prueba):
        ganadora = int(np.argmin(np.sum((pesos - patron) ** 2, axis=1)))
        if etiquetas[ganadora] == clase:
            aciertos += 1
    exactitud = aciertos / len(patrones_prueba)

    colores_de_clase = ["#2a78d6", "#eb6834", "#1baf7a"]
    figura, (ejes_espacio, ejes_mapa) = plt.subplots(1, 2, figsize=(11.0, 4.8))

    for indice in range(len(centros)):
        seleccion = clases_entrenamiento == indice
        ejes_espacio.scatter(patrones_entrenamiento[seleccion, 0],
                             patrones_entrenamiento[seleccion, 1],
                             s=10, c=colores_de_clase[indice], alpha=0.30,
                             label=f"clase {chr(65 + indice)}")
    malla = pesos.reshape(forma[0], forma[1], 2)
    for fila in range(forma[0]):
        ejes_espacio.plot(malla[fila, :, 0], malla[fila, :, 1], color="#4a4f57", lw=0.8)
    for columna in range(forma[1]):
        ejes_espacio.plot(malla[:, columna, 0], malla[:, columna, 1], color="#4a4f57", lw=0.8)
    for indice, peso in enumerate(pesos):
        color = colores_de_clase[etiquetas[indice]] if etiquetas[indice] >= 0 else "white"
        ejes_espacio.scatter(peso[0], peso[1], s=70, c=color, edgecolor="black",
                             lw=0.7, zorder=5)
    ejes_espacio.set_title("El mapa desplegado sobre los datos\n(cada neurona pintada con su etiqueta)")
    ejes_espacio.set_xlabel("$x_1$")
    ejes_espacio.set_ylabel("$x_2$")
    ejes_espacio.legend(fontsize=8, loc="upper left")
    ejes_espacio.set_aspect("equal")
    ejes_espacio.grid(True, alpha=0.3, ls=":")

    for fila in range(forma[0]):
        for columna in range(forma[1]):
            indice = fila * forma[1] + columna
            etiqueta = etiquetas[indice]
            color = colores_de_clase[etiqueta] if etiqueta >= 0 else "#e8eaed"
            ejes_mapa.add_patch(
                plt.Rectangle((columna, -fila), 1, 1, facecolor=color,
                              edgecolor="white", lw=1.5)
            )
            texto = chr(65 + etiqueta) if etiqueta >= 0 else "–"
            ejes_mapa.text(columna + 0.5, -fila + 0.5, texto, ha="center", va="center",
                           color="white" if etiqueta >= 0 else "#8a8f98",
                           fontsize=11, fontweight="bold")
    ejes_mapa.set_xlim(0, forma[1])
    ejes_mapa.set_ylim(-forma[0] + 1, 1)
    ejes_mapa.set_aspect("equal")
    apagar_grilla(ejes_mapa)
    ejes_mapa.set_title(f"El mapa $6\\times 6$ etiquetado\n"
                        f"exactitud sobre los datos de prueba: {exactitud:.1%}")
    figura.tight_layout()
    guardar(figura, "10-etiquetado.png")
    return exactitud, int(np.sum(etiquetas < 0))


# ---------------------------------------------------------------------------
# 11. Cuantización escalar y vectorial
# ---------------------------------------------------------------------------


def figura_11_cuantizacion():
    figura, ejes = plt.subplots(1, 3, figsize=(13.0, 3.8))

    tiempo = np.linspace(0, 2 * np.pi, 800)
    senal = np.sin(tiempo)
    niveles = 8
    cuantizada = np.round(senal * (niveles / 2)) / (niveles / 2)
    ejes[0].plot(tiempo, senal, color=COLOR_DATOS, lw=1.6, label="señal original")
    ejes[0].step(tiempo, cuantizada, color=COLOR_PESOS, lw=1.6, where="mid",
                 label=f"cuantizada, {niveles} niveles")
    for nivel in np.arange(-1, 1.01, 2 / niveles):
        ejes[0].axhline(nivel, color="#c8ccd2", lw=0.6, ls=":")
    ejes[0].set_title("Cuantizador escalar\n(un eje, cuantos uniformes)")
    ejes[0].set_xlabel("$t$")
    ejes[0].set_ylabel("amplitud")
    ejes[0].legend(fontsize=8, loc="upper right")

    generador = np.random.default_rng(13)
    nube = np.concatenate([
        np.array([-1.0, 0.8]) + generador.normal(0, 0.22, (250, 2)),
        np.array([1.0, 0.6]) + generador.normal(0, 0.16, (250, 2)),
        np.array([0.2, -0.9]) + generador.normal(0, 0.30, (250, 2)),
    ])

    ejes[1].scatter(nube[:, 0], nube[:, 1], s=8, c=COLOR_DATOS, alpha=0.5)
    for linea in np.linspace(-2, 2, 9):
        ejes[1].axvline(linea, color=COLOR_VECINA, lw=0.8)
        ejes[1].axhline(linea, color=COLOR_VECINA, lw=0.8)
    ejes[1].set_title("Cuantización vectorial UNIFORME\n(la rejilla de una foto: 64 cuantos)")

    prototipos, _ = entrenar_som(
        nube, (1, 9), cantidad_de_epocas=120,
        tasa_inicial=0.4, tasa_final=0.01,
        radio_inicial=0.0, radio_final=0.0, semilla=31,
    )
    ejes[2].scatter(nube[:, 0], nube[:, 1], s=8, c=COLOR_DATOS, alpha=0.5)
    ejes[2].scatter(prototipos[:, 0], prototipos[:, 1], s=140, marker="*",
                    c=COLOR_PESOS, edgecolor="black", lw=0.5, zorder=5)
    for indice, prototipo in enumerate(prototipos):
        ejes[2].text(prototipo[0] + 0.07, prototipo[1] + 0.07, str(indice + 1),
                     fontsize=8, color=COLOR_PESOS)
    ejes[2].set_title("Cuantización vectorial ADAPTADA\n(9 prototipos aprendidos: el diccionario)")

    for eje in ejes[1:]:
        eje.set_xlim(-2, 2)
        eje.set_ylim(-2, 2)
        eje.set_aspect("equal")
        eje.set_xlabel("$x_1$")
        eje.grid(False)
    ejes[1].set_ylabel("$x_2$")
    figura.tight_layout()
    guardar(figura, "11-cuantizacion.png")


# ---------------------------------------------------------------------------
# 12. LVQ1: los dos casos gráficos
# ---------------------------------------------------------------------------


def figura_12_lvq1_grafico():
    figura, ejes = plt.subplots(1, 2, figsize=(10.5, 4.6))

    prototipo = np.array([0.0, 0.0])
    patron = np.array([1.4, 0.7])
    alfa = 0.35

    generador = np.random.default_rng(19)
    nube_a = np.array([1.6, 0.9]) + generador.normal(0, 0.30, (60, 2))
    nube_b = np.array([-1.2, -0.6]) + generador.normal(0, 0.30, (60, 2))

    escenarios = [
        (+1, "Acertó: $\\mathcal{C}(c(n)) = d(n)$, $s = +1$\nel prototipo se ACERCA", COLOR_ACENTO),
        (-1, "Erró: $\\mathcal{C}(c(n)) \\neq d(n)$, $s = -1$\nel prototipo se ALEJA", COLOR_NARANJA),
    ]
    for eje, (signo, titulo, color) in zip(ejes, escenarios):
        eje.scatter(nube_a[:, 0], nube_a[:, 1], s=12, c=COLOR_VECINA, alpha=0.35,
                    label="clase A (a la que pertenece $\\mathbf{x}(n)$)")
        eje.scatter(nube_b[:, 0], nube_b[:, 1], s=12, c=COLOR_NARANJA, alpha=0.35,
                    label="clase B")
        nuevo = prototipo + signo * alfa * (patron - prototipo)
        eje.scatter(*patron, s=110, marker="X", c="black", zorder=6)
        eje.text(patron[0] + 0.10, patron[1] + 0.10, r"$\mathbf{x}(n)$", fontsize=10)
        eje.scatter(*prototipo, s=140, marker="*", facecolor="white",
                    edgecolor=COLOR_PESOS, lw=2, zorder=6)
        eje.text(prototipo[0] - 0.55, prototipo[1] - 0.05, r"$\mathbf{m}_c(n)$",
                 fontsize=10, color=COLOR_PESOS)
        eje.scatter(*nuevo, s=160, marker="*", c=COLOR_PESOS, zorder=6)
        eje.text(nuevo[0] - 0.10, nuevo[1] - 0.40, r"$\mathbf{m}_c(n+1)$",
                 fontsize=10, color=COLOR_PESOS, ha="center")
        eje.add_patch(FancyArrowPatch(prototipo, patron, arrowstyle="->",
                                      color="#8a8f98", lw=1.2, ls=":",
                                      mutation_scale=12, zorder=4))
        eje.text((prototipo[0] + patron[0]) / 2 - 0.15,
                 (prototipo[1] + patron[1]) / 2 + 0.18,
                 r"$\mathbf{x}-\mathbf{m}_c$", fontsize=9, color="#6f7681")
        eje.add_patch(FancyArrowPatch(prototipo, nuevo, arrowstyle="-|>",
                                      color=color, lw=2.4, mutation_scale=16, zorder=5))
        eje.set_title(titulo, color=color)
        eje.set_xlim(-2.2, 2.4)
        eje.set_ylim(-1.8, 1.9)
        eje.set_aspect("equal")
        eje.set_xlabel("$x_1$")
        eje.grid(True, alpha=0.3, ls=":")
        eje.legend(fontsize=7.5, loc="lower right")
    ejes[0].set_ylabel("$x_2$")
    figura.tight_layout()
    guardar(figura, "12-lvq1-grafico.png")


def figura_13_lvq1_frontera():
    """LVQ1 corriendo de verdad: cómo se mueven los prototipos y qué frontera arman."""
    generador = np.random.default_rng(23)
    nube_a = np.concatenate([
        np.array([-1.3, 0.9]) + generador.normal(0, 0.35, (150, 2)),
        np.array([-1.0, -1.1]) + generador.normal(0, 0.35, (150, 2)),
    ])
    nube_b = np.array([1.2, 0.1]) + generador.normal(0, 0.50, (300, 2))
    patrones = np.concatenate([nube_a, nube_b])
    clases = np.concatenate([np.zeros(len(nube_a), int), np.ones(len(nube_b), int)])

    prototipos = generador.uniform(-0.5, 0.5, size=(4, 2))
    clases_de_prototipo = np.array([0, 0, 1, 1])
    prototipos_iniciales = prototipos.copy()

    alfa = 0.30
    cantidad_de_epocas = 40
    historia_de_error = []
    for epoca in range(cantidad_de_epocas):
        orden = generador.permutation(len(patrones))
        errores = 0
        for indice in orden:
            patron, clase = patrones[indice], clases[indice]
            ganador = int(np.argmin(np.sum((prototipos - patron) ** 2, axis=1)))
            signo = +1 if clases_de_prototipo[ganador] == clase else -1
            if signo == -1:
                errores += 1
            prototipos[ganador] += signo * alfa * (patron - prototipos[ganador])
        historia_de_error.append(errores / len(patrones))
        alfa *= 0.92

    figura, (ejes_espacio, ejes_error) = plt.subplots(
        1, 2, figsize=(11.0, 4.6), gridspec_kw={"width_ratios": [1.25, 1]}
    )

    rejilla_x, rejilla_y = np.meshgrid(np.linspace(-3, 3, 400), np.linspace(-3, 3, 400))
    puntos = np.stack([rejilla_x.ravel(), rejilla_y.ravel()], axis=1)
    ganadores = np.argmin(
        ((puntos[:, None, :] - prototipos[None, :, :]) ** 2).sum(axis=2), axis=1
    )
    prediccion = clases_de_prototipo[ganadores].reshape(rejilla_x.shape)
    ejes_espacio.contourf(rejilla_x, rejilla_y, prediccion, levels=[-0.5, 0.5, 1.5],
                          colors=["#2a78d6", "#eb6834"], alpha=0.10)
    ejes_espacio.contour(rejilla_x, rejilla_y, prediccion, levels=[0.5],
                         colors=["#4a4f57"], linewidths=1.4)

    ejes_espacio.scatter(nube_a[:, 0], nube_a[:, 1], s=10, c=COLOR_VECINA, alpha=0.40,
                         label="clase A")
    ejes_espacio.scatter(nube_b[:, 0], nube_b[:, 1], s=10, c=COLOR_NARANJA, alpha=0.40,
                         label="clase B")
    for inicial, final, clase in zip(prototipos_iniciales, prototipos, clases_de_prototipo):
        color = COLOR_VECINA if clase == 0 else COLOR_NARANJA
        ejes_espacio.annotate("", xy=final, xytext=inicial,
                              arrowprops=dict(arrowstyle="->", color="#4a4f57",
                                              lw=1.0, ls=":"))
        ejes_espacio.scatter(*inicial, s=80, marker="o", facecolor="white",
                             edgecolor=color, lw=1.6, zorder=5)
        ejes_espacio.scatter(*final, s=170, marker="*", c=color, edgecolor="black",
                             lw=0.6, zorder=6)
    ejes_espacio.set_title("LVQ1 con 2 prototipos por clase\n"
                           "(círculo: inicio; estrella: final)")
    ejes_espacio.set_xlabel("$x_1$")
    ejes_espacio.set_ylabel("$x_2$")
    ejes_espacio.set_xlim(-3, 3)
    ejes_espacio.set_ylim(-3, 3)
    ejes_espacio.set_aspect("equal")
    ejes_espacio.legend(fontsize=8, loc="upper left")
    ejes_espacio.grid(True, alpha=0.25, ls=":")

    ejes_error.plot(np.arange(1, cantidad_de_epocas + 1),
                    100 * np.array(historia_de_error), color=COLOR_PESOS, lw=1.8)
    ejes_error.set_xlabel("época")
    ejes_error.set_ylabel("error de clasificación [%]")
    ejes_error.set_title(f"Error de entrenamiento\n(final: {100*historia_de_error[-1]:.1f} %)")
    ejes_error.grid(True, alpha=0.3, ls=":")
    figura.tight_layout()
    guardar(figura, "13-lvq1-frontera.png")
    return historia_de_error[0], historia_de_error[-1]


# ---------------------------------------------------------------------------
# 14. La velocidad de aprendizaje óptima de LVQ1-O
# ---------------------------------------------------------------------------


def figura_14_alfa_optimo():
    cantidad_de_pasos = 60
    alfa_inicial = 0.9

    # todos los signos +1 (el caso limpio) para poder comparar sin ruido
    alfa_optimo = np.empty(cantidad_de_pasos)
    alfa_optimo[0] = alfa_inicial
    for n in range(1, cantidad_de_pasos):
        alfa_optimo[n] = alfa_optimo[n - 1] / (1 + alfa_optimo[n - 1])

    alfa_constante = np.full(cantidad_de_pasos, 0.30)

    def pesos_efectivos(alfas):
        """Cuánto pesa cada patrón x(k) en el centroide final m(N)."""
        cantidad = len(alfas)
        pesos = np.empty(cantidad)
        for k in range(cantidad):
            factor = alfas[k]
            for j in range(k + 1, cantidad):
                factor *= (1 - alfas[j])
            pesos[k] = factor
        return pesos

    pesos_optimos = pesos_efectivos(alfa_optimo)
    pesos_constantes = pesos_efectivos(alfa_constante)

    figura, (ejes_alfa, ejes_peso) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    pasos = np.arange(1, cantidad_de_pasos + 1)
    ejes_alfa.plot(pasos, alfa_optimo, color=COLOR_PESOS, lw=2.0,
                   label=r"$\alpha_c(n) = \frac{\alpha_c(n-1)}{1+s(n)\alpha_c(n-1)}$")
    ejes_alfa.plot(pasos, alfa_constante, color=COLOR_VECINA, lw=1.8, ls="--",
                   label=r"$\alpha = 0{,}30$ constante")
    ejes_alfa.plot(pasos, alfa_inicial / (1 + alfa_inicial * (pasos - 1)),
                   color="black", lw=1.0, ls=":",
                   label=r"forma cerrada $\frac{\alpha_0}{1+\alpha_0 (n-1)}$")
    ejes_alfa.set_xlabel("iteración $n$")
    ejes_alfa.set_ylabel(r"$\alpha_c(n)$")
    ejes_alfa.set_title(r"La regla óptima hace decaer $\alpha$ como $1/n$")
    ejes_alfa.legend(fontsize=8)
    ejes_alfa.grid(True, alpha=0.3, ls=":")

    ejes_peso.plot(pasos, pesos_optimos, color=COLOR_PESOS, lw=2.0, marker="o",
                   markersize=2.5, label=r"con $\alpha_c(n)$ óptimo")
    ejes_peso.plot(pasos, pesos_constantes, color=COLOR_VECINA, lw=1.8, ls="--",
                   label=r"con $\alpha$ constante")
    ejes_peso.axhline(1 / cantidad_de_pasos, color="black", lw=0.9, ls=":",
                      label=f"$1/N = {1/cantidad_de_pasos:.4f}$")
    ejes_peso.set_xlabel("índice $k$ del patrón mostrado")
    ejes_peso.set_ylabel("peso de $\\mathbf{x}(k)$ en $\\mathbf{m}_c$ final")
    ejes_peso.set_title("Con la regla óptima todos los patrones\npesan exactamente lo mismo")
    ejes_peso.set_yscale("log")
    ejes_peso.legend(fontsize=8, loc="lower right")
    ejes_peso.grid(True, alpha=0.3, ls=":", which="both")
    figura.tight_layout()
    guardar(figura, "14-alfa-optimo.png")

    return alfa_optimo, pesos_optimos, pesos_constantes


# ---------------------------------------------------------------------------


def main():
    figura_01_arquitectura()
    figura_02_vecindades()
    figura_03_funciones_laterales()
    pesos_r1, media_izquierda, media_derecha = figura_04_ejemplo_r1()
    error_maximo = figura_05_ejemplo_r2_sin_entorno()
    resumen_entorno = figura_06_efecto_del_entorno()
    figura_07_despliegue()
    conteos_de_cruces = figura_08_sin_ordenamiento()
    figura_09_etapas()
    exactitud, neuronas_muertas = figura_10_etiquetado()
    figura_11_cuantizacion()
    figura_12_lvq1_grafico()
    error_inicial, error_final = figura_13_lvq1_frontera()
    alfa_optimo, pesos_optimos, pesos_constantes = figura_14_alfa_optimo()

    print()
    print("=" * 62)
    print("NÚMEROS QUE VAN AL APUNTE")
    print("=" * 62)
    print(f"Ejemplo R1: w1={pesos_r1[0]:.4f} w2={pesos_r1[1]:.4f}")
    print(f"            medias reales: {media_izquierda:.4f} / {media_derecha:.4f}")
    print(f"Ejemplo R2 sin entorno: peor error peso-centro = {error_maximo:.4f}")
    print(f"Efecto del entorno (30 semillas): {resumen_entorno}")
    print(f"Cruces de la malla: {conteos_de_cruces}")
    print(f"Etiquetado: exactitud={exactitud:.4f}  neuronas sin etiqueta={neuronas_muertas}")
    print(f"LVQ1: error inicial={error_inicial:.4f}  final={error_final:.4f}")
    print(f"alfa optimo: n=1 -> {alfa_optimo[0]:.4f}, n=2 -> {alfa_optimo[1]:.4f}, "
          f"n=3 -> {alfa_optimo[2]:.4f}, n=10 -> {alfa_optimo[9]:.4f}")
    print(f"pesos efectivos con alfa optimo: min={pesos_optimos.min():.6f} "
          f"max={pesos_optimos.max():.6f} (relacion {pesos_optimos.max()/pesos_optimos.min():.6f})")
    print(f"pesos efectivos con alfa constante: primero={pesos_constantes[0]:.3e} "
          f"ultimo={pesos_constantes[-1]:.3e} "
          f"(relacion {pesos_constantes[-1]/pesos_constantes[0]:.3e})")


if __name__ == "__main__":
    main()
