import matplotlib.pyplot as plt
import numpy as np

SUPERFICIE = "#fcfcfb"
TINTA_PRIMARIA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_TENUE = "#898781"
GRILLA = "#e1e0d9"
EJE = "#c3c2b7"
COLOR_CLASE_POSITIVA = "#2a78d6"
COLOR_CLASE_NEGATIVA = "#eb6834"


def _recta_de_separacion(pesos, umbral, x1):
    w1, w2 = pesos
    if w2 == 0:
        return None
    return (umbral - w1 * x1) / w2


def _dibujar_patrones(ejes, entradas, salidas_deseadas, tamanio_punto):
    for clase, color, etiqueta in (
        (1, COLOR_CLASE_POSITIVA, "clase +1"),
        (-1, COLOR_CLASE_NEGATIVA, "clase -1"),
    ):
        pertenecen_a_la_clase = salidas_deseadas == clase
        ejes.scatter(
            entradas[pertenecen_a_la_clase, 0],
            entradas[pertenecen_a_la_clase, 1],
            s=tamanio_punto,
            c=color,
            edgecolors=SUPERFICIE,
            linewidths=0.5,
            alpha=0.85,
            label=etiqueta,
            zorder=2,
        )


def _aplicar_estilo(ejes, limite_x1, limite_x2):
    ejes.set_facecolor(SUPERFICIE)
    ejes.set_xlim(*limite_x1)
    ejes.set_ylim(*limite_x2)
    ejes.set_aspect("equal", adjustable="box")
    ejes.grid(True, color=GRILLA, linewidth=0.8, zorder=0)
    ejes.set_axisbelow(True)
    ejes.axhline(0, color=EJE, linewidth=1.0, zorder=1)
    ejes.axvline(0, color=EJE, linewidth=1.0, zorder=1)
    for lado in ("top", "right"):
        ejes.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ejes.spines[lado].set_color(EJE)
    ejes.tick_params(colors=TINTA_TENUE, labelsize=9)
    ejes.set_xlabel("x₁", color=TINTA_SECUNDARIA, fontsize=11)


def graficar_entrenamiento(entradas, salidas_deseadas, historial_pesos, titulo,
                           archivo_salida=None, dpi=150):
    figura, ejes = plt.subplots(figsize=(6.6, 6.0), dpi=dpi)
    figura.patch.set_facecolor(SUPERFICIE)

    _dibujar_patrones(ejes, entradas, salidas_deseadas, tamanio_punto=26)

    x1_minimo, x1_maximo = entradas[:, 0].min(), entradas[:, 0].max()
    x2_minimo, x2_maximo = entradas[:, 1].min(), entradas[:, 1].max()
    margen_x1 = 0.12 * (x1_maximo - x1_minimo)
    margen_x2 = 0.12 * (x2_maximo - x2_minimo)

    x1 = np.linspace(x1_minimo - margen_x1, x1_maximo + margen_x1, 100)
    cantidad_de_rectas_previas = len(historial_pesos) - 1

    for numero_de_recta, (pesos, umbral) in enumerate(historial_pesos[:-1]):
        x2 = _recta_de_separacion(pesos, umbral, x1)
        if x2 is None:
            continue
        avance = numero_de_recta / max(cantidad_de_rectas_previas - 1, 1)
        ejes.plot(x1, x2, color=TINTA_TENUE, linewidth=1.1,
                  alpha=0.25 + 0.45 * avance, zorder=3)

    pesos_finales, umbral_final = historial_pesos[-1]
    x2_final = _recta_de_separacion(pesos_finales, umbral_final, x1)
    if x2_final is not None:
        ejes.plot(x1, x2_final, color=TINTA_PRIMARIA, linewidth=2.2, zorder=4,
                  label=f"recta final (época {cantidad_de_rectas_previas})")
    if cantidad_de_rectas_previas > 0:
        ejes.plot([], [], color=TINTA_TENUE, linewidth=1.1, alpha=0.5,
                  label=f"inicio + épocas previas ({cantidad_de_rectas_previas})")

    _aplicar_estilo(ejes,
                    (x1_minimo - margen_x1, x1_maximo + margen_x1),
                    (x2_minimo - margen_x2, x2_maximo + margen_x2))
    ejes.set_ylabel("x₂", color=TINTA_SECUNDARIA, fontsize=11)
    ejes.set_title(titulo, color=TINTA_PRIMARIA, fontsize=13, pad=14, loc="left")
    ejes.legend(loc="upper left", bbox_to_anchor=(0, -0.12), ncol=2,
                frameon=False, fontsize=9, labelcolor=TINTA_SECUNDARIA)

    figura.tight_layout()
    if archivo_salida is not None:
        figura.savefig(archivo_salida, facecolor=SUPERFICIE, bbox_inches="tight")
    return figura


