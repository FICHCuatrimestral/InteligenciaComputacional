"""Figuras y verificaciones del apunte de introduccion al aprendizaje profundo.

Genera todos los PNG que referencia ../Resumenes/01-aprendizaje-profundo.md e
imprime por consola todas las verificaciones numericas que cita el apunte.
Los numeros del apunte salen de esta corrida.

    python3 graficos_profundo.py

Requiere numpy y matplotlib. sympy es opcional: sin sympy se saltea la figura
de la explosion de expresiones.
"""

import math
import os

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


def titulo_verificacion(texto):
    print()
    print("=" * 72)
    print(texto)
    print("=" * 72)


# ===========================================================================
# Un motor de derivacion automatica en modo reverso, en 60 lineas.
# Es lo que hace PyTorch por dentro (seccion 7 del apunte). Se usa para
# verificar todas las derivadas del apunte contra las formulas a mano.
# ===========================================================================


class Valor:
    """Un numero que recuerda de donde vino, para poder derivar hacia atras."""

    def __init__(self, dato, padres=(), derivadas_locales=(), operacion=""):
        self.dato = float(dato)          # el valor primal v_i
        self.grad = 0.0                  # el adjunto  v_i barra = dy/dv_i
        self.padres = padres             # de que nodos sale
        self.derivadas_locales = derivadas_locales  # dv_i/dv_padre
        self.operacion = operacion

    # --- primitivas: cada una sabe su derivada local ----------------------
    def __add__(self, otro):
        otro = otro if isinstance(otro, Valor) else Valor(otro)
        return Valor(self.dato + otro.dato, (self, otro), (1.0, 1.0), "+")

    __radd__ = __add__

    def __neg__(self):
        return Valor(-self.dato, (self,), (-1.0,), "neg")

    def __sub__(self, otro):
        return self + (-(otro if isinstance(otro, Valor) else Valor(otro)))

    def __rsub__(self, otro):
        return Valor(otro) - self

    def __mul__(self, otro):
        otro = otro if isinstance(otro, Valor) else Valor(otro)
        return Valor(self.dato * otro.dato, (self, otro), (otro.dato, self.dato), "*")

    __rmul__ = __mul__

    def __truediv__(self, otro):
        otro = otro if isinstance(otro, Valor) else Valor(otro)
        return self * otro ** -1

    def __rtruediv__(self, otro):
        return Valor(otro) * self ** -1

    def __pow__(self, exponente):
        return Valor(self.dato ** exponente, (self,),
                     (exponente * self.dato ** (exponente - 1),), "pow")

    def log(self):
        return Valor(math.log(self.dato), (self,), (1.0 / self.dato,), "log")

    def exp(self):
        e = math.exp(self.dato)
        return Valor(e, (self,), (e,), "exp")

    def sin(self):
        return Valor(math.sin(self.dato), (self,), (math.cos(self.dato),), "sin")

    # --- la pasada hacia atras --------------------------------------------
    def backward(self):
        orden, visitados = [], set()

        def recorrer(nodo):
            if id(nodo) in visitados:
                return
            visitados.add(id(nodo))
            for padre in nodo.padres:
                recorrer(padre)
            orden.append(nodo)

        recorrer(self)
        self.grad = 1.0                                  # y barra = dy/dy = 1
        for nodo in reversed(orden):                     # de la salida a la entrada
            for padre, local in zip(nodo.padres, nodo.derivadas_locales):
                padre.grad += nodo.grad * local          # regla de la cadena, ACUMULANDO


def sigmoide(v):
    return 1.0 / (1.0 + (-v).exp()) if isinstance(v, Valor) else 1.0 / (1.0 + math.exp(-v))


# ===========================================================================
# Verificaciones
# ===========================================================================


def verificar_mapa_logistico():
    titulo_verificacion("Mapa logistico: derivada manual, simbolica, numerica y automatica")

    def f(x):
        v = x
        for _ in [1, 2, 3]:
            v = 4 * v * (1 - v)
        return v

    def f_cerrada(x):
        return 64 * x * (1 - x) * (1 - 2 * x) ** 2 * (1 - 8 * x + 8 * x * x) ** 2

    def fp_manual(x):
        return (128 * x * (1 - x) * (-8 + 16 * x) * (1 - 2 * x) ** 2 * (1 - 8 * x + 8 * x * x)
                + 64 * (1 - x) * (1 - 2 * x) ** 2 * (1 - 8 * x + 8 * x * x) ** 2
                - 64 * x * (1 - 2 * x) ** 2 * (1 - 8 * x + 8 * x * x) ** 2
                - 256 * x * (1 - x) * (1 - 2 * x) * (1 - 8 * x + 8 * x * x) ** 2)

    def fp_simplificada(x):
        return 64 * (1 - 42 * x + 504 * x**2 - 2640 * x**3 + 7040 * x**4
                     - 9984 * x**5 + 7168 * x**6 - 2048 * x**7)

    def fp_automatica(x):
        v, dv = x, 1.0
        for _ in [1, 2, 3]:
            v, dv = 4 * v * (1 - v), 4 * dv - 8 * v * dv
        return v, dv

    def fp_numerica(x, h=0.000001):
        return (f(x + h) - f(x)) / h

    for x0 in [0.1, 0.3, 0.7]:
        _, auto = fp_automatica(x0)
        print(f"x={x0}: f={f(x0):.10f} (cerrada {f_cerrada(x0):.10f})  "
              f"manual={fp_manual(x0):.10f}  simplif={fp_simplificada(x0):.10f}  "
              f"auto={auto:.10f}  numerica={fp_numerica(x0):.10f}  "
              f"err num={abs(fp_numerica(x0) - auto):.2e}")

    # tabla de la iteracion 1 a 3 con x = 0,3 para el paso a paso del apunte
    x0 = 0.3
    v, dv = x0, 1.0
    print(f"  n=1: l={v:.6f} dl/dx={dv:.6f}")
    for n in [2, 3, 4]:
        v, dv = 4 * v * (1 - v), 4 * dv - 8 * v * dv
        print(f"  n={n}: l={v:.6f} dl/dx={dv:.6f}")
    return fp_automatica, f


