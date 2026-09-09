# Apuntes — Capacidad de generalización

Inteligencia Computacional · FICH-UNL · Diego Milone

| Archivo | Qué es |
|---|---|
| `01-capacidad-de-generalizacion.md` | La unidad completa: superficies de error, sobre-entrenamiento, sesgo y varianza, corte temprano, conjunto de monitoreo, validación cruzada y sus variantes, medidas de desempeño en clasificación y en predicción, formulario y autoevaluación |

Fuentes: `Capacidad de generalización.pdf` (50 diapositivas) y las transcripciones 001 a 008.

## Lo que hay que saber de las fuentes

- **La unidad es casi toda pizarrón.** Las diapositivas 3, 4 y 5 (superficies de error en una y dos dimensiones), la 9 y la 10 (el planteo del problema) y la 15 y la 16 (las preguntas sobre cómo evitar el sobre-entrenamiento) tienen sólo el título o una pregunta suelta. **Las trece figuras del apunte están generadas de cero** a partir de la descripción hablada; ninguna es una captura de la cátedra.
- **Las curvas de sobre-entrenamiento de las diapositivas 12 a 16 no tienen números ni ejes rotulados.** Las figuras 4 y 5 del apunte las reconstruyen con ejes y escala.
- **Los ejemplos numéricos del apunte son corridas reales**, no estimaciones: los porcentajes de la tabla de la sección 3.2 salen de entrenar tres modelos con una partición de prueba del 35 %, los MSE de la sección 3.3 de los ajustes polinómicos de la figura 7, y las siete medidas de la sección 6.4 de la matriz de confusión $28/3/2/52$ que usa el profesor en clase.
- **Las ocho transcripciones son distintas entre sí** (verificado por md5) y cubren la unidad completa sin huecos.

## Carpetas

- `../imagenes/` — los PNG y el script de Python que los genera.
- `../Transcripciones/` — las transcripciones de las clases.
- `../build/` — el filtro y el estilo para regenerar el PDF con Pandoc.

## Regenerar

Las figuras (necesita `matplotlib`, `numpy` y `scikit-learn`):

```bash
python3 ../imagenes/graficos_generalizacion.py
```

El PDF (necesita Pandoc y XeLaTeX), desde esta carpeta:

```bash
../build/construir.sh 01-capacidad-de-generalizacion.md
```
