"""Figuras y verificaciones del apunte de arboles de decision.

Genera todos los PNG que referencia ../Resumenes/01-arboles-de-decision.md e
imprime las verificaciones que cita el apunte. Trae una implementacion propia
de CART (cortes binarios paralelos a los ejes, impureza de Gini o entropia) de
unas 80 lineas; si scikit-learn esta instalado, se la compara contra
DecisionTreeClassifier.

    python3 graficos_arboles.py
"""

import os
from math import log2

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

DIRECTORIO_SALIDA = os.path.dirname(os.path.abspath(__file__))

AZUL = "#2a78d6"
ROJO = "#d1495b"
VERDE = "#1baf7a"
NARANJA = "#eb6834"
GRIS = "#8a8f98"
GRIS_CLARO = "#c8ccd2"
TINTA = "#222222"
FONDO_AZUL = "#e3eefb"
FONDO_ROJO = "#fbe3e6"

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


# ===========================================================================
# Impurezas
# ===========================================================================


def proporciones(conteos):
    conteos = np.asarray(conteos, dtype=float)
    return conteos / conteos.sum()


def entropia(conteos):
    p = proporciones(conteos)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def gini(conteos):
    p = proporciones(conteos)
    return float(1 - (p ** 2).sum())


def clasificacion(conteos):
    p = proporciones(conteos)
    return float(1 - p.max())


def varianza(conteos):
    p = proporciones(conteos)
    return float(p[0] * p[1])


def caida(impureza, padre, izquierda, derecha):
    """Delta i(T) = i(N) - P_L i(N_L) - (1 - P_L) i(N_R)."""
    n_izq, n_der = sum(izquierda), sum(derecha)
    p_izq = n_izq / (n_izq + n_der)
    return impureza(padre) - p_izq * impureza(izquierda) - (1 - p_izq) * impureza(derecha)


# ===========================================================================
# CART minimo: cortes binarios x_k <= umbral, crecimiento voraz
# ===========================================================================


class Nodo:
    def __init__(self, conteos):
        self.conteos = conteos          # patrones de cada clase que llegan al nodo
        self.atributo = None            # k de la pregunta "x_k <= umbral?"
        self.umbral = None
        self.izquierda = None
        self.derecha = None

    @property
    def es_hoja(self):
        return self.atributo is None

    @property
    def etiqueta(self):                 # pregunta 5: la clase mayoritaria
        return int(np.argmax(self.conteos))


def contar(y, cantidad_clases):
    return np.bincount(y, minlength=cantidad_clases)


def mejor_corte(X, y, cantidad_clases, impureza):
    padre = contar(y, cantidad_clases)
    mejor = (0.0, None, None)
    for k in range(X.shape[1]):
        valores = np.unique(X[:, k])
        for umbral in (valores[:-1] + valores[1:]) / 2:       # puntos medios
            va_izq = X[:, k] <= umbral
            d = caida(impureza, padre, contar(y[va_izq], cantidad_clases),
                      contar(y[~va_izq], cantidad_clases))
            if d > mejor[0] + 1e-12:
                mejor = (d, k, umbral)
    return mejor


def crecer(X, y, cantidad_clases, impureza=gini, profundidad_max=50, caida_min=0.0, profundidad=0):
    nodo = Nodo(contar(y, cantidad_clases))
    if impureza(nodo.conteos) == 0 or profundidad >= profundidad_max:
        return nodo                                           # pregunta 3: parar
    d, k, umbral = mejor_corte(X, y, cantidad_clases, impureza)
    if k is None or d <= caida_min:
        return nodo
    nodo.atributo, nodo.umbral = k, umbral
    va_izq = X[:, k] <= umbral
    nodo.izquierda = crecer(X[va_izq], y[va_izq], cantidad_clases, impureza, profundidad_max, caida_min,
                            profundidad + 1)
    nodo.derecha = crecer(X[~va_izq], y[~va_izq], cantidad_clases, impureza, profundidad_max, caida_min,
                          profundidad + 1)
    return nodo


