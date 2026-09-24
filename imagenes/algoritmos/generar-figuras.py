#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las 24 figuras de algoritmos.pdf.

    python3 imagenes/algoritmos/generar-figuras.py

Escribe los PNG en la carpeta de este mismo script.

Criterios (versión 2):
  * un solo mensaje por figura, dicho en el título;
  * los procesos van como secuencia de pasos numerados (1, 2, 3): es el guion
    para dibujarlo en la pizarra;
  * todo rotulado, sin superposiciones;
  * colores con significado fijo en todo el apunte:
        azul    AZ  entrada, clase +, lo que va hacia adelante
        naranja NA  error, corrección, clase −, lo que está mal
        verde   VE  resultado, lo nuevo, lo que quedó bien
        violeta VI  δ, lo que viaja hacia atrás, giros y vecindad
        gris    GR  lo viejo / neutro
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import (FancyArrowPatch, Polygon, Rectangle, Circle, Ellipse,
                                FancyBboxPatch)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'mathtext.fontset': 'dejavusans',
                     'savefig.dpi': 220, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.06,
                     'figure.facecolor': 'white', 'axes.titlesize': 9.5})

AZ = '#2a78d6'; NA = '#eb6834'; VE = '#1baf7a'; GR = '#52514e'; NE = '#1d1d1b'
CL = '#d4d6d1'; VI = '#6a5aa8'
AZf = '#e3eefb'; NAf = '#fcebe2'; VEf = '#dff4ec'; VIf = '#ebe8f5'; GRf = '#f3f3f0'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
BB = dict(boxstyle='round,pad=0.25', fc='white', ec='none', alpha=0.92)


def save(fig, name):
    fig.savefig(OUT + name); plt.close(fig); print(name)


def arrow(ax, p, q, c, lw=2.0, ls='-', ms=11, z=5, rad=0.0, style='-|>'):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=c, lw=lw,
                                 linestyle=ls, shrinkA=0, shrinkB=0, zorder=z,
                                 connectionstyle=f'arc3,rad={rad}'))


def clean(ax, box=True):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(box); s.set_color(CL); s.set_linewidth(0.8)


def num(ax, k, x=0.035, y=0.965, color=NE):
    """Círculo numerado en la esquina (coordenadas del eje)."""
    ax.text(x, y, str(k), transform=ax.transAxes, fontsize=12, fontweight='bold', color=color,
            ha='left', va='top', zorder=20,
            bbox=dict(boxstyle='circle,pad=0.25', fc='white', ec=color, lw=1.2))


def title(ax, head, sub=None, color=NE):
    t = head if sub is None else head + '\n' + sub
    ax.set_title(t, fontsize=9.5, color=color, loc='left', pad=6, linespacing=1.35)


def suptitle(fig, text, y=1.0, color=NE, size=10.5):
    fig.text(0.01, y, text, fontsize=size, color=color, fontweight='bold', ha='left', va='bottom')


def box(ax, x, y, w, h, fc, ec='none', lw=1.0, r=0.08, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc=fc, ec=ec, lw=lw, zorder=z))


def neuron(ax, x, y, r, label, fc='white', ec=GR, lw=1.6, fs=10, tc=NE, z=4):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=z))
    ax.text(x, y, label, ha='center', va='center', fontsize=fs, color=tc, zorder=z + 1)


# =========================================================== 1 · PERCEPTRÓN
# 01 · la regla de corrección como secuencia de tres pasos
L = 2.6

def halfplanes(ax, w):
    n = w / np.linalg.norm(w); t = np.array([-n[1], n[0]]); big = 10
    ax.add_patch(Polygon([t * big, t * big + n * big, -t * big + n * big, -t * big], color=AZf, zorder=0, lw=0))
    ax.add_patch(Polygon([t * big, t * big - n * big, -t * big - n * big, -t * big], color=NAf, zorder=0, lw=0))

def line(ax, w, c, ls='-', lw=2.2, z=3):
    n = w / np.linalg.norm(w); t = np.array([-n[1], n[0]])
    ax.plot([-t[0] * 5, t[0] * 5], [-t[1] * 5, t[1] * 5], color=c, ls=ls, lw=lw, zorder=z)

def frame01(ax, head, sub, k):
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect('equal'); clean(ax)
    ax.axhline(0, color='white', lw=0.8, zorder=1); ax.axvline(0, color='white', lw=0.8, zorder=1)
    num(ax, k); title(ax, head, sub)

w0 = np.array([1.5, -0.8]); x = np.array([0.6, 1.8]); step = 0.62 * x; w1 = w0 + step
fig, axs = plt.subplots(1, 3, figsize=(8.4, 3.35)); plt.subplots_adjust(wspace=0.08)
ax = axs[0]; frame01(ax, 'Antes', 'x cae del lado equivocado', 1)
halfplanes(ax, w0); line(ax, w0, NE)
arrow(ax, (0, 0), tuple(w0), GR, 2.4); ax.text(w0[0] - 0.05, w0[1] - 0.38, r'$\mathbf{w}(n)$', color=GR, fontsize=10, ha='center')
ax.plot(*x, 'o', ms=10, color=AZ, mec='white', mew=1.5, zorder=8)
ax.text(x[0] + 0.24, x[1] + 0.02, 'x (clase +)', color=AZ, fontsize=8.5, va='center', fontweight='bold')
ax.text(-1.9, 1.4, 'lado −', color=NA, fontsize=9, fontweight='bold', va='center')
ax.text(1.45, -2.2, 'lado +', color=AZ, fontsize=9, fontweight='bold', va='center')
ax.text(-2.4, -1.8, r'$d=+1,\ y=-1 \Rightarrow e=+2$', color=NE, fontsize=8.5, bbox=BB, zorder=9)
ax.text(-2.4, -2.35, r'$\langle\mathbf{w},\mathbf{x}\rangle<0 \Rightarrow y=-1$', color=NA, fontsize=8.5, bbox=BB, zorder=9)
ax = axs[1]; frame01(ax, 'Corrección', 'se le suma un trozo de x', 2); ax.set_facecolor('#fafaf8')
arrow(ax, (0, 0), tuple(x), AZ, 1.3, ls=(0, (3, 2)))
ax.plot(*x, 'o', ms=10, color=AZ, mec='white', mew=1.5, zorder=8); ax.text(x[0] - 0.25, x[1] + 0.05, 'x', color=AZ, fontsize=10, ha='right', fontweight='bold')
arrow(ax, (0, 0), tuple(w0), GR, 2.4); ax.text(w0[0] + 0.05, w0[1] - 0.38, r'$\mathbf{w}(n)$', color=GR, fontsize=10, ha='center')
arrow(ax, tuple(w0), tuple(w1), NA, 2.4)
ax.text(w0[0] + step[0] / 2 + 0.15, w0[1] + step[1] / 2 - 0.25, r'$+\frac{\eta}{2}\,e\,\mathbf{x}$', color=NA, fontsize=11)
arrow(ax, (0, 0), tuple(w1), VE, 2.8, z=6); ax.text(w1[0] - 0.55, w1[1] + 0.3, r'$\mathbf{w}(n+1)$', color=VE, fontsize=10, ha='center', fontweight='bold')
ax.text(-2.4, -1.95, 'la corrección es paralela a x:\nw se inclina hacia el patrón', color=NE, fontsize=8.3, va='top')
ax = axs[2]; frame01(ax, 'Después', 'la recta giró y x quedó bien', 3)
halfplanes(ax, w1); line(ax, w0, GR, ls=(0, (4, 3)), lw=1.3); line(ax, w1, NE)
arrow(ax, (0, 0), tuple(w1), VE, 2.8); ax.text(w1[0] - 0.1, w1[1] + 0.3, r'$\mathbf{w}(n+1)$', color=VE, fontsize=10, ha='center', fontweight='bold')
ax.plot(*x, 'o', ms=10, color=AZ, mec='white', mew=1.5, zorder=8)
ax.text(x[0] - 0.22, x[1] + 0.02, 'x', color=AZ, fontsize=10, va='center', ha='right', fontweight='bold')
def ang(w): n = w / np.linalg.norm(w); return np.arctan2(n[0], -n[1])
a0, a1 = ang(w0) + np.pi, ang(w1) + np.pi; r = 1.7
arrow(ax, (r * np.cos(a0), r * np.sin(a0)), (r * np.cos(a1), r * np.sin(a1)), VI, 1.8, rad=-0.3, z=7)
ax.text(0.55, -1.45, 'la recta\ngiró', color=VI, fontsize=8.3, fontweight='bold')
ax.text(-2.4, -2.35, r'$\langle\mathbf{w},\mathbf{x}\rangle>0 \Rightarrow y=+1$ ✓', color=AZ, fontsize=8.5, bbox=BB, zorder=9)
fig.text(0.125, 0.06, 'Si x ya estaba del lado correcto:  e = 0  →  no se toca nada.     '
         '(Umbral omitido para poder dibujar en 2D.)', fontsize=8.5, color=GR)
