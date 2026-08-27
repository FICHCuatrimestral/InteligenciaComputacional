"""
Figuras del apunte: XOR con tres perceptrones (diapositivas 1-10).
Inteligencia Computacional - FICH-UNL
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ---------------------------------------------------------------- paleta
SUPERFICIE      = "#fcfcfb"
TINTA_PRIMARIA  = "#0b0b0b"
TINTA_SECUNDARIA= "#52514e"
COLOR_CLASE_POS = "#2a78d6"   # slot 1 - azul   -> clase +1
COLOR_CLASE_NEG = "#eb6834"   # slot 2 - naranja -> clase -1
COLOR_RECTA_A   = "#1baf7a"   # slot 3 - aqua
COLOR_RECTA_B   = "#4a3aa7"   # slot 7 - violeta
COLOR_GRILLA    = "#d8d7d2"

plt.rcParams.update({
    "figure.facecolor":  SUPERFICIE,
    "axes.facecolor":    SUPERFICIE,
    "savefig.facecolor": SUPERFICIE,
    "font.size":         11,
    "axes.labelsize":    12,
    "axes.titlesize":    13,
    "text.color":        TINTA_PRIMARIA,
    "axes.labelcolor":   TINTA_PRIMARIA,
    "xtick.color":       TINTA_SECUNDARIA,
    "ytick.color":       TINTA_SECUNDARIA,
})

# Patrones del XOR con codificacion bipolar: (x1, x2, salida deseada)
PATRONES_XOR = [(-1, -1, -1), (-1, +1, +1), (+1, -1, +1), (+1, +1, -1)]

LIMITE = 2.4


def preparar_ejes(ax, etiqueta_x, etiqueta_y, titulo):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-LIMITE, LIMITE)
    ax.set_ylim(-LIMITE, LIMITE)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.grid(True, color=COLOR_GRILLA, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(TINTA_SECUNDARIA)
        ax.spines[lado].set_linewidth(1.0)
    ax.axhline(0, color=TINTA_SECUNDARIA, linewidth=1.0, zorder=1)
    ax.axvline(0, color=TINTA_SECUNDARIA, linewidth=1.0, zorder=1)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y, rotation=0, labelpad=14)
    ax.set_title(titulo, pad=14, fontweight="bold")


def dibujar_patrones_xor(ax, tamanio=170):
    for x1, x2, deseada in PATRONES_XOR:
        if deseada == +1:
            ax.scatter(x1, x2, s=tamanio, marker="o",
                       facecolor=COLOR_CLASE_POS, edgecolor=SUPERFICIE,
                       linewidth=2, zorder=6)
        else:
            ax.scatter(x1, x2, s=tamanio, marker="s",
                       facecolor=COLOR_CLASE_NEG, edgecolor=SUPERFICIE,
                       linewidth=2, zorder=6)
        ax.annotate(f"{deseada:+d}", (x1, x2), textcoords="offset points",
                    xytext=(0, 15), ha="center", fontsize=10,
                    color=TINTA_SECUNDARIA, zorder=7)


def leyenda_clases(ax, **kwargs):
    elementos = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLOR_CLASE_POS,
               markeredgecolor=SUPERFICIE, markersize=11, label="XOR $= +1$"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=COLOR_CLASE_NEG,
               markeredgecolor=SUPERFICIE, markersize=11, label="XOR $= -1$"),
    ]
    ax.legend(handles=elementos, frameon=False, fontsize=10,
              labelcolor=TINTA_SECUNDARIA, **kwargs)


def recta_suma(ax, constante, color, etiqueta, estilo="-"):
    """Dibuja x1 + x2 = constante  ->  x2 = constante - x1."""
    x = np.array([-LIMITE, LIMITE])
    ax.plot(x, constante - x, estilo, color=color, linewidth=2.2, zorder=5,
            label=etiqueta)


# ============================================================ FIGURA 1
def figura_problema():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    preparar_ejes(ax, "$x_1$", "$x_2$", "El XOR no es linealmente separable")

    for constante, desplazamiento in [(0.6, 0), (1.7, 0), (-1.4, 0)]:
        x = np.array([-LIMITE, LIMITE])
        ax.plot(x, constante - x, "--", color=TINTA_SECUNDARIA,
                linewidth=1.3, alpha=0.55, zorder=3)
    x = np.array([-LIMITE, LIMITE])
    ax.plot(x, 0.9 * x + 0.3, "--", color=TINTA_SECUNDARIA,
            linewidth=1.3, alpha=0.55, zorder=3)

    dibujar_patrones_xor(ax)
    ax.text(0.0, -2.05, "cualquier recta deja al menos\nun patrón mal clasificado",
            ha="center", va="center", fontsize=9.5, color=TINTA_SECUNDARIA,
            style="italic", zorder=9,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SUPERFICIE,
                      edgecolor="none"))
    leyenda_clases(ax, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/01-xor-no-separable.png", dpi=200)
    plt.close(fig)


# ============================================================ FIGURA 2
def figura_perceptron_a():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    preparar_ejes(ax, "$x_1$", "$x_2$",
                  "Perceptrón A:  $y_A=\\mathrm{sgn}(x_1+x_2+1)$")

    x = np.linspace(-LIMITE, LIMITE, 400)
    ax.fill_between(x, -1 - x, LIMITE, color=COLOR_RECTA_A, alpha=0.13, zorder=2)
    recta_suma(ax, -1.0, COLOR_RECTA_A, None)

    dibujar_patrones_xor(ax)
    ax.text(1.55, 2.05, "$y_A = +1$", fontsize=12, color=COLOR_RECTA_A,
            fontweight="bold", zorder=8)
    ax.text(-1.95, -1.95, "$y_A = -1$", fontsize=12, color=TINTA_SECUNDARIA,
            fontweight="bold", zorder=8)
    ax.text(-2.28, 1.48, "$x_1+x_2=-1$", fontsize=10, color=COLOR_RECTA_A,
            ha="left", fontweight="bold")
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/02-perceptron-A.png", dpi=200)
    plt.close(fig)


# ============================================================ FIGURA 3
def figura_perceptron_b():
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    preparar_ejes(ax, "$x_1$", "$x_2$",
                  "Perceptrón B:  $y_B=\\mathrm{sgn}(x_1+x_2-1)$")

    x = np.linspace(-LIMITE, LIMITE, 400)
    ax.fill_between(x, 1 - x, LIMITE, color=COLOR_RECTA_B, alpha=0.13, zorder=2)
    recta_suma(ax, -1.0, COLOR_RECTA_A, None, estilo="--")
    recta_suma(ax, 1.0, COLOR_RECTA_B, None)

    dibujar_patrones_xor(ax)
    ax.text(1.15, 1.55, "$y_B = +1$", fontsize=12, color=COLOR_RECTA_B,
            fontweight="bold", zorder=8)
    ax.text(-1.95, -1.95, "$y_B = -1$", fontsize=12, color=TINTA_SECUNDARIA,
            fontweight="bold", zorder=8)
    ax.text(-2.28, 1.48, "$A$", fontsize=12, color=COLOR_RECTA_A, ha="left",
            fontweight="bold")
    ax.text(2.28, -1.62, "$B$", fontsize=12, color=COLOR_RECTA_B, ha="right",
            fontweight="bold")
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/03-perceptron-B.png", dpi=200)
    plt.close(fig)


# ============================================================ FIGURA 4
def figura_franjas():
    fig, ax = plt.subplots(figsize=(5.8, 5.8))
    preparar_ejes(ax, "$x_1$", "$x_2$",
                  "Las tres franjas y su código $(y_A,\\,y_B)$")

    x = np.linspace(-LIMITE, LIMITE, 400)
    ax.fill_between(x, 1 - x, LIMITE, color=COLOR_CLASE_NEG, alpha=0.13, zorder=2)
    ax.fill_between(x, -1 - x, 1 - x, color=COLOR_CLASE_POS, alpha=0.16, zorder=2)
    ax.fill_between(x, -LIMITE, -1 - x, color=COLOR_CLASE_NEG, alpha=0.13, zorder=2)

    recta_suma(ax, -1.0, COLOR_RECTA_A, None)
    recta_suma(ax, 1.0, COLOR_RECTA_B, None)
    dibujar_patrones_xor(ax)

    ax.text(1.25, 1.75, "$(+1,+1)$\n$y_C=-1$", fontsize=10.5, ha="center",
            color=TINTA_PRIMARIA, zorder=8,
            bbox=dict(boxstyle="round,pad=0.32", facecolor=SUPERFICIE,
                      edgecolor=COLOR_CLASE_NEG, linewidth=1.1))
    ax.text(-0.25, -0.28, "$(+1,-1)$\n$y_C=+1$", fontsize=10.5, ha="center",
            color=TINTA_PRIMARIA, zorder=8,
            bbox=dict(boxstyle="round,pad=0.32", facecolor=SUPERFICIE,
                      edgecolor=COLOR_CLASE_POS, linewidth=1.1))
    ax.text(-1.25, -1.75, "$(-1,-1)$\n$y_C=-1$", fontsize=10.5, ha="center",
            color=TINTA_PRIMARIA, zorder=8,
            bbox=dict(boxstyle="round,pad=0.32", facecolor=SUPERFICIE,
                      edgecolor=COLOR_CLASE_NEG, linewidth=1.1))
    ax.text(-2.28, 1.48, "$A$", fontsize=12, color=COLOR_RECTA_A, ha="left",
            fontweight="bold")
    ax.text(2.28, -1.62, "$B$", fontsize=12, color=COLOR_RECTA_B, ha="right",
            fontweight="bold")
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/04-tres-franjas.png", dpi=200)
    plt.close(fig)


# ============================================================ FIGURA 5
def figura_plano_oculto():
    """Plano oculto con los ejes de Milone: yB horizontal, yA vertical."""
    fig, ax = plt.subplots(figsize=(5.8, 5.8))
    preparar_ejes(ax, "$y_B$", "$y_A$",
                  "Plano oculto y recta del perceptrón C")

    # Region donde yC = +1:  yA - yB - 1 > 0  ->  yA > yB + 1  (por ENCIMA de la recta)
    eje = np.linspace(-LIMITE, LIMITE, 400)
    ax.fill_between(eje, eje + 1, LIMITE, color=COLOR_CLASE_POS, alpha=0.13,
                    zorder=2)
    ax.plot(eje, eje + 1, "-", color=COLOR_RECTA_B, linewidth=2.2, zorder=5)

    # (yA, yB, yC) de los tres codigos alcanzables
    codigos = [(+1, -1, +1), (+1, +1, -1), (-1, -1, -1)]
    for ya, yb, yc in codigos:
        color = COLOR_CLASE_POS if yc == +1 else COLOR_CLASE_NEG
        marcador = "o" if yc == +1 else "s"
        ax.scatter(yb, ya, s=200, marker=marcador, facecolor=color,
                   edgecolor=SUPERFICIE, linewidth=2, zorder=6)
        ax.annotate(f"$y_C={yc:+d}$", (yb, ya), textcoords="offset points",
                    xytext=(0, 18), ha="center", fontsize=10.5,
                    color=TINTA_SECUNDARIA, zorder=7)

    # Codigo imposible: yA = -1, yB = +1
    ax.scatter(+1, -1, s=200, marker="X", facecolor="none",
               edgecolor=TINTA_SECUNDARIA, linewidth=2.0, zorder=6)
    ax.annotate("imposible\n(don't care)", (+1, -1), textcoords="offset points",
                xytext=(0, 18), ha="center", fontsize=9.5, style="italic",
                color=TINTA_SECUNDARIA, zorder=7)

    ax.text(-2.28, -1.05, "$y_A = 1 + y_B$", fontsize=10.5, color=COLOR_RECTA_B,
            ha="left", fontweight="bold", zorder=9,
            bbox=dict(boxstyle="round,pad=0.25", facecolor=SUPERFICIE,
                      edgecolor="none"))
    ax.text(-1.35, 1.95, "$y_C = +1$", fontsize=11.5, color=COLOR_CLASE_POS,
            fontweight="bold", zorder=9)
    ax.text(1.35, -2.05, "$y_C = -1$", fontsize=11.5, color=TINTA_SECUNDARIA,
            fontweight="bold", ha="center", zorder=9)
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/05-plano-oculto.png", dpi=200)
    plt.close(fig)


# ============================================================ FIGURA 6
def figura_arquitectura():
    """Arquitectura de la red de tres neuronas con todos los pesos."""
    from matplotlib.patches import Circle, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.set_xlim(-0.9, 9.4)
    ax.set_ylim(-0.6, 5.05)
    ax.set_aspect("equal")
    ax.axis("off")

    RADIO = 0.42
    nodos = {
        "x0a": (0.4, 3.85), "x1": (0.4, 2.30), "x2": (0.4, 0.75),
        "A":   (4.0, 3.05), "B":  (4.0, 1.35),
        "x0c": (4.0, 4.30), "C":  (7.4, 2.20),
    }

    def dibujar_nodo(clave, etiqueta, color_borde, relleno):
        x, y = nodos[clave]
        ax.add_patch(Circle((x, y), RADIO, facecolor=relleno,
                            edgecolor=color_borde, linewidth=1.8, zorder=5))
        ax.text(x, y, etiqueta, ha="center", va="center", fontsize=12,
                fontweight="bold", color=TINTA_PRIMARIA, zorder=6)

    def conectar(origen, destino, peso, fraccion=0.30, color=None):
        """fraccion: posicion de la etiqueta sobre la flecha (0 = origen, 1 = destino)."""
        x0, y0 = nodos[origen]
        x1, y1 = nodos[destino]
        dx, dy = x1 - x0, y1 - y0
        largo = np.hypot(dx, dy)
        ux, uy = dx / largo, dy / largo
        inicio = (x0 + ux * RADIO, y0 + uy * RADIO)
        final = (x1 - ux * RADIO, y1 - uy * RADIO)
        ax.add_patch(FancyArrowPatch(inicio, final, arrowstyle="-|>",
                                     mutation_scale=13,
                                     color=color or TINTA_SECUNDARIA,
                                     linewidth=1.4, zorder=3))
        ex = inicio[0] + fraccion * (final[0] - inicio[0])
        ey = inicio[1] + fraccion * (final[1] - inicio[1])
        ax.text(ex, ey, peso, ha="center", va="center", fontsize=11,
                fontweight="bold", color=color or TINTA_PRIMARIA, zorder=7,
                bbox=dict(boxstyle="round,pad=0.20", facecolor=SUPERFICIE,
                          edgecolor="none"))

    dibujar_nodo("x0a", "$-1$", TINTA_SECUNDARIA, "#f0efec")
    dibujar_nodo("x1", "$x_1$", TINTA_SECUNDARIA, "#f0efec")
    dibujar_nodo("x2", "$x_2$", TINTA_SECUNDARIA, "#f0efec")
    dibujar_nodo("x0c", "$-1$", TINTA_SECUNDARIA, "#f0efec")
    dibujar_nodo("A", "$A$", COLOR_RECTA_A, "#e6f6f0")
    dibujar_nodo("B", "$B$", COLOR_RECTA_B, "#eceaf6")
    dibujar_nodo("C", "$C$", COLOR_CLASE_POS, "#e4eefa")

    conectar("x0a", "A", "$-1$", 0.20, COLOR_RECTA_A)
    conectar("x0a", "B", "$+1$", 0.42, COLOR_RECTA_B)
    conectar("x1", "A", "$+1$", 0.20, COLOR_RECTA_A)
    conectar("x1", "B", "$+1$", 0.62, COLOR_RECTA_B)
    conectar("x2", "A", "$+1$", 0.62, COLOR_RECTA_A)
    conectar("x2", "B", "$+1$", 0.20, COLOR_RECTA_B)
    conectar("x0c", "C", "$+1$", 0.28, COLOR_CLASE_POS)
    conectar("A", "C", "$+1$", 0.45, COLOR_CLASE_POS)
    conectar("B", "C", "$-1$", 0.45, COLOR_CLASE_POS)

    xc, yc = nodos["C"]
    flecha_salida = FancyArrowPatch((xc + RADIO, yc), (xc + 1.45, yc),
                                    arrowstyle="-|>", mutation_scale=13,
                                    color=TINTA_SECUNDARIA, linewidth=1.4)
    ax.add_patch(flecha_salida)
    ax.text(xc + 1.62, yc, "$y$", fontsize=13, va="center",
            fontweight="bold", color=TINTA_PRIMARIA)

    ax.text(0.4, -0.35, "entrada", ha="center", fontsize=10,
            color=TINTA_SECUNDARIA, style="italic")
    ax.text(4.0, -0.35, "capa oculta", ha="center", fontsize=10,
            color=TINTA_SECUNDARIA, style="italic")
    ax.text(7.4, -0.35, "capa de salida", ha="center", fontsize=10,
            color=TINTA_SECUNDARIA, style="italic")
    ax.set_title("Arquitectura de la red de tres neuronas", fontsize=13,
                 fontweight="bold", pad=10)
    fig.tight_layout()
    fig.savefig("/home/claude/figuras/06-arquitectura.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    figura_problema()
    figura_perceptron_a()
    figura_perceptron_b()
    figura_franjas()
    figura_plano_oculto()
    figura_arquitectura()
    print("figuras generadas")
