"""Figuras matemáticas: funciones de activación, fronteras de decisión, OR/XOR, gradiente."""
import math, os, sys
sys.path.insert(0, "/home/claude/work/figs")
from svgkit import *

OUT = "/home/claude/work/figs/out/"


# --------------------------------------------------------- funciones de activación
def activaciones():
    W, H = 720, 430
    s = SVG(W, H)
    pw, ph = 190, 138
    cols = [30, 265, 500]
    rows = [46, 258]

    def panel(ix, iy, title, f, extra=None, xr=(-3, 3), yr=(-1.55, 1.55),
              formula=None, color=BLUE):
        ax = Axes(s, cols[ix], rows[iy], pw, ph, xr=xr, yr=yr)
        # marco suave
        s.rect(cols[ix] - 12, rows[iy] - 30, pw + 30, ph + 76,
               fill="#ffffff", color=GRID, sw=1, rx=8)
        s.text(cols[ix] + pw / 2, rows[iy] - 12, title, size=12.5, color=SECOND,
               weight="600")
        # ejes
        s.line(ax.X(xr[0]), ax.Y(0), ax.X(xr[1]) + 8, ax.Y(0), color=AXIS, w=1.3, arrow=True)
        s.line(ax.X(0), ax.Y(yr[0]), ax.X(0), ax.Y(yr[1]) - 6, color=AXIS, w=1.3, arrow=True)
        s.text(ax.X(0) - 7, ax.Y(1) + 4, "+1", size=10, color=MUTED, anchor="end")
        s.text(ax.X(0) - 7, ax.Y(-1) + 4, "−1", size=10, color=MUTED, anchor="end")
        s.line(ax.X(xr[0]), ax.Y(1), ax.X(xr[1]), ax.Y(1), color=GRID, w=1, dash="3 3")
        s.line(ax.X(xr[0]), ax.Y(-1), ax.X(xr[1]), ax.Y(-1), color=GRID, w=1, dash="3 3")
        if extra:
            extra(ax)
        if isinstance(f, list):
            for (fn, c, dash) in f:
                ax.curve(fn, color=c, w=2.4, dash=dash)
        else:
            ax.curve(f, color=color, w=2.4)
        s.text(ax.X(xr[1]) + 12, ax.Y(0) + 4, "z", size=12, color=MUTED,
               family=MATHF, italic=True)
        if formula:
            s.text(cols[ix] + pw / 2, rows[iy] + ph + 30, formula, size=11.5,
                   color=SECOND, family=MATHF, italic=True)

    # 1. signo
    def sgn_curve(ax):
        s.poly([ax.P(-3, -1), ax.P(-0.001, -1)], color=BLUE, w=2.6)
        s.poly([ax.P(0, 1), ax.P(3, 1)], color=BLUE, w=2.6)
        s.line(ax.X(0), ax.Y(-1), ax.X(0), ax.Y(1), color=BLUE, w=2.6, dash="4 3")
        s.circle(ax.X(0), ax.Y(1), 3.6, fill=BLUE, color="none", w=0)
        s.circle(ax.X(0), ax.Y(-1), 3.6, fill=SURFACE, color=BLUE, w=2)
    panel(0, 0, "signo — sgn(z)", [], extra=sgn_curve,
          formula="−1 si z &lt; 0  ·  +1 si z ≥ 0")

    # 2. lineal a tramos
    a = 1.2
    panel(1, 0, "lineal a tramos — sln(z)",
          lambda z: -1 if z < -a else (1 if z >= a else z / a),
          formula="rampa de pendiente α entre −a y a")

    # 3. sigmoidea (dos pendientes)
    sig = lambda k: (lambda z: (1 - math.exp(-k * z)) / (1 + math.exp(-k * z)))
    panel(2, 0, "sigmoidea — sig(z)",
          [(sig(1.0), BLUE, None), (sig(4.0), VIOLET, "6 4")],
          formula="(1 − e⁻ᵃᶻ) ⁄ (1 + e⁻ᵃᶻ)")

    # 4. gaussiana
    panel(0, 1, "gaussiana", lambda z: math.exp(-z * z * 1.6),
          formula="e⁻ᵃᶻ²")

    # 5. sinusoidal
    panel(1, 1, "sinusoidal", lambda z: math.sin(3.2 * z) * math.exp(-abs(z) * 0.18),
          formula="variante periódica")

    # 6. nota
    s.rect(cols[2] - 12, rows[1] - 30, pw + 30, ph + 76, fill="#f4f2fb",
           color=GRID, sw=1, rx=8)
    s.text(cols[2] + pw / 2, rows[1] - 12, "la clave", size=12.5, color=VIOLET,
           weight="600")
    txt = ["A mayor a, la sigmoidea",
           "se parece más al escalón.",
           "",
           "En el límite a → ∞ es",
           "exactamente sgn(z).",
           "",
           "Pero sig es derivable",
           "y sgn no: por eso el MLP",
           "se entrena con sig."]
    for i, t in enumerate(txt):
        s.text(cols[2] + pw / 2, rows[1] + 22 + i * 18, t, size=11.5, color=SECOND)
    s.save(OUT + "fig04_activaciones.svg")