def predecir_uno(nodo, x):
    while not nodo.es_hoja:
        nodo = nodo.izquierda if x[nodo.atributo] <= nodo.umbral else nodo.derecha
    return nodo.etiqueta


def predecir(nodo, X):
    return np.array([predecir_uno(nodo, x) for x in X])


def hojas(nodo):
    return 1 if nodo.es_hoja else hojas(nodo.izquierda) + hojas(nodo.derecha)


def profundidad(nodo):
    return 0 if nodo.es_hoja else 1 + max(profundidad(nodo.izquierda), profundidad(nodo.derecha))


def podar_con_validacion(nodo, X, y):
    """Post-poda de error reducido: de abajo hacia arriba, un par de hojas hermanas
    se fusiona si con eso no aumenta el error sobre el conjunto de validacion."""
    if nodo.es_hoja:
        return nodo
    va_izq = X[:, nodo.atributo] <= nodo.umbral
    nodo.izquierda = podar_con_validacion(nodo.izquierda, X[va_izq], y[va_izq])
    nodo.derecha = podar_con_validacion(nodo.derecha, X[~va_izq], y[~va_izq])
    if nodo.izquierda.es_hoja and nodo.derecha.es_hoja:
        errores_hijos = np.sum(predecir(nodo, X) != y) if len(y) else 0
        errores_hoja = np.sum(nodo.etiqueta != y) if len(y) else 0
        if errores_hoja <= errores_hijos:
            nodo.atributo = nodo.umbral = nodo.izquierda = nodo.derecha = None
    return nodo


# ===========================================================================
# Verificaciones
# ===========================================================================


def verificar_ejemplo_90_10():
    titulo("Ejemplo 90/10 de Duda: corte (20,10) | (70,0)")
    padre, izq, der = (90, 10), (20, 10), (70, 0)
    filas = []
    for nombre, f in (("clasificacion", clasificacion), ("Gini", gini), ("entropia", entropia)):
        d = caida(f, padre, izq, der)
        ponderado = 0.3 * f(izq) + 0.7 * f(der)
        filas.append((nombre, f(padre), f(izq), f(der), ponderado, d))
        print(f"  {nombre:13s}: padre {f(padre):.4f}  izq {f(izq):.4f}  der {f(der):.4f}  "
              f"ponderado {ponderado:.4f}  caida {d:.4f}")
    # otro corte malo, para comparar: (45,5) | (45,5)
    for nombre, f in (("clasificacion", clasificacion), ("Gini", gini), ("entropia", entropia)):
        print(f"  corte inutil (45,5)|(45,5) con {nombre}: caida {caida(f, padre, (45, 5), (45, 5)):.4f}")
    return filas


def verificar_nodo_30():
    titulo("Autoevaluacion 7: nodo (20,10)")
    print(f"  Gini {gini((20, 10)):.4f}  entropia {entropia((20, 10)):.4f}  "
          f"clasificacion {clasificacion((20, 10)):.4f}  varianza {varianza((20, 10)):.4f}")
    print(f"  maximos con dos clases: entropia {entropia((1, 1))}, Gini {gini((1, 1))}, "
          f"clasificacion {clasificacion((1, 1))}, varianza {varianza((1, 1))}")
    print(f"  Gini con 3 clases iguales = {gini((1, 1, 1)):.4f}; entropia = {entropia((1, 1, 1)):.4f}")


def datos_xor(rng, n=200):
    X = rng.uniform(-1, 1, (n, 2))
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
    return X, y


