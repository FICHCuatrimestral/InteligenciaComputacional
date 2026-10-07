# Apuntes — Algoritmos evolutivos, segunda parte: variantes, hormigas y enjambres

Inteligencia Computacional · FICH-UNL

| Archivo | Qué es |
|---|---|
| `01-variantes.md` | Parámetros que evolucionan; estrategias de evolución (variables objetivo y de control, mutación gaussiana, regla de 1/5, $(\mu+\lambda)$ y $(\mu,\lambda)$); representación binaria o real y epistasis; longitud variable; programación genética (árboles, cruza y mutación de ramas); las cinco formas de considerar las restricciones |
| `02-colonias-de-hormigas.md` | Inspiración y estigmergía; puente binario; el modelo ($G$, $\sigma_{ij}$, $N_i$, $\mathbf{p}_k$); sACO (probabilidad con $\alpha$, ciclos, evaporación, depósito, una iteración a mano); AS ($\eta=1/d$ con $\beta$, lista tabú, depósito global, uniforme y local); parámetros |
| `03-enjambre-de-particulas.md` | Inspiración (cognitivo y social); el modelo ($\mathbf{x}_k$, $\mathbf{v}_k$, $\mathbf{y}_k$, $\hat{\mathbf{y}}$); mejor global (estrella) y mejor local (anillo por índices); la velocidad término por término con un ejemplo a mano; inercia y $V_{\max}$; comparación con algoritmo genético y hormigas |

Cada apunte tiene mapa mental, diagramas de flujo de los algoritmos, guion para el pizarrón, formulario, errores típicos y autoevaluación.

## Números de los apuntes

Todos salen de `../imagenes/graficos_enjambres.py` (numpy y matplotlib).

| Afirmación | Verificación |
|---|---|
| Regla de 1/5, $(1+1)$, $x^2+y^2$ desde (8, 6) | $f$ final mediano (20 corridas, 600 iteraciones): $\sigma$ fijo $1{,}9\times10^{-3}$; regla de 1/5 $3{,}6\times10^{-6}$ |
| $(\mu+\lambda)$ contra $(\mu,\lambda)$, Rastrigin 5-D, 10/70 | final 2,98 contra 6,96; el mejor empeora alguna vez en 0 % contra 100 % de las corridas |
| Epistasis, 0–100 en 7 bits | 27 de 128 valores inválidos (21 %); 69 de 707 mutaciones de un bit vuelven inválido un valor válido (9,8 %); reescalado: resolución 0,79 |
| Cruza en programación genética | tablas (00, 01, 10, 11): padres 1110 y 1001; hijos 1101 y 1000 |
| Puente binario (ramas 1 y 2) | la corta se queda con > 90 % en 30/30 corridas; ramas iguales: siempre elige una, la 0 en 57 % |
| Probabilidad con $\alpha$ ($\sigma$ = 0,20; 0,21; 0,19) | $\alpha=1$: 0,333/0,350/0,317; $\alpha=20$: 0,249/0,661/0,089 |
| AS con $d$ = 1, 2, 4 | $\beta=1$: 0,567/0,298/0,135; $\beta=2$: 0,757/0,199/0,045 |
| Iteración a mano | conexiones a 0,59 y 0,423; $p_{OA}$ = 0,582 (sACO) y 0,736 (AS, $\beta=1$) |
| sACO en cuadrícula 6 × 6 con pared | camino medio 16,3 → 13,0; mínimo (BFS) 13 |
| Evaporación y $\alpha$ (ramas 1 y 1,5) | corta > 90 %: $\rho=0$ 37 %; $\rho=0{,}1$ 95 %; $\alpha=2$ 70 % (larga 30 %) |
| AS en viajante de 12 ciudades | óptimo exacto (Held-Karp) 35,60; $\beta=0$: 1,29 × óptimo, 0 %; $\beta=2$: óptimo en 90 % (global), 100 % (uniforme y local) |
| Velocidad a mano | $\mathbf v$ nueva $(-2{,}65;\ -3{,}4)$, $\mathbf x$ nueva $(-0{,}65;\ -0{,}4)$ |
| Inercia, esfera 2-D | $\lvert v\rvert$ a las 150 iteraciones: $w=1$ $7\times10^4$; $\lvert v\rvert\le1$ 0,89; $w=0{,}7$ $4{,}5\times10^{-6}$ |
| Global contra local, Rastrigin 10-D | a 50 iteraciones 31,7 contra 35,0; dispersión a 60: 1,65 contra 4,98; final 9,0 contra 8,5 |

## Carpetas

- `../imagenes/`: los PNG y el script que los genera (`python3 graficos_enjambres.py [función …]`).
- `../imagenes/mermaid/`: los diagramas Mermaid ya dibujados (nombre = sha1 del bloque) y `tema.json`.
- `../build/`: el filtro y el estilo, iguales a los de la unidad 09.

## Regenerar

```bash
python3 ../imagenes/graficos_enjambres.py
../build/construir.sh 01-variantes.md
../build/construir.sh 02-colonias-de-hormigas.md
../build/construir.sh 03-enjambre-de-particulas.md
```