def verificar_grafo_baydin():
    titulo_verificacion("f(x1,x2) = ln x1 + x1 x2 - sin x2 en (2,5): modo directo y reverso")
    x1, x2 = 2.0, 5.0
    v_1, v0 = x1, x2
    v1 = math.log(v_1)
    v2 = v_1 * v0
    v3 = math.sin(v0)
    v4 = v1 + v2
    v5 = v4 - v3
    print(f"primales: v1={v1:.4f} v2={v2:.4f} v3={v3:.4f} v4={v4:.4f} v5={v5:.4f}")

    # directo con x1 punto = 1
    d_1, d0 = 1.0, 0.0
    d1 = d_1 / v_1
    d2 = d_1 * v0 + d0 * v_1
    d3 = d0 * math.cos(v0)
    d4 = d1 + d2
    d5 = d4 - d3
    print(f"directo (x1'=1): v1'={d1} v2'={d2} v3'={d3} v4'={d4} v5'={d5}")
    # directo con x2 punto = 1 (la segunda pasada que hace falta)
    d_1, d0 = 0.0, 1.0
    e5 = (d_1 / v_1 + d_1 * v0 + d0 * v_1) - d0 * math.cos(v0)
    print(f"directo (x2'=1): dy/dx2={e5:.6f}")

    # reverso, a mano
    b5 = 1.0
    b4 = b5 * 1
    b3 = b5 * -1
    b1 = b4 * 1
    b2 = b4 * 1
    b0 = b3 * math.cos(v0)
    b_1 = b2 * v0
    b0 = b0 + b2 * v_1
    b_1 = b_1 + b1 / v_1
    print(f"reverso: v3b={b3} v0b(parcial)={b3 * math.cos(v0):.6f} v0b={b0:.6f} v-1b={b_1}")

    # con el motor Valor
    a, b = Valor(2.0), Valor(5.0)
    y = a.log() + a * b - b.sin()
    y.backward()
    print(f"motor Valor: y={y.dato:.6f}  dy/dx1={a.grad:.6f}  dy/dx2={b.grad:.6f}")
    h = 1e-6
    ff = lambda p, q: math.log(p) + p * q - math.sin(q)
    print(f"numerica centrada: {(ff(2 + h, 5) - ff(2 - h, 5)) / 2 / h:.6f} "
          f"{(ff(2, 5 + h) - ff(2, 5 - h)) / 2 / h:.6f}")
    return dict(v_1=v_1, v0=v0, v1=v1, v2=v2, v3=v3, v4=v4, v5=v5)


def verificar_neurona():
    titulo_verificacion("Una neurona sigmoidea: gradiente a mano vs automatico (MSE y entropia cruzada)")
    w0 = [0.0, 0.5, 0.5]
    x = [-1.0, 0.8, -0.3]
    yd = 1.0
    mu = 0.1

    # a mano
    v = sum(wi * xi for wi, xi in zip(w0, x))
    y = sigmoide(v)
    grad_mse_mano = [-2 * (yd - y) * y * (1 - y) * xi for xi in x]
    grad_ce_mano = [(y - yd) * xi for xi in x]
    print(f"v={v:.6f} y={y:.6f}")
    print("grad MSE a mano   :", [f"{g:.6f}" for g in grad_mse_mano])

    w = [Valor(wi) for wi in w0]
    vv = sum((wi * xi for wi, xi in zip(w, x)), Valor(0.0))
    yy = sigmoide(vv)
    e2 = (yd - yy) ** 2
    e2.backward()
    print("grad MSE automat. :", [f"{wi.grad:.6f}" for wi in w])
    nuevo = [wi - mu * g for wi, g in zip(w0, grad_mse_mano)]
    print("w(n+1) MSE        :", [f"{n:.6f}" for n in nuevo])

    w = [Valor(wi) for wi in w0]
    vv = sum((wi * xi for wi, xi in zip(w, x)), Valor(0.0))
    yy = sigmoide(vv)
    ce = -(yd * yy.log() + (1 - yd) * (1 - yy).log())
    ce.backward()
    print("grad CE a mano    :", [f"{g:.6f}" for g in grad_ce_mano])
    print("grad CE automat.  :", [f"{wi.grad:.6f}" for wi in w])
    print(f"cociente |grad CE| / |grad MSE| en la 1ra componente: "
          f"{abs(grad_ce_mano[0]) / abs(grad_mse_mano[0]):.3f}  (= 1/(2 y(1-y)) = {1 / (2 * y * (1 - y)):.3f})")

    # neurona saturada: y cerca de 0 con yd = 1
    vs = -6.0
    ys = sigmoide(vs)
    print(f"saturada v=-6: y={ys:.5f}  factor MSE 2(yd-y)y(1-y)={2 * (1 - ys) * ys * (1 - ys):.5f}  "
          f"factor CE (y-yd)={ys - 1:.5f}")

    # dos pasos de entrenamiento con cada criterio, para el ejemplo del apunte
    return v, y


