# Métodos de gradiente aplicados al perceptrón simple

**Inteligencia Computacional — FICH-UNL — Diego Milone**
Apunte de estudio sobre las diapositivas 40–60 de *Perceptrón simple* y la transcripción de clase correspondiente.

---

## Convención de notación

Todo vector es **columna**. Para un perceptrón de $N$ entradas más el sesgo:

$$
w(n) = \begin{bmatrix} w_0 \\ w_1 \\ \vdots \\ w_N \end{bmatrix},
\qquad
x(n) = \begin{bmatrix} x_0 \\ x_1 \\ \vdots \\ x_N \end{bmatrix},
\qquad
x_0 = -1 \ \ \text{(entrada de sesgo)}, \quad w_0 = u \ \ \text{(umbral)}
$$

- $n$ es el índice de **iteración de entrenamiento** (equivalentemente, el patrón que se está mostrando).
- El producto interno $\langle w, x\rangle = w^{T}x = \sum_{i=0}^{N} w_i x_i$ es un **escalar**.
- La salida de la neurona es $y = \varphi\big(\langle w, x\rangle\big)$, con $\varphi$ la función de activación.
- $d(n)$ (o $y_d(n)$) es la **salida deseada** del patrón $n$; $e(n) = d(n) - y(n)$ es el **error**.

La entrada extendida con $x_0 = -1$ y $w_0 = u$ es lo que permite escribir el umbral como un peso más, y por lo tanto **aprenderlo con la misma regla que los demás**. Sin sesgo, la frontera de decisión pasa obligatoriamente por el origen.

---

## 1. Por qué existe esta parte

En la unidad anterior el aprendizaje se dedujo **por corrección de error**, con un argumento intuitivo:

> Si la salida es correcta, no se toca nada (principio de mínima perturbación). Si es incorrecta, se penaliza: se actualizan los $w_i$ en el sentido opuesto a aquel con el que contribuyeron a la salida incorrecta.

Eso da una regla que funciona, pero cuyo único sustento es el sentido común. Lo que se hace ahora es llegar **a la misma ecuación** por un camino formal: definir una función de error y minimizarla con **descenso por gradiente**.

> **Idea central para la defensa oral:** no hay un algoritmo nuevo. Hay una *justificación matemática* de un algoritmo que ya se tenía. El valor está en que ese camino formal es el que después **sí generaliza** al perceptrón multicapa, donde la intuición ya no alcanza.

---

## 2. El método de gradiente

### 2.1 La superficie de error

Pensemos el error como una **superficie** definida sobre el espacio de pesos. Con dos pesos se puede graficar literalmente: un eje para $w_1$, otro para $w_2$, y en vertical el error $\xi$.

- Cada combinación de pesos $(w_1, w_2)$ es un punto sobre esa superficie, con un valor de error asociado.
- En cada punto existe el **vector gradiente** $\nabla_w \xi$, que apunta hacia donde la superficie de error **crece** más rápido.
- Lo que se busca es el **mínimo**: la combinación de pesos con el menor error posible.

Como el gradiente apunta hacia donde el error crece, para bajar hay que moverse **en el sentido opuesto**.

### 2.2 Ecuación básica

$$
w(n+1) = w(n) - \mu\, \nabla_w \xi\big(w(n)\big)
$$

| Término | Significado |
|---|---|
| $w(n+1)$ | vector de pesos en la iteración siguiente |
| $w(n)$ | vector de pesos actual |
| $\nabla_w \xi$ | gradiente del error **respecto de los pesos** (vector columna, mismo tamaño que $w$) |
| $\mu$ | velocidad (o constante) de aprendizaje |
| signo $-$ | es *todo* el algoritmo: bajar en contra del gradiente |

### 2.3 El rol de $\mu$

- $\mu$ **grande** → pasos largos, se recorre rápido la superficie, pero se corre riesgo de pasarse del mínimo y oscilar o divergir.
- $\mu$ **chico** → convergencia lenta pero estable.
- Criterio práctico dado en clase: si la superficie es **suave**, se puede avanzar rápido; si es **escarpada o con muchos altibajos**, hay que moverse con más cuidado (y eventualmente con criterios adicionales, como $\mu$ variable o momento).

### 2.4 Detalle fino: por qué la figura es un paraboloide

No es una elección arbitraria del dibujo. Como se verá en la sección 3, en el **caso lineal con error cuadrático** la función de error es **cuadrática en $w$**, es decir **convexa**, con **un único mínimo global**. Por eso:

- el descenso por gradiente en este caso **converge al óptimo** (con $\mu$ razonable);
- esa garantía **se pierde** en el perceptrón multicapa, donde la superficie tiene mínimos locales, mesetas y regiones de gradiente casi nulo. Ahí el mismo método pasa a llamarse **back-propagation**.