def verificar_horizonte():
    titulo("Efecto horizonte sobre un XOR")
    rng = np.random.default_rng(0)
    X, y = datos_xor(rng, 400)
    d, k, u = mejor_corte(X, y, 2, gini)
    print(f"  mejor caida de Gini en la raiz: {d:.4f} (x{k + 1} <= {u:.3f})")
    for umbral in (0.01, 0.0):
        arbol = crecer(X, y, 2, gini, caida_min=umbral)
        err = np.mean(predecir(arbol, X) != y)
        print(f"  parada con caida_min={umbral}: {hojas(arbol)} hojas, error de entrenamiento {err:.3f}")
    # con dos niveles fijos en 0 se separa perfecto
    izq = X[:, 0] <= 0
    print(f"  caida si se corta x1<=0 y despues x2<=0 en cada hijo: "
          f"raiz {caida(gini, contar(y, 2), contar(y[izq], 2), contar(y[~izq], 2)):.4f}, "
          f"hijos quedan puros -> impureza 0")
    return X, y


def datos_oblicuos(rng, n=300):
    X = rng.uniform(0, 1, (n, 2))
    y = (X[:, 1] > X[:, 0]).astype(int)
    return X, y


def verificar_oblicuo():
    titulo("Frontera oblicua x2 = x1: cuantas hojas necesita un arbol axial")
    resultados = []
    for n in (50, 200, 800):
        hs = []
        for semilla in range(10):
            X, y = datos_oblicuos(np.random.default_rng(semilla), n)
            hs.append(hojas(crecer(X, y, 2, gini)))
        resultados.append((n, np.mean(hs), min(hs), max(hs)))
        print(f"  n={n}: hojas del arbol puro = {np.mean(hs):.1f} (min {min(hs)}, max {max(hs)}); "
              f"un nodo multivariado x2 - x1 > 0 alcanza")
    return resultados


def datos_ruidosos(rng, n):
    X = rng.uniform(0, 1, (n, 2))
    y = ((X[:, 0] - 0.5) ** 2 + (X[:, 1] - 0.5) ** 2 < 0.09).astype(int)
    voltear = rng.uniform(size=n) < 0.15
    y[voltear] = 1 - y[voltear]
    return X, y


def verificar_sobreajuste_y_poda():
    titulo("Sobreajuste y poda: circulo con 15% de etiquetas volteadas, 20 semillas")
    profundidades = list(range(1, 16))
    err_ent = np.zeros((20, len(profundidades)))
    err_pru = np.zeros((20, len(profundidades)))
    completo, podado, hojas_c, hojas_p = [], [], [], []
    for semilla in range(20):
        rng = np.random.default_rng(100 + semilla)
        Xe, ye = datos_ruidosos(rng, 300)
        Xv, yv = datos_ruidosos(rng, 150)
        Xp, yp = datos_ruidosos(rng, 2000)
        for j, pmax in enumerate(profundidades):
            a = crecer(Xe, ye, 2, gini, profundidad_max=pmax)
            err_ent[semilla, j] = np.mean(predecir(a, Xe) != ye)
            err_pru[semilla, j] = np.mean(predecir(a, Xp) != yp)
        entero = crecer(Xe, ye, 2, gini)
        completo.append(np.mean(predecir(entero, Xp) != yp))
        hojas_c.append(hojas(entero))
        chico = podar_con_validacion(crecer(Xe, ye, 2, gini), Xv, yv)
        podado.append(np.mean(predecir(chico, Xp) != yp))
        hojas_p.append(hojas(chico))
    print(f"  arbol entero: error de prueba {np.mean(completo):.3f} +- {np.std(completo):.3f}, "
          f"{np.mean(hojas_c):.0f} hojas; error de entrenamiento 0")
    print(f"  podado con validacion: error de prueba {np.mean(podado):.3f} +- {np.std(podado):.3f}, "
          f"{np.mean(hojas_p):.0f} hojas; gana en {np.sum(np.array(podado) < np.array(completo))} de 20")
    mejor = int(np.argmin(err_pru.mean(0)))
    print(f"  mejor profundidad maxima (prueba): {profundidades[mejor]} con error {err_pru.mean(0)[mejor]:.3f}")
    print("  (el error minimo posible es ~0.15, el ruido de etiquetas)")
    return profundidades, err_ent, err_pru, np.mean(completo), np.mean(podado)


