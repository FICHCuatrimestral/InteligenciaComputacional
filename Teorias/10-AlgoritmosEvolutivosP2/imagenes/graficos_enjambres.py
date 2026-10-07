"""Figuras y verificaciones de los apuntes de la unidad 10.

Genera los PNG que usan ../Resumenes/01-variantes.md, 02-colonias-de-hormigas.md
y 03-enjambre-de-particulas.md, e imprime todos los números que citan.
Implementa: estrategia evolutiva (1+1) con regla de 1/5 y (mu+lambda)/(mu,lambda),
colonia de hormigas simple (sACO) y sistema de hormigas (AS), y enjambre de
partículas del mejor global y del mejor local.

    python3 graficos_enjambres.py          (tarda unos dos minutos)
"""

import os
import itertools

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Ellipse

DIR = os.path.dirname(os.path.abspath(__file__))
AZUL, ROJO, VERDE, NARANJA, VIOLETA = "#2a78d6", "#d1495b", "#1baf7a", "#eb6834", "#7b5cc4"
GRIS, GRIS_CLARO, TINTA = "#8a8f98", "#c8ccd2", "#222222"
FONDO_AZUL, FONDO_VERDE, FONDO_NARANJA = "#e3eefb", "#ddf3ea", "#fdeadf"

plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "grid.linestyle": ":", "figure.dpi": 150,
                     "savefig.bbox": "tight", "savefig.facecolor": "white"})


def guardar(fig, nombre):
    fig.savefig(os.path.join(DIR, nombre)); plt.close(fig); print("generado:", nombre)


def titulo(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


def apagar(ax):
    ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def rastrigin(x):
    x = np.atleast_2d(x)
    return 10 * x.shape[1] + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x), axis=1)


def esfera(x):
    return np.sum(np.atleast_2d(x) ** 2, axis=1)


# ===========================================================================
# 01 — Variantes: estrategias de evolución
# ===========================================================================


def es_1mas1(f, x0, sigma0, iteraciones, generador, regla=True, cada=20):
    x, fx, s = np.array(x0, float), f(x0)[0], sigma0
    camino, sigmas, fs, exitos = [x.copy()], [s], [fx], []
    for t in range(iteraciones):
        hijo = x + s * generador.normal(size=x.shape)
        fh = f(hijo)[0]
        exito = fh < fx                       # la mutación sólo se acepta si no empeora
        exitos.append(exito)
        if exito:
            x, fx = hijo, fh
        if regla and (t + 1) % cada == 0:     # regla de 1/5 sobre las últimas `cada` mutaciones
            tasa = np.mean(exitos[-cada:])
            s = s / 0.85 if tasa > 0.2 else s * 0.85 if tasa < 0.2 else s
        camino.append(x.copy()); sigmas.append(s); fs.append(fx)
    return np.array(camino), np.array(sigmas), np.array(fs)


def figura_es():
    titulo("(1+1)-ES con y sin regla de 1/5 (esfera 2D)")
    resultados = {}
    fig, (ea, eb) = plt.subplots(1, 2, figsize=(10, 3.4))
    for regla, color, nombre in [(False, ROJO, "σ fijo = 1"), (True, VERDE, "σ con regla de 1/5")]:
        finales = []
        for s in range(20):
            g = np.random.default_rng(s)
            camino, sig, fs = es_1mas1(esfera, [8.0, 6.0], 1.0, 600, g, regla=regla)
            finales.append(fs[-1])
            if s == 0:
                ea.plot(camino[:, 0], camino[:, 1], color=color, linewidth=1, label=nombre)
                eb.semilogy(fs, color=color, label=f"f del padre, {nombre}")
                if regla:
                    eb.semilogy(sig, color=VERDE, linestyle="--", linewidth=1, label="σ (regla de 1/5)")
        resultados[nombre] = np.median(finales)
        print(f"  {nombre}: f final mediana (20 semillas, 600 iteraciones) = {np.median(finales):.2e}")
    ea.plot(0, 0, "*", color=TINTA, markersize=12); ea.plot(8, 6, "o", color=TINTA)
    ea.set_aspect("equal"); ea.legend(fontsize=7); ea.set_title("Camino del padre desde (8, 6)")
    eb.set_xlabel("iteración"); eb.legend(fontsize=7); eb.set_title("f y tamaño de paso")
    guardar(fig, "v1-es-regla-un-quinto.png")
    return resultados


def es_mu_lambda(f, mu, lam, plus, dim, iteraciones, generador, tau=None):
    tau = tau or 1 / np.sqrt(dim)
    X = generador.uniform(-5.12, 5.12, (mu, dim)); S = np.full((mu, dim), 1.0)
    F = f(X); hist = [F.min()]
    for _ in range(iteraciones):
        padres = generador.integers(0, mu, lam)                   # selección de padres al azar
        Sh = S[padres] * np.exp(tau * generador.normal(size=(lam, dim)))   # muta primero σ
        Xh = X[padres] + Sh * generador.normal(size=(lam, dim))           # y con ese σ, x
        Fh = f(Xh)
        if plus:
            Xa, Sa, Fa = np.vstack([X, Xh]), np.vstack([S, Sh]), np.concatenate([F, Fh])
        else:
            Xa, Sa, Fa = Xh, Sh, Fh
        orden = np.argsort(Fa)[:mu]                               # reproducción determinística
        X, S, F = Xa[orden], Sa[orden], Fa[orden]
        hist.append(F.min())
    return np.array(hist), S


