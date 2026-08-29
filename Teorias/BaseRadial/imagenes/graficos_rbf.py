"""
Figuras del apunte: redes neuronales con funciones de base radial.
Inteligencia Computacional - FICH-UNL

Varias diapositivas de la catedra estan vacias (solo el titulo): el profesor
dibujaba en el pizarron. Las figuras 01, 02, 03, 05, 10 y 11 reconstruyen esos
dibujos a partir de la descripcion hablada en las transcripciones 015 y 017.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch

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
    ruta = f"{DESTINO}/{nombre}"
    figura.savefig(ruta, dpi=170, bbox_inches="tight")
    plt.close(figura)
    print("escrita:", nombre)


def limpiar(ejes, color_marco=COLOR_GRILLA):
    ejes.set_xticks([]); ejes.set_yticks([])
    for lado in ejes.spines.values():
        lado.set_color(color_marco)


def sigmoide(v, b=1.0):
    return 2.0 / (1.0 + np.exp(-b * v)) - 1.0


def gaussiana(X, Y, mu, sigma):
    return np.exp(-((X - mu[0]) ** 2 + (Y - mu[1]) ** 2) / (2 * sigma ** 2))


# ============================================================ FIGURA 01
def figura_papel_doblado():
    """El 'papel doblado': como se ve una sigmoide en 3D y como dos de ellas
    forman la franja del XOR. Reconstruye las diapositivas 2-4, vacias."""
    figura = plt.figure(figsize=(11.0, 3.9))
    rejilla = np.linspace(-2.2, 2.2, 120)
    X, Y = np.meshgrid(rejilla, rejilla)

    paneles = [
        ("Una sigmoide: un papel doblado",  sigmoide(2.4 * (X + 0.9))),
        ("La otra, corrida",                sigmoide(-2.4 * (X - 0.9))),
        ("Las dos juntas: la franja",       np.minimum(sigmoide(2.4 * (X + 0.9)),
                                                       sigmoide(-2.4 * (X - 0.9)))),
    ]
    for indice, (titulo, Z) in enumerate(paneles, start=1):
        ejes = figura.add_subplot(1, 3, indice, projection="3d")
        ejes.plot_surface(X, Y, Z, cmap="Blues", edgecolor="none",
                          alpha=0.92, rstride=3, cstride=3)
        ejes.set_title(titulo, fontsize=10, color=TINTA_SECUNDARIA, pad=0)
        ejes.set_xlabel("$x_1$", labelpad=-8, fontsize=9)
        ejes.set_ylabel("$x_2$", labelpad=-8, fontsize=9)
        ejes.set_zlim(-1.15, 1.15)
        ejes.set_xticks([]); ejes.set_yticks([]); ejes.set_zticks([-1, 1])
        ejes.set_zticklabels(["$-1$", "$+1$"], fontsize=8)
        ejes.view_init(elev=26, azim=-58)
        ejes.set_box_aspect((1, 1, 0.62))
    guardar(figura, "01-papel-doblado.png")


# ============================================================ FIGURA 02
def figura_sigmoide_vs_radial():
    """Slide 4 y 5, ambas vacias: 'Funciones sigmoideas' / 'Funciones radiales'."""
    figura = plt.figure(figsize=(9.2, 3.9))
    rejilla = np.linspace(-3, 3, 130)
    X, Y = np.meshgrid(rejilla, rejilla)

    ejes = figura.add_subplot(1, 2, 1, projection="3d")
    ejes.plot_surface(X, Y, sigmoide(2.0 * X), cmap="Blues", edgecolor="none",
                      alpha=0.93, rstride=3, cstride=3)
    ejes.set_title("Sigmoidea: separa dos mitades\ndel espacio, sin frontera lejana",
                   fontsize=10, color=TINTA_SECUNDARIA, pad=-2)

    ejes2 = figura.add_subplot(1, 2, 2, projection="3d")
    ejes2.plot_surface(X, Y, gaussiana(X, Y, (0, 0), 0.85), cmap="Oranges",
                       edgecolor="none", alpha=0.93, rstride=3, cstride=3)
    ejes2.set_title("Radial: encierra una zona\nacotada alrededor de un centro",
                    fontsize=10, color=TINTA_SECUNDARIA, pad=-2)

    for e in (ejes, ejes2):
        e.set_xlabel("$x_1$", labelpad=-8, fontsize=9)
        e.set_ylabel("$x_2$", labelpad=-8, fontsize=9)
        e.set_xticks([]); e.set_yticks([]); e.set_zticks([])
        e.view_init(elev=24, azim=-60)
        e.set_box_aspect((1, 1, 0.6))
    guardar(figura, "02-sigmoide-vs-radial.png")


# ============================================================ FIGURA 03
def figura_regiones_radiales():
    """Slide 6: el XOR resuelto encerrando cada clase con circulos."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(9.0, 4.3))
    puntos = [(-1, -1, "B"), (-1, +1, "A"), (+1, -1, "A"), (+1, +1, "B")]

    def dibujar_puntos(ejes):
        for x1, x2, clase in puntos:
            color = COLOR_CLASE_A if clase == "A" else COLOR_CLASE_B
            ejes.scatter([x1], [x2], s=150, color=color, zorder=5,
                         edgecolor=SUPERFICIE, linewidth=1.5)
            etiqueta = "$+1$" if clase == "A" else "$-1$"
            desplazamiento = 16 if x2 > 0 else -26
            ejes.annotate(etiqueta, (x1, x2), textcoords="offset points",
                          xytext=(0, desplazamiento), ha="center",
                          fontsize=11, color=color)
        ejes.axhline(0, color=COLOR_GRILLA, linewidth=1.0, zorder=0)
        ejes.axvline(0, color=COLOR_GRILLA, linewidth=1.0, zorder=0)
        ejes.set_xlim(-2.1, 2.1); ejes.set_ylim(-2.1, 2.1)
        ejes.set_aspect("equal")
        ejes.set_xlabel("$x_1$"); ejes.set_ylabel("$x_2$")
        limpiar(ejes)

    dibujar_puntos(izq)
    for corrimiento, estilo in [(-0.85, "--"), (0.85, "--")]:
        izq.plot([-2.1, 2.1], [-2.1 + corrimiento * 2, 2.1 + corrimiento * 2],
                 estilo, color=TINTA_SECUNDARIA, linewidth=1.6)
    izq.set_title("Con rectas: hacen falta dos,\ny una tercera que las combine",
                  fontsize=10, color=TINTA_SECUNDARIA)

    dibujar_puntos(der)
    for centro in [(-1, 1), (1, -1)]:
        der.add_patch(Circle(centro, 0.72, facecolor=COLOR_CLASE_A, alpha=0.16,
                             edgecolor=COLOR_CLASE_A, linewidth=1.8, zorder=1))
    der.set_title("Con radiales: un circulo por clase,\ny la salida los suma",
                  fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "03-regiones-radiales.png")


