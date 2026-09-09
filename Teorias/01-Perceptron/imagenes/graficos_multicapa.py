"""
Figuras del apunte: perceptrón multicapa (diapositivas 30-43).
Inteligencia Computacional - FICH-UNL
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, FancyArrowPatch, FancyBboxPatch

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


def generar_medialunas(cantidad_por_clase=60, semilla=7):
    """Dos medialunas entrelazadas, el ejemplo clásico de clases no convexas."""
    generador = np.random.default_rng(semilla)
    angulos = np.linspace(0, np.pi, cantidad_por_clase)
    ruido = 0.09

    luna_a = np.column_stack([np.cos(angulos), np.sin(angulos)])
    luna_b = np.column_stack([1 - np.cos(angulos), 0.5 - np.sin(angulos)])
    luna_a = luna_a + generador.normal(0, ruido, luna_a.shape)
    luna_b = luna_b + generador.normal(0, ruido, luna_b.shape)
    return luna_a, luna_b


# ============================================================ FIGURA 7
def figura_regiones_de_decision():
    """Tabla clásica: qué puede resolver cada arquitectura."""
    filas = ["Una capa", "Dos capas", "Tres capas"]
    columnas = ["Estructura", "Región de decisión", "Problema XOR",
                "Clases entrelazadas"]

    figura, ejes = plt.subplots(3, 4, figsize=(11.5, 8.6))
    puntos_xor = [(-1, -1, "B"), (-1, +1, "A"), (+1, -1, "A"), (+1, +1, "B")]
    luna_a, luna_b = generar_medialunas()

    def limpiar(ax):
        ax.set_xticks([]); ax.set_yticks([])
        for lado in ax.spines.values():
            lado.set_color(COLOR_GRILLA)
        ax.set_aspect("equal", adjustable="box")

    # ---------------------------------------------------- columna estructura
    def dibujar_estructura(ax, neuronas_por_capa):
        limpiar(ax)
        ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.15, 1.15)
        posiciones = []
        cantidad_capas = len(neuronas_por_capa)
        for indice_capa, cantidad in enumerate(neuronas_por_capa):
            x = indice_capa / max(cantidad_capas - 1, 1)
            alturas = np.linspace(0.5 - 0.11 * (cantidad - 1),
                                  0.5 + 0.11 * (cantidad - 1), cantidad)
            posiciones.append([(x, y) for y in alturas])
        for indice_capa in range(cantidad_capas - 1):
            for origen in posiciones[indice_capa]:
                for destino in posiciones[indice_capa + 1]:
                    ax.plot([origen[0], destino[0]], [origen[1], destino[1]],
                            color=COLOR_GRILLA, linewidth=0.9, zorder=1)
        for indice_capa, capa in enumerate(posiciones):
            es_entrada = (indice_capa == 0)
            for x, y in capa:
                ax.add_patch(Circle((x, y), 0.048, zorder=3,
                                    facecolor="#f0efec" if es_entrada else "#e4eefa",
                                    edgecolor=TINTA_SECUNDARIA if es_entrada else COLOR_CLASE_A,
                                    linewidth=1.2))

    # ------------------------------------------- columnas con regiones y datos
    def preparar_plano(ax, limite=2.2):
        limpiar(ax)
        ax.set_xlim(-limite, limite); ax.set_ylim(-limite, limite)

    def puntos_de_medialunas(ax):
        ax.scatter(luna_a[:, 0] * 1.5 - 0.7, luna_a[:, 1] * 1.5 - 0.4, s=9,
                   color=COLOR_CLASE_A, zorder=5)
        ax.scatter(luna_b[:, 0] * 1.5 - 0.7, luna_b[:, 1] * 1.5 - 0.4, s=9,
                   marker="s", color=COLOR_CLASE_B, zorder=5)

    def puntos_de_xor(ax):
        for x1, x2, clase in puntos_xor:
            if clase == "A":
                ax.scatter(x1, x2, s=95, marker="o", color=COLOR_CLASE_A,
                           edgecolor=SUPERFICIE, linewidth=1.6, zorder=6)
            else:
                ax.scatter(x1, x2, s=95, marker="s", color=COLOR_CLASE_B,
                           edgecolor=SUPERFICIE, linewidth=1.6, zorder=6)

    def region(ax, vertices, color=COLOR_CLASE_A, alpha=0.16):
        ax.add_patch(Polygon(vertices, closed=True, facecolor=color,
                             alpha=alpha, edgecolor=color, linewidth=1.8, zorder=2))

    L = 2.2
    # ---- fila 1: una capa -> semiplano
    dibujar_estructura(ejes[0, 0], [2, 1])
    preparar_plano(ejes[0, 1]); region(ejes[0, 1], [(-L, L), (L, L), (L, -0.3), (-L, 1.1)])
    ejes[0, 1].text(0, -1.5, "semiplano", ha="center", fontsize=10,
                    color=TINTA_SECUNDARIA, style="italic")
    preparar_plano(ejes[0, 2])
    region(ejes[0, 2], [(-L, L), (L, L), (L, -L * 0.1), (-L, L * 0.9)])
    puntos_de_xor(ejes[0, 2])
    preparar_plano(ejes[0, 3])
    region(ejes[0, 3], [(-L, L), (L, L), (L, -0.6), (-L, 0.8)])
    puntos_de_medialunas(ejes[0, 3])

    # ---- fila 2: dos capas -> region convexa
    dibujar_estructura(ejes[1, 0], [2, 3, 1])
    preparar_plano(ejes[1, 1])
    region(ejes[1, 1], [(-1.5, -1.2), (1.5, -1.2), (1.8, 0.4), (0, 1.7), (-1.8, 0.4)])
    ejes[1, 1].text(0, -1.85, "región convexa", ha="center", fontsize=10,
                    color=TINTA_SECUNDARIA, style="italic")
    preparar_plano(ejes[1, 2])
    region(ejes[1, 2], [(-L, L - 1.2), (L - 1.2, -L), (L, -L + 1.2), (-L + 1.2, L)])
    puntos_de_xor(ejes[1, 2])
    preparar_plano(ejes[1, 3])
    region(ejes[1, 3], [(-2.0, 0.1), (0.2, 1.9), (2.0, 0.4), (1.4, -0.9), (-1.2, -0.7)])
    puntos_de_medialunas(ejes[1, 3])

    # ---- fila 3: tres capas -> regiones arbitrarias
    dibujar_estructura(ejes[2, 0], [2, 3, 2, 1])
    preparar_plano(ejes[2, 1])
    region(ejes[2, 1], [(-1.9, -1.4), (-0.2, -1.4), (-0.2, 0.4), (0.6, 0.4),
                        (0.6, -1.4), (1.9, -1.4), (1.9, 1.6), (-1.9, 1.6)])
    ejes[2, 1].text(0, -1.9, "regiones arbitrarias", ha="center", fontsize=10,
                    color=TINTA_SECUNDARIA, style="italic")
    preparar_plano(ejes[2, 2])
    for centro in [(-1, 1), (1, -1)]:
        ejes[2, 2].add_patch(Circle(centro, 0.75, facecolor=COLOR_CLASE_A,
                                    alpha=0.16, edgecolor=COLOR_CLASE_A,
                                    linewidth=1.8, zorder=2))
    puntos_de_xor(ejes[2, 2])
    preparar_plano(ejes[2, 3])
    angulos = np.linspace(0, np.pi, 60)
    banda_externa = np.column_stack([np.cos(angulos), np.sin(angulos)]) * 1.5
    banda_externa[:, 0] -= 0.7; banda_externa[:, 1] -= 0.4
    normales = np.column_stack([np.cos(angulos), np.sin(angulos)])
    contorno = np.vstack([banda_externa + normales * 0.42,
                          (banda_externa - normales * 0.42)[::-1]])
    region(ejes[2, 3], contorno)
    puntos_de_medialunas(ejes[2, 3])

    for indice, titulo in enumerate(columnas):
        ejes[0, indice].set_title(titulo, fontsize=11.5, fontweight="bold", pad=12)
    for indice, etiqueta in enumerate(filas):
        ejes[indice, 0].set_ylabel(etiqueta, fontsize=11.5, fontweight="bold",
                                   labelpad=16)

    figura.suptitle("Qué problemas resuelve cada arquitectura",
                    fontsize=14, fontweight="bold", y=0.985)
    figura.tight_layout(rect=[0, 0, 1, 0.96])
    figura.savefig("/home/claude/figuras/07-regiones-decision.png", dpi=170)
    plt.close(figura)


# ============================================================ FIGURA 8
def figura_sigmoide():
    figura, ax = plt.subplots(figsize=(6.4, 4.4))
    v = np.linspace(-6, 6, 800)

    ax.step(v, np.where(v >= 0, 1, -1), where="post", color=TINTA_SECUNDARIA,
            linewidth=1.8, linestyle="--", zorder=4)
    ax.text(1.5, 1.14, "$\\mathrm{sgn}(v)$", fontsize=11.5,
            color=TINTA_SECUNDARIA, fontweight="bold")

    for parametro, color in [(0.5, "#9cc4ee"), (1.5, COLOR_CLASE_A), (5.0, "#17407a")]:
        ax.plot(v, 2 / (1 + np.exp(-parametro * v)) - 1, color=color,
                linewidth=2.2, zorder=5)
        ax.annotate(f"$b={parametro}$",
                    xy=(0.9 if parametro < 1 else 0.45, 0.0), fontsize=10,
                    color=color, fontweight="bold",
                    xytext={0.5: (3.4, -0.42), 1.5: (1.35, -0.86),
                            5.0: (0.30, -1.18)}[parametro])

    ax.axhline(0, color=TINTA_SECUNDARIA, linewidth=1.0)
    ax.axvline(0, color=TINTA_SECUNDARIA, linewidth=1.0)
    ax.grid(True, color=COLOR_GRILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.set_xlim(-6, 6); ax.set_ylim(-1.35, 1.35)
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel("$v$")
    ax.set_ylabel("$\\varphi(v)$", rotation=0, labelpad=18)
    ax.set_title("Sigmoide simétrica $\\varphi(v)=\\dfrac{2}{1+e^{-bv}}-1$",
                 fontweight="bold", pad=12)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/08-sigmoide.png", dpi=200)
    plt.close(figura)


# ============================================================ FIGURA 9
def figura_arquitectura_general():
    figura, ax = plt.subplots(figsize=(9.6, 5.8))
    ax.set_xlim(-1.1, 10.6); ax.set_ylim(-0.35, 6.15)
    ax.set_aspect("equal"); ax.axis("off")

    capas = [("entrada", 0.3, 4, "#f0efec", TINTA_SECUNDARIA),
             ("I", 3.2, 5, "#e6f6f0", COLOR_ACENTO),
             ("II", 6.1, 4, "#eceaf6", "#4a3aa7"),
             ("III", 9.0, 2, "#e4eefa", COLOR_CLASE_A)]
    RADIO = 0.28
    posiciones = []
    for _, x, cantidad, _, _ in capas:
        alturas = np.linspace(2.5 - 0.72 * (cantidad - 1) / 2,
                              2.5 + 0.72 * (cantidad - 1) / 2, cantidad)[::-1]
        posiciones.append([(x, y) for y in alturas])

    for indice in range(len(capas) - 1):
        for origen in posiciones[indice]:
            for destino in posiciones[indice + 1]:
                ax.plot([origen[0] + RADIO, destino[0] - RADIO],
                        [origen[1], destino[1]], color="#e2e1dc",
                        linewidth=0.8, zorder=1)

    etiquetas_entrada = ["$x_1$", "$x_2$", "$x_3$", "$x_4$"]
    for indice_capa, (nombre, x, cantidad, relleno, borde) in enumerate(capas):
        for indice_neurona, (px, py) in enumerate(posiciones[indice_capa]):
            ax.add_patch(Circle((px, py), RADIO, facecolor=relleno,
                                edgecolor=borde, linewidth=1.6, zorder=4))
            if indice_capa == 0:
                ax.text(px, py, etiquetas_entrada[indice_neurona], ha="center",
                        va="center", fontsize=10, zorder=5)
        if indice_capa == len(capas) - 1:
            for indice_neurona, (px, py) in enumerate(posiciones[indice_capa]):
                ax.annotate("", xy=(px + 1.25, py), xytext=(px + RADIO, py),
                            arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                            linewidth=1.3))
                ax.text(px + 1.45, py, f"$y_{indice_neurona + 1}$", fontsize=11,
                        va="center", fontweight="bold")

    nombres = ["capa de entrada", "capa I", "capa II (oculta)", "capa III (salida)"]
    for indice, (nombre, x, _, _, borde) in enumerate(capas):
        ax.text(x, 0.45, nombres[indice], ha="center", fontsize=10,
                color=TINTA_SECUNDARIA, style="italic")
        if indice > 0:
            medio = (capas[indice - 1][1] + x) / 2
            ax.text(medio, 5.35, f"$\\mathbf{{W}}^{{{nombre}}}$", ha="center",
                    fontsize=13, color=borde, fontweight="bold")
            ax.annotate("", xy=(x - RADIO - 0.15, 5.0),
                        xytext=(capas[indice - 1][1] + RADIO + 0.15, 5.0),
                        arrowprops=dict(arrowstyle="-|>", color=borde, linewidth=1.2))
        if indice > 0:
            ax.text(x, 4.35, f"$\\mathbf{{y}}^{{{nombre}}}$", ha="center",
                    fontsize=12, color=borde, fontweight="bold")

    ax.text(4.65, -0.05,
            "cada neurona de cada capa recibe además la entrada de sesgo $x_0=-1$",
            ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    ax.set_title("Arquitectura general del perceptrón multicapa",
                 fontsize=13.5, fontweight="bold", pad=4)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/09-arquitectura-general.png", dpi=180)
    plt.close(figura)


# ============================================================ FIGURA 10
def figura_cadena():
    figura, ax = plt.subplots(figsize=(10.2, 2.9))
    ax.set_xlim(0, 10.2); ax.set_ylim(0, 2.9); ax.axis("off")

    eslabones = [
        ("$w_{ji}(n)$", "el peso que\nquiero ajustar", "#f0efec", TINTA_SECUNDARIA),
        ("$v_j(n)$", "salida lineal", "#e6f6f0", COLOR_ACENTO),
        ("$y_j(n)$", "salida tras $\\varphi$", "#eceaf6", "#4a3aa7"),
        ("$e_j(n)$", "error de la neurona", "#fdece4", COLOR_CLASE_B),
        ("$\\xi(n)$", "error total", "#e4eefa", COLOR_CLASE_A),
    ]
    ancho, alto, separacion = 1.62, 0.95, 0.44
    for indice, (titulo, aclaracion, relleno, borde) in enumerate(eslabones):
        x = 0.25 + indice * (ancho + separacion)
        ax.add_patch(FancyBboxPatch((x, 1.35), ancho, alto,
                                    boxstyle="round,pad=0.04,rounding_size=0.12",
                                    facecolor=relleno, edgecolor=borde,
                                    linewidth=1.6))
        ax.text(x + ancho / 2, 1.95, titulo, ha="center", va="center", fontsize=13)
        ax.text(x + ancho / 2, 1.60, aclaracion, ha="center", va="center",
                fontsize=8.2, color=TINTA_SECUNDARIA)
        if indice < len(eslabones) - 1:
            ax.annotate("", xy=(x + ancho + separacion - 0.06, 1.83),
                        xytext=(x + ancho + 0.06, 1.83),
                        arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                        linewidth=1.4))

    ax.annotate("", xy=(0.9, 1.12), xytext=(9.3, 1.12),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_B,
                                linewidth=1.8,
                                connectionstyle="arc3,rad=-0.12"))
    ax.text(5.1, 0.30, "la regla de la cadena recorre esta misma sucesión al revés",
            ha="center", fontsize=10, color=COLOR_CLASE_B, style="italic")
    ax.set_title("De qué depende qué: la cadena que hay que derivar",
                 fontsize=12.5, fontweight="bold", pad=2)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/10-cadena-dependencias.png", dpi=190)
    plt.close(figura)


# ============================================================ FIGURA 11
def figura_derivada_sigmoide():
    """La sigmoide y su derivada: dónde la red aprende y dónde se satura."""
    figura, (arriba, abajo) = plt.subplots(2, 1, figsize=(6.6, 5.8), sharex=True,
                                           gridspec_kw={"hspace": 0.16})
    v = np.linspace(-8, 8, 900)
    y = 2 / (1 + np.exp(-v)) - 1
    derivada = 0.5 * (1 + y) * (1 - y)

    for ax in (arriba, abajo):
        ax.axvspan(-8, -3, color=COLOR_CLASE_B, alpha=0.07, zorder=0)
        ax.axvspan(3, 8, color=COLOR_CLASE_B, alpha=0.07, zorder=0)
        ax.grid(True, color=COLOR_GRILLA, linewidth=0.8)
        ax.set_axisbelow(True)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        ax.axhline(0, color=TINTA_SECUNDARIA, linewidth=1.0)
        ax.set_xlim(-8, 8)

    arriba.plot(v, y, color=COLOR_CLASE_A, linewidth=2.4)
    arriba.set_ylim(-1.3, 1.3); arriba.set_yticks([-1, 0, 1])
    arriba.set_ylabel("$\\varphi(v)$", rotation=0, labelpad=20)
    arriba.set_title("La sigmoide y su derivada", fontweight="bold", pad=12)

    abajo.plot(v, derivada, color=COLOR_ACENTO, linewidth=2.4)
    abajo.set_ylim(-0.06, 0.62); abajo.set_yticks([0, 0.25, 0.5])
    abajo.set_ylabel("$\\varphi'(v)$", rotation=0, labelpad=20)
    abajo.set_xlabel("$v$")
    abajo.annotate("máximo $=0{,}5$", xy=(0, 0.5), xytext=(1.1, 0.565),
                   fontsize=9.5, color=COLOR_ACENTO,
                   arrowprops=dict(arrowstyle="-", color=COLOR_ACENTO, linewidth=1))

    for ax, altura in ((arriba, 1.12), (abajo, 0.40)):
        ax.text(-5.5, altura, "saturación", ha="center", fontsize=9.5,
                color=COLOR_CLASE_B, style="italic")
        ax.text(5.5, altura, "saturación", ha="center", fontsize=9.5,
                color=COLOR_CLASE_B, style="italic")

    abajo.text(0, -0.045, "en las zonas naranjas $\\varphi'\\approx 0$: la corrección se apaga",
               ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/11-derivada-sigmoide.png", dpi=200)
    plt.close(figura)


# ============================================================ FIGURA 12
def figura_neurona_en_detalle():
    """Una neurona por dentro: el camino hacia adelante y el camino hacia atrás."""
    figura, ax = plt.subplots(figsize=(10.0, 5.0))
    ax.set_xlim(0, 10.6); ax.set_ylim(-0.2, 5.2); ax.axis("off")

    entradas = [("$y_1$", 4.35), ("$y_i$", 3.25), ("$y_N$", 2.15)]
    x_entrada, x_suma, x_activacion, x_salida = 0.75, 3.55, 5.65, 7.95
    y_centro = 3.25

    for etiqueta, altura in entradas:
        ax.add_patch(Circle((x_entrada, altura), 0.30, facecolor="#f0efec",
                            edgecolor=TINTA_SECUNDARIA, linewidth=1.5, zorder=4))
        ax.text(x_entrada, altura, etiqueta, ha="center", va="center", fontsize=11,
                zorder=5)
        destacada = etiqueta == "$y_i$"
        color = COLOR_CLASE_A if destacada else "#c9c8c3"
        ax.annotate("", xy=(x_suma - 0.42, y_centro), xytext=(x_entrada + 0.30, altura),
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    linewidth=2.0 if destacada else 1.2))
    ax.text(1.95, 4.32, "$w_{j1}$", fontsize=10, color=TINTA_SECUNDARIA)
    ax.text(2.05, 3.42, "$w_{ji}$", fontsize=12.5, color=COLOR_CLASE_A,
            fontweight="bold")
    ax.text(1.95, 2.10, "$w_{jN}$", fontsize=10, color=TINTA_SECUNDARIA)
    ax.text(x_entrada, 1.45, "salidas de la\ncapa anterior", ha="center",
            fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    ax.add_patch(Circle((x_suma, y_centro), 0.42, facecolor="#e6f6f0",
                        edgecolor=COLOR_ACENTO, linewidth=1.8, zorder=4))
    ax.text(x_suma, y_centro, "$\\sum$", ha="center", va="center", fontsize=17,
            zorder=5)
    ax.annotate("", xy=(x_activacion - 0.55, y_centro), xytext=(x_suma + 0.42, y_centro),
                arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA, linewidth=1.6))
    ax.text((x_suma + x_activacion) / 2, y_centro + 0.32, "$v_j$", ha="center",
            fontsize=13, color=COLOR_ACENTO, fontweight="bold")

    ax.add_patch(FancyBboxPatch((x_activacion - 0.55, y_centro - 0.45), 1.10, 0.90,
                                boxstyle="round,pad=0.03,rounding_size=0.10",
                                facecolor="#eceaf6", edgecolor="#4a3aa7",
                                linewidth=1.8, zorder=4))
    ax.text(x_activacion, y_centro, "$\\varphi$", ha="center", va="center",
            fontsize=17, zorder=5)
    ax.annotate("", xy=(x_salida - 0.32, y_centro), xytext=(x_activacion + 0.55, y_centro),
                arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA, linewidth=1.6))
    ax.add_patch(Circle((x_salida, y_centro), 0.32, facecolor="#e4eefa",
                        edgecolor=COLOR_CLASE_A, linewidth=1.8, zorder=4))
    ax.text(x_salida, y_centro, "$y_j$", ha="center", va="center", fontsize=12, zorder=5)
    ax.text(x_salida + 1.35, y_centro, "a la capa\nsiguiente", ha="center", va="center",
            fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    ax.annotate("", xy=(x_suma, 2.10), xytext=(x_salida, 2.10),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_B, linewidth=2.0,
                                connectionstyle="arc3,rad=0.16"))
    ax.text((x_suma + x_salida) / 2, 1.30, "$\\delta_j$", ha="center", fontsize=15,
            color=COLOR_CLASE_B, fontweight="bold")
    ax.text((x_suma + x_salida) / 2, 0.86,
            "gradiente de error local: se calcula una vez por neurona",
            ha="center", fontsize=9.5, color=COLOR_CLASE_B, style="italic")

    ax.add_patch(FancyBboxPatch((1.85, 0.02), 6.9, 0.60,
                                boxstyle="round,pad=0.05,rounding_size=0.12",
                                facecolor="#fdece4", edgecolor=COLOR_CLASE_B,
                                linewidth=1.5))
    ax.text(5.3, 0.32,
            "$\\Delta w_{ji} = \\mu\;\\delta_j\;y_i$   —   "
            "lo de la neurona $\\times$ lo que entró por la conexión",
            ha="center", va="center", fontsize=11.5)

    ax.set_title("Una neurona por dentro: hacia adelante y hacia atrás",
                 fontsize=13.5, fontweight="bold", pad=6)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/12-neurona-en-detalle.png", dpi=180)
    plt.close(figura)


# ============================================================ FIGURA 13
def figura_delta_salida_vs_oculta():
    """El quiebre de back-propagation: en la salida se conoce el error; en la oculta no."""
    figura, (izq, der) = plt.subplots(1, 2, figsize=(11.4, 5.0))
    for ax in (izq, der):
        ax.set_xlim(0, 5.6); ax.set_ylim(0, 5.0); ax.axis("off")

    izq.set_title("Capa de salida: el error se conoce", fontsize=12.5,
                  fontweight="bold", color=COLOR_ACENTO, pad=8)
    izq.add_patch(Circle((1.6, 3.3), 0.44, facecolor="#e4eefa",
                         edgecolor=COLOR_CLASE_A, linewidth=1.8, zorder=4))
    izq.text(1.6, 3.3, "$j$", ha="center", va="center", fontsize=13, zorder=5)
    izq.annotate("", xy=(1.16, 3.3), xytext=(0.25, 3.3),
                 arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA, linewidth=1.5))
    izq.text(0.68, 3.55, "$y^{II}_i$", ha="center", fontsize=11,
             color=TINTA_SECUNDARIA)
    izq.annotate("", xy=(3.05, 3.3), xytext=(2.04, 3.3),
                 arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA, linewidth=1.5))
    izq.text(2.55, 3.58, "$y^{III}_j$", ha="center", fontsize=11)
    izq.add_patch(FancyBboxPatch((3.20, 3.0), 1.55, 0.62,
                                 boxstyle="round,pad=0.05,rounding_size=0.12",
                                 facecolor="#e6f6f0", edgecolor=COLOR_ACENTO,
                                 linewidth=1.6))
    izq.text(3.98, 3.31, "$d_j$ conocida", ha="center", va="center", fontsize=11)
    izq.text(2.8, 2.30, "$e_j = d_j - y^{III}_j$", ha="center", fontsize=13.5)
    izq.add_patch(FancyBboxPatch((0.30, 0.80), 5.0, 0.95,
                                 boxstyle="round,pad=0.05,rounding_size=0.12",
                                 facecolor="#e6f6f0", edgecolor=COLOR_ACENTO,
                                 linewidth=1.6))
    izq.text(2.8, 1.27,
             "$\\delta^{III}_j = \\frac{1}{2}\\,e_j\\,(1+y^{III}_j)(1-y^{III}_j)$",
             ha="center", va="center", fontsize=13)
    izq.text(2.8, 0.32, "sale directo del dato de entrenamiento",
             ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    der.set_title("Capa oculta: no hay salida deseada", fontsize=12.5,
                  fontweight="bold", color=COLOR_CLASE_B, pad=8)
    der.add_patch(Circle((1.5, 3.3), 0.44, facecolor="#eceaf6",
                         edgecolor="#4a3aa7", linewidth=1.8, zorder=4))
    der.text(1.5, 3.3, "$j$", ha="center", va="center", fontsize=13, zorder=5)
    der.annotate("", xy=(1.06, 3.3), xytext=(0.25, 3.3),
                 arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA, linewidth=1.5))
    der.text(0.62, 3.55, "$y^{I}_i$", ha="center", fontsize=11,
             color=TINTA_SECUNDARIA)
    for indice, altura in enumerate([4.20, 3.30, 2.40]):
        der.add_patch(Circle((3.95, altura), 0.32, facecolor="#e4eefa",
                             edgecolor=COLOR_CLASE_A, linewidth=1.5, zorder=4))
        der.text(3.95, altura, f"$k_{indice+1}$", ha="center", va="center",
                 fontsize=10, zorder=5)
        der.annotate("", xy=(3.63, altura), xytext=(1.94, 3.3),
                     arrowprops=dict(arrowstyle="-|>", color="#c9c8c3", linewidth=1.2))
    der.annotate("", xy=(1.95, 2.85), xytext=(3.75, 2.15),
                 arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_B,
                                 linewidth=1.8, connectionstyle="arc3,rad=0.20"))
    der.text(4.78, 3.30, "$\\delta^{III}_k$", ha="center", fontsize=12.5,
             color=COLOR_CLASE_B, fontweight="bold")
    der.text(1.5, 4.30, "$d_j = \;?$", ha="center", fontsize=14,
             color=COLOR_CLASE_B, fontweight="bold")
    der.add_patch(FancyBboxPatch((0.15, 0.80), 5.3, 0.95,
                                 boxstyle="round,pad=0.05,rounding_size=0.12",
                                 facecolor="#fdece4", edgecolor=COLOR_CLASE_B,
                                 linewidth=1.6))
    der.text(2.8, 1.27,
             "$\\delta^{II}_j = \\left[\\sum_k \\delta^{III}_k\\,w^{III}_{kj}\\right]"
             "\\,\\frac{1}{2}(1+y^{II}_j)(1-y^{II}_j)$",
             ha="center", va="center", fontsize=12)
    der.text(2.8, 0.32, "se arma con los $\\delta$ de la capa siguiente",
             ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    figura.tight_layout()
    figura.savefig("/home/claude/figuras/13-delta-salida-vs-oculta.png", dpi=180)
    plt.close(figura)


# ============================================================ FIGURA 14
def figura_indices():
    """Los tres índices de back-propagation: i, j y k, y a qué capa pertenece cada uno."""
    figura, ax = plt.subplots(figsize=(10.4, 4.8))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.8); ax.axis("off")

    capas = [
        (1.5, "$p-1$", "capa anterior", "$i$", "#f0efec", TINTA_SECUNDARIA),
        (5.2, "$p$", "capa actual", "$j$", "#eceaf6", "#4a3aa7"),
        (8.9, "$p+1$", "capa siguiente", "$k$", "#e4eefa", COLOR_CLASE_A),
    ]
    alturas = [3.55, 2.75, 1.95]
    posiciones = {}
    for x, _, _, indice, relleno, borde in capas:
        posiciones[indice] = []
        for altura in alturas:
            ax.add_patch(Circle((x, altura), 0.30, facecolor=relleno,
                                edgecolor=borde, linewidth=1.5, zorder=4))
            posiciones[indice].append((x, altura))

    for origen in posiciones["$i$"]:
        for destino in posiciones["$j$"]:
            ax.plot([origen[0] + 0.30, destino[0] - 0.30], [origen[1], destino[1]],
                    color="#dedcd6", linewidth=0.9, zorder=1)
    for origen in posiciones["$j$"]:
        for destino in posiciones["$k$"]:
            ax.plot([origen[0] + 0.30, destino[0] - 0.30], [origen[1], destino[1]],
                    color="#dedcd6", linewidth=0.9, zorder=1)

    ax.add_patch(Circle(posiciones["$i$"][1], 0.30, facecolor="#f0efec",
                        edgecolor=TINTA_SECUNDARIA, linewidth=2.6, zorder=5))
    ax.add_patch(Circle(posiciones["$j$"][1], 0.30, facecolor="#eceaf6",
                        edgecolor="#4a3aa7", linewidth=2.6, zorder=5))
    ax.text(*posiciones["$i$"][1], "$i$", ha="center", va="center", fontsize=13, zorder=6)
    ax.text(*posiciones["$j$"][1], "$j$", ha="center", va="center", fontsize=13, zorder=6)
    for indice, posicion in enumerate(posiciones["$k$"]):
        ax.text(*posicion, f"$k_{indice+1}$", ha="center", va="center", fontsize=10.5,
                zorder=6)

    ax.annotate("", xy=(posiciones["$j$"][1][0] - 0.30, posiciones["$j$"][1][1]),
                xytext=(posiciones["$i$"][1][0] + 0.30, posiciones["$i$"][1][1]),
                arrowprops=dict(arrowstyle="-|>", color="#4a3aa7", linewidth=2.2))
    ax.text(3.35, 2.98, "$w^{(p)}_{ji}$", ha="center", fontsize=13, color="#4a3aa7",
            fontweight="bold")
    ax.text(3.35, 2.42, "el peso que\nse ajusta", ha="center", fontsize=9,
            color=TINTA_SECUNDARIA, style="italic")

    for posicion in posiciones["$k$"]:
        ax.annotate("", xy=(posiciones["$j$"][1][0] + 0.34, posiciones["$j$"][1][1] - 0.14),
                    xytext=(posicion[0] - 0.34, posicion[1] - 0.14),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_B, linewidth=1.5,
                                    connectionstyle="arc3,rad=0.10"))
    ax.text(7.05, 1.30, "$w^{(p+1)}_{kj}$", ha="center", fontsize=13,
            color=COLOR_CLASE_B, fontweight="bold")
    ax.text(7.05, 0.80, "por acá vuelven los $\\delta$", ha="center", fontsize=9.5,
            color=COLOR_CLASE_B, style="italic")

    for x, nombre, descripcion, indice, _, borde in capas:
        ax.text(x, 4.30, nombre, ha="center", fontsize=14, fontweight="bold",
                color=borde)
        ax.text(x, 3.98, descripcion, ha="center", fontsize=9.5,
                color=TINTA_SECUNDARIA, style="italic")
        ax.text(x, 1.32, f"índice {indice}", ha="center", fontsize=11.5,
                color=borde, fontweight="bold")

    ax.set_title("Los tres índices: $i$ de dónde viene, $j$ dónde estoy, "
                 "$k$ adónde va", fontsize=13, fontweight="bold", pad=4)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/14-indices.png", dpi=180)
    plt.close(figura)


# ============================================================ FIGURA 15
def figura_espejo():
    """Propagación hacia adelante y retropropagación: los mismos pesos, al revés."""
    figura, (arriba, abajo) = plt.subplots(2, 1, figsize=(9.8, 6.4))

    def dibujar_fila(ax, hacia_adelante):
        ax.set_xlim(0, 9.8); ax.set_ylim(0, 3.0); ax.axis("off")
        columnas = [(1.4, "#f0efec", TINTA_SECUNDARIA),
                    (4.9, "#eceaf6", "#4a3aa7"),
                    (8.4, "#e4eefa", COLOR_CLASE_A)]
        for x, relleno, borde in columnas:
            for altura in (2.15, 1.45, 0.75):
                ax.add_patch(Circle((x, altura), 0.26, facecolor=relleno,
                                    edgecolor=borde, linewidth=1.5, zorder=4))
        color = COLOR_CLASE_A if hacia_adelante else COLOR_CLASE_B
        for x_izq, x_der in ((1.4, 4.9), (4.9, 8.4)):
            if hacia_adelante:
                ax.annotate("", xy=(x_der - 0.34, 1.45), xytext=(x_izq + 0.34, 1.45),
                            arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.6))
            else:
                ax.annotate("", xy=(x_izq + 0.34, 1.45), xytext=(x_der - 0.34, 1.45),
                            arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.6))
        return columnas

    dibujar_fila(arriba, True)
    arriba.set_title("Propagación hacia adelante", fontsize=12.5, fontweight="bold",
                     color=COLOR_CLASE_A, pad=2)
    arriba.text(3.15, 1.85, "$\\mathbf{W}^{(p)}$", ha="center", fontsize=13,
                color=COLOR_CLASE_A, fontweight="bold")
    arriba.text(6.65, 1.85, "$\\mathbf{W}^{(p+1)}$", ha="center", fontsize=13,
                color=COLOR_CLASE_A, fontweight="bold")
    for x, etiqueta in ((1.4, "$\\mathbf{y}^{(p-1)}$"), (4.9, "$\\mathbf{y}^{(p)}$"),
                        (8.4, "$\\mathbf{y}^{(p+1)}$")):
        arriba.text(x, 0.18, etiqueta, ha="center", fontsize=12)
    arriba.text(4.9, 2.68, "cada capa pondera lo que recibe y lo pasa a la siguiente",
                ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    dibujar_fila(abajo, False)
    abajo.set_title("Retropropagación del error", fontsize=12.5, fontweight="bold",
                    color=COLOR_CLASE_B, pad=2)
    abajo.text(3.15, 1.85, "$\\mathbf{W}^{(p)}$", ha="center", fontsize=13,
               color=COLOR_CLASE_B, fontweight="bold")
    abajo.text(6.65, 1.85, "$\\mathbf{W}^{(p+1)}$", ha="center", fontsize=13,
               color=COLOR_CLASE_B, fontweight="bold")
    for x, etiqueta in ((1.4, "$\\delta^{(p-1)}$"), (4.9, "$\\delta^{(p)}$"),
                        (8.4, "$\\delta^{(p+1)}$")):
        abajo.text(x, 0.18, etiqueta, ha="center", fontsize=12)
    abajo.text(4.9, 2.68,
               "los $\\delta$ atraviesan LOS MISMOS pesos, en sentido contrario",
               ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")

    figura.tight_layout()
    figura.savefig("/home/claude/figuras/15-espejo.png", dpi=185)
    plt.close(figura)


# ---------------------------------------------------------------- red de ejemplo
# Red del resumen del algoritmo: 2 entradas, 3 neuronas en la capa I,
# 2 en la capa II y 1 en la capa de salida.
POSICIONES_ENTRADAS = [(0.75, 2.75), (0.75, 1.35)]
POSICIONES_CAPA_I   = [(3.30, 3.55), (3.30, 2.05), (3.30, 0.55)]
POSICIONES_CAPA_II  = [(6.00, 2.90), (6.00, 1.20)]
POSICIONES_CAPA_III = [(8.55, 2.05)]
RADIO_NEURONA = 0.34


def _dibujar_esqueleto(ax, color_conexiones="#dedcd6", grosor=1.0,
                       resaltadas=(), color_resaltado=None, hacia_atras=False):
    """Dibuja la red del resumen. `resaltadas` son tuplas (capa_origen, i, j)."""
    capas = [POSICIONES_ENTRADAS, POSICIONES_CAPA_I, POSICIONES_CAPA_II,
             POSICIONES_CAPA_III]
    for indice_capa in range(len(capas) - 1):
        for i, origen in enumerate(capas[indice_capa]):
            for j, destino in enumerate(capas[indice_capa + 1]):
                esta_resaltada = (indice_capa, i, j) in resaltadas
                color = color_resaltado if esta_resaltada else color_conexiones
                ancho = 2.4 if esta_resaltada else grosor
                # Hacia atrás no hay delta para las entradas: ese tramo va sin punta.
                sin_punta = hacia_atras and indice_capa == 0
                if hacia_atras and not sin_punta:
                    inicio, final = destino, origen
                else:
                    inicio, final = origen, destino
                dx, dy = final[0] - inicio[0], final[1] - inicio[1]
                largo = np.hypot(dx, dy)
                ux, uy = dx / largo, dy / largo
                ax.annotate("", xy=(final[0] - ux * RADIO_NEURONA,
                                    final[1] - uy * RADIO_NEURONA),
                            xytext=(inicio[0] + ux * RADIO_NEURONA,
                                    inicio[1] + uy * RADIO_NEURONA),
                            arrowprops=dict(arrowstyle="-" if sin_punta else "-|>",
                                            color=color, linewidth=ancho),
                            zorder=2 if not esta_resaltada else 3)

    estilos = [("#f0efec", TINTA_SECUNDARIA), ("#e6f6f0", COLOR_ACENTO),
               ("#eceaf6", "#4a3aa7"), ("#e4eefa", COLOR_CLASE_A)]
    etiquetas = [["$x_1$", "$x_2$"],
                 ["$\\varphi(v^{I}_1)$", "$\\varphi(v^{I}_2)$", "$\\varphi(v^{I}_3)$"],
                 ["$\\varphi(v^{II}_1)$", "$\\varphi(v^{II}_2)$"],
                 ["$\\varphi(v^{III}_1)$"]]
    for indice_capa, capa in enumerate(capas):
        relleno, borde = estilos[indice_capa]
        for indice_neurona, (px, py) in enumerate(capa):
            radio = RADIO_NEURONA if indice_capa > 0 else 0.28
            ax.add_patch(Circle((px, py), radio, facecolor=relleno,
                                edgecolor=borde, linewidth=1.6, zorder=5))
            tamanio = 11 if indice_capa == 0 else 7.5
            ax.text(px, py, etiquetas[indice_capa][indice_neurona], ha="center",
                    va="center", fontsize=tamanio, zorder=6)

    salida = POSICIONES_CAPA_III[0]
    ax.annotate("", xy=(salida[0] + 1.15, salida[1]),
                xytext=(salida[0] + RADIO_NEURONA, salida[1]),
                arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                linewidth=1.4))
    ax.text(salida[0] + 1.35, salida[1], "$y$", fontsize=13, va="center",
            fontweight="bold")

    for x, nombre in ((0.75, "entrada"), (3.30, "capa I"), (6.00, "capa II"),
                      (8.55, "capa III")):
        ax.text(x, -0.35, nombre, ha="center", fontsize=9.5,
                color=TINTA_SECUNDARIA, style="italic")


def _preparar_lienzo(titulo, color_titulo):
    figura, ax = plt.subplots(figsize=(9.8, 5.0))
    ax.set_xlim(-0.1, 10.4); ax.set_ylim(-0.7, 4.9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(titulo, fontsize=13.5, fontweight="bold", color=color_titulo, pad=2)
    return figura, ax


def _caja_formula(ax, x, y, ancho, alto, texto, color, tamanio=11.5):
    ax.add_patch(FancyBboxPatch((x, y), ancho, alto,
                                boxstyle="round,pad=0.06,rounding_size=0.12",
                                facecolor=SUPERFICIE, edgecolor=color,
                                linewidth=1.5, zorder=8))
    ax.text(x + ancho / 2, y + alto / 2, texto, ha="center", va="center",
            fontsize=tamanio, zorder=9)


# ============================================================ FIGURA 16
def figura_ciclo_bp():
    """Los cinco pasos del algoritmo, como bucle."""
    figura, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 9.6); ax.set_ylim(0, 3.6); ax.axis("off")

    pasos = [
        ("1. Inicializar", "pesos al azar\nen $[-0{,}5;\\,0{,}5]$", "#f0efec",
         TINTA_SECUNDARIA),
        ("2. Hacia adelante", "entra el patrón,\nsale $y$", "#e4eefa", COLOR_CLASE_A),
        ("3. Hacia atrás", "se calculan\nlos $\\delta$", "#fdece4", COLOR_CLASE_B),
        ("4. Ajustar pesos", "$w \\leftarrow w + \\Delta w$\nen todas las capas",
         "#e6f6f0", COLOR_ACENTO),
    ]
    ancho, alto = 2.05, 1.15
    for indice, (titulo, detalle, relleno, borde) in enumerate(pasos):
        x = 0.25 + indice * (ancho + 0.35)
        ax.add_patch(FancyBboxPatch((x, 1.65), ancho, alto,
                                    boxstyle="round,pad=0.05,rounding_size=0.14",
                                    facecolor=relleno, edgecolor=borde, linewidth=1.8))
        ax.text(x + ancho / 2, 2.48, titulo, ha="center", va="center", fontsize=11,
                fontweight="bold", color=borde)
        ax.text(x + ancho / 2, 2.02, detalle, ha="center", va="center", fontsize=8.8,
                color=TINTA_SECUNDARIA)
        if indice < len(pasos) - 1:
            ax.annotate("", xy=(x + ancho + 0.30, 2.22), xytext=(x + ancho + 0.05, 2.22),
                        arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                        linewidth=1.6))

    ax.annotate("", xy=(2.50, 1.42), xytext=(8.65, 1.42),
                arrowprops=dict(arrowstyle="-|>", color=TINTA_SECUNDARIA,
                                linewidth=1.8, connectionstyle="arc3,rad=-0.14"))
    ax.text(5.6, 0.62, "5. Siguiente patrón — y cuando pasaron todos, "
            "eso es una época", ha="center", fontsize=10.5,
            color=TINTA_SECUNDARIA)
    ax.text(5.6, 0.22, "se repiten muchas épocas hasta convergencia",
            ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    ax.set_title("El algoritmo de retropropagación, de punta a punta",
                 fontsize=13, fontweight="bold", pad=2)
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/16-ciclo-bp.png", dpi=185)
    plt.close(figura)


# ============================================================ FIGURA 17
def figura_paso_adelante():
    figura, ax = _preparar_lienzo("Paso 2 — propagación hacia adelante",
                                  COLOR_CLASE_A)
    _dibujar_esqueleto(ax, resaltadas={(0, 0, 0), (0, 1, 0)},
                       color_resaltado=COLOR_CLASE_A)
    _caja_formula(ax, 1.05, 4.05, 7.0, 0.68,
                  "$y^{I}_1 = \\varphi\\left(w^{I}_{11}x_1 + w^{I}_{12}x_2 "
                  "+ w^{I}_{10}(-1)\\right)$", COLOR_CLASE_A)
    ax.text(2.05, 3.05, "$w^{I}_{11}$", fontsize=10, color=COLOR_CLASE_A,
            fontweight="bold")
    ax.text(2.05, 2.30, "$w^{I}_{12}$", fontsize=10, color=COLOR_CLASE_A,
            fontweight="bold")
    ax.text(5.2, -0.68, "cada capa pondera lo que recibe, le aplica $\\varphi$ "
            "y pasa el resultado a la siguiente",
            ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/17-paso-adelante.png", dpi=185)
    plt.close(figura)


# ============================================================ FIGURA 18
def figura_paso_atras():
    figura, ax = _preparar_lienzo("Paso 3 — propagación hacia atrás",
                                  COLOR_CLASE_B)
    _dibujar_esqueleto(ax, resaltadas={(2, 0, 0), (2, 1, 0)},
                       color_resaltado=COLOR_CLASE_B, hacia_atras=True)
    for posicion, etiqueta in ((POSICIONES_CAPA_III[0], "$\\delta^{III}$"),):
        ax.text(posicion[0], posicion[1] - 0.72, etiqueta, ha="center", fontsize=12,
                color=COLOR_CLASE_B, fontweight="bold")
    for indice, posicion in enumerate(POSICIONES_CAPA_II):
        ax.text(posicion[0] - 0.05, posicion[1] - 0.70, f"$\\delta^{{II}}_{indice+1}$",
                ha="center", fontsize=11, color=COLOR_CLASE_B, fontweight="bold")
    for indice, posicion in enumerate(POSICIONES_CAPA_I):
        ax.text(posicion[0] - 0.05, posicion[1] - 0.68, f"$\\delta^{{I}}_{indice+1}$",
                ha="center", fontsize=11, color=COLOR_CLASE_B, fontweight="bold")

    _caja_formula(ax, 0.15, 4.28, 4.6, 0.60,
                  "$\\delta^{III} = (d-y)\\,\\frac{1}{2}(1+y^{III})(1-y^{III})$",
                  COLOR_CLASE_B, tamanio=10.5)
    _caja_formula(ax, 5.05, 4.28, 5.2, 0.60,
                  "$\\delta^{I}_1 = \\left(w^{II}_{11}\\delta^{II}_1 + "
                  "w^{II}_{21}\\delta^{II}_2\\right)\\frac{1}{2}(1+y^{I}_1)(1-y^{I}_1)$",
                  COLOR_CLASE_B, tamanio=10)
    ax.text(5.2, -0.68, "el error entra por la salida y retrocede; cada neurona "
            "junta los $\\delta$ de todas las que alimenta",
            ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/18-paso-atras.png", dpi=185)
    plt.close(figura)


# ============================================================ FIGURA 19
def figura_paso_ajuste():
    figura, ax = _preparar_lienzo("Paso 4 — adaptación de los pesos",
                                  COLOR_ACENTO)
    _dibujar_esqueleto(ax, resaltadas={(0, 0, 0), (0, 1, 0)},
                       color_resaltado=COLOR_ACENTO)
    ax.text(2.05, 3.05, "$\\Delta w^{I}_{11}$", fontsize=10, color=COLOR_ACENTO,
            fontweight="bold")
    ax.text(2.00, 2.28, "$\\Delta w^{I}_{12}$", fontsize=10, color=COLOR_ACENTO,
            fontweight="bold")
    _caja_formula(ax, 0.55, 4.28, 4.3, 0.60,
                  "$\\Delta w^{I}_{11} = \\mu\\,\\delta^{I}_1\\,x_1$",
                  COLOR_ACENTO, tamanio=12)
    _caja_formula(ax, 5.30, 4.28, 4.7, 0.60,
                  "$w^{I}_{11}(n{+}1) = w^{I}_{11}(n) + \\Delta w^{I}_{11}$",
                  COLOR_ACENTO, tamanio=11.5)
    ax.text(5.2, -0.68,
            "el orden entre capas no importa: todas las salidas ya se guardaron "
            "en el paso 2, con los pesos viejos",
            ha="center", fontsize=9.5, color=TINTA_SECUNDARIA, style="italic")
    figura.tight_layout()
    figura.savefig("/home/claude/figuras/19-paso-ajuste.png", dpi=185)
    plt.close(figura)


if __name__ == "__main__":
    figura_regiones_de_decision()
    figura_sigmoide()
    figura_arquitectura_general()
    figura_cadena()
    figura_derivada_sigmoide()
    figura_neurona_en_detalle()
    figura_delta_salida_vs_oculta()
    figura_indices()
    figura_espejo()
    figura_ciclo_bp()
    figura_paso_adelante()
    figura_paso_atras()
    figura_paso_ajuste()
    print("figuras del multicapa generadas")


# ============================================================ FIGURA 23
def figura_ejemplo_numerico():
    """La red 2-3-2-1 del ejemplo, con los valores de ida y los delta de vuelta."""
    figura, ejes = plt.subplots(figsize=(11.0, 4.6))
    ejes.set_xlim(0, 13.2); ejes.set_ylim(-0.9, 7.6)
    ejes.set_xticks([]); ejes.set_yticks([])
    for lado in ejes.spines.values():
        lado.set_visible(False)

    columnas = {"ent": 1.3, "I": 4.3, "II": 7.9, "III": 11.2}
    nodos = {
        "ent": [(4.6, "$x_1$", "1.00", None), (2.0, "$x_2$", "$-1.00$", None)],
        "I":   [(5.5, "$y^I_1$", "0.380", "0.0736"), (3.3, "$y^I_2$", "$-0.336$", "0.0346"),
                (1.1, "$y^I_3$", "$-0.149$", "$-0.0794$")],
        "II":  [(4.6, "$y^{II}_1$", "$-0.063$", "0.2070"), (2.0, "$y^{II}_2$", "$-0.138$", "$-0.1274$")],
        "III": [(3.3, "$y$", "$-0.041$", "0.5195")],
    }
    for origen, destino in [("ent", "I"), ("I", "II"), ("II", "III")]:
        for altura_o, *_ in nodos[origen]:
            for altura_d, *_ in nodos[destino]:
                ejes.plot([columnas[origen] + 0.52, columnas[destino] - 0.52],
                          [altura_o, altura_d], color=COLOR_GRILLA, linewidth=1.0, zorder=1)

    for capa, lista in nodos.items():
        if capa == "ent":
            borde, relleno = COLOR_CLASE_A, "#e4eefb"
        elif capa == "III":
            borde, relleno = COLOR_ACENTO, "#e2f3ed"
        else:
            borde, relleno = TINTA_SECUNDARIA, "white"
        for altura, nombre, valor, delta in lista:
            ejes.add_patch(Circle((columnas[capa], altura), 0.52, facecolor=relleno,
                                  edgecolor=borde, linewidth=1.6, zorder=4))
            ejes.text(columnas[capa], altura + 0.14, nombre, ha="center", va="center",
                      fontsize=9.5, zorder=5)
            ejes.text(columnas[capa], altura - 0.20, valor, ha="center", va="center",
                      fontsize=8, zorder=5, color=COLOR_CLASE_A)
            if delta:
                ejes.text(columnas[capa], altura - 0.88, f"$\\delta=${delta}", ha="center",
                          va="center", fontsize=7.6, color=COLOR_CLASE_B)

    ejes.text(11.2, 3.3 + 0.95, "$d = 1.00$", ha="center", fontsize=9, color=COLOR_ACENTO)
    for capa, etiqueta in [("ent", "entrada"), ("I", "capa I"), ("II", "capa II"), ("III", "capa III")]:
        ejes.text(columnas[capa], -0.6, etiqueta, ha="center", fontsize=8.5,
                  color=TINTA_SECUNDARIA, style="italic")
    ejes.annotate("", xy=(9.6, 7.25), xytext=(2.4, 7.25),
                  arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_A, linewidth=1.6))
    ejes.text(6.0, 7.4, "paso 1: hacia adelante  (en azul, las salidas)", ha="center",
              fontsize=8.6, color=COLOR_CLASE_A)
    ejes.annotate("", xy=(2.4, 6.75), xytext=(9.6, 6.75),
                  arrowprops=dict(arrowstyle="-|>", color=COLOR_CLASE_B, linewidth=1.6))
    ejes.text(6.0, 6.42, "paso 3: hacia atrás  (en naranja, los $\\delta$)", ha="center",
              fontsize=8.6, color=COLOR_CLASE_B)
    figura.savefig("23-ejemplo-numerico.png", dpi=170, bbox_inches="tight")
    plt.close(figura)
    print("escrita: 23-ejemplo-numerico.png")
