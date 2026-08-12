"""Mini-toolkit para dibujar figuras SVG consistentes."""
import math

INK      = "#0b0b0b"
SECOND   = "#52514e"
MUTED    = "#898781"
GRID     = "#e1e0d9"
AXIS     = "#c3c2b7"
SURFACE  = "#fcfcfb"
BLUE     = "#2a78d6"   # clase +1
ORANGE   = "#eb6834"   # clase -1
AQUA     = "#1baf7a"
VIOLET   = "#4a3aa7"
BLUE_F   = "#e8f1fc"   # relleno suave
ORANGE_F = "#fdeee7"

SANS  = "system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MATHF = "Georgia,'Times New Roman',serif"


class SVG:
    def __init__(self, w, h, pad=0):
        self.w, self.h = w, h
        self.parts = []
        self.defs = []
        self._marker_ids = set()

    # ---------- infra ----------
    def marker(self, name, color, size=7):
        mid = f"arw-{name}"
        if mid in self._marker_ids:
            return mid
        self._marker_ids.add(mid)
        self.defs.append(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 10 5 L 0 9 z" fill="{color}"/></marker>')
        return mid

    def raw(self, s):
        self.parts.append(s)

    # ---------- primitivas ----------
    def line(self, x1, y1, x2, y2, color=INK, w=2, dash=None, arrow=None,
             cap="round", opacity=1):
        extra = ""
        if dash:
            extra += f' stroke-dasharray="{dash}"'
        if arrow:
            mid = self.marker(f"{color[1:]}", color)
            extra += f' marker-end="url(#{mid})"'
            if arrow == "both":
                extra += f' marker-start="url(#{mid})"'
        self.parts.append(
            f'<path d="M {x1:.2f} {y1:.2f} L {x2:.2f} {y2:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}"'
            f' opacity="{opacity}"{extra}/>')

    def path(self, d, color=INK, w=2, fill="none", dash=None, arrow=None, opacity=1):
        extra = ""
        if dash:
            extra += f' stroke-dasharray="{dash}"'
        if arrow:
            mid = self.marker(f"{color[1:]}", color)
            extra += f' marker-end="url(#{mid})"'
        self.parts.append(
            f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"{extra}/>')

    def poly(self, pts, color=INK, w=2, fill="none", dash=None, opacity=1):
        d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
        self.path(d, color, w, fill, dash, opacity=opacity)

    def circle(self, cx, cy, r, fill="none", color=INK, w=2, opacity=1):
        self.parts.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
            f'stroke="{color}" stroke-width="{w}" opacity="{opacity}"/>')

    def rect(self, x, y, w_, h_, fill="none", color="none", sw=2, rx=4, opacity=1):
        self.parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w_:.2f}" height="{h_:.2f}" rx="{rx}" '
            f'fill="{fill}" stroke="{color}" stroke-width="{sw}" opacity="{opacity}"/>')

    def text(self, x, y, s, size=13, color=INK, anchor="middle", family=SANS,
             italic=False, weight="normal", opacity=1):
        st = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-family="{family}" font-weight="{weight}"'
            f'{st} opacity="{opacity}">{s}</text>')

    def mtext(self, x, y, s, size=14, color=INK, anchor="middle", **kw):
        self.text(x, y, s, size=size, color=color, anchor=anchor,
                  family=MATHF, italic=True, **kw)

    def var(self, x, y, base, sub="", size=16, color=INK, anchor="middle",
            upright_sub=True):
        """Variable matemática con subíndice: base en itálica, subíndice chico."""
        sb = ""
        if sub:
            st = "" if upright_sub else ' font-style="italic"'
            sb = (f'<tspan font-size="{size*0.66:.1f}" dy="{size*0.22:.1f}"{st}>'
                  f'{sub}</tspan>')
        self.parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-family="{MATHF}" font-style="italic">'
            f'{base}{sb}</text>')

    def render(self):
        defs = ("<defs>" + "".join(self.defs) + "</defs>") if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="100%" style="max-width:{self.w}px;height:auto" '
                f'font-family="{SANS}">{defs}'
                + "".join(self.parts) + "</svg>")

    def save(self, path, standalone_bg=False):
        body = self.render()
        if standalone_bg:
            body = body.replace("<defs>", f'<rect width="{self.w}" height="{self.h}" '
                                          f'fill="{SURFACE}"/><defs>', 1)
            if "<defs>" not in self.render():
                body = body.replace(">", f'><rect width="{self.w}" height="{self.h}" '
                                         f'fill="{SURFACE}"/>', 1)
        open(path, "w").write(body)