# ============================================================ FIGURA 04
def figura_suma_de_gaussianas():
    """Slide 10: la aproximacion p(x) = suma de w_j phi(||x - mu_j||)."""
    figura = plt.figure(figsize=(6.6, 4.4))
    ejes = figura.add_subplot(111, projection="3d")
    rejilla = np.linspace(0, 10, 150)
    X, Y = np.meshgrid(rejilla, rejilla)

    centros = [((2.0, 2.5), 1.0, 0.85), ((7.0, 7.0), 0.75, 1.10),
               ((5.5, 2.0), 0.55, 0.75), ((8.2, 3.0), 0.90, 0.70)]
    Z = np.zeros_like(X)
    for mu, peso, sigma in centros:
        Z += peso * gaussiana(X, Y, mu, sigma)

    ejes.plot_surface(X, Y, Z, cmap="Blues", edgecolor="none",
                      alpha=0.95, rstride=2, cstride=2)
    for (mx, my), peso, _ in centros:
        ejes.plot([mx, mx], [my, my], [0, 0], marker="o", markersize=4,
                  color=COLOR_CLASE_B)
    ejes.set_xlabel("$x_1$", fontsize=9, labelpad=-4)
    ejes.set_ylabel("$x_2$", fontsize=9, labelpad=-4)
    ejes.set_zlabel("$p(x)$", fontsize=9, labelpad=-6)
    ejes.tick_params(labelsize=7, pad=-2)
    ejes.set_zticks([0, 0.5, 1.0])
    ejes.view_init(elev=28, azim=-56)
    ejes.set_box_aspect((1, 1, 0.55))
    ejes.set_title("Cada pico es un centro $\\mu_j$; el peso $w_j$ le da la altura",
                   fontsize=10, color=TINTA_SECUNDARIA, pad=-4)
    guardar(figura, "04-suma-de-gaussianas.png")


