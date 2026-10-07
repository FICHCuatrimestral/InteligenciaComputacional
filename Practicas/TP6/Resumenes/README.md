# Resumen — TP 6: algoritmos genéticos

Inteligencia Computacional · FICH-UNL

| Archivo | Qué es |
|---|---|
| `01-tp6.md` | Guía para defender `TP6-v3.ipynb`: el algoritmo genético (operadores con ejemplos, parámetros); ej. 1 contra gradiente descendiente; ej. 2 selección de genes (normalizar, prefiltro, 1 vecino, dejar uno afuera, UAR, β); resultados con su interpretación, guion, formulario, errores típicos y autoevaluación |

## Números del resumen

Los resultados de las corridas salen de ejecutar `../TP6-v3.ipynb` (dan idénticos a `TP6-v2.ipynb`). Las cuentas de los ejemplos salen de `../imagenes/numeros_tp6.py`.

| Afirmación | Verificación |
|---|---|
| Ej. 1: AG 10/10 en las dos funciones; gradiente 1/10 ($f_1$, promedio −158,35) y 0/10 ($f_2$, promedio 7,89) | notebook, celdas de `comparar` |
| Ej. 2: genes, cantidad y UAR de las 5 corridas; todos 0,76, top 10 0,93, AG 0,83 | notebook, tablas del ej. 2 |
| Sin prefiltro: UAR de test entre 0,48 y 0,79 | notebook (texto de la idea del ej. 2) |
| `1010` → 10 → $x$ = 170,67, $f_1$ = −81,46 | `numeros_tp6.py` |
| Resolución 0,001 y 0,0002; el más cercano a 0 es 0,0000954 y $f_2$ = 0,01996 | `numeros_tp6.py` |
| Evaluaciones: AG 10 050; gradiente 2000 y 4000 | `numeros_tp6.py` |
| Siempre ALL: 71 % de aciertos, UAR 0,5 | `numeros_tp6.py` |
| Aptitud con UAR 1: 0,992 / 0,988 / 0,984 (2, 3, 4 genes); un gen 0,004, un error 0,045 / 0,019 | `numeros_tp6.py` |
| Un error en test: 0,036 (AML), 0,025 (ALL) | `numeros_tp6.py` |

## Carpetas

- `../imagenes/`: los gráficos exportados del notebook y `numeros_tp6.py`.
- `../imagenes/mermaid/`: los diagramas Mermaid ya dibujados (nombre = sha1 del bloque) y `tema.json`.
- `../build/`: el filtro y el estilo, iguales a los de los resúmenes de teoría.

## Regenerar

```bash
python3 ../imagenes/numeros_tp6.py      # desde imagenes/
../build/construir.sh 01-tp6.md
```
