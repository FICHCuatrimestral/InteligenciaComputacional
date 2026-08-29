"""
Figuras del apunte: redes neuronales dinamicas.
Inteligencia Computacional - FICH-UNL

Cuatro bloques de diapositivas no tienen dibujo (las tres aproximaciones, los
campos energeticos, la arquitectura TDNN) o lo tienen ilegible (Elman/Jordan):
el profesor dibujaba en el pizarron. Se reconstruyen desde las transcripciones
026 a 031.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

SUPERFICIE       = "#fcfcfb"
TINTA_PRIMARIA   = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
COLOR_CLASE_A    = "#2a78d6"   # azul
COLOR_CLASE_B    = "#eb6834"   # naranja
COLOR_ACENTO     = "#1baf7a"   # aqua
COLOR_GRILLA     = "#d8d7d2"

plt.rcParams.update({
    "figure.facecolor":  SUPERFICIE,
    "axes.facecolor":    SUPERFICIE,
    "savefig.facecolor": SUPERFICIE,
    "font.size":         10,
    "text.color":        TINTA_PRIMARIA,
    "axes.labelcolor":   TINTA_PRIMARIA,
    "xtick.color":       TINTA_SECUNDARIA,
    "ytick.color":       TINTA_SECUNDARIA,
})

DESTINO = __file__.rsplit("/", 1)[0]


def guardar(figura, nombre):
    figura.savefig(f"{DESTINO}/{nombre}", dpi=170, bbox_inches="tight")
    plt.close(figura)
    print("escrita:", nombre)


def limpiar(ejes, color_marco="none"):
    ejes.set_xticks([]); ejes.set_yticks([])
    for lado in ejes.spines.values():
        lado.set_color(color_marco)


def caja(ejes, centro, ancho, alto, texto, color=TINTA_SECUNDARIA,
         relleno="white", tamano=9.5, alfa=1.0):
    ejes.add_patch(FancyBboxPatch((centro[0] - ancho / 2, centro[1] - alto / 2),
                                  ancho, alto, boxstyle="round,pad=0.04",
                                  linewidth=1.4, edgecolor=color,
                                  facecolor=relleno, alpha=alfa, zorder=3))
    ejes.text(*centro, texto, ha="center", va="center", fontsize=tamano,
              zorder=4, color=TINTA_PRIMARIA)


def flecha(ejes, desde, hasta, color=TINTA_SECUNDARIA, ancho=1.3,
           estilo="-|>", curva=0.0, guiones=None):
    parche = FancyArrowPatch(desde, hasta, arrowstyle=estilo, mutation_scale=12,
                             color=color, linewidth=ancho, zorder=2,
                             connectionstyle=f"arc3,rad={curva}",
                             shrinkA=0, shrinkB=0)
    if guiones:
        parche.set_linestyle(guiones)
    ejes.add_patch(parche)


# ============================================================ FIGURA 01
def figura_tres_aproximaciones():
    """Diapositivas 3 a 6: las ecuaciones estan, los diagramas los dibujo el."""
    figura, paneles = plt.subplots(1, 3, figsize=(13.0, 3.6))
    titulos = [
        "1. Entradas desplazadas\n$y(n)=f(\\mathbf{x}(n))$",
        "2. Realimentación de las salidas\n$y(n)=f(\\mathbf{x}(n),\\mathbf{y}_1(n))$",
        "3. Realimentación de estados internos\n$y(n)=f(\\mathbf{x}(n),\\mathbf{z}_1(n))$",
    ]
    for ejes in paneles:
        ejes.set_xlim(0, 10); ejes.set_ylim(0, 7.4); limpiar(ejes)

    # --- panel 1: entradas desplazadas
    ejes = paneles[0]
    caja(ejes, (5.8, 3.6), 2.6, 2.6, "red\nestática", COLOR_CLASE_A)
    for altura, etiqueta in [(5.0, "$\\mathbf{x}(n)$"), (3.6, "$\\mathbf{x}(n-1)$"),
                             (2.2, "$\\mathbf{x}(n-2)$")]:
        ejes.text(1.5, altura, etiqueta, ha="center", va="center", fontsize=9.5)
        flecha(ejes, (2.9, altura), (4.5, altura))
    for altura in (4.35, 2.95):
        caja(ejes, (2.9, altura), 0.62, 0.62, "$z^{-1}$", COLOR_CLASE_B, tamano=8)
        flecha(ejes, (2.9, altura + 0.31), (2.9, altura - 0.31), COLOR_CLASE_B, 1.0)
    flecha(ejes, (7.1, 3.6), (8.9, 3.6))
    ejes.text(9.3, 3.6, "$y(n)$", ha="center", va="center", fontsize=9.5)
    ejes.text(5.0, 0.7, "la red no cambia: sólo\nrecibe más entradas",
              ha="center", fontsize=8.6, color=TINTA_SECUNDARIA, style="italic")

    # --- panel 2: realimentacion de salidas
    ejes = paneles[1]
    caja(ejes, (5.4, 4.6), 2.8, 2.2, "red\nestática", COLOR_CLASE_A)
    ejes.text(1.1, 5.2, "$\\mathbf{x}(n)$", ha="center", va="center", fontsize=9.5)
    flecha(ejes, (1.9, 5.2), (4.0, 5.2))
    flecha(ejes, (6.8, 4.6), (8.6, 4.6))
    ejes.text(9.3, 4.6, "$y(n)$", ha="center", va="center", fontsize=9.5)
    caja(ejes, (5.4, 1.9), 0.72, 0.72, "$z^{-1}$", COLOR_CLASE_B, tamano=8)
    flecha(ejes, (7.7, 4.6), (7.7, 1.9), COLOR_CLASE_B, 1.2, estilo="-")
    flecha(ejes, (7.7, 1.9), (5.76, 1.9), COLOR_CLASE_B, 1.2)
    flecha(ejes, (5.04, 1.9), (2.6, 1.9), COLOR_CLASE_B, 1.2, estilo="-")
    flecha(ejes, (2.6, 1.9), (2.6, 4.1), COLOR_CLASE_B, 1.2, estilo="-")
    flecha(ejes, (2.6, 4.1), (4.0, 4.1), COLOR_CLASE_B, 1.2)
    ejes.text(5.0, 0.7, "vuelve $y(n-1)$ como entrada",
              ha="center", fontsize=8.6, color=TINTA_SECUNDARIA, style="italic")

    # --- panel 3: realimentacion de estados internos
    ejes = paneles[2]
    caja(ejes, (5.4, 4.6), 2.8, 2.2, "", COLOR_CLASE_A)
    for altura in (5.25, 4.6, 3.95):
        ejes.add_patch(Circle((5.4, altura), 0.17, facecolor=COLOR_ACENTO,
                              alpha=0.35, edgecolor=COLOR_ACENTO,
                              linewidth=1.0, zorder=5))
    ejes.text(6.35, 5.9, "$\\mathbf{z}(n)$: estado interno", ha="center",
              fontsize=8.4, color=COLOR_ACENTO)
    ejes.text(1.1, 5.2, "$\\mathbf{x}(n)$", ha="center", va="center", fontsize=9.5)
    flecha(ejes, (1.9, 5.2), (4.0, 5.2))
    flecha(ejes, (6.8, 4.6), (8.6, 4.6))
    ejes.text(9.3, 4.6, "$y(n)$", ha="center", va="center", fontsize=9.5)
    caja(ejes, (5.4, 1.9), 0.72, 0.72, "$z^{-1}$", COLOR_ACENTO, tamano=8)
    flecha(ejes, (5.4, 3.5), (5.4, 2.26), COLOR_ACENTO, 1.2, estilo="-")
    flecha(ejes, (5.04, 1.9), (2.6, 1.9), COLOR_ACENTO, 1.2, estilo="-")
    flecha(ejes, (2.6, 1.9), (2.6, 4.1), COLOR_ACENTO, 1.2, estilo="-")
    flecha(ejes, (2.6, 4.1), (4.0, 4.1), COLOR_ACENTO, 1.2)
    ejes.text(5.0, 0.7, "vuelve el estado interno:\nacá la red ya es dinámica",
              ha="center", fontsize=8.6, color=COLOR_ACENTO, style="italic")

    for ejes, titulo in zip(paneles, titulos):
        ejes.set_title(titulo, fontsize=9.8, color=TINTA_SECUNDARIA, pad=6)
    guardar(figura, "01-tres-aproximaciones.png")


# ============================================================ FIGURA 02
def figura_clasificacion():
    """Diapositivas 7 a 10, como arbol."""
    figura, ejes = plt.subplots(figsize=(11.0, 4.4))
    ejes.set_xlim(0, 12); ejes.set_ylim(0, 6.2); limpiar(ejes)

    caja(ejes, (1.5, 3.1), 2.4, 0.85, "DNN", COLOR_CLASE_A, tamano=10.5)
    caja(ejes, (4.9, 5.2), 3.0, 0.75, "TDNN\n(retardos)", COLOR_CLASE_B, tamano=8.8)
    caja(ejes, (4.9, 2.2), 3.0, 0.75, "RNN (recurrentes)", COLOR_CLASE_B, tamano=8.8)
    flecha(ejes, (2.7, 3.35), (3.4, 5.2), COLOR_GRILLA, 1.2, estilo="-")
    flecha(ejes, (2.7, 2.85), (3.4, 2.2), COLOR_GRILLA, 1.2, estilo="-")

    caja(ejes, (8.6, 3.3), 3.2, 0.7, "totalmente recurrentes",
         TINTA_SECUNDARIA, tamano=8.5)
    caja(ejes, (8.6, 1.1), 3.2, 0.7, "parcialmente recurrentes (PRNN)",
         TINTA_SECUNDARIA, tamano=8.0)
    flecha(ejes, (6.4, 2.35), (7.0, 3.3), COLOR_GRILLA, 1.2, estilo="-")
    flecha(ejes, (6.4, 2.05), (7.0, 1.1), COLOR_GRILLA, 1.2, estilo="-")

    ejes.text(10.5, 4.05, "• Hopfield  (memorias asociativas)\n"
                          "• Boltzmann  (supervisadas)\n• ART",
              fontsize=8.4, va="top", color=TINTA_SECUNDARIA)
    ejes.text(10.5, 0.95, "• BPTT\n• Elman\n• Jordan",
              fontsize=8.4, va="top", color=TINTA_SECUNDARIA)
    ejes.text(4.9, 4.35, "se entrenan con los\nalgoritmos que ya sabemos",
              fontsize=8.2, ha="center", color=COLOR_ACENTO, style="italic")
    guardar(figura, "02-clasificacion.png")


# ============================================================ FIGURA 03
def figura_hopfield_arquitectura():
    """Diapositiva 12, redibujada legible."""
    figura, ejes = plt.subplots(figsize=(8.6, 4.6))
    ejes.set_xlim(0, 11); ejes.set_ylim(0, 6.6); limpiar(ejes)
    alturas = [5.0, 3.3, 1.6]

    for indice, altura in enumerate(alturas, start=1):
        ejes.add_patch(Circle((5.2, altura), 0.42, facecolor=COLOR_CLASE_A,
                              alpha=0.16, edgecolor=COLOR_CLASE_A,
                              linewidth=1.6, zorder=5))
        ejes.text(5.2, altura, f"${indice}$", ha="center", va="center",
                  fontsize=10, zorder=6, color=COLOR_CLASE_A)
        ejes.text(1.5, altura, f"$x_{indice}$", ha="center", va="center", fontsize=10)
        flecha(ejes, (2.0, altura), (4.78, altura))
        flecha(ejes, (5.62, altura), (8.3, altura))
        ejes.text(8.75, altura, f"$y_{indice}$", ha="center", va="center", fontsize=10)

    # realimentaciones: de cada salida a las OTRAS dos neuronas, con retardo
    canales = {1: 9.55, 2: 10.1, 3: 10.65}
    for origen, altura_origen in zip((1, 2, 3), alturas):
        x_canal = canales[origen]
        flecha(ejes, (8.3, altura_origen), (x_canal, altura_origen),
               COLOR_CLASE_B, 1.0, estilo="-")
        flecha(ejes, (x_canal, altura_origen), (x_canal, 6.2), COLOR_CLASE_B, 1.0, estilo="-")
        flecha(ejes, (x_canal, 6.2), (3.6 - 0.35 * origen, 6.2), COLOR_CLASE_B, 1.0, estilo="-")
        destino_bajo = min(a for i, a in zip((1, 2, 3), alturas) if i != origen)
        flecha(ejes, (3.6 - 0.35 * origen, 6.2), (3.6 - 0.35 * origen, destino_bajo),
               COLOR_CLASE_B, 1.0, estilo="-")
        for indice_destino, altura_destino in zip((1, 2, 3), alturas):
            if indice_destino == origen:
                continue
            flecha(ejes, (3.6 - 0.35 * origen, altura_destino), (4.78, altura_destino),
                   COLOR_CLASE_B, 1.0)
    caja(ejes, (9.9, 0.55), 1.5, 0.6, "$z^{-1}$", COLOR_CLASE_B, tamano=9)
    ejes.text(9.9, 0.02, "todas las vueltas\npasan por un retardo", ha="center",
              va="top", fontsize=8, color=COLOR_CLASE_B, style="italic")
    ejes.text(1.9, 0.55, "$w_{ji}=w_{ij}$   y   $w_{ii}=0$", fontsize=10,
              color=TINTA_PRIMARIA)
    ejes.text(1.9, 0.02, "tantas neuronas como entradas y como salidas", fontsize=8.4,
              va="top", color=TINTA_SECUNDARIA, style="italic")
    guardar(figura, "03-hopfield-arquitectura.png")


# ============================================================ FIGURA 04
def figura_hebb_tres_casos():
    """Los tres casos que analiza en la clase 028."""
    figura, paneles = plt.subplots(1, 3, figsize=(11.6, 3.3))
    generador = np.random.default_rng(3)
    cantidad = 14
    casos = [
        ("Siempre iguales", "$w_{ji}$ grande y positivo", COLOR_ACENTO,
         lambda: (lambda s: (s, s))(generador.choice([-1, 1], cantidad))),
        ("Siempre opuestas", "$w_{ji}$ grande y negativo", COLOR_CLASE_B,
         lambda: (lambda s: (s, -s))(generador.choice([-1, 1], cantidad))),
        ("Sin relación", "$w_{ji} \\approx 0$", TINTA_SECUNDARIA,
         lambda: (generador.choice([-1, 1], cantidad),
                  generador.choice([-1, 1], cantidad))),
    ]
    for ejes, (titulo, pie, color, generar) in zip(paneles, casos):
        a, b = generar()
        indices = np.arange(cantidad)
        ejes.scatter(indices, np.full(cantidad, 1.6), s=90,
                     c=[COLOR_CLASE_A if v > 0 else "white" for v in a],
                     edgecolor=COLOR_CLASE_A, linewidth=1.2, zorder=3)
        ejes.scatter(indices, np.full(cantidad, 0.7), s=90,
                     c=[COLOR_CLASE_A if v > 0 else "white" for v in b],
                     edgecolor=COLOR_CLASE_A, linewidth=1.2, zorder=3)
        productos = a * b
        for x, p in zip(indices, productos):
            ejes.text(x, 0.05, "$+$" if p > 0 else "$-$", ha="center",
                      fontsize=9, color=color)
        ejes.text(-1.5, 1.6, "$x^*_{kj}$", ha="center", va="center", fontsize=9.5)
        ejes.text(-1.5, 0.7, "$x^*_{ki}$", ha="center", va="center", fontsize=9.5)
        ejes.text(-1.5, 0.05, "prod.", ha="center", va="center", fontsize=8,
                  color=TINTA_SECUNDARIA)
        ejes.set_title(f"{titulo}\n{pie}", fontsize=9.6, color=color)
        ejes.set_xlim(-2.6, cantidad); ejes.set_ylim(-0.5, 2.2); limpiar(ejes)
    guardar(figura, "04-hebb-tres-casos.png")


# ============================================================ FIGURA 06
def figura_campos_energeticos():
    """Diapositiva 29, que tiene dos vinetas y ningun dibujo."""
    figura, ejes = plt.subplots(figsize=(9.6, 4.2))
    x = np.linspace(0, 10, 900)

    def valle(centro, ancho, profundidad):
        return -profundidad * np.exp(-((x - centro) ** 2) / (2 * ancho ** 2))

    energia = (2.0 + valle(1.9, 0.62, 1.7) + valle(5.2, 0.62, 1.9)
               + valle(8.4, 0.62, 1.6) + valle(3.6, 0.34, 0.55))
    ejes.plot(x, energia, color=TINTA_SECUNDARIA, linewidth=2.0, zorder=2)

    for centro, etiqueta in [(1.9, "$\\mathbf{x}^*_1$"), (5.2, "$\\mathbf{x}^*_2$"),
                             (8.4, "$\\mathbf{x}^*_3$")]:
        indice = np.argmin(np.abs(x - centro))
        ejes.scatter(x[indice], energia[indice], s=80, color=COLOR_ACENTO,
                     zorder=6, linewidth=0)
        ejes.annotate(etiqueta, (x[indice], energia[indice]), xytext=(0, -22),
                      textcoords="offset points", ha="center", fontsize=10,
                      color=COLOR_ACENTO)
    indice_espurio = np.argmin(np.abs(x - 3.6))
    ejes.scatter(x[indice_espurio], energia[indice_espurio], s=80,
                 color=COLOR_CLASE_B, zorder=6, linewidth=0)
    ejes.annotate("estado espúreo", (x[indice_espurio], energia[indice_espurio]),
                  xytext=(-86, 40), textcoords="offset points", fontsize=9,
                  color=COLOR_CLASE_B,
                  arrowprops=dict(arrowstyle="->", color=COLOR_CLASE_B,
                                  linewidth=1.0, shrinkB=6))

    # dos recuperaciones: una que llega, otra que se traba
    for inicio, color, etiqueta, destino in [
            (6.35, COLOR_CLASE_A, "$\\mathbf{y}(0)=\\mathbf{x}$", 5.2),
            (4.35, COLOR_CLASE_B, "otro $\\mathbf{y}(0)$", 3.6)]:
        camino = np.linspace(inicio, destino, 7)
        alturas = np.interp(camino, x, energia)
        ejes.plot(camino, alturas + 0.09, "o--", color=color, markersize=4.5,
                  linewidth=1.3, zorder=5)
        ejes.annotate(etiqueta, (inicio, np.interp(inicio, x, energia)),
                      xytext=(26, 14), textcoords="offset points", ha="left",
                      fontsize=9, color=color)

    ejes.set_ylabel("energía", fontsize=9.5)
    ejes.set_xlabel("espacio de estados $\\mathbf{y}$", fontsize=9.5, labelpad=10)
    ejes.set_ylim(energia.min() - 0.55, energia.max() + 0.45)
    ejes.set_title("El almacenamiento cava los valles; la recuperación baja por uno",
                   fontsize=10, color=TINTA_SECUNDARIA)
    limpiar(ejes, COLOR_GRILLA)
    guardar(figura, "06-campos-energeticos.png")


# ============================================================ FIGURA 05
def figura_recuperacion():
    """El proceso iterativo: se elige una neurona al azar y se recalcula."""
    generador = np.random.default_rng(12)
    lado = 8
    limpio = np.ones((lado, lado)) * -1
    limpio[2:6, 2] = 1; limpio[2, 2:6] = 1; limpio[5, 2:6] = 1; limpio[2:6, 5] = 1
    ruidoso = limpio.copy()
    posiciones = generador.choice(lado * lado, 14, replace=False)
    ruidoso.flat[posiciones] *= -1

    pasos = [ruidoso]
    actual = ruidoso.copy()
    for fraccion in (0.45, 0.8, 1.0):
        siguiente = actual.copy()
        diferentes = np.flatnonzero(siguiente != limpio)
        cuantos = int(len(diferentes) * fraccion)
        siguiente.flat[diferentes[:cuantos]] = limpio.flat[diferentes[:cuantos]]
        pasos.append(siguiente)
        actual = siguiente

    titulos = ["$\\mathbf{y}(0)=\\mathbf{x}$\n(ruidoso)", "algunas iteraciones",
               "más iteraciones", "$\\mathbf{y}(M)$: no cambia nada\n(memoria fundamental)"]
    figura, paneles = plt.subplots(1, 4, figsize=(11.4, 3.2))
    for ejes, matriz, titulo in zip(paneles, pasos, titulos):
        ejes.imshow(matriz, cmap="Blues", vmin=-1.6, vmax=1.4)
        ejes.set_xticks(np.arange(-0.5, lado, 1), minor=True)
        ejes.set_yticks(np.arange(-0.5, lado, 1), minor=True)
        ejes.grid(which="minor", color=SUPERFICIE, linewidth=1.4)
        ejes.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
        ejes.set_title(titulo, fontsize=9.2, color=TINTA_SECUNDARIA)
    guardar(figura, "05-recuperacion.png")


# ============================================================ FIGURA 07
def figura_desenrollado():
    """La red recurrente y su version desplegada en el tiempo (clase 030)."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(12.4, 3.9),
                                      gridspec_kw={"width_ratios": [1, 2.5]})
    for ejes in (izq, der):
        limpiar(ejes)

    # --- izquierda: la red con recurrencia total
    izq.set_xlim(0, 6); izq.set_ylim(0, 5.4)
    for altura, indice in [(3.6, 1), (1.6, 2)]:
        izq.add_patch(Circle((3.2, altura), 0.42, facecolor=COLOR_CLASE_A,
                             alpha=0.16, edgecolor=COLOR_CLASE_A,
                             linewidth=1.6, zorder=5))
        izq.text(3.2, altura, f"${indice}$", ha="center", va="center",
                 fontsize=10, zorder=6, color=COLOR_CLASE_A)
        izq.text(0.7, altura, f"$x_{indice}(n)$", ha="center", va="center", fontsize=9)
        flecha(izq, (1.5, altura), (2.78, altura))
        flecha(izq, (3.62, altura), (4.7, altura))
        izq.text(5.3, altura, f"$y_{indice}(n)$", ha="center", va="center", fontsize=9)
    # recurrencias: propias y cruzadas
    for altura in (3.6, 1.6):
        flecha(izq, (3.2, altura + 0.42), (3.2, altura + 0.42), COLOR_CLASE_B, 1.2)
        izq.add_patch(FancyArrowPatch((2.95, altura + 0.40), (3.45, altura + 0.40),
                                      connectionstyle="arc3,rad=-1.9",
                                      arrowstyle="-|>", mutation_scale=10,
                                      color=COLOR_CLASE_B, linewidth=1.2, zorder=4))
    izq.add_patch(FancyArrowPatch((3.55, 3.30), (3.55, 1.90),
                                  connectionstyle="arc3,rad=-0.65", arrowstyle="-|>",
                                  mutation_scale=10, color=COLOR_CLASE_B,
                                  linewidth=1.2, zorder=4))
    izq.add_patch(FancyArrowPatch((2.85, 1.90), (2.85, 3.30),
                                  connectionstyle="arc3,rad=-0.65", arrowstyle="-|>",
                                  mutation_scale=10, color=COLOR_CLASE_B,
                                  linewidth=1.2, zorder=4))
    izq.text(3.2, 0.35, "todas con todas,\ny cada una consigo misma", ha="center",
             fontsize=8.4, color=COLOR_CLASE_B, style="italic")
    izq.set_title("Recurrencia total", fontsize=10, color=TINTA_SECUNDARIA)

    # --- derecha: desenrollada
    der.set_xlim(0, 15); der.set_ylim(0, 5.4)
    columnas = [2.2, 5.6, 9.0, 12.4]
    etiquetas = ["$t-3$", "$t-2$", "$t-1$", "$t$"]
    for columna, etiqueta in zip(columnas, etiquetas):
        for altura, indice in [(3.5, 1), (1.7, 2)]:
            der.add_patch(Circle((columna, altura), 0.34, facecolor=COLOR_CLASE_A,
                                 alpha=0.16, edgecolor=COLOR_CLASE_A,
                                 linewidth=1.3, zorder=5))
        der.text(columna, 0.55, etiqueta, ha="center", fontsize=9,
                 color=TINTA_SECUNDARIA)
        der.annotate("", xy=(columna, 4.55), xytext=(columna, 3.5 + 0.34),
                     arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                     linewidth=1.0))
        der.annotate("", xy=(columna, 1.7 - 0.34), xytext=(columna, 1.05),
                     arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                     linewidth=1.0))
    der.text(0.55, 4.55, "$\\mathbf{y}_t$", ha="center", va="center", fontsize=9.5)
    der.text(0.55, 1.05, "$\\mathbf{x}_t$", ha="center", va="center", fontsize=9.5)
    for izquierda, derecha in zip(columnas, columnas[1:]):
        for altura_origen in (3.5, 1.7):
            for altura_destino in (3.5, 1.7):
                flecha(der, (izquierda + 0.34, altura_origen),
                       (derecha - 0.34, altura_destino), COLOR_CLASE_B, 1.0)
    der.text(7.3, 5.15, "los pesos $\\mathbf{W}$ son los MISMOS en cada paso",
             ha="center", fontsize=9, color=COLOR_CLASE_B)
    der.text(14.3, 2.6, "$\\dots$", fontsize=12, color=TINTA_SECUNDARIA)
    der.set_title("Desenrollada en el tiempo: ya es sólo hacia adelante",
                  fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "07-desenrollado.png")