def figura_mu_lambda():
    titulo("(mu+lambda) contra (mu,lambda) en Rastrigin 5D")
    fig, ax = plt.subplots(figsize=(7, 3))
    for plus, color, nombre in [(True, AZUL, "(μ + λ) = (10 + 70)"), (False, NARANJA, "(μ, λ) = (10, 70)")]:
        curvas = []
        for s in range(15):
            h, S = es_mu_lambda(rastrigin, 10, 70, plus, 5, 300, np.random.default_rng(100 + s))
            curvas.append(h)
        curvas = np.array(curvas)
        ax.semilogy(np.median(curvas, axis=0), color=color, label=nombre)
        sube = np.mean(np.any(np.diff(curvas, axis=1) > 1e-12, axis=1))
        print(f"  {nombre}: f final mediana {np.median(curvas[:, -1]):.2f}; corridas donde el mejor alguna vez empeora: {sube:.0%}")
    ax.set_xlabel("generación"); ax.set_ylabel("mejor f (mediana de 15)"); ax.legend(fontsize=8)
    ax.set_title("Rastrigin, 5 variables")
    guardar(fig, "v2-mu-lambda.png")


def verificar_siete_bits():
    titulo("Representación: 0..100 con 7 bits")
    invalidos = sum(1 for v in range(128) if v > 100)
    print(f"  enteros de 7 bits mayores que 100: {invalidos} de 128 ({invalidos / 128:.1%})")
    # probabilidad de que una mutación de 1 bit lleve un valor válido a inválido
    total = cuenta = 0
    for v in range(101):
        for b in range(7):
            total += 1
            cuenta += (v ^ (1 << b)) > 100
    print(f"  mutación de un bit sobre un valor válido que lo vuelve inválido: {cuenta}/{total} = {cuenta / total:.1%}")
    print(f"  con escala x = 100*entero/127: resolución {100 / 127:.4f}")
    for v in (0, 64, 127):
        print(f"    entero {v} -> {100 * v / 127:.2f}")


# ---------------------------------------------------------------------------
# Programación genética: el ejemplo de la cátedra
# ---------------------------------------------------------------------------


def evaluar(arbol, A, B):
    op = arbol[0]
    if op == "A": return A
    if op == "B": return B
    if op == "NOT": return not evaluar(arbol[1], A, B)
    a, b = evaluar(arbol[1], A, B), evaluar(arbol[2], A, B)
    return {"AND": a and b, "OR": a or b, "XOR": a != b}[op]


def texto(arbol):
    op = arbol[0]
    if op in ("A", "B"): return op
    if op == "NOT": return f"NOT {texto(arbol[1])}"
    return f"({texto(arbol[1])} {op} {texto(arbol[2])})"


def preorden(arbol, ruta=()):
    yield ruta, arbol
    for i, h in enumerate(arbol[1:]):
        yield from preorden(h, ruta + (i + 1,))


def reemplazar(arbol, ruta, nuevo):
    if not ruta: return nuevo
    l = list(arbol); l[ruta[0]] = reemplazar(arbol[ruta[0]], ruta[1:], nuevo); return tuple(l)


def subarbol(arbol, ruta):
    for r in ruta: arbol = arbol[r]
    return arbol


def dibujar_arbol(ax, arbol, x, y, ancho, numerar, resaltar, ruta=(), contador=None):
    """resaltar: ruta (tupla) del subárbol a pintar; numerar: si se escribe el número en preorden."""
    if contador is None:
        contador = [0]
    contador[0] += 1
    n = contador[0]
    op = arbol[0]
    hoja = op in ("A", "B")
    marcado = resaltar is not None and ruta[:len(resaltar)] == resaltar
    col, fondo = (NARANJA, FONDO_NARANJA) if marcado else (TINTA, "white")
    if hoja:
        ax.add_patch(Rectangle((x - 0.22, y - 0.17), 0.44, 0.34, facecolor=fondo, edgecolor=col))
    else:
        ax.add_patch(Ellipse((x, y), 0.95, 0.38, facecolor=fondo, edgecolor=col))
    ax.text(x, y, op, ha="center", va="center", fontsize=8, fontstyle="italic" if hoja else "normal")
    if numerar:
        ax.text(x + 0.42, y + 0.2, str(n), fontsize=7, color=GRIS)
    hijos = arbol[1:]
    xs = [x] if len(hijos) == 1 else [x - ancho / 2, x + ancho / 2]
    for i, (h, xh) in enumerate(zip(hijos, xs)):
        ax.plot([x, xh], [y - 0.19, y - 0.8], color=GRIS, linewidth=0.8)
        dibujar_arbol(ax, h, xh, y - 1.0, ancho / 2, numerar, resaltar, ruta + (i + 1,), contador)


