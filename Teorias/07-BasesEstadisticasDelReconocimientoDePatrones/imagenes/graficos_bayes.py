"""Figuras y verificaciones del apunte de bases estadisticas del reconocimiento de patrones.

Genera todos los PNG que referencia ../Resumenes/01-bases-estadisticas.md e
imprime las verificaciones numericas que cita el apunte.

    python3 graficos_bayes.py

Las densidades del ejemplo del brillo (0 contra 9) se reconstruyeron para que
reproduzcan los numeros de la lamina 31: P(0) = P(9) = 0,5; p(45|0) = 0,033;
p(45) = 0,054, y los picos de las curvas del dibujo (0,095 y 0,147).
"""

import os
from math import erf, sqrt, pi, exp

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DIRECTORIO_SALIDA = os.path.dirname(os.path.abspath(__file__))

AZUL = "#2a78d6"
ROJO = "#d1495b"
VERDE = "#1baf7a"
NARANJA = "#eb6834"
GRIS = "#8a8f98"
GRIS_CLARO = "#c8ccd2"
TINTA = "#222222"

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
    figura.savefig(os.path.join(DIRECTORIO_SALIDA, nombre_archivo))
    plt.close(figura)
    print("generado:", nombre_archivo)


def apagar_ejes(ejes):
    ejes.grid(False)
    ejes.set_xticks([])
    ejes.set_yticks([])
    for lado in ejes.spines.values():
        lado.set_visible(False)


def titulo(texto):
    print()
    print("=" * 72)
    print(texto)
    print("=" * 72)


# ---------------------------------------------------------------------------
# El ejemplo del brillo: dos gaussianas reconstruidas de la lamina 31
# ---------------------------------------------------------------------------

SIGMA_0 = 1 / (0.095 * sqrt(2 * pi))                         # pico 0,095
MU_0 = 45 - SIGMA_0 * sqrt(-2 * np.log(0.033 / 0.095))       # p(45|0) = 0,033
SIGMA_9 = 1 / (0.147 * sqrt(2 * pi))                         # pico 0,147
MU_9 = 45 + SIGMA_9 * sqrt(-2 * np.log(0.075 / 0.147))       # p(45|9) = 0,075 -> p(45) = 0,054


def gauss(x, mu, sigma):
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * sqrt(2 * pi))


def cdf(x, mu, sigma):
    return 0.5 * (1 + erf((x - mu) / (sigma * sqrt(2))))


def p0(x):
    return gauss(x, MU_0, SIGMA_0)


def p9(x):
    return gauss(x, MU_9, SIGMA_9)


def frontera_bayes(prior0=0.5, desde=MU_0, hasta=MU_9):
    """Punto entre las medias donde P(0)p(x|0) = P(9)p(x|9), por biseccion."""
    f = lambda x: prior0 * p0(x) - (1 - prior0) * p9(x)
    a, b = desde, hasta
    for _ in range(200):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def error_con_umbral(umbral, prior0=0.5):
    """Error de decidir '0' si x < umbral y '9' si no (integral exacta con la normal)."""
    return prior0 * (1 - cdf(umbral, MU_0, SIGMA_0)) + (1 - prior0) * cdf(umbral, MU_9, SIGMA_9)


