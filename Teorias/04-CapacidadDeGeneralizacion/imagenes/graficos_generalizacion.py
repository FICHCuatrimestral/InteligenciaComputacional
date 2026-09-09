"""Figuras del apunte de Capacidad de generalización (IC, FICH-UNL).

Genera todos los PNG de ../imagenes/ a partir de las descripciones habladas
de las clases 001 a 008 y de las diapositivas de la cátedra.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

DIRECTORIO_SALIDA = os.path.dirname(os.path.abspath(__file__))

COLOR_ENTRENAMIENTO = "#c0392b"
COLOR_PRUEBA = "#1baf7a"
COLOR_MONITOREO = "#2a78d6"
COLOR_ACENTO = "#eb6834"
COLOR_GRIS = "#52514e"

plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "axes.grid": True,
    "grid.alpha": 0.30,
    "grid.linestyle": ":",
    "figure.dpi": 160,
    "savefig.bbox": "tight",
})


def guardar(figura, nombre_archivo):
    ruta_completa = os.path.join(DIRECTORIO_SALIDA, nombre_archivo)
    figura.savefig(ruta_completa)
    plt.close(figura)
    print("generado:", nombre_archivo)


# ---------------------------------------------------------------- figura 01
def figura_curva_de_error_un_parametro():
    figura, ejes = plt.subplots(figsize=(5.0, 3.0))
    valores_del_peso = np.linspace(-1.5, 3.5, 400)
    peso_optimo = 1.0
    error = 0.35 * (valores_del_peso - peso_optimo) ** 2 + 0.15
    ejes.plot(valores_del_peso, error, color=COLOR_ENTRENAMIENTO, linewidth=2)
    ejes.plot([peso_optimo], [0.15], "o", color=COLOR_ACENTO, markersize=7, zorder=5)
    ejes.annotate(r"$w^{*}$: el valor que busca el entrenamiento",
                  xy=(peso_optimo, 0.15), xytext=(-1.3, 1.55),
                  arrowprops=dict(arrowstyle="->", color=COLOR_GRIS), color=COLOR_GRIS)
    for peso_de_muestra in (0.1, 0.2):
        error_de_muestra = 0.35 * (peso_de_muestra - peso_optimo) ** 2 + 0.15
        ejes.plot([peso_de_muestra, peso_de_muestra], [0, error_de_muestra],
                  color=COLOR_GRIS, linestyle="--", linewidth=0.8)
        ejes.plot([peso_de_muestra], [error_de_muestra], "o", color=COLOR_GRIS, markersize=4)
    ejes.set_xlabel(r"$w$  (el único parámetro ajustable)")
    ejes.set_ylabel(r"error $\varepsilon$")
    ejes.set_title("Curva de error con un solo parámetro")
    ejes.set_ylim(0, 2.2)
    ejes.set_xlim(-1.5, 3.5)
    guardar(figura, "01-curva-error-1d.png")


# ---------------------------------------------------------------- figura 02
def superficie_de_un_solo_minimo(malla_x, malla_y):
    return 0.45 * (malla_x - 0.6) ** 2 + 0.30 * (malla_y + 0.4) ** 2 + 0.1


def figura_superficie_dos_parametros():
    figura = plt.figure(figsize=(5.4, 3.6))
    ejes = figura.add_subplot(111, projection="3d")
    eje_w1 = np.linspace(-3, 3, 60)
    eje_w2 = np.linspace(-3, 3, 60)
    malla_w1, malla_w2 = np.meshgrid(eje_w1, eje_w2)
    superficie = superficie_de_un_solo_minimo(malla_w1, malla_w2)
    ejes.plot_wireframe(malla_w1, malla_w2, superficie, color=COLOR_GRIS, linewidth=0.4)

    # trayectoria de descenso por gradiente desde una inicialización cualquiera
    punto = np.array([-2.6, 2.6])
    trayectoria = [punto.copy()]
    for _ in range(28):
        gradiente = np.array([0.9 * (punto[0] - 0.6), 0.6 * (punto[1] + 0.4)])
        punto = punto - 0.18 * gradiente
        trayectoria.append(punto.copy())
    trayectoria = np.array(trayectoria)
    alturas = superficie_de_un_solo_minimo(trayectoria[:, 0], trayectoria[:, 1])
    ejes.plot(trayectoria[:, 0], trayectoria[:, 1], alturas,
              color=COLOR_ACENTO, linewidth=2, marker="o", markersize=2.5)
    ejes.set_xlabel(r"$w_1$")
    ejes.set_ylabel(r"$w_2$")
    ejes.set_zlabel(r"$\varepsilon$")
    ejes.set_title("Superficie de error con dos parámetros: un único mínimo")
    ejes.view_init(elev=28, azim=-58)
    guardar(figura, "02-superficie-un-minimo.png")


# ---------------------------------------------------------------- figura 03
def figura_superficies_dificiles():
    eje_x = np.linspace(-3, 3, 90)
    eje_y = np.linspace(-3, 3, 90)
    malla_x, malla_y = np.meshgrid(eje_x, eje_y)

    superficie_multiples_minimos = (
        -1.4 * np.exp(-((malla_x - 1.2) ** 2 + (malla_y - 1.2) ** 2))
        - 1.0 * np.exp(-((malla_x + 1.4) ** 2 + (malla_y - 1.1) ** 2))
        - 1.1 * np.exp(-((malla_x - 1.3) ** 2 + (malla_y + 1.3) ** 2))
        - 0.9 * np.exp(-((malla_x + 1.2) ** 2 + (malla_y + 1.4) ** 2))
        + 0.06 * (malla_x ** 2 + malla_y ** 2)
    )
    superficie_con_mesetas = (
        0.5 * np.tanh(1.8 * (malla_x - 1.2))
        + 0.5 * np.tanh(1.8 * (malla_x + 1.2))
        + 0.12 * malla_y ** 2
        - 0.9 * np.exp(-((malla_x) ** 2 + (malla_y) ** 2) / 0.5)
    )
    superficie_irregular = (
        0.10 * (malla_x ** 2 + malla_y ** 2)
        + 0.55 * np.sin(3.1 * malla_x) * np.cos(2.9 * malla_y)
        + 0.30 * np.sin(5.3 * malla_x + 1.0) * np.sin(4.7 * malla_y)
    )

    titulos = ["Cuatro mínimos: el algoritmo cae\nen el que le queda cerca",
               "Mesetas: gradiente casi nulo,\nno sabe hacia dónde ir",
               "Caso realista: muchos mínimos\ny superficie muy irregular"]
    superficies = [superficie_multiples_minimos, superficie_con_mesetas, superficie_irregular]

    figura = plt.figure(figsize=(9.6, 3.1))
    for indice, (superficie, titulo) in enumerate(zip(superficies, titulos)):
        ejes = figura.add_subplot(1, 3, indice + 1, projection="3d")
        ejes.plot_wireframe(malla_x, malla_y, superficie, color=COLOR_GRIS, linewidth=0.32)
        ejes.set_title(titulo, fontsize=8.5)
        ejes.set_xticklabels([])
        ejes.set_yticklabels([])
        ejes.set_zticklabels([])
        ejes.set_xlabel(r"$w_1$", labelpad=-10)
        ejes.set_ylabel(r"$w_2$", labelpad=-10)
        ejes.grid(False)
        ejes.view_init(elev=32, azim=-60)
    guardar(figura, "03-superficies-dificiles.png")


# ---------------------------------------------------------------- figura 04
def figura_error_versus_epocas():
    figura, ejes = plt.subplots(figsize=(5.6, 3.4))
    epocas = np.linspace(1, 400, 400)
    error_de_entrenamiento = 0.95 * np.exp(-epocas / 90) + 0.06
    error_de_monitoreo = 0.95 * np.exp(-epocas / 70) + 0.16 + 0.00055 * np.maximum(epocas - 150, 0)

    indice_minimo = int(np.argmin(error_de_monitoreo))
    epoca_de_corte = epocas[indice_minimo]

    ejes.plot(epocas, error_de_entrenamiento, color=COLOR_ENTRENAMIENTO, linewidth=2,
              label=r"error de entrenamiento $\varepsilon_e$")
    ejes.plot(epocas, error_de_monitoreo, color=COLOR_PRUEBA, linewidth=2,
              label=r"error de monitoreo $\varepsilon_m$")
    ejes.axvline(epoca_de_corte, color=COLOR_ACENTO, linestyle="--", linewidth=1.4)
    ejes.plot([epoca_de_corte], [error_de_monitoreo[indice_minimo]], "o",
              color=COLOR_ACENTO, markersize=7, zorder=5)
    ejes.annotate("corte temprano:\ngeneralización máxima",
                  xy=(epoca_de_corte, error_de_monitoreo[indice_minimo]),
                  xytext=(epoca_de_corte + 55, 0.62),
                  arrowprops=dict(arrowstyle="->", color=COLOR_ACENTO), color=COLOR_ACENTO)
    ejes.axvspan(epoca_de_corte, 400, color=COLOR_ACENTO, alpha=0.06)
    ejes.text(epoca_de_corte + 105, 0.15, "sobre-entrenamiento", color=COLOR_ACENTO,
              fontsize=8.5, ha="center")
    ejes.set_xlabel("épocas de entrenamiento")
    ejes.set_ylabel(r"error $\varepsilon$")
    ejes.set_title("El error de monitoreo se estanca y después sube")
    ejes.set_xlim(0, 400)
    ejes.set_ylim(0, 1.15)
    ejes.legend(frameon=False, fontsize=8.5)
    guardar(figura, "04-error-vs-epocas.png")


# ---------------------------------------------------------------- figura 05
def figura_error_versus_complejidad():
    figura, ejes = plt.subplots(figsize=(5.6, 3.4))
    parametros_libres = np.linspace(1, 60, 400)
    error_de_entrenamiento = 0.9 * np.exp(-parametros_libres / 9) + 0.04
    error_de_monitoreo = 0.9 * np.exp(-parametros_libres / 7) + 0.14 + 0.0075 * np.maximum(parametros_libres - 14, 0)

    indice_minimo = int(np.argmin(error_de_monitoreo))
    complejidad_optima = parametros_libres[indice_minimo]

    ejes.plot(parametros_libres, error_de_entrenamiento, color=COLOR_ENTRENAMIENTO,
              linewidth=2, label=r"$\varepsilon_e$")
    ejes.plot(parametros_libres, error_de_monitoreo, color=COLOR_PRUEBA,
              linewidth=2, label=r"$\varepsilon_m$")
    ejes.axvline(complejidad_optima, color=COLOR_ACENTO, linestyle="--", linewidth=1.4)
    ejes.plot([complejidad_optima], [error_de_monitoreo[indice_minimo]], "o",
              color=COLOR_ACENTO, markersize=7, zorder=5)
    ejes.text(complejidad_optima, 1.06, "complejidad óptima", color=COLOR_ACENTO,
              fontsize=8.5, ha="center")
    ejes.text(6.5, 0.72, "sub-ajuste\n(modelo demasiado\nelemental)", color=COLOR_GRIS,
              fontsize=8, ha="center")
    ejes.text(46, 0.55, "sobre-ajuste\n(le sobran grados\nde libertad)", color=COLOR_GRIS,
              fontsize=8, ha="center")
    ejes.set_xlabel("cantidad de parámetros libres del modelo")
    ejes.set_ylabel(r"error $\varepsilon$")
    ejes.set_title("La misma curva, ahora contra la complejidad del modelo")
    ejes.set_xlim(0, 60)
    ejes.set_ylim(0, 1.18)
    ejes.legend(frameon=False, fontsize=8.5)
    guardar(figura, "05-error-vs-complejidad.png")


# ---------------------------------------------------------------- figura 06
def generar_dos_clases(semilla=7):
    generador = np.random.default_rng(semilla)
    cantidad_por_clase = 60
    angulos = generador.uniform(0, np.pi, cantidad_por_clase)
    clase_azul = np.column_stack([
        1.6 * np.cos(angulos) + generador.normal(0, 0.28, cantidad_por_clase),
        1.6 * np.sin(angulos) + generador.normal(0, 0.28, cantidad_por_clase) - 0.5,
    ])
    clase_roja = np.column_stack([
        1.6 * np.cos(angulos) + generador.normal(0, 0.28, cantidad_por_clase) + 1.0,
        -1.6 * np.sin(angulos) + generador.normal(0, 0.28, cantidad_por_clase) + 0.5,
    ])
    entradas = np.vstack([clase_azul, clase_roja])
    etiquetas = np.concatenate([np.zeros(cantidad_por_clase), np.ones(cantidad_por_clase)])
    # se ensucian tres etiquetas a propósito: es el "ruido" del que habla la clase
    indices_ruidosos = generador.choice(len(etiquetas), 3, replace=False)
    etiquetas[indices_ruidosos] = 1 - etiquetas[indices_ruidosos]
    return entradas, etiquetas


def figura_clasificacion_tres_ajustes():
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC

    entradas, etiquetas = generar_dos_clases()
    (entradas_de_entrenamiento, entradas_de_prueba,
     etiquetas_de_entrenamiento, etiquetas_de_prueba) = train_test_split(
        entradas, etiquetas, test_size=0.35, random_state=0, stratify=etiquetas)

    malla_x, malla_y = np.meshgrid(np.linspace(-3.0, 3.6, 300), np.linspace(-2.8, 2.6, 300))
    puntos_de_la_malla = np.column_stack([malla_x.ravel(), malla_y.ravel()])

    modelos = [
        ("Sub-ajuste: una recta", LogisticRegression()),
        ("Ajuste adecuado", SVC(kernel="rbf", C=2.0, gamma=0.7)),
        ("Sobre-ajuste", SVC(kernel="rbf", C=1e6, gamma=60.0)),
    ]

    figura, conjunto_de_ejes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    for ejes, (titulo, modelo) in zip(conjunto_de_ejes, modelos):
        modelo.fit(entradas_de_entrenamiento, etiquetas_de_entrenamiento)
        prediccion = modelo.predict(puntos_de_la_malla).reshape(malla_x.shape)
        ejes.contourf(malla_x, malla_y, prediccion, levels=[-0.5, 0.5, 1.5],
                      colors=["#cfe0f5", "#f7d3cd"], alpha=0.9)
        ejes.contour(malla_x, malla_y, prediccion, levels=[0.5], colors=["#20304a"], linewidths=1.0)
        ejes.scatter(*entradas_de_entrenamiento[etiquetas_de_entrenamiento == 0].T,
                     s=11, color="#1f4e9c", zorder=3)
        ejes.scatter(*entradas_de_entrenamiento[etiquetas_de_entrenamiento == 1].T,
                     s=11, color="#b3261e", zorder=3)
        ejes.scatter(*entradas_de_prueba[etiquetas_de_prueba == 0].T, s=26, marker="x",
                     color="#1f4e9c", linewidths=1.0, zorder=4)
        ejes.scatter(*entradas_de_prueba[etiquetas_de_prueba == 1].T, s=26, marker="x",
                     color="#b3261e", linewidths=1.0, zorder=4)
        aciertos_entrenamiento = modelo.score(entradas_de_entrenamiento, etiquetas_de_entrenamiento)
        aciertos_prueba = modelo.score(entradas_de_prueba, etiquetas_de_prueba)
        ejes.set_title(f"{titulo}\nentrenamiento {aciertos_entrenamiento*100:.1f} %  ·  "
                       f"prueba {aciertos_prueba*100:.1f} %", fontsize=8.8)
        ejes.set_xticks([]); ejes.set_yticks([]); ejes.grid(False)
    figura.text(0.5, -0.03, "puntos = datos de entrenamiento;  cruces = datos de prueba",
                ha="center", fontsize=8, color=COLOR_GRIS)
    guardar(figura, "06-clasificacion-tres-ajustes.png")


# ---------------------------------------------------------------- figura 07
def figura_regresion_sesgo_varianza():
    generador = np.random.default_rng(3)
    abscisas_de_entrenamiento = np.sort(generador.uniform(0, 1, 14))
    funcion_verdadera = lambda t: np.sin(2 * np.pi * t) * 0.7 + 0.4 * t
    ordenadas = funcion_verdadera(abscisas_de_entrenamiento) + generador.normal(0, 0.09, 14)
    abscisas_densas = np.linspace(-0.03, 1.03, 500)

    grados = [1, 4, 13]
    titulos = ["Grado 1: sesgo alto\n(el modelo no da)",
               "Grado 4: el punto justo",
               "Grado 13: varianza alta\n(pasa por todos los puntos)"]

    figura, conjunto_de_ejes = plt.subplots(1, 3, figsize=(9.6, 3.0))
    for ejes, grado, titulo in zip(conjunto_de_ejes, grados, titulos):
        coeficientes = np.polyfit(abscisas_de_entrenamiento, ordenadas, grado)
        ajuste = np.polyval(coeficientes, abscisas_densas)
        ejes.plot(abscisas_densas, funcion_verdadera(abscisas_densas), color=COLOR_GRIS,
                  linewidth=1.4, linestyle="--", label="función real")
        ejes.plot(abscisas_densas, ajuste, color=COLOR_MONITOREO, linewidth=1.8, label="modelo")
        ejes.plot(abscisas_de_entrenamiento, ordenadas, "o", color="#b3261e", markersize=4.5,
                  label="datos de entrenamiento")
        error_de_entrenamiento = np.mean(
            (np.polyval(coeficientes, abscisas_de_entrenamiento) - ordenadas) ** 2)
        ejes.set_title(f"{titulo}\nMSE en entrenamiento: {error_de_entrenamiento:.4f}", fontsize=8.5)
        ejes.set_ylim(-1.4, 1.6)
        ejes.set_xlim(-0.03, 1.03)
        ejes.set_xticks([]); ejes.set_yticks([])
    conjunto_de_ejes[0].legend(frameon=False, fontsize=7.2, loc="lower left")
    guardar(figura, "07-regresion-sesgo-varianza.png")


# ---------------------------------------------------------------- figura 08
def dibujar_dataset(ejes, matriz, etiquetas_de_clase, titulo, resaltar=None):
    ejes.imshow(matriz, aspect="auto", cmap="viridis", interpolation="nearest",
                extent=[0, matriz.shape[1], matriz.shape[0], 0])
    columna_de_clase = np.array(etiquetas_de_clase).reshape(-1, 1)
    ejes.imshow(columna_de_clase, aspect="auto", cmap="gray_r", vmin=0, vmax=1,
                interpolation="nearest",
                extent=[matriz.shape[1] + 0.4, matriz.shape[1] + 1.6, matriz.shape[0], 0])
    ejes.set_xlim(0, matriz.shape[1] + 1.8)
    ejes.set_ylim(matriz.shape[0], 0)
    ejes.set_title(titulo, fontsize=8.8)
    ejes.set_xticks([]); ejes.set_yticks([]); ejes.grid(False)
    if resaltar is not None:
        fila_inicial, cantidad_de_filas = resaltar
        ejes.add_patch(Rectangle((-0.3, fila_inicial), matriz.shape[1] + 2.2, cantidad_de_filas,
                                 fill=False, edgecolor=COLOR_ACENTO, linewidth=2.0, zorder=6))


def figura_desordenar_los_datos():
    generador = np.random.default_rng(11)
    cantidad_de_patrones, cantidad_de_atributos = 40, 9
    matriz_ordenada = np.vstack([
        generador.uniform(0.35, 1.0, (20, cantidad_de_atributos)),
        generador.uniform(0.0, 0.65, (20, cantidad_de_atributos)),
    ])
    clases_ordenadas = np.array([1] * 20 + [0] * 20)
    permutacion = generador.permutation(cantidad_de_patrones)

    figura, (ejes_izquierdo, ejes_derecho) = plt.subplots(1, 2, figsize=(7.2, 3.6))
    dibujar_dataset(ejes_izquierdo, matriz_ordenada, clases_ordenadas,
                    "Como vienen: ordenados por clase\n(el bloque de prueba sale todo de clase 1)",
                    resaltar=(0, 8))
    dibujar_dataset(ejes_derecho, matriz_ordenada[permutacion], clases_ordenadas[permutacion],
                    "Desordenados al azar\n(el bloque de prueba representa a las dos clases)",
                    resaltar=(0, 8))
    guardar(figura, "08-desordenar-los-datos.png")


# ---------------------------------------------------------------- figura 09
def figura_particion_del_conjunto():
    figura, ejes = plt.subplots(figsize=(7.4, 1.9))
    bloques = [("entrenamiento propiamente dicho", 0.0, 0.62, COLOR_ENTRENAMIENTO),
               ("monitoreo\n(validación)", 0.62, 0.18, COLOR_MONITOREO),
               ("prueba", 0.80, 0.20, COLOR_PRUEBA)]
    for nombre, inicio, ancho, color in bloques:
        ejes.add_patch(Rectangle((inicio, 0), ancho, 1, facecolor=color, alpha=0.28,
                                 edgecolor=color, linewidth=1.6))
        ejes.text(inicio + ancho / 2, 0.5, nombre, ha="center", va="center", fontsize=8.6,
                  color=color)
    ejes.annotate("", xy=(0.0, 1.25), xytext=(0.80, 1.25),
                  arrowprops=dict(arrowstyle="<->", color=COLOR_GRIS))
    ejes.text(0.40, 1.34, "todo esto es «el conjunto de entrenamiento»: es lo único que tocamos",
              ha="center", fontsize=8.3, color=COLOR_GRIS)
    ejes.text(0.90, -0.28, "no se toca nunca", ha="center", fontsize=8.3, color=COLOR_PRUEBA)
    ejes.set_xlim(-0.02, 1.02)
    ejes.set_ylim(-0.45, 1.55)
    ejes.axis("off")
    guardar(figura, "09-particion-del-conjunto.png")


# ---------------------------------------------------------------- figura 10
def dibujar_esquema_de_particiones(ejes, bloques_de_prueba, cantidad_de_patrones, titulo,
                                   con_reposicion=False, generador=None):
    cantidad_de_repeticiones = len(bloques_de_prueba)
    for indice, bloque in enumerate(bloques_de_prueba):
        base_y = -indice * 1.35
        ejes.add_patch(Rectangle((0, base_y), cantidad_de_patrones, 1.0,
                                 facecolor="#e8e8e4", edgecolor=COLOR_GRIS, linewidth=0.7))
        for inicio, largo in bloque:
            ejes.add_patch(Rectangle((inicio, base_y), largo, 1.0,
                                     facecolor=COLOR_PRUEBA, alpha=0.55,
                                     edgecolor=COLOR_PRUEBA, linewidth=0.9))
        ejes.text(-1.2, base_y + 0.5, f"{indice + 1}", ha="right", va="center",
                  fontsize=7.5, color=COLOR_GRIS)
    ejes.set_xlim(-3.5, cantidad_de_patrones + 0.5)
    ejes.set_ylim(-cantidad_de_repeticiones * 1.35, 1.5)
    ejes.set_title(titulo, fontsize=8.8)
    ejes.axis("off")


def figura_esquemas_de_validacion_cruzada():
    cantidad_de_patrones = 100
    figura, conjunto_de_ejes = plt.subplots(1, 3, figsize=(9.8, 3.2))

    bloques_disjuntos = [[(i * 10, 10)] for i in range(5)]
    dibujar_esquema_de_particiones(
        conjunto_de_ejes[0], bloques_disjuntos, cantidad_de_patrones,
        "Particiones disjuntas\n(leave-$k$-out / $k$-fold)")

    bloques_solapados = [[(i * 5, 10)] for i in range(5)]
    dibujar_esquema_de_particiones(
        conjunto_de_ejes[1], bloques_solapados, cantidad_de_patrones,
        "Particiones solapadas\n(más repeticiones, menos independencia)")

    generador = np.random.default_rng(5)
    bloques_con_reposicion = []
    for _ in range(5):
        indices = generador.integers(0, cantidad_de_patrones, 10)
        bloques_con_reposicion.append([(int(i), 1) for i in indices])
    dibujar_esquema_de_particiones(
        conjunto_de_ejes[2], bloques_con_reposicion, cantidad_de_patrones,
        "Muestreo con reposición\n(bootstrap: un patrón puede repetirse)")

    figura.text(0.5, -0.02, "verde = bloque reservado para prueba en esa repetición; "
                            "gris = lo que se usa para entrenar",
                ha="center", fontsize=8, color=COLOR_GRIS)
    guardar(figura, "10-esquemas-validacion-cruzada.png")


# ---------------------------------------------------------------- figura 11
def figura_leave_uno_afuera():
    cantidad_de_patrones = 20
    figura, ejes = plt.subplots(figsize=(6.4, 3.0))
    for indice in range(8):
        base_y = -indice * 1.3
        ejes.add_patch(Rectangle((0, base_y), cantidad_de_patrones, 1.0,
                                 facecolor="#e8e8e4", edgecolor=COLOR_GRIS, linewidth=0.7))
        ejes.add_patch(Rectangle((indice, base_y), 1.0, 1.0,
                                 facecolor=COLOR_PRUEBA, edgecolor=COLOR_PRUEBA, linewidth=0.9))
        ejes.text(-0.8, base_y + 0.5, f"{indice + 1}", ha="right", va="center",
                  fontsize=7.5, color=COLOR_GRIS)
    ejes.text(cantidad_de_patrones / 2, -8 * 1.3 - 0.5, r"$\vdots$   hasta la repetición $P$",
              ha="center", fontsize=9, color=COLOR_GRIS)
    ejes.set_xlim(-2.5, cantidad_de_patrones + 0.5)
    ejes.set_ylim(-8 * 1.3 - 1.6, 1.4)
    ejes.set_title("leave-1-out: un patrón de prueba por repetición, $P$ entrenamientos completos",
                   fontsize=8.8)
    ejes.axis("off")
    guardar(figura, "11-leave-uno-afuera.png")


# ---------------------------------------------------------------- figura 12
def figura_matriz_de_confusion():
    figura, ejes = plt.subplots(figsize=(5.4, 2.9))
    valores = np.array([[28, 3], [2, 52]])
    ejes.imshow(valores, cmap="Blues", vmin=0, vmax=60)
    etiquetas_de_celda = [[r"$t_\oplus = 28$", r"$f_\ominus = 3$"],
                          [r"$f_\oplus = 2$", r"$t_\ominus = 52$"]]
    for fila in range(2):
        for columna in range(2):
            color_del_texto = "white" if valores[fila][columna] > 35 else "#0b0b0b"
            ejes.text(columna, fila, etiquetas_de_celda[fila][columna], ha="center",
                      va="center", fontsize=11, color=color_del_texto)
    ejes.set_xticks([0, 1]); ejes.set_xticklabels([r"predijo $\oplus$", r"predijo $\ominus$"])
    ejes.set_yticks([0, 1]); ejes.set_yticklabels([r"era $\oplus$", r"era $\ominus$"])
    ejes.set_xlabel("predicciones del clasificador")
    ejes.set_ylabel("clases correctas")
    ejes.set_title(r"Matriz de confusión: $N_\oplus = 31$, $N_\ominus = 54$, $N = 85$",
                   fontsize=9)
    ejes.grid(False)
    guardar(figura, "12-matriz-de-confusion.png")


# ---------------------------------------------------------------- figura 13
def figura_errores_en_series():
    tiempo = np.linspace(0, 4 * np.pi, 400)
    serie_correcta = np.sin(tiempo) * 0.9
    generador = np.random.default_rng(2)
    prediccion_mala = serie_correcta + 0.30 * np.sin(3.3 * tiempo) + generador.normal(0, 0.05, 400)
    prediccion_buena = serie_correcta + 0.09 * np.sin(3.3 * tiempo) + generador.normal(0, 0.02, 400)

    figura, conjunto_de_ejes = plt.subplots(2, 1, figsize=(6.6, 3.8), sharex=True)
    for ejes, prediccion, nombre in zip(conjunto_de_ejes,
                                        [prediccion_mala, prediccion_buena],
                                        ["predictor peor", "predictor mejor"]):
        ejes.plot(tiempo, serie_correcta, color="#0b0b0b", linewidth=1.4, label=r"valor correcto $y_i$")
        ejes.plot(tiempo, prediccion, color=COLOR_MONITOREO, linewidth=1.0,
                  label=r"predicción $\hat{y}_i$")
        ejes.fill_between(tiempo, serie_correcta, prediccion, color=COLOR_MONITOREO, alpha=0.35)
        error_absoluto_medio = np.mean(np.abs(prediccion - serie_correcta))
        error_cuadratico_medio = np.mean((prediccion - serie_correcta) ** 2)
        ejes.set_title(f"{nombre} — MAE = {error_absoluto_medio:.3f}, "
                       f"MSE = {error_cuadratico_medio:.4f}, "
                       f"RMSE = {np.sqrt(error_cuadratico_medio):.3f}", fontsize=8.5)
        ejes.set_ylabel(r"$y$")
        ejes.set_ylim(-1.5, 1.5)
    conjunto_de_ejes[0].legend(frameon=False, fontsize=7.5, ncol=2, loc="upper right")
    conjunto_de_ejes[1].set_xlabel("tiempo")
    figura.tight_layout()
    guardar(figura, "13-errores-en-series.png")


if __name__ == "__main__":
    figura_curva_de_error_un_parametro()
    figura_superficie_dos_parametros()
    figura_superficies_dificiles()
    figura_error_versus_epocas()
    figura_error_versus_complejidad()
    figura_clasificacion_tres_ajustes()
    figura_regresion_sesgo_varianza()
    figura_desordenar_los_datos()
    figura_particion_del_conjunto()
    figura_esquemas_de_validacion_cruzada()
    figura_leave_uno_afuera()
    figura_matriz_de_confusion()
    figura_errores_en_series()