save(fig, '01-frontera-y-giro.png')

# 02 · XOR: ninguna recta alcanza; dos rectas sí
pts = [(-1, -1, -1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3)); plt.subplots_adjust(wspace=0.12)
for k, ax in enumerate(axs):
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.9, 1.9); ax.set_aspect('equal'); clean(ax)
    ax.axhline(0, color=CL, lw=0.7, zorder=0); ax.axvline(0, color=CL, lw=0.7, zorder=0)
    if k == 1:
        xs = np.linspace(-2, 2, 2)
        ax.fill_between(xs, -xs - 1.0, -xs + 1.0, color=AZf, zorder=0)
        ax.fill_between(xs, -xs + 1.0, 3, color=NAf, zorder=0); ax.fill_between(xs, -3, -xs - 1.0, color=NAf, zorder=0)
        ax.plot(xs, -xs + 1.0, color=NE, lw=2); ax.plot(xs, -xs - 1.0, color=NE, lw=2)
        ax.text(0.12, 0.12, 'clase +', color=AZ, fontsize=8.5, fontweight='bold', rotation=-45, ha='center', va='center')
        ax.text(1.25, 1.55, 'clase −', color=NA, fontsize=8.5, fontweight='bold', ha='center', bbox=BB)
        ax.text(-1.25, -1.65, 'clase −', color=NA, fontsize=8.5, fontweight='bold', ha='center', bbox=BB)
        num(ax, 2, color=VE); title(ax, 'Con dos rectas, sí', 'una capa oculta de 2 neuronas: la franja')
    else:
        for (m, b, bad) in [(1.1, -0.35, '1 mal'), (-1.1, 0.3, '1 mal'), (0.15, -0.95, '1 mal')]:
            xs = np.linspace(-1.9, 1.9, 2); ax.plot(xs, m * xs + b, color=GR, lw=1.1, ls=(0, (4, 3)))
        ax.text(0, -1.72, 'toda recta deja al menos un punto mal', color=NA, fontsize=8.2, ha='center', bbox=BB)
        num(ax, 1, color=NA); title(ax, 'Con una recta, no', 'el perceptrón simple oscila para siempre')
    for (px, py, d) in pts:
        ax.plot(px, py, 'o', ms=13, color=AZ if d > 0 else NA, mec='white', mew=1.5, zorder=6)
        ax.text(px, py, '+' if d > 0 else '−', color='white', fontsize=10, fontweight='bold', ha='center', va='center', zorder=7)
save(fig, '02-xor.png')

# ==================================================================== 2 · LMS
# 03 · el gradiente apunta cuesta arriba, y el tamaño del paso
fig, axs = plt.subplots(1, 3, figsize=(8.4, 2.9)); plt.subplots_adjust(wspace=0.1)
t = np.linspace(-1.05, 1.05, 200)
for k, ax in enumerate(axs):
    clean(ax); ax.plot(t, t ** 2, color=NE, lw=1.8, zorder=2); ax.set_xlim(-1.1, 1.1); ax.set_ylim(-0.2, 1.25)
    ax.plot(0, 0, 'o', ms=7, color=VE, zorder=6)
    ax.set_xlabel('peso w', fontsize=8.5, color=GR, labelpad=2)
    if k == 0: ax.set_ylabel(r'error $e^2$', fontsize=8.5, color=GR, labelpad=2)
p = -0.5; s = 2 * p; ax = axs[0]
ax.plot([p - 0.33, p + 0.33], [p ** 2 - s * 0.33, p ** 2 + s * 0.33], color=GR, lw=1, ls=':', zorder=3)
arrow(ax, (p, p ** 2), (p - 0.3, p ** 2 - s * 0.3), NA, 2.2)
ax.text(p - 0.22, p ** 2 - s * 0.3 + 0.05, r'$\nabla e^2$ (cuesta arriba)', color=NA, fontsize=8.3, ha='left', va='bottom')
arrow(ax, (p, p ** 2), (p + 0.45, p ** 2), VE, 2.2)
ax.text(p + 0.5, p ** 2 + 0.03, r'$-\mu\nabla e^2$', color=VE, fontsize=9, va='bottom')
ax.plot(p, p ** 2, 'o', ms=8, color=NE, zorder=7)
ax.text(0.05, 0.07, 'mínimo', color=VE, fontsize=8.3)
num(ax, 1); title(ax, 'Por qué el menos', 'el gradiente sube; se va al revés')
for k, (mu, c, h, sub) in enumerate([(0.14, AZ, r'$\mu$ chico', 'converge, pero lento'),
                                      (0.93, NA, r'$\mu$ grande', 'rebota de un lado al otro')]):
    ax = axs[k + 1]; p = -0.9; P = [p]
    for _ in range(7): p = p - mu * 2 * p; P.append(p)
    P = np.array(P)
    for i in range(len(P) - 1):
        arrow(ax, (P[i], P[i] ** 2), (P[i + 1], P[i + 1] ** 2), c, 1.4, ms=9, z=4)
    ax.plot(P, P ** 2, 'o', color=c, ms=5, zorder=5)
    ax.text(P[0] + 0.1, P[0] ** 2 + 0.02, 'inicio', color=GR, fontsize=8, ha='left')
    num(ax, k + 2); title(ax, h, sub)
save(fig, '03-gradiente.png')

# ============================================================ 3 · MULTICAPA
# 04 · ida por fila, vuelta por columna
fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.1)); plt.subplots_adjust(wspace=0.18)
def mat(ax, hi, kind, col, colf):
    clean(ax, False); ax.set_xlim(-1.3, 4.6); ax.set_ylim(3.35, -0.75)
    for i in range(3):
        for j in range(4):
            on = (kind == 'row' and i == hi) or (kind == 'col' and j == hi)
            fc = col if on else (GRf if j else '#e9e9e4')
            ax.add_patch(Rectangle((j, i), 1, 1, fc=fc, ec='white', lw=2))
            ax.text(j + .5, i + .52, r'$w_{%d%d}$' % (i + 1, j), ha='center', va='center', fontsize=9.5,
                    color='white' if on else GR)
    for j in range(4): ax.text(j + .5, -0.25, 'j=%d' % j if j else 'sesgo', ha='center', fontsize=8, color=GR)
    for i in range(3): ax.text(-0.15, i + .5, 'k=%d' % (i + 1), ha='right', va='center', fontsize=8, color=GR)
mat(axs[0], 1, 'row', AZ, AZf)
title(axs[0], 'IDA: la neurona k usa su FILA', r'$v_k=\sum_j w_{kj}\,y_j$   (lo que le ENTRA a k)', AZ)
mat(axs[1], 2, 'col', VI, VIf)
title(axs[1], 'VUELTA: la neurona j usa su COLUMNA', r'$\sum_k \delta_k\,w_{kj}$   (lo que SALE de j)', VI)
fig.text(0.5, 0.02, r'La misma matriz $\mathbf{W}^{(p+1)}$: filas = neurona que RECIBE ($k$), columnas = neurona que ENVÍA ($j$). Ida por filas, vuelta por columnas = transpuesta.', ha='center', fontsize=8.3, color=GR)
save(fig, '04-fila-columna.png')

# 05 · sigmoide simétrica y su derivada
fig, axs = plt.subplots(1, 2, figsize=(8.2, 2.9)); plt.subplots_adjust(wspace=0.16)
v = np.linspace(-6, 6, 400); y = 2 / (1 + np.exp(-v)) - 1; dy = 0.5 * (1 + y) * (1 - y)
for k, (ax, dat, c) in enumerate([(axs[0], y, AZ), (axs[1], dy, NA)]):
    clean(ax); ax.set_xlim(-6, 6)
    ax.axvspan(-6, -3, color=GRf, zorder=0); ax.axvspan(3, 6, color=GRf, zorder=0)
    ax.axhline(0, color=CL, lw=0.8); ax.axvline(0, color=CL, lw=0.8)
    ax.plot(v, dat, color=c, lw=2.4, zorder=3)
    ax.set_xlabel('campo local v', fontsize=8.5, color=GR, labelpad=2)
