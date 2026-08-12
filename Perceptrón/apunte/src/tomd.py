"""Convierte contenido.html a Markdown para GitHub (con math LaTeX y alerts)."""
import re, sys
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = "/home/claude/work/contenido.html"
DST = "/home/claude/work/APUNTE.md"
FIGDIR = "figuras"

ALERT = {"biblio": "NOTE", "parcial": "TIP", "clave": "IMPORTANT", "ojo": "WARNING"}


def esc(t):
    """Escapa caracteres de Markdown fuera de math."""
    return t.replace("|", "\\|")


def inline(node, in_table=False):
    """Serializa contenido inline a Markdown."""
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            s = str(c)
            s = re.sub(r"\s+", " ", s)
            out.append(s.replace("|", "\\|") if in_table else s)
        elif isinstance(c, Tag):
            if c.name in ("strong", "b"):
                out.append(f"**{inline(c, in_table).strip()}**")
            elif c.name in ("em", "i", "cite"):
                out.append(f"*{inline(c, in_table).strip()}*")
            elif c.name == "code":
                out.append(f"`{c.get_text()}`")
            elif c.name == "a":
                txt = inline(c, in_table).strip()
                href = c.get("href", "")
                out.append(f"[{txt}]({href})" if not href.startswith("#") else txt)
            elif c.name == "br":
                out.append("<br>" if in_table else "\n")
            elif c.name == "span":
                out.append(inline(c, in_table))
            else:
                out.append(inline(c, in_table))
    return "".join(out)


def eqnum(el):
    """<div class='eqn'><div class='eq'>$$..$$</div><span class='tag'>(n)</span></div>"""
    eq = el.find("div", class_="eq")
    tag = el.find("span", class_="tag")
    body = eq.get_text().strip()
    m = re.match(r"^\$\$(.*)\$\$$", body, re.S)
    tex = m.group(1).strip() if m else body
    if tag:
        n = tag.get_text().strip().strip("()")
        tex = tex + r"\qquad\qquad \text{(" + n + ")}"
    return "$$\n" + tex + "\n$$"


def table(el):
    rows = []
    head = el.find("thead")
    cols = 0
    if head:
        hs = [inline(th, True).strip() for th in head.find_all(["th", "td"])]
        cols = len(hs)
        rows.append("| " + " | ".join(hs) + " |")
        rows.append("|" + "|".join(["---"] * cols) + "|")
    body = el.find("tbody") or el
    for tr in body.find_all("tr"):
        cells = [inline(td, True).strip() for td in tr.find_all(["td", "th"])]
        if not cells:
            continue
        if not cols:
            cols = len(cells)
            rows.append("| " + " | ".join([" "] * cols) + " |")
            rows.append("|" + "|".join(["---"] * cols) + "|")
        while len(cells) < cols:
            cells.append("")
        rows.append("| " + " | ".join(cells[:cols]) + " |")
    return "\n".join(rows)


def lista(el, depth=0, ordered=False):
    out = []
    pad = "  " * depth
    for i, li in enumerate(el.find_all("li", recursive=False), 1):
        sub = []
        for ch in list(li.children):
            if isinstance(ch, Tag) and ch.name in ("ul", "ol"):
                sub.append(lista(ch, depth + 1, ch.name == "ol"))
                ch.extract()
        marker = f"{i}." if ordered else "-"
        txt = inline(li).strip()
        out.append(f"{pad}{marker} {txt}")
        out.extend(sub)
    return "\n".join(out)


BLOCK_TAGS = {"p", "ul", "ol", "table", "div", "blockquote", "figure", "h3", "h4"}


def children_blocks(el):
    """Agrupa los hijos en bloques; las corridas de contenido inline forman párrafos."""
    out, buf = [], []
    def flush():
        if buf:
            frag = BeautifulSoup("<p>" + "".join(str(x) for x in buf) + "</p>", "html.parser")
            t = inline(frag.p).strip()
            if t:
                out.append(t)
            buf.clear()
    for ch in el.children:
        if isinstance(ch, Tag) and ch.name in BLOCK_TAGS:
            flush()
            b = block(ch)
            if b:
                out.append(b)
        else:
            if isinstance(ch, NavigableString) and not ch.strip():
                continue
            buf.append(ch)
    flush()
    return out