def verificar_probabilidades():
    titulo("Ejemplo del brillo (lamina 31): las cuatro probabilidades")
    print(f"gaussiana del 0: mu={MU_0:.2f} sigma={SIGMA_0:.2f};  del 9: mu={MU_9:.2f} sigma={SIGMA_9:.2f}")
    x = 45.0
    a0 = 0.5
    c0, c9 = p0(x), p9(x)
    conj0, conj9 = a0 * c0, (1 - a0) * c9
    incond = conj0 + conj9
    print(f"P(0)=0.5  p(45|0)={c0:.4f}  p(45,0)={conj0:.4f}  p(45|9)={c9:.4f}  p(45,9)={conj9:.4f}  p(45)={incond:.4f}")
    print(f"a posteriori en 45: P(0|45)={conj0 / incond:.4f}  P(9|45)={conj9 / incond:.4f}")
    for xx in [30, 35, 40, 42, 43, 44, 46, 50, 55]:
        c0, c9 = p0(xx), p9(xx)
        post0 = c0 / (c0 + c9)
        print(f"  x={xx}: P(0|x)={post0:.4f}  P(9|x)={1 - post0:.4f}  P(error|x)={1 - max(post0, 1 - post0):.4f}")
    xb = frontera_bayes()
    print(f"frontera de Bayes (priors iguales): x* = {xb:.3f}")
    print(f"error de Bayes (integral) = {error_con_umbral(xb):.4f}")
    # integral numerica de P(error|x) p(x) como control
    xs = np.linspace(0, 90, 200001)
    px = 0.5 * p0(xs) + 0.5 * p9(xs)
    perr = 1 - np.maximum(0.5 * p0(xs), 0.5 * p9(xs)) / px
    integrar = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    print(f"control: integral numerica de P(error|x) p(x) dx = {integrar(perr * px, xs):.4f}")
    d = p0(xs) - p9(xs)
    cruces = xs[np.where(np.diff(np.sign(d)))[0]]
    print(f"cruces de p(x|0) = p(x|9): {np.round(cruces, 2)}")
    # otros umbrales
    for u in [40, 42, 44, 45, 46, 48]:
        print(f"  umbral {u}: error = {error_con_umbral(u):.4f}")
    # priors distintos
    for prior0 in [0.5, 0.7, 0.9, 0.99]:
        a, b = prior0 * p0(xs), (1 - prior0) * p9(xs)
        err = integrar(np.minimum(a, b), xs)
        cr = xs[np.where(np.diff(np.sign(a - b)))[0]]
        print(f"  P(0)={prior0}: fronteras {np.round(cr, 2)}, error de Bayes {err:.4f}, "
              f"error del trivial (decir siempre 0) = {1 - prior0:.4f}")


def verificar_ejemplo_lineal_1d():
    titulo("Lamina 26: g0 = (-x+71)/100, g1 = (x-20)/100")
    g0 = lambda x: (-x + 71) / 100
    g1 = lambda x: (x - 20) / 100
    print(f"frontera g0 = g1 -> x = {(71 + 20) / 2}")
    for x in [30, 45, 55]:
        print(f"  x={x}: g0={g0(x):.2f} g1={g1(x):.2f} -> clase {0 if g0(x) > g1(x) else 1}")


def verificar_parametros():
    titulo("Cantidad de parametros: lineal d+1, cuadratico d(d+1)/2 + d + 1")
    for d in [1, 2, 3, 5, 10, 100]:
        print(f"  d={d}: lineal {d + 1}, cuadratico {d * (d + 1) // 2 + d + 1}")
    # control por conteo: W simetrica tiene d(d+1)/2 libres
    d = 3
    libres = len({(min(i, j), max(i, j)) for i in range(d) for j in range(d)})
    print(f"  control d=3: terminos distintos x_i x_j = {libres}")


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------


def figura_01_diagrama():
    figura, ejes = plt.subplots(figsize=(10.5, 3.9))
    apagar_ejes(ejes)
    ejes.set_xlim(0, 10.5)
    ejes.set_ylim(0, 4.2)

    def caja(x, y, texto, ancho=1.75, alto=0.62, punteada=False, color=TINTA, fondo="white"):
        ejes.add_patch(FancyBboxPatch((x - ancho / 2, y - alto / 2), ancho, alto,
                                      boxstyle="round,pad=0.02,rounding_size=0.08", fc=fondo, ec=color,
                                      lw=1.2, ls="--" if punteada else "-"))
        ejes.text(x, y, texto, ha="center", va="center", fontsize=8.5, color=color)

    def flecha(a, b, color=TINTA, estilo="-"):
        ejes.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=color, lw=1.1,
                                       ls=estilo))

    fila = 1.0
    ejes.text(0.35, fila, "patrón\n$\\mathbf{y}\\in\\mathbb{R}^n$", ha="center", va="center", fontsize=9)
    caja(2.2, fila, "Preprocesamiento")
    caja(4.75, fila, "Extracción de\ncaracterísticas")
    caja(7.3, fila, "Clasificación")
    ejes.text(9.75, fila, "clase\n$\\omega_i$", ha="center", va="center", fontsize=9)
    flecha((0.85, fila), (1.3, fila))
    flecha((3.1, fila), (3.85, fila))
    flecha((5.65, fila), (6.4, fila))
    flecha((8.2, fila), (9.3, fila))
    ejes.text(6.02, fila + 0.18, "$\\mathbf{x}\\in\\mathbb{R}^d$", ha="center", fontsize=8.5)

    arriba = 2.55
    caja(2.2, arriba, "Ajuste y\nacondicionamiento", color=AZUL)
    caja(4.75, arriba, "Selección de\ncaracterísticas", color=AZUL, fondo="#eef4fc")
    caja(7.3, arriba, "Diseño del\nclasificador", color=AZUL, fondo="#eef4fc")
    caja(4.75, 3.75, "Conocimiento sobre la tarea", ancho=2.8, alto=0.45, punteada=True, color=GRIS)
    for x in (2.2, 4.75, 7.3):
        flecha((x, arriba - 0.33), (x, fila + 0.33), color=AZUL, estilo="--")
    flecha((4.2, 3.52), (2.6, arriba + 0.33), color=GRIS)
    flecha((4.75, 3.52), (4.75, arriba + 0.33), color=GRIS)
    flecha((5.3, 3.52), (6.9, arriba + 0.33), color=GRIS)
    ejes.plot([0.2, 10.3], [1.78, 1.78], color=GRIS, ls=":", lw=1)
    ejes.text(0.25, 1.87, "ENTRENAMIENTO", fontsize=7.5, color=GRIS, family="monospace")
    ejes.text(0.25, 1.6, "CLASIFICACIÓN", fontsize=7.5, color=GRIS, family="monospace", va="top")
    ejes.text(6.05, 2.55, "van\njuntos", fontsize=7.5, color=AZUL, ha="center", va="center", style="italic")
    guardar(figura, "01-diagrama-de-bloques.png")