# ============================================================ FIGURA 05
def figura_arquitectura():
    """Slides 11 y 12, vacias. La arquitectura tal como la describe la clase 015."""
    figura, ejes = plt.subplots(figsize=(9.4, 5.0))
    limpiar(ejes, "none")
    ejes.set_xlim(0, 10); ejes.set_ylim(0, 6.3)

    columna_entrada, columna_radial, columna_salida = 1.2, 4.6, 8.4
    entradas = [("$x_1$", 3.9), ("$x_2$", 2.3)]
    radiales = [4.7, 3.7, 2.7, 1.7]

    for etiqueta, altura in entradas:
        ejes.add_patch(Circle((columna_entrada, altura), 0.30, facecolor="white",
                              edgecolor=TINTA_SECUNDARIA, linewidth=1.4, zorder=4))
        ejes.text(columna_entrada, altura, etiqueta, ha="center", va="center",
                  fontsize=11, zorder=5)

    for indice, altura in enumerate(radiales, start=1):
        ejes.add_patch(Circle((columna_radial, altura), 0.36,
                              facecolor=COLOR_CLASE_B, alpha=0.16,
                              edgecolor=COLOR_CLASE_B, linewidth=1.6, zorder=4))
        ejes.text(columna_radial, altura, f"$\\varphi_{indice}$", ha="center",
                  va="center", fontsize=11, zorder=5, color=COLOR_CLASE_B)
        for _, altura_entrada in entradas:
            ejes.annotate("", xy=(columna_radial - 0.36, altura),
                          xytext=(columna_entrada + 0.30, altura_entrada),
                          arrowprops=dict(arrowstyle="-", color=COLOR_GRILLA,
                                          linewidth=1.0))

    ejes.add_patch(Circle((columna_salida, 3.2), 0.36, facecolor=COLOR_CLASE_A,
                          alpha=0.16, edgecolor=COLOR_CLASE_A, linewidth=1.6, zorder=4))
    ejes.text(columna_salida, 3.2, "$\\Sigma$", ha="center", va="center",
              fontsize=12, zorder=5, color=COLOR_CLASE_A)
    for indice, altura in enumerate(radiales, start=1):
        ejes.annotate("", xy=(columna_salida - 0.36, 3.2),
                      xytext=(columna_radial + 0.36, altura),
                      arrowprops=dict(arrowstyle="-", color=COLOR_CLASE_A,
                                      linewidth=1.2, alpha=0.65))
    ejes.text(6.45, 4.30, "$w_{k1}$", fontsize=10, color=COLOR_CLASE_A)
    ejes.text(6.45, 1.75, "$w_{k4}$", fontsize=10, color=COLOR_CLASE_A)

    # sesgo de la capa de salida
    ejes.add_patch(Circle((columna_radial, 5.75), 0.28, facecolor="white",
                          edgecolor=TINTA_SECUNDARIA, linewidth=1.2, zorder=4))
    ejes.text(columna_radial, 5.75, "$-1$", ha="center", va="center", fontsize=9, zorder=5)
    ejes.annotate("", xy=(columna_salida - 0.36, 3.2),
                  xytext=(columna_radial + 0.28, 5.75),
                  arrowprops=dict(arrowstyle="-", color=COLOR_CLASE_A,
                                  linewidth=1.2, alpha=0.65))
    ejes.text(6.5, 5.15, "$w_{k0}$", fontsize=10, color=COLOR_CLASE_A)

    ejes.annotate("", xy=(9.6, 3.2), xytext=(columna_salida + 0.36, 3.2),
                  arrowprops=dict(arrowstyle="->", color=TINTA_PRIMARIA, linewidth=1.4))
    ejes.text(9.65, 3.2, "$y_k$", fontsize=11, va="center")

    for x, texto in [(columna_entrada, "entradas"),
                     (columna_radial, "capa radial"),
                     (columna_salida, "salida lineal")]:
        ejes.text(x, 0.20, texto, ha="center", fontsize=9.5,
                  color=TINTA_SECUNDARIA, style="italic")

    ejes.text(2.55, 5.35, "pesos fijos en 1\n(no se entrenan)", fontsize=8.5,
              ha="center", color=TINTA_SECUNDARIA)
    ejes.text(4.6, 0.80, "sin sesgo; sus parametros\nson $\\mu_j$ y $\\sigma_j$", fontsize=8.5,
              ha="center", color=COLOR_CLASE_B)
    guardar(figura, "05-arquitectura.png")