def verificar_swish():
    titulo_verificacion("Lamina 147: derivada de phi(v) = v / (1 + e^-v)")
    for v in [-2.0, 0.7, 3.0]:
        s = sigmoide(v)
        y = v * s
        h = 1e-6
        numerica = ((v + h) * sigmoide(v + h) - (v - h) * sigmoide(v - h)) / (2 * h)
        lamina_intermedia = (1 + math.exp(-v) + v * (1 + math.exp(-v))) / (1 + math.exp(-v)) ** 2
        lamina_final = y * (1 + v * (1 - y))
        correcta = (1 + math.exp(-v) + v * math.exp(-v)) / (1 + math.exp(-v)) ** 2
        forma_sigma = s * (1 + v * (1 - s))
        forma_y = y + s * (1 - y)
        vv = Valor(v)
        yy = vv * sigmoide(vv)
        yy.backward()
        print(f"v={v:+.1f}: numerica={numerica:.6f} automatica={vv.grad:.6f} | "
              f"correcta={correcta:.6f} sigma(1+v(1-sigma))={forma_sigma:.6f} y+sigma(1-y)={forma_y:.6f} | "
              f"LAMINA intermedia={lamina_intermedia:.6f} final={lamina_final:.6f}")


def verificar_mlp():
    titulo_verificacion("Perceptron multicapa 2-1-1 (lamina 151): retropropagacion a mano vs automatica")
    x = [-1.0, 0.8, -0.3]
    yd = 1.0
    w1 = [0.0, 0.5, 0.5]
    w2 = [0.0, 0.5]
    # a mano, con delta
    v1 = sum(a * b for a, b in zip(w1, x))
    y1 = sigmoide(v1)
    ye = [-1.0, y1]
    v = sum(a * b for a, b in zip(w2, ye))
    y = sigmoide(v)
    delta2 = (yd - y) * y * (1 - y)                     # sin el 2: se lo pone afuera
    delta1 = delta2 * w2[1] * y1 * (1 - y1)
    g2 = [-2 * delta2 * e for e in ye]
    g1 = [-2 * delta1 * e for e in x]
    # automatico
    W1 = [Valor(a) for a in w1]
    W2 = [Valor(a) for a in w2]
    V1 = sum((a * b for a, b in zip(W1, x)), Valor(0.0))
    Y1 = sigmoide(V1)
    V = W2[0] * -1.0 + W2[1] * Y1
    Y = sigmoide(V)
    E = (yd - Y) ** 2
    E.backward()
    print("capa 2 a mano:", [f"{g:.6f}" for g in g2], " auto:", [f"{a.grad:.6f}" for a in W2])
    print("capa 1 a mano:", [f"{g:.6f}" for g in g1], " auto:", [f"{a.grad:.6f}" for a in W1])


def verificar_relu_con_if():
    titulo_verificacion("Derivar a traves de un if (laminas 161 a 166)")
    for v0 in [1.5, -1.5]:
        v = Valor(v0)
        salida = v if v.dato > 0 else v / 4          # 'ReLU con fuga' de la lamina 163
        salida.backward()
        print(f"v={v0:+}: salida={salida.dato:+.3f}  derivada={v.grad}")
    for v0 in [1.5, -1.5]:
        v = Valor(v0)
        salida = sigmoide(v) if v.dato > 0 else v / 4  # la de la lamina 165
        salida.backward()
        s = sigmoide(v0)
        print(f"v={v0:+}: lamina 165 derivada={v.grad:.6f} (esperada {s * (1 - s) if v0 > 0 else 0.25:.6f})")
    print("lamina 165 en v=0: por izquierda vale 0/4 = 0, por derecha sigma(0) = 0.5 -> discontinua")


# ===========================================================================
# Figuras
# ===========================================================================