def digito_siete():
    imagen = np.zeros((12, 10), dtype=int)
    imagen[1:3, 1:9] = 1                       # barra superior
    for fila in range(3, 11):                  # diagonal hacia abajo a la izquierda
        c = 8 - (fila - 3) * 5 // 8
        imagen[fila, c - 1:c + 1] = 1
    return imagen


DIRECCIONES_8 = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]  # 0..7, (dfila, dcol)


def codigo_de_contorno(imagen):
    """Codigo de cadena de Freeman (8 direcciones) del borde exterior.

    Trazado de Moore: se arranca en el pixel de mas arriba a la izquierda y se
    recorre el borde en sentido horario (en pantalla). Con las direcciones de
    DIRECCIONES_8, 'horario' es ir bajando el indice.
    """
    es_trazo = lambda f, c: 0 <= f < imagen.shape[0] and 0 <= c < imagen.shape[1] and imagen[f, c]
    filas, cols = np.nonzero(imagen)
    inicio = (int(filas.min()), int(cols[filas == filas.min()].min()))
    actual, desde = inicio, 4                  # el 'vecino de fondo' inicial es el de la izquierda
    codigo, camino = [], [inicio]
    for _ in range(1000):
        for k in range(8):
            d = (desde - k) % 8
            df, dc = DIRECCIONES_8[d]
            if es_trazo(actual[0] + df, actual[1] + dc):
                # el vecino de fondo examinado justo antes, visto desde el pixel nuevo
                fa, ca = DIRECCIONES_8[(d + 1) % 8]
                fondo = (actual[0] + fa, actual[1] + ca)
                nuevo = (actual[0] + df, actual[1] + dc)
                desde = DIRECCIONES_8.index((fondo[0] - nuevo[0], fondo[1] - nuevo[1]))
                codigo.append(d)
                actual = nuevo
                camino.append(actual)
                break
        if actual == inicio:
            break
    return codigo, camino


