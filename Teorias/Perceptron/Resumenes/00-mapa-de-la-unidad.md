---
title: "Mapa de la unidad: del perceptrón simple a back-propagation"
subtitle: "Inteligencia Computacional · FICH-UNL \\newline Una carilla para ubicarse antes de estudiar, y para repasar la estructura el día antes"
lang: es
---

## El recorrido completo

![Cada caja responde una pregunta, y esa respuesta abre la siguiente. El color indica en qué apunte está desarrollada.](imagenes/22-mapa-unidad.png)

---

## La unidad en ocho preguntas

Si podés contestar estas ocho, tenés la estructura. Los detalles están en los apuntes; esto es el andamio.

| # | La pregunta | La respuesta, en una línea |
|:---:|---|---|
| 1 | ¿Qué hace una neurona? | Un producto interno y una decisión: $y = \varphi(\langle w,x\rangle)$ |
| 2 | ¿Qué puede decidir? | Sólo lo que separa un hiperplano: problemas **linealmente separables** |
| 3 | ¿Cómo aprende? | Moviendo $w$ en contra del gradiente del error. La regla intuitiva y la formal dan **lo mismo** |
| 4 | ¿Dónde se rompe? | En el XOR. Y no por mal entrenamiento: **no existe** un $w$ que lo resuelva |
| 5 | ¿Cómo se arregla? | Con una capa más. La capa oculta **cambia la representación**: en su espacio el problema sí es separable |
| 6 | ¿Cuánta profundidad hace falta? | Una capa: semiplanos. Dos: regiones convexas. Tres: cualquier región |
| 7 | ¿Cómo se entrena eso? | Mismo gradiente, pero con $\varphi$ derivable: $\Delta w_{ji} = \mu\,\delta_j\,y_i$ |
| 8 | ¿Y el error de una neurona oculta, que nadie mide? | Se reconstruye: los $\delta$ de la capa siguiente vuelven por los mismos pesos |

---

## Dónde está cada cosa

| Tema | Archivo | Sección |
|---|---|---|
| Neurona biológica, modelo, activaciones, geometría, sesgo, corrección de error | `01-perceptron-simple.md` | 1 a 6 |
| Método del gradiente y LMS, ejemplo numérico, el límite del XOR | `02-metodos-de-gradiente.md` | todo |
| XOR con tres neuronas: rectas, pesos, tabla de verdad, arquitectura | `03-xor-con-tres-neuronas.md` | 1 a 11 |
| Regiones de decisión y arquitectura general | `04-perceptron-multicapa.md` | 1 a 3 |
| Sigmoide, criterio de error, regla de la cadena | `04-perceptron-multicapa.md` | 4 a 6 |
| Los factores, el $\delta$ y la derivada de la activación | `04-perceptron-multicapa.md` | 7 a 10 |
| Capa de salida, capas ocultas, generalización, algoritmo | `04-perceptron-multicapa.md` | 11 a 15 |
| **Las siete deducciones para practicar en pizarra** | `05-derivaciones-para-pizarra.md` | D1 a D7 |

---

## Las cinco fórmulas que sostienen todo

$$
y = \varphi\big(\langle w, x\rangle\big)
\qquad\qquad
\xi(n) = \tfrac{1}{2}\sum_j e_j^2(n)
$$

$$
\varphi'(v_j) = \tfrac{1}{2}\big(1+y_j\big)\big(1-y_j\big)
\qquad\qquad
\Delta w_{ji}(n) = \mu\,\delta_j(n)\,y_i(n)
$$

$$
\delta^{(p)}_j = \Big[\textstyle\sum_k \delta^{(p+1)}_k\,w^{(p+1)}_{kj}\Big]\;\tfrac{1}{2}\big(1+y^{(p)}_j\big)\big(1-y^{(p)}_j\big)
$$

---

## Las seis frases

Las que conviene tener listas, porque contestan solas la mitad de lo que se puede preguntar:

1. **"El XOR no es un problema de entrenamiento, es un problema de modelo."** No existe solución con una recta; ninguna cantidad de épocas la va a encontrar.

2. **"La capa oculta no agrega potencia de cálculo, cambia la representación."** Cada neurona responde una pregunta binaria, y el vector de respuestas es una codificación nueva del patrón en la que el problema ya es fácil.

3. **"Tres capas resuelven cualquier problema, pero eso es existencia, no aprendizaje."** La arquitectura lo permite; encontrar los pesos es otra cosa y no está garantizado.

4. **"Se cambia el signo por la sigmoide porque hay que derivar."** El método del gradiente exige una activación derivable, y $\mathrm{sgn}$ tiene una discontinuidad justo donde importa.

5. **"Back-propagation es el LMS con el error corregido."** Misma estructura —$\mu$, algo local de la neurona, la entrada— con el error crudo reemplazado por el $\delta$.

6. **"Retropropagación quiere decir que los $\delta$ atraviesan los mismos pesos, al revés."** Hacia adelante se usan las filas de $\mathbf{W}$; hacia atrás, las columnas.

---

## Los cuatro errores que hay que no cometer

- **Perder un signo.** Hay seis lugares donde se cancela un menos; están listados al final de `05-derivaciones-para-pizarra.md`.
- **Confundir $y_i$ con $y_j$.** La primera es la entrada por la conexión, la segunda la salida de la neurona. Se diferencian por un subíndice.
- **Contar mal las capas.** En esta materia son capas **de neuronas**: las entradas no cuentan. La red del XOR es de dos capas.
- **Mezclar las dos sigmoides.** La simétrica va de $-1$ a $+1$; la logística de $0$ a $1$. Si copiás fórmulas de un libro que usa la otra, no cierra nada.