def nube_de_patrones(semilla=3):
    generador = np.random.default_rng(semilla)
    centros_reales = [(1.2, 3.4), (4.2, 4.0), (3.0, 1.0)]
    grupos = [generador.normal(c, 0.52, size=(22, 2)) for c in centros_reales]
    return np.vstack(grupos)


# ============================================================ FIGURA 06
def figura_kmedias_por_lotes():
    """Los cuatro pasos del algoritmo por lotes (slides 26-29)."""
    patrones = nube_de_patrones()
    generador = np.random.default_rng(11)
    etiquetas = generador.integers(0, 3, size=len(patrones))   # reparto al azar
    colores = [COLOR_CLASE_A, COLOR_CLASE_B, COLOR_ACENTO]

    figura, paneles = plt.subplots(1, 4, figsize=(12.4, 3.4))
    titulos = ["1. Reparto al azar", "2. Centroides", "3. Reasignacion",
               "Converge: ya no hay cambios"]

    def dibujar(ejes, etiquetas, centroides, mostrar_centroides=True):
        for grupo in range(3):
            seleccion = patrones[etiquetas == grupo]
            ejes.scatter(seleccion[:, 0], seleccion[:, 1], s=22,
                         color=colores[grupo], alpha=0.75, linewidth=0)
        if mostrar_centroides:
            for grupo, centro in enumerate(centroides):
                ejes.scatter(*centro, s=180, marker="X", color=colores[grupo],
                             edgecolor=SUPERFICIE, linewidth=1.6, zorder=6)
        ejes.set_xlim(-0.4, 6.0); ejes.set_ylim(-0.7, 5.7)
        ejes.set_aspect("equal"); limpiar(ejes)

    def centroides_de(etiquetas):
        return np.array([patrones[etiquetas == g].mean(axis=0) for g in range(3)])

    dibujar(paneles[0], etiquetas, None, mostrar_centroides=False)
    centroides = centroides_de(etiquetas)
    dibujar(paneles[1], etiquetas, centroides)
    distancias = ((patrones[:, None, :] - centroides[None, :, :]) ** 2).sum(axis=2)
    etiquetas = distancias.argmin(axis=1)
    dibujar(paneles[2], etiquetas, centroides)
    for _ in range(30):
        centroides = centroides_de(etiquetas)
        distancias = ((patrones[:, None, :] - centroides[None, :, :]) ** 2).sum(axis=2)
        etiquetas = distancias.argmin(axis=1)
    dibujar(paneles[3], etiquetas, centroides_de(etiquetas))

    for ejes, titulo in zip(paneles, titulos):
        ejes.set_title(titulo, fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "06-kmedias-por-lotes.png")


