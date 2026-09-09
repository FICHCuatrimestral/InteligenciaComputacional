# Apuntes — Redes con funciones de base radial

Inteligencia Computacional · FICH-UNL · Diego Milone

| Archivo | Qué es |
|---|---|
| `01-redes-de-base-radial.md` | La unidad completa: por qué radiales, arquitectura, modelo, $k$-medias, LMS de la salida, gaussianas $N$-dimensionales, comparación con MLP, el ejemplo de seis patrones resuelto de punta a punta, derivaciones para pizarra y formulario |

Fuentes: `Redes con funciones de base radial.pdf` (55 diapositivas) y las transcripciones 015 a 018.

## El ejemplo que atraviesa el apunte

Seis patrones en $\mathbb{R}^1$ —$x = 0,1,2,3,4,5$ con $d = +1,+1,-1,-1,+1,+1$— y tres neuronas
radiales. Cada sección tiene un recuadro **EN NÚMEROS** que aplica sobre ese caso lo que se acaba de
explicar, y la sección 11 lo resuelve entero, de los datos crudos a la red entrenada. Los recuadros
**EN CRIOLLO** dan la analogía en palabras de cada concepto, para poder explicarlo sin ecuaciones.
Las figuras 14 a 19 son las del ejemplo.

## Lo que hay que saber de las fuentes

- **Cinco diapositivas están vacías** (sólo el título): la 4 *Funciones sigmoideas*, la 5 *Funciones radiales*, la 11 y la 12 *Arquitectura*, y la 44 *Comparación RBF-NN vs. MLP*. El profesor dibujaba en el pizarrón. Las figuras 1, 2, 3, 5, 10 y 11 del apunte reconstruyen esos dibujos a partir de su descripción hablada.
- **Dos constantes de normalización están mal** en las diapositivas 53 y 54 (ver el recuadro OJO de la sección 9). En la red no molestan; en el pizarrón sí.
- **El error cambia de signo** respecto de la unidad del perceptrón: acá es $e_k = y_k - d_k$ y la regla resta. Está en la sección 8.3.

## Carpetas

- `../imagenes/` — los PNG y el script de Python que los genera.
- `../Transcripciones/` — las transcripciones de las clases.
- `../build/` — el filtro y el estilo para regenerar el PDF con Pandoc.

## Regenerar

Las figuras:

```bash
python3 ../imagenes/graficos_rbf.py
```

El PDF (necesita Pandoc y XeLaTeX), desde esta carpeta:

```bash
../build/construir.sh 01-redes-de-base-radial.md
```