def figura_02_dos_aproximaciones():
    rng = np.random.default_rng(3)
    figura, (ejes_g, ejes_s) = plt.subplots(1, 2, figsize=(11.0, 4.3),
                                           gridspec_kw={"width_ratios": [1.15, 1]})
    medias = {"0": (170, 165), "6": (205, 135), "9": (135, 205)}
    colores = {"0": GRIS, "6": AZUL, "9": ROJO}
    for digito, (mx, my) in medias.items():
        puntos = rng.multivariate_normal([mx, my], [[380, 150], [150, 380]], 300)
        ejes_g.scatter(puntos[:, 0], puntos[:, 1], s=6, color=colores[digito], alpha=0.55,
                       label=f"dígito {digito}")
    xs = np.linspace(60, 260, 10)
    ejes_g.plot(xs, xs + 15, color=VERDE, lw=1.6)
    ejes_g.plot(xs, xs - 15, color=VERDE, lw=1.6)
    ejes_g.set_xlim(70, 260)
    ejes_g.set_ylim(70, 260)
    ejes_g.set_xlabel("brillo de la mitad superior $x_1$")
    ejes_g.set_ylabel("brillo de la mitad inferior $x_2$")
    ejes_g.set_title("Geométrica: el patrón es un punto de $\\mathbb{R}^2$")
    ejes_g.legend(fontsize=8, loc="upper right")
    ejes_g.text(95, 240, "región del 9", color=ROJO, fontsize=8)
    ejes_g.text(228, 88, "región\ndel 6", color=AZUL, fontsize=8)

    imagen = digito_siete()
    codigo, camino = codigo_de_contorno(imagen)
    apagar_ejes(ejes_s)
    ejes_s.imshow(1 - imagen, cmap="gray", vmin=-0.4, vmax=1, extent=(-0.5, imagen.shape[1] - 0.5,
                                                                    imagen.shape[0] - 0.5, -0.5))
    cam = np.array(camino)
    ejes_s.plot(cam[:, 1], cam[:, 0], "-", color=NARANJA, lw=1.4)
    ejes_s.plot(cam[0, 1], cam[0, 0], "o", color=NARANJA, ms=6)
    # rosa de direcciones
    ox, oy = 13.3, 2.2
    for d, (df, dc) in enumerate(DIRECCIONES_8):
        ejes_s.annotate("", xy=(ox + dc * 1.1, oy + df * 1.1), xytext=(ox, oy),
                        arrowprops=dict(arrowstyle="-|>", color=TINTA, lw=0.8))
        ejes_s.text(ox + dc * 1.6, oy + df * 1.6, str(d), ha="center", va="center", fontsize=8)
    ejes_s.set_xlim(-0.8, 15.5)
    ejes_s.set_ylim(12.5, -1.0)
    cadena = "".join(str(c) for c in codigo)
    partes = [cadena[i:i + 26] for i in range(0, len(cadena), 26)]
    ejes_s.text(7.3, 7.0, "cadena:\n" + "\n".join(partes), fontsize=7.6, family="monospace", va="top")
    ejes_s.set_title("Sintáctica: el patrón es una cadena de símbolos")
    guardar(figura, "02-dos-aproximaciones.png")
    return cadena


def figura_03_maquina():
    figura, ejes = plt.subplots(figsize=(9.0, 3.2))
    apagar_ejes(ejes)
    ejes.set_xlim(0, 9)
    ejes.set_ylim(-0.35, 3.4)
    ejes.text(0.6, 1.7, "$\\mathbf{x}\\in E$", ha="center", va="center", fontsize=11)
    alturas = [2.8, 2.0, 0.6]
    etiquetas = ["$g_1(\\mathbf{x})$", "$g_2(\\mathbf{x})$", "$g_c(\\mathbf{x})$"]
    valores = ["0,2", "0,8", "…"]
    for y, e, v in zip(alturas, etiquetas, valores):
        ejes.add_patch(FancyBboxPatch((2.4, y - 0.28), 1.6, 0.56, boxstyle="round,pad=0.02", fc="white",
                                      ec=TINTA))
        ejes.text(3.2, y, e, ha="center", va="center", fontsize=10)
        ejes.add_patch(FancyArrowPatch((1.0, 1.7), (2.35, y), arrowstyle="-|>", mutation_scale=10,
                                       color=TINTA))
        ejes.add_patch(FancyArrowPatch((4.05, y), (5.55, 1.7), arrowstyle="-|>", mutation_scale=10,
                                       color=TINTA))
        ejes.text(4.5, y + 0.12, v, fontsize=8, color=AZUL)
    ejes.text(3.2, 1.35, "$\\vdots$", ha="center", fontsize=12)
    ejes.add_patch(FancyBboxPatch((5.6, 1.35), 1.2, 0.7, boxstyle="round,pad=0.02", fc="#eef4fc", ec=AZUL))
    ejes.text(6.2, 1.7, "máx", ha="center", va="center", fontsize=11, color=AZUL)
    ejes.add_patch(FancyArrowPatch((6.85, 1.7), (7.8, 1.7), arrowstyle="-|>", mutation_scale=10,
                                   color=TINTA))
    ejes.text(8.35, 1.7, "$\\omega_2$", ha="center", va="center", fontsize=12)
    ejes.text(0.6, -0.25, "ej. anemia: conteo de glóbulos rojos → $g_{sano}=0{,}2$, $g_{enfermo}=0{,}8$ "
                         "→ «enfermo»", fontsize=8, color=GRIS)
    guardar(figura, "03-maquina-de-funciones-discriminantes.png")


