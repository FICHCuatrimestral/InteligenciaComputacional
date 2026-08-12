"""Figuras del aprendizaje: geometría de la corrección de pesos + ejemplo numérico."""
import math, os, sys
sys.path.insert(0, "/home/claude/work/figs")
from svgkit import *

OUT = "/home/claude/work/figs/out/"


def correccion():
    """w(n+1) = w(n) ± ηx rota el vector de pesos hacia / en contra de la entrada."""
    W, H = 720, 392
    s = SVG(W, H)

    def panel(x0, titulo, sub, signo, color_paso):
        ax = Axes(s, x0, 86, 262, 232, xr=(-1.1, 2.3), yr=(-1.1, 2.3))
        s.rect(x0 - 16, 62, 300, 288, fill="#ffffff", color=GRID, sw=1, rx=8)
        s.line(ax.X(-1.1), ax.Y(0), ax.X(2.3) + 6, ax.Y(0), color=AXIS, w=1.3, arrow=True)
        s.line(ax.X(0), ax.Y(-1.1), ax.X(0), ax.Y(2.3) - 6, color=AXIS, w=1.3, arrow=True)

        wv = (1.55, 0.42)
        xv = (0.55, 1.35)
        eta = 0.62
        wn = (wv[0] + signo * eta * xv[0], wv[1] + signo * eta * xv[1])

        # frontera actual (perpendicular a w) y nueva
        def recta(v, col, dash, wdt):
            m = -v[0] / v[1] if abs(v[1]) > 1e-9 else 1e9
            pts = ax.clipline(m, 0)
            if len(pts) == 2:
                s.line(*ax.P(*pts[0]), *ax.P(*pts[1]), color=col, w=wdt, dash=dash)
        recta(wv, MUTED, "5 4", 1.6)
        recta(wn, INK, None, 2.2)

        # vector entrada
        s.line(*ax.P(0, 0), *ax.P(*xv), color=BLUE, w=2.6, arrow=True)
        s.mtext(*[c + d for c, d in zip(ax.P(*xv), (-16, -6))], "x", size=16,
                color=BLUE, weight="bold")
        # w viejo
        s.line(*ax.P(0, 0), *ax.P(*wv), color=MUTED, w=2.2, arrow=True)
        s.text(*[c + d for c, d in zip(ax.P(*wv), (6, 22) if signo > 0 else (10, -12))],
               "w(n)", size=12, color=MUTED, family=MATHF, italic=True)
        # paso
        s.line(*ax.P(*wv), *ax.P(*wn), color=color_paso, w=2.4, arrow=True, dash="5 3")
        mx, my = (wv[0] + wn[0]) / 2, (wv[1] + wn[1]) / 2
        off = (40, 6) if signo > 0 else (42, 16)
        s.text(*[c + d for c, d in zip(ax.P(mx, my), off)],
               ("+ η x" if signo > 0 else "− η x"), size=13, color=color_paso,
               family=MATHF, italic=True, weight="600")
        # w nuevo
        s.line(*ax.P(0, 0), *ax.P(*wn), color=VIOLET, w=2.6, arrow=True)
        s.text(*[c + d for c, d in zip(ax.P(*wn), (-6, -14) if signo > 0 else (14, 22))],
               "w(n+1)", size=12.5, color=VIOLET, family=MATHF, italic=True,
               weight="600", anchor="middle")

        s.text(x0 + 130, 34, titulo, size=13, color=INK, weight="600")
        s.text(x0 + 130, 52, sub, size=11.5, color=SECOND)
        s.text(x0 + 130, 370, "línea punteada: frontera vieja · línea llena: nueva",
               size=11, color=MUTED)

    panel(40, "Faltó activarse:  yd = +1,  y = −1", "hay que acercar w a x", +1, AQUA)
    panel(400, "Se activó de más:  yd = −1,  y = +1", "hay que alejar w de x", -1, ORANGE)
    s.save(OUT + "fig11_correccion.svg")


def ejemplo_numerico():
    """El ejemplo del gradiente de la diapositiva, paso a paso."""
    W, H = 700, 300
    s = SVG(W, H)
    box = lambda x, y, w, h, f, c: s.rect(x, y, w, h, fill=f, color=c, sw=1.6, rx=8)

    # antes
    box(24, 54, 196, 210, "#fdeee7", ORANGE)
    s.text(122, 40, "antes de corregir", size=13, color=ORANGE, weight="600")
    filas = [("w(n)", "( +1, +1, +1 )", VIOLET),
             ("x(n)", "( −1, +1, +1 )", BLUE),
             ("⟨w, x⟩", "−1 + 1 + 1 = +1", INK),
             ("y", "sgn(+1) = +1", INK),
             ("yd", "−1", AQUA),
             ("e = yd − y", "−2", "#d03b3b")]
    for i, (a, b, c) in enumerate(filas):
        s.text(40, 84 + i * 30, a, size=12, color=SECOND, anchor="start",
               family=MATHF, italic=True)
        s.text(206, 84 + i * 30, b, size=12, color=c, anchor="end", weight="600")

    # flecha
    s.line(232, 158, 288, 158, color=MUTED, w=2, arrow=True)
    s.text(260, 142, "µ = ½", size=12, color=SECOND, family=MATHF, italic=True)

    # actualizacion
    box(300, 84, 200, 150, "#f4f2fb", VIOLET)
    s.text(400, 70, "actualización", size=13, color=VIOLET, weight="600")
    s.text(400, 116, "w(n+1) = w(n) + 2µ e x(n)", size=12.5, color=INK,
           family=MATHF, italic=True)
    s.text(400, 152, "( +1, +1, +1 ) + ( +2, −2, −2 )", size=12, color=SECOND)
    s.text(400, 186, "= ( +3, −1, −1 )", size=14, color=VIOLET, weight="700")

    # despues
    box(514, 54, 176, 210, "#eef4fc", BLUE)
    s.text(602, 40, "después", size=13, color=BLUE, weight="600")
    filas2 = [("w(n+1)", "( +3, −1, −1 )", VIOLET),
              ("x", "( −1, +1, +1 )", BLUE),
              ("⟨w, x⟩", "−3 − 1 − 1 = −5", INK),
              ("y", "sgn(−5) = −1", INK),
              ("yd", "−1", AQUA),
              ("e", "0  ✓", "#0ca30c")]
    for i, (a, b, c) in enumerate(filas2):
        s.text(528, 84 + i * 30, a, size=12, color=SECOND, anchor="start",
               family=MATHF, italic=True)
        s.text(678, 84 + i * 30, b, size=12, color=c, anchor="end", weight="600")
    s.text(350, 288, "una sola iteración alcanzó para corregir este ejemplo",
           size=12, color=SECOND)
    s.save(OUT + "fig12_ejemplo.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    correccion()
    ejemplo_numerico()
    print("ok")