### 2.5 Alcance del método

El mismo método sirve para dos casos:

- **Caso sencillo:** perceptrón simple → **LMS** (*least mean squares*, también llamado regla delta o Widrow-Hoff).
- **Caso general:** perceptrón multicapa → **back-propagation**.

---

## 3. Derivación para el perceptrón simple (caso lineal)

### 3.1 Criterio del error instantáneo

$$
e^2(n) = \big[d(n) - y(n)\big]^2 = \big[d(n) - \langle w(n), x(n)\rangle\big]^2
$$

Dos cosas para notar:

1. **Error cuadrático**: si la diferencia entre deseada y obtenida es cero, el error es cero; si es $+1$, $-1$, $+2$ o $-2$, el cuadrado da siempre positivo y penaliza fuerte las diferencias grandes. El signo del error no importa para el costo, sólo su magnitud.
2. **Se reemplazó $y$ por el producto interno.** Es decir, se pasó de $y = \varphi(\langle w,x\rangle)$ a $y = \langle w,x\rangle$: **se eliminó la función de activación**.

> **Esta es la simplificación clave, y en clase se remarca dos veces.** Se está analizando un **caso lineal**: la activación es la identidad, no $\mathrm{sgn}$ ni una sigmoide. Es una simplificación didáctica — entre otras cosas porque $\mathrm{sgn}$ ni siquiera es derivable. En las partes siguientes se rehace con la activación completa.

### 3.2 La derivada

Hay que calcular $\nabla_w e^2(n)$, o sea derivar **respecto de $w$**.

> **Punto donde se traba todo el mundo:** acá la variable es $w$. **$x(n)$ y $d(n)$ son constantes.** No se deriva respecto de $x$ como en Matemática.

Aplicando regla de la cadena sobre el cuadrado — se baja el 2, se deja el paréntesis como está, y se multiplica por la derivada de lo de adentro:

$$
\nabla_w e^2(n) = 2\big[d(n) - \langle w(n),x(n)\rangle\big] \cdot \nabla_w\big(d(n) - \langle w(n),x(n)\rangle\big)
$$

Analizando el paréntesis interior:

- $d(n)$ es una **constante que está sumando** al término que contiene la variable → su derivada es **cero**.
- $\langle w,x\rangle = \sum_{i=0}^{N} w_i x_i$: derivando respecto de cada $w_i$ queda $x_i$, así que el gradiente completo es el **vector columna $x(n)$**. Con el signo menos que lo precede, queda $-x(n)$.

Por lo tanto:

$$
\nabla_w e^2(n) = 2\big[d(n) - \langle w(n),x(n)\rangle\big]\,\big(-x(n)\big) = 2\,e(n)\,\big(-x(n)\big)
$$

### 3.3 Reemplazo en la ecuación del gradiente

$$
w(n+1) = w(n) - \mu\,\nabla_w \xi\big(w(n)\big) = w(n) - \mu\,\big[2\,e(n)\,(-x(n))\big]
$$

$$
\boxed{\;w(n+1) = w(n) + 2\mu\, e(n)\, x(n)\;}
$$

El menos del descenso se cancela con el menos de $-x(n)$: por eso la actualización queda **sumando**.

### 3.4 Consistencia dimensional

$$
\underbrace{w(n+1)}_{(N+1)\times 1} = \underbrace{w(n)}_{(N+1)\times 1} + 2\mu\,\underbrace{e(n)}_{\text{escalar}}\,\underbrace{x(n)}_{(N+1)\times 1}
$$

**Lectura geométrica:** $e(n)$ es un escalar y $x(n)$ un vector columna, así que la corrección $2\mu\,e(n)\,x(n)$ es un vector **en la dirección del patrón de entrada**, con magnitud proporcional al error y signo dado por si la salida se quedó corta o larga. Cada paso empuja a $w$ a lo largo de $x$.

---

## 4. Equivalencia con la regla intuitiva

La regla obtenida en la parte anterior era:

$$
w(n+1) = w(n) + \frac{\eta}{2}\big[y_d(n) - y(n)\big]\,x(n)
$$

La obtenida ahora, con $e(n) = d(n) - y(n)$:

$$
w(n+1) = w(n) + 2\mu\,e(n)\,x(n)
$$

Son **la misma ecuación**, con la única diferencia de la constante que multiplica. Igualando:

$$
\frac{\eta}{2} = 2\mu \quad\Longleftrightarrow\quad \eta = 4\mu
$$

Como la constante de aprendizaje se elige libremente, el número concreto no es el punto: lo relevante es que **la forma de la ecuación es idéntica**. Eso es exactamente lo que había que demostrar.