def figura_pg():
    titulo("Programación genética: cruza del ejemplo de la cátedra")
    padre1 = ("OR", ("NOT", ("B",)), ("AND", ("NOT", ("A",)), ("B",)))
    padre2 = ("AND", ("XOR", ("B",), ("NOT", ("A",))), ("OR", ("NOT", ("A",)), ("B",)))
    rutas1 = [r for r, _ in preorden(padre1)]; rutas2 = [r for r, _ in preorden(padre2)]
    r1, r2 = rutas1[2 - 1], rutas2[6 - 1]
    s1, s2 = subarbol(padre1, r1), subarbol(padre2, r2)
    hijo1, hijo2 = reemplazar(padre1, r1, s2), reemplazar(padre2, r2, s1)
    for nombre, a in [("padre 1", padre1), ("padre 2", padre2), ("hijo 1", hijo1), ("hijo 2", hijo2)]:
        tabla = [int(evaluar(a, A, B)) for A, B in itertools.product([0, 1], repeat=2)]
        print(f"  {nombre}: {texto(a)}   tabla (A,B)=00,01,10,11 -> {tabla}")
    fig, ejes = plt.subplots(1, 4, figsize=(12.5, 3.2))
    for ax, (nombre, a, ruta, numerar) in zip(ejes, [("padre 1 (corte en el nodo 2)", padre1, r1, True),
                                                    ("padre 2 (corte en el nodo 6)", padre2, r2, True),
                                                    ("hijo 1", hijo1, r1, False),
                                                    ("hijo 2", hijo2, r2, False)]):
        apagar(ax)
        dibujar_arbol(ax, a, 0, 0, 2.2, numerar, ruta)
        ax.set_xlim(-2.3, 2.3); ax.set_ylim(-3.4, 0.5); ax.set_title(nombre, fontsize=9)
    guardar(fig, "v3-pg-cruza.png")


# ===========================================================================
# 02 — Colonia de hormigas
# ===========================================================================


def puente(largos, hormigas, iteraciones, generador, alfa=1.0, rho=0.1, sigma0=0.01, deposito="global", abre_en=0):
    """Puente binario: dos ramas de longitudes `largos`. Una iteración = todas las hormigas
    van y vuelven; deposito global = 1/longitud por hormiga."""
    sigma = generador.uniform(0, sigma0, 2)
    fraccion = []
    for t in range(iteraciones):
        if t == abre_en and abre_en > 0:
            sigma[0] = generador.uniform(0, sigma0)              # la rama 0 recién aparece
        p = sigma ** alfa / np.sum(sigma ** alfa)
        if t < abre_en:
            p = np.array([0.0, 1.0])                             # rama 0 todavía cerrada
        elecciones = generador.random(hormigas) < p[0]       # True = rama 0
        n0 = elecciones.sum(); n1 = hormigas - n0
        fraccion.append(n0 / hormigas)
        sigma = (1 - rho) * sigma
        if deposito == "global":
            sigma += np.array([n0 / largos[0], n1 / largos[1]])
        else:
            sigma += np.array([n0, n1], float)
    return np.array(fraccion), sigma


def figura_puente():
    titulo("Puente binario")
    fig, (ea, eb) = plt.subplots(1, 2, figsize=(10, 3.2))
    finales = []
    for s in range(30):
        fr, _ = puente((1.0, 2.0), 10, 60, np.random.default_rng(s))
        finales.append(fr[-5:].mean())
        ea.plot(fr, color=AZUL, alpha=0.25, linewidth=1)
    ea.set_ylim(-0.03, 1.03); ea.axhline(0.5, color=GRIS, linestyle="--", linewidth=0.8)
    ea.set_xlabel("iteración"); ea.set_ylabel("fracción que va por la rama corta")
    ea.set_title("Ramas de largo 1 y 2: 30 corridas", fontsize=9)
    gana_corta = np.mean(np.array(finales) > 0.9)
    print(f"  ramas 1 y 2: la rama corta termina con > 90 % de las hormigas en {gana_corta:.0%} de 30 corridas")
    finales_iguales = []
    for s in range(30):
        fr, _ = puente((1.0, 1.0), 10, 60, np.random.default_rng(100 + s), alfa=2.0)
        finales_iguales.append(fr[-5:].mean())
        eb.plot(fr, color=VIOLETA, alpha=0.25, linewidth=1)
    fi = np.array(finales_iguales)
    print(f"  ramas iguales (alfa=2): terminan casi todas en una sola rama (>90 % o <10 %) en {np.mean((fi > 0.9) | (fi < 0.1)):.0%}; la rama 0 gana en {np.mean(fi > 0.5):.0%}")
    eb.set_ylim(-0.03, 1.03); eb.axhline(0.5, color=GRIS, linestyle="--", linewidth=0.8)
    eb.set_xlabel("iteración"); eb.set_ylabel("fracción por la rama 0"); eb.set_title("Ramas iguales (α = 2): se elige una al azar y se refuerza", fontsize=9)
    guardar(fig, "h1-puente-binario.png")