# ============================================================ FIGURA 07
def figura_centroide_bien_y_mal():
    """El ejemplo que dibuja el profesor: el centroide en el medio minimiza J."""
    generador = np.random.default_rng(5)
    grupo = generador.normal((2.5, 2.5), 0.62, size=(14, 2))
    centro_bueno = grupo.mean(axis=0)
    centro_malo = np.array([4.4, 3.9])

    figura, (izq, der) = plt.subplots(1, 2, figsize=(8.8, 4.0))
    for ejes, centro, titulo, color in [
            (izq, centro_bueno, "Centroide en el medio", COLOR_ACENTO),
            (der, centro_malo,  "Centroide corrido",     COLOR_CLASE_B)]:
        for punto in grupo:
            ejes.plot([centro[0], punto[0]], [centro[1], punto[1]],
                      color=color, linewidth=0.9, alpha=0.55, zorder=1)
        ejes.scatter(grupo[:, 0], grupo[:, 1], s=26, color=COLOR_CLASE_A,
                     zorder=3, linewidth=0)
        ejes.scatter(*centro, s=200, marker="X", color=color, zorder=5,
                     edgecolor=SUPERFICIE, linewidth=1.6)
        suma = np.sqrt(((grupo - centro) ** 2).sum(axis=1)).sum()
        ejes.set_title(f"{titulo}\n$\\sum \\|x_\\ell - \\mu_j\\| = {suma:.1f}$",
                       fontsize=10, color=TINTA_SECUNDARIA)
        ejes.set_xlim(0.4, 5.2); ejes.set_ylim(0.4, 4.8)
        ejes.set_aspect("equal"); limpiar(ejes)
    guardar(figura, "07-centroide-bien-y-mal.png")


# ============================================================ FIGURA 08
def figura_kmedias_online():
    """El centroide ganador da un paso hacia el patron que acaba de entrar."""
    figura, ejes = plt.subplots(figsize=(6.4, 4.0))
    generador = np.random.default_rng(2)
    nube = generador.normal((2.2, 2.2), 0.55, size=(16, 2))
    ejes.scatter(nube[:, 0], nube[:, 1], s=24, color=COLOR_GRILLA, linewidth=0, zorder=1)

    patron = np.array([4.3, 3.4])
    mu_ganador = np.array([2.3, 2.2])
    mu_perdedor = np.array([1.0, 4.0])
    eta = 0.45
    mu_nuevo = mu_ganador + eta * (patron - mu_ganador)

    ejes.scatter(*patron, s=110, color=COLOR_CLASE_A, zorder=5, linewidth=0)
    ejes.annotate("$x_\\ell$", patron, xytext=(10, 6), textcoords="offset points",
                  fontsize=11, color=COLOR_CLASE_A)
    for centro, etiqueta, color in [(mu_ganador, "$\\mu_{j^*}(n)$", COLOR_CLASE_B),
                                    (mu_perdedor, "$\\mu_i(n)$", TINTA_SECUNDARIA)]:
        ejes.scatter(*centro, s=170, marker="X", color=color, zorder=5,
                     edgecolor=SUPERFICIE, linewidth=1.5)
        ejes.annotate(etiqueta, centro, xytext=(-14, -22),
                      textcoords="offset points", fontsize=10, color=color)

    ejes.plot([mu_ganador[0], patron[0]], [mu_ganador[1], patron[1]],
              linestyle=":", color=COLOR_CLASE_B, linewidth=1.3)
    ejes.plot([mu_perdedor[0], patron[0]], [mu_perdedor[1], patron[1]],
              linestyle=":", color=COLOR_GRILLA, linewidth=1.3)
    ejes.add_patch(FancyArrowPatch(tuple(mu_ganador), tuple(mu_nuevo),
                                   arrowstyle="-|>", mutation_scale=15,
                                   color=COLOR_ACENTO, linewidth=2.2, zorder=6))
    ejes.scatter(*mu_nuevo, s=170, marker="X", color=COLOR_ACENTO, zorder=6,
                 edgecolor=SUPERFICIE, linewidth=1.5)
    ejes.annotate("$\\mu_{j^*}(n+1)$", mu_nuevo, xytext=(-30, 16),
                  textcoords="offset points", fontsize=10, color=COLOR_ACENTO)
    ejes.text(3.05, 1.55, "$\\eta\\,(x_\\ell - \\mu_{j^*})$", fontsize=10,
              color=COLOR_ACENTO)
    ejes.set_title("Solo se mueve el ganador, y solo una fraccion $\\eta$ del camino",
                   fontsize=10, color=TINTA_SECUNDARIA)
    ejes.set_xlim(0.0, 5.4); ejes.set_ylim(0.6, 4.9)
    ejes.set_aspect("equal"); limpiar(ejes)
    guardar(figura, "08-kmedias-online.png")


