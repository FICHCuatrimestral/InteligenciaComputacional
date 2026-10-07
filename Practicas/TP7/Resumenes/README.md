# Resumen — TP 7: enjambre de partículas y colonia de hormigas

Inteligencia Computacional · FICH-UNL

| Archivo | Qué es |
|---|---|
| `01-tp7.md` | Guía para defender `TP7.ipynb`: enjambre de partículas (velocidad término por término, una actualización a mano); ej. 1 contra el algoritmo genético; sistema de hormigas (probabilidad, lista tabú, evaporación, depósito global, uniforme y local, un paso a mano); ej. 2 viajante `gr17`; resultados con su interpretación, guion, formulario, errores típicos y autoevaluación |

## Números del resumen

Los resultados de las corridas salen de ejecutar `../TP7.ipynb`. Las cuentas de los ejemplos salen de `../imagenes/numeros_tp7.py`.

| Afirmación | Verificación |
|---|---|
| Ej. 1, $f_1$: AG 10/10 (llega en la iteración 27), enjambre 8/10 (3,5), promedio −396,03 | notebook, `tabla1` |
| Ej. 1, $f_2$: AG 8/10 (65), promedio 0,111; enjambre 10/10 (55), promedio 0,016 | notebook, `tabla2` |
| Las 2 corridas trabadas del enjambre terminan en $x$ = −512, $f_1$ = −304,23 | semillas 6 y 7 de `enjambre(f1, ...)` |
| Ej. 2: tabla de 12 configuraciones (largos, llegadas al óptimo, iteraciones, tiempos) | notebook, `tabla` |
| Ninguna corrida del ej. 2 termina por convergencia: todas llegan a 200 iteraciones | corrido aparte con las mismas semillas |
| Velocidad a mano: 0,365 − 0,75 − 2,4 = −2,785; $x$ = −0,785 | `numeros_tp7.py` |
| Probabilidades desde la ciudad 0 (6, 5, 2): 0,542 / 0,289 / 0,169 | `numeros_tp7.py` |
| Depósito con $L$ = 2100 y $d$ = 80: 0,00048 / 1 / 0,0125 | `numeros_tp7.py` |
| $0{,}99^{200}$ = 0,134; $0{,}5^{10}$ = 0,001 | `numeros_tp7.py` |

## Carpetas

- `../imagenes/`: los gráficos exportados del notebook y `numeros_tp7.py`.
- `../imagenes/mermaid/`: los diagramas Mermaid ya dibujados (nombre = sha1 del bloque) y `tema.json`.
- `../build/`: el filtro y el estilo, iguales a los de los resúmenes de teoría.

## Regenerar

```bash
python3 ../imagenes/numeros_tp7.py      # desde imagenes/
../build/construir.sh 01-tp7.md
```
