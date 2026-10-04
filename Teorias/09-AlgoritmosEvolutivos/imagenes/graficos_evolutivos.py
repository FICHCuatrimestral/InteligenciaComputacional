"""Figuras y verificaciones de los apuntes de la unidad 09.

Genera todos los PNG que referencian ../Resumenes/01-inteligencia-colectiva.md y
../Resumenes/02-algoritmos-evolutivos.md, e imprime los numeros que citan los
apuntes. Trae una implementacion propia de un algoritmo genetico binario
(seleccion por ruleta, ventanas o competencia; cruza simple; mutacion por gen;
reemplazo total, brecha generacional o elitismo) de unas 120 lineas.

    python3 graficos_evolutivos.py

Solo usa numpy y matplotlib. Tarda alrededor de dos minutos.
"""

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Circle, RegularPolygon, Wedge

DIRECTORIO_SALIDA = os.path.dirname(os.path.abspath(__file__))

AZUL = "#2a78d6"
ROJO = "#d1495b"
VERDE = "#1baf7a"
NARANJA = "#eb6834"
VIOLETA = "#7b5cc4"
GRIS = "#8a8f98"
GRIS_CLARO = "#c8ccd2"
TINTA = "#222222"
FONDO_AZUL = "#e3eefb"
FONDO_ROJO = "#fbe3e6"
FONDO_VERDE = "#ddf3ea"
FONDO_NARANJA = "#fdeadf"

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


def caja(ejes, x, y, texto, ancho=1.6, alto=0.55, fondo=FONDO_AZUL, borde=AZUL, tam=8.5, negrita=False):
    ejes.add_patch(
        FancyBboxPatch(
            (x - ancho / 2, y - alto / 2), ancho, alto,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=fondo, edgecolor=borde, linewidth=1.1,
        )
    )
    ejes.text(x, y, texto, ha="center", va="center", fontsize=tam,
              color=TINTA, fontweight="bold" if negrita else "normal")


def flecha(ejes, x0, y0, x1, y1, color=TINTA, texto=None, curva=0.0, tam=8, desplazamiento=(0, 0.12)):
    ejes.add_patch(
        FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=11,
                        color=color, linewidth=1.1, connectionstyle=f"arc3,rad={curva}")
    )
    if texto:
        ejes.text((x0 + x1) / 2 + desplazamiento[0], (y0 + y1) / 2 + desplazamiento[1], texto,
                  ha="center", va="center", fontsize=tam, color=color)


# ===========================================================================
# Funciones de prueba
# ===========================================================================


def funcion_ejemplo_1(x, y):
    """Superficie con minimos locales concentricos y el global en el origen.

    Es la forma de la diapositiva «Ejemplo 1». Se minimiza en [-100, 100]^2.
    """
    r2 = x ** 2 + y ** 2
    return r2 ** 0.25 * (np.sin(50.0 * r2 ** 0.1) ** 2 + 1.0)


def funcion_escalones(x, y):
    """Piramide invertida de escalones planos (la forma del «Ejemplo 2»)."""
    return np.floor(np.abs(x) / 10.0) + np.floor(np.abs(y) / 10.0)


def rastrigin(x):
    x = np.asarray(x, dtype=float)
    return 10.0 * x.shape[-1] + np.sum(x ** 2 - 10.0 * np.cos(2 * np.pi * x), axis=-1)


# ===========================================================================
# Codificacion binaria
# ===========================================================================


def decodificar(cromosomas, n_variables, bits_por_variable, minimo, maximo):
    """x = a + (b - a) * entero / (2^L - 1), variable por variable."""
    cromosomas = np.atleast_2d(cromosomas)
    potencias = 2 ** np.arange(bits_por_variable - 1, -1, -1)
    enteros = cromosomas.reshape(cromosomas.shape[0], n_variables, bits_por_variable) @ potencias
    return minimo + (maximo - minimo) * enteros / (2 ** bits_por_variable - 1)


def codificar(valores, bits_por_variable, minimo, maximo):
    """Inversa de decodificar (redondeando al entero mas cercano)."""
    valores = np.atleast_2d(valores)
    enteros = np.rint((np.clip(valores, minimo, maximo) - minimo) / (maximo - minimo) * (2 ** bits_por_variable - 1)).astype(np.int64)
    bits = (enteros[..., None] >> np.arange(bits_por_variable - 1, -1, -1)) & 1
    return bits.reshape(valores.shape[0], -1).astype(np.int8)


def a_gray(entero):
    return entero ^ (entero >> 1)


def hamming(a, b):
    return bin(a ^ b).count("1")


# ===========================================================================
# Operadores de seleccion
# ===========================================================================


def seleccion_ruleta(aptitudes, cantidad, generador):
    probabilidades = aptitudes / aptitudes.sum()
    acumulada = np.cumsum(probabilidades)
    tiradas = generador.random(cantidad)
    return np.searchsorted(acumulada, tiradas * acumulada[-1])


