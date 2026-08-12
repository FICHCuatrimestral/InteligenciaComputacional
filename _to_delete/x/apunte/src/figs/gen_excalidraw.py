"""Versiones editables (.excalidraw) de los diagramas clave."""
import json, os, math, itertools

OUT = "/home/claude/work/excalidraw/"
BLUE, ORANGE, AQUA, VIOLET = "#1971c2", "#e8590c", "#099268", "#5f3dc4"
INK, GREY = "#1e1e1e", "#868e96"
BG_BLUE, BG_ORANGE, BG_VIOLET = "#d0ebff", "#ffe8cc", "#e5dbff"

_id = itertools.count(1)


def base(t, **kw):
    n = next(_id)
    el = {
        "id": f"el{n}", "type": t, "x": 0, "y": 0, "width": 0, "height": 0,
        "angle": 0, "strokeColor": INK, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": 1000 + n * 7, "version": 1,
        "versionNonce": 2000 + n * 13, "isDeleted": False, "boundElements": None,
        "updated": 1, "link": None, "locked": False,
    }
    el.update(kw)
    return el


def ellipse(x, y, w, h, **kw):
    return base("ellipse", x=x, y=y, width=w, height=h, **kw)


def rect(x, y, w, h, **kw):
    kw.setdefault("roundness", {"type": 3})
    return base("rectangle", x=x, y=y, width=w, height=h, **kw)


def text(x, y, s, size=20, color=INK, align="left", **kw):
    lines = s.split("\n")
    return base("text", x=x, y=y, width=max(len(l) for l in lines) * size * 0.55,
                height=len(lines) * size * 1.25, text=s, originalText=s,
                fontSize=size, fontFamily=1, textAlign=align,
                verticalAlign="top", baseline=int(size * 0.9),
                containerId=None, lineHeight=1.25, strokeColor=color, **kw)


def line(x1, y1, x2, y2, arrow=False, color=INK, dashed=False, width=2):
    return base("arrow" if arrow else "line", x=x1, y=y1,
                width=abs(x2 - x1), height=abs(y2 - y1),
                points=[[0, 0], [x2 - x1, y2 - y1]],
                lastCommittedPoint=None, startBinding=None, endBinding=None,
                startArrowhead=None, endArrowhead="arrow" if arrow else None,
                strokeColor=color, strokeWidth=width,
                strokeStyle="dashed" if dashed else "solid")


def save(name, els, title=None):
    doc = {"type": "excalidraw", "version": 2,
           "source": "Inteligencia Computacional - FICH-UNL",
           "elements": els, "appState": {"gridSize": None,
                                         "viewBackgroundColor": "#ffffff"},
           "files": {}}
    os.makedirs(OUT, exist_ok=True)
    json.dump(doc, open(OUT + name, "w"), ensure_ascii=False, indent=1)
    print(" ", name, f"({len(els)} elementos)")


# ------------------------------------------------------------ 1. modelo de neurona
def modelo():
    e = []
    e.append(text(180, 20, "Perceptrón simple", 28))
    cx, cy, R = 520, 260, 90
    filas = [(120, "x₁", "w₁"), (200, "x₂", "w₂"), (280, "xᵢ", "wᵢ"), (420, "x_N", "w_N")]
    for (y, xl, wl) in filas:
        e.append(text(120, y - 14, xl, 24))
        e.append(line(175, y, cx - R, cy + (y - cy) * 0.45, color=GREY))
        t = 0.45
        px = 175 + t * (cx - R - 175)
        py = y + t * (cy + (y - cy) * 0.45 - y)
        e.append(ellipse(px - 26, py - 26, 52, 52, strokeColor=VIOLET,
                         backgroundColor=BG_VIOLET))
        e.append(text(px - 18, py - 11, wl, 18, VIOLET))
    e.append(text(140, 340, "⋮", 26, GREY))
    # entrada extendida
    y = 500
    e.append(text(80, y - 14, "x₀ = −1", 22, AQUA))
    e.append(line(190, y, cx - R, cy + (y - cy) * 0.45, color=AQUA, dashed=True))
    t = 0.45
    px = 190 + t * (cx - R - 190); py = y + t * (cy + (y - cy) * 0.45 - y)
    e.append(ellipse(px - 26, py - 26, 52, 52, strokeColor=AQUA, backgroundColor="#c3fae8"))
    e.append(text(px - 18, py - 11, "w₀", 18, AQUA))
    # cuerpo
    e.append(ellipse(cx - R, cy - R, 2 * R, 2 * R, backgroundColor=BG_VIOLET,
                     strokeColor=INK, strokeWidth=2))
    e.append(text(cx - 42, cy - 52, "N\nΣ\ni = 0", 20, align="center"))
    e.append(text(cx - 34, cy + 30, "> 0 ?", 18))
    e.append(line(cx + R, cy, 800, cy, arrow=True, color=GREY))
    e.append(text(820, cy - 14, "y", 26))
    e.append(text(140, 600, "y = φ( ⟨w, x⟩ )      con  w₀ = u  (umbral / bias)", 20, GREY))
    save("01-modelo-neurona.excalidraw", e)