# ============================================================ FIGURA 08
def figura_aportes():
    """Los dos aportes al gradiente en t=1 (grafico de las notas, ampliado)."""
    figura, ejes = plt.subplots(figsize=(9.2, 3.6))
    ejes.set_xlim(0, 12); ejes.set_ylim(0, 5.2); limpiar(ejes)

    for columna, etiqueta in [(3.4, "$t=0$"), (7.2, "$t=1$")]:
        ejes.text(columna, 4.75, etiqueta, ha="center", fontsize=10,
                  color=TINTA_SECUNDARIA)
        ejes.add_patch(Circle((columna, 2.6), 0.42, facecolor=COLOR_CLASE_A,
                              alpha=0.16, edgecolor=COLOR_CLASE_A,
                              linewidth=1.5, zorder=5))
        ejes.text(columna, 2.6, "$\\varphi$", ha="center", va="center",
                  fontsize=10, zorder=6, color=COLOR_CLASE_A)
    ejes.text(1.0, 2.6, "$y_{-1}$", ha="center", va="center", fontsize=10)
    flecha(ejes, (1.5, 2.6), (2.98, 2.6), COLOR_CLASE_B, 1.6)
    ejes.text(2.24, 3.0, "$w$", ha="center", fontsize=10, color=COLOR_CLASE_B)
    flecha(ejes, (3.82, 2.6), (6.78, 2.6), COLOR_CLASE_B, 1.6)
    ejes.text(5.3, 3.0, "$w$", ha="center", fontsize=10, color=COLOR_CLASE_B)
    ejes.text(5.3, 2.15, "$y_0$", ha="center", fontsize=9.5, color=TINTA_SECUNDARIA)
    for columna, etiqueta in [(3.4, "$x_0$"), (7.2, "$x_1$")]:
        ejes.text(columna, 0.85, etiqueta, ha="center", fontsize=9.5)
        flecha(ejes, (columna, 1.15), (columna, 2.18), TINTA_SECUNDARIA, 1.1)
    flecha(ejes, (7.62, 2.6), (9.4, 2.6), TINTA_SECUNDARIA, 1.4)
    ejes.text(9.8, 2.6, "$y_1$", ha="center", va="center", fontsize=10)
    ejes.text(11.2, 2.6, "$e_1$", ha="center", va="center", fontsize=10,
              color=COLOR_CLASE_B)
    flecha(ejes, (10.2, 2.6), (10.9, 2.6), TINTA_SECUNDARIA, 1.2)

    ejes.annotate("aporte directo: el $w$ que actúa en $t=1$",
                  (5.3, 3.15), xytext=(5.3, 4.35), ha="center", fontsize=9,
                  color=COLOR_ACENTO,
                  arrowprops=dict(arrowstyle="->", color=COLOR_ACENTO, linewidth=1.2))
    ejes.annotate("aporte indirecto: el mismo $w$, actuando en $t=0$",
                  (2.24, 2.15), xytext=(3.0, 0.25), ha="center", fontsize=9,
                  color=COLOR_CLASE_B,
                  arrowprops=dict(arrowstyle="->", color=COLOR_CLASE_B, linewidth=1.2))
    ejes.set_title("$w_{0,ji}$ y $w_{1,ji}$ son el MISMO peso: los dos aportes se suman",
                   fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "08-aportes.png")