### 4.1 Detalle fino: de dónde sale el $\tfrac{1}{2}$

Con activación $\mathrm{sgn}$, las salidas son $\pm 1$, así que el error $e = d - y$ sólo puede tomar tres valores: $0$, $+2$ o $-2$. Entonces

$$
\frac{\eta}{2}\,e(n) \in \{0,\; +\eta,\; -\eta\}
$$

y la regla se lee, patrón por patrón:

- $y(n) = d(n)$ → $e = 0$ → **no se cambia nada** (mínima perturbación).
- $y(n) = +1$ y $d(n) = -1$ → $w(n+1) = w(n) - \eta\,x(n)$.
- $y(n) = -1$ y $d(n) = +1$ → $w(n+1) = w(n) + \eta\,x(n)$.

Es decir: **el $\tfrac{1}{2}$ está puesto para normalizar ese factor 2** que introduce la salida bipolar, y así recuperar exactamente la regla de corrección de error de las diapositivas 35–37.

### 4.2 Detalle fino: gradiente instantáneo (estocástico)

Se está minimizando $e^2(n)$, el error de **un solo patrón**, no el error medio sobre todo el conjunto de entrenamiento. Es decir, es un **gradiente instantáneo**: una aproximación ruidosa del gradiente verdadero.

Consecuencia práctica: cada ejemplo tira de los pesos para su lado. Por eso conviene $\mu$ **chico**, de modo que el promedio de muchos pasos pequeños aproxime el descenso real. Es la diferencia entre entrenamiento **estocástico / por patrón** y entrenamiento **por lote (batch)**.

---

## 5. Ejemplo numérico completo

### Estado inicial

$$
w(n) = \begin{bmatrix} +1 \\ +1 \\ +1 \end{bmatrix},
\qquad
x(n) = \begin{bmatrix} -1 \\ +1 \\ +1 \end{bmatrix},
\qquad
d(n) = -1
$$

Recordar que $x_0 = -1$ **siempre**: es la entrada de sesgo, no un dato del problema. Las entradas reales del patrón son $x_1 = +1$ y $x_2 = +1$.

### Paso 1 — salida actual

$$
\langle w,x\rangle = w^{T}x = \begin{bmatrix} +1 & +1 & +1 \end{bmatrix}\begin{bmatrix} -1 \\ +1 \\ +1 \end{bmatrix} = (-1) + (+1) + (+1) = +1
$$

$$
y(n) = \mathrm{sgn}(+1) = +1
$$

La salida deseada era $-1$, así que **hay error** y corresponde corregir los pesos.

### Paso 2 — error

$$
e(n) = d(n) - y(n) = -1 - (+1) = -2
$$

### Paso 3 — actualización

Se toma $\mu = \tfrac{1}{2}$, con lo cual $2\mu = 1$:

$$
w(n+1) = \begin{bmatrix} +1 \\ +1 \\ +1 \end{bmatrix} + 2\mu\,(-2)\begin{bmatrix} -1 \\ +1 \\ +1 \end{bmatrix}
= \begin{bmatrix} +1 \\ +1 \\ +1 \end{bmatrix} + \begin{bmatrix} +2 \\ -2 \\ -2 \end{bmatrix}
= \begin{bmatrix} +3 \\ -1 \\ -1 \end{bmatrix}
$$

### Paso 4 — verificación con el mismo patrón

$$
\langle w,x\rangle = \begin{bmatrix} +3 & -1 & -1 \end{bmatrix}\begin{bmatrix} -1 \\ +1 \\ +1 \end{bmatrix} = -3 - 1 - 1 = -5
$$

$$
y = \mathrm{sgn}(-5) = -1 \qquad\Longrightarrow\qquad e(n+1) = -1 - (-1) = 0
$$

**El error es cero: la neurona aprendió ese ejemplo en una sola iteración de actualización.**

### Observación crítica sobre este ejemplo

La fórmula se dedujo asumiendo salida **lineal** (sección 3.1), pero en el ejemplo se aplica $\mathrm{sgn}$. Es un atajo didáctico deliberado.

> Si en la defensa preguntan por esta inconsistencia, la respuesta correcta es: para el caso **no lineal** hay que derivar también $\varphi$, y por regla de la cadena aparece el factor $\varphi'\big(\langle w,x\rangle\big)$ en el gradiente. Eso es justamente lo que se desarrolla en las partes siguientes y lo que da lugar al término de **sensibilidad local** en back-propagation. Con $\mathrm{sgn}$ ese factor no existe (derivada nula o indefinida), y ése es uno de los motivos por los que se pasa a activaciones sigmoides.

---

## 6. Del ejemplo al entrenamiento real