def seleccion_ventanas(aptitudes, cantidad, generador, ventana_minima=None):
    orden = np.argsort(-aptitudes)                 # de mayor a menor aptitud
    n = len(aptitudes)
    if ventana_minima is None:
        ventana_minima = max(2, n // 10)
    ventanas = np.linspace(n, ventana_minima, cantidad).round().astype(int)
    return np.array([orden[generador.integers(0, ventana)] for ventana in ventanas])


def seleccion_competencia(aptitudes, cantidad, generador, k=2):
    n = len(aptitudes)
    elegidos = np.empty(cantidad, dtype=int)
    for i in range(cantidad):
        competidores = generador.choice(n, size=k, replace=False)
        elegidos[i] = competidores[np.argmax(aptitudes[competidores])]
    return elegidos


# ===========================================================================
# Algoritmo genetico binario
# ===========================================================================


def algoritmo_genetico(
    aptitud,                 # funcion: matriz de cromosomas -> vector de aptitudes (mayor es mejor)
    longitud,
    generador,
    individuos=100,
    generaciones=200,
    probabilidad_cruza=0.9,
    probabilidad_mutacion=None,  # por gen; por defecto 1/longitud
    seleccion="competencia",
    reemplazo="elitismo",        # "total", "brecha" o "elitismo"
    brecha=0.2,
    aptitud_requerida=np.inf,
    mejora_local=None,           # funcion opcional (cromosomas -> cromosomas, aptitudes)
    lamarck=True,
):
    if probabilidad_mutacion is None:
        probabilidad_mutacion = 1.0 / longitud
    poblacion = generador.integers(0, 2, size=(individuos, longitud), dtype=np.int8)
    aptitudes = aptitud(poblacion)
    historia_mejor, historia_media, evaluaciones = [], [], [individuos]
    for generacion in range(generaciones):
        if mejora_local is not None:
            mejorados, aptitudes_mejoradas, costo = mejora_local(poblacion)
            evaluaciones[-1] += costo
            if lamarck:
                poblacion = mejorados          # lo aprendido se escribe en los genes
            aptitudes = aptitudes_mejoradas    # en los dos casos se selecciona por lo aprendido
        historia_mejor.append(aptitudes.max())
        historia_media.append(aptitudes.mean())
        if aptitudes.max() >= aptitud_requerida:
            break

        if reemplazo == "brecha":
            sobrevivientes = int(round(brecha * individuos))
        elif reemplazo == "elitismo":
            sobrevivientes = 1
        else:
            sobrevivientes = 0
        hijos_necesarios = individuos - sobrevivientes

        operador = {"ruleta": seleccion_ruleta, "ventanas": seleccion_ventanas,
                    "competencia": seleccion_competencia}[seleccion]
        if seleccion == "ruleta":
            base = aptitudes - aptitudes.min() + 1e-9   # la ruleta necesita valores positivos
            padres = operador(base, hijos_necesarios + 1, generador)
        else:
            padres = operador(aptitudes, hijos_necesarios + 1, generador)

        hijos = poblacion[padres].copy()
        for i in range(0, hijos_necesarios, 2):
            if generador.random() < probabilidad_cruza:
                punto = generador.integers(1, longitud)
                cola = hijos[i, punto:].copy()
                hijos[i, punto:] = hijos[i + 1, punto:]
                hijos[i + 1, punto:] = cola
        hijos = hijos[:hijos_necesarios]
        mascara = generador.random(hijos.shape) < probabilidad_mutacion
        hijos[mascara] ^= 1

        if reemplazo == "brecha":
            quedan = seleccion_competencia(aptitudes, sobrevivientes, generador)
            poblacion = np.vstack([poblacion[quedan], hijos])
        elif reemplazo == "elitismo":
            poblacion = np.vstack([poblacion[np.argmax(aptitudes)][None, :], hijos])
        else:
            poblacion = hijos
        aptitudes = aptitud(poblacion)
        evaluaciones.append(evaluaciones[-1] + hijos_necesarios)
    return poblacion, aptitudes, np.array(historia_mejor), np.array(historia_media), np.array(evaluaciones)


# ===========================================================================
# 01 — Inteligencia colectiva
# ===========================================================================


def figura_automata():
    figura, (eje_a, eje_b, eje_c) = plt.subplots(1, 3, figsize=(10.5, 3.0), gridspec_kw={"width_ratios": [1.25, 1, 1]})
    for eje in (eje_a, eje_b, eje_c):
        apagar_ejes(eje)
        eje.set_aspect("equal")

    # Grafo de estados
    eje_a.set_xlim(-0.6, 4.6)
    eje_a.set_ylim(-1.2, 1.6)
    posiciones = {1: (0.3, 0.2), 2: (1.9, 1.0), 3: (1.9, -0.6), 4: (3.6, 0.2)}
    for estado, (x, y) in posiciones.items():
        eje_a.add_patch(Circle((x, y), 0.33, facecolor=FONDO_AZUL, edgecolor=AZUL, linewidth=1.2))
        if estado == 4:
            eje_a.add_patch(Circle((x, y), 0.26, facecolor="none", edgecolor=AZUL, linewidth=1.0))
        eje_a.text(x, y, str(estado), ha="center", va="center", fontsize=10, fontweight="bold")
    eje_a.annotate("", xy=(0.3 - 0.33, 0.2), xytext=(-0.55, 0.2), arrowprops=dict(arrowstyle="-|>", color=TINTA))
    eje_a.text(-0.5, 0.42, "inicio", fontsize=7.5)
    flecha(eje_a, 0.6, 0.38, 1.6, 0.86)
    flecha(eje_a, 1.7, 0.72, 0.62, 0.12, curva=0.45)
    flecha(eje_a, 0.6, 0.02, 1.6, -0.5)
    flecha(eje_a, 2.2, -0.45, 3.32, 0.06)
    flecha(eje_a, 2.2, 0.86, 3.32, 0.36)
    eje_a.add_patch(FancyArrowPatch((0.1, 0.48), (0.5, 0.48), connectionstyle="arc3,rad=-1.6",
                                    arrowstyle="-|>", mutation_scale=10, color=TINTA))
    eje_a.text(0.3, 0.95, "se queda", fontsize=7.5, ha="center")
    eje_a.text(4.0, -0.25, "final", fontsize=7.5, ha="center")
    eje_a.set_title("Estados y transiciones (un grafo)")

    # Regla determinista
    eje_b.set_xlim(-0.4, 3.2)
    eje_b.set_ylim(-1.2, 1.6)
    for estado, (x, y) in {1: (0.2, 0.2), 3: (2.6, 0.2)}.items():
        eje_b.add_patch(Circle((x, y), 0.33, facecolor=FONDO_AZUL, edgecolor=AZUL, linewidth=1.2))
        eje_b.text(x, y, str(estado), ha="center", va="center", fontsize=10, fontweight="bold")
    flecha(eje_b, 0.55, 0.2, 2.25, 0.2, texto="si  $x > 5$", desplazamiento=(0, 0.22))
    eje_b.text(1.4, -0.75, "siempre que $x>5$ pasa a 3", ha="center", fontsize=8, color=GRIS)
    eje_b.set_title("Regla determinista")

    # Regla probabilistica
    eje_c.set_xlim(-0.4, 3.2)
    eje_c.set_ylim(-1.2, 1.6)
    for estado, (x, y) in {1: (0.2, 0.2), 3: (2.6, 1.0), 4: (2.6, -0.6)}.items():
        eje_c.add_patch(Circle((x, y), 0.33, facecolor=FONDO_AZUL, edgecolor=AZUL, linewidth=1.2))
        eje_c.text(x, y, str(estado), ha="center", va="center", fontsize=10, fontweight="bold")
    flecha(eje_c, 0.5, 0.35, 2.28, 0.92, texto="0,1", desplazamiento=(-0.1, 0.2))
    flecha(eje_c, 0.5, 0.05, 2.28, -0.52, texto="0,9", desplazamiento=(-0.1, -0.22))
    eje_c.text(1.4, -1.1, "se sortea: va a 4 casi siempre,\npero no siempre", ha="center", fontsize=8, color=GRIS)
    eje_c.set_title("Regla probabilística")
    guardar(figura, "c1-automata-y-reglas.png")


def figura_vecindades():
    figura, ejes = plt.subplots(1, 4, figsize=(10.5, 2.9))
    casos = [("von Neumann, radio 1", "vn", 1), ("von Neumann, radio 2", "vn", 2),
             ("Moore, radio 1", "moore", 1), ("Moore, radio 2", "moore", 2)]
    for eje, (nombre, tipo, radio) in zip(ejes, casos):
        apagar_ejes(eje)
        eje.set_aspect("equal")
        cuenta = 0
        for i in range(-3, 4):
            for j in range(-3, 4):
                distancia = abs(i) + abs(j) if tipo == "vn" else max(abs(i), abs(j))
                if i == 0 and j == 0:
                    color, borde = AZUL, AZUL
                elif distancia <= radio:
                    color, borde = FONDO_AZUL, AZUL
                    cuenta += 1
                else:
                    color, borde = "white", GRIS_CLARO
                eje.add_patch(Rectangle((i - 0.5, j - 0.5), 1, 1, facecolor=color, edgecolor=borde, linewidth=0.8))
        eje.set_xlim(-3.6, 3.6)
        eje.set_ylim(-3.6, 3.6)
        eje.set_title(f"{nombre}\n{cuenta} vecinos", fontsize=9)
        print(f"  {nombre}: {cuenta} vecinos")
    guardar(figura, "c2-vecindades.png")


def figura_topologias():
    figura, ejes = plt.subplots(1, 3, figsize=(9.0, 2.8))
    for eje in ejes:
        apagar_ejes(eje)
        eje.set_aspect("equal")
    # Rectangular
    eje = ejes[0]
    for i in range(5):
        for j in range(5):
            eje.add_patch(Rectangle((i, j), 1, 1, facecolor=FONDO_AZUL if (abs(i - 2) + abs(j - 2) == 1) else "white",
                                    edgecolor=AZUL, linewidth=0.8))
    eje.add_patch(Rectangle((2, 2), 1, 1, facecolor=AZUL, edgecolor=AZUL))
    eje.set_xlim(-0.2, 5.2); eje.set_ylim(-0.2, 5.2)
    eje.set_title("Rectangular (4 vecinos de lado)")
    # Triangular
    eje = ejes[1]
    alto = np.sqrt(3) / 2
    centro = (2, 1)
    for fila in range(4):
        for col in range(-1, 9):
            x0 = col * 0.5
            y0 = fila * alto
            arriba = (col + fila) % 2 == 0
            if arriba:
                puntos = [(x0, y0), (x0 + 1, y0), (x0 + 0.5, y0 + alto)]
            else:
                puntos = [(x0, y0 + alto), (x0 + 1, y0 + alto), (x0 + 0.5, y0)]
            color = "white"
            if (col, fila) == (4, 2):
                color = AZUL
            elif (col, fila) in [(3, 2), (5, 2), (4, 1)]:
                color = FONDO_AZUL
            eje.add_patch(Polygon(puntos, closed=True, facecolor=color, edgecolor=AZUL, linewidth=0.8))
    eje.set_xlim(-0.2, 5.2); eje.set_ylim(-0.2, 4 * alto + 0.2)
    eje.set_title("Triangular (3 vecinos de lado)")
    # Hexagonal
    eje = ejes[2]
    radio = 0.55
    xc = 2 * np.sqrt(3) * radio
    yc = 2 * 1.5 * radio
    for fila in range(5):
        for col in range(5):
            x = col * np.sqrt(3) * radio + (fila % 2) * np.sqrt(3) * radio / 2
            y = fila * 1.5 * radio
            distancia = np.hypot(x - xc, y - yc)
            vecino = 0.1 < distancia < 1.1 * np.sqrt(3) * radio
            color = AZUL if distancia < 0.1 else (FONDO_AZUL if vecino else "white")
            eje.add_patch(RegularPolygon((x, y), 6, radius=radio, orientation=0, facecolor=color, edgecolor=AZUL, linewidth=0.8))
    eje.set_xlim(-0.8, 5.3); eje.set_ylim(-0.8, 6.8 * radio)
    eje.set_title("Hexagonal (6 vecinos, como el SOM)")
    guardar(figura, "c3-topologias.png")


def paso_vida(grilla):
    vecinos = sum(np.roll(np.roll(grilla, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0))
    return ((grilla == 1) & ((vecinos == 2) | (vecinos == 3))) | ((grilla == 0) & (vecinos == 3))


def figura_juego_de_la_vida():
    titulo("Juego de la vida: el planeador")
    grilla = np.zeros((8, 8), dtype=int)
    for (i, j) in [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]:
        grilla[i, j] = 1
    estados = [grilla.copy()]
    for _ in range(4):
        grilla = paso_vida(grilla).astype(int)
        estados.append(grilla.copy())
    desplazado = np.roll(np.roll(estados[0], 1, 0), 1, 1)
    print("  despues de 4 pasos el planeador es el mismo, corrido una celda en diagonal:",
          bool(np.array_equal(estados[4], desplazado)))
    figura, ejes = plt.subplots(1, 5, figsize=(10.5, 2.4))
    for paso, (eje, estado) in enumerate(zip(ejes, estados)):
        apagar_ejes(eje)
        eje.set_aspect("equal")
        for i in range(8):
            for j in range(8):
                eje.add_patch(Rectangle((j, 7 - i), 1, 1, facecolor=TINTA if estado[i, j] else "white",
                                        edgecolor=GRIS_CLARO, linewidth=0.6))
        eje.set_xlim(0, 8); eje.set_ylim(0, 8)
        eje.set_title(f"paso {paso}")
    guardar(figura, "c4-planeador.png")


def figura_agente():
    figura, eje = plt.subplots(figsize=(7.5, 2.8))
    apagar_ejes(eje)
    eje.set_xlim(0, 10)
    eje.set_ylim(0, 3.6)
    eje.add_patch(FancyBboxPatch((0.2, 0.2), 9.6, 3.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                                 facecolor="#f6f7f9", edgecolor=GRIS, linewidth=1.0))
    eje.text(9.6, 3.1, "AMBIENTE", ha="right", fontsize=9, color=GRIS, fontweight="bold")
    caja(eje, 5.0, 1.8, "AGENTE\npercibir · conocer\ndecidir · actuar", ancho=2.6, alto=1.3, negrita=False, tam=9)
    caja(eje, 1.6, 1.8, "sensores", ancho=1.5, alto=0.6, fondo=FONDO_VERDE, borde=VERDE)
    caja(eje, 8.4, 1.8, "efectores", ancho=1.5, alto=0.6, fondo=FONDO_NARANJA, borde=NARANJA)
    flecha(eje, 2.35, 1.8, 3.7, 1.8, texto="percepciones", desplazamiento=(0, 0.2))
    flecha(eje, 6.3, 1.8, 7.65, 1.8, texto="acciones", desplazamiento=(0, 0.2))
    eje.add_patch(FancyArrowPatch((8.4, 1.48), (1.6, 1.48), connectionstyle="arc3,rad=-0.28",
                                  arrowstyle="-|>", mutation_scale=11, color=GRIS, linewidth=1.0, linestyle="--"))
    eje.text(5.0, 0.3, "lo que hace cambia el ambiente, que vuelve a percibir: aprende de la experiencia",
             ha="center", fontsize=8, color=GRIS)
    guardar(figura, "c5-agente.png")


# ===========================================================================
# 02 — Algoritmos evolutivos
# ===========================================================================


def figura_jirafas():
    titulo("Jirafas: variacion + seleccion natural")
    generador = np.random.default_rng(3)
    cuellos = generador.normal(1.0, 0.10, 1000)
    instantaneas = {0: cuellos.copy()}
    for generacion in range(1, 41):
        probabilidad = 1.0 / (1.0 + np.exp(-(cuellos - 1.1) / 0.05))   # mas alto -> mas hojas
        padres = generador.choice(len(cuellos), size=len(cuellos), p=probabilidad / probabilidad.sum())
        cuellos = cuellos[padres] + generador.normal(0, 0.03, len(cuellos))  # variacion en el hijo
        if generacion in (10, 40):
            instantaneas[generacion] = cuellos.copy()
    figura, eje = plt.subplots(figsize=(7.0, 2.7))
    colores = {0: GRIS, 10: AZUL, 40: VERDE}
    for generacion, valores in instantaneas.items():
        eje.hist(valores, bins=40, range=(0.6, 2.2), alpha=0.55, color=colores[generacion],
                 label=f"generación {generacion}: media {valores.mean():.2f}")
        print(f"  generacion {generacion:2d}: media {valores.mean():.3f}, desvio {valores.std():.3f}")
    eje.set_xlabel("largo del cuello (unidades arbitrarias)")
    eje.set_ylabel("jirafas")
    eje.legend(fontsize=8, loc="upper right")
    eje.set_title("Nadie estira el cuello: la población se corre porque los de cuello largo dejan más hijos")
    guardar(figura, "01-jirafas.png")


def figura_ciclo():
    figura, eje = plt.subplots(figsize=(8.6, 3.5))
    apagar_ejes(eje)
    eje.set_xlim(0, 10.6)
    eje.set_ylim(-0.2, 4.2)
    caja(eje, 1.1, 3.6, "Inicializar\n(al azar)", ancho=1.7, alto=0.75)
    caja(eje, 3.5, 3.6, "Evaluar\naptitud", ancho=1.6, alto=0.75)
    caja(eje, 6.2, 3.6, "¿mejor aptitud\n≥ requerida?", ancho=2.0, alto=0.75, fondo=FONDO_NARANJA, borde=NARANJA)
    caja(eje, 9.3, 3.6, "FIN", ancho=1.0, alto=0.6, fondo=FONDO_VERDE, borde=VERDE, negrita=True)
    caja(eje, 7.6, 1.2, "Selección\n(progenitores)", ancho=1.9, alto=0.75)
    caja(eje, 5.0, 1.2, "Cruza +\nmutación", ancho=1.7, alto=0.75)
    caja(eje, 2.5, 1.2, "Reemplazo\n(nueva población)", ancho=2.1, alto=0.75)
    flecha(eje, 1.95, 3.6, 2.7, 3.6)
    flecha(eje, 4.3, 3.6, 5.2, 3.6)
    flecha(eje, 7.2, 3.6, 8.8, 3.6, texto="sí", desplazamiento=(0, 0.2))
    flecha(eje, 6.4, 3.22, 7.4, 1.58, texto="no", desplazamiento=(0.3, 0.0))
    flecha(eje, 6.65, 1.2, 5.85, 1.2)
    flecha(eje, 4.15, 1.2, 3.55, 1.2)
    flecha(eje, 2.6, 1.58, 3.3, 3.22, texto="nueva generación", desplazamiento=(-0.9, 0.0))
    eje.text(7.6, 0.25, "favorece a los aptos,\npero todos pueden salir", ha="center", fontsize=7.5, color=GRIS)
    eje.text(5.0, 0.25, "variación: mantiene\nla diversidad", ha="center", fontsize=7.5, color=GRIS)
    eje.text(2.5, 0.25, "total, con brecha\no con elitismo", ha="center", fontsize=7.5, color=GRIS)
    guardar(figura, "02-ciclo-evolutivo.png")


def figura_genotipo_fenotipo():
    figura, eje = plt.subplots(figsize=(8.6, 2.9))
    apagar_ejes(eje)
    eje.set_xlim(0, 10)
    eje.set_ylim(0, 3.4)
    eje.add_patch(FancyBboxPatch((0.2, 0.3), 3.6, 2.8, boxstyle="round,pad=0.02,rounding_size=0.2",
                                 facecolor=FONDO_AZUL, edgecolor=AZUL))
    eje.add_patch(FancyBboxPatch((6.2, 0.3), 3.6, 2.8, boxstyle="round,pad=0.02,rounding_size=0.2",
                                 facecolor=FONDO_VERDE, edgecolor=VERDE))
    eje.text(2.0, 2.8, "espacio del GENOTIPO", ha="center", fontweight="bold", color=AZUL)
    eje.text(8.0, 2.8, "espacio del FENOTIPO", ha="center", fontweight="bold", color=VERDE)
    ejemplos = ["0000", "0101", "1001", "1111"]
    for k, bits in enumerate(ejemplos):
        entero = int(bits, 2)
        valor = -100 + 200 * entero / 15
        y = 2.25 - 0.5 * k
        eje.text(2.0, y, bits, ha="center", va="center", family="monospace", fontsize=10)
        eje.text(8.0, y, f"x = {valor:+.2f}", ha="center", va="center", fontsize=9)
        eje.plot([2.6, 7.3], [y, y], color=GRIS_CLARO, linewidth=0.6, linestyle=":")
    flecha(eje, 4.0, 2.2, 6.0, 2.2, color=VERDE, texto="decodificación\n(para evaluar)", desplazamiento=(0, 0.32))
    flecha(eje, 6.0, 0.55, 4.0, 0.55, color=AZUL, texto="codificación", desplazamiento=(0, -0.2))
    eje.text(5.0, 1.45, "4 bits en [−100, 100]:\n$x = a + (b-a)\\,\\frac{\\mathrm{entero}}{2^L-1}$",
             ha="center", va="center", fontsize=8.5)
    guardar(figura, "03-genotipo-fenotipo.png")


def dibujar_cromosoma(eje, y, segmentos, titulo_fila):
    x = 0.0
    for texto, ancho, color in segmentos:
        eje.add_patch(Rectangle((x, y), ancho, 0.55, facecolor=color, edgecolor="white", linewidth=1.5))
        eje.text(x + ancho / 2, y + 0.275, texto, ha="center", va="center", fontsize=7.5)
        x += ancho
    eje.text(-0.15, y + 0.275, titulo_fila, ha="right", va="center", fontsize=8.5, fontweight="bold")
    return x


def figura_cromosomas():
    figura, eje = plt.subplots(figsize=(10.0, 4.4))
    apagar_ejes(eje)
    fila = 4.0
    dibujar_cromosoma(eje, fila, [("figura\n2 bits", 0.9, FONDO_NARANJA), ("coord. 1\n4 bits", 1.5, FONDO_AZUL),
                                  ("coord. 2\n4 bits", 1.5, FONDO_VERDE), ("figura", 0.9, FONDO_NARANJA),
                                  ("coord. 1", 1.5, FONDO_AZUL), ("coord. 2", 1.5, FONDO_VERDE),
                                  ("· · ·  (10 figuras × 10 bits = 100 bits)", 3.0, "#f1f2f4")], "Figuras en\nun área")
    fila -= 1.0
    dibujar_cromosoma(eje, fila, [("neuronas\ncapa 1", 1.0, FONDO_NARANJA), ("neuronas\nocultas", 1.0, FONDO_NARANJA),
                                  ("neuronas\nsalida", 1.0, FONDO_NARANJA), ("$w_{11}$", 0.9, FONDO_AZUL),
                                  ("$w_{12}$", 0.9, FONDO_AZUL), ("· · ·", 0.9, FONDO_AZUL),
                                  ("pesos capa 2 ...", 1.8, FONDO_VERDE), ("· · ·", 1.3, "#f1f2f4")], "Red\nneuronal")
    fila -= 1.0
    dibujar_cromosoma(eje, fila, [("instr.\n01 = si", 0.9, FONDO_NARANJA), ("argumentos\n6 bits", 1.6, FONDO_AZUL),
                                  ("instr.\n11 = avanzar", 1.0, FONDO_NARANJA), ("argumentos", 1.6, FONDO_AZUL),
                                  ("instr.", 0.9, FONDO_NARANJA), ("argumentos", 1.6, FONDO_AZUL),
                                  ("· · ·", 1.2, "#f1f2f4")], "Programa\ndel robot")
    fila -= 1.0
    dibujar_cromosoma(eje, fila, [("nodo i", 0.9, FONDO_AZUL), ("nodo j", 0.9, FONDO_AZUL),
                                  ("componente\n(R, C, L, AO)", 1.4, FONDO_NARANJA), ("valor", 0.9, FONDO_VERDE),
                                  ("nodo i", 0.9, FONDO_AZUL), ("nodo j", 0.9, FONDO_AZUL),
                                  ("componente", 1.4, FONDO_NARANJA), ("valor", 0.9, FONDO_VERDE),
                                  ("· · ·", 1.2, "#f1f2f4")], "Circuito\n(filtro)")
    fila -= 1.0
    dibujar_cromosoma(eje, fila, [(f"ciudad\n{c}", 1.2, FONDO_AZUL if k % 2 == 0 else FONDO_VERDE)
                                  for k, c in enumerate([3, 1, 7, 5, 2, 8, 4, 6])], "Viajante\n(8 ciudades)")
    eje.set_xlim(-1.6, 11.0)
    eje.set_ylim(-0.2, 4.8)
    guardar(figura, "04-cromosomas-de-los-ejemplos.png")


def figura_aptitud_propiedades():
    figura, ejes = plt.subplots(1, 4, figsize=(11.0, 2.7))
    bondad = np.linspace(0, 1, 300)
    eje = ejes[0]
    eje.plot(bondad, bondad, color=AZUL, label="lineal")
    eje.plot(bondad, bondad ** 3, color=VERDE, label="favorece a los muy buenos")
    eje.set_title("Monótonas: sirven")
    eje.legend(fontsize=7)
    eje = ejes[1]
    no_monotona = bondad + 0.25 * np.sin(4 * np.pi * bondad)
    eje.plot(bondad, no_monotona, color=ROJO)
    a, b = 0.15, 0.34
    fa, fb = a + 0.25 * np.sin(4 * np.pi * a), b + 0.25 * np.sin(4 * np.pi * b)
    eje.plot([a, b], [fa, fb], "o", color=ROJO)
    eje.text(0.03, 0.93, "B es mejor que A,\npero tiene menos aptitud", fontsize=7, va="top", transform=eje.transAxes)
    eje.text(a, fa + 0.06, "A", fontsize=8, ha="center")
    eje.text(b, fb - 0.13, "B", fontsize=8, ha="center")
    eje.set_title("No monótona: no sirve")
    eje = ejes[2]
    eje.plot(bondad, np.where(bondad < 0.5, 1, 5), color=ROJO, label="sólo «malo» o «bueno»")
    eje.plot(bondad, 1 + 4 * bondad, color=AZUL, label="distingue a los parecidos")
    eje.set_title("Precisión")
    eje.legend(fontsize=7)
    eje = ejes[3]
    for beta, color in [(40, ROJO), (10, AZUL), (3, VERDE)]:
        eje.plot(bondad, 1 / (1 + np.exp(-beta * (bondad - 0.5))), color=color, label=f"$\\beta={beta}$")
    eje.set_title("Suavidad regulable (sigmoide)")
    eje.legend(fontsize=7)
    for eje in ejes:
        eje.set_xlabel("qué tan bueno es en el problema")
    ejes[0].set_ylabel("aptitud")
    guardar(figura, "05-aptitud-propiedades.png")


def figura_aptitud_area():
    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(10.0, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})
    eje = eje_a
    apagar_ejes(eje)
    eje.set_aspect("equal")
    eje.add_patch(Rectangle((0, 0), 10, 6, facecolor="#f3f3f3", edgecolor=TINTA, linewidth=1.2))
    eje.add_patch(Rectangle((0.5, 0.5), 3, 2.5, facecolor=FONDO_AZUL, edgecolor=AZUL, hatch="---", linewidth=1))
    eje.add_patch(Rectangle((2.8, 2.2), 2.5, 2.5, facecolor=FONDO_AZUL, edgecolor=AZUL, hatch="---", linewidth=1))
    eje.add_patch(Rectangle((2.8, 2.2), 0.7, 0.8, facecolor=FONDO_ROJO, edgecolor=ROJO, hatch="|||", linewidth=1))
    circulo = Circle((9.3, 3.6), 1.6, facecolor=FONDO_AZUL, edgecolor=AZUL, hatch="---", linewidth=1)
    eje.add_patch(circulo)
    parte_fuera = Rectangle((10, 0), 2, 6.5, facecolor=FONDO_NARANJA, edgecolor=NARANJA, hatch="xxx", linewidth=1)
    eje.add_patch(parte_fuera)
    parte_fuera.set_clip_path(Circle((9.3, 3.6), 1.6, transform=eje.transData))
    eje.plot([10, 10], [0, 6], color=TINTA, linewidth=1.2)
    eje.text(6.3, 0.8, "desperdicio", fontsize=8, color=GRIS)
    eje.annotate("solapada", xy=(3.15, 2.6), xytext=(4.3, 1.4), fontsize=7.5, color=ROJO,
                 arrowprops=dict(arrowstyle="-", color=ROJO, linewidth=0.8))
    eje.text(10.25, 5.5, "fuera", fontsize=7.5, color=NARANJA)
    eje.text(1.0, 3.6, "ocupada", fontsize=7.5, color=AZUL)
    eje.set_xlim(-0.3, 11.6)
    eje.set_ylim(-0.4, 6.4)
    eje.set_title("$f = A_{ocup} - A_{desp} - A_{solap} - 1000\\,A_{fuera}$", fontsize=9)

    eje = eje_b
    frecuencias = np.logspace(0, 4, 400)
    deseada = np.where((frecuencias > 60) & (frecuencias < 170), 1.0, 0.0)
    obtenida = 1.0 / np.sqrt(1 + ((np.log10(frecuencias) - 2.0) / 0.28) ** 4)
    eje.semilogx(frecuencias, deseada, color=TINTA, label="la que se pide (pasa ~100 Hz)")
    eje.semilogx(frecuencias, obtenida, color=AZUL, label="la de un individuo")
    eje.fill_between(frecuencias, deseada, obtenida, color=ROJO, alpha=0.25, label="error $E$ (área)")
    eje.set_xlabel("frecuencia")
    eje.set_ylabel("ganancia")
    eje.legend(fontsize=7, loc="upper right")
    eje.set_title("Filtro: $f = \\dfrac{1}{1+E}$  (vale 1 si $E=0$)", fontsize=9)
    guardar(figura, "06-aptitud-ejemplos.png")


def figura_ruleta():
    titulo("Ejemplo x^2: una generacion a mano")
    poblacion = [13, 24, 8, 19]
    aptitudes = np.array([x * x for x in poblacion], dtype=float)
    probabilidades = aptitudes / aptitudes.sum()
    print("  cromosomas:", [format(x, "05b") for x in poblacion], "aptitudes:", aptitudes.tolist(),
          "suma", aptitudes.sum(), "media", aptitudes.mean())
    print("  tajadas (%):", np.round(100 * probabilidades, 1).tolist())

    def cruza(a, c, k):
        A, C = format(a, "05b"), format(c, "05b")
        return int(A[:k] + C[k:], 2), int(C[:k] + A[k:], 2)
    hijos = [*cruza(13, 24, 4), *cruza(24, 19, 2)]
    aptitudes_hijos = [x * x for x in hijos]
    print("  hijos:", hijos, [format(x, "05b") for x in hijos], "aptitudes", aptitudes_hijos,
          "media", np.mean(aptitudes_hijos), "maximo", max(aptitudes_hijos))
    esquema = [x for x in poblacion if x >= 16]
    media_esquema = np.mean([x * x for x in esquema])
    print(f"  esquema 1****: instancias {esquema}, aptitud media {media_esquema}, cociente {media_esquema / aptitudes.mean():.3f},"
          f" copias esperadas {len(esquema) * media_esquema / aptitudes.mean():.2f}; en los hijos: {[x for x in hijos if x >= 16]}")
    orden = sorted(poblacion, key=lambda x: -x * x)
    for r, x in enumerate(orden):
        competencia = (3 - r) / 6
        ventanas = 0.25 * sum(1 / w for w in [4, 3, 2, 1] if r < w)
        print(f"  rango {r + 1} (x={x}): competencia k=2 {competencia:.3f}; ventanas 4-3-2-1 {ventanas:.4f}")

    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(9.5, 3.3), gridspec_kw={"width_ratios": [1, 1.4]})
    colores = [AZUL, VERDE, NARANJA, ROJO]
    etiquetas = [f"{format(x, '05b')}\n$x$={x}" for x in poblacion]
    eje_a.pie(probabilidades, labels=etiquetas, colors=colores, startangle=90, counterclock=False,
              wedgeprops=dict(edgecolor="white", linewidth=1.2, alpha=0.85),
              autopct=lambda p: f"{p:.1f}%", pctdistance=0.68, textprops=dict(fontsize=8))
    eje_a.set_title("Tajada = $f_i / \\sum f$")
    acumulada = np.concatenate([[0], np.cumsum(probabilidades)])
    for i in range(4):
        eje_b.barh(0, probabilidades[i], left=acumulada[i], color=colores[i], alpha=0.85, edgecolor="white", height=0.5)
        eje_b.text(acumulada[i] + probabilidades[i] / 2, 0, f"$x$={poblacion[i]}", ha="center", va="center", color="white", fontweight="bold", fontsize=8)
    for k, x in enumerate(acumulada):
        eje_b.text(x, -0.36 - 0.14 * (k % 2), f"{x:.3f}", ha="center", fontsize=7, color=GRIS)
    r = 0.45
    eje_b.annotate(f"$r = {r}$: cae en $x$=24", xy=(r, 0.25), xytext=(r, 0.75), ha="center",
                   arrowprops=dict(arrowstyle="-|>", color=TINTA))
    eje_b.set_xlim(0, 1)
    eje_b.set_ylim(-0.65, 1.0)
    eje_b.set_yticks([])
    eje_b.set_xlabel("probabilidad acumulada")
    eje_b.set_title("Programada: sortear $r\\sim U(0,1)$ y ver en qué tramo cae")
    guardar(figura, "07-ruleta.png")


