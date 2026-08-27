# Apuntes — Perceptrón simple y multicapa

Inteligencia Computacional · FICH-UNL · Diego Milone

Los archivos están **numerados en orden de lectura**. El `00` orienta, del `01` al `04` es la teoría en el orden de la cursada, y el `05` es para practicar.

| # | Archivo | Qué es | Cuándo usarlo |
|:---:|---|---|---|
| 00 | `00-mapa-de-la-unidad.md` | El recorrido completo en una carilla: 8 preguntas, 5 fórmulas, 6 frases | Antes de empezar, y el día antes del parcial |
| 01 | `01-perceptron-simple.pdf` | Neurona biológica, modelo, activaciones, geometría, sesgo, corrección de error | Primera pasada del tema |
| 02 | `02-metodos-de-gradiente.md` | Método del gradiente y LMS, ejemplo numérico, el límite del XOR | Después del 01 |
| 03 | `03-xor-con-tres-neuronas.md` | El XOR resuelto a mano con tres perceptrones | Después del 02 |
| 04 | `04-perceptron-multicapa.md` | Regiones de decisión, arquitectura, sigmoide y back-propagation completo | El más largo; es el corazón de la unidad |
| 05 | `05-derivaciones-para-pizarra.md` | Las 7 deducciones en pasos, con checkpoints y guion de pizarra | Para practicar, una vez entendido el resto |
| 06 | `06-implementacion-en-python.md` | La clase `PerceptronMulticapa` del TP2 mapeada contra las ecuaciones | Para defender el TP2 |

Cada `.md` tiene su `.pdf` al lado, generado desde el mismo archivo.

## Cómo está armado cada apunte

- **Tablas de claves** al final de cada sección: tapás el cuerpo y respondés en voz alta.
- **Recuadros** `IDEA DE FONDO`, `OJO` y `PARA LA DEFENSA` con los detalles finos.
- **Formulario**, **errores típicos** y **autoevaluación** al final.

## Dónde vive esto

```
Teorias/
  Perceptron/          <- esta carpeta
Practicas/
  TP1/  TP2/  ...
```

Los apuntes son personales y van en `Teorias/`; los TP, que se comparten con
los compañeros, van en `Practicas/`.

## Carpetas

- `imagenes/` — los PNG de los apuntes y los scripts de Python que los generan.
- `catedra/` — las diapositivas originales de Milone, tal como se descargaron.
- `Transcripciones/` — las transcripciones de las clases grabadas.
- `build/` — el filtro y el estilo para regenerar los PDF con Pandoc (opcional).

## Regenerar

Las figuras:

```bash
python3 imagenes/graficos_xor.py
python3 imagenes/graficos_multicapa.py
python3 imagenes/graficos_gradiente.py
python3 imagenes/graficos_derivaciones.py
```

Los PDF (necesita Pandoc y XeLaTeX):

```bash
./build/construir.sh 04-perceptron-multicapa.md
```