# ============================================================ FIGURA 09
def figura_delta_hacia_atras():
    """Como el delta de t+1 vuelve a la neurona j de t por las N conexiones."""
    figura, ejes = plt.subplots(figsize=(8.4, 3.8))
    ejes.set_xlim(0, 11); ejes.set_ylim(0, 5.6); limpiar(ejes)

    ejes.add_patch(Circle((2.6, 2.8), 0.46, facecolor=COLOR_CLASE_A, alpha=0.16,
                          edgecolor=COLOR_CLASE_A, linewidth=1.6, zorder=5))
    ejes.text(2.6, 2.8, "$\\varphi_j$", ha="center", va="center", fontsize=10,
              zorder=6, color=COLOR_CLASE_A)
    ejes.text(2.6, 1.95, "$y_{\\tau,j}$", ha="center", fontsize=9.5,
              color=TINTA_SECUNDARIA)
    ejes.text(0.7, 2.8, "$v_{\\tau,j}$", ha="center", va="center", fontsize=10)
    flecha(ejes, (1.2, 2.8), (2.14, 2.8))

    alturas = [4.5, 3.3, 2.1, 0.9]
    nombres = ["$\\varphi_1$", "$\\varphi_k$", "$\\varphi_{k'}$", "$\\varphi_N$"]
    subindices = ["1", "k", "k'", "N"]
    for altura, nombre, sub in zip(alturas, nombres, subindices):
        ejes.add_patch(Circle((6.6, altura), 0.40, facecolor=COLOR_CLASE_B,
                              alpha=0.16, edgecolor=COLOR_CLASE_B,
                              linewidth=1.4, zorder=5))
        ejes.text(6.6, altura, nombre, ha="center", va="center", fontsize=9,
                  zorder=6, color=COLOR_CLASE_B)
        flecha(ejes, (3.02, 3.02), (6.24, altura + 0.16), COLOR_GRILLA, 1.2)
        flecha(ejes, (6.24, altura - 0.16), (3.02, 2.58), COLOR_CLASE_B, 1.3,
               guiones=(0, (3, 2)))
        ejes.text(8.7, altura, f"$\\delta_{{\\tau+1,{sub}}}$", ha="center",
                  va="center", fontsize=9, color=COLOR_CLASE_B)
        flecha(ejes, (8.1, altura), (7.06, altura), COLOR_CLASE_B, 1.2)
    ejes.text(4.7, 4.95, "hacia adelante: $w_{jk}$", fontsize=9,
              color=TINTA_SECUNDARIA, ha="center")
    ejes.text(4.7, 0.25, "hacia atrás: $\\sum_k w_{jk}\\,\\delta_{\\tau+1,k}$",
              fontsize=9.5, color=COLOR_CLASE_B, ha="center")
    ejes.text(1.4, 4.6, "$\\tau$", fontsize=10, color=TINTA_SECUNDARIA)
    ejes.text(6.6, 5.25, "$\\tau+1$", fontsize=10, color=TINTA_SECUNDARIA, ha="center")
    guardar(figura, "09-delta-hacia-atras.png")