def ejemplo_probabilidades():
    titulo("Probabilidades de transición a mano")
    sigma = np.array([0.20, 0.21, 0.19])
    for alfa in (1, 5, 20):
        p = sigma ** alfa / np.sum(sigma ** alfa)
        print(f"  alfa={alfa}: p = {np.round(p, 3)}")
    d = np.array([1.0, 2.0, 4.0]); eta = 1 / d
    for alfa, beta in [(1, 0), (1, 1), (1, 2)]:
        num = sigma ** alfa * eta ** beta
        print(f"  AS alfa={alfa} beta={beta}: numeradores {np.round(num, 4)} -> p = {np.round(num / num.sum(), 3)}")
    # actualización a mano
    s = 0.5; rho = 0.1
    print(f"  evaporación: 0.5 -> {(1 - rho) * s:.3f}; con dos hormigas de caminos 4 y 5 por la arista: {(1 - rho) * s + 1 / 4 + 1 / 5:.3f}")


def grafo_cuadricula(n=5):
    """Cuadrícula n x n de nodos, aristas a los vecinos (4-conexión) con largo 1,
    más un 'atajo' diagonal largo de costo 1.6 en algunas celdas para que haya
    varios caminos de largos distintos."""
    nodos = [(i, j) for i in range(n) for j in range(n)]
    idx = {v: k for k, v in enumerate(nodos)}
    aristas = {}
    for (i, j) in nodos:
        for di, dj in ((1, 0), (0, 1)):
            a, b = (i, j), (i + di, j + dj)
            if b in idx:
                aristas[(idx[a], idx[b])] = aristas[(idx[b], idx[a])] = 1.0
    return nodos, idx, aristas


def sACO(nodos, aristas, origen, destino, hormigas, iteraciones, generador, alfa=1.0, rho=0.1, sigma0=0.1,
         tabu=False, beta=0.0, deposito="global", Q=1.0, guardar_t=()):
    n = len(nodos)
    vecinos = {i: [j for (a, j) in aristas if a == i] for i in range(n)}
    sigma = {e: generador.uniform(0, sigma0) for e in aristas}
    mejor, mejor_largo, historia, fotos = None, np.inf, [], {}
    for t in range(iteraciones):
        caminos = []
        for k in range(hormigas):
            i, camino, visitados = origen, [origen], {origen}
            pasos = 0
            while i != destino and pasos < 10 * n:
                cand = [j for j in vecinos[i] if not (tabu and j in visitados)]
                if not cand:
                    break
                w = np.array([sigma[(i, j)] ** alfa * (1 / aristas[(i, j)]) ** beta for j in cand])
                j = cand[generador.choice(len(cand), p=w / w.sum())]
                camino.append(j); visitados.add(j); i = j; pasos += 1
            if i != destino:
                continue
            # eliminar ciclos
            limpio = []
            for v in camino:
                if v in limpio:
                    limpio = limpio[:limpio.index(v) + 1]
                else:
                    limpio.append(v)
            largo = sum(aristas[(a, b)] for a, b in zip(limpio[:-1], limpio[1:]))
            caminos.append((limpio, largo))
            if largo < mejor_largo:
                mejor, mejor_largo = limpio, largo
        for e in sigma:
            sigma[e] *= (1 - rho)
        for camino, largo in caminos:
            for a, b in zip(camino[:-1], camino[1:]):
                d = {"global": Q / largo, "uniforme": Q, "local": Q / aristas[(a, b)]}[deposito]
                sigma[(a, b)] += d
                sigma[(b, a)] += d
        largos = [l for _, l in caminos]
        historia.append((np.mean(largos) if largos else np.nan, mejor_largo))
        if t in guardar_t:
            fotos[t] = dict(sigma)
    return mejor, mejor_largo, np.array(historia), fotos