def buscar_inestabilidad():
    titulo("Inestabilidad: mover UN punto cambia el arbol")
    grilla = np.stack(np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100)), -1).reshape(-1, 2)
    for semilla in range(40):
        rng = np.random.default_rng(semilla)
        X = np.r_[rng.normal([0.32, 0.32], 0.14, (20, 2)), rng.normal([0.68, 0.68], 0.14, (20, 2))]
        y = np.r_[np.zeros(20, int), np.ones(20, int)]
        X = np.clip(X, 0.02, 0.98)
        base = crecer(X, y, 2, gini, profundidad_max=3)
        zona_base = predecir(base, grilla)
        mejor = None
        for i in range(len(X)):
            for dx, dy in [(0, -0.05), (0, 0.05), (-0.05, 0), (0.05, 0)]:
                X2 = X.copy()
                X2[i] = np.clip(X2[i] + [dx, dy], 0.01, 0.99)
                otro = crecer(X2, y, 2, gini, profundidad_max=3)
                if otro.atributo != base.atributo:
                    cambio = np.mean(predecir(otro, grilla) != zona_base)
                    if mejor is None or cambio > mejor[0]:
                        mejor = (cambio, i, (dx, dy), X2, otro)
        if mejor is not None:
            break
    cambio, i, desplazamiento, X2, otro = mejor
    print(f"  semilla {semilla}: raiz original x{base.atributo + 1} <= {base.umbral:.3f};  moviendo el punto {i} "
          f"en {desplazamiento}: x{otro.atributo + 1} <= {otro.umbral:.3f}")
    print(f"  fraccion del cuadrado que cambia de clase: {cambio:.3f}; hojas {hojas(base)} -> {hojas(otro)}")
    return X, y, base, X2, otro, i


def comparar_con_sklearn():
    titulo("Control contra scikit-learn (DecisionTreeClassifier, criterio Gini)")
    try:
        from sklearn.tree import DecisionTreeClassifier
    except ImportError:
        print("  scikit-learn no instalado: se saltea")
        return
    coincidencias = 0
    for semilla in range(10):
        rng = np.random.default_rng(semilla)
        X, y = datos_ruidosos(rng, 200)
        propio = predecir(crecer(X, y, 2, gini, profundidad_max=4), X)
        sk = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=0).fit(X, y).predict(X)
        coincidencias += np.mean(propio == sk)
    print(f"  acuerdo medio en las predicciones (10 semillas, profundidad 4): {coincidencias / 10:.4f}")


# ===========================================================================
# Figuras
# ===========================================================================


