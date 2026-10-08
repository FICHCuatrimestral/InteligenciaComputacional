import math
import random


# evaluo f en un punto guardado como lista: [x] o [x, y]
def f1(punto):
    x = punto[0]
    return -x * math.sin(math.sqrt(abs(x)))         # [-512, 512] minimo: -418.98


def f2(punto):
    x = punto[0]
    y = punto[1]
    return (x**2 + y**2)**0.25 * (math.sin(50 * (x**2 + y**2)**0.1)**2 + 1)     # [-100, 100] minimo: 0


def txt(punto):
    """Muestra un punto [x] o [x, y] con 2 decimales."""
    return "[" + ", ".join(f"{c:8.2f}" for c in punto) + "]"


# enjambre de particulas (mejor global)
# ver = cuantas iteraciones se muestran en detalle (particula por particula)
def enjambre(funcion, limites, n_particulas=20, iteraciones=100, w=0.73, c1=1.5, c2=1.5, ver=2):
    dimensiones = len(limites)
    print(f"limites = {limites}  ->  dimensiones = {dimensiones}")
    print(f"cada particula es una lista de {dimensiones} numero(s): una solucion candidata\n")

    # ---------------- 1) posiciones al azar y velocidades en 0 ----------------
    print("=== 1) INICIALIZACION ===")
    posiciones = []
    velocidades = []
    for k in range(n_particulas):
        x = []
        for i in range(dimensiones):
            a, b = limites[i]
            sorteo = random.uniform(a, b)
            x.append(sorteo)
            print(f"  particula {k}, dimension {i}: sorteo uniforme entre {a} y {b} -> {sorteo:8.2f}")
        posiciones.append(x)
        velocidades.append([0] * dimensiones)
        print(f"  => posicion de la particula {k}: {txt(x)}   velocidad: {velocidades[k]}\n")

    # ---------------- 2) mejor propio inicial = donde esta ----------------
    print("=== 2) MEJORES PROPIOS INICIALES (cada una todavia solo conoce donde esta) ===")
    mejores_propios = []
    f_propios = []
    for k in range(n_particulas):
        mejores_propios.append(posiciones[k][:])
        f_propios.append(funcion(posiciones[k]))
        print(f"  particula {k}: mejor propio = {txt(mejores_propios[k])}   f = {f_propios[k]:9.3f}")
    print()

    historia = []
    fotos = []

    for it in range(iteraciones):
        detalle = it < ver

        # ---------------- 3) mejor global = el mejor de los mejores propios ----------------
        g = f_propios.index(min(f_propios))
        mejor_global = mejores_propios[g][:]
        historia.append(f_propios[g])
        fotos.append([x[:] for x in posiciones])

        if detalle:
            print(f"=== ITERACION {it} ===")
            print("  f de los mejores propios:", [round(v, 3) for v in f_propios])
            print(f"  el menor es el de la particula {g} -> mejor global = {txt(mejor_global)}  f = {f_propios[g]:9.3f}\n")

        # ---------------- 4) mover cada particula ----------------
        for k in range(n_particulas):
            if detalle:
                print(f"  -- particula {k} --  posicion {txt(posiciones[k])}  mejor propio {txt(mejores_propios[k])}")
            for i in range(dimensiones):
                r1 = random.random()
                r2 = random.random()
                v_vieja = velocidades[k][i]
                x_vieja = posiciones[k][i]
                inercia = w * v_vieja
                cognitivo = c1 * r1 * (mejores_propios[k][i] - x_vieja)     # hacia su mejor
                social = c2 * r2 * (mejor_global[i] - x_vieja)              # hacia el mejor del enjambre
                velocidades[k][i] = inercia + cognitivo + social
                posiciones[k][i] = x_vieja + velocidades[k][i]

                a, b = limites[i]
                recorte = ""
                if posiciones[k][i] < a:
                    posiciones[k][i] = a
                    recorte = f"  (se salio: queda en el borde {a})"
                if posiciones[k][i] > b:
                    posiciones[k][i] = b
                    recorte = f"  (se salio: queda en el borde {b})"

                if detalle:
                    print(f"     dim {i}: r1={r1:.2f} r2={r2:.2f}")
                    print(f"            inercia   w*v            = {w}*{v_vieja:.2f} = {inercia:8.2f}")
                    print(f"            cognitivo c1*r1*(y - x)  = {c1}*{r1:.2f}*({mejores_propios[k][i]:.2f} - {x_vieja:.2f}) = {cognitivo:8.2f}")
                    print(f"            social    c2*r2*(g - x)  = {c2}*{r2:.2f}*({mejor_global[i]:.2f} - {x_vieja:.2f}) = {social:8.2f}")
                    print(f"            v nueva = {velocidades[k][i]:8.2f}   x nueva = {x_vieja:.2f} + {velocidades[k][i]:.2f} = {posiciones[k][i]:8.2f}{recorte}")

            # ---------------- 5) actualizar el mejor propio ----------------
            f_nueva = funcion(posiciones[k])
            if f_nueva < f_propios[k]:
                if detalle:
                    print(f"     f nueva = {f_nueva:9.3f} < f del mejor propio {f_propios[k]:9.3f}  -> MEJORO, nuevo mejor propio")
                f_propios[k] = f_nueva
                mejores_propios[k] = posiciones[k][:]
            elif detalle:
                print(f"     f nueva = {f_nueva:9.3f} >= {f_propios[k]:9.3f}  -> no mejoro, el mejor propio queda donde estaba")
            if detalle:
                print()

        if not detalle and (it % 10 == 0 or it == iteraciones - 1):
            print(f"iteracion {it:3d}: mejor f del enjambre = {historia[-1]:9.3f}   en {txt(mejor_global)}")

    g = f_propios.index(min(f_propios))
    print(f"\nRESULTADO: mejor posicion {txt(mejores_propios[g])}   f = {f_propios[g]:.3f}")
    return mejores_propios[g], f_propios[g], historia, fotos


if __name__ == "__main__":
    random.seed(1)
    # pocas particulas para que los prints se puedan leer
    enjambre(f1, [(-512, 512)], n_particulas=3, iteraciones=30, ver=2)
    # enjambre(f2, [(-100, 100), (-100, 100)], n_particulas=3, iteraciones=30, ver=1)