def figura_aco_cuadricula():
    titulo("sACO en una cuadrícula 6x6 con obstáculo")
    n = 6
    nodos, idx, aristas = grafo_cuadricula(n)
    # obstáculo: se quitan las aristas que entran a los nodos de una pared
    pared = [(2, j) for j in range(0, 4)]
    for p in pared:
        for e in list(aristas):
            if idx[p] in e:
                del aristas[e]
    origen, destino = idx[(0, 0)], idx[(n - 1, 0)]
    g = np.random.default_rng(3)
    mejor, largo, hist, fotos = sACO(nodos, aristas, origen, destino, 15, 60, g, alfa=1.0, rho=0.1, guardar_t=(0, 10, 59))
    # BFS
    from collections import deque
    dist = {origen: 0}; q = deque([origen]); vec = {}
    for (a, b) in aristas: vec.setdefault(a, []).append(b)
    while q:
        u = q.popleft()
        for v in vec.get(u, []):
            if v not in dist: dist[v] = dist[u] + 1; q.append(v)
    print(f"  BFS: largo mínimo = {dist[destino]}; sACO encontró {largo}; largo medio de las hormigas: iteración 0 = {hist[0, 0]:.1f}, iteración 59 = {hist[-1, 0]:.1f}")
    fig, ejes = plt.subplots(1, 3, figsize=(11, 3.8))
    for ax, t in zip(ejes, (0, 10, 59)):
        apagar(ax); ax.set_aspect("equal")
        s = fotos[t]; smax = max(s.values())
        for (a, b), v in s.items():
            if a < b:
                (i1, j1), (i2, j2) = nodos[a], nodos[b]
                ax.plot([i1, i2], [j1, j2], color=NARANJA, linewidth=0.3 + 6 * v / smax, alpha=0.85, solid_capstyle="round")
        for (i, j) in nodos:
            if (i, j) in pared:
                ax.add_patch(Rectangle((i - 0.3, j - 0.3), 0.6, 0.6, color=GRIS_CLARO))
            else:
                ax.plot(i, j, "o", color=TINTA, markersize=2.5)
        ax.plot(*nodos[origen], "s", color=AZUL, markersize=8); ax.plot(*nodos[destino], "*", color=VERDE, markersize=13)
        ax.set_title(f"feromonas después de la iteración {t + 1}", fontsize=9)
        ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.6, n - 0.4)
    guardar(fig, "h2-aco-cuadricula.png")
    return dist[destino], largo


def figura_evaporacion():
    titulo("Evaporación y alfa en el puente (ramas 1 y 1,5; 60 corridas)")
    fig, (ea, eb) = plt.subplots(1, 2, figsize=(10.5, 3.2))
    for rho, color in [(0.0, ROJO), (0.1, AZUL)]:
        fin, curvas = [], []
        for s in range(60):
            fr, _ = puente((1.0, 1.5), 10, 100, np.random.default_rng(s), alfa=1.0, rho=rho)
            fin.append(fr[-10:].mean()); curvas.append(fr)
        fin = np.array(fin)
        ea.plot(np.mean(curvas, axis=0), color=color, label=f"ρ = {rho}")
        print(f"  alfa=1, rho={rho}: la corta queda con > 90 % en {np.mean(fin > 0.9):.0%}; la larga con > 90 % en {np.mean(fin < 0.1):.0%}; fracción media final {fin.mean():.2f}")
    ea.set_ylim(0, 1.02); ea.set_xlabel("iteración"); ea.set_ylabel("fracción por la rama corta (media)")
    ea.legend(fontsize=8); ea.set_title("α = 1: sin evaporación la colonia no termina de decidir", fontsize=9)
    bins = np.linspace(0, 1, 11)
    for alfa, color in [(1.0, AZUL), (2.0, NARANJA)]:
        fin = []
        for s in range(60):
            fr, _ = puente((1.0, 1.5), 10, 100, np.random.default_rng(s), alfa=alfa, rho=0.1)
            fin.append(fr[-10:].mean())
        fin = np.array(fin)
        eb.hist(fin, bins=bins, alpha=0.6, color=color, label=f"α = {alfa:g}")
        print(f"  rho=0.1, alfa={alfa}: corta > 90 % en {np.mean(fin > 0.9):.0%}; larga > 90 % en {np.mean(fin < 0.1):.0%}")
    eb.set_xlabel("fracción final por la rama corta"); eb.set_ylabel("corridas"); eb.legend(fontsize=8)
    eb.set_title("ρ = 0,1: con α = 2, una de cada tres se queda con la larga", fontsize=9)
    guardar(fig, "h3-evaporacion.png")