# --------------------------------------------------------- frontera de decisión
def frontera(fname, w1, w2, w0, pts, title, note=None, show_normal=False,
             extra_lines=None, W=430, H=380):
    s = SVG(W, H)
    ax = Axes(s, 62, 52, 300, 262, xr=(-2, 2), yr=(-2, 2))
    ax.halfplane(w1, w2, w0, +1, BLUE_F)
    ax.halfplane(w1, w2, w0, -1, ORANGE_F)
    ax.frame(ticks=[-1, 1])

    # recta
    if abs(w2) > 1e-9:
        m, b = -w1 / w2, w0 / w2
        p = ax.clipline(m, b)
        if len(p) == 2:
            s.poly([ax.P(*p[0]), ax.P(*p[1])], color=INK, w=2.6)

    # rectas alternativas fallidas
    for (m2, b2, col) in (extra_lines or []):
        p = ax.clipline(m2, b2)
        if len(p) == 2:
            s.poly([ax.P(*p[0]), ax.P(*p[1])], color=col, w=2, dash="6 4")

    # vector normal w
    if show_normal:
        n = math.hypot(w1, w2)
        # punto de la recta más cercano al origen
        px, py = w1 * w0 / (n * n), w2 * w0 / (n * n)
        L = 0.8
        s.line(*ax.P(px, py), *ax.P(px + w1 / n * L, py + w2 / n * L),
               color=VIOLET, w=2.6, arrow=True)
        s.mtext(*[c + d for c, d in zip(ax.P(px + w1 / n * L, py + w2 / n * L), (18, 2))],
                "w", size=17, color=VIOLET, weight="bold")
        # marca de ángulo recto
        ux, uy = w1 / n, w2 / n            # direccion de w
        tx, ty = -uy, ux                   # direccion de la recta
        d = 0.19
        c0 = ax.P(px + tx * d, py + ty * d)
        c1 = ax.P(px + tx * d + ux * d, py + ty * d + uy * d)
        c2 = ax.P(px + ux * d, py + uy * d)
        s.poly([c0, c1, c2], color=VIOLET, w=1.6)
        s.circle(*ax.P(px, py), 3.4, fill=VIOLET, color="none", w=0)

    # etiquetas de región
    s.text(*[c + d for c, d in zip(ax.P(1.35, 1.5), (0, 0))], "y = +1",
           size=13, color=BLUE, weight="600")
    s.text(*[c + d for c, d in zip(ax.P(-1.35, -1.6), (0, 0))], "y = −1",
           size=13, color=ORANGE, weight="600")

    for (x, y, k, lb) in pts:
        ax.dot(x, y, kind=k, label=lb)

    s.text(W / 2, 26, title, size=13.5, color=INK, weight="600")
    if note:
        s.text(W / 2, H - 14, note, size=12, color=SECOND)
    s.save(OUT + fname)


