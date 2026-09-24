#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las figuras 25 a 27 de algoritmos.pdf (algoritmos tradicionales).

    python3 imagenes/algoritmos/generar-figuras-tradicionales.py

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

from math import comb

# ================================================================ 10 · k-NN
# 25 · el efecto de k
rng = np.random.default_rng(7)
A = rng.normal([-0.6, 0.3], 0.85, (60, 2))
B = rng.normal([0.8, -0.4], 0.85, (40, 2))
X = np.vstack([A, B]); Y = np.r_[np.ones(60), -np.ones(40)]
g = np.linspace(-3, 3, 240); GX, GY = np.meshgrid(g, g)
G = np.c_[GX.ravel(), GY.ravel()]
D2 = ((G[:, None, :] - X[None, :, :]) ** 2).sum(-1)
orden = np.argsort(D2, axis=1)

fig, axs = plt.subplots(1, 3, figsize=(8.8, 3.25)); plt.subplots_adjust(wspace=0.06)
spec = [(1, 'k = 1: sigue a cada punto', 'frontera dentada:\nse aprende el ruido', NA),
        (15, 'k = 15: frontera suave', 'el punto medio,\nelegido con monitoreo', VE),
        (100, 'k = N = 100: la mayoritaria', 'ya no mira nada:\nsubajuste', GR)]
for k_, (ax, (k, h, sub, c)) in enumerate(zip(axs, spec)):
    voto = np.sign(Y[orden[:, :k]].sum(1) + 1e-9).reshape(GX.shape)
    ax.contourf(GX, GY, voto, levels=[-2, 0, 2], colors=[NAf, AZf])
    ax.contour(GX, GY, voto, levels=[0], colors=[c], linewidths=1.6)
    ax.scatter(A[:, 0], A[:, 1], s=13, c=AZ, edgecolors='white', lw=0.4, zorder=5)
    ax.scatter(B[:, 0], B[:, 1], s=13, c=NA, edgecolors='white', lw=0.4, zorder=5)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); clean(ax)
    num(ax, k_ + 1, color=c); title(ax, h, sub, c)
fig.text(0.5, -0.03, 'k chico: varianza alta (sobreajuste) · k grande: sesgo alto (subajuste) · el k se elige con validación, NUNCA con la prueba',
         ha='center', fontsize=8.8, color=NE)
save(fig, '25-knn-k.png')

# ================================================================ 13 · SVM
# 26 · margen máximo y truco del núcleo
fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.5), gridspec_kw={'width_ratios': [1.05, 1]})
plt.subplots_adjust(wspace=0.12)
ax = axs[0]
pos = np.array([[-1.0, 1.0], [1.5, 1.0], [-2.0, 2.1], [0.4, 2.4], [2.2, 1.9], [-0.6, 1.7]])
neg = np.array([[0.3, -1.0], [-1.8, -1.6], [1.9, -1.5], [-0.8, -2.3], [1.0, -2.2]])
xs = np.array([-3, 3])
for m, b in [(0.35, 0.25), (-0.3, -0.2), (0.12, 0.62)]:
    ax.plot(xs, m * xs + b, color=CL, lw=1.3, zorder=1)
ax.fill_between(xs, -1, 1, color=VIf, zorder=0)
ax.axhline(0, color=VE, lw=2.4, zorder=3)
ax.axhline(1, color=VI, lw=1.1, ls='--', zorder=2); ax.axhline(-1, color=VI, lw=1.1, ls='--', zorder=2)
ax.scatter(pos[:, 0], pos[:, 1], s=34, c=AZ, zorder=5, edgecolors='white', lw=0.6)
ax.scatter(neg[:, 0], neg[:, 1], s=34, c=NA, zorder=5, edgecolors='white', lw=0.6)
sv = np.array([[-1.0, 1.0], [1.5, 1.0], [0.3, -1.0]])
ax.scatter(sv[:, 0], sv[:, 1], s=150, facecolors='none', edgecolors=NE, lw=1.4, zorder=6)
arrow(ax, (2.55, 0.02), (2.55, 0.98), VI, lw=1.3, ms=8, style='<|-|>')
ax.text(2.45, 0.5, 'margen', color=VI, fontsize=8.5, ha='right', va='center', bbox=BB)
ax.text(-2.85, 0.12, 'hiperplano óptimo', color=VE, fontsize=8.5, va='bottom', bbox=BB)
ax.text(-2.85, -2.85, 'grises: también separan, pero pasan raspando', color=GR, fontsize=7.8)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal'); clean(ax)
num(ax, 1, color=VE); title(ax, 'El pasillo más ancho', 'sólo los puntos del borde (círculos) lo definen:\nson los vectores de soporte', VE)

