"""Figuras: neurona biológica, sinapsis, y las tres etapas del modelo."""
import math, os, sys, random
sys.path.insert(0, "/home/claude/work/figs")
from svgkit import *

OUT = "/home/claude/work/figs/out/"


# ---------------------------------------------------------------- neurona biológica
def neurona_biologica():
    s = SVG(780, 380)
    cx, cy = 340, 190
    tips = []

    def rama(x, y, ang, L, depth, w):
        x2 = x + L * math.cos(ang)
        y2 = y + L * math.sin(ang)
        s.line(x, y, x2, y2, color=VIOLET, w=w, opacity=0.9)
        if depth == 1:
            tips.append((x2, y2))
            return
        rama(x2, y2, ang - 0.42, L * 0.68, depth - 1, max(1.2, w - 0.7))
        rama(x2, y2, ang + 0.42, L * 0.68, depth - 1, max(1.2, w - 0.7))

    for a in (-0.95, -0.34, 0.28, 0.86):
        rama(cx - 48, cy + 16 * math.sin(a), math.pi + a * 0.9, 50, 4, 3.4)

    # soma
    s.path(f"M {cx-54} {cy} C {cx-52} {cy-48}, {cx+18} {cy-54}, {cx+48} {cy-22} "
           f"C {cx+64} {cy-4}, {cx+60} {cy+26}, {cx+32} {cy+42} "
           f"C {cx-4} {cy+58}, {cx-52} {cy+40}, {cx-54} {cy} Z",
           color=INK, w=2.4, fill="#f4f2fb")
    s.circle(cx + 2, cy - 6, 15, fill="#ddd8f2", color=VIOLET, w=2)

    # axón + mielina
    ay = cy - 10
    s.line(cx + 54, ay, 700, ay, color=INK, w=3)
    for i in range(4):
        s.rect(404 + i * 60, ay - 11, 42, 22, fill="#eef4fc", color=BLUE, sw=2, rx=9)
    for dy in (-38, 0, 38):
        s.line(700, ay, 726, ay + dy, color=INK, w=2.4)
        s.circle(731, ay + dy, 7, fill=AQUA, color=SURFACE, w=2)

    # botones sinápticos en las puntas de las dendritas
    random.seed(3)
    for (x, y) in random.sample(tips, 7):
        s.circle(x, y, 6, fill=ORANGE, color=SURFACE, w=1.8)

    lead = lambda a, b, c, d: s.line(a, b, c, d, color=MUTED, w=1.1, dash="3 3")
    L = lambda x, y, t, c=SECOND, an="middle": s.text(x, y, t, size=12.5, color=c, anchor=an)

    lead(126, 66, 176, 116); L(122, 58, "botones sinápticos", ORANGE, "end")
    L(122, 74, "(entradas)", MUTED, "end")
    lead(150, 322, 206, 268); L(150, 338, "árbol dendrítico", VIOLET, "middle")
    lead(cx - 26, 330, cx - 20, 246); L(cx - 26, 346, "soma", INK)
    lead(cx + 44, 330, cx + 12, 216); L(cx + 50, 346, "núcleo", VIOLET)
    lead(448, 92, 432, 166); L(452, 84, "vaina de mielina", BLUE, "start")
    lead(500, 288, 512, 194); L(496, 304, "nodo de Ranvier", MUTED)
    lead(706, 300, 730, 240); L(706, 316, "terminales", AQUA)
    L(646, 152, "axón", INK)

    s.line(170, 34, 262, 34, color=MUTED, w=1.6, arrow=True)
    L(216, 26, "sentido de la señal", MUTED)
    s.save(OUT + "fig01_neurona.svg")