# --------------------------------------------------------- OR sin bias (falla)
def or_sin_bias():
    W, H = 430, 410
    s = SVG(W, H)
    ax = Axes(s, 62, 78, 300, 262, xr=(-2, 2), yr=(-2, 2))
    ax.frame(ticks=[-1, 1])
    for (m, b, c) in [(-0.5, 0, ORANGE), (-2.4, 0, VIOLET), (0.55, 0, AQUA)]:
        p = ax.clipline(m, b)
        if len(p) == 2:
            s.poly([ax.P(*p[0]), ax.P(*p[1])], color=c, w=1.8, dash="6 4")
    # el par antipodal problematico
    s.line(*ax.P(-1, 1), *ax.P(1, -1), color="#d03b3b", w=1.6, dash="3 4", opacity=0.8)
    for (x, y, k) in [(1, 1, "+"), (-1, 1, "+"), (1, -1, "+"), (-1, -1, "-")]:
        ax.dot(x, y, kind=k)
    for (x, y) in [(-1, 1), (1, -1)]:
        s.circle(*ax.P(x, y), 15, fill="none", color="#d03b3b", w=2)
    s.text(*[c + d for c, d in zip(ax.P(-1.35, 1.62), (0, 0))],
           "ambos deben dar +1", size=11.5, color="#d03b3b", weight="600")
    s.line(*[c + d for c, d in zip(ax.P(-1.35, 1.5), (0, 0))],
           *[c + d for c, d in zip(ax.P(-1.05, 1.18), (0, 0))],
           color="#d03b3b", w=1.1, dash="3 3")
    s.text(W / 2, 26, "OR sin bias: toda recta pasa por el origen", size=13.5,
           color=INK, weight="600")
    s.text(W / 2, 44, "(−1,+1) y (+1,−1) son opuestos entre sí", size=11.5, color="#d03b3b")
    s.text(W / 2, H - 30, "sus activaciones son iguales y de signo contrario:", size=12,
           color=SECOND)
    s.text(W / 2, H - 13, "o uno queda mal, o ambos caen sobre la recta", size=12,
           color=SECOND)
    s.save(OUT + "fig06_or_sin_bias.svg")


# --------------------------------------------------------- XOR
def xor():
    W, H = 430, 410
    s = SVG(W, H)
    ax = Axes(s, 62, 78, 300, 262, xr=(-2, 2), yr=(-2, 2))
    ax.frame(ticks=[-1, 1])
    for (m, b, c) in [(-1, 0.9, ORANGE), (1, -0.9, AQUA), (-1, -0.9, VIOLET)]:
        p = ax.clipline(m, b)
        if len(p) == 2:
            s.poly([ax.P(*p[0]), ax.P(*p[1])], color=c, w=1.8, dash="6 4")
    # los dos segmentos se cruzan en el origen
    s.line(*ax.P(-1, 1), *ax.P(1, -1), color=BLUE, w=2, opacity=0.55)
    s.line(*ax.P(-1, -1), *ax.P(1, 1), color=ORANGE, w=2, opacity=0.55)
    s.circle(*ax.P(0, 0), 6.5, fill="none", color="#d03b3b", w=2.2)
    s.text(*[c + d for c, d in zip(ax.P(0, 0), (58, 5))], "se cruzan", size=11.5,
           color="#d03b3b", weight="600")
    for (x, y, k) in [(-1, 1, "+"), (1, -1, "+"), (1, 1, "-"), (-1, -1, "-")]:
        ax.dot(x, y, kind=k)
    s.text(W / 2, 26, "XOR: los +1 quedan en diagonal", size=13.5, color=INK,
           weight="600")
    s.text(W / 2, 44, "y los −1 en la otra diagonal", size=11.5, color=SECOND)
    s.text(W / 2, H - 30, "los segmentos que unen cada clase se cruzan:", size=12,
           color=SECOND)
    s.text(W / 2, H - 13, "ninguna recta puede separarlas, ni con bias", size=12,
           color="#d03b3b")
    s.save(OUT + "fig09_xor.svg")