ax = axs[0]; ax.set_ylim(-1.3, 1.3)
for yy in (-1, 1): ax.axhline(yy, color=GR, lw=0.8, ls=':')
ax.text(5.8, 0.87, '+1', color=GR, fontsize=8, ha='right'); ax.text(-5.8, -0.93, '−1', color=GR, fontsize=8)
ax.text(-4.5, 0.35, 'saturada', color=GR, fontsize=8.3, ha='center'); ax.text(4.5, -0.45, 'saturada', color=GR, fontsize=8.3, ha='center')
num(ax, 1, color=AZ); title(ax, r'$\varphi(v)=\frac{2}{1+e^{-v}}-1$', 'simétrica: salidas centradas en 0', AZ)
ax = axs[1]; ax.set_ylim(-0.05, 0.62)
ax.plot(0, 0.5, 'o', color=NA, ms=6, zorder=5); ax.text(0.3, 0.52, 'máximo: 0,5 en v = 0', color=NA, fontsize=8.3)
ax.text(-4.5, 0.2, r"$\varphi'\approx 0$", color=GR, fontsize=9, ha='center')
ax.text(-4.5, 0.12, r'$\Rightarrow\ \delta\approx 0$' + '\nno aprende', color=GR, fontsize=8.3, ha='center', va='top')
num(ax, 2, color=NA); title(ax, r"$\varphi'(v)=\frac{1}{2}(1+y)(1-y)$", 'se calcula con la salida y, que ya está', NA)
save(fig, '05-sigmoide.png')

# 06 · la cadena y el corte del delta
fig, ax = plt.subplots(figsize=(8.2, 2.7)); clean(ax, False); ax.set_xlim(0, 20); ax.set_ylim(-0.4, 6.2)
items = [(r'$w_{ji}$', 'peso'), (r'$v_j$', 'campo local'), (r'$y_j$', 'salida'), (r'$e_j$', 'error'), (r'$\xi$', 'error total')]
xs = [1.6, 5.6, 9.6, 13.6, 17.6]
for i, ((s_, lab), xc) in enumerate(zip(items, xs)):
    inside = 1 <= i <= 3
    box(ax, xc - 1.0, 2.9, 2.0, 1.2, VIf if inside else GRf, ec=VI if inside else CL, lw=1.2)
    ax.text(xc, 3.5, s_, ha='center', va='center', fontsize=14)
    ax.text(xc, 2.55, lab, ha='center', va='top', fontsize=8.3, color=GR)
ders = [r'$\frac{\partial v_j}{\partial w_{ji}}=y_i$', r"$\frac{\partial y_j}{\partial v_j}=\varphi'$",
        r'$\frac{\partial e_j}{\partial y_j}=-1$', r'$\frac{\partial \xi}{\partial e_j}=e_j$']
for i in range(4):
    arrow(ax, (xs[i] + 1.05, 3.5), (xs[i + 1] - 1.05, 3.5), GR, 1.4, ms=9)
    ax.text((xs[i] + xs[i + 1]) / 2, 4.35, ders[i], ha='center', va='bottom', fontsize=10.5,
            color=NA if i == 0 else VI)
# llaves
ax.plot([2.4, 2.4, 4.8, 4.8], [5.85, 6.0, 6.0, 5.85], color=NA, lw=1.4)
ax.text(3.6, 6.1, 'CONEXIÓN', color=NA, fontsize=8.5, ha='center', va='bottom', fontweight='bold')
ax.plot([6.4, 6.4, 16.8, 16.8], [5.85, 6.0, 6.0, 5.85], color=VI, lw=1.4)
ax.text(11.6, 6.1, r'adentro de la NEURONA  →  se agrupa en  $\delta_j=-\partial\xi/\partial v_j$',
        color=VI, fontsize=8.5, ha='center', va='bottom', fontweight='bold')
ax.text(10, 0.6, r'$\frac{\partial\xi}{\partial w_{ji}}=-\,\delta_j\,y_i$   $\Longrightarrow$   $\Delta w_{ji}=\mu\,\delta_j\,y_i$',
        ha='center', fontsize=13, color=NE)
ax.text(10, -0.35, 'el δ se calcula UNA vez por neurona y sirve para todos los pesos que le entran',
        ha='center', fontsize=8.5, color=GR)
save(fig, '06-cadena-delta.png')

# 07 · los dos deltas
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.2)); plt.subplots_adjust(wspace=0.08)
for ax in axs: clean(ax); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.set_aspect('equal')
ax = axs[0]; num(ax, 1, color=VE); title(ax, 'Capa de SALIDA', 'hay salida deseada: el error se mide')
neuron(ax, 2.2, 3.3, 0.8, r'$y_j$', ec=GR, fs=12)
arrow(ax, (3.05, 3.3), (5.4, 3.3), GR, 1.6)
neuron(ax, 6.0, 3.3, 0.55, '−', fc=NAf, ec=NA, fs=14, tc=NA)
ax.text(6.0, 5.55, r'$d_j$', ha='center', va='center', fontsize=12, color=VE)
arrow(ax, (6.0, 5.2), (6.0, 3.9), VE, 1.6)
arrow(ax, (6.6, 3.3), (8.2, 3.3), NA, 1.8)
ax.text(8.35, 3.3, r'$e_j$', va='center', fontsize=13, color=NA)
ax.text(5.0, 1.15, r"$\delta_j = e_j\;\varphi'(v_j)$", ha='center', fontsize=14, color=VI, bbox=dict(boxstyle='round,pad=0.35', fc=VIf, ec='none'))
ax = axs[1]; num(ax, 2, color=VI); title(ax, 'Capa OCULTA', 'no hay salida deseada: el error se pide prestado')
neuron(ax, 2.2, 3.3, 0.8, r'$j$', ec=VI, fs=13, lw=2)
for i, yy in enumerate([5.0, 3.3, 1.6]):
    neuron(ax, 8.2, yy, 0.62, r'$\delta_{%d}$' % (i + 1), fc=VI, ec=VI, fs=11, tc='white')
    arrow(ax, (7.55, yy), (3.05, 3.3 + (yy - 3.3) * 0.25), VI, 1.5, ms=10)
    ax.text(5.3, 3.3 + (yy - 3.3) * 0.62 + 0.18, r'$w_{%dj}$' % (i + 1), fontsize=10, color=GR, ha='center',
            bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))
ax.text(8.2, 5.85, 'capa siguiente', ha='center', fontsize=8.3, color=GR)
ax.text(4.6, 0.6, r"$\delta_j = \left[\sum_k \delta_k\,w_{kj}\right]\,\varphi'(v_j)$", ha='center', fontsize=12.5, color=VI,
        bbox=dict(boxstyle='round,pad=0.35', fc=VIf, ec='none'))
fig.text(0.5, 0.0, 'Lo único que cambia entre las dos: el corchete ocupa el lugar de $e_j$. El resto de la fórmula es idéntico.',
         ha='center', fontsize=8.6, color=GR)
save(fig, '07-dos-deltas.png')

# 08 · los dos bordes de la fórmula general
fig, ax = plt.subplots(figsize=(8.4, 3.3)); clean(ax, False); ax.set_xlim(0, 21); ax.set_ylim(-1.3, 10.0)
cols = [(1.2, 'x', 'entrada\nde la red', AZ), (5.6, 'I', 'primera\ncapa', NE), (10.5, 'II', 'capa\ncualquiera', NE),
        (15.4, 'III', 'capa de\nsalida', NE)]
for xc, lab, sub, c in cols:
    if lab == 'x':
        for yy in (3.0, 4.2, 5.4): neuron(ax, xc, yy, 0.38, '', fc=AZf, ec=AZ, lw=1.4)
    else:
        box(ax, xc - 1.3, 2.3, 2.6, 3.8, GRf, ec=CL)
        for yy in (3.0, 4.2, 5.4): neuron(ax, xc, yy, 0.42, '', fc='white', ec=GR, lw=1.4)
        ax.text(xc, 6.5, lab, ha='center', fontsize=12, fontweight='bold', color=NE)
    ax.text(xc, 1.9, sub, ha='center', va='top', fontsize=8.3, color=GR)
for a, b in [(1.2, 5.6), (5.6, 10.5), (10.5, 15.4)]:
    arrow(ax, (a + 0.6 if a < 2 else a + 1.4, 4.2), (b - 1.4, 4.2), GR, 1.5)