ax = axs[1]
x1 = np.array([-2.4, -2.0, -1.6, 1.6, 2.0, 2.4]); x2 = np.array([-0.9, -0.4, 0.0, 0.5, 0.9])
ax.axhline(-0.35, color=CL, lw=0.8)
ax.scatter(x1, np.full_like(x1, -0.35), s=28, c=NA, zorder=5, edgecolors='white', lw=0.5)
ax.scatter(x2, np.full_like(x2, -0.35), s=28, c=AZ, zorder=5, edgecolors='white', lw=0.5)
ax.text(2.75, -0.62, r'$x$', color=GR, fontsize=9)
ax.text(0, -1.02, 'en 1D: ningún umbral los separa', color=GR, fontsize=7.8, ha='center', va='bottom')
ax.scatter(x1, x1 ** 2 / 2 + 0.5, s=28, c=NA, zorder=5, edgecolors='white', lw=0.5)
ax.scatter(x2, x2 ** 2 / 2 + 0.5, s=28, c=AZ, zorder=5, edgecolors='white', lw=0.5)
xx = np.linspace(-2.7, 2.7, 100); ax.plot(xx, xx ** 2 / 2 + 0.5, color=CL, lw=1, zorder=1)
ax.axhline(1.35, color=VE, lw=2.2)
ax.text(-2.75, 1.45, 'en $(x,\\,x^2)$ una recta sí alcanza', color=VE, fontsize=8.2, bbox=BB)
for xv in (-1.3, 1.3):
    ax.plot([xv, xv], [-0.6, -0.1], color=VE, lw=2, ls=':')
ax.text(0, 0.2, 'y vuelta a 1D: la recta es un intervalo', color=VE, fontsize=7.6, ha='center')
ax.set_xlim(-2.9, 2.9); ax.set_ylim(-1.1, 3.9); clean(ax)
num(ax, 2, color=VI); title(ax, 'El truco del núcleo', 'separar linealmente en un\nespacio transformado', VI)
save(fig, '26-svm.png')

# ============================================================ 14 · ENSAMBLES
# 27 · por qué votar funciona, y los dos esquemas
fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.3), gridspec_kw={'width_ratios': [1, 1.1]})
plt.subplots_adjust(wspace=0.18)
ax = axs[0]
Ms = np.arange(1, 42, 2)
def mayoria(p, M): return sum(comb(M, k) * p ** k * (1 - p) ** (M - k) for k in range(M // 2 + 1, M + 1))
for p, c, lab in [(0.3, VE, 'independientes, 30 % de error c/u'), (0.45, AZ, 'independientes, 45 % de error c/u')]:
    ax.plot(Ms, [mayoria(p, M) for M in Ms], color=c, lw=2, marker='o', ms=3, label=lab)
ax.plot(Ms, np.full(len(Ms), 0.3), color=NA, lw=2, ls='--', label='todos iguales (30 %): no gana nada')
ax.set_xlabel('cantidad de clasificadores que votan', fontsize=8.5); ax.set_ylabel('error del voto por mayoría', fontsize=8.5)
ax.set_ylim(0, 0.5); ax.legend(fontsize=7.5, frameon=False, loc='upper right')
for s in ax.spines.values(): s.set_color(CL)
ax.tick_params(labelsize=7.5, colors=GR)
num(ax, 1, x=0.035, y=0.2, color=VE); title(ax, 'Votar funciona si se equivocan distinto', 'con 5 de 30 %: 16 %; con 21: 2,6 %', VE)

ax = axs[1]; clean(ax, False); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.text(0.1, 5.7, 'Bagging — en paralelo', color=AZ, fontsize=9, fontweight='bold')
for i in range(3):
    box(ax, 0.3 + i * 2.2, 4.25, 1.9, 1.15, AZf)
    ax.text(1.25 + i * 2.2, 4.82, f'muestra\nbootstrap {i+1}\n→ árbol {i+1}', ha='center', va='center', fontsize=7.3, color=NE)
    arrow(ax, (1.25 + i * 2.2, 4.2), (1.25 + i * 2.2, 3.78), AZ, lw=1.3, ms=8)
box(ax, 0.3, 3.3, 6.3, 0.45, AZ)
ax.text(3.45, 3.52, 'voto por mayoría (todos igual)', ha='center', va='center', fontsize=7.2, color='white', fontweight='bold')
ax.text(0.1, 2.6, 'AdaBoost — en serie, corrigiendo', color=NA, fontsize=9, fontweight='bold')
for i in range(3):
    box(ax, 0.3 + i * 2.2, 1.0, 1.9, 1.2, NAf)
    ax.text(1.25 + i * 2.2, 1.6, f'stump {i+1}\n(los errados\npesan más)', ha='center', va='center', fontsize=7.3, color=NE)
    if i < 2: arrow(ax, (2.2 + i * 2.2, 1.6), (2.5 + i * 2.2, 1.6), NA, lw=1.4, ms=8)
arrow(ax, (6.6, 1.6), (7.05, 1.6), NA, lw=1.4, ms=8)
box(ax, 7.1, 1.0, 2.6, 1.2, NA)
ax.text(8.4, 1.6, 'voto\nponderado', ha='center', va='center', fontsize=7.6, color='white', fontweight='bold')
ax.text(4.3, 0.3, 'bagging baja la varianza · boosting baja el sesgo', ha='center', fontsize=8.2, color=GR)
num(ax, 2, x=0.9, y=0.12, color=VI)
save(fig, '27-ensambles.png')