def figura_as_viajante():
    titulo("Sistema de hormigas (AS) en un viajante de 12 ciudades")
    g = np.random.default_rng(7)
    ciudades = g.uniform(0, 10, (12, 2))
    n = len(ciudades)
    D = np.linalg.norm(ciudades[:, None] - ciudades[None], axis=2)
    # óptimo exacto por fuerza bruta reducida (Held-Karp)
    from functools import lru_cache
    @lru_cache(None)
    def hk(mask, j):
        if mask == (1 << j) | 1 and j != 0:
            return D[0, j]
        best = np.inf
        prev = mask & ~(1 << j)
        for k in range(1, n):
            if prev & (1 << k):
                best = min(best, hk(prev, k) + D[k, j])
        return best
    full = (1 << n) - 1
    optimo = min(hk(full, j) + D[j, 0] for j in range(1, n))
    print(f"  recorrido óptimo (Held-Karp): {optimo:.3f}")

    def AS(alfa, beta, rho, Q, deposito, iters, gen, m=12):
        sigma = gen.uniform(0, 0.01, (n, n))
        mejor, mejor_l, hist = None, np.inf, []
        for _ in range(iters):
            tours = []
            for k in range(m):
                i = gen.integers(n); tour = [i]; libres = set(range(n)) - {i}
                while libres:
                    c = np.array(sorted(libres))
                    w = sigma[i, c] ** alfa * (1 / D[i, c]) ** beta
                    j = c[gen.choice(len(c), p=w / w.sum())]
                    tour.append(j); libres.remove(j); i = j
                L = sum(D[a, b] for a, b in zip(tour, tour[1:] + tour[:1]))
                tours.append((tour, L))
                if L < mejor_l: mejor, mejor_l = tour, L
            sigma *= (1 - rho)
            for tour, L in tours:
                for a, b in zip(tour, tour[1:] + tour[:1]):
                    d = {"global": Q / L, "uniforme": Q, "local": Q / D[a, b]}[deposito]
                    sigma[a, b] += d; sigma[b, a] += d
            hist.append(mejor_l)
        return mejor, mejor_l, np.array(hist)

    fig, (ea, eb) = plt.subplots(1, 2, figsize=(10.5, 3.4), gridspec_kw={"width_ratios": [1.3, 1]})
    resultados = {}
    for (nombre, kw, color) in [("β = 0 (sólo feromonas)", dict(beta=0, deposito="global"), ROJO),
                                ("β = 2, depósito global", dict(beta=2, deposito="global"), AZUL),
                                ("β = 2, depósito uniforme", dict(beta=2, deposito="uniforme"), NARANJA),
                                ("β = 2, depósito local", dict(beta=2, deposito="local"), VIOLETA)]:
        curvas, finales = [], []
        for s in range(10):
            mej, L, h = AS(alfa=1, rho=0.5, Q=1, iters=60, gen=np.random.default_rng(300 + s), **kw)
            curvas.append(h); finales.append(L)
        ea.plot(np.median(curvas, axis=0) / optimo, color=color, label=nombre)
        resultados[nombre] = (np.median(finales) / optimo, np.mean(np.isclose(finales, optimo)))
        print(f"  {nombre}: mejor recorrido / óptimo, mediana de 10 = {np.median(finales) / optimo:.3f}; óptimo exacto en {np.mean(np.isclose(finales, optimo)):.0%}")
    ea.set_xlabel("iteración"); ea.set_ylabel("mejor recorrido / óptimo"); ea.legend(fontsize=7)
    ea.set_title("Doce ciudades, 12 hormigas, α = 1, ρ = 0,5")
    mej, L, _ = AS(1, 2, 0.5, 1, "global", 60, np.random.default_rng(300))
    t = mej + mej[:1]
    eb.plot(ciudades[t, 0], ciudades[t, 1], "-", color=AZUL)
    eb.plot(ciudades[:, 0], ciudades[:, 1], "o", color=TINTA, markersize=4)
    eb.set_aspect("equal"); eb.set_title(f"Recorrido encontrado: {L:.2f} (óptimo {optimo:.2f})", fontsize=9)
    guardar(fig, "h4-as-viajante.png")
    return optimo, resultados


# ===========================================================================
# 03 — Enjambre de partículas
# ===========================================================================


def pso(f, dim, N, iters, gen, c1=1.5, c2=1.5, w=1.0, vmax=None, topologia="global", vecinos=1,
        lim=5.12, guardar_t=()):
    X = gen.uniform(-lim, lim, (N, dim)); V = np.zeros((N, dim))
    Y = X.copy(); FY = f(Y)
    hist, vel, fotos = [], [], {}
    for t in range(iters):
        FX = f(X)
        mejora = FX < FY
        Y[mejora], FY[mejora] = X[mejora], FX[mejora]
        if topologia == "global":
            Yh = np.tile(Y[np.argmin(FY)], (N, 1))
        else:
            Yh = np.empty_like(Y)
            for k in range(N):
                vec = [(k + d) % N for d in range(-vecinos, vecinos + 1)]
                Yh[k] = Y[vec[np.argmin(FY[vec])]]
        if t in guardar_t:
            fotos[t] = (X.copy(), Y[np.argmin(FY)].copy())
        r1, r2 = gen.random((N, dim)), gen.random((N, dim))
        V = w * V + c1 * r1 * (Y - X) + c2 * r2 * (Yh - X)
        if vmax is not None:
            V = np.clip(V, -vmax, vmax)
        X = X + V
        hist.append(FY.min()); vel.append(np.mean(np.linalg.norm(V, axis=1)))
    return np.array(hist), np.array(vel), fotos, Y[np.argmin(FY)]