def probabilidad_por_rango(metodo, aptitudes, repeticiones, generador, **opciones):
    n = len(aptitudes)
    orden = np.argsort(-aptitudes)
    rango = np.empty(n, dtype=int)
    rango[orden] = np.arange(n)
    cuenta = np.zeros(n)
    for _ in range(repeticiones):
        elegidos = metodo(aptitudes, n, generador, **opciones)
        np.add.at(cuenta, rango[elegidos], 1)
    return cuenta / repeticiones   # copias esperadas por rango en una generacion de n selecciones


def figura_mares():
    titulo("Mar de mediocres y mar de virtuosos")
    generador = np.random.default_rng(7)
    mediocres = np.concatenate([[10.0], np.ones(990)])
    p = 10 / mediocres.sum()
    print(f"  mediocres: tajada del bueno = {p:.4f} ({p * 100:.2f} %)")
    print(f"  prob. de que NO salga en 2 tiradas = {(1 - p) ** 2:.3f}")
    print(f"  prob. de que NO salga en 198 tiradas (brecha 20 %) = {(1 - p) ** 198:.3f}")
    print(f"  copias esperadas en 991 tiradas = {991 * p:.2f}")
    virtuosos = np.linspace(49.9, 50.1, 100)
    print(f"  virtuosos: tajada del mejor = {virtuosos.max() / virtuosos.sum():.5f} contra 1/100 = 0.01;"
          f" copias esperadas = {100 * virtuosos.max() / virtuosos.sum():.4f}")

    # Toma de la poblacion por el bueno, solo seleccion (sin cruza ni mutacion)
    perdidas = 0
    generaciones_hasta_tomar = []
    for semilla in range(200):
        g = np.random.default_rng(1000 + semilla)
        poblacion = mediocres.copy()
        for generacion in range(1, 50):
            poblacion = poblacion[seleccion_ruleta(poblacion, len(poblacion), g)]
            buenos = np.sum(poblacion == 10.0)
            if buenos == 0:
                perdidas += 1
                break
            if buenos > 0.9 * len(poblacion):
                generaciones_hasta_tomar.append(generacion)
                break
    print(f"  solo seleccion por ruleta, 200 corridas: el bueno se pierde en {perdidas};"
          f" si sobrevive ocupa el 90 % en {np.median(generaciones_hasta_tomar):.0f} generaciones (mediana)")

    figura, ejes = plt.subplots(1, 3, figsize=(11.0, 3.0), gridspec_kw={"width_ratios": [1, 1, 1.3]})
    eje = ejes[0]
    eje.bar([1, 10], [990, 1], width=0.6, color=[GRIS, VERDE])
    eje.set_yscale("log")
    eje.set_xlabel("aptitud")
    eje.set_ylabel("individuos (escala log)")
    eje.set_title("Mar de mediocres: 990 con 1, uno con 10")
    eje = ejes[1]
    eje.hist(virtuosos, bins=np.linspace(0, 60, 61), color=AZUL)
    eje.set_xlabel("aptitud")
    eje.set_title("Mar de virtuosos: 100 entre 49,9 y 50,1")
    eje = ejes[2]
    metodos = [("ruleta", seleccion_ruleta, {}), ("ventanas", seleccion_ventanas, {}),
               ("competencia $k=2$", seleccion_competencia, {"k": 2}), ("competencia $k=5$", seleccion_competencia, {"k": 5})]
    copias_virtuosos = []
    for nombre, metodo, opciones in metodos:
        copias = probabilidad_por_rango(metodo, virtuosos, 3000, generador, **opciones)
        copias_virtuosos.append(copias[0])
        eje.plot(np.arange(1, 101), copias, marker=".", markersize=3, linewidth=1, label=nombre)
        print(f"  virtuosos, {nombre}: copias esperadas del mejor = {copias[0]:.2f}, del mediano = {copias[49]:.2f}, del peor = {copias[-1]:.2f}")
    eje.axhline(1.0, color=GRIS, linewidth=0.8, linestyle="--")
    eje.set_xlabel("rango (1 = el mejor)")
    eje.set_ylabel("copias esperadas por generación")
    eje.set_title("Virtuosos: la ruleta no distingue; las otras sí")
    eje.legend(fontsize=7)
    guardar(figura, "08-mares.png")
    return copias_virtuosos


