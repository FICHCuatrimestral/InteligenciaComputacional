# Apuntes — Inteligencia colectiva y algoritmos evolutivos

Inteligencia Computacional · FICH-UNL

| Archivo | Qué es |
|---|---|
| `01-inteligencia-colectiva.md` | La clase introductoria del bloque: autómatas ($A=\langle X,Y,E,D\rangle$, reglas deterministas y probabilísticas), autómatas celulares ($R=\langle A,T,C\rangle$, topologías, vecindades de von Neumann y Moore, juego de la vida), agentes y sistemas multiagente, y las características de la inteligencia colectiva, con la estigmergía como pregunta de parcial |
| `02-algoritmos-evolutivos.md` | El tema completo: Lamarck y Darwin, el algoritmo (pseudocódigo de la diapositiva y versión con las cinco piezas), representación (decodificación, Gray, los cinco ejemplos del pizarrón, representación fenotípica), aptitud (las cuatro características y los ejemplos con fórmula), selección (ruleta, los dos mares con números, re-escalado, ventanas, competencias, tabla comparativa), cruza y mutación (tasas, multipunto, rol de cada operador, operadores reales), reemplazo (brecha y elitismo), características y teorema de los esquemas, paralelismo, **Lamarck para acelerar la convergencia**, cómo encarar «proponga un algoritmo evolutivo para…», desarrollos para el pizarrón, formulario, errores típicos y autoevaluación |

## Lo que hay que saber de las fuentes

- **Las diapositivas son casi todas títulos.** Los ejemplos de representación y de aptitud (figuras en un área, red, robot, filtro, viajante), la ruleta y el rol de cada operador se desarrollaron en el pizarrón: el apunte los reconstruye de las transcripciones, con figuras propias.
- **`Transcripciones/001.txt` y `transcripcion-001.txt` son el mismo archivo** (mismo md5). Se puede borrar uno.
- **Los parciales 2013–2018 preguntan más que la clase:** restricciones (cuatro de seis), representaciones fenotípicas y sus operadores, cruza múltiple, estrategias evolutivas y Lamarck para acelerar la convergencia. Eso se armó con Engelbrecht (caps. 8, 9, 12, ap. A), Mitchell (caps. 1, 3, 4) y Goldberg, de `Bibliografía/`, y está marcado.
- **Dos correcciones a la clase:** el ejemplo de tasas de mutación compara 1 % con 10 % (se rehízo con la misma tasa), y el teorema de los esquemas no «asegura la convergencia»: es una cota sobre el crecimiento esperado de un esquema en una generación.
- **Matiz en el mar de mediocres:** la clase dice que el bueno queda ahogado; la simulación muestra que, si se elige la generación entera, el bueno no se pierde y se adueña de la población en 4 generaciones (convergencia prematura). El apunte da las dos caras.

## Números del apunte

Todos salen de `../imagenes/graficos_evolutivos.py` (AG binario propio: ruleta, ventanas o competencia; cruza simple; mutación por gen; reemplazo total, brecha o elitismo).

| Afirmación | Verificación |
|---|---|
| Vecindades | von Neumann 4 y 12; Moore 8 y 24 vecinos (radio 1 y 2) |
| Planeador | a los 4 pasos, misma forma corrida una celda en diagonal |
| Jirafas | media del cuello 1,00 → 1,26 (gen. 10) → 1,41 (gen. 40) |
| Mar de mediocres | tajada 1 %; no sale en 2 tiradas con prob. 0,98, en 198 con 0,14; en 991 espera 9,9 copias; sólo con selección nunca se pierde (200 corridas) y ocupa el 90 % en 4 generaciones |
| Mar de virtuosos (copias del mejor) | ruleta 0,98; ventanas 2,61; competencia $k=2$ 1,96, $k=5$ 5,00 |
| Cruza y mutación | 38 hijos, todos repiten la $x$ o la $y$ de un padre; mutantes de un bit: mediana 4,7, 6 de 20 saltan más de 25 |
| Tasas de mutación | 1 %: 1 individuo o 10 genes (9,6 % de individuos); 10 %: 10 individuos o 100 genes (65 %) |
| Gray | 7 → 8: Hamming 4 en binario, 1 en Gray |
| Ejemplo 1 | AG 30/30 llega a $f<0{,}5$ (mediana 0,02); gradiente 0/30 (mediana 12,7) |
| Elitismo | el mejor empeora 0 veces con elitismo, mediana 64 veces sin él (20 semillas, 150 gen.) |
| Penalización | $(x-3)^2$, $x\le2$: cuadrática $\lambda=100$ → 2,01; lineal $\lambda=10$ → 2,00 |
| Viajante | la cruza simple repite 2 y 4 y pierde 5 y 7; la cruza de orden da `7 1 3 4 5 6 8 2` |
| Lamarck (Rastrigin 6-D, 20 semillas) | hasta $f<0{,}01$: AG solo 10/20 (306 gen.), baldwiniano 20/20 (56 gen.), lamarckiano 20/20 (16,5 gen., 4184 evaluaciones) |

Las restricciones (§12) y las otras ramas (§14) se desarrollan en `Teorias/10-AlgoritmosEvolutivosP2/Resumenes/01-variantes.md`; acá quedan sólo los punteros.

## Selección de características (§15)

Sale del repaso de la práctica 6 (`Practicas/TP6/repasoAG_introFS.pdf`), traducido y explicado. Los números son de `graficos_evolutivos.py` (clasificador k vecinos con validación cruzada, scikit-learn):

| Afirmación | Verificación |
|---|---|
| Reducción contra selección | proyección sobre $z$: 0,99; sólo $x_1$: 0,54 |
| Interacción (XOR) | sólo $x$ 0,51; sólo $y$ 0,47; las dos 1,00 |
| Redundancia | sólo $x$ 0,60; sólo $y$ 0,57; las dos 0,99 |
| 20 variables, útiles la 3 y la 11 | ranking: puestos 6 y 15; las 5 mejores del ranking 0,46; todas 0,74; el AG encuentra {3, 11} en 10/10 corridas (acierto 1,00), con ~5900 subconjuntos evaluados de $2^{20}$ |
| Combinatoria | $\binom{20}{5} = 15\,504$; $\binom{100}{50} = 1{,}01\times10^{29}$; $2^{7129} \approx 10^{2146}$ |

## Carpetas

- `../imagenes/`: los 22 PNG y el script que los genera (numpy y matplotlib; tarda menos de un minuto).
- `../imagenes/mermaid/`: los diagramas Mermaid ya dibujados (un PNG por diagrama, con nombre = sha1 del bloque) y `tema.json`, los colores de los diagramas.
- `../build/`: el filtro y el estilo. El filtro reemplaza cada bloque ` ```mermaid ` del `.md` por su PNG; si el diagrama cambió y falta el PNG, lo genera con `mmdc` (mermaid-cli). En GitHub, los mismos bloques se ven como diagramas directamente.

## Regenerar

```bash
python3 ../imagenes/graficos_evolutivos.py
../build/construir.sh 01-inteligencia-colectiva.md
../build/construir.sh 02-algoritmos-evolutivos.md
```

El filtro necesita Pandoc 3 (usa `pandoc.write`); con una versión anterior falla en los recuadros. Para regenerar diagramas Mermaid que cambiaron hace falta `npm i -g @mermaid-js/mermaid-cli`.