def figura_01_arbol_frutas():
    figura, ejes = plt.subplots(figsize=(11.0, 5.4))
    apagar_ejes(ejes)
    ejes.set_xlim(0, 11)
    ejes.set_ylim(0, 5.6)

    def pregunta(x, y, texto):
        ejes.add_patch(FancyBboxPatch((x - 0.62, y - 0.22), 1.24, 0.44, boxstyle="round,pad=0.02",
                                      fc="#eef4fc", ec=AZUL, lw=1.1))
        ejes.text(x, y, texto, ha="center", va="center", fontsize=8.8, color=AZUL)

    def hoja(x, y, texto, color=TINTA):
        ejes.text(x, y, texto, ha="center", va="center", fontsize=8.6, color=color, weight="bold",
                  bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GRIS, lw=0.8))

    def rama(x0, y0, x1, y1, rotulo):
        ejes.add_patch(FancyArrowPatch((x0, y0 - 0.24), (x1, y1 + 0.24), arrowstyle="-", lw=0.9, color=GRIS))
        ejes.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.05, rotulo, ha="center", va="center", fontsize=7.6,
                  color=TINTA, style="italic", bbox=dict(fc="white", ec="none", pad=0.4))

    pregunta(5.5, 5.1, "¿Color?")
    pregunta(1.9, 3.7, "¿Tamaño?")
    pregunta(5.5, 3.7, "¿Forma?")
    pregunta(9.0, 3.7, "¿Tamaño?")
    rama(5.5, 5.1, 1.9, 3.7, "verde")
    rama(5.5, 5.1, 5.5, 3.7, "amarillo")
    rama(5.5, 5.1, 9.0, 3.7, "rojo")
    hoja(0.7, 2.3, "Sandía")
    hoja(1.9, 2.3, "Manzana", ROJO)
    hoja(3.1, 2.3, "Uva")
    rama(1.9, 3.7, 0.7, 2.3, "grande")
    rama(1.9, 3.7, 1.9, 2.3, "mediana")
    rama(1.9, 3.7, 3.1, 2.3, "chica")
    pregunta(4.6, 2.3, "¿Tamaño?")
    hoja(6.4, 2.3, "Banana", VERDE)
    rama(5.5, 3.7, 4.6, 2.3, "redonda")
    rama(5.5, 3.7, 6.4, 2.3, "fina")
    hoja(3.9, 0.9, "Pomelo")
    hoja(5.3, 0.9, "Limón")
    rama(4.6, 2.3, 3.9, 0.9, "grande")
    rama(4.6, 2.3, 5.3, 0.9, "chica")
    hoja(8.2, 2.3, "Manzana", ROJO)
    pregunta(9.8, 2.3, "¿Sabor?")
    rama(9.0, 3.7, 8.2, 2.3, "mediana")
    rama(9.0, 3.7, 9.8, 2.3, "chica")
    hoja(9.2, 0.9, "Cereza")
    hoja(10.4, 0.9, "Uva")
    rama(9.8, 2.3, 9.2, 0.9, "dulce")
    rama(9.8, 2.3, 10.4, 0.9, "ácida")
    ejes.text(0.1, 5.35, "nivel 0 (raíz)", fontsize=7.5, color=GRIS)
    ejes.text(0.1, 0.25, "Manzana = (verde ∧ mediana) ∨ (rojo ∧ mediana)        "
                         "Banana ⇐ amarillo ∧ fina", fontsize=8.2, color=TINTA)
    guardar(figura, "01-arbol-de-las-frutas.png")


def figura_02_impurezas():
    p = np.linspace(0.0005, 0.9995, 800)
    figura, ejes = plt.subplots(figsize=(6.8, 3.8))
    ent = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    ejes.plot(p, ent, color=ROJO, lw=1.8, label=r"entropía $-\sum P\log_2 P$")
    ejes.plot(p, 1 - p ** 2 - (1 - p) ** 2, color=AZUL, lw=1.8, label=r"Gini $1-\sum P^2$")
    ejes.plot(p, 1 - np.maximum(p, 1 - p), color=NARANJA, lw=1.8, label=r"clasificación $1-\max P$")
    ejes.plot(p, p * (1 - p), color=VERDE, lw=1.4, ls="--", label=r"varianza $P_1P_2$")
    ejes.set_xlabel(r"$P(\omega_1)$ en el nodo")
    ejes.set_ylabel("$i(N)$")
    ejes.set_title("Las cuatro impurezas con dos clases")
    ejes.legend(fontsize=8)
    ejes.set_ylim(0, 1.05)
    guardar(figura, "02-impurezas.png")