arrow(ax, (16.8, 4.2), (18.4, 4.2), GR, 1.5)
ax.text(18.6, 4.2, r'$y$  vs  $d$', va='center', fontsize=11, color=VE)
# rótulos de los bordes
ax.text(10.5, 9.4, r'fórmula general:   $\Delta w^{(p)}_{ji}=\eta\,\langle\boldsymbol{\delta}^{(p+1)},\mathbf{w}^{(p+1)}_j\rangle\,(1+y^{(p)}_j)(1-y^{(p)}_j)\,y^{(p-1)}_i$', ha='center', fontsize=10.5, color=NE)
ax.text(5.6, 8.3, r'falta $p-1$:', ha='center', fontsize=9, color=AZ, fontweight='bold')
ax.text(5.6, 7.7, r'$y^{(p-1)}_i$ es $x_i$', ha='center', fontsize=9, color=AZ)
ax.text(10.5, 8.3, 'la fórmula', ha='center', fontsize=9, color=NE, fontweight='bold')
ax.text(10.5, 7.7, 'tal cual', ha='center', fontsize=9, color=NE)
ax.text(15.4, 8.3, r'falta $p+1$:', ha='center', fontsize=9, color=VE, fontweight='bold')
ax.text(15.4, 7.7, r'el corchete es $e_j$', ha='center', fontsize=9, color=VE)
arrow(ax, (15.4, -0.9), (5.6, -0.9), VI, 2.0)
ax.text(10.5, -0.65, r'orden de cálculo de los $\delta$:  III $\rightarrow$ II $\rightarrow$ I  (de la salida hacia atrás)',
        ha='center', fontsize=9, color=VI, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'))
save(fig, '08-bordes.png')

# ============================================================ 4 · BASE RADIAL
# 09 · semiplano contra burbuja
fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.4)); plt.subplots_adjust(wspace=0.08)
X, Y = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-3, 3, 300))
from matplotlib.colors import LinearSegmentedColormap
cmA = LinearSegmentedColormap.from_list('a', ['#ffffff', AZ]); cmV = LinearSegmentedColormap.from_list('v', ['#ffffff', VE])
ax = axs[0]; clean(ax); ax.set_aspect('equal')
Z = 1 / (1 + np.exp(-2.2 * (0.8 * X + 0.5 * Y)))
ax.contourf(X, Y, Z, levels=14, cmap=cmA, alpha=0.9); ax.contour(X, Y, Z, levels=[0.5], colors=NE, linewidths=2)
arrow(ax, (0, 0), (0.8 * 1.4, 0.5 * 1.4), NE, 2); ax.text(1.25, 0.75, r'$\mathbf{w}$', fontsize=11)
ax.text(2.05, -1.7, 'responde\n(salida alta)', color='white', fontsize=8.5, fontweight='bold', ha='center')
ax.text(-1.7, 1.8, 'no responde', color=GR, fontsize=8.5, ha='center')
ax.text(-2.1, -1.2, 'frontera =\nrecta', color=NE, fontsize=8.3, rotation=0)
num(ax, 1, color=AZ); title(ax, 'Sigmoide: global', 'se enciende en TODO un semiplano', AZ)
ax = axs[1]; clean(ax); ax.set_aspect('equal')
cs = [(-1.3, 1.1, .7), (1.2, 0.9, .55), (0.2, -1.4, .8)]
Z = sum(np.exp(-((X - a) ** 2 + (Y - b) ** 2) / (2 * s ** 2)) for a, b, s in cs)
ax.contourf(X, Y, Z, levels=14, cmap=cmV, alpha=0.9)
for i, (a, b, s_) in enumerate(cs):
    ax.plot(a, b, 'x', color=NE, ms=8, mew=2)
    ax.text(a + 0.12, b + 0.12, r'$\boldsymbol{\mu}_%d$' % (i + 1), fontsize=10)
    ax.add_patch(Circle((a, b), s_, fill=False, ec=NE, lw=1, ls=(0, (3, 2))))
a, b, s_ = cs[2]; ax.plot([a, a + s_], [b, b], color=NE, lw=1.2); ax.text(a + s_ / 2, b - 0.32, r'$\sigma_3$', fontsize=10, ha='center')
ax.text(2.0, -2.5, 'lejos de todo:\nnadie responde', color=GR, fontsize=8.3, ha='center')
num(ax, 2, color=VE); title(ax, 'Radial: local', 'se enciende sólo CERCA de su centro', VE)
save(fig, '09-local-vs-global.png')

# 10 · k-medias en pasos
P = np.array([[1.2, 1.5], [1.6, 2.1], [0.9, 2.4], [1.9, 1.2], [1.3, 1.9], [2.2, 2.6],
              [5.4, 1.7], [6.1, 2.3], [5.8, 1.1], [6.4, 1.8], [5.9, 2.6], [4.9, 2.4]])
mu0 = np.array([[3.3, 3.3], [4.3, 0.5]])
d = np.linalg.norm(P[:, None, :] - mu0[None, :, :], axis=2); a = d.argmin(1)
mu1 = np.array([P[a == j].mean(0) for j in range(2)])
fig, axs = plt.subplots(1, 3, figsize=(8.6, 3.0)); plt.subplots_adjust(wspace=0.08)
CC = [AZ, NA]
for k, ax in enumerate(axs):
    clean(ax); ax.set_xlim(0.2, 7.0); ax.set_ylim(0, 3.9)
    for i, p in enumerate(P):
        c = GR if k == 0 else CC[a[i]]
        if k == 1: ax.plot([p[0], mu0[a[i]][0]], [p[1], mu0[a[i]][1]], color=c, lw=0.8, alpha=0.5, zorder=1)
        ax.plot(*p, 'o', ms=7, color=c, mec='white', mew=1, zorder=3)
    if k < 2:
        for j in range(2):
            ax.plot(*mu0[j], 'X', ms=13, color=GR if k == 0 else CC[j], mec='white', mew=1.2, zorder=5)
            ax.text(mu0[j][0] + 0.25, mu0[j][1] + 0.12, r'$\boldsymbol{\mu}_%d$' % (j + 1), fontsize=10, color=GR if k == 0 else CC[j])
    else:
        for j in range(2):
            ax.plot(*mu0[j], 'X', ms=11, color='white', mec=CC[j], mew=1.2, zorder=4)
            arrow(ax, tuple(mu0[j]), tuple(mu1[j]), CC[j], 1.8, ls=(0, (3, 2)), z=5)
            ax.plot(*mu1[j], 'X', ms=13, color=CC[j], mec='white', mew=1.2, zorder=6)
            ax.text(mu1[j][0] + 0.15, mu1[j][1] - 0.45, 'promedio', fontsize=8, color=CC[j], ha='center')
if True:
    num(axs[0], 1); title(axs[0], 'Arranque', 'centros al azar; datos sin grupo')
    num(axs[1], 2); title(axs[1], 'Asignar', 'cada dato al centro más cercano')
    num(axs[2], 3); title(axs[2], 'Recalcular', 'cada centro salta al promedio')
fig.text(0.5, -0.02, 'Los datos nunca se mueven (en 2 sólo cambian de color).  Se repiten 2 y 3 hasta que ningún dato cambie de grupo.', ha='center', fontsize=9, color=NE, fontweight='bold')
save(fig, '10-kmedias.png')

# 11 · la salida es una suma pesada de campanas
fig, ax = plt.subplots(figsize=(7.6, 3.0)); clean(ax)
xx = np.linspace(-4, 6, 500); cs = [(-2.2, 0.8, 0.9, AZ), (0.3, 0.7, -0.6, NA), (3.0, 0.9, 0.5, VE)]
tot = np.zeros_like(xx)
for c, s_, w, col in cs:
    ph = np.exp(-(xx - c) ** 2 / (2 * s_ ** 2)); tot += w * ph
    ax.plot(xx, ph, color=col, lw=1, alpha=0.35)
    ax.fill_between(xx, 0, w * ph, color=col, alpha=0.18)
    ax.plot(xx, w * ph, color=col, lw=1.6, ls=(0, (4, 2)))
    ax.text(c + 0.95 * s_ + 0.15, w * 0.62, r'$w=%.1f$' % w, color=col, fontsize=10, ha='left', fontweight='bold', va='center', bbox=BB, zorder=8)
ax.plot(xx, tot, color=NE, lw=2.6, zorder=5)
ax.axhline(0, color=CL, lw=1)
ax.text(5.9, 1.0, r'negro:  $y=\sum_j w_{j}\,\varphi_j(x)$', fontsize=11, ha='right', color=NE)
ax.set_ylim(-0.85, 1.2); ax.set_xlim(-4, 6)
title(ax, 'La salida es una suma de campanas pesadas',
      r'cambiar un $w_{kj}$ sólo sube, baja o da vuelta SU campana (línea fina: la campana sin pesar)')
save(fig, '11-combinacion.png')