def graficar_comparacion_dispersiones(resultados, archivo_salida=None, dpi=150):
    figura, panel_de_ejes = plt.subplots(1, len(resultados), figsize=(13.5, 5.2), dpi=dpi,
                                         sharex=True, sharey=True)
    figura.patch.set_facecolor(SUPERFICIE)

    limite = max(abs(resultado["entradas"]).max() for resultado in resultados) * 1.1

    for ejes, resultado in zip(panel_de_ejes, resultados):
        _dibujar_patrones(ejes, resultado["entradas"], resultado["salidas_deseadas"],
                          tamanio_punto=18)

        x1 = np.linspace(-limite, limite, 100)
        x2 = _recta_de_separacion(resultado["pesos"], resultado["umbral"], x1)
        if x2 is not None:
            ejes.plot(x1, x2, color=TINTA_PRIMARIA, linewidth=2.2, zorder=4,
                      label="recta aprendida")

        _aplicar_estilo(ejes, (-limite, limite), (-limite, limite))

        convergio = "convergió" if resultado["convergio"] else "no convergió"
        ejes.set_title(resultado["nombre"], color=TINTA_PRIMARIA, fontsize=13, pad=18)
        ejes.text(0.5, 1.03,
                  f"test {resultado['porcentaje_aciertos']:.1f}%  ·  {convergio} en {resultado['epocas']} épocas",
                  transform=ejes.transAxes, ha="center",
                  color=TINTA_SECUNDARIA, fontsize=9.5)

    panel_de_ejes[0].set_ylabel("x₂", color=TINTA_SECUNDARIA, fontsize=11)
    manejadores, etiquetas = panel_de_ejes[0].get_legend_handles_labels()

    figura.suptitle("Perceptrón simple sobre OR con dispersión creciente",
                    color=TINTA_PRIMARIA, fontsize=15, y=1.04)
    figura.tight_layout()
    figura.subplots_adjust(bottom=0.20)
    figura.legend(manejadores, etiquetas, loc="lower center", ncol=3, frameon=False,
                  fontsize=10.5, labelcolor=TINTA_SECUNDARIA, bbox_to_anchor=(0.5, 0.0))

    if archivo_salida is not None:
        figura.savefig(archivo_salida, facecolor=SUPERFICIE, bbox_inches="tight")
    return figura


def graficar_errores_por_epoca(series, titulo, archivo_salida=None, dpi=150):
    figura, ejes = plt.subplots(figsize=(9.0, 4.6), dpi=dpi)
    figura.patch.set_facecolor(SUPERFICIE)
    ejes.set_facecolor(SUPERFICIE)

    colores = (COLOR_CLASE_POSITIVA, "#1baf7a", COLOR_CLASE_NEGATIVA)

    for numero_de_serie, (serie, color) in enumerate(zip(series, colores)):
        porcentaje = 100 * np.array(serie["errores"]) / serie["cantidad_patrones"]
        epocas = np.arange(1, len(porcentaje) + 1)

        ejes.plot(epocas, porcentaje, color=color, linewidth=2.0,
                  label=serie["etiqueta"], zorder=3)
        ejes.scatter(epocas, porcentaje, s=22, color=color,
                     edgecolors=SUPERFICIE, linewidths=1.2, zorder=4)

        convergio = porcentaje[-1] == 0
        detalle = f"0 errores en la época {len(porcentaje)}" if convergio else \
                  f"se estanca en {porcentaje[-1]:.1f} %"
        ejes.annotate(
            f"{serie['etiqueta']}: {detalle}",
            xy=(epocas[-1], porcentaje[-1]),
            xytext=(22, 20 + 26 * numero_de_serie),
            textcoords="offset points",
            color=TINTA_SECUNDARIA, fontsize=9,
            ha="right" if not convergio else "left",
            arrowprops=dict(arrowstyle="-", color=TINTA_TENUE, linewidth=0.9,
                            shrinkA=0, shrinkB=3),
        )

    ejes.grid(True, color=GRILLA, linewidth=0.8, zorder=0)
    ejes.set_axisbelow(True)
    ejes.set_ylim(bottom=-0.4)
    for lado in ("top", "right"):
        ejes.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ejes.spines[lado].set_color(EJE)
    ejes.tick_params(colors=TINTA_TENUE, labelsize=9)
    ejes.set_xlabel("época", color=TINTA_SECUNDARIA, fontsize=11)
    ejes.set_ylabel("% de patrones mal clasificados", color=TINTA_SECUNDARIA, fontsize=11)
    ejes.set_title(titulo, color=TINTA_PRIMARIA, fontsize=13, pad=12, loc="left")
    ejes.legend(frameon=False, fontsize=10, labelcolor=TINTA_SECUNDARIA,
                loc="lower right")

    figura.tight_layout()
    if archivo_salida is not None:
        figura.savefig(archivo_salida, facecolor=SUPERFICIE, bbox_inches="tight")
    return figura