def figura_03_ejemplo_90_10(filas):
    figura, (ejes_a, ejes_b) = plt.subplots(1, 2, figsize=(11.0, 3.8), gridspec_kw={"width_ratios": [1, 1.1]})
    apagar_ejes(ejes_a)
    ejes_a.set_xlim(0, 6)
    ejes_a.set_ylim(0, 4)

    def nodo(x, y, a, b, texto):
        ejes_a.add_patch(FancyBboxPatch((x - 1.15, y - 0.4), 2.3, 0.8, boxstyle="round,pad=0.02",
                                        fc="white", ec=TINTA))
        ejes_a.text(x, y + 0.12, f"{a} de $\\omega_1$ / {b} de $\\omega_2$", ha="center", fontsize=8.3)
        ejes_a.text(x, y - 0.2, texto, ha="center", fontsize=7.6, color=GRIS)

    nodo(3, 3.3, 90, 10, "padre $N$")
    nodo(1.4, 1.1, 20, 10, "$N_L$ ($P_L = 0{,}3$)")
    nodo(4.6, 1.1, 70, 0, "$N_R$: puro")
    for x in (1.4, 4.6):
        ejes_a.add_patch(FancyArrowPatch((3, 2.88), (x, 1.52), arrowstyle="-|>", mutation_scale=10,
                                         color=TINTA))
    ejes_a.set_title("El corte de Duda: deja un hijo puro")

    nombres = [{"clasificacion": "clasificación", "entropia": "entropía"}.get(f[0], f[0]) for f in filas]
    x = np.arange(len(filas))
    ejes_b.bar(x - 0.2, [f[1] for f in filas], 0.38, color=GRIS_CLARO, label="$i(N)$ del padre")
    ejes_b.bar(x + 0.2, [f[4] for f in filas], 0.38, color=AZUL, label="hijos ponderados")
    for j, f in enumerate(filas):
        ejes_b.text(j, max(f[1], f[4]) + 0.02, f"$\\Delta i$ = {abs(f[5]) if abs(f[5]) < 1e-9 else f[5]:.3f}".replace(".", ","), ha="center",
                    fontsize=8.5, color=ROJO if f[5] < 1e-9 else VERDE)
    ejes_b.set_xticks(x)
    ejes_b.set_xticklabels(nombres)
    ejes_b.set_ylim(0, 0.6)
    ejes_b.set_title("Cuánto baja cada impureza")
    ejes_b.legend(fontsize=8, loc="upper left")
    guardar(figura, "03-ejemplo-90-10.png")