# ============================================================ FIGURA 09
def figura_desdoblamiento():
    """La simplificacion de la clase 017: con la capa radial congelada, lo que
    queda es un perceptron simple con entradas phi_j."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 3.9))
    for ejes in (izq, der):
        ejes.set_xlim(0, 10); ejes.set_ylim(0, 6.0); limpiar(ejes, "none")

    # --- izquierda: la red completa, con la parte congelada sombreada
    izq.add_patch(FancyBboxPatch((0.5, 0.9), 4.6, 4.4,
                                 boxstyle="round,pad=0.15", linewidth=1.4,
                                 edgecolor=COLOR_CLASE_B, facecolor=COLOR_CLASE_B,
                                 alpha=0.10, zorder=0))
    izq.text(2.8, 5.55, "congelado tras la etapa 1", fontsize=9,
             ha="center", color=COLOR_CLASE_B, style="italic")
    for altura, etiqueta in [(3.8, "$x_1$"), (2.2, "$x_2$")]:
        izq.add_patch(Circle((1.4, altura), 0.32, facecolor="white",
                             edgecolor=TINTA_SECUNDARIA, linewidth=1.3, zorder=4))
        izq.text(1.4, altura, etiqueta, ha="center", va="center", fontsize=10, zorder=5)
    alturas_radiales = [4.5, 3.5, 2.5, 1.5]
    for indice, altura in enumerate(alturas_radiales, start=1):
        izq.add_patch(Circle((4.1, altura), 0.32, facecolor=COLOR_CLASE_B,
                             alpha=0.20, edgecolor=COLOR_CLASE_B, linewidth=1.3, zorder=4))
        izq.text(4.1, altura, f"$\\varphi_{indice}$", ha="center", va="center",
                 fontsize=9.5, zorder=5, color=COLOR_CLASE_B)
        for altura_entrada in (3.8, 2.2):
            izq.annotate("", xy=(4.1 - 0.32, altura), xytext=(1.4 + 0.32, altura_entrada),
                         arrowprops=dict(arrowstyle="-", color=COLOR_GRILLA, linewidth=0.9))
        izq.annotate("", xy=(7.9 - 0.32, 3.0), xytext=(4.1 + 0.32, altura),
                     arrowprops=dict(arrowstyle="-", color=COLOR_CLASE_A,
                                     linewidth=1.1, alpha=0.7))
    izq.add_patch(Circle((7.9, 3.0), 0.34, facecolor=COLOR_CLASE_A, alpha=0.18,
                         edgecolor=COLOR_CLASE_A, linewidth=1.4, zorder=4))
    izq.text(7.9, 3.0, "$\\Sigma$", ha="center", va="center", fontsize=11,
             zorder=5, color=COLOR_CLASE_A)
    izq.set_title("La red tal como es", fontsize=10, color=TINTA_SECUNDARIA)

    # --- derecha: el perceptron simple equivalente
    for indice, altura in enumerate(alturas_radiales, start=1):
        der.add_patch(Circle((2.6, altura), 0.34, facecolor="white",
                             edgecolor=COLOR_CLASE_B, linewidth=1.4, zorder=4))
        der.text(2.6, altura, f"$\\varphi_{indice}$", ha="center", va="center",
                 fontsize=9.5, zorder=5, color=COLOR_CLASE_B)
        der.annotate("", xy=(7.4 - 0.34, 3.0), xytext=(2.6 + 0.34, altura),
                     arrowprops=dict(arrowstyle="-", color=COLOR_CLASE_A,
                                     linewidth=1.2, alpha=0.75))
    der.add_patch(Circle((7.4, 3.0), 0.34, facecolor=COLOR_CLASE_A, alpha=0.18,
                         edgecolor=COLOR_CLASE_A, linewidth=1.4, zorder=4))
    der.text(7.4, 3.0, "$\\Sigma$", ha="center", va="center", fontsize=11,
             zorder=5, color=COLOR_CLASE_A)
    der.text(2.6, 0.75, "las nuevas entradas", fontsize=9, ha="center",
             color=COLOR_CLASE_B, style="italic")
    der.text(5.0, 5.3, "$w_{kj}$: lo unico que queda por entrenar",
             fontsize=9.5, ha="center", color=COLOR_CLASE_A)
    der.set_title("Como conviene pensarla: un perceptron simple con salida lineal",
                  fontsize=10, color=TINTA_SECUNDARIA)
    guardar(figura, "09-desdoblamiento.png")


# ============================================================ FIGURA 10
def figura_local_vs_global():
    """Slide 44, vacia. Representacion local (radial) contra global (sigmoidea)."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(9.0, 4.0))
    rejilla = np.linspace(-3, 3, 260)
    X, Y = np.meshgrid(rejilla, rejilla)

    izq.contourf(X, Y, sigmoide(2.2 * (0.8 * X + 0.6 * Y)), levels=24, cmap="Blues")
    izq.set_title("Hiperplano sigmoideo: parte el espacio\nen dos mitades infinitas",
                  fontsize=10, color=TINTA_SECUNDARIA)
    der.contourf(X, Y, gaussiana(X, Y, (0, 0), 0.9), levels=24, cmap="Oranges")
    der.set_title("Funcion radial: activa solo en una\nzona acotada del espacio",
                  fontsize=10, color=TINTA_SECUNDARIA)
    for ejes in (izq, der):
        ejes.set_aspect("equal"); limpiar(ejes)
        ejes.set_xlabel("$x_1$"); ejes.set_ylabel("$x_2$")
    guardar(figura, "10-local-vs-global.png")