def figura_ventanas():
    figura, eje = plt.subplots(figsize=(7.5, 2.6))
    n = 10
    ventanas = np.linspace(n, 2, 5).round().astype(int)
    for k, w in enumerate(ventanas):
        eje.barh(k, w, left=0.5, color=AZUL, alpha=0.18 + 0.12 * k, edgecolor=AZUL, height=0.6)
        eje.text(w + 0.6, k, f"sorteo entre los {w} mejores", va="center", fontsize=8)
    eje.set_yticks(range(len(ventanas)))
    eje.set_yticklabels([f"padre {k + 1}" for k in range(len(ventanas))])
    eje.set_xticks(range(1, n + 1))
    eje.set_xlim(0.4, 14.5)
    eje.invert_yaxis()
    eje.set_xlabel("individuos ordenados de mayor a menor aptitud (1 = el mejor)")
    eje.set_title("Ventanas: el mejor está en todas; el peor, sólo en la primera")
    guardar(figura, "09-ventanas.png")


def figura_operadores():
    figura, ejes = plt.subplots(3, 1, figsize=(9.0, 5.0))
    for eje in ejes:
        apagar_ejes(eje)
        eje.set_xlim(-0.5, 21)
        eje.set_ylim(-0.6, 2.0)

    def bits(eje, x0, y, cadena, colores, resaltar=None):
        for k, b in enumerate(cadena):
            color = colores[k] if isinstance(colores, list) else colores
            borde = NARANJA if resaltar is not None and k in resaltar else "white"
            eje.add_patch(Rectangle((x0 + k * 0.85, y), 0.8, 0.6, facecolor=color, edgecolor=borde, linewidth=2))
            eje.text(x0 + k * 0.85 + 0.4, y + 0.3, b, ha="center", va="center", family="monospace", fontsize=10)

    eje = ejes[0]
    bits(eje, 0.5, 0.6, "10111101", FONDO_AZUL, resaltar=[4])
    bits(eje, 12.5, 0.6, "10110101", FONDO_AZUL, resaltar=[4])
    flecha(eje, 8.0, 0.9, 12.0, 0.9, texto="se invierte un bit al azar", desplazamiento=(0, 0.45))
    eje.text(-0.4, 1.6, "Mutación", fontweight="bold", fontsize=9)

    eje = ejes[1]
    padre_1, padre_2 = "10111101", "11100011"
    corte = 5
    bits(eje, 0.5, 1.15, padre_1, FONDO_AZUL)
    bits(eje, 0.5, 0.2, padre_2, FONDO_VERDE)
    hijo_1 = padre_1[:corte] + padre_2[corte:]
    hijo_2 = padre_2[:corte] + padre_1[corte:]
    bits(eje, 12.5, 1.15, hijo_1, [FONDO_AZUL] * corte + [FONDO_VERDE] * (8 - corte))
    bits(eje, 12.5, 0.2, hijo_2, [FONDO_VERDE] * corte + [FONDO_AZUL] * (8 - corte))
    eje.plot([0.5 + corte * 0.85 - 0.025] * 2, [0.05, 1.9], color=NARANJA, linewidth=2)
    flecha(eje, 8.0, 1.05, 12.0, 1.05, texto="se intercambian las colas", desplazamiento=(0, 0.45))
    eje.text(-0.4, 1.95, "Cruza simple (un punto)", fontweight="bold", fontsize=9)
    print("  cruza de la diapositiva:", padre_1, padre_2, "->", hijo_1, hijo_2)

    eje = ejes[2]
    mascara = "01101001"
    hijo_u1 = "".join(a if m == "0" else b for a, b, m in zip(padre_1, padre_2, mascara))
    hijo_u2 = "".join(b if m == "0" else a for a, b, m in zip(padre_1, padre_2, mascara))
    bits(eje, 0.5, 1.15, padre_1, FONDO_AZUL)
    bits(eje, 0.5, 0.2, padre_2, FONDO_VERDE)
    bits(eje, 12.5, 1.15, hijo_u1, [FONDO_AZUL if m == "0" else FONDO_VERDE for m in mascara])
    bits(eje, 12.5, 0.2, hijo_u2, [FONDO_VERDE if m == "0" else FONDO_AZUL for m in mascara])
    flecha(eje, 8.0, 1.05, 12.0, 1.05, texto=f"máscara {mascara}", desplazamiento=(0, 0.45))
    eje.text(-0.4, 1.95, "Cruza uniforme (bibliografía): cada gen se intercambia con prob. 1/2", fontweight="bold", fontsize=9)
    guardar(figura, "10-operadores.png")