def figura_01_mapa_logistico():
    figura = plt.figure(figsize=(11.0, 5.2))
    rejilla = figura.add_gridspec(2, 3, width_ratios=[1, 1, 1.35], wspace=0.28, hspace=0.45)
    casos = [(2.8, "punto fijo"), (3.1, "ciclo de 2"), (3.5, "ciclo de 4"), (3.9, "caos")]
    for k, (r, rotulo) in enumerate(casos):
        ejes = figura.add_subplot(rejilla[k // 2, k % 2])
        l = np.empty(100)
        l[0] = 0.2
        for n in range(99):
            l[n + 1] = r * l[n] * (1 - l[n])
        ejes.plot(np.arange(1, 101), l, "-", color=AZUL, lw=0.9)
        ejes.plot(np.arange(1, 101), l, ".", color=AZUL, ms=2.5)
        ejes.set_ylim(0, 1.02)
        ejes.set_title(f"$r = {r}$ — {rotulo}")
        ejes.set_xlabel("$n$")
        if k % 2 == 0:
            ejes.set_ylabel(r"$\ell_n$")

    ejes = figura.add_subplot(rejilla[:, 2])
    valores_r = np.linspace(2.5, 4.0, 1600)
    l = np.full_like(valores_r, 0.2)
    for _ in range(600):
        l = valores_r * l * (1 - l)
    for _ in range(160):
        l = valores_r * l * (1 - l)
        ejes.plot(valores_r, l, ",", color=AZUL, alpha=0.35)
    for r, _ in casos:
        ejes.axvline(r, color=NARANJA, lw=0.8, ls="--")
    ejes.set_xlabel("$r$")
    ejes.set_ylabel(r"$\ell_n$ a largo plazo")
    ejes.set_title("Diagrama de bifurcación")
    ejes.set_xlim(2.5, 4.0)
    ejes.set_ylim(0, 1)
    guardar(figura, "01-mapa-logistico.png")


def figura_02_cuatro_formas():
    figura, ejes = plt.subplots(figsize=(11.0, 6.4))
    apagar_ejes(ejes)
    ejes.set_xlim(0, 10)
    ejes.set_ylim(0, 7.2)

    def caja(x, y, ancho, alto, texto, color_fondo="white", tam=7.6, borde=TINTA):
        ejes.add_patch(FancyBboxPatch((x, y), ancho, alto, boxstyle="round,pad=0.02,rounding_size=0.06",
                                      fc=color_fondo, ec=borde, lw=1.0))
        ejes.text(x + 0.12, y + alto - 0.12, texto, ha="left", va="top", family="monospace",
                  fontsize=tam, color=TINTA, linespacing=1.25)

    def flecha(x0, y0, x1, y1, rotulo="", dx=0.0, dy=0.0, color=TINTA):
        ejes.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=11,
                                       lw=1.1, color=color))
        if rotulo:
            ejes.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, rotulo, ha="center", va="center",
                      fontsize=8.2, color=color, style="italic",
                      bbox=dict(fc="white", ec="none", pad=1.0))

    caja(0.2, 5.75, 3.9, 1.3,
         "l1 = x\nl(n+1) = 4 l(n) (1 - l(n))\n\nf(x) = l4 = 64x(1-x)(1-2x)^2\n            (1-8x+8x^2)^2", tam=7.4)
    caja(5.9, 5.75, 3.9, 1.3,
         "f'(x) = 128x(1-x)(-8+16x)(1-2x)^2\n (1-8x+8x^2) + 64(1-x)(1-2x)^2\n (1-8x+8x^2)^2 - 64x(1-2x)^2\n (1-8x+8x^2)^2 - 256x(1-x)(1-2x)\n (1-8x+8x^2)^2",
         color_fondo="#eeeeee", tam=6.6)
    caja(0.2, 3.05, 3.9, 2.05,
         "def f(x):\n    v = x\n    for i in [1,2,3]:\n        v = 4*v*(1-v)\n    return v\n\n# o en forma cerrada:\n# return 64*x*(1-x)*...", tam=7.4)
    caja(5.9, 3.05, 3.9, 2.05,
         "def fp(x):\n    return 128*x*(1-x)*(-8+16*x)\n      *((1-2*x)**2)*(1-8*x+8*x*x)\n      +64*(1-x)*((1-2*x)**2)*...\n      -64*x*((1-2*x)**2)*...\n      -256*x*(1-x)*(1-2*x)*...\n\n          fp(x0) = f'(x0)  EXACTO",
         color_fondo="#eeeeee", tam=6.9)
    caja(0.2, 0.2, 3.9, 2.0,
         "def fp(x):\n    (v,dv) = (x,1)\n    for i in [1,2,3]:\n        (v,dv) = (4*v*(1-v),\n                  4*dv-8*v*dv)\n    return (v,dv)\n\n      fp(x0) = f'(x0)  EXACTO",
         color_fondo="#e3f4ec", borde=VERDE, tam=7.2)
    caja(5.9, 0.2, 3.9, 2.0,
         "def fp_n(x):\n    h = 0.000001\n    return (f(x+h)-f(x))/h\n\n\n\n      fp(x0) ~ f'(x0)  APROXIMADO",
         color_fondo="#fbe9e0", borde=NARANJA, tam=7.2)

    flecha(4.15, 6.4, 5.85, 6.4, "derivada manual", dy=0.2)
    flecha(2.15, 5.7, 2.15, 5.15, "codificación", dx=0.8)
    flecha(7.85, 5.7, 7.85, 5.15, "codificación", dx=0.8)
    flecha(4.15, 4.3, 5.85, 4.8, "derivada simbólica", dy=0.28)
    flecha(2.15, 3.0, 2.15, 2.25, "diferenciación automática", dx=1.25, color=VERDE)
    flecha(4.15, 3.3, 5.85, 1.9, "diferenciación numérica", dx=0.35, dy=0.3, color=NARANJA)
    guardar(figura, "02-cuatro-formas.png")