def ejemplo_velocidad():
    titulo("Actualización de la velocidad a mano")
    x = np.array([2.0, 3.0]); v = np.array([0.5, -1.0]); y = np.array([1.0, 1.0]); yh = np.array([0.0, 0.0])
    c1 = c2 = 1.5; r1 = np.array([0.5, 0.2]); r2 = np.array([0.8, 0.4])
    cog = c1 * r1 * (y - x); soc = c2 * r2 * (yh - x)
    vn = v + cog + soc; xn = x + vn
    print(f"  cognitivo {cog}, social {soc}, v nueva {vn}, x nueva {xn}")
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    def flecha(p, d, color, txt, off=(0.05, 0.05)):
        ax.add_patch(FancyArrowPatch(p, p + d, arrowstyle="-|>", mutation_scale=12, color=color, linewidth=1.6))
        ax.text(*(p + d / 2 + np.array(off)), txt, color=color, fontsize=8)
    ax.plot(*x, "o", color=TINTA, markersize=7); ax.text(x[0] + 0.08, x[1] + 0.1, "x (posición actual)", fontsize=8)
    ax.plot(*y, "s", color=VERDE, markersize=7); ax.text(y[0] + 0.08, y[1] - 0.25, "y: su mejor posición", fontsize=8, color=VERDE)
    ax.plot(*yh, "*", color=AZUL, markersize=12); ax.text(yh[0] + 0.1, yh[1] - 0.3, "ŷ: mejor del enjambre", fontsize=8, color=AZUL)
    flecha(x, v, GRIS, "v (inercia)", (0.08, 0))
    flecha(x + v, cog, VERDE, "cognitivo", (0.08, 0.05))
    flecha(x + v + cog, soc, AZUL, "social", (-0.9, -0.1))
    flecha(x, vn, NARANJA, "v nueva", (-0.6, 0.1))
    ax.plot(*xn, "o", color=NARANJA, markersize=7, markerfacecolor="white")
    ax.text(xn[0] - 0.2, xn[1] - 0.35, f"x nueva = ({xn[0]:.2f}, {xn[1]:.2f})", fontsize=8, color=NARANJA)
    ax.set_xlim(-0.6, 3.2); ax.set_ylim(-0.8, 3.5); ax.set_aspect("equal")
    ax.set_title("v(t+1) = v + c₁r₁(y − x) + c₂r₂(ŷ − x)")
    guardar(fig, "p1-velocidad.png")
    return cog, soc, vn, xn


def figura_explosion():
    titulo("PSO de la clase (w = 1) contra inercia y velocidad máxima")
    fig, (ea, eb) = plt.subplots(1, 2, figsize=(10, 3.2))
    casos = [("w = 1, sin límite (el de la clase)", dict(w=1.0), ROJO),
             ("w = 1, |v| ≤ 1", dict(w=1.0, vmax=1.0), NARANJA),
             ("w = 0,7", dict(w=0.7), AZUL)]
    for nombre, kw, color in casos:
        hs, vs = [], []
        for s in range(20):
            h, v, _, _ = pso(esfera, 2, 20, 150, np.random.default_rng(400 + s), **kw)
            hs.append(h); vs.append(v)
        ea.semilogy(np.median(vs, axis=0), color=color, label=nombre)
        eb.semilogy(np.median(hs, axis=0), color=color, label=nombre)
        print(f"  {nombre}: |v| media en la iteración 150 = {np.median(vs, axis=0)[-1]:.3g}; mejor f = {np.median(np.array(hs)[:, -1]):.3g}")
    ea.set_xlabel("iteración"); ea.set_ylabel("|v| media"); ea.legend(fontsize=7); ea.set_title("Velocidad de las partículas")
    eb.set_xlabel("iteración"); eb.set_ylabel("mejor f"); eb.set_title("Esfera 2D: mejor f encontrado")
    guardar(fig, "p2-explosion.png")


def figura_gbest_lbest():
    titulo("Mejor global contra mejor local")
    fig = plt.figure(figsize=(11, 6.4))
    xs = np.linspace(-5.12, 5.12, 300); XX, YY = np.meshgrid(xs, xs)
    Z = rastrigin(np.column_stack([XX.ravel(), YY.ravel()])).reshape(XX.shape)
    for fila, (top, color) in enumerate([("global", AZUL), ("local", VERDE)]):
        _, _, fotos, _ = pso(rastrigin, 2, 30, 80, np.random.default_rng(5), w=0.7, topologia=top, guardar_t=(0, 5, 15, 40))
        for col, t in enumerate((0, 5, 15, 40)):
            ax = fig.add_subplot(3, 4, 1 + col + 4 * fila)
            ax.imshow(Z, extent=(-5.12, 5.12, -5.12, 5.12), origin="lower", cmap="Greys", alpha=0.5)
            X, mejor = fotos[t]
            ax.plot(X[:, 0], X[:, 1], "o", color=color, markersize=3)
            ax.plot(0, 0, "+", color=ROJO, markersize=9)
            ax.set_xlim(-5.12, 5.12); ax.set_ylim(-5.12, 5.12)
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            ax.set_title(f"{'mejor global' if top == 'global' else 'mejor local (anillo, ±1)'} · t = {t}", fontsize=8)
    ea = fig.add_subplot(3, 2, 5); eb = fig.add_subplot(3, 2, 6)
    for top, color in [("global", AZUL), ("local", VERDE)]:
        hs, ds = [], []
        for s in range(30):
            g = np.random.default_rng(500 + s)
            h, _, _, _ = pso(rastrigin, 10, 30, 400, g, w=0.7, topologia=top)
            hs.append(h)
        # dispersión: se repite guardando posiciones cada iteración
        for s in range(10):
            g = np.random.default_rng(700 + s)
            _, _, fotos, _ = pso(rastrigin, 10, 30, 150, g, w=0.7, topologia=top, guardar_t=tuple(range(150)))
            ds.append([np.mean(np.linalg.norm(fotos[t][0] - fotos[t][0].mean(0), axis=1)) for t in range(150)])
        hs = np.array(hs)
        ea.semilogy(np.median(hs, axis=0), color=color, label=f"mejor {top}")
        eb.semilogy(np.median(ds, axis=0), color=color, label=f"mejor {top}")
        q = np.percentile(hs[:, -1], [25, 50, 75])
        print(f"  Rastrigin 10D, {top}: mejor f a las 50 iteraciones (mediana) {np.median(hs[:, 49]):.1f}; final cuartiles {np.round(q, 2)}")
        print(f"     dispersión media a t=20: {np.median(ds, axis=0)[20]:.3f}; a t=60: {np.median(ds, axis=0)[60]:.4f}")
    ea.set_xlabel("iteración"); ea.set_ylabel("mejor f (mediana de 30)"); ea.legend(fontsize=8)
    ea.set_title("Rastrigin 10D: mejor f", fontsize=9)
    eb.set_xlabel("iteración"); eb.set_ylabel("distancia media al centro"); eb.legend(fontsize=8)
    eb.set_title("Rastrigin 10D: qué tan desparramado está el enjambre", fontsize=9)
    guardar(fig, "p3-global-local.png")