Un solo ejemplo se corrige de una. Con un archivo de entrenamiento de 50 o 100 casos, no se puede corregir a fondo por cada patrón: se arregla uno y se rompe otro. De ahí las tres decisiones prácticas:

1. **$\mu$ pequeño**, para que la red aprenda "un poquito de cada uno" en lugar de saltar de patrón en patrón.
2. **Múltiples pasadas (épocas)** sobre todo el archivo de entrenamiento, mostrándolo muchas veces.
3. **Criterio de finalización**: que no se equivoque en ningún caso, o en la menor cantidad posible; o error por debajo de un umbral; o máximo de épocas alcanzado.

### Algoritmo completo

1. **Inicialización al azar**: $w(1) \in [-0.5,\ 0.5]$.
2. Para cada ejemplo de entrenamiento $x(n)\,|\,d(n)$:
   - obtener la salida: $y(n) = \varphi\big(\langle w(n), x(n)\rangle\big)$
   - adaptar los pesos: $w(n+1) = w(n) + 2\mu\, e(n)\, x(n)$
3. Volver a 2 hasta satisfacer el criterio de finalización.

> **Detalle fino:** la inicialización aleatoria en un rango chico y centrado en cero no es capricho. Valores grandes saturarían activaciones sigmoides (gradiente ≈ 0, no aprende), y valores todos iguales romperían la simetría necesaria cuando haya más de una neurona.

---

## 7. El límite: el problema del XOR

La última diapositiva plantea la trampa. Con las cuatro muestras dispuestas en diagonal —$(-1)$ y $(+1)$ cruzados— se prueba a ubicar la recta a mano:

- se la pone en una posición → queda mal clasificado un caso;
- se la desplaza usando el sesgo → sigue quedando mal otro caso;
- se la inclina → se clasifica mal uno o hasta dos casos.

**Donde sea que se ubique la recta, siempre hay al menos un caso mal clasificado.**

### La razón de fondo

El perceptrón simple genera una **frontera de decisión lineal**:

$$
\langle w, x\rangle = 0
$$

que en 2D es una recta y en general un **hiperplano**. Por lo tanto sólo puede resolver problemas **linealmente separables**. El **XOR (o exclusivo) no lo es**.

> **Esto es lo importante:** no es un problema de aprendizaje, ni de elegir bien $\mu$, ni de darle más épocas. El algoritmo funciona perfecto — es una **limitación estructural del modelo**. El OR y el AND sí son linealmente separables y el perceptrón los resuelve; el XOR no.

La salida es agregar capas: con neuronas ocultas se componen varias fronteras lineales y se obtienen regiones de decisión no convexas. Ése es el **perceptrón multicapa**, y para entrenarlo hace falta exactamente el método de gradiente desarrollado acá, extendido con la regla de la cadena a través de las capas: **back-propagation**.

---

## Resumen de fórmulas

| Concepto | Expresión |
|---|---|
| Salida del perceptrón | $y(n) = \varphi\big(\langle w(n), x(n)\rangle\big)$ |
| Entrada extendida | $x_0 = -1$, $w_0 = u$ |
| Error instantáneo | $e(n) = d(n) - y(n)$ |
| Criterio de costo | $e^2(n) = \big[d(n) - \langle w(n),x(n)\rangle\big]^2$ |
| Gradiente (caso lineal) | $\nabla_w e^2(n) = 2\,e(n)\,\big(-x(n)\big)$ |
| Ecuación básica del gradiente | $w(n+1) = w(n) - \mu\,\nabla_w \xi\big(w(n)\big)$ |
| **Regla LMS resultante** | $w(n+1) = w(n) + 2\mu\, e(n)\, x(n)$ |
| Regla por corrección de error | $w(n+1) = w(n) + \dfrac{\eta}{2}\big[d(n)-y(n)\big]x(n)$ |
| Equivalencia | $\eta = 4\mu$ |
| Frontera de decisión | $\langle w, x\rangle = 0$ |

---

## Puntos a tener listos para la defensa oral

1. **Por qué se usa gradiente si ya había una regla.** Porque el argumento formal es el que generaliza al multicapa; la intuición no.
2. **De dónde sale el signo menos** y por qué la actualización final queda sumando.
3. **Que se deriva respecto de $w$, con $x$ y $d$ constantes.**
4. **Que la deducción es para el caso lineal**, sin función de activación, y qué cambia al incluirla ($\varphi'$).
5. **Que la equivalencia $\eta = 4\mu$** hace que ambos caminos den lo mismo, y que el $\tfrac{1}{2}$ normaliza el factor 2 de las salidas bipolares.
6. **Que el gradiente es instantáneo**, no del error total, y qué implica para la elección de $\mu$.
7. **Que el XOR falla por limitación estructural**, no por entrenamiento.