def figura_03_explosion_y_error(fp_automatica, f):
    figura, (ejes_a, ejes_b) = plt.subplots(1, 2, figsize=(11.0, 4.1))
    print()
    print("Explosion de expresiones (conteo de operaciones):")
    try:
        import sympy as sp
        x = sp.symbols("x")
        l = x
        n_valores, ingenua, simplificada, automatica = [], [], [], []
        for n in range(1, 7):
            d = sp.diff(l, x)
            n_valores.append(n)
            ingenua.append(sp.count_ops(d))
            simplificada.append(sp.count_ops(sp.expand(d)))
            automatica.append(7 * (n - 1))
            print(f"  n={n}: simbolica sin simplificar={ingenua[-1]} ops, "
                  f"expandida={simplificada[-1]} ops, automatica={automatica[-1]} ops")
            l = 4 * l * (1 - l)
        n_valores, ingenua, simplificada, automatica = (n_valores[1:], ingenua[1:],
                                                         simplificada[1:], automatica[1:])
        ejes_a.semilogy(n_valores, ingenua, "o-", color=ROJO, label="simbólica, sin simplificar")
        ejes_a.semilogy(n_valores, simplificada, "s-", color=NARANJA, label="simbólica, expandida")
        ejes_a.semilogy(n_valores, [max(a, 1) for a in automatica], "^-", color=VERDE,
                        label="automática (7 ops por iteración)")
        ejes_a.set_xticks(n_valores)
        ejes_a.set_xlabel(r"$n$ (derivada de $\ell_n$)")
        ejes_a.set_ylabel("operaciones de la expresión")
        ejes_a.set_title("Explosión de expresiones")
        ejes_a.legend(fontsize=8)
    except ImportError:
        ejes_a.text(0.5, 0.5, "instalar sympy", ha="center")

    x0 = 0.3
    _, exacta = fp_automatica(x0)
    pasos = np.logspace(-16, -1, 61)
    errores_adelante = [abs((f(x0 + h) - f(x0)) / h - exacta) for h in pasos]
    errores_centrada = [abs((f(x0 + h) - f(x0 - h)) / (2 * h) - exacta) for h in pasos]
    ejes_b.loglog(pasos, errores_adelante, "-", color=NARANJA, label=r"$(f(x+h)-f(x))/h$")
    ejes_b.loglog(pasos, errores_centrada, "-", color=ROJO, lw=0.9, alpha=0.8,
                  label=r"$(f(x+h)-f(x-h))/2h$")
    ejes_b.axhline(max(abs(fp_automatica(x0)[1] - exacta), 1e-16), color=VERDE, lw=1.5,
                   label="automática (error = 0)")
    ejes_b.axvline(1e-6, color=GRIS, ls="--", lw=0.8)
    ejes_b.text(1.4e-6, 1e-13, "$h = 10^{-6}$\n(el de la lámina)", fontsize=7.5, color=GRIS)
    ejes_b.set_xlabel("$h$")
    ejes_b.set_ylabel(r"$|f'_{num}(0{,}3) - f'(0{,}3)|$")
    ejes_b.set_title("Error de la diferenciación numérica")
    ejes_b.set_ylim(1e-17, 1e3)
    ejes_b.legend(fontsize=7.5, loc="lower left", bbox_to_anchor=(0.0, 0.1))
    guardar(figura, "03-explosion-y-error-numerico.png")

    mejor = int(np.argmin(errores_adelante))
    mejor_c = int(np.argmin(errores_centrada))
    err_lamina = abs((f(x0 + 1e-6) - f(x0)) / 1e-6 - exacta)
    err_chico = abs((f(x0 + 1e-13) - f(x0)) / 1e-13 - exacta)
    print(f"  error numerico hacia adelante: h=1e-6 -> {err_lamina:.2e};  h=1e-13 -> {err_chico:.2e};  "
          f"mejor h={pasos[mejor]:.1e} -> {errores_adelante[mejor]:.2e}; "
          f"centrada mejor h={pasos[mejor_c]:.1e} -> {errores_centrada[mejor_c]:.2e}")


POSICIONES_GRAFO = {
    "x1": (0.0, 2.0), "x2": (0.0, 0.0),
    "v-1": (1.3, 2.0), "v0": (1.3, 0.0),
    "v1": (2.9, 2.0), "v2": (2.9, 1.0), "v3": (4.5, 0.0),
    "v4": (4.5, 2.0), "v5": (6.1, 1.0), "y": (7.5, 1.0),
}
ARISTAS_GRAFO = [
    ("x1", "v-1", ""), ("x2", "v0", ""),
    ("v-1", "v1", "ln"), ("v-1", "v2", "×"), ("v0", "v2", "×"), ("v0", "v3", "sin"),
    ("v1", "v4", "+"), ("v2", "v4", "+"), ("v4", "v5", "−"), ("v3", "v5", "−"),
    ("v5", "y", ""),
]
NOMBRES = {"v-1": r"$v_{-1}$", "v0": r"$v_0$", "v1": r"$v_1$", "v2": r"$v_2$", "v3": r"$v_3$",
           "v4": r"$v_4$", "v5": r"$v_5$", "x1": r"$x_1$", "x2": r"$x_2$", "y": r"$y$"}


def dibujar_grafo(ejes, anotaciones=None, color_aristas=TINTA, invertir=False, derivadas=None,
                  color_derivadas=VERDE):
    apagar_ejes(ejes)
    ejes.set_xlim(-0.5, 8.1)
    ejes.set_ylim(-0.9, 2.9)
    for a, b, rotulo in ARISTAS_GRAFO:
        (xa, ya), (xb, yb) = POSICIONES_GRAFO[a], POSICIONES_GRAFO[b]
        if invertir:
            (xa, ya), (xb, yb) = (xb, yb), (xa, ya)
        ejes.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=10,
                                       lw=1.0, color=color_aristas, shrinkA=13, shrinkB=13))
        if derivadas and (a, b) in derivadas:
            xm, ym = (xa + xb) / 2, (ya + yb) / 2
            ejes.text(xm, ym + 0.17, derivadas[(a, b)], ha="center", va="bottom", fontsize=7.2,
                      color=color_derivadas, bbox=dict(fc="white", ec="none", pad=0.4))
    for nodo, (x, y) in POSICIONES_GRAFO.items():
        if nodo in ("x1", "x2", "y"):
            ejes.text(x, y, NOMBRES[nodo], ha="center", va="center", fontsize=10)
            continue
        ejes.add_patch(plt.Circle((x, y), 0.25, fc="white", ec=TINTA, lw=1.1, zorder=3))
        ejes.text(x, y, NOMBRES[nodo], ha="center", va="center", fontsize=9, zorder=4)
        if anotaciones and nodo in anotaciones:
            texto, color = anotaciones[nodo]
            ejes.text(x, y - 0.36, texto, ha="center", va="top", fontsize=7.4, color=color,
                      linespacing=1.15)