# ============================================================ FIGURA 10
def figura_tdnn():
    """Diapositiva 36, completamente vacia. Reconstruida desde la clase 031."""
    figura, ejes = plt.subplots(figsize=(10.6, 5.0))
    ejes.set_xlim(0, 14.5); ejes.set_ylim(0, 8.0); limpiar(ejes)

    def bloque(centro, ancho, alto, color, relleno):
        ejes.add_patch(Rectangle((centro[0] - ancho / 2, centro[1] - alto / 2),
                                 ancho, alto, facecolor=relleno, edgecolor=color,
                                 linewidth=1.4, zorder=4))

    # --- entradas retardadas
    etiquetas = ["$\\mathbf{x}(n)$", "$\\mathbf{x}(n\\!-\\!1)$", "$\\mathbf{x}(n\\!-\\!2)$"]
    alturas_entrada = [6.4, 4.2, 2.0]
    for indice, (altura, etiqueta) in enumerate(zip(alturas_entrada, etiquetas)):
        bloque((3.0, altura), 0.55, 0.95, TINTA_PRIMARIA, TINTA_PRIMARIA)
        ejes.text(2.45, altura, etiqueta, ha="right", va="center", fontsize=8.8)
        flecha(ejes, (3.35, altura), (5.75, 4.2), COLOR_CLASE_B, 1.2)
        ejes.text(4.3, altura + (0.42 if indice == 0 else (0.30 if indice == 1 else -0.55)),
                  f"$\\mathbf{{W}}^{{I}}_{{{indice}}}$", fontsize=8.8,
                  color=COLOR_CLASE_B, ha="center")
    for altura in (5.3, 3.1):
        caja(ejes, (3.0, altura), 0.66, 0.52, "$z^{-1}$", COLOR_CLASE_B, tamano=7.5)
        flecha(ejes, (3.0, altura + 0.72), (3.0, altura + 0.28), COLOR_CLASE_B, 1.0)
        flecha(ejes, (3.0, altura - 0.28), (3.0, altura - 0.72), COLOR_CLASE_B, 1.0)

    # --- capa 1
    bloque((6.1, 4.2), 0.72, 2.4, COLOR_CLASE_A, "#dbe7f7")
    ejes.text(6.1, 5.75, "capa 1", ha="center", fontsize=9, color=COLOR_CLASE_A)

    # --- salida de capa 1, actual y retardada
    flecha(ejes, (6.46, 4.2), (10.24, 4.2), COLOR_ACENTO, 1.2)
    ejes.text(8.3, 4.45, "$\\mathbf{z}(n)$", ha="center", fontsize=8.6,
              color=COLOR_ACENTO)
    caja(ejes, (7.3, 2.5), 0.66, 0.52, "$z^{-1}$", COLOR_ACENTO, tamano=7.5)
    flecha(ejes, (6.7, 3.6), (7.3, 2.78), COLOR_ACENTO, 1.1)
    bloque((8.9, 2.0), 0.55, 1.3, COLOR_ACENTO, "#d6f0e6")
    ejes.text(8.9, 1.15, "$\\mathbf{z}(n\\!-\\!1)$", ha="center", fontsize=8.6,
              color=COLOR_ACENTO)
    flecha(ejes, (7.63, 2.4), (8.6, 2.0), COLOR_ACENTO, 1.1)
    flecha(ejes, (9.2, 2.2), (10.24, 3.6), COLOR_ACENTO, 1.2)

    # --- capa 2 y salida
    bloque((10.6, 4.2), 0.72, 2.4, COLOR_CLASE_A, "#dbe7f7")
    ejes.text(10.6, 5.75, "capa 2", ha="center", fontsize=9, color=COLOR_CLASE_A)
    flecha(ejes, (10.96, 4.2), (12.8, 4.2), TINTA_SECUNDARIA, 1.4)
    bloque((13.2, 4.2), 0.55, 1.3, COLOR_CLASE_A, "#dbe7f7")
    ejes.text(13.2, 3.25, "salida", ha="center", fontsize=8.8, color=COLOR_CLASE_A)

    ejes.text(7.6, 7.55, "retardos en la ENTRADA", fontsize=9.5,
              color=COLOR_CLASE_B, ha="center")
    ejes.text(7.6, 7.10, "y también en la salida de CADA CAPA", fontsize=9.5,
              color=COLOR_ACENTO, ha="center")
    ejes.text(7.6, 0.45, "se entrena con back-propagation, igual que un MLP:\n"
                         "sólo hay más conjuntos de pesos", fontsize=8.8,
              ha="center", va="top", color=TINTA_SECUNDARIA, style="italic")
    guardar(figura, "10-tdnn.png")