# ---------------------------------------------------------------- sinapsis
def sinapsis():
    s = SVG(700, 310)
    s.path("M 30 46 C 120 36, 240 54, 258 98 C 270 132, 270 162, 258 196 "
           "C 240 242, 120 258, 30 248 Z", color=INK, w=2.2, fill="#fdeee7")
    s.text(140, 34, "terminal presináptica", size=12.5, color=ORANGE)
    for (x, y) in [(132, 96), (180, 122), (152, 158), (200, 182), (112, 196),
                   (184, 72), (224, 146)]:
        s.circle(x, y, 11, fill=SURFACE, color=ORANGE, w=2)
        for k in range(4):
            a = k * 1.57 + 0.4
            s.circle(x + 4.6 * math.cos(a), y + 4.6 * math.sin(a), 1.8,
                     fill=ORANGE, color="none", w=0)
    s.text(120, 232, "vesículas", size=11, color=ORANGE)

    s.rect(262, 66, 46, 176, fill="#f2f1ed", color="none", sw=0, rx=2)
    s.line(285, 250, 285, 266, color=MUTED, w=1.1, dash="3 3")
    s.text(272, 282, "hendidura sináptica", size=12, color=MUTED)

    random.seed(9)
    for i in range(12):
        s.circle(268 + random.random() * 36, 78 + random.random() * 150, 3.4,
                 fill=AQUA, color="none", w=0)
    s.line(276, 56, 302, 56, color=AQUA, w=1.6, arrow=True)
    s.text(300, 44, "neurotransmisores", size=11, color=AQUA)

    s.path("M 312 50 L 312 258 L 402 258 C 364 202, 364 106, 402 50 Z",
           color=INK, w=2.2, fill="#eef4fc")
    s.text(392, 34, "membrana postsináptica", size=12.5, color=BLUE, anchor="middle")
    for y in (92, 128, 164, 200):
        s.rect(306, y - 9, 14, 18, fill=BLUE, color=SURFACE, sw=1.6, rx=3)
    s.text(358, 232, "receptores", size=11, color=BLUE)

    s.line(412, 106, 466, 106, color=MUTED, w=1.6, arrow=True)
    s.text(580, 102, "entran iones +  →  despolariza", size=12.5, color=BLUE)
    s.text(580, 120, "efecto excitatorio  (w > 0)", size=11, color=MUTED)
    s.line(412, 182, 466, 182, color=MUTED, w=1.6, arrow=True)
    s.text(582, 178, "entran iones −  →  hiperpolariza", size=12.5, color=ORANGE)
    s.text(582, 196, "efecto inhibitorio  (w < 0)", size=11, color=MUTED)
    s.save(OUT + "fig02_sinapsis.svg")


# ---------------------------------------------------------------- modelo de neurona
def modelo(stage, fname):
    s = SVG(620, 372)
    cx, cy, R = 356, 168, 66
    rows = [(40, "x", "1", "w", "1"),
            (92, "x", "2", "w", "2"),
            (144, "x", "i", "w", "i"),
            (248, "x", "N", "w", "N")]

    for (y, xb, xs_, wb, ws_) in rows:
        s.var(84, y + 6, xb, xs_, size=17, color=INK, anchor="end")
        x1, y1 = 96, y
        x2, y2 = cx - R - 4, cy + (y - cy) * 0.42
        s.line(x1, y1, x2, y2, color=AXIS, w=1.6)
        t = 0.42
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        s.circle(px, py, 15, fill=SURFACE, color=VIOLET, w=2)
        s.var(px, py + 5, wb, ws_, size=13.5, color=VIOLET)

    s.text(78, 200, "⋮", size=22, color=MUTED, anchor="end")
    s.text(170, 208, "⋮", size=20, color=MUTED)

    if stage == 3:
        y = 316
        s.text(88, y + 6, "x₀ = −1", size=16, color=AQUA, anchor="end",
               family=MATHF, italic=True)
        x1, y1 = 96, y
        x2, y2 = cx - R - 4, cy + (y - cy) * 0.42
        s.line(x1, y1, x2, y2, color=AQUA, w=1.8, dash="6 4")
        t = 0.42
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        s.circle(px, py, 15, fill=SURFACE, color=AQUA, w=2)
        s.var(px, py + 5, "w", "0", size=13.5, color=AQUA)

    s.circle(cx, cy, R, fill="#f4f2fb", color=INK, w=2.4)
    if stage == 1:
        s.text(cx, cy - 12, "Σ", size=34, color=INK, family=MATHF)
        s.text(cx, cy + 26, "&gt; u ?", size=17, color=INK, family=MATHF, italic=True)
        cap = "el umbral u se compara afuera de la suma"
        capc = MUTED
    elif stage == 2:
        s.text(cx, cy - 6, "Σ − u", size=26, color=INK, family=MATHF, italic=True)
        s.text(cx, cy + 28, "&gt; 0 ?", size=17, color=INK, family=MATHF, italic=True)
        cap = "el umbral entra en la suma, restando"
        capc = MUTED
    else:
        s.text(cx, cy - 34, "N", size=12, color=INK, family=MATHF, italic=True)
        s.text(cx, cy - 2, "Σ", size=32, color=INK, family=MATHF)
        s.text(cx, cy + 22, "i = 0", size=12, color=INK, family=MATHF, italic=True)
        s.text(cx, cy + 48, "&gt; 0 ?", size=16, color=INK, family=MATHF, italic=True)
        cap = "el umbral es una entrada más:  x₀ = −1,  w₀ = u"
        capc = AQUA

    s.line(cx + R, cy, 540, cy, color=AXIS, w=1.8, arrow=True)
    s.var(560, cy + 7, "y", "", size=19, color=INK)
    s.text(330, 352, cap, size=12.5, color=capc)
    s.save(OUT + fname)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    neurona_biologica()
    sinapsis()
    modelo(1, "fig03a_modelo.svg")
    modelo(2, "fig03b_modelo.svg")
    modelo(3, "fig03c_modelo.svg")
    print("ok")