def figura_04_grafo(valores):
    figura, ejes = plt.subplots(figsize=(9.0, 3.5))
    anot = {
        "v-1": ("= 2", AZUL), "v0": ("= 5", AZUL), "v1": ("ln 2 = 0,693", AZUL),
        "v2": ("2·5 = 10", AZUL), "v3": ("sin 5 = −0,959", AZUL),
        "v4": ("10,693", AZUL), "v5": ("11,652", AZUL),
    }
    derivadas = {("v-1", "v1"): r"$1/v_{-1}$", ("v-1", "v2"): r"$v_0$", ("v0", "v2"): r"$v_{-1}$",
                 ("v0", "v3"): r"$\cos v_0$", ("v1", "v4"): "1", ("v2", "v4"): "1",
                 ("v4", "v5"): "1", ("v3", "v5"): "−1"}
    dibujar_grafo(ejes, anot, derivadas=derivadas, color_derivadas=ROJO)
    ejes.set_title(r"$f(x_1,x_2) = \ln x_1 + x_1x_2 - \sin x_2$ en $(2,5)$: valores (azul) y "
                   r"derivada local de cada arista (rojo)")
    guardar(figura, "04-grafo-de-primitivas.png")


def figura_05_directo_reverso():
    figura, (ejes_d, ejes_r) = plt.subplots(2, 1, figsize=(9.0, 7.0))
    anot_d = {
        "v-1": (r"$\dot v_{-1}=1$", VERDE), "v0": (r"$\dot v_0=0$", VERDE),
        "v1": (r"$1/2 = 0{,}5$", VERDE), "v2": (r"$1\cdot5+0\cdot2=5$", VERDE),
        "v3": (r"$0\cdot\cos5=0$", VERDE), "v4": (r"$0{,}5+5=5{,}5$", VERDE),
        "v5": (r"$5{,}5-0=\mathbf{5{,}5}$", VERDE),
    }
    dibujar_grafo(ejes_d, anot_d, color_aristas=VERDE)
    ejes_d.set_title(r"Modo directo: se siembra $\dot x_1 = 1$ y las tangentes "
                     r"$\dot v_i = \partial v_i/\partial x_1$ viajan con los valores "
                     r"$\Rightarrow\ \partial y/\partial x_1$", fontsize=9.5)
    anot_r = {
        "v5": (r"$\bar v_5=1$", ROJO), "v4": (r"$\bar v_4=1$", ROJO), "v3": (r"$\bar v_3=-1$", ROJO),
        "v1": (r"$\bar v_1=1$", ROJO), "v2": (r"$\bar v_2=1$", ROJO),
        "v0": (r"$-\cos5 + 1\cdot2$" "\n" r"$=\mathbf{1{,}716}$", ROJO),
        "v-1": (r"$1\cdot5 + 1/2$" "\n" r"$=\mathbf{5{,}5}$", ROJO),
    }
    dibujar_grafo(ejes_r, anot_r, color_aristas=ROJO, invertir=True)
    ejes_r.set_title(r"Modo reverso: se siembra $\bar y = 1$ y los adjuntos "
                     r"$\bar v_i = \partial y/\partial v_i$ vuelven $\Rightarrow$ "
                     r"$\partial y/\partial x_1$ y $\partial y/\partial x_2$ juntas", fontsize=9.5)
    guardar(figura, "05-modo-directo-y-reverso.png")


def figura_06_jacobiano():
    figura, (ejes_d, ejes_r) = plt.subplots(1, 2, figsize=(10.0, 3.6))
    n, m = 7, 3
    for ejes, modo in ((ejes_d, "directo"), (ejes_r, "reverso")):
        apagar_ejes(ejes)
        ejes.set_xlim(-0.5, n + 3.2)
        ejes.set_ylim(-1.3, m + 0.9)
        ejes.set_aspect("equal")
        for i in range(m):
            for j in range(n):
                resaltada = (modo == "directo" and j == 2) or (modo == "reverso" and i == 1)
                ejes.add_patch(plt.Rectangle((j, m - 1 - i), 0.92, 0.92,
                                             fc=(VERDE if modo == "directo" else ROJO) if resaltada else "#eeeeee",
                                             ec="white"))
        ejes.text(n / 2, m + 0.45, r"$J = \partial \mathbf{y}/\partial \mathbf{x}$  ($m \times n$)",
                  ha="center", fontsize=9)
        ejes.text(-0.35, m / 2, "$m$", ha="right", va="center", fontsize=10)
        ejes.text(n / 2, -0.35, "$n$ entradas", ha="center", va="top", fontsize=9)
    ejes_d.text(n + 0.3, m / 2, "1 pasada\n= 1 columna\n\n$n$ pasadas\nen total", va="center",
                fontsize=8.5, color=VERDE)
    ejes_r.text(n + 0.3, m / 2, "1 pasada\n= 1 fila\n\n$m$ pasadas\nen total", va="center",
                fontsize=8.5, color=ROJO)
    ejes_d.set_title("Modo directo", fontsize=10)
    ejes_r.set_title("Modo reverso", fontsize=10)
    figura.text(0.5, -0.04, "Entrenar una red: $n$ = millones de pesos, $m$ = 1 (el error). "
                            "Reverso: una sola pasada hacia atrás.", ha="center", fontsize=9)
    guardar(figura, "06-directo-vs-reverso.png")


