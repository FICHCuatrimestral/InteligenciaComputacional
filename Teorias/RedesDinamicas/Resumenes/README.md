# Apuntes — Redes neuronales dinámicas

Inteligencia Computacional · FICH-UNL · Diego Milone

| Archivo | Qué es |
|---|---|
| `01-redes-dinamicas.md` | La unidad completa: por qué dinámicas, clasificación, Hopfield (arquitectura, Hebb con ejemplo numérico, recuperación con traza paso a paso, la función de energía y por qué converge), BPTT con la derivación entera y la versión optimizada, TDNN, Elman y Jordan, el cuadro de toda la materia, cuatro derivaciones para pizarra y formulario |

Fuentes: `Redes neuronales dinámicas.pdf` (39 diapositivas), `Redes neuronales dinámicas 2 (extensión de BPTT notas completas).pdf` (11 páginas) y las transcripciones 026 a 031.

## Lo que hay que saber de las fuentes

- **El segundo PDF es el corazón del tema.** Tiene la derivación completa de BPTT que las diapositivas no traen y que la clase 030 tampoco da, más una sección de BPTT optimizado ($\delta^*$, $O(T)$) que no se dio en clase.
- **Cuatro bloques de diapositivas están vacíos o ilegibles**: las tres aproximaciones (3–6, sólo ecuaciones), los campos energéticos (29, dos viñetas), la arquitectura TDNN (36, sólo el título) y Elman/Jordan (38–39, diagramas minúsculos). Las figuras 1, 6, 10 y 12 del apunte los reconstruyen desde las transcripciones.
- **Dos errores en las notas de BPTT**, en la sección 12 del apunte: el índice del factor $\varphi'$ en el aporte indirecto (va $j$, dice $i$) y el $\tfrac{1}{2}$ que falta en la derivada de la sigmoide.
- **La función de energía no está en las diapositivas.** La sección 6 del apunte la escribe y demuestra que $\Delta E \le 0$, que es lo que explica la convergencia y por qué la simetría de $\mathbf{W}$ es indispensable. Está marcada como complemento.
- **Clase y notas difieren** sobre los pesos compartidos: la clase habla de "promediación ponderada", las notas suman. Vale la suma.

## Carpetas

- `../imagenes/` — los PNG y el script de Python que los genera.
- `../Transcripciones/` — las transcripciones de las clases.
- `../build/` — el filtro y el estilo para regenerar el PDF con Pandoc.

## Regenerar

```bash
python3 ../imagenes/graficos_dinamicas.py
../build/construir.sh 01-redes-dinamicas.md
```