# 12 · de círculos a elipses: la matriz de covarianza
fig, axs = plt.subplots(1, 3, figsize=(8.4, 3.2)); plt.subplots_adjust(wspace=0.08)
specs = [('σ escalar', 'círculo: 1 parámetro', 1.0, 1.0, 0, r'$\sigma^2\,\mathbf{I}$'),
         ('Diagonal', 'elipse alineada: d parámetros', 1.5, 0.7, 0, r'$\mathrm{diag}(\sigma_1^2,\sigma_2^2)$'),
         ('Completa', 'elipse rotada: d(d+1)/2', 1.6, 0.6, 35, '')]
for k, (ax, (h, sub, a_, b_, th, M)) in enumerate(zip(axs, specs)):
    clean(ax); ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.6, 2.2); ax.set_aspect('equal')
    for f, al in [(1.8, 0.12), (1.2, 0.2), (0.6, 0.35)]:
        ax.add_patch(Ellipse((0, 0), 2 * a_ * f / 1.2, 2 * b_ * f / 1.2, angle=th, fc=VI, alpha=al, ec='none'))
    ax.add_patch(Ellipse((0, 0), 2 * a_, 2 * b_, angle=th, fill=False, ec=VI, lw=1.6))
    ax.plot(0, 0, 'x', color=NE, ms=8, mew=2)
    ax.text(0, -2.15, M if k < 2 else '', ha='center', fontsize=10.5, color=NE)
    num(ax, k + 1, color=VI); title(ax, h, sub)
axs[2].text(0, -2.15, r'$\sigma_{12}\neq 0$: el término cruzado la ROTA', ha='center', fontsize=8.5, color=NA, fontweight='bold')
axs[2].text(1.35, 1.55, r'$\mathbf{\Sigma}_j$ completa', fontsize=8.5, color=VI, ha='center')
save(fig, '12-covarianza.png')

# =============================================================== 5 · HOPFIELD
# 13 · dos fases que no se mezclan; la recuperación como lazo
fig, ax = plt.subplots(figsize=(8.6, 3.9)); clean(ax, False); ax.set_xlim(0, 22); ax.set_ylim(0, 10)
box(ax, 0.2, 1.4, 7.4, 8.2, AZf, ec=AZ, lw=1.4, r=0.3)
ax.text(3.9, 9.0, 'FASE 1 · ALMACENAR', ha='center', fontsize=10.5, fontweight='bold', color=AZ)
ax.text(3.9, 8.35, 'una sola cuenta: no itera', ha='center', fontsize=8.5, color=AZ)
ax.text(3.9, 6.6, r'$w_{ji}=\frac{1}{N}\sum_{k=1}^{P} x^*_{kj}\,x^*_{ki}$', ha='center', fontsize=13)
ax.text(3.9, 5.0, 'coincidencias − diferencias\n(regla de Hebb)', ha='center', fontsize=8.5, color=GR)
ax.text(3.9, 3.35, r'$w_{jj}=0 \qquad w_{ji}=w_{ij}$', ha='center', fontsize=12)
ax.text(3.9, 2.3, 'sin autoconexión · simétrica', ha='center', fontsize=8.5, color=GR)
arrow(ax, (7.8, 5.5), (9.1, 5.5), GR, 2.2)
ax.text(8.45, 6.0, 'W fija', ha='center', fontsize=8, color=GR)
box(ax, 9.3, 1.4, 12.5, 8.2, NAf, ec=NA, lw=1.4, r=0.3)
ax.text(15.55, 9.0, 'FASE 2 · RECUPERAR', ha='center', fontsize=10.5, fontweight='bold', color=NA)
ax.text(15.55, 8.35, 'itera, una neurona por vez', ha='center', fontsize=8.5, color=NA)
steps = [(r'$\mathbf{y}(0)=\mathbf{x}$', 'cargar el patrón sucio'),
         (r'$j^*=\mathrm{rnd}(N)$', 'sortear una neurona'),
         (r'$v_{j^*}=\sum_i w_{j^*i}\,y_i$', 'votación ponderada'),
         (r'$y_{j^*}=\mathrm{sgn}(v_{j^*})$', 'gana la mayoría')]
for i, (f, d_) in enumerate(steps):
    yy = 7.3 - i * 1.45
    ax.text(10.0, yy, str(i + 1), fontsize=10, fontweight='bold', color=NA, ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.2', fc='white', ec=NA))
    ax.text(10.7, yy, f, fontsize=11, va='center')
    ax.text(15.8, yy, d_, fontsize=8.5, va='center', color=GR)
ax.text(10.0, 1.9, '5', fontsize=10, fontweight='bold', color=VE, ha='center', va='center',
        bbox=dict(boxstyle='circle,pad=0.2', fc='white', ec=VE))
ax.text(10.7, 1.9, '¿las N estables?   sí → FIN', fontsize=9.5, va='center', color=VE, fontweight='bold')
ax.plot([18.6, 21.2, 21.2], [1.9, 1.9, 5.85], color=NA, lw=1.8)
arrow(ax, (21.2, 5.85), (20.3, 5.85), NA, 1.8)
ax.text(21.0, 3.9, 'no', fontsize=9, color=NA, fontweight='bold', va='center', ha='right')
save(fig, '13-hopfield-fases.png')

# 14 · la energía nunca sube
fig, ax = plt.subplots(figsize=(8.0, 3.2)); clean(ax)
xx = np.linspace(-0.3, 10.3, 600)
def E(x): return (-1.0 * np.exp(-((x - 1.4) / .55) ** 2) - 0.35 * np.exp(-((x - 3.8) / .45) ** 2)
                  - 1.0 * np.exp(-((x - 6.2) / .55) ** 2) - 0.75 * np.exp(-((x - 8.8) / .5) ** 2) + 0.012 * (x - 5) ** 2)
ax.plot(xx, E(xx), color=NE, lw=2.4)
for xm, lab, c in [(1.4, r'$\mathbf{x}^*_1$' + '\nmemoria', AZ), (3.8, 'espurio\n(mezcla)', NA),
                   (6.2, r'$-\mathbf{x}^*_1$' + '\nespurio (negativo)', NA), (8.8, r'$\mathbf{x}^*_2$' + '\nmemoria', AZ)]:
    ax.plot(xm, E(xm), 'o', ms=10, color=c, mec='white', mew=1.5, zorder=6)
    ax.text(xm, E(xm) - 0.12, lab, ha='center', va='top', fontsize=8.5, color=c, fontweight='bold')
xs_ = [2.75, 2.4, 2.1, 1.85, 1.62, 1.45]
for a_, b_ in zip(xs_[:-1], xs_[1:]):
    arrow(ax, (a_, E(a_) + 0.06), (b_, E(b_) + 0.06), VE, 1.6, ms=9, z=7)
ax.plot(xs_[0], E(xs_[0]) + 0.06, 'o', ms=11, color=VE, mec='white', mew=1.5, zorder=8)
ax.text(xs_[0] + 0.15, E(xs_[0]) + 0.2, 'patrón sucio\n(estado inicial)', fontsize=8.5, color=VE, fontweight='bold')
ax.text(2.55, -0.75, r'$\Delta E\leq 0$' + '\nen cada paso', fontsize=8.5, color=VE, ha='left', va='top')
ax.set_ylabel('energía E', fontsize=9, color=GR); ax.set_xlabel('estados posibles', fontsize=9, color=GR)
ax.set_ylim(-1.55, 0.45)
title(ax, 'La energía nunca sube: la red rueda al mínimo más cercano',
      'por eso recupera la memoria más parecida… y por eso también puede caer en un espurio')
save(fig, '14-energia.png')

# ================================================================== 6 · BPTT
# 15 · la red desenrollada: la misma W en cada flecha
fig, ax = plt.subplots(figsize=(8.6, 3.9)); clean(ax, False); ax.set_xlim(-1.2, 21.5); ax.set_ylim(-1.2, 9.4)
xs = [2.5, 7.5, 12.5, 17.5]; T = len(xs)
ax.text(-0.6, 5.0, r'$\mathbf{y}_{-1}=\mathbf{0}$', fontsize=10, ha='center', va='center', color=GR)
for t, xc in enumerate(xs):
    neuron(ax, xc, 5.0, 0.95, r'$\mathbf{y}_%d$' % t, fc='white', ec=GR, fs=12)
    ax.text(xc, 0.9, r'$\mathbf{x}_%d$' % t, ha='center', fontsize=12, color=AZ)
    arrow(ax, (xc, 1.5), (xc, 3.95), AZ, 1.8)
    ax.text(xc - 0.2, 1.9, r'$\mathbf{W}^{I}$', fontsize=10, color=AZ, ha='right')
    a0 = 0.5 if t == 0 else xs[t - 1] + 1.0
    arrow(ax, (a0, 5.0), (xc - 1.05, 5.0), AZ, 1.8)
    ax.text((a0 + xc - 1.05) / 2, 5.25, r'$\mathbf{W}$', fontsize=11, color=AZ, ha='center', fontweight='bold')
    if t in (1, 3):
        arrow(ax, (xc, 6.0), (xc, 7.3), NA, 1.6)
        ax.text(xc, 7.55, r'$\mathbf{e}_%d$' % t, ha='center', fontsize=12, color=NA)
    else:
        ax.text(xc, 7.55, 'sin $d$', ha='center', fontsize=8.5, color=GR)
    ax.text(xc, -0.3, r'$t=%d$' % t, ha='center', fontsize=9, color=GR)
for t in range(T - 1, 0, -1):
    arrow(ax, (xs[t] - 0.9, 3.55), (xs[t - 1] + 0.9, 3.55), VI, 1.8, rad=-0.25)
    ax.text((xs[t] + xs[t - 1]) / 2, 2.65, r'$\mathbf{W}^{\mathsf{T}}$', fontsize=10, color=VI, ha='center')
ax.text(10.0, 9.0, 'IDA: la MISMA W en todas las flechas (y se guarda todo)', ha='center', fontsize=9.5, color=AZ, fontweight='bold')
ax.text(20.0, 3.4, r'$\boldsymbol{\delta}^*$ vuelve' + '\npor ' + r'$\mathbf{W}^{\mathsf{T}}$', fontsize=9, color=VI, fontweight='bold', va='center')
ax.text(10.0, -1.1, r'$\Delta\mathbf{W}=\sum_t \boldsymbol{\delta}^*_t\,\mathbf{y}^{\mathsf{T}}_{t-1}$:  los aportes de todos los instantes se SUMAN, y W se actualiza al final',
        ha='center', fontsize=9.5, color=NE)
save(fig, '15-bptt.png')

# ================================================================== 7 · SOM
# 16 · dos espacios: la grilla (vecindad) y los datos (competencia)
fig, axs = plt.subplots(1, 2, figsize=(8.6, 4.0)); plt.subplots_adjust(wspace=0.1)
n = 5; G = (1, 2); nb = [(0, 2), (2, 2), (1, 1), (1, 3)]
ax = axs[0]; clean(ax); ax.set_xlim(-0.7, 4.7); ax.set_ylim(-0.7, 4.7); ax.set_aspect('equal')
ax.add_patch(Circle(G, 1.35, fc=VIf, ec=VI, lw=1.2, ls=(0, (4, 2)), zorder=0))
for i in range(n):
    for j in range(n):
        if i < n - 1: ax.plot([i, i + 1], [j, j], color=CL, lw=1.2, zorder=1)
        if j < n - 1: ax.plot([i, i], [j, j + 1], color=CL, lw=1.2, zorder=1)
for i in range(n):
    for j in range(n):
        c = NA if (i, j) == G else (VI if (i, j) in nb else 'white')
        ax.add_patch(Circle((i, j), 0.2, fc=c, ec=GR if c == 'white' else c, lw=1.2, zorder=3))
ax.text(G[0] + 0.25, G[1] + 0.28, 'G', color=NA, fontsize=11, fontweight='bold', zorder=5)
num(ax, 1, color=VI); title(ax, 'GRILLA: acá se mide la VECINDAD', r'violeta: el entorno $\Lambda_G$ (no se deforma nunca)')
ax = axs[1]; clean(ax); ax.set_aspect('equal'); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.5, 5.5)
rng = np.random.default_rng(4)
Wp = {(i, j): np.array([0.35 + 1.1 * i + 0.25 * np.sin(j * 1.3), 0.4 + 1.05 * j + 0.2 * np.cos(i)]) + rng.normal(0, 0.08, 2)
      for i in range(n) for j in range(n)}