def figura_04_lineal_cuadratico():
    rng = np.random.default_rng(7)
    m1, S1 = np.array([-1.0, 0.0]), np.array([[0.6, 0.0], [0.0, 0.6]])
    m2, S2 = np.array([1.2, 0.3]), np.array([[2.2, 0.9], [0.9, 0.8]])
    A = rng.multivariate_normal(m1, S1, 200)
    B = rng.multivariate_normal(m2, S2, 200)
    xx, yy = np.meshgrid(np.linspace(-4, 5, 400), np.linspace(-3.5, 3.5, 400))
    P = np.c_[xx.ravel(), yy.ravel()]

    def g_gauss(P, m, S):
        Si = np.linalg.inv(S)
        d = P - m
        return -0.5 * np.einsum("ij,jk,ik->i", d, Si, d) - 0.5 * np.log(np.linalg.det(S))

    ma, mb = A.mean(0), B.mean(0)
    Sa, Sb = np.cov(A.T), np.cov(B.T)
    Sp = (Sa + Sb) / 2
    lineal = (g_gauss(P, ma, Sp) - g_gauss(P, mb, Sp)).reshape(xx.shape)
    cuad = (g_gauss(P, ma, Sa) - g_gauss(P, mb, Sb)).reshape(xx.shape)
    figura, ejes_l = plt.subplots(1, 2, figsize=(10.5, 4.0))
    for ejes, campo, nombre, par in ((ejes_l[0], lineal, "Lineal: frontera = hiperplano", "$d+1 = 3$"),
                                     (ejes_l[1], cuad, "Cuadrático: frontera = hipercuádrica",
                                      "$\\frac{1}{2} d(d+1)+d+1 = 6$")):
        ejes.contourf(xx, yy, campo > 0, levels=[-0.5, 0.5, 1.5], colors=["#fbe3e6", "#e3eefb"], alpha=0.8)
        ejes.contour(xx, yy, campo, levels=[0], colors=[TINTA], linewidths=1.5)
        ejes.scatter(A[:, 0], A[:, 1], s=7, color=AZUL, alpha=0.7, label="$\\omega_1$")
        ejes.scatter(B[:, 0], B[:, 1], s=7, color=ROJO, alpha=0.7, label="$\\omega_2$")
        ejes.set_title(nombre)
        ejes.text(-3.8, -3.2, "parámetros por función ($d=2$): " + par, fontsize=8)
        ejes.set_xlabel("$x_1$")
        ejes.set_ylabel("$x_2$")
        err = np.mean(np.r_[(campo.ravel()[0:1] * 0)]) if False else None
    ejes_l[0].legend(fontsize=8, loc="upper left")

    def tasa(fun):
        ga = fun(A)
        gb = fun(B)
        return (np.sum(ga <= 0) + np.sum(gb > 0)) / (len(A) + len(B))

    e_lin = tasa(lambda Q: g_gauss(Q, ma, Sp) - g_gauss(Q, mb, Sp))
    e_cua = tasa(lambda Q: g_gauss(Q, ma, Sa) - g_gauss(Q, mb, Sb))
    guardar(figura, "04-lineal-y-cuadratico.png")