def figura_cruza_vs_mutacion():
    titulo("Cruza explota, mutacion explora (1 variable, 8 bits)")
    def g(x):
        x = np.asarray(x, dtype=float)
        return np.exp(-((x - 70) / 25) ** 2) + 1.6 * np.exp(-((x - 200) / 18) ** 2)
    padre_a, padre_b = 60, 85
    hijos = set()
    for k in range(1, 8):
        a, c = format(padre_a, "08b"), format(padre_b, "08b")
        hijos |= {int(a[:k] + c[k:], 2), int(c[:k] + a[k:], 2)}
    hijos = sorted(hijos - {padre_a, padre_b})
    mutantes = [padre_a ^ (1 << k) for k in range(8)]
    print("  padres:", padre_a, format(padre_a, "08b"), padre_b, format(padre_b, "08b"))
    print("  hijos de cruza (todos los cortes):", hijos)
    print("  mutantes de A (bit de menor a mayor peso):", mutantes)
    figura, eje = plt.subplots(figsize=(8.5, 3.2))
    xs = np.arange(256)
    eje.plot(xs, g(xs), color=GRIS, linewidth=1.2)
    eje.axvspan(0, 127.5, color=FONDO_AZUL, alpha=0.5)
    eje.text(64, 1.72, "primer bit = 0", ha="center", fontsize=8, color=AZUL)
    eje.text(192, 1.72, "primer bit = 1", ha="center", fontsize=8, color=GRIS)
    eje.scatter(hijos, g(hijos), s=30, color=AZUL, zorder=3, label="hijos de la cruza A × B (todos los cortes)")
    eje.scatter(mutantes, g(mutantes) + 0.06, s=40, marker="x", color=ROJO, zorder=3, label="mutantes de A (un bit cada uno)")
    for x, nombre in [(padre_a, "A = 00111100"), (padre_b, "B = 01010101")]:
        eje.scatter([x], [g(x)], s=80, color=TINTA, zorder=4)
        eje.annotate(nombre, xy=(x, g(x)), xytext=(x - 5 if x == padre_a else x + 5, g(x) + 0.35), fontsize=7.5,
                     ha="right" if x == padre_a else "left", arrowprops=dict(arrowstyle="-", color=GRIS, linewidth=0.7))
    eje.annotate("A con el primer bit\ninvertido: 188", xy=(188, g(188) + 0.06), xytext=(150, 1.25), fontsize=7.5,
                 color=ROJO, arrowprops=dict(arrowstyle="-|>", color=ROJO))
    eje.set_xlim(-2, 257)
    eje.set_ylim(-0.05, 1.85)
    eje.set_xlabel("$x$ (8 bits, 0 a 255)")
    eje.set_ylabel("aptitud")
    eje.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0.0, 0.92))
    guardar(figura, "11-cruza-y-mutacion.png")