# ============================================================ FIGURA 11
def figura_region_compleja():
    """Lo que dibuja en la clase 017: con suficientes gaussianas se arma
    cualquier region, por complicada que sea."""
    figura, paneles = plt.subplots(1, 3, figsize=(11.0, 3.7))
    rejilla = np.linspace(-0.2, 6.2, 300)
    X, Y = np.meshgrid(rejilla, rejilla)

    contorno = [(1.0, 1.0), (2.2, 1.3), (3.0, 2.4), (4.2, 2.0), (5.0, 3.0),
                (4.0, 4.2), (2.6, 4.0), (1.6, 3.0), (2.4, 2.6), (1.2, 2.2)]
    for ejes, cantidad in zip(paneles, [3, 6, 10]):
        centros = contorno[:cantidad]
        Z = np.zeros_like(X)
        for centro in centros:
            Z = np.maximum(Z, gaussiana(X, Y, centro, 0.62))
        ejes.contourf(X, Y, Z, levels=[0.5, 10], colors=[COLOR_CLASE_B], alpha=0.35)
        ejes.contour(X, Y, Z, levels=[0.5], colors=[COLOR_CLASE_B], linewidths=1.6)
        for centro in centros:
            ejes.scatter(*centro, s=26, color=COLOR_CLASE_B, zorder=4, linewidth=0)
        ejes.set_title(f"{cantidad} gaussianas", fontsize=10, color=TINTA_SECUNDARIA)
        ejes.set_xlim(-0.2, 6.2); ejes.set_ylim(-0.2, 5.4)
        ejes.set_aspect("equal"); limpiar(ejes)
    guardar(figura, "11-region-compleja.png")