# ===========================================================================
# Esquemas para dibujar en el pizarrón
# ===========================================================================


def esquema_puente():
    """Las dos mesas y el puente de dos ramas, visto desde arriba."""
    fig, ax = plt.subplots(figsize=(7, 2.6))
    apagar(ax); ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), 2, 3, color=GRIS_CLARO)); ax.text(1, 1.5, "hormiguero", ha="center", va="center", fontsize=10)
    ax.add_patch(Rectangle((8, 0), 2, 3, color=GRIS_CLARO)); ax.text(9, 1.5, "comida", ha="center", va="center", fontsize=10)
    # bifurcaciones
    ax.plot([2, 3], [1.5, 1.5], color=TINTA, linewidth=6, solid_capstyle="butt")
    ax.plot([7, 8], [1.5, 1.5], color=TINTA, linewidth=6, solid_capstyle="butt")
    t = np.linspace(0, 1, 100)
    ax.plot(3 + 4 * t, 1.5 + 1.4 * np.sin(np.pi * t) ** 0.6, color=ROJO, linewidth=6)          # larga
    ax.plot([3, 4, 6, 7], [1.5, 0.9, 0.9, 1.5], color=VERDE, linewidth=6)                         # corta
    ax.text(5, 3.05, "rama larga", ha="center", color=ROJO, fontsize=10)
    ax.text(5, 0.45, "rama corta", ha="center", color=VERDE, fontsize=10)
    ax.plot(3, 1.5, "o", color=TINTA, markersize=8); ax.text(3, 1.95, "bifurcación", ha="center", fontsize=8)
    ax.set_xlim(-0.2, 10.2); ax.set_ylim(0, 3.5)
    guardar(fig, "h0-puente-esquema.png")


def esquema_topologias():
    """Estrella (todas con todas) y anillo por índices, con 6 partículas."""
    fig, (ea, eb) = plt.subplots(1, 2, figsize=(8, 3.6))
    ang = np.pi / 2 - 2 * np.pi * np.arange(6) / 6
    P = np.column_stack([np.cos(ang), np.sin(ang)])
    for ax, titulo_, pares, color in [
            (ea, "Estrella (mejor global): cada una ve a todas", list(itertools.combinations(range(6), 2)), AZUL),
            (eb, "Anillo (mejor local, n = 1): vecinas por índice", [(k, (k + 1) % 6) for k in range(6)], VERDE)]:
        apagar(ax); ax.set_aspect("equal")
        for a, b in pares:
            ax.plot(*zip(P[a], P[b]), color=color, linewidth=1.5, alpha=0.8)
        for k, (x, y) in enumerate(P):
            ax.add_patch(Circle((x, y), 0.16, color="white", ec=TINTA, zorder=3))
            ax.text(x, y, str(k + 1), ha="center", va="center", fontsize=10, zorder=4)
        ax.set_title(titulo_, fontsize=9); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    eb.annotate("entorno de la 1:\n{6, 1, 2}", xy=P[0], xytext=(0.55, 1.05), fontsize=8, color=VERDE)
    guardar(fig, "p0-topologias.png")


if __name__ == "__main__":
    import sys
    todas = ["figura_es", "figura_mu_lambda", "verificar_siete_bits", "figura_pg", "figura_puente",
             "ejemplo_probabilidades", "figura_aco_cuadricula", "figura_evaporacion", "figura_as_viajante",
             "ejemplo_velocidad", "figura_explosion", "figura_gbest_lbest",
             "esquema_puente", "esquema_topologias"]
    for nombre in (sys.argv[1:] or todas):
        globals()[nombre]()
