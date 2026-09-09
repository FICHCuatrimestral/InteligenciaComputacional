# Apuntes — Mapas auto-organizativos

Inteligencia Computacional · FICH-UNL · Diego Milone

| Archivo | Qué es |
|---|---|
| `01-mapas-autoorganizativos.md` | La unidad completa: auto-organización, arquitectura, vecindades y funciones de excitación lateral, el algoritmo de entrenamiento, las tres etapas, la formación de mapas topológicos (los siete ejemplos, reconstruidos), etiquetado y clasificación, cuantización vectorial, LVQ1, la demostración entera de LVQ1-O, cuatro desarrollos para pizarrón, formulario, errores típicos y autoevaluación |

Fuentes: `Mapas autoorganizativos.pdf` (62 diapositivas), las dos erratas (`023_errata.txt`, `025_errata.txt`) y las transcripciones 001 a 007.

## Lo que hay que saber de las fuentes

- **El bloque más importante de la unidad no está en las diapositivas.** "Formación de mapas topológicos" (láminas 29 a 36) son siete viñetas con el enunciado de cada ejemplo y ninguna figura: los ejemplos 1, 2 y 3 se desarrollaron enteros en el pizarrón (transcripciones 004 y 005). La sección 7 del apunte los reconstruye y los verifica con simulaciones.
- **La interpretación gráfica de LVQ1 tampoco está** (láminas 47 a 50: "Caso de clasificación correcta / incorrecta", sin dibujo). Es la figura 12.
- **La última diapositiva deja una demostración como tarea** ("Demostrar que $\alpha_c(n) = \alpha_c(n-1)/[1+s(n)\alpha_c(n-1)]$"). Va completa en la sección 12, en cuatro pasos, más la explicación de por qué hay que saturar en $\alpha = 1$ (que la cátedra menciona sin justificar).
- **Errata 025 — incorporada al apunte.** La diapositiva de LVQ1 escribe $c(n) = d(n)$; va $\mathcal{C}(c(n)) = d(n)$, la **clase** del prototipo ganador. $c(n)$ es un índice y $\mathbf{m}_{c}$ un vector de $\mathbb{R}^N$: comparar eso con una clase no tiene sentido dimensional.
- **Errata 023** (dirección del movimiento del centroide de la neurona 1 en el ejemplo del entorno): la figura 6 del apunte dibuja el caso correcto, cada neurona corriéndose hacia el patrón que entró.
- **La clase agrega el mapa hexagonal**, que la lámina de vecindades no muestra. Está en la figura 2.
- **Las tres etapas son criterios prácticos**, no resultados teóricos — el profesor lo repite dos veces. El apunte los da como tales y los verifica: sin la etapa de ordenamiento la malla queda anudada (1328 cruces contra 0).

## Números del apunte

Todos salen de corridas reales de `../imagenes/graficos_som.py`:

| Afirmación | Verificación |
|---|---|
| Sin entorno el SOM es $k$-medias | 4 neuronas, 4 grupos: peor peso a 0,042 del centro de su grupo |
| El entorno produce ordenamiento topológico | Mapa $6\times6$, 8 semillas: vecinas a 0,38 con entorno, a 1,09 sin entorno (pares cualesquiera: 1,06 en ambos) |
| Hace falta la etapa de ordenamiento | 0 cruces de la malla con ella, 1328 sin ella |
| El SOM etiquetado clasifica | 3 clases gaussianas, mapa $6\times6$: 100 % sobre 180 patrones de prueba, etiquetas en regiones conexas |
| LVQ1 converge | 600 patrones, 4 prototipos: error de 1,33 % a 0,17 % en 40 épocas |
| La $\alpha$ óptima iguala el peso de todos los patrones | Relación último/primer patrón: $1{,}4\times10^{9}$ con $\alpha$ constante, **1,000000** con la regla óptima |

## Carpetas

- `../imagenes/` — los 14 PNG y el script de Python que los genera.
- `../Transcripciones/` — las transcripciones de las clases.
- `../build/` — el filtro y el estilo para regenerar el PDF con Pandoc.

## Regenerar

```bash
python3 ../imagenes/graficos_som.py
../build/construir.sh 01-mapas-autoorganizativos.md
```