def dibujar_regiones(ejes, arbol, X, y, titulo_ejes, limites=(0, 1, 0, 1), pasos=300):
    x0, x1, y0, y1 = limites
    gx, gy = np.meshgrid(np.linspace(x0, x1, pasos), np.linspace(y0, y1, pasos))
    z = predecir(arbol, np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
    ejes.contourf(gx, gy, z, levels=[-0.5, 0.5, 1.5], colors=[FONDO_AZUL, FONDO_ROJO])
    ejes.contour(gx, gy, z, levels=[0.5], colors=[TINTA], linewidths=1.0)
    ejes.scatter(X[y == 0, 0], X[y == 0, 1], s=8, color=AZUL)
    ejes.scatter(X[y == 1, 0], X[y == 1, 1], s=8, color=ROJO)
    ejes.set_xlim(x0, x1)
    ejes.set_ylim(y0, y1)
    ejes.set_title(titulo_ejes)
    ejes.set_xlabel("$x_1$")
    ejes.set_ylabel("$x_2$")


def figura_04_cortes_axiales():
    rng = np.random.default_rng(4)
    X = np.r_[rng.normal([0.3, 0.3], 0.12, (60, 2)), rng.normal([0.72, 0.4], 0.1, (40, 2)),
              rng.normal([0.45, 0.78], 0.1, (40, 2))]
    y = np.r_[np.zeros(60, int), np.ones(40, int), np.ones(40, int)]
    X = np.clip(X, 0.01, 0.99)
    figura, ejes = plt.subplots(1, 3, figsize=(11.5, 3.7))
    for e, pmax in zip(ejes, (1, 2, 5)):
        arbol = crecer(X, y, 2, gini, profundidad_max=pmax)
        dibujar_regiones(e, arbol, X, y, f"profundidad {pmax}: {hojas(arbol)} hojas")
    guardar(figura, "04-cortes-paralelos-a-los-ejes.png")


def figura_05_oblicua_y_xor(X_xor, y_xor):
    X, y = datos_oblicuos(np.random.default_rng(0), 200)
    arbol = crecer(X, y, 2, gini)
    figura, ejes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    dibujar_regiones(ejes[0], arbol, X, y, f"Frontera oblicua: {hojas(arbol)} hojas en escalera")
    ejes[0].plot([0, 1], [0, 1], color=VERDE, lw=1.4, ls="--")
    ejes[0].text(0.55, 0.08, "un nodo multivariado\n$x_2 - x_1 > 0$ alcanza", color=VERDE, fontsize=8)
    arbol_x = crecer(X_xor, y_xor, 2, gini, profundidad_max=2)
    d, k, u = mejor_corte(X_xor, y_xor, 2, gini)
    dibujar_regiones(ejes[1], arbol_x, X_xor, y_xor,
                     f"XOR: la mejor caída en la raíz es {d:.4f}".replace(".", ","), limites=(-1, 1, -1, 1))
    guardar(figura, "05-oblicua-y-xor.png")


def figura_06_sobreajuste(profundidades, err_ent, err_pru, completo, podado):
    figura, ejes = plt.subplots(figsize=(7.2, 3.9))
    ejes.plot(profundidades, err_ent.mean(0), "o-", color=AZUL, ms=3.5, label="entrenamiento")
    ejes.plot(profundidades, err_pru.mean(0), "o-", color=ROJO, ms=3.5, label="prueba")
    ejes.axhline(0.15, color=GRIS, ls=":", lw=1)
    ejes.text(12.0, 0.137, "ruido de etiquetas (15 %)", fontsize=7.5, color=GRIS)
    ejes.axhline(podado, color=VERDE, ls="--", lw=1.2)
    ejes.text(1.2, podado + 0.008, f"árbol entero podado con validación: {podado:.3f}".replace(".", ","),
              fontsize=7.8, color=VERDE)
    ejes.set_xlabel("profundidad máxima (pre-poda)")
    ejes.set_ylabel("error")
    ejes.set_title("Sobreajuste de un árbol (20 semillas)")
    ejes.legend(fontsize=8, loc="upper right")
    guardar(figura, "06-sobreajuste-y-poda.png")


def figura_07_inestabilidad(X, y, base, X2, otro, i):
    figura, ejes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    dibujar_regiones(ejes[0], base, X, y, f"Original: raíz $x_{base.atributo + 1} \\leq$ "
                                          f"{base.umbral:.2f}".replace(".", ","))
    dibujar_regiones(ejes[1], otro, X2, y, f"Un punto movido: raíz $x_{otro.atributo + 1} \\leq$ "
                                           f"{otro.umbral:.2f}".replace(".", ","))
    for e, XX in ((ejes[0], X), (ejes[1], X2)):
        e.scatter([XX[i, 0]], [XX[i, 1]], s=90, facecolors="none", edgecolors=VERDE, linewidths=1.8)
    ejes[1].annotate("", xy=X2[i], xytext=X[i], arrowprops=dict(arrowstyle="-|>", color=VERDE))
    guardar(figura, "07-inestabilidad.png")


def main():
    filas = verificar_ejemplo_90_10()
    verificar_nodo_30()
    X_xor, y_xor = verificar_horizonte()
    verificar_oblicuo()
    resultados = verificar_sobreajuste_y_poda()
    inestable = buscar_inestabilidad()
    comparar_con_sklearn()
    titulo("Figuras")
    figura_01_arbol_frutas()
    figura_02_impurezas()
    figura_03_ejemplo_90_10(filas)
    figura_04_cortes_axiales()
    figura_05_oblicua_y_xor(X_xor, y_xor)
    figura_06_sobreajuste(*resultados)
    figura_07_inestabilidad(*inestable)


if __name__ == "__main__":
    main()