Wp[(2, 2)] = np.array([4.3, 1.3])        # vecina en la grilla, lejos en los datos
D = rng.uniform(0, 5, (260, 2)); ax.plot(D[:, 0], D[:, 1], '.', color=CL, ms=3, zorder=0)
for (i, j), p in Wp.items():
    for q in [(i + 1, j), (i, j + 1)]:
        if q in Wp: ax.plot([p[0], Wp[q][0]], [p[1], Wp[q][1]], color=GR, lw=0.9, zorder=1, alpha=0.7)
xin = Wp[G] + np.array([-0.55, 0.45])
for (i, j), p in Wp.items():
    c = NA if (i, j) == G else (VI if (i, j) in nb else 'white')
    ax.add_patch(Circle(p, 0.13, fc=c, ec=GR if c == 'white' else c, lw=1, zorder=3))
    if (i, j) == G or (i, j) in nb:
        tgt = p + 0.45 * (xin - p)
        arrow(ax, tuple(p), tuple(tgt), NA if (i, j) == G else VI, 1.6, ms=9, z=4)
ax.plot(*xin, 'o', ms=11, color=AZ, mec='white', mew=1.5, zorder=6)
ax.text(xin[0] - 0.15, xin[1] + 0.25, 'x', color=AZ, fontsize=12, fontweight='bold', ha='right')
ax.text(Wp[(2, 2)][0] + 0.2, Wp[(2, 2)][1] - 0.55, 'vecina de G en la grilla:\nse mueve aunque esté lejos', color=VI, fontsize=8.3, ha='center', bbox=BB, zorder=9)
num(ax, 2, color=NA); title(ax, 'DATOS: acá se mide la COMPETENCIA', 'gana la más cercana a x; ella y sus vecinas se acercan')
save(fig, '16-som-dos-espacios.png')

# 17 · la vecindad se mide sobre índices
fig, axs = plt.subplots(1, 2, figsize=(8.4, 2.9), sharey=True); plt.subplots_adjust(wspace=0.08)
idx = np.arange(0, 11); Gi = 5; beta = 0.9
hu = np.where(np.abs(idx - Gi) <= 2, beta, 0.0); hg = beta * np.exp(-(idx - Gi) ** 2 / (2 * 1.6 ** 2))
for k, (ax, h, head, sub) in enumerate([(axs[0], hu, 'Uniforme', r'$\beta(n)$ dentro del radio, 0 afuera'),
                                          (axs[1], hg, 'Gaussiana', r'pico $\beta(n)$, ancho $\sigma(n)$')]):
    clean(ax); ax.set_xlim(-0.7, 10.7); ax.set_ylim(-0.25, 1.1)
    for i, hv in zip(idx, h):
        c = NA if i == Gi else (VI if hv > 0.02 else CL)
        ax.plot([i, i], [0, hv], color=c, lw=3, solid_capstyle='butt')
        ax.plot(i, -0.12, 'o', ms=11, color=c if hv > 0.02 else 'white', mec=c if hv > 0.02 else GR, mew=1.2, zorder=3)
    if k == 1:
        xx = np.linspace(0, 10, 200); ax.plot(xx, beta * np.exp(-(xx - Gi) ** 2 / (2 * 1.6 ** 2)), color=VI, lw=1.2, ls=':')
    else:
        ax.plot([Gi - 2, Gi + 2], [1.0, 1.0], color=VI, lw=1.2); ax.text(Gi, 1.02, 'radio 2', ha='center', va='bottom', fontsize=8.3, color=VI)
    ax.text(Gi, beta + 0.03, 'G', ha='center', va='bottom', fontsize=10, color=NA, fontweight='bold') if k == 1 else None
    num(ax, k + 1, color=VI); title(ax, head, sub)
    ax.set_xlabel(r'índice $i$ en la GRILLA (no en los datos):  $|G-i|$', fontsize=8.5, color=GR)
axs[0].set_ylabel(r'$h_{G,i}$', fontsize=10, color=GR)
save(fig, '17-vecindad.png')

# 18 · las tres etapas: η y el entorno se apagan juntos
fig, axs = plt.subplots(2, 1, figsize=(8.0, 3.8), sharex=True); plt.subplots_adjust(hspace=0.12)
ep = np.linspace(0, 5000, 1000)
eta = np.piecewise(ep, [ep < 1000, (ep >= 1000) & (ep < 2000), ep >= 2000],
                   [lambda e: 0.9 - 0.2 * e / 1000, lambda e: 0.7 - 0.6 * (e - 1000) / 1000, 0.1])
lam = np.piecewise(ep, [ep < 1000, (ep >= 1000) & (ep < 2000), ep >= 2000],
                   [5.0, lambda e: 5 - 4 * (e - 1000) / 1000, 0.0])
for ax in axs:
    clean(ax)
    for a_, b_, c in [(0, 1000, AZf), (1000, 2000, VIf), (2000, 5000, VEf)]: ax.axvspan(a_, b_, color=c, zorder=0)