# ============================================================ FIGURA 12
def figura_casos_de_covarianza():
    """Los cuatro casos de la clase 018, del mas simple al mas general."""
    figura, paneles = plt.subplots(1, 4, figsize=(12.6, 3.5))
    generador = np.random.default_rng(9)

    definiciones = [
        ("$\\mathbf{U}_j = \\mathbf{I}$",
         "circulos, todos del mismo tamano",
         [((1.6, 1.6), 0.8, 0.8, 0), ((3.6, 3.2), 0.8, 0.8, 0), ((2.0, 3.8), 0.8, 0.8, 0)]),
        ("$\\mathbf{U}_j = \\sigma_j^2\\,\\mathbf{I}$",
         "circulos de distinto tamano",
         [((1.6, 1.6), 1.15, 1.15, 0), ((3.7, 3.3), 0.55, 0.55, 0), ((2.0, 3.9), 0.8, 0.8, 0)]),
        ("$\\mathbf{U}_j$ diagonal ($\\sigma_{jk}$)",
         "elipses, pero alineadas a los ejes",
         [((1.6, 1.6), 1.5, 0.6, 0), ((3.7, 3.3), 0.5, 1.2, 0), ((2.0, 4.0), 1.0, 0.45, 0)]),
        ("$\\mathbf{U}_j$ completa",
         "elipses tambien rotadas",
         [((1.6, 1.6), 1.5, 0.6, 32), ((3.7, 3.3), 0.5, 1.2, -25), ((2.0, 4.0), 1.0, 0.45, 65)]),
    ]
    for ejes, (titulo, pie, elipses) in zip(paneles, definiciones):
        for (centro, ancho, alto, angulo) in elipses:
            ejes.add_patch(Ellipse(centro, 2 * ancho, 2 * alto, angle=angulo,
                                   facecolor=COLOR_CLASE_B, alpha=0.18,
                                   edgecolor=COLOR_CLASE_B, linewidth=1.6))
            ejes.scatter(*centro, s=22, color=COLOR_CLASE_B, zorder=4, linewidth=0)
        ejes.set_title(titulo, fontsize=10.5, color=TINTA_PRIMARIA, pad=8)
        ejes.set_xlabel(pie, fontsize=8.8, color=TINTA_SECUNDARIA)
        ejes.set_xlim(-0.5, 5.6); ejes.set_ylim(-0.5, 5.6)
        ejes.set_aspect("equal"); limpiar(ejes)
    guardar(figura, "12-casos-de-covarianza.png")


# ============================================================ FIGURA 13
def figura_sigma_desde_el_grupo():
    """Como se estima sigma_j una vez que k-medias dio el centroide."""
    generador = np.random.default_rng(4)
    apretado = generador.normal((1.7, 2.6), 0.28, size=(20, 2))
    disperso = generador.normal((4.6, 2.6), 0.85, size=(20, 2))

    figura, ejes = plt.subplots(figsize=(7.0, 3.1))
    for grupo, color in [(apretado, COLOR_CLASE_A), (disperso, COLOR_CLASE_B)]:
        centro = grupo.mean(axis=0)
        sigma = np.sqrt(((grupo - centro) ** 2).sum(axis=1).mean() / 2)
        ejes.scatter(grupo[:, 0], grupo[:, 1], s=26, color=color, linewidth=0, alpha=0.8)
        ejes.scatter(*centro, s=170, marker="X", color=color, zorder=5,
                     edgecolor=SUPERFICIE, linewidth=1.5)
        for factor, alfa in [(1, 0.30), (2, 0.14)]:
            ejes.add_patch(Circle(centro, factor * sigma, facecolor=color,
                                  alpha=alfa * 0.5, edgecolor=color,
                                  linewidth=1.2, zorder=1))
        ejes.annotate(f"$\\sigma_j \\approx {sigma:.2f}$", centro,
                      xytext=(-22, -46), textcoords="offset points",
                      fontsize=10, color=color)
    ejes.set_title("El mismo criterio da una gaussiana chica o grande\n"
                   "segun lo apretado que este el grupo",
                   fontsize=10, color=TINTA_SECUNDARIA)
    ejes.set_xlim(0.0, 7.2); ejes.set_ylim(0.1, 5.1)
    ejes.set_aspect("equal"); limpiar(ejes)
    guardar(figura, "13-sigma-desde-el-grupo.png")


if __name__ == "__main__":
    figura_papel_doblado()
    figura_sigmoide_vs_radial()
    figura_regiones_radiales()
    figura_suma_de_gaussianas()
    figura_arquitectura()
    figura_kmedias_por_lotes()
    figura_centroide_bien_y_mal()
    figura_kmedias_online()
    figura_desdoblamiento()
    figura_local_vs_global()
    figura_region_compleja()
    figura_casos_de_covarianza()
    figura_sigma_desde_el_grupo()