def figura_mutacion_tasas():
    titulo("Tasa de mutacion: por individuo o por gen")
    individuos, genes = 100, 10
    total = individuos * genes
    for tasa in (0.01, 0.10):
        print(f"  tasa {tasa:.0%}: por individuo -> {tasa * individuos:.0f} individuos mutados;"
              f" por gen -> {tasa * total:.0f} genes mutados de {total};"
              f" fraccion de individuos con al menos un gen mutado = {1 - (1 - tasa) ** genes:.3f}")


def figura_gray():
    titulo("Codigo Gray: el acantilado de Hamming")
    for a, b in [(7, 8), (3, 4), (15, 16)]:
        print(f"  {a}->{b}: binario {a:05b}->{b:05b} Hamming {hamming(a, b)};"
              f" Gray {a_gray(a):05b}->{a_gray(b):05b} Hamming {hamming(a_gray(a), a_gray(b))}")
    resolucion = 200 / (2 ** 20 - 1)
    print(f"  resolucion con 20 bits en [-100, 100]: {resolucion:.3e}")
    print(f"  resolucion con 4 bits en [-100, 100]: {200 / 15:.3f}")


def figura_restricciones():
    titulo("Restricciones: funcion de penalizacion")
    x = np.linspace(-1, 4, 2001)
    objetivo = (x - 3.0) ** 2            # minimo sin restriccion en x = 3
    violacion = np.maximum(0, x - 2.0)   # restriccion: x <= 2  ->  p(x) = max(0, x - 2)
    figura, eje = plt.subplots(figsize=(7.4, 3.1))
    eje.axvspan(-1, 2, color=FONDO_VERDE, alpha=0.6, label="región factible ($x\\leq 2$)")
    eje.plot(x, objetivo, color=TINTA, label="$f(x)=(x-3)^2$, mín. en 3 (afuera)")
    casos = [(1.0, 2, NARANJA, "--"), (100.0, 2, AZUL, "--"), (1.0, 1, VIOLETA, "-"), (10.0, 1, VERDE, "-")]
    for lam, potencia, color, estilo in casos:
        penalizada = objetivo + lam * violacion ** potencia
        minimo = x[np.argmin(penalizada)]
        etiqueta = f"$f+{lam:g}\\,p^{potencia}$: mín. en {minimo:.2f}" if potencia == 2 else f"$f+{lam:g}\\,p$: mín. en {minimo:.2f}"
        eje.plot(x, penalizada, color=color, linestyle=estilo, label=etiqueta)
        print(f"  lambda={lam:g}, p^{potencia}: minimo de la penalizada en x = {minimo:.3f} (factible: {minimo <= 2 + 1e-9})")
    eje.set_ylim(0, 6)
    eje.set_xlabel("$x$")
    eje.legend(fontsize=7, loc="upper left")
    eje.set_title("La penalización cambia la forma de la función: elegir λ es parte del diseño")
    guardar(figura, "15-penalizacion.png")