# --------------------------------------------------------- separabilidad lineal
def separabilidad():
    W, H = 700, 300
    s = SVG(W, H)
    import random
    for panel, sep in ((0, True), (1, False)):
        x0 = 50 + panel * 350
        ax = Axes(s, x0, 60, 260, 190, xr=(0, 10), yr=(0, 7))
        s.rect(x0 - 10, 48, 280, 214, fill="#ffffff", color=GRID, sw=1, rx=8)
        random.seed(7)
        A, B = [], []
        if sep:
            for i in range(14):
                A.append((random.uniform(0.9, 4.0), random.uniform(3.6, 6.2)))
                B.append((random.uniform(5.6, 9.1), random.uniform(0.8, 3.4)))
        else:
            # patron tipo XOR: cada clase en dos esquinas opuestas
            for i in range(7):
                A.append((random.uniform(0.9, 3.6), random.uniform(4.0, 6.2)))
                A.append((random.uniform(6.2, 9.0), random.uniform(0.8, 3.0)))
                B.append((random.uniform(6.2, 9.0), random.uniform(4.0, 6.2)))
                B.append((random.uniform(0.9, 3.6), random.uniform(0.8, 3.0)))
        for (x, y) in A:
            s.circle(ax.X(x), ax.Y(y), 6, fill=BLUE, color=SURFACE, w=1.6)
        for (x, y) in B:
            px, py = ax.X(x), ax.Y(y)
            s.rect(px - 5.6, py - 5.6, 11.2, 11.2, fill=ORANGE, color=SURFACE, sw=1.6, rx=2)
        if sep:
            p = ax.clipline(-0.62, 7.3)
            s.poly([ax.P(*p[0]), ax.P(*p[1])], color=INK, w=2.6)
        else:
            for (m, b, c) in ((-1.0, 8.4, VIOLET), (0.0, 3.5, AQUA), (1.0, -0.6, ORANGE)):
                p = ax.clipline(m, b)
                if len(p) == 2:
                    s.poly([ax.P(*p[0]), ax.P(*p[1])], color=c, w=1.8, dash="6 4")
        s.text(x0 + 130, 36, "linealmente separable" if sep else "no separable linealmente",
               size=13, color=INK if sep else "#d03b3b", weight="600")
        s.text(x0 + 130, 284,
               "existe un hiperplano: el perceptrón converge"
               if sep else "no existe: el perceptrón nunca converge",
               size=11.5, color=SECOND)
    s.save(OUT + "fig10_separabilidad.svg")