# ------------------------------------------------------------ 2. plano de decisión
def plano(name, titulo, pts, recta, extra_txt, w0_txt):
    """recta: (m, b) en coordenadas de datos; el plano va de -2 a 2."""
    e = []
    O = (450, 340)      # origen en pantalla
    S = 110             # px por unidad
    P = lambda x, y: (O[0] + x * S, O[1] - y * S)

    e.append(text(160, 30, titulo, 26))
    # ejes
    e.append(line(O[0] - 2.4 * S, O[1], O[0] + 2.4 * S, O[1], arrow=True, color=GREY))
    e.append(line(O[0], O[1] + 2.4 * S, O[0], O[1] - 2.4 * S, arrow=True, color=GREY))
    e.append(text(O[0] + 2.5 * S, O[1] - 10, "x₁", 20, GREY))
    e.append(text(O[0] + 12, O[1] - 2.7 * S, "x₂", 20, GREY))
    # marcas
    for v in (-1, 1):
        x, y = P(v, 0); e.append(line(x, y - 8, x, y + 8, color=GREY, width=1))
        e.append(text(x - 8, y + 14, str(v), 14, GREY))
        x, y = P(0, v); e.append(line(x - 8, y, x + 8, y, color=GREY, width=1))
        e.append(text(x - 26, y - 10, str(v), 14, GREY))
    # recta
    if recta:
        m, b = recta
        x1, x2 = -2.2, 2.2
        e.append(line(*P(x1, m * x1 + b), *P(x2, m * x2 + b), width=3))
    # puntos
    for (x, y, cls) in pts:
        px, py = P(x, y)
        if cls == "+":
            e.append(ellipse(px - 16, py - 16, 32, 32, strokeColor=BLUE,
                             backgroundColor=BG_BLUE))
        else:
            e.append(rect(px - 15, py - 15, 30, 30, strokeColor=ORANGE,
                          backgroundColor=BG_ORANGE))
    e.append(text(*[c for c in P(1.15, 1.75)], "y = +1", 20, BLUE))
    e.append(text(*[c for c in P(-2.15, -1.55)], "y = −1", 20, ORANGE))
    e.append(text(140, 700, extra_txt, 20, GREY))
    if w0_txt:
        e.append(text(140, 730, w0_txt, 20, GREY))
    save(name, e)


# ------------------------------------------------------------ 3. neurona biológica
def biologica():
    e = []
    e.append(text(200, 20, "Neurona biológica", 28))
    cx, cy = 480, 300
    e.append(ellipse(cx - 90, cy - 70, 180, 140, backgroundColor=BG_VIOLET))
    e.append(ellipse(cx - 24, cy - 24, 48, 48, strokeColor=VIOLET,
                     backgroundColor="#d0bfff"))
    # dendritas
    for a in (-0.9, -0.35, 0.3, 0.85):
        x0, y0 = cx - 88, cy + 45 * math.sin(a)
        for k in range(3):
            L = 90 - k * 22
            ang = math.pi + a + (0.35 if k % 2 else -0.35)
            e.append(line(x0, y0, x0 + L * math.cos(ang), y0 + L * math.sin(ang),
                          color=VIOLET, width=2))
            x0, y0 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
        e.append(ellipse(x0 - 11, y0 - 11, 22, 22, strokeColor=ORANGE,
                         backgroundColor=BG_ORANGE))
    # axón
    e.append(line(cx + 90, cy - 20, 1010, cy - 20, width=4))
    for i in range(4):
        e.append(rect(640 + i * 82, cy - 42, 58, 44, strokeColor=BLUE,
                      backgroundColor=BG_BLUE))
    for dy in (-60, 0, 60):
        e.append(line(1010, cy - 20, 1060, cy - 20 + dy, width=3))
        e.append(ellipse(1058, cy - 32 + dy, 24, 24, strokeColor=AQUA,
                         backgroundColor="#c3fae8"))
    # rótulos
    for (x, y, t, c) in [(120, 120, "botones sinápticos\n(entradas)", ORANGE),
                         (150, 470, "árbol dendrítico", VIOLET),
                         (430, 470, "soma", INK),
                         (560, 400, "núcleo", VIOLET),
                         (660, 150, "vaina de mielina", BLUE),
                         (860, 430, "nodo de Ranvier", GREY),
                         (1020, 130, "terminales", AQUA),
                         (860, 210, "axón", INK)]:
        e.append(text(x, y, t, 18, c))
    e.append(text(140, 560,
                  "muchas entradas  →  una sola salida", 22, GREY))
    save("04-neurona-biologica.excalidraw", e)


if __name__ == "__main__":
    print("Generando .excalidraw:")
    modelo()
    plano("02-or-con-bias.excalidraw", "OR resuelto:  x₁ + x₂ + 1 = 0",
          [(1, 1, "+"), (-1, 1, "+"), (1, -1, "+"), (-1, -1, "-")],
          (-1, -1),
          "La recta no pasa por el origen gracias a w₀ = −1.",
          "Sin ese término, el OR no tiene solución.")
    plano("03-xor.excalidraw", "XOR: no es linealmente separable",
          [(-1, 1, "+"), (1, -1, "+"), (1, 1, "-"), (-1, -1, "-")],
          None,
          "Los segmentos que unen cada clase se cruzan en el origen.",
          "Ninguna recta puede separarlas, ni con bias.")
    biologica()