def figura_viajante():
    titulo("Viajante: la cruza simple rompe permutaciones")
    p1 = [1, 2, 3, 4, 5, 6, 7, 8]
    p2 = [3, 7, 5, 1, 6, 8, 2, 4]
    corte = 4
    h1 = p1[:corte] + p2[corte:]
    repetidas = sorted({c for c in h1 if h1.count(c) > 1})
    faltan = sorted(set(p1) - set(h1))
    print(f"  cruza simple: {p1} x {p2} corte {corte} -> {h1}; repetidas {repetidas}, faltan {faltan}")
    # Cruza de orden (OX): se copia un tramo de p1 y se completa con el orden de p2
    a, b = 2, 5
    tramo = p1[a:b]
    resto = [c for c in p2 if c not in tramo]
    hijo = resto[:a] + tramo + resto[a:]
    print(f"  cruza de orden OX, tramo {tramo} de p1 en posiciones {a}..{b - 1}: hijo {hijo}; es permutacion: {sorted(hijo) == p1}")
    return h1, repetidas, faltan, hijo


def figura_lamarck():
    titulo("Lamarck en la computadora: AG + busqueda local")
    n_variables, bits = 6, 14
    minimo, maximo = -5.12, 5.12
    longitud = n_variables * bits
    umbral = 0.01

    def aptitud(cromosomas):
        return -rastrigin(decodificar(cromosomas, n_variables, bits, minimo, maximo))

    def busqueda_local(cromosomas, pasos=3, tasa=0.004):
        x = decodificar(cromosomas, n_variables, bits, minimo, maximo)
        for _ in range(pasos):
            gradiente = 2 * x + 20 * np.pi * np.sin(2 * np.pi * x)
            x = np.clip(x - tasa * gradiente, minimo, maximo)
        mejorados = codificar(x, bits, minimo, maximo)
        # costo: cada paso de gradiente cuenta como una evaluacion
        return mejorados, aptitud(mejorados), pasos * len(cromosomas)

    resultados = {}
    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(10.0, 3.1))
    variantes = [("darwiniano (AG solo)", {}, GRIS, 480),
                 ("baldwiniano", {"mejora_local": busqueda_local, "lamarck": False}, AZUL, 120),
                 ("lamarckiano", {"mejora_local": busqueda_local, "lamarck": True}, VERDE, 120)]
    for nombre, opciones, color, generaciones in variantes:
        curvas, curvas_eval, gen_llegada, eval_llegada = [], [], [], []
        for semilla in range(20):
            g = np.random.default_rng(500 + semilla)
            _, _, mejor, _, evaluaciones = algoritmo_genetico(aptitud, longitud, g, individuos=60, generaciones=generaciones,
                                                             seleccion="competencia", reemplazo="elitismo", **opciones)
            f = -mejor
            curvas.append(f)
            curvas_eval.append(evaluaciones[: len(f)])
            llegada = np.nonzero(f < umbral)[0]
            if len(llegada):
                gen_llegada.append(llegada[0])
                eval_llegada.append(evaluaciones[llegada[0]])
        largo = min(len(c) for c in curvas)
        curvas = np.array([c[:largo] for c in curvas])
        curvas_eval = np.array([c[:largo] for c in curvas_eval])
        resultados[nombre] = (len(gen_llegada), np.median(gen_llegada) if gen_llegada else None,
                              np.median(eval_llegada) if eval_llegada else None)
        print(f"  {nombre:22s}: llega a f<{umbral} en {len(gen_llegada)}/20;"
              f" generaciones (mediana) {resultados[nombre][1]}; evaluaciones (mediana) {resultados[nombre][2]};"
              f" f final mediana {np.median(curvas[:, -1]):.3f}")
        eje_a.plot(np.median(curvas, axis=0)[:120], color=color, label=nombre)
        eje_b.plot(np.median(curvas_eval, axis=0), np.median(curvas, axis=0), color=color, label=nombre)
    for eje in (eje_a, eje_b):
        eje.set_yscale("symlog", linthresh=0.01)
        eje.set_ylabel("$f$ del mejor (mediana de 20)")
        eje.legend(fontsize=7)
    eje_a.set_xlabel("generación")
    eje_a.set_title("Rastrigin, 6 variables: por generación")
    eje_b.set_xlabel("evaluaciones (la búsqueda local también cuesta)")
    eje_b.set_title("Por costo")
    guardar(figura, "16-lamarck.png")
    return resultados


def figura_paralelismo():
    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(10.0, 3.0))
    for eje in (eje_a, eje_b):
        apagar_ejes(eje)
        eje.set_xlim(0, 10)
        eje.set_ylim(0, 4)
    caja(eje_a, 5, 3.3, "maestro: selección,\ncruza, mutación", ancho=3.4, alto=0.75, negrita=False)
    for k in range(5):
        x = 1.2 + k * 1.9
        caja(eje_a, x, 0.8, f"nodo {k + 1}\naptitud", ancho=1.5, alto=0.7, fondo=FONDO_VERDE, borde=VERDE, tam=7.5)
        flecha(eje_a, 5 + (x - 5) * 0.35, 2.9, x, 1.18, color=GRIS)
    eje_a.set_title("Maestro–esclavo: sólo se reparte la evaluación\n(el algoritmo no cambia)")
    centros = [(2.0, 2.9), (8.0, 2.9), (5.0, 0.8)]
    for (x, y), k in zip(centros, range(3)):
        eje_b.add_patch(Circle((x, y), 0.75, facecolor=FONDO_AZUL, edgecolor=AZUL))
        eje_b.text(x, y, f"isla {k + 1}\n50 ind.", ha="center", va="center", fontsize=7.5)
    for i in range(3):
        for j in range(3):
            if i != j:
                (x0, y0), (x1, y1) = centros[i], centros[j]
                d = np.hypot(x1 - x0, y1 - y0)
                eje_b.add_patch(FancyArrowPatch((x0 + 0.8 * (x1 - x0) / d, y0 + 0.8 * (y1 - y0) / d),
                                                (x1 - 0.8 * (x1 - x0) / d, y1 - 0.8 * (y1 - y0) / d),
                                                connectionstyle="arc3,rad=0.15", arrowstyle="-|>",
                                                mutation_scale=9, color=GRIS, linewidth=0.8))
    eje_b.text(5.0, 3.6, "cada tanto migran individuos", ha="center", fontsize=8, color=GRIS)
    eje_b.set_title("Islas (colonias): cada una evoluciona aparte\n(esto sí cambia el algoritmo)")
    guardar(figura, "17-paralelismo.png")


if __name__ == "__main__":
    titulo("Unidad 09 — figuras")
    figura_automata()
    figura_vecindades()
    figura_topologias()
    figura_juego_de_la_vida()
    figura_agente()
    figura_jirafas()
    figura_ciclo()
    figura_genotipo_fenotipo()
    figura_cromosomas()
    figura_aptitud_propiedades()
    figura_aptitud_area()
    figura_ruleta()
    figura_mares()
    figura_ventanas()
    figura_operadores()
    figura_cruza_vs_mutacion()
    figura_mutacion_tasas()
    figura_gray()
    figura_busqueda_multipunto()
    figura_escalones()
    figura_elitismo()
    figura_restricciones()
    figura_viajante()
    figura_lamarck()
    figura_paralelismo()


# ===========================================================================
# Seleccion de caracteristicas con AG (repaso de TP6)
# ===========================================================================