# ============================================================ FIGURA 11
def figura_memoria_de_memoria():
    """La idea de la clase 031: cada capa ve una memoria mas larga."""
    figura, ejes = plt.subplots(figsize=(8.0, 3.4))
    ejes.set_xlim(0, 10); ejes.set_ylim(0, 4.6); limpiar(ejes)
    niveles = [
        (1.4, 9, "entrada", "instantes sueltos", TINTA_SECUNDARIA),
        (4.6, 5, "capa 1", "memoria corta:\nve 3 instantes", COLOR_CLASE_B),
        (7.2, 3, "capa 2", "memoria de la memoria", COLOR_ACENTO),
        (9.2, 1, "salida", "memoria larga", COLOR_CLASE_A),
    ]
    for x, cantidad, titulo, pie, color in niveles:
        alturas = np.linspace(3.5, 3.5 - 0.32 * (cantidad - 1), cantidad)
        for altura in alturas:
            ejes.add_patch(Rectangle((x - 0.32, altura - 0.13), 0.64, 0.26,
                                     facecolor=color, alpha=0.35,
                                     edgecolor=color, linewidth=1.0, zorder=4))
        ejes.text(x, 1.05, titulo, ha="center", fontsize=9, color=color)
        ejes.text(x, 0.65, pie, ha="center", va="top", fontsize=8,
                  color=TINTA_SECUNDARIA)
    for (x1, *_), (x2, *_) in zip(niveles, niveles[1:]):
        flecha(ejes, (x1 + 0.45, 2.6), (x2 - 0.45, 2.6), COLOR_GRILLA, 1.4)
    ejes.set_title("Clasificación espacio-temporal: la memoria se alarga con cada capa",
                   fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "11-memoria-de-memoria.png")