def block(el, quote=""):
    """Devuelve markdown de un elemento de bloque."""
    if not isinstance(el, Tag):
        return ""
    cls = el.get("class") or []
    if el.name == "p":
        t = inline(el).strip()
        return t
    if el.name in ("h3", "h4"):
        lvl = "###" if el.name == "h3" else "####"
        return f"{lvl} {inline(el).strip()}"
    if el.name == "table":
        return table(el)
    if el.name == "ul":
        return lista(el, 0, False)
    if el.name == "ol":
        return lista(el, 0, True)
    if el.name == "blockquote":
        cite = el.find("cite")
        citetxt = None
        if cite:
            citetxt = inline(cite).strip()
            cite.extract()
        parts = children_blocks(el)
        if citetxt:
            parts.append("— " + citetxt)
        body = "\n\n".join(parts)
        return "\n".join("> " + l if l.strip() else ">" for l in body.split("\n"))
    if el.name == "div" and "eqn" in cls:
        return eqnum(el)
    if el.name == "div" and "eq" in cls:
        body = el.get_text().strip()
        m = re.match(r"^\$\$(.*)\$\$$", body, re.S)
        return "$$\n" + (m.group(1).strip() if m else body) + "\n$$"
    if el.name == "div" and "box" in cls:
        kind = next((c for c in cls if c in ALERT), None)
        tag = el.find("span", class_="tag")
        label = tag.get_text().strip() if tag else ""
        if tag:
            tag.extract()
        body = "\n\n".join(children_blocks(el))
        head = f"> [!{ALERT[kind]}]\n" if kind else "> "
        if not kind:
            head = "> "
        lines = []
        if label:
            lines.append(f"**{label}**")
        lines.append(body)
        q = "\n\n".join(lines)
        q = "\n".join("> " + l if l.strip() else ">" for l in q.split("\n"))
        return (f"> [!{ALERT[kind]}]\n" if kind else "") + q
    if el.name == "div" and "algo" in cls:
        tit = el.find("div", class_="tit")
        out = []
        if tit:
            out.append(f"**{tit.get_text().strip()}**")
            tit.extract()
        out.extend(children_blocks(el))
        return "\n\n".join(out)
    if el.name == "figure":
        svg = el.find("svg")
        cap = el.find("figcaption")
        name = el.get("data-fig")
        md = f"![{name or 'figura'}]({FIGDIR}/{name}.svg)" if name else ""
        if cap:
            b = cap.find("b")
            if b:
                lead = b.get_text().strip()
                b.extract()
                rest = inline(cap).strip()
                md += f"\n\n**{lead}** *{rest}*"
            else:
                md += "\n\n*" + inline(cap).strip() + "*"
        return md
    if el.name == "nav" or el.name == "header":
        return ""
    return inline(el).strip()


def main():
    raw = open(SRC, encoding="utf-8").read()
    # marcar figuras antes de que se inserten los svg
    raw = re.sub(r"<figure>\s*\{\{([a-z0-9_]+)\}\}", r'<figure data-fig="\1">', raw)
    soup = BeautifulSoup(raw, "html.parser")

    out = []
    out.append("# El perceptrón simple")
    out.append("### Material de estudio — Unidad 1: Redes neuronales\n")
    out.append("**Inteligencia Computacional** · Ingeniería en Informática · FICH–UNL\n")
    out.append(
        "De la fisiología de una neurona al primer modelo que aprende solo: suma ponderada, "
        "umbral, frontera de decisión, corrección de error y descenso por gradiente — hasta "
        "chocar con el XOR.\n")
    out.append(
        "> Construido sobre las clases 001–005 de **Diego Milone** y su presentación "
        "*Perceptrón simple* (60 diapositivas), ampliado con la bibliografía de cátedra: "
        "Haykin, *Neural Networks and Learning Machines* (caps. 1 y 3) · Freeman & Skapura, "
        "*Neural Networks: Algorithms, Applications and Programming Techniques* (cap. 1) · "
        "Kosko, *Neural Networks and Fuzzy Systems* (cap. 2).\n")
    out.append("**📄 [Versión PDF, 46 páginas, lista para imprimir]"
               "(Perceptron-simple-apunte.pdf)**\n")
    out.append("---\n")

    # índice
    nav = soup.find("nav", class_="toc")
    if nav:
        out.append("## Contenido\n")
        for li in nav.find_all("li"):
            num = li.find("span").get_text().strip()
            a = li.find("a")
            txt = a.get_text().strip()
            anchor = re.sub(r"[^\w\s-]", "", f"{num} {txt}".lower()).strip().replace(" ", "-")
            out.append(f"{num}. [{txt}](#{anchor})")
        out.append("\n---\n")

    main_el = soup.find("main")
    skip = True
    for el in main_el.children:
        if not isinstance(el, Tag):
            continue
        if el.name == "h2":
            skip = False
            num = el.find("span", class_="num")
            n = num.get_text().strip() if num else ""
            if num:
                num.extract()
            out.append(f"\n## {n} {el.get_text().strip()}\n")
            continue
        if skip:
            continue
        b = block(el)
        if b:
            out.append(b + "\n")

    md = "\n".join(out)
    def split_display(line):
        m = re.match(r"^((?:> )*)(.*)$", line)
        pre, rest = m.group(1), m.group(2)
        if "$$" not in rest or rest.startswith("$$"):
            return line
        parts = re.split(r"\$\$([^\n]+?)\$\$", rest)
        out = []
        for i, seg in enumerate(parts):
            seg = seg.strip()
            if not seg:
                continue
            out.append("$$ " + seg + " $$" if i % 2 else seg)
        q = pre.rstrip() + (" " if pre else "")
        blank = pre.rstrip() if pre else ""
        return ("\n" + blank + "\n").join(q + o for o in out)

    md = "\n".join(split_display(l) for l in md.split("\n"))
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    md = md.replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    open(DST, "w", encoding="utf-8").write(md)
    print(f"APUNTE.md — {len(md)//1024} KB, {md.count(chr(10))} líneas")


if __name__ == "__main__":
    main()