axs[0].plot(ep, eta, color=NA, lw=2.4); axs[0].set_ylim(0, 1.05); axs[0].set_ylabel(r'$\eta(n)$', fontsize=11, color=NA)
for e_, v_, t_ in [(40, 0.9, '0,9'), (1000, 0.7, '0,7'), (2000, 0.1, '0,1')]:
    axs[0].text(e_ + 40, v_ + 0.05, t_, fontsize=8.5, color=NA)
axs[0].text(3500, 0.2, '0,1 → 0,01 (casi constante)', fontsize=8.5, color=NA, ha='center')
axs[1].plot(ep, lam, color=VI, lw=2.4); axs[1].set_ylim(-0.4, 6.0); axs[1].set_ylabel(r'radio $\Lambda_G$', fontsize=10, color=VI)
axs[1].text(500, 5.3, '≈ medio mapa', fontsize=8.5, color=VI, ha='center')
axs[1].text(1500, 3.4, '→ 1, lineal', fontsize=8.5, color=VI, ha='left')
axs[1].text(3500, 0.35, '0: sólo la ganadora', fontsize=8.5, color=VI, ha='center')
for x_, t_, c in [(500, '1 · ORDENAR\n500–1000 ép.', AZ), (1500, '2 · TRANSICIÓN\n≈ 1000 ép.', VI), (3500, '3 · AJUSTE FINO\n≈ 3000 ép.', VE)]:
    axs[0].text(x_, 1.12, t_, ha='center', va='bottom', fontsize=8.2, color=c, fontweight='bold')
axs[1].set_xlabel('épocas  (se corta por cantidad de épocas: no hay error que mirar)', fontsize=8.5, color=GR)
save(fig, '18-etapas.png')

# ================================================================== 8 · LVQ
# 19 · todo LVQ está en el signo (y lo que mueve es la frontera)
def bis(ax, a, b, c, ls='-', lw=2):
    m = (a + b) / 2; d = b - a; t = np.array([-d[1], d[0]]); t = t / np.linalg.norm(t)
    ax.plot([m[0] - 4 * t[0], m[0] + 4 * t[0]], [m[1] - 4 * t[1], m[1] + 4 * t[1]], color=c, ls=ls, lw=lw, zorder=1)
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.5)); plt.subplots_adjust(wspace=0.08)
al = 0.45
for k, ax in enumerate(axs):
    clean(ax); ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.0, 2.0); ax.set_aspect('equal')
    A = np.array([-1.5, 0.0]); B = np.array([1.3, 0.1])
    x_ = np.array([-0.7, 0.8]) if k == 0 else np.array([0.35, 0.75])
    if k == 0:
        A1 = A + al * (x_ - A); bis(ax, A, B, GR, (0, (4, 3)), 1.2); bis(ax, A1, B, NE)
        ax.plot(*A, 's', ms=11, color='white', mec=AZ, mew=1.6, zorder=4); arrow(ax, tuple(A), tuple(A1), VE, 2.2, z=5)
        ax.plot(*A1, 's', ms=12, color=AZ, zorder=6); ax.plot(*B, 's', ms=12, color=NA, zorder=6)
        ax.text(A[0], A[1] - 0.35, r'$\mathbf{m}_c(n)$', ha='center', va='top', fontsize=9, color=AZ)
        ax.text(B[0], B[1] - 0.35, 'otro prototipo\n(no se toca)', ha='center', va='top', fontsize=8.3, color=NA)
        num(ax, 1, color=VE); title(ax, r'Acierta la clase ($s=+1$): se ACERCA', 'el ganador y x son de la misma clase')
    else:
        B1 = B - al * (x_ - B); bis(ax, A, B, GR, (0, (4, 3)), 1.2); bis(ax, A, B1, NE)
        ax.plot(*B, 's', ms=11, color='white', mec=NA, mew=1.6, zorder=4); arrow(ax, tuple(B), tuple(B1), NA, 2.2, z=5)
        ax.plot(*B1, 's', ms=12, color=NA, zorder=6); ax.plot(*A, 's', ms=12, color=AZ, zorder=6)
        ax.text(B[0] + 0.15, B[1] + 0.3, r'$\mathbf{m}_c(n)$', ha='left', fontsize=9, color=NA)
        ax.text(0.2, -1.75, 'la frontera se corrió: x quedó del lado +', ha='center', fontsize=8.5, color=VI, fontweight='bold', bbox=BB)
        num(ax, 2, color=NA); title(ax, r'Se equivoca ($s=-1$): se ALEJA', 'ganó un prototipo de la clase − para un x de clase +')
    ax.plot(*x_, 'o', ms=11, color=AZ, mec='white', mew=1.5, zorder=7)
    ax.text(x_[0], x_[1] + 0.28, 'x (clase +)', ha='center', fontsize=9, color=AZ, fontweight='bold', bbox=BB, zorder=9)
fig.text(0.5, 0.0, r'$\mathbf{m}_c \leftarrow \mathbf{m}_c + s\,\alpha\,(\mathbf{x}-\mathbf{m}_c)$     ·     línea punteada: frontera antes;  línea llena: frontera después     ·     sólo se mueve el ganador',
         ha='center', fontsize=8.8, color=GR)
save(fig, '19-lvq.png')

# ======================================================== 9 · GENERALIZACIÓN
# 20 · parada temprana
fig, ax = plt.subplots(figsize=(7.8, 3.2)); clean(ax)
n_ = np.linspace(0, 10, 300); tr = 0.08 + 0.9 * np.exp(-n_ / 1.9); mo = 0.16 + 0.85 * np.exp(-n_ / 1.9) + 0.012 * n_ ** 2
ns = n_[mo.argmin()]
ax.axvspan(0, ns, color=AZf, zorder=0); ax.axvspan(ns, 10, color=NAf, zorder=0)
ax.plot(n_, tr, color=AZ, lw=2.4, label='entrenamiento'); ax.plot(n_, mo, color=NA, lw=2.4, label='monitoreo')
ax.axvline(ns, color=NE, lw=1.2, ls=(0, (4, 2)))
ax.plot(ns, mo.min(), 'o', ms=10, color=VE, mec='white', mew=1.5, zorder=6)
ax.text(ns + 0.15, mo.min() - 0.1, r'$n^*$: acá se GUARDAN los pesos', fontsize=9, color=VE, fontweight='bold', va='top')
ax.plot([ns, ns + 1.6], [0.95, 0.95], color=VI, lw=1.5); ax.text(ns + 0.8, 0.98, 'paciencia', ha='center', va='bottom', fontsize=8.5, color=VI)
ax.text(ns / 2, 0.02, 'aprende la regla\n(las dos bajan)', ha='center', fontsize=8.5, color=AZ, fontweight='bold')
ax.text((ns + 10) / 2 + 0.3, 0.42, 'memoriza el ruido\n(monitoreo sube)', ha='center', fontsize=8.5, color=NA, fontweight='bold')
ax.text(9.9, tr[-1] + 0.04, 'entrenamiento', ha='right', color=AZ, fontsize=9)
ax.text(7.5, 0.97, 'monitoreo', ha='right', va='center', color=NA, fontsize=9)
ax.set_xlabel('épocas', fontsize=9, color=GR); ax.set_ylabel('error', fontsize=9, color=GR); ax.set_ylim(-0.03, 1.1); ax.set_xlim(0, 10)
title(ax, 'Parada temprana: se corta en el mínimo del MONITOREO, no del entrenamiento')
save(fig, '20-parada-temprana.png')

# 21 · tres conjuntos, un trabajo cada uno, misma proporción de clases
fig, ax = plt.subplots(figsize=(8.4, 3.3)); clean(ax, False); ax.set_xlim(0, 100); ax.set_ylim(-3, 30)
rng = np.random.default_rng(1); lab = rng.permutation(np.r_[np.ones(14), np.zeros(26)])
for i, l in enumerate(lab):
    ax.add_patch(Rectangle((i * 2.5, 22), 2.3, 4, fc=AZ if l else NA, alpha=0.75, ec='none'))
ax.text(0, 27.2, '1 · mezclar el conjunto completo  (35 % clase A, 65 % clase B)', fontsize=9, color=NE, fontweight='bold')
ax.text(0, 17.6, '2 · partir en tres, disjuntos y ESTRATIFICADOS (franja de abajo: la misma proporción en los tres)', fontsize=9, color=NE, fontweight='bold')
parts = [(0, 60, 'ENTRENAMIENTO', '≈ 60 %', 'ajusta los pesos', AZ, AZf),
         (61, 20, 'MONITOREO', '≈ 20 %', 'decide épocas y\narquitectura', VI, VIf),
         (82, 18, 'PRUEBA', '≈ 20 %', 'se mira UNA vez,\nal final', VE, VEf)]
