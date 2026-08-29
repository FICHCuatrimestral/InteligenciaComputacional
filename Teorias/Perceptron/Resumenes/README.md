# Apuntes — Perceptrón simple y multicapa

Inteligencia Computacional · FICH-UNL · Diego Milone

Tres apuntes, en orden de lectura.

| # | Archivo | Qué es | Páginas |
|:---:|---|---|:---:|
| 01 | `01-perceptron-simple-y-gradiente.md` | Del modelo de neurona al límite del XOR: activaciones, geometría, sesgo, corrección de error, **método del gradiente y LMS**, y el XOR resuelto a mano con tres perceptrones | 21 |
| 02 | `02-perceptron-multicapa.md` | Regiones de decisión, arquitectura general, sigmoide y **back-propagation** completo | 27 |
| 03 | `03-implementacion-en-python.md` | El código del TP2 mapeado contra las ecuaciones, y el ejercicio 2 resuelto | 7 |

Cada `.md` tiene su `.pdf` al lado.

## El hilo del gradiente

Es el tema que más se reparte, así que conviene tenerlo ubicado:

| Dónde | Qué agrega |
|---|---|
| `01` §6 | La regla intuitiva, sin gradiente todavía |
| `01` §7 | La idea: superficie de error, $\Delta w = -\mu\nabla\xi$, el rol de $\mu$, la justificación por Taylor |
| `01` §8 | La derivación en el caso lineal → LMS |
| `01` §9 | Las dos reglas son la misma ($\eta = 4\mu$), pero no el mismo algoritmo |
| `01` §12 | El límite: en el XOR no existe el $w$ |
| `02` §6 | La misma ecuación por peso individual, y aparece la regla de la cadena |
| `02` §7 a §13 | Resolver cada eslabón y evaluar el $\delta$ en salida, en oculta y en capa $p$ |

Es **una sola ecuación**; lo que cambia es qué hay entre el peso y el error. En el `01` no hay nada (salida lineal, una neurona). En el `02` hay una sigmoide y varias capas, y por eso aparece la cadena.

## Cómo está armado cada apunte

- **Tablas de claves** al final de cada sección: tapás el cuerpo y respondés en voz alta.
- **Recuadros** `IDEA DE FONDO`, `OJO` y `PARA LA DEFENSA` con los detalles finos.
- **Cajas "Para la pizarra"** dentro de las secciones que las necesitan: el paso a paso de la deducción, con checkpoints y trampas.
- **Formulario**, **errores típicos** y **autoevaluación** al final.

## Carpetas

- `../imagenes/` — los PNG y los scripts de Python que los generan.
- `../Transcripciones/` — las transcripciones de las clases.
- `../build/` — el filtro y el estilo para regenerar los PDF con Pandoc.

## Regenerar

```bash
../build/construir.sh 02-perceptron-multicapa.md
```