def figura_05_brillo_1d():
    rng = np.random.default_rng(11)
    ceros = rng.normal(37, 5.0, 220)
    unos = rng.normal(51, 2.5, 220)
    figura, ejes = plt.subplots(figsize=(7.4, 3.8))
    bins = np.arange(20, 61, 1)
    h0, _ = np.histogram(ceros, bins)
    h1, _ = np.histogram(unos, bins)
    ejes.bar(bins[:-1] + 0.5, h0 / h0.sum(), width=0.9, color=ROJO, alpha=0.55, label="ceros")
    ejes.bar(bins[:-1] + 0.5, h1 / h1.sum(), width=0.9, color=AZUL, alpha=0.55, label="unos")
    x = np.linspace(20, 60, 100)
    ejes.plot(x, (-x + 71) / 100, color=ROJO, lw=1.8, label="$g_0(x) = (-x+71)/100$")
    ejes.plot(x, (x - 20) / 100, color=AZUL, lw=1.8, label="$g_1(x) = (x-20)/100$")
    ejes.axvline(45.5, color=TINTA, ls="--", lw=1)
    ejes.text(45.8, 0.37, "frontera\n$x = 45{,}5$", fontsize=8)
    ejes.plot([55, 55], [0, 0.35], color=GRIS, lw=0.8, ls=":")
    ejes.plot(55, 0.35, "o", color=AZUL, ms=4)
    ejes.plot(55, 0.16, "o", color=ROJO, ms=4)
    ejes.text(55.6, 0.33, "$g_1(55)=0{,}35$", fontsize=7.5, color=AZUL)
    ejes.text(55.6, 0.14, "$g_0(55)=0{,}16$", fontsize=7.5, color=ROJO)
    ejes.set_xlim(20, 62)
    ejes.set_ylim(0, 0.45)
    ejes.set_xlabel("$x$ (brillo global)")
    ejes.set_ylabel("frecuencia relativa")
    ejes.set_title("Reconstrucción de la lámina 26: una característica, dos clases")
    ejes.legend(fontsize=7.5, loc="upper left")
    guardar(figura, "05-brillo-una-dimension.png")


def figura_06_cuatro_probabilidades():
    x = np.linspace(20, 60, 800)
    figura, (ejes_c, ejes_j) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    ejes_c.plot(x, p0(x), color=ROJO, lw=1.7, label="$p(x|0)$")
    ejes_c.plot(x, p9(x), color=AZUL, lw=1.7, label="$p(x|9)$")
    ejes_c.set_title("Densidades condicionales ($P(0)=P(9)=0{,}5$)")
    ejes_c.axvline(45, color=GRIS, ls=":", lw=1)
    ejes_c.plot(45, p0(45), "o", color=ROJO, ms=5)
    ejes_c.annotate(f"$p(45|0) = {p0(45):.3f}$".replace(".", "{,}"), (45, p0(45)), (48.5, 0.03),
                    fontsize=8, color=ROJO, arrowprops=dict(arrowstyle="-", color=ROJO, lw=0.7))
    ejes_c.set_ylim(0, 0.2)
    ejes_c.legend(fontsize=8)
    ejes_c.set_xlabel("$x$ (brillo global)")

    ejes_j.plot(x, 0.5 * p0(x), color=ROJO, lw=1.5, label="$p(x,0) = P(0)\\,p(x|0)$")
    ejes_j.plot(x, 0.5 * p9(x), color=AZUL, lw=1.5, label="$p(x,9) = P(9)\\,p(x|9)$")
    ejes_j.plot(x, 0.5 * p0(x) + 0.5 * p9(x), color=TINTA, lw=1.8, label="$p(x) = p(x,0)+p(x,9)$")
    ejes_j.axvline(45, color=GRIS, ls=":", lw=1)
    for val, col in ((0.5 * p0(45), ROJO), (0.5 * p0(45) + 0.5 * p9(45), TINTA)):
        ejes_j.plot(45, val, "o", color=col, ms=5)
    ejes_j.text(45.6, 0.5 * p0(45) - 0.004, "0,0165", fontsize=8, color=ROJO)
    ejes_j.text(45.6, 0.5 * p0(45) + 0.5 * p9(45) + 0.002, "0,054", fontsize=8, color=TINTA)
    ejes_j.set_ylim(0, 0.1)
    ejes_j.set_title("Conjuntas e incondicional")
    ejes_j.legend(fontsize=7.8, loc="upper left")
    ejes_j.set_xlabel("$x$ (brillo global)")
    guardar(figura, "06-cuatro-probabilidades.png")