def _knn_cv(X, y, k=5, folds=3, semilla=0):
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    if X.shape[1] == 0:
        return 0.5
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=semilla)
    return cross_val_score(KNeighborsClassifier(n_neighbors=k), X, y, cv=cv).mean()


def datos_interaccion(n=400, generador=None):
    g = generador or np.random.default_rng(0)
    centros = np.array([[-1, 1], [1, 1], [-1, -1], [1, -1]], dtype=float)
    clase_centro = np.array([0, 1, 1, 0])           # diagonal = una clase (XOR)
    c = g.integers(0, 4, n)
    X = centros[c] + g.normal(0, 0.3, (n, 2))
    return X, clase_centro[c]


def datos_redundantes(n=400, generador=None):
    g = generador or np.random.default_rng(1)
    y = g.integers(0, 2, n)
    t = g.normal(0, 1.6, n)                          # a lo largo de la diagonal
    s = np.where(y == 1, 0.55, -0.55) + g.normal(0, 0.22, n)   # perpendicular
    X = np.column_stack([t - s, t + s]) / np.sqrt(2)
    return X, y


def figura_reduccion_vs_seleccion():
    titulo("Reduccion de dimension contra seleccion de caracteristicas")
    g = np.random.default_rng(3)
    X, y = datos_redundantes(300, g)
    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(9.6, 3.6))
    for eje, modo in ((eje_a, "pca"), (eje_b, "fs")):
        eje.scatter(X[y == 0, 0], X[y == 0, 1], s=8, color=AZUL, alpha=0.6)
        eje.scatter(X[y == 1, 0], X[y == 1, 1], s=8, color=ROJO, alpha=0.6)
        eje.set_aspect("equal"); eje.set_xlabel("$x_1$"); eje.set_ylabel("$x_2$")
        eje.set_xlim(-4, 4); eje.set_ylim(-4, 4)
    d = np.array([-1, 1]) / np.sqrt(2)
    eje_a.annotate("", xy=3.4 * d, xytext=-3.4 * d, arrowprops=dict(arrowstyle="-|>", color=VERDE, linewidth=2))
    eje_a.text(-3.6, 3.2, "nueva variable\n$z = (x_2 - x_1)/\\sqrt{2}$", fontsize=8, color=VERDE)
    eje_a.set_title("Reducción de dimensión (p. ej. PCA):\nse crea una variable nueva combinando las originales", fontsize=9)
    eje_b.annotate("", xy=(3.6, -3.6), xytext=(-3.6, -3.6), arrowprops=dict(arrowstyle="-|>", color=VERDE, linewidth=2))
    eje_b.text(-3.5, -3.2, "se queda con $x_1$ tal cual; $x_2$ se descarta", fontsize=8, color=VERDE)
    eje_b.set_title("Selección de características:\nse elige un subconjunto de las variables originales", fontsize=9)
    z = X @ d
    print(f"  proyeccion sobre z: acierto kNN {_knn_cv(z[:, None], y):.3f}; solo x1: {_knn_cv(X[:, :1], y):.3f}")
    guardar(figura, "18-reduccion-vs-seleccion.png")


def figura_interaccion_y_redundancia():
    titulo("Interaccion y redundancia")
    figura = plt.figure(figsize=(10.5, 4.4))
    resultados = {}
    for col, (nombre, fn) in enumerate([("interaccion", datos_interaccion), ("redundancia", datos_redundantes)]):
        X, y = fn(400, np.random.default_rng(10 + col))
        ax = figura.add_axes([0.06 + 0.5 * col, 0.12, 0.30, 0.62])
        ax_x = figura.add_axes([0.06 + 0.5 * col, 0.76, 0.30, 0.14], sharex=ax)
        ax_y = figura.add_axes([0.37 + 0.5 * col, 0.12, 0.07, 0.62], sharey=ax)
        for clase, color in ((0, AZUL), (1, ROJO)):
            ax.scatter(X[y == clase, 0], X[y == clase, 1], s=7, color=color, alpha=0.55)
            ax_x.hist(X[y == clase, 0], bins=30, color=color, alpha=0.5)
            ax_y.hist(X[y == clase, 1], bins=30, color=color, alpha=0.5, orientation="horizontal")
        for e in (ax_x, ax_y):
            e.tick_params(labelbottom=False, labelleft=False); e.grid(False)
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
        a_x, a_y, a_xy = _knn_cv(X[:, :1], y), _knn_cv(X[:, 1:], y), _knn_cv(X, y)
        resultados[nombre] = (a_x, a_y, a_xy)
        print(f"  {nombre}: acierto kNN (validacion cruzada) solo x {a_x:.3f}; solo y {a_y:.3f}; x e y {a_xy:.3f}")
        ax_x.set_title(("Interacción: cada una sola no sirve" if col == 0 else "Redundancia: muy correlacionadas, juntas separan")
                       + f"\nsólo x: {a_x * 100:.0f} %   sólo y: {a_y * 100:.0f} %   las dos: {a_xy * 100:.0f} %", fontsize=9)
    guardar(figura, "19-interaccion-y-redundancia.png")
    return resultados


def figura_ag_seleccion():
    titulo("AG para seleccion de caracteristicas (datos sinteticos)")
    from sklearn.feature_selection import mutual_info_classif
    g = np.random.default_rng(42)
    n, m = 300, 20
    X = g.normal(0, 1, (n, m))
    Xi, y = datos_interaccion(n, g)
    X[:, 3], X[:, 11] = Xi[:, 0], Xi[:, 1]           # las dos utiles (interactuan) en posiciones 3 y 11
    # ranking univariado (filtro): cada variable sola
    solo = np.array([_knn_cv(X[:, [j]], y) for j in range(m)])
    orden = np.argsort(-solo)
    print("  acierto de cada variable sola: utiles 3 y 11 ->", np.round(solo[[3, 11]], 3),
          "; puestos en el ranking:", int(np.where(orden == 3)[0][0]) + 1, int(np.where(orden == 11)[0][0]) + 1, "de", m)
    print("  quedarse con las 5 mejores del ranking:", sorted(orden[:5].tolist()), "-> acierto", round(_knn_cv(X[:, orden[:5]], y), 3))
    print("  todas las variables:", round(_knn_cv(X, y), 3), "; solo 3 y 11:", round(_knn_cv(X[:, [3, 11]], y), 3))
    cache = {}
    alfa, beta = 1.0, 0.1

    def aptitud(cromosomas):
        valores = []
        for c in cromosomas:
            clave = c.tobytes()
            if clave not in cache:
                sel = np.nonzero(c)[0]
                acc = _knn_cv(X[:, sel], y) if len(sel) else 0.0
                cache[clave] = alfa * acc - beta * len(sel) / m
            valores.append(cache[clave])
        return np.array(valores)
    exitos, finales, curvas = 0, [], []
    for semilla in range(10):
        gg = np.random.default_rng(semilla)
        pob, apt, mejor, media, _ = algoritmo_genetico(aptitud, m, gg, individuos=30, generaciones=40,
                                                       seleccion="competencia", reemplazo="elitismo")
        b = pob[np.argmax(apt)]
        sel = np.nonzero(b)[0].tolist()
        finales.append(sel); curvas.append(mejor)
        exitos += (3 in sel and 11 in sel)
    print(f"  AG (30 ind., 40 gen., 10 semillas): encuentra 3 y 11 en {exitos}/10; subconjuntos finales: {finales}")
    print(f"  evaluaciones distintas (memo): {len(cache)} de 2^20 = {2 ** 20} subconjuntos posibles")
    figura, (eje_a, eje_b) = plt.subplots(1, 2, figsize=(10.5, 3.2), gridspec_kw={"width_ratios": [1.15, 1]})
    eje_a.bar(range(m), solo, color=[VERDE if j in (3, 11) else GRIS_CLARO for j in range(m)])
    eje_a.axhline(0.5, color=GRIS, linestyle="--", linewidth=0.8)
    eje_a.set_ylim(0.3, 1.0); eje_a.set_xticks(range(m))
    eje_a.set_xlabel("variable"); eje_a.set_ylabel("acierto usando sólo esa variable")
    eje_a.set_title("Filtro por ranking: las útiles (verde) parecen ruido", fontsize=9)
    for c in curvas:
        eje_b.plot(c, color=AZUL, alpha=0.4, linewidth=1)
    eje_b.set_xlabel("generación"); eje_b.set_ylabel("aptitud del mejor")
    eje_b.set_title("AG con aptitud = acierto − 0,1·(fracción usada)", fontsize=9)
    guardar(figura, "20-ag-seleccion.png")
    return exitos


if __name__ == "__main__" and os.environ.get("SOLO_SELECCION"):
    figura_reduccion_vs_seleccion()
    figura_interaccion_y_redundancia()
    figura_ag_seleccion()