class Axes:
    """Sistema de ejes cartesianos dentro de un SVG."""

    def __init__(self, svg, x0, y0, w, h, xr=(-2, 2), yr=(-2, 2)):
        self.s = svg
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xr, self.yr = xr, yr

    def X(self, x):
        a, b = self.xr
        return self.x0 + (x - a) / (b - a) * self.w

    def Y(self, y):
        a, b = self.yr
        return self.y0 + self.h - (y - a) / (b - a) * self.h

    def P(self, x, y):
        return self.X(x), self.Y(y)

    def frame(self, xlabel="x₁", ylabel="x₂", ticks=None, labelsize=14):
        s = self.s
        # ejes con flechas
        s.line(self.x0 - 8, self.Y(0), self.x0 + self.w + 10, self.Y(0),
               color=AXIS, w=1.5, arrow=True)
        s.line(self.X(0), self.y0 + self.h + 8, self.X(0), self.y0 - 10,
               color=AXIS, w=1.5, arrow=True)
        if xlabel:
            s.mtext(self.x0 + self.w + 16, self.Y(0) + 5, xlabel, size=labelsize, color=SECOND)
        if ylabel:
            s.mtext(self.X(0) - 4, self.y0 - 16, ylabel, size=labelsize, color=SECOND,
                    anchor="end")
        for t in (ticks or []):
            x, y = self.P(t, 0)
            s.line(x, y - 4, x, y + 4, color=AXIS, w=1.5)
            s.text(x, y + 17, str(t), size=11, color=MUTED)
            x, y = self.P(0, t)
            s.line(x - 4, y, x + 4, y, color=AXIS, w=1.5)
            s.text(x - 9, y + 4, str(t), size=11, color=MUTED, anchor="end")

    def clipline(self, m, b):
        """Devuelve los dos extremos de y = m x + b recortados al marco."""
        xa, xb = self.xr
        ya, yb = self.yr
        pts = []
        for x in (xa, xb):
            y = m * x + b
            if ya - 1e-9 <= y <= yb + 1e-9:
                pts.append((x, y))
        if abs(m) > 1e-9:
            for y in (ya, yb):
                x = (y - b) / m
                if xa - 1e-9 <= x <= xb + 1e-9:
                    pts.append((x, y))
        # unicos
        out = []
        for p in pts:
            if not any(abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6 for q in out):
                out.append(p)
        return out[:2]

    def halfplane(self, w1, w2, w0, sign, fill):
        """Sombrea {x : sign*(w1 x1 + w2 x2 - w0) > 0} dentro del marco."""
        xa, xb = self.xr
        ya, yb = self.yr
        N = 160
        poly = []
        # muestreo del rectangulo en grilla fina -> usar recorte por semiplano
        corners = [(xa, ya), (xb, ya), (xb, yb), (xa, yb)]
        def inside(p):
            return sign * (w1 * p[0] + w2 * p[1] - w0) >= 0
        # Sutherland-Hodgman contra la recta
        out = []
        n = len(corners)
        for i in range(n):
            cur, nxt = corners[i], corners[(i + 1) % n]
            ci, ni = inside(cur), inside(nxt)
            if ci:
                out.append(cur)
            if ci != ni:
                f1 = w1 * cur[0] + w2 * cur[1] - w0
                f2 = w1 * nxt[0] + w2 * nxt[1] - w0
                t = f1 / (f1 - f2)
                out.append((cur[0] + t * (nxt[0] - cur[0]),
                            cur[1] + t * (nxt[1] - cur[1])))
        if len(out) >= 3:
            pts = [self.P(*p) for p in out]
            d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"
            self.s.path(d, color="none", w=0, fill=fill)

    def curve(self, f, xs=None, color=BLUE, w=2.5, dash=None, n=300):
        xa, xb = self.xr
        ya, yb = self.yr
        xs = xs or (xa, xb)
        segs, cur = [], []
        for i in range(n + 1):
            x = xs[0] + (xs[1] - xs[0]) * i / n
            try:
                y = f(x)
            except Exception:
                y = None
            if y is None or not (ya - 1e-9 <= y <= yb + 1e-9):
                if len(cur) > 1:
                    segs.append(cur)
                cur = []
            else:
                cur.append(self.P(x, y))
        if len(cur) > 1:
            segs.append(cur)
        for sg in segs:
            self.s.poly(sg, color=color, w=w, dash=dash)

    def dot(self, x, y, kind="+", r=7, label=None, lblcolor=None):
        s = self.s
        px, py = self.P(x, y)
        if kind == "+":
            s.circle(px, py, r, fill=BLUE, color=SURFACE, w=2)
        else:
            s.rect(px - r, py - r, 2 * r, 2 * r, fill=ORANGE, color=SURFACE, sw=2, rx=2)
        if label:
            s.text(px, py - r - 8, label, size=12,
                   color=lblcolor or (BLUE if kind == "+" else ORANGE), weight="600")