def figura_07_activaciones():
    v = np.linspace(-5, 5, 801)
    s = 1 / (1 + np.exp(-v))
    funciones = [
        ("sigmoide", s, s * (1 - s), AZUL),
        ("tanh", np.tanh(v), 1 - np.tanh(v) ** 2, VERDE),
        ("ReLU", np.maximum(v, 0), (v > 0).astype(float), NARANJA),
        (r"$v$ / $v/4$ (lám. 163)", np.where(v > 0, v, v / 4), np.where(v > 0, 1.0, 0.25), GRIS),
        (r"$v\,\sigma(v)$ (lám. 145)", v * s, s * (1 + v * (1 - s)), ROJO),
    ]
    figura, (ejes_f, ejes_d) = plt.subplots(1, 2, figsize=(11.0, 4.0))
    for nombre, fv, dv, color in funciones:
        ejes_f.plot(v, fv, color=color, lw=1.5, label=nombre)
        ejes_d.plot(v, dv, color=color, lw=1.5, label=nombre)
    ejes_f.set_ylim(-1.5, 3.5)
    ejes_f.set_title(r"$\varphi(v)$")
    ejes_d.set_title(r"$\varphi'(v)$")
    ejes_d.axhline(0.25, color=AZUL, ls=":", lw=0.9)
    ejes_d.text(-4.9, 0.28, "máx. de la sigmoide = 0,25", fontsize=7.5, color=AZUL)
    ejes_d.set_ylim(-0.2, 1.3)
    for ejes in (ejes_f, ejes_d):
        ejes.set_xlabel("$v$")
    ejes_f.legend(fontsize=7.8, loc="upper left")
    guardar(figura, "07-activaciones.png")


def figura_08_swish_errata():
    v = np.linspace(-5, 5, 801)
    s = 1 / (1 + np.exp(-v))
    y = v * s
    correcta = s * (1 + v * (1 - s))
    lamina = y * (1 + v * (1 - y))
    intermedia = (1 + np.exp(-v) + v * (1 + np.exp(-v))) / (1 + np.exp(-v)) ** 2
    h = 1e-5
    numerica = ((v + h) / (1 + np.exp(-(v + h))) - (v - h) / (1 + np.exp(-(v - h)))) / (2 * h)
    figura, ejes = plt.subplots(figsize=(7.0, 3.8))
    ejes.plot(v, numerica, color=GRIS_CLARO, lw=6, label="numérica (referencia)")
    ejes.plot(v, correcta, color=VERDE, lw=1.6, label=r"$\sigma(v)\,[1+v(1-\sigma(v))]$ (correcta)")
    ejes.plot(v, lamina, color=ROJO, lw=1.4, ls="--", label=r"$y\,[1+v(1-y)]$ (lámina 147, final)")
    ejes.plot(v, intermedia, color=NARANJA, lw=1.2, ls="-.", label="lámina 147, paso intermedio")
    ejes.set_ylim(-2.5, 3.0)
    ejes.set_xlabel("$v$")
    ejes.set_title(r"Derivada de $\varphi(v) = v/(1+e^{-v})$")
    ejes.legend(fontsize=7.8, loc="upper left")
    guardar(figura, "08-errata-lamina-147.png")


def figura_09_desvanecimiento():
    titulo_verificacion("Desvanecimiento del gradiente: red de 30 capas de 50 neuronas, 10 semillas")
    capas, ancho = 30, 50
    resultados = {}
    for nombre in ("sigmoide", "tanh", "ReLU"):
        normas_por_semilla = []
        for semilla in range(10):
            rng = np.random.default_rng(semilla)
            x = rng.standard_normal(ancho)
            pesos, entradas, locales = [], [], []
            a = x
            for _ in range(capas):
                if nombre == "ReLU":
                    W = rng.standard_normal((ancho, ancho)) * np.sqrt(2.0 / ancho)
                else:
                    W = rng.standard_normal((ancho, ancho)) * np.sqrt(1.0 / ancho)
                vv = W @ a
                if nombre == "sigmoide":
                    a = 1 / (1 + np.exp(-vv))
                    d = a * (1 - a)
                elif nombre == "tanh":
                    a = np.tanh(vv)
                    d = 1 - a ** 2
                else:
                    a = np.maximum(vv, 0)
                    d = (vv > 0).astype(float)
                pesos.append(W)
                entradas.append(None)
                locales.append(d)
            # retropropagacion de un gradiente unitario desde la salida
            g = np.ones(ancho) / np.sqrt(ancho)
            normas = []
            for k in reversed(range(capas)):
                delta = g * locales[k]
                normas.append(np.linalg.norm(delta))
                g = pesos[k].T @ delta
            normas_por_semilla.append(normas[::-1])
        media = np.exp(np.mean(np.log(np.array(normas_por_semilla) + 1e-300), axis=0))
        resultados[nombre] = (media, np.array(normas_por_semilla))
        razon = media[0] / media[-1]
        print(f"{nombre:9s}: |delta| capa 30 = {media[-1]:.3e}, capa 1 = {media[0]:.3e}, "
              f"capa1/capa30 = {razon:.2e}  (min/max entre semillas de la razon: "
              f"{(np.array(normas_por_semilla)[:, 0] / np.array(normas_por_semilla)[:, -1]).min():.1e} / "
              f"{(np.array(normas_por_semilla)[:, 0] / np.array(normas_por_semilla)[:, -1]).max():.1e})")

    figura, ejes = plt.subplots(figsize=(7.4, 3.9))
    for nombre, color in (("sigmoide", AZUL), ("tanh", VERDE), ("ReLU", NARANJA)):
        media, todas = resultados[nombre]
        for fila in todas:
            ejes.semilogy(np.arange(1, capas + 1), fila, color=color, alpha=0.12, lw=0.8)
        ejes.semilogy(np.arange(1, capas + 1), media, color=color, lw=2, label=nombre)
    ejes.set_xlabel("capa (1 = la más cercana a la entrada)")
    ejes.set_ylabel(r"$\|\boldsymbol{\delta}\|$ de la capa")
    ejes.set_title("Cuánto gradiente llega a cada capa (30 capas, 10 semillas)")
    ejes.legend(fontsize=8)
    guardar(figura, "09-desvanecimiento.png")