# ============================================================ FIGURA 12
def figura_elman_jordan():
    """Diapositivas 38 y 39, redibujadas legibles."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(10.4, 4.0))

    def red(ejes, titulo, desde_capa_oculta):
        ejes.set_xlim(0, 10); ejes.set_ylim(0, 7.0); limpiar(ejes)
        color = COLOR_ACENTO if desde_capa_oculta else COLOR_CLASE_B
        for altura, nombre in [(1.3, "entrada"), (3.5, "capa oculta"), (5.7, "salida")]:
            ejes.add_patch(Rectangle((2.0, altura - 0.28), 3.4, 0.56,
                                     facecolor=TINTA_PRIMARIA, edgecolor="none",
                                     zorder=4))
            ejes.text(1.7, altura, nombre, ha="right", va="center", fontsize=9,
                      color=TINTA_SECUNDARIA)
        flecha(ejes, (3.2, 1.6), (3.2, 3.2), TINTA_SECUNDARIA, 1.4)
        flecha(ejes, (3.2, 3.8), (3.2, 5.4), TINTA_SECUNDARIA, 1.4)
        ejes.text(2.95, 2.4, "$\\omega$", fontsize=9.5, ha="right")
        ejes.text(2.95, 4.6, "$\\omega$", fontsize=9.5, ha="right")

        altura_origen = 3.5 if desde_capa_oculta else 5.7
        ejes.add_patch(Rectangle((6.8, 1.3 - 0.28), 2.2, 0.56,
                                 facecolor=color, alpha=0.45, edgecolor=color,
                                 linewidth=1.3, zorder=4))
        ejes.text(7.9, 0.65, "contexto", ha="center", fontsize=8.6, color=color)
        flecha(ejes, (5.4, altura_origen), (7.9, altura_origen), color, 1.3, estilo="-")
        flecha(ejes, (7.9, altura_origen), (7.9, 1.6), color, 1.3)
        caja(ejes, (7.9, 3.1), 0.66, 0.5, "$z^{-1}$", color, tamano=8)
        flecha(ejes, (6.8, 1.3), (5.4, 1.3), color, 1.3)
        ejes.text(6.1, 1.62, "$1$", fontsize=9, ha="center", color=color)
        ejes.set_title(titulo, fontsize=10.5, color=TINTA_PRIMARIA)

    red(izq, "Elman: realimenta la capa oculta", True)
    red(der, "Jordan: realimenta la salida", False)
    guardar(figura, "12-elman-jordan.png")


if __name__ == "__main__":
    figura_tres_aproximaciones()
    figura_clasificacion()
    figura_hopfield_arquitectura()
    figura_hebb_tres_casos()
    figura_recuperacion()
    figura_campos_energeticos()
    figura_desenrollado()
    figura_aportes()
    figura_delta_hacia_atras()
    figura_tdnn()
    figura_memoria_de_memoria()
    figura_elman_jordan()


# ============================================================ FIGURA 13
def figura_energia_del_ejemplo():
    """La traza del ejemplo a mano: la energia baja en escalones y se queda."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 3.3),
                                      gridspec_kw={"width_ratios": [1.15, 1]})

    x1 = np.array([1, 1, 1, 1, -1, -1, -1, -1])
    ruidoso = x1.copy(); ruidoso[[1, 6]] *= -1
    intermedio = ruidoso.copy(); intermedio[6] = -1
    tiras = [("$\\mathbf{y}(0)$: ruidoso", ruidoso),
             ("tras corregir $y_7$", intermedio),
             ("$\\mathbf{y}(M) = \\mathbf{x}^*_1$", x1)]
    for fila, (etiqueta, tira) in enumerate(tiras):
        for columna, valor in enumerate(tira):
            distinto = valor != x1[columna]
            izq.add_patch(Rectangle((columna, -fila), 0.9, 0.9,
                                    facecolor=COLOR_CLASE_A if valor > 0 else "white",
                                    edgecolor=COLOR_CLASE_B if distinto else COLOR_GRILLA,
                                    linewidth=2.2 if distinto else 1.0, zorder=3))
        izq.text(-0.4, -fila + 0.45, etiqueta, ha="right", va="center", fontsize=9)
    izq.set_xlim(-5.6, 8.4); izq.set_ylim(-2.3, 1.1); limpiar(izq)
    izq.set_title("Dos bits dados vuelta, y cómo se corrigen",
                  fontsize=10, color=TINTA_SECUNDARIA)

    pasos = [0, 1, 2, 3, 4, 5, 6]
    energias = [-1.0, -1.5, -1.5, -3.0, -3.0, -3.0, -3.0]
    der.step(pasos, energias, where="post", color=COLOR_CLASE_A, linewidth=2.0)
    der.scatter(pasos, energias, s=34, color=COLOR_CLASE_A, zorder=4, linewidth=0)
    for paso, etiqueta in [(1, "cambia $y_7$"), (3, "cambia $y_2$")]:
        der.annotate(etiqueta, (paso, energias[paso]), xytext=(8, 16),
                     textcoords="offset points", fontsize=8.6, color=COLOR_CLASE_B,
                     arrowprops=dict(arrowstyle="->", color=COLOR_CLASE_B, linewidth=1.0))
    der.axhline(-3.0, color=COLOR_ACENTO, linestyle=":", linewidth=1.4)
    der.text(6.0, -2.86, "energía de $\\mathbf{x}^*_1$", ha="right", fontsize=8.6,
             color=COLOR_ACENTO)
    der.set_xlabel("iteración"); der.set_ylabel("$E$")
    der.set_ylim(-3.5, -0.5)
    der.set_title("Nunca sube: baja en escalones y se queda",
                  fontsize=10, color=TINTA_SECUNDARIA)
    limpiar(der, COLOR_GRILLA)
    der.set_xticks(pasos); der.set_xticklabels([str(p) for p in pasos], fontsize=8)
    der.set_yticks([-3, -2, -1]); der.set_yticklabels(["$-3$", "$-2$", "$-1$"], fontsize=8)
    guardar(figura, "13-energia-del-ejemplo.png")