for x0, w, name, pct, job, c, cf in parts:
    ax.add_patch(Rectangle((x0, 8), w, 8, fc=cf, ec=c, lw=1.4))
    ax.add_patch(Rectangle((x0, 8), w * 0.35, 1.6, fc=AZ, alpha=0.75, ec='none'))
    ax.add_patch(Rectangle((x0 + w * 0.35, 8), w * 0.65, 1.6, fc=NA, alpha=0.75, ec='none'))
    ax.text(x0 + w / 2, 13.6, name, ha='center', fontsize=9.5, color=c, fontweight='bold')
    ax.text(x0 + w / 2, 11.2, pct, ha='center', fontsize=8.5, color=c)
    ax.text(x0 + w / 2, 6.8, job, ha='center', va='top', fontsize=8.5, color=GR)
ax.text(50, 0.2, '3 · normalizar con media y desvío del ENTRENAMIENTO, y aplicarlos a los otros dos',
        ha='center', fontsize=9, color=NE, fontweight='bold')
save(fig, '21-particiones.png')

# 22 · validación cruzada k = 5
fig, ax = plt.subplots(figsize=(8.0, 3.3)); clean(ax, False); ax.set_xlim(-3.2, 16); ax.set_ylim(-2.1, 6.4)
errs = [8.0, 10.0, 7.0, 9.0, 6.0]
for r in range(5):
    y0 = 4.6 - r
    ax.text(-0.3, y0 + 0.4, f'vuelta {r + 1}', ha='right', va='center', fontsize=9, color=GR)
    for c in range(5):
        test = (c == r)
        ax.add_patch(Rectangle((c * 1.9, y0), 1.8, 0.8, fc=NA if test else AZf, ec='white', lw=1.5))
        if test: ax.text(c * 1.9 + 0.9, y0 + 0.4, 'prueba', ha='center', va='center', fontsize=8.3, color='white', fontweight='bold')
    ax.text(10.0, y0 + 0.4, '→', ha='center', va='center', fontsize=12, color=GR)
    ax.text(10.6, y0 + 0.4, r'$\varepsilon_%d = %d\,\%%$' % (r + 1, errs[r]), va='center', fontsize=10, color=NA)
for c in range(5): ax.text(c * 1.9 + 0.9, 5.7, r'$\mathcal{F}_%d$' % (c + 1), ha='center', fontsize=10, color=GR)
m = np.mean(errs); sd = np.std(errs)
ax.text(10.6, -0.4, r'$\bar\varepsilon = %.0f\,\%% \pm %.1f\,\%%$' % (m, sd), fontsize=12, color=NE, fontweight='bold')
ax.text(10.6, -1.2, 'media Y desvío, siempre juntos', fontsize=8.5, color=GR)
ax.text(4.6, -0.15, 'cada vuelta REINICIA los pesos\ncada patrón mide 1 vez y entrena k−1', ha='center', va='top', fontsize=8.5, color=VI, fontweight='bold')
ax.add_patch(Rectangle((0, -1.95), 1.0, 0.45, fc=AZf)); ax.text(1.2, -1.73, 'entrenamiento', va='center', fontsize=8.3, color=GR)
ax.add_patch(Rectangle((4.2, -1.95), 1.0, 0.45, fc=NA)); ax.text(5.4, -1.73, 'prueba de esa vuelta', va='center', fontsize=8.3, color=GR)
title(ax, 'Validación cruzada con k = 5: cinco entrenamientos, cada bloque es prueba una sola vez')
save(fig, '22-kfold.png')

# 23 · matriz de confusión: qué mira cada medida
def cm(ax, hl, vals=None, head=True, big=False):
    clean(ax, False); ax.set_xlim(-1.6, 2.1); ax.set_ylim(-0.5, 2.9); ax.invert_yaxis(); ax.set_aspect('equal')
    names = [[r'$t_\oplus$', r'$f_\ominus$'], [r'$f_\oplus$', r'$t_\ominus$']]
    for i in range(2):
        for j in range(2):
            on = hl[i][j]
            ax.add_patch(Rectangle((j, i + 0.4), 1, 1, fc=on if on else GRf, ec='white', lw=2))
            txt = names[i][j] if vals is None else str(vals[i][j])
            ax.text(j + .5, i + .9, txt, ha='center', va='center', fontsize=13 if big else 11,
                    color='white' if on else GR, fontweight='bold' if vals is not None else 'normal')
    if head:
        ax.text(0.5, 0.25, r'dijo $\oplus$', ha='center', fontsize=8.5, color=GR)
        ax.text(1.5, 0.25, r'dijo $\ominus$', ha='center', fontsize=8.5, color=GR)
        ax.text(-0.1, 0.9, r'era $\oplus$', ha='right', va='center', fontsize=8.5, color=GR)
        ax.text(-0.1, 1.9, r'era $\ominus$', ha='right', va='center', fontsize=8.5, color=GR)
fig, axs = plt.subplots(1, 4, figsize=(8.8, 2.9)); plt.subplots_adjust(wspace=0.02)
spec = [('Sensibilidad', r'$s^+=t_\oplus/N_\oplus$', 'de los que ERAN +,\ncuántos agarré', [[AZ, AZ], [0, 0]]),
        ('Especificidad', r'$s^-=t_\ominus/N_\ominus$', 'de los que ERAN −,\ncuántos dejé bien', [[0, 0], [NA, NA]]),
        ('Precisión', r'$p=t_\oplus/(t_\oplus+f_\oplus)$', 'de los que DIJE +,\ncuántos acerté', [[VI, 0], [VI, 0]]),
        ('Exactitud', r'$a=(t_\oplus+t_\ominus)/N$', 'la diagonal\nsobre el total', [[VE, 0], [0, VE]])]
for k, (ax, (h, f, d_, hl)) in enumerate(zip(axs, spec)):
    cm(ax, hl, head=True)
    ax.text(0.5, 2.75, f, ha='center', fontsize=9.5, color=NE)
    ax.text(0.5, 3.0, d_, ha='center', va='top', fontsize=8.3, color=GR)
    ax.set_title(h + ('\n(una FILA)' if k < 2 else '\n(una COLUMNA)' if k == 2 else '\n(la diagonal)'), fontsize=9.5,
                 color=[AZ, NA, VI, VE][k], fontweight='bold', pad=2)
    ax.set_ylim(3.9, -0.1)
fig.text(0.5, 1.04, r'Filas = lo que ERA · columnas = lo que DIJO · el subíndice de $f$ nombra lo que DIJO ($f_\ominus$: dijo −, era +)',
         ha='center', fontsize=9, color=NE)
save(fig, '23-confusion.png')

# 24 · el clasificador trivial
fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.3)); plt.subplots_adjust(wspace=0.12)
data = [('Dice SIEMPRE «−»', NA, [[0, 5], [0, 95]], [('a', 0.95), ('s⁺', 0.0), ('s⁻', 1.0), ('F₁', 0.0)]),
        ('Un clasificador útil', VE, [[4, 1], [1, 94]], [('a', 0.98), ('s⁺', 0.80), ('s⁻', 0.99), ('F₁', 0.80)])]
for k, (ax, (h, c, vals, mets)) in enumerate(zip(axs, data)):
    cm(ax, [[c, 0], [0, c]], vals=vals, big=True)
    ax.set_xlim(-1.6, 5.4); ax.set_ylim(3.0, -0.1)
    for i, (mn, mv) in enumerate(mets):
        yy = 0.55 + i * 0.6
        ax.text(2.45, yy, mn, fontsize=10, va='center', color=NE, fontweight='bold')
        ax.add_patch(Rectangle((2.95, yy - 0.17), 2.2, 0.34, fc=GRf, ec='none'))
        ax.add_patch(Rectangle((2.95, yy - 0.17), 2.2 * mv, 0.34, fc=c, ec='none', alpha=0.85))
        ax.text(3.0 + 2.2 * max(mv, 0) + 0.05 if mv < 0.6 else 3.0, yy, f'{mv:.2f}'.replace('.', ','), va='center', fontsize=9,
                color=NE if mv < 0.6 else 'white', fontweight='bold')
    num(ax, k + 1, color=c); title(ax, h, '95 negativos y 5 positivos', c)
fig.text(0.5, -0.02, 'Exactitud casi igual (0,95 contra 0,98), utilidad opuesta: el primero no encuentra NINGÚN positivo. Nunca una sola medida.',
         ha='center', fontsize=8.8, color=NE)
save(fig, '24-trivial.png')