def figura_07_a_posteriori():
    x = np.linspace(20, 60, 800)
    px = 0.5 * p0(x) + 0.5 * p9(x)
    post0 = 0.5 * p0(x) / px
    post9 = 0.5 * p9(x) / px
    xb = frontera_bayes()
    figura, (ejes_p, ejes_e) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    ejes_p.plot(x, post0, color=ROJO, lw=1.8, label="$P(0|x)$")
    ejes_p.plot(x, post9, color=AZUL, lw=1.8, label="$P(9|x)$")
    ejes_p.axvline(xb, color=TINTA, ls="--", lw=1)
    ejes_p.text(xb + 0.4, 0.52, f"frontera\n$x^* = {xb:.1f}$".replace(".", "{,}"), fontsize=8)
    ejes_p.fill_between(x, 0, 1, where=x < xb, color=ROJO, alpha=0.06)
    ejes_p.fill_between(x, 0, 1, where=x >= xb, color=AZUL, alpha=0.06)
    ejes_p.text(24, 0.9, "$R_0$: se decide 0", fontsize=8, color=ROJO)
    ejes_p.text(50, 0.9, "$R_9$", fontsize=8, color=AZUL)
    ejes_p.set_title("Probabilidades a posteriori")
    ejes_p.set_ylim(-0.02, 1.02)
    ejes_p.legend(fontsize=8, loc="center left")
    ejes_p.set_xlabel("$x$ (brillo global)")

    perr = 1 - np.maximum(post0, post9)
    ejes_e.plot(x, perr, color=NARANJA, lw=1.8, label="$P(error|x) = 1 - \\max_i P(\\omega_i|x)$")
    ejes_e.fill_between(x, 0, np.minimum(0.5 * p0(x), 0.5 * p9(x)) * 8, color=GRIS, alpha=0.35,
                        label="$P(error|x)\\,p(x)$ (×8)")
    for xx in (30, 40):
        valor = 1 - max(0.5 * p0(xx), 0.5 * p9(xx)) / (0.5 * p0(xx) + 0.5 * p9(xx))
        ejes_e.plot(xx, valor, "o", color=NARANJA, ms=5)
        ejes_e.text(xx, valor + 0.03, f"{valor:.2f}".replace(".", ","), ha="center", fontsize=8)
    ejes_e.axvline(xb, color=TINTA, ls="--", lw=1)
    ejes_e.set_ylim(0, 0.6)
    ejes_e.set_title(f"Error puntual; el área gris es el error de Bayes = {error_con_umbral(xb):.3f}".replace(".", ","))
    ejes_e.legend(fontsize=7.8, loc="upper left")
    ejes_e.set_xlabel("$x$ (brillo global)")
    guardar(figura, "07-a-posteriori-y-error.png")


def figura_08_umbral_y_priori():
    umbrales = np.linspace(36, 54, 400)
    figura, (ejes_u, ejes_p) = plt.subplots(1, 2, figsize=(11.0, 3.8))
    errores = [error_con_umbral(u) for u in umbrales]
    xb = frontera_bayes()
    ejes_u.plot(umbrales, errores, color=AZUL, lw=1.8)
    ejes_u.plot(xb, error_con_umbral(xb), "o", color=ROJO, ms=6)
    ejes_u.annotate(f"Bayes: $x^*$ = {xb:.2f}\nerror = {error_con_umbral(xb):.4f}".replace(".", ","),
                    (xb, error_con_umbral(xb)), (37.0, 0.44), fontsize=8,
                    arrowprops=dict(arrowstyle="-", color=ROJO, lw=0.8))
    ejes_u.set_xlabel("umbral $u$ (decidir 0 si $x<u$)")
    ejes_u.set_ylabel("probabilidad de error")
    ejes_u.set_title("Ningún umbral le gana al de Bayes")

    x = np.linspace(20, 60, 800)
    for prior0, color in ((0.5, TINTA), (0.9, VERDE), (0.99, NARANJA)):
        num0 = prior0 * p0(x)
        num9 = (1 - prior0) * p9(x)
        ejes_p.plot(x, num0 / (num0 + num9), color=color, lw=1.6, label=f"$P(0|x)$ con $P(0)={prior0}$")
        cruces = x[np.where(np.diff(np.sign(num0 - num9)))[0]]
        for xb2 in cruces:
            ejes_p.axvline(xb2, color=color, ls=":", lw=1)
    ejes_p.set_title("Si cambia la a priori, se corre la frontera")
    ejes_p.set_xlabel("$x$ (brillo global)")
    ejes_p.legend(fontsize=7.8, loc="lower left")
    guardar(figura, "08-umbral-y-a-priori.png")


def main():
    verificar_probabilidades()
    verificar_ejemplo_lineal_1d()
    verificar_parametros()
    titulo("Figuras")
    figura_01_diagrama()
    cadena = figura_02_dos_aproximaciones()
    print("cadena del 7:", cadena)
    figura_03_maquina()
    figura_04_lineal_cuadratico()
    figura_05_brillo_1d()
    figura_06_cuatro_probabilidades()
    figura_07_a_posteriori()
    figura_08_umbral_y_priori()


if __name__ == "__main__":
    main()