# --------------------------------------------------------- superficie de error
def gradiente():
    W, H = 700, 340
    s = SVG(W, H)
    # --- panel izq: corte 1-D ---
    ax = Axes(s, 56, 58, 250, 210, xr=(-2.4, 2.4), yr=(-0.4, 6.2))
    s.rect(40, 46, 286, 240, fill="#ffffff", color=GRID, sw=1, rx=8)
    ax.curve(lambda w: w * w + 0.4, color=BLUE, w=2.6)
    s.line(ax.X(-2.4), ax.Y(0), ax.X(2.4) + 6, ax.Y(0), color=AXIS, w=1.3, arrow=True)
    s.line(ax.X(0), ax.Y(-0.4), ax.X(0), ax.Y(6.2) - 6, color=AXIS, w=1.3, arrow=True)
    s.text(ax.X(2.4) + 14, ax.Y(0) + 4, "w", size=13, color=MUTED, family=MATHF, italic=True)
    s.text(ax.X(0) - 10, ax.Y(6.2) - 2, "ξ", size=14, color=MUTED, family=MATHF,
           italic=True, anchor="end")
    # pasos de descenso
    w = -2.05
    for i in range(5):
        g = 2 * w
        wn = w - 0.32 * g
        s.circle(ax.X(w), ax.Y(w * w + 0.4), 5.5, fill=ORANGE, color=SURFACE, w=1.6)
        s.line(ax.X(w), ax.Y(w * w + 0.4), ax.X(wn), ax.Y(wn * wn + 0.4),
               color=ORANGE, w=1.8, arrow=True, opacity=0.85)
        w = wn
    s.circle(ax.X(0), ax.Y(0.4), 6, fill=AQUA, color=SURFACE, w=2)
    s.text(ax.X(0), ax.Y(0.4) + 22, "mínimo", size=11, color=AQUA, weight="600")
    s.text(183, 34, "descenso por gradiente", size=13, color=INK, weight="600")
    s.text(183, 306, "cada paso resta  µ · ∇ξ", size=12, color=ORANGE)

    # --- panel der: curvas de nivel 2-D ---
    ax2 = Axes(s, 410, 58, 240, 210, xr=(-2.3, 2.3), yr=(-2.1, 2.1))
    s.rect(394, 46, 276, 240, fill="#ffffff", color=GRID, sw=1, rx=8)
    for r in (0.45, 0.9, 1.35, 1.8):
        pts = []
        for k in range(81):
            t = 2 * math.pi * k / 80
            pts.append(ax2.P(r * 1.25 * math.cos(t), r * 0.85 * math.sin(t)))
        s.poly(pts, color=BLUE, w=1.4, opacity=0.45)
    s.line(ax2.X(-2.3), ax2.Y(0), ax2.X(2.3) + 6, ax2.Y(0), color=AXIS, w=1.3, arrow=True)
    s.line(ax2.X(0), ax2.Y(-2.1), ax2.X(0), ax2.Y(2.1) - 6, color=AXIS, w=1.3, arrow=True)
    s.text(ax2.X(2.3) + 14, ax2.Y(0) + 4, "w₁", size=12.5, color=MUTED, family=MATHF, italic=True)
    s.text(ax2.X(0) - 12, ax2.Y(2.1) - 2, "w₂", size=12.5, color=MUTED, family=MATHF,
           italic=True, anchor="end")
    # trayectoria
    p, q = -1.85, 1.5
    for i in range(7):
        gx, gy = 2 * p / (1.25 ** 2), 2 * q / (0.85 ** 2)
        pn, qn = p - 0.14 * gx, q - 0.14 * gy
        s.line(ax2.X(p), ax2.Y(q), ax2.X(pn), ax2.Y(qn), color=ORANGE, w=2,
               arrow=True, opacity=0.9)
        p, q = pn, qn
    s.circle(ax2.X(0), ax2.Y(0), 6, fill=AQUA, color=SURFACE, w=2)
    # gradiente ascendente en un punto
    s.line(ax2.X(-1.85), ax2.Y(1.5), ax2.X(-1.85) - 26, ax2.Y(1.5) - 22,
           color=VIOLET, w=2.2, arrow=True)
    s.text(ax2.X(-1.85) - 4, ax2.Y(1.5) - 32, "∇ξ", size=13, color=VIOLET,
           weight="600", anchor="start")
    s.text(532, 34, "curvas de nivel del error", size=13, color=INK, weight="600")
    s.text(532, 306, "el gradiente apunta al ascenso; nos movemos al revés",
           size=11.5, color=SECOND)
    s.save(OUT + "fig08_gradiente.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    activaciones()
    # frontera sin bias
    frontera("fig05_frontera.svg", 1, 1, 0,
             [], "Frontera de decisión: w₁x₁ + w₂x₂ = 0",
             note="pasa siempre por el origen; pendiente −w₁/w₂", show_normal=False)
    # w como normal
    frontera("fig07_normal.svg", 1, 1.6, 1.1, [],
             "El vector w es perpendicular a la frontera",
             note="w apunta hacia el semiplano donde y = +1", show_normal=True)
    or_sin_bias()
    # OR con bias
    frontera("fig06b_or_con_bias.svg", 1, 1, -1,
             [(1, 1, "+", None), (-1, 1, "+", None), (1, -1, "+", None),
              (-1, -1, "-", None)],
             "OR con bias: x₁ + x₂ + 1 = 0",
             note="w₀ = −1 desplaza la recta y resuelve el problema")
    xor()
    separabilidad()
    gradiente()
    print("ok")