def figura_10_neurona_como_grafo(v, y):
    figura, ejes = plt.subplots(figsize=(10.0, 3.3))
    apagar_ejes(ejes)
    ejes.set_xlim(-0.4, 10.4)
    ejes.set_ylim(-1.4, 1.2)
    nodos = [
        (0.0, 0.6, r"$\mathbf{w}$"), (0.0, -0.6, r"$\mathbf{x}$"),
        (2.2, 0.0, r"$v=\langle\mathbf{w},\mathbf{x}\rangle$"),
        (4.8, 0.0, r"$y=\varphi(v)$"), (7.4, 0.0, r"$e = y_d - y$"), (9.7, 0.0, r"$\xi = e^2$"),
    ]
    for x, yy, texto in nodos:
        ejes.text(x, yy, texto, ha="center", va="center", fontsize=10,
                  bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=TINTA, lw=1.0))
    for (x0, y0), (x1, y1) in [((0.3, 0.55), (1.35, 0.1)), ((0.3, -0.55), (1.35, -0.1)),
                               ((3.05, 0), (4.05, 0)), ((5.55, 0), (6.6, 0)), ((8.2, 0), (9.2, 0))]:
        ejes.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=10,
                                       color=AZUL, lw=1.1))
    locales = [
        (1.25, 0.62, r"$\frac{\partial v}{\partial \mathbf{w}} = \mathbf{x}$"),
        (3.55, 0.75, r"$\frac{\partial y}{\partial v} = \varphi'(v)$"),
        (6.1, 0.75, r"$\frac{\partial e}{\partial y} = -1$"),
        (8.7, 0.75, r"$\frac{\partial \xi}{\partial e} = 2e$"),
    ]
    for x, yy, texto in locales:
        ejes.text(x, yy, texto, ha="center", fontsize=10, color=ROJO)
    ejes.add_patch(FancyArrowPatch((9.4, -0.9), (0.4, -0.9), arrowstyle="-|>", mutation_scale=12,
                                   color=ROJO, lw=1.3, ls="--"))
    ejes.text(4.9, -1.25, r"hacia atrás: $\nabla_{\mathbf{w}}\xi = 2e \cdot (-1) \cdot \varphi'(v) \cdot "
                          r"\mathbf{x}$ — el producto de las derivadas locales del camino",
              ha="center", fontsize=9, color=ROJO)
    guardar(figura, "10-neurona-como-grafo.png")


def figura_11_perdidas():
    y = np.linspace(0.001, 0.999, 500)
    figura, (ejes_a, ejes_b) = plt.subplots(1, 2, figsize=(10.5, 3.8))
    ejes_a.plot(y, (1 - y) ** 2, color=AZUL, lw=1.6, label=r"cuadrático $(1-y)^2$")
    ejes_a.plot(y, -np.log(y), color=ROJO, lw=1.6, label=r"entropía cruzada $-\log y$")
    ejes_a.set_xlabel("$y$ (salida de la neurona)")
    ejes_a.set_title(r"Error con $y_d = 1$")
    ejes_a.set_ylim(0, 4)
    ejes_a.legend(fontsize=8)
    v = np.linspace(-8, 8, 600)
    s = 1 / (1 + np.exp(-v))
    ejes_b.plot(v, np.abs(2 * (1 - s) * s * (1 - s)), color=AZUL, lw=1.6,
                label=r"cuadrático: $|2(y_d-y)\,y(1-y)|$")
    ejes_b.plot(v, np.abs(s - 1), color=ROJO, lw=1.6, label=r"entropía cruzada: $|y-y_d|$")
    ejes_b.axvspan(-8, -4, color=GRIS_CLARO, alpha=0.4)
    ejes_b.text(-7.8, 0.85, "saturada\ny equivocada", fontsize=7.5, color=TINTA)
    ejes_b.set_xlabel("$v$")
    ejes_b.set_title(r"$|\partial\xi/\partial v|$ con $y_d = 1$")
    ejes_b.legend(fontsize=8, loc="upper right")
    guardar(figura, "11-cuadratico-vs-entropia.png")


def main():
    fp_automatica, f = verificar_mapa_logistico()
    valores = verificar_grafo_baydin()
    v, y = verificar_neurona()
    verificar_swish()
    verificar_mlp()
    verificar_relu_con_if()

    titulo_verificacion("Figuras")
    figura_01_mapa_logistico()
    figura_02_cuatro_formas()
    figura_03_explosion_y_error(fp_automatica, f)
    figura_04_grafo(valores)
    figura_05_directo_reverso()
    figura_06_jacobiano()
    figura_07_activaciones()
    figura_08_swish_errata()
    figura_09_desvanecimiento()
    figura_10_neurona_como_grafo(v, y)
    figura_11_perdidas()


if __name__ == "__main__":
    main()
