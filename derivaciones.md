---
title: "Las deducciones, paso a paso"
subtitle: "Inteligencia Computacional · FICH-UNL · cada línea de cada deducción, con qué se hizo y por qué"
lang: es
---

*`algoritmos.pdf` dice qué hace cada algoritmo. Este apunte dice **de dónde salen** sus fórmulas: las deducciones que se piden en el pizarrón, una línea por vez. Cada paso tiene un título que dice **qué movimiento se hace** —«aplico la regla de la cadena», «reemplazo por la definición»— y debajo por qué. La idea es que nunca estés escribiendo una línea sin saber qué operación estás haciendo.*

# Cómo leer una deducción

Casi todas las deducciones de la materia usan **los mismos seis movimientos**, repetidos en distinto orden. Si reconocés cuál estás haciendo en cada renglón, la deducción deja de ser una tira de símbolos y pasa a ser una receta.

| # | Movimiento | Cuándo se usa | Qué pinta tiene |
|---|---|---|---|
| **M1** | **Regla de la cadena** | lo que querés derivar no depende directo de la variable, sino a través de otras | partir una derivada en un producto de derivadas |
| **M2** | **Sobrevive un solo término** | derivás una sumatoria respecto de *una* de sus variables | $\frac{\partial}{\partial x_j}\sum_k f(x_k) = f'(x_j)$ |
| **M3** | **Lo que no depende de la variable, da cero** | hay constantes o términos de otras variables | $\frac{\partial d}{\partial w} = 0$ |
| **M4** | **Reemplazar por la definición** | aparece un símbolo que tiene fórmula conocida | $e = d-y$, $v = \sum w\,y$, $\xi = \frac12\sum e^2$ |
| **M5** | **Reconocer algo ya bautizado** | en el resultado aparece una expresión que ya tiene nombre | «eso de ahí adentro **es** $\delta_k$» |
| **M6** | **Juntar y simplificar** | quedaron factores sueltos | signos que se cancelan, factores comunes |

> **IDEA DE FONDO — la pregunta que hay que hacerse antes de cada renglón**
> *«¿Respecto de qué estoy derivando, y de qué depende esto?»* Si lo que tenés arriba depende de la variable **directamente**, derivás. Si depende **a través de otra cosa**, es M1. Si es una suma y sólo uno de los términos contiene la variable, es M2. Casi todos los errores de pizarrón son olvidarse de esa pregunta.

Y una regla de oro: **escribí primero el resultado al que querés llegar**. Una deducción se entiende mucho mejor cuando sabés adónde va. Por eso cada una de las de abajo arranca con **«Adónde quiero llegar»**.

---

# 1. El descenso por gradiente

**Adónde quiero llegar:** $\;\mathbf{w}(n+1) = \mathbf{w}(n) - \mu\,\nabla_{\mathbf{w}}\xi\;$ y por qué eso baja el error.

**La estrategia:** aproximar el error cerca del punto actual con una recta (Taylor), y ver qué pasa si me muevo en contra del gradiente.

**Paso 1 — Planteo el error como función de los pesos.**

$$\xi = \xi(\mathbf{w})$$

El error depende de los pesos: otros pesos, otro error. Así que se puede pensar como una **superficie** sobre el espacio de pesos, y entrenar es buscar el punto más bajo.

**Paso 2 — Recuerdo qué dice el gradiente.**

$$\nabla_{\mathbf{w}}\xi = \left(\frac{\partial \xi}{\partial w_1},\ \dots,\ \frac{\partial \xi}{\partial w_N}\right)$$

Apunta hacia donde el error **crece** más rápido. No apunta al mínimo: apunta cuesta arriba.

**Paso 3 — Propongo moverme en contra.**

$$\Delta\mathbf{w} = -\mu\,\nabla_{\mathbf{w}}\xi$$

Si el gradiente sube, el opuesto baja. $\mu$ es el tamaño del paso.

**Paso 4 — Verifico con Taylor de primer orden que el error baja.**

$$\xi(\mathbf{w} + \Delta\mathbf{w}) \approx \xi(\mathbf{w}) + \nabla\xi^{\mathsf{T}}\,\Delta\mathbf{w}$$

Cerca de $\mathbf{w}$, la superficie se parece a un plano. **(M4)** Reemplazo $\Delta\mathbf{w}$ por lo que propuse:

$$\xi(\mathbf{w} + \Delta\mathbf{w}) \approx \xi(\mathbf{w}) - \mu\,\lVert\nabla\xi\rVert^2$$

**Paso 5 — Leo el signo.** $\lVert\nabla\xi\rVert^2 \ge 0$ siempre, así que el término que se resta es positivo: **el error nuevo es menor que el viejo**.

> **OJO — el límite de esta garantía**
> Vale sólo **cerca** de $\mathbf{w}$, porque Taylor de primer orden es una aproximación local. Con $\mu$ grande el paso cae lejos, la aproximación deja de valer y el error puede subir: es la oscilación.

---

# 2. La regla LMS (perceptrón simple)

**Adónde quiero llegar:** $\;\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\,e(n)\,\mathbf{x}(n)$

**La estrategia:** tomar el error de un patrón, derivarlo respecto de los pesos, y meterlo en la ecuación del gradiente.

**Paso 0 — Declaro la simplificación.** Caso **lineal**: $y = \langle \mathbf{w}, \mathbf{x}\rangle$, sin función de activación. Hay que decirlo en voz alta: $\operatorname{sgn}$ ni siquiera es derivable, y es lo que hace que todo salga limpio.

**Paso 1 — Escribo el criterio y reemplazo la salida. (M4)**

$$e^2(n) = \big[d(n) - y(n)\big]^2 = \big[d(n) - \langle \mathbf{w}(n), \mathbf{x}(n)\rangle\big]^2$$

**Paso 2 — Aclaro respecto de qué derivo.** La variable es $\mathbf{w}$. **$\mathbf{x}$ y $d$ son constantes**: son los datos del patrón, no cambian cuando movés los pesos.

**Paso 3 — Derivo el cuadrado con la regla de la cadena. (M1)**

$$\nabla_{\mathbf{w}}\,e^2(n) = 2\big[d(n) - \langle \mathbf{w},\mathbf{x}\rangle\big]\cdot\nabla_{\mathbf{w}}\big(d(n) - \langle \mathbf{w},\mathbf{x}\rangle\big)$$

La derivada de algo al cuadrado es *dos veces ese algo, por la derivada de ese algo*.

**Paso 4 — Resuelvo el paréntesis de adentro. (M3 y M2)**

$$\nabla_{\mathbf{w}}\big(d - \langle \mathbf{w},\mathbf{x}\rangle\big) = 0 - \mathbf{x}(n)$$

$d$ no depende de $\mathbf{w}$: da cero. $\langle \mathbf{w},\mathbf{x}\rangle = \sum_i w_i x_i$ derivado respecto de $w_i$ deja sólo $x_i$. En vector: $\mathbf{x}$.

**Paso 5 — Reconozco el error y junto. (M5)**

$$\nabla_{\mathbf{w}}\,e^2(n) = 2\,e(n)\,\big(-\mathbf{x}(n)\big)$$

El corchete del paso 3 era justamente $e(n)$.

**Paso 6 — Reemplazo en la ecuación del gradiente y simplifico signos. (M4, M6)**

$$\mathbf{w}(n+1) = \mathbf{w}(n) - \mu\cdot 2\,e(n)\,\big(-\mathbf{x}(n)\big) = \boxed{\;\mathbf{w}(n) + 2\mu\,e(n)\,\mathbf{x}(n)\;}$$

El menos del descenso se cancela con el menos de $-\mathbf{x}$: por eso la corrección queda **sumando**.

**Leído en voz alta:** *paso, por error, por entrada.* Comparando con la corrección de error, $\frac{\eta}{2} = 2\mu$, o sea $\eta = 4\mu$.

---

# 3. Back-propagation: la cadena y la definición de $\delta$

**Adónde quiero llegar:** $\;\Delta w_{ji}(n) = \mu\,\delta_j(n)\,y_i(n)$

**La estrategia:** el error no depende directo del peso, sino a través de una cadena de cuatro eslabones. Se parte la derivada en esos cuatro, se resuelve el más fácil, y los otros tres se agrupan con un nombre.

**Paso 1 — Escribo la regla del gradiente.**

$$\Delta w_{ji}(n) = -\mu\,\frac{\partial \xi(n)}{\partial w_{ji}(n)}$$

**Paso 2 — Escribo de qué depende qué.**

$$\xi \;\leftarrow\; e_j \;\leftarrow\; y_j \;\leftarrow\; v_j \;\leftarrow\; w_{ji}$$

El error depende del error de la neurona, que depende de su salida, que depende de su campo local, que es lo **único** que depende directamente del peso.

**Paso 3 — Aplico la regla de la cadena siguiendo esa lista. (M1)**

$$\frac{\partial \xi}{\partial w_{ji}} = \frac{\partial \xi}{\partial e_j}\;\frac{\partial e_j}{\partial y_j}\;\frac{\partial y_j}{\partial v_j}\;\frac{\partial v_j}{\partial w_{ji}}$$

Un factor por cada flecha. Ésta es **la ecuación fundamental**: todo lo que sigue es resolver estos cuatro factores.

**Paso 4 — Resuelvo el último factor. (M4, M2)**

$$v_j = \sum_i w_{ji}\,y_i \quad\Longrightarrow\quad \frac{\partial v_j}{\partial w_{ji}} = y_i(n)$$

Reemplazo $v_j$ por su definición y derivo respecto de **un** peso: de toda la suma sólo sobrevive el término que tiene ese peso.

> **Trampa:** confundir $y_i$ con $y_j$. $y_i$ es la **entrada** que llega por esa conexión (salida de la capa anterior). $y_j$ es la salida de la neurona.

**Paso 5 — Agrupo los tres factores que quedan y les pongo nombre.**

$$\delta_j(n) \triangleq -\frac{\partial \xi}{\partial y_j}\,\frac{\partial y_j}{\partial v_j}$$

Los dos primeros factores del paso 3 se escriben fusionados como $\partial\xi/\partial y_j$. El nombre: **gradiente** (es una derivada), **local** (de esa neurona), **instantáneo** (en la iteración $n$).

¿Por qué se corta justo ahí? Porque $\delta_j$ junta **todo lo que es de la neurona** y deja afuera **lo que es de la conexión**. Así se calcula una vez por neurona y sirve para todos los pesos que entran a ella.

**Paso 6 — Reemplazo en la regla del gradiente. (M4, M6)**

$$\Delta w_{ji} = -\mu\,\frac{\partial \xi}{\partial y_j}\,\frac{\partial y_j}{\partial v_j}\,y_i = \boxed{\;\mu\,\delta_j(n)\,y_i(n)\;}$$

El menos que puse en la definición de $\delta$ se come el menos del gradiente: la actualización queda **sumando**.

> **OJO — por qué no se define $\delta$ directamente con $e_j$**
> Porque las neuronas ocultas **no tienen** $e_j$: no hay salida deseada para ellas. Lo que sí tienen siempre es $\partial\xi/\partial y_j$. La definición genérica es la única que sirve para las dos capas.

---

# 4. La derivada de la sigmoide simétrica

**Adónde quiero llegar:** $\;\varphi'(v_j) = \tfrac{1}{2}\big(1+y_j\big)\big(1-y_j\big)$

**La estrategia:** derivar, y después usar dos trucos algebraicos para que la exponencial desaparezca y todo quede escrito con la **salida** $y_j$.

**Paso 1 — Escribo la función.** Con $b=1$:

$$y_j = \varphi(v_j) = \frac{2}{1+e^{-v_j}} - 1$$

**Paso 2 — Derivo como cociente.** El $-1$ da cero **(M3)**; el resto es $2\,(1+e^{-v})^{-1}$:

$$\frac{\partial y_j}{\partial v_j} = \frac{2\,e^{-v_j}}{\big(1+e^{-v_j}\big)^2}$$

**Paso 3 — Parto la fracción en dos factores.** El cuadrado de abajo se reparte uno para cada lado:

$$\frac{\partial y_j}{\partial v_j} = 2\cdot\underbrace{\frac{1}{1+e^{-v_j}}}_{(1)}\cdot\underbrace{\frac{e^{-v_j}}{1+e^{-v_j}}}_{(2)}$$

**Paso 4 — En el factor (2), sumo y resto 1 en el numerador.**

$$\frac{e^{-v_j}}{1+e^{-v_j}} = \frac{-1 + 1 + e^{-v_j}}{1+e^{-v_j}} = 1 - \frac{1}{1+e^{-v_j}}$$

*Sumar y restar uno es no hacer nada*, pero me deja partir la fracción en «todo el denominador sobre sí mismo» menos «uno sobre el denominador». Ahora los dos factores tienen el mismo pedazo: $\frac{1}{1+e^{-v_j}}$.

**Paso 5 — Despejo ese pedazo de la definición.** De la ecuación del paso 1:

$$y_j + 1 = \frac{2}{1+e^{-v_j}} \quad\Longrightarrow\quad \frac{1}{1+e^{-v_j}} = \frac{y_j+1}{2}$$

**Paso 6 — Reemplazo en los dos factores. (M4)** La exponencial desaparece:

$$\frac{\partial y_j}{\partial v_j} = 2\cdot\frac{y_j+1}{2}\left(1 - \frac{y_j+1}{2}\right)$$

**Paso 7 — Simplifico. (M6)** El 2 de adelante se cancela con el primer $/2$, y adentro del paréntesis $1 - \frac{y+1}{2} = \frac{1-y}{2}$:

$$\boxed{\;\varphi'(v_j) = \tfrac{1}{2}\big(1+y_j\big)\big(1-y_j\big)\;}$$

**Leído en voz alta:** *un medio, por uno más la salida, por uno menos la salida.* Y quedó en función de $y_j$, que la pasada hacia adelante ya calculó: no hay que recalcular ninguna exponencial.

> **OJO — el control de tres segundos**
> En $v=0$ la salida es $y=0$ y la derivada tiene que dar $+0{,}5$. Si escribiste $(1+y)(y-1)$, da $-0{,}5$: tenés los factores dados vuelta, y una función creciente no puede tener derivada negativa.

---

# 5. El $\delta$ de la capa de salida

**Adónde quiero llegar:** $\;\delta^{III}_j = \tfrac{1}{2}\,e_j\,\big(1+y^{III}_j\big)\big(1-y^{III}_j\big)$

**La estrategia:** partir de la definición de $\delta$; la derivada de la activación ya la tengo; sólo falta $\partial\xi/\partial y_j$, que en la capa de salida es fácil porque ahí **sí** hay error.

**Paso 1 — Escribo la definición y reemplazo lo que ya sé. (M4)**

$$\delta^{III}_j = -\frac{\partial \xi}{\partial y^{III}_j}\cdot\tfrac{1}{2}\big(1+y^{III}_j\big)\big(1-y^{III}_j\big)$$

El segundo factor es la derivada de la sigmoide (deducción 4). Me queda sólo el primero.

**Paso 2 — Abro el primero en dos eslabones. (M1)**

$$\frac{\partial \xi}{\partial y^{III}_j} = \frac{\partial \xi}{\partial e_j}\;\frac{\partial e_j}{\partial y^{III}_j}$$

$\xi$ depende de $y_j$ a través de $e_j$.

**Paso 3 — Resuelvo el primer eslabón. (M4, M2)**

$$\xi = \tfrac{1}{2}\sum_k e_k^2 \quad\Longrightarrow\quad \frac{\partial \xi}{\partial e_j} = \tfrac{1}{2}\cdot 2\,e_j = e_j(n)$$

Reemplazo $\xi$ por su definición. Derivo respecto de $e_j$: de toda la suma **sobrevive un solo término**, el $k=j$, porque los otros errores no dependen de $e_j$. El 2 que baja se cancela con el $\tfrac12$ — para eso estaba.

**Paso 4 — Resuelvo el segundo eslabón. (M4, M3)**

$$e_j = d_j - y^{III}_j \quad\Longrightarrow\quad \frac{\partial e_j}{\partial y^{III}_j} = -1$$

$d_j$ es la salida deseada: un dato, constante, da cero.

**Paso 5 — Junto todo. (M6)**

$$\delta^{III}_j = -\,(e_j)(-1)\cdot\tfrac{1}{2}\big(1+y^{III}_j\big)\big(1-y^{III}_j\big) = \boxed{\;\tfrac{1}{2}\,e_j\,\big(1+y^{III}_j\big)\big(1-y^{III}_j\big)\;} \quad\star$$

El $-1$ del paso 4 cancela el menos de la definición. **Marcá la estrella:** la vas a reusar en la deducción 6.

**Paso 6 — Armo el ajuste. (M4)**

$$\Delta w^{III}_{ji} = \mu\,\delta^{III}_j\,y^{II}_i = \eta\;e_j\,\big(1+y^{III}_j\big)\big(1-y^{III}_j\big)\;y^{II}_i$$

con $\eta = \mu/2$, que absorbe el $\tfrac12$ de la derivada. Y $y^{II}_i$ es **la entrada** a la capa III, o sea la salida de la capa II.

**Leído en voz alta:** *velocidad de aprendizaje, por error, por derivada de la activación, por entrada.*

---

# 6. El $\delta$ de una capa oculta

**Adónde quiero llegar:** $\;\delta^{II}_j = \left[\sum_k \delta^{III}_k\,w^{III}_{kj}\right]\tfrac{1}{2}\big(1+y^{II}_j\big)\big(1-y^{II}_j\big)$

**La estrategia:** es la misma cuenta que la de salida, pero acá no hay $e_j$. El error se mide recién en la capa III, así que hay que **atravesar** la capa III para llegar desde $\xi$ hasta $y^{II}_j$.

**Paso 0 — Marco los tres índices.** $i$: de dónde viene la entrada (capa I). $j$: la neurona donde estoy (capa II). $k$: las neuronas a las que alimenta (capa III). **Sin esto la cuenta se mezcla.**

**Paso 1 — Escribo la definición con la derivada ya conocida. (M4)**

$$\delta^{II}_j = -\frac{\partial \xi}{\partial y^{II}_j}\cdot\tfrac{1}{2}\big(1+y^{II}_j\big)\big(1-y^{II}_j\big)$$

**Paso 2 — Reemplazo $\xi$ y meto la derivada adentro de la suma. (M4)**

$$\frac{\partial \xi}{\partial y^{II}_j} = \frac{\partial}{\partial y^{II}_j}\,\tfrac{1}{2}\sum_k e_k^2 = \sum_k e_k\,\frac{\partial e_k}{\partial y^{II}_j}$$

> **Trampa:** acá **no** sobrevive un solo término. En la capa de salida sí, porque $e_j$ dependía sólo de $y_j$. Pero la neurona oculta $j$ alimenta a **todas** las neuronas de la capa III, así que **todos** los $e_k$ dependen de ella. La suma queda entera.

**Paso 3 — Abro $\partial e_k/\partial y^{II}_j$ atravesando la capa III. (M1)**

$$\frac{\partial e_k}{\partial y^{II}_j} = \frac{\partial e_k}{\partial y^{III}_k}\;\frac{\partial y^{III}_k}{\partial v^{III}_k}\;\frac{\partial v^{III}_k}{\partial y^{II}_j}$$

El camino: $y^{II}_j$ entra al campo local de la neurona $k$, que pasa por su activación, que da su salida, que da su error.

**Paso 4 — Resuelvo los tres eslabones.**

$$\frac{\partial e_k}{\partial y^{III}_k} = -1 \qquad\qquad \text{(M3: } e_k = d_k - y_k \text{)}$$

$$\frac{\partial y^{III}_k}{\partial v^{III}_k} = \tfrac{1}{2}\big(1+y^{III}_k\big)\big(1-y^{III}_k\big) \qquad \text{(la derivada de la sigmoide, en la neurona } k\text{)}$$

$$\frac{\partial v^{III}_k}{\partial y^{II}_j} = w^{III}_{kj} \qquad\qquad \text{(M4, M2: } v_k = \sum_j w_{kj}\,y_j \text{, sobrevive el término } j\text{)}$$

> **Trampa:** hay **dos** derivadas de activación distintas en esta cuenta. La del paso 4 va evaluada en **$k$** (capa III). La que arrastro desde el paso 1 va en **$j$** (capa II). No son la misma.

**Paso 5 — Reemplazo todo. (M4, M6)** El $-1$ cancela el menos de la definición:

$$\delta^{II}_j = \sum_k e_k\,\tfrac{1}{2}\big(1+y^{III}_k\big)\big(1-y^{III}_k\big)\,w^{III}_{kj}\;\cdot\;\tfrac{1}{2}\big(1+y^{II}_j\big)\big(1-y^{II}_j\big)$$

**Paso 6 — Reconozco la estrella. (M5)** Lo que multiplica a $w^{III}_{kj}$ adentro de la suma es exactamente el $\delta^{III}_k$ de la deducción 5:

$$e_k\,\tfrac{1}{2}\big(1+y^{III}_k\big)\big(1-y^{III}_k\big) = \delta^{III}_k \quad\star$$

$$\boxed{\;\delta^{II}_j = \left[\sum_k \delta^{III}_k\,w^{III}_{kj}\right]\tfrac{1}{2}\big(1+y^{II}_j\big)\big(1-y^{II}_j\big)\;}$$

**Leído en voz alta:** *el corchete es una suma ponderada de los deltas de la capa siguiente, pesados por los mismos pesos que unen a las neuronas, recorridos al revés.* **El corchete reemplaza al error**; el resto de la fórmula es idéntico al de la capa de salida. Eso es «retropropagar».

---

# 7. La generalización a una capa $p$ cualquiera

**Adónde quiero llegar:** una sola fórmula para todas las capas.

**Paso 1 — Renombro.** $p$ es la capa donde estoy, $p-1$ de donde viene la entrada, $p+1$ la siguiente. La deducción 6 no usó en ningún momento que la red tuviera tres capas.

**Paso 2 — Escribo la fórmula con los nombres nuevos.**

$$\Delta w^{(p)}_{ji} = \eta\;\big\langle \boldsymbol{\delta}^{(p+1)},\ \mathbf{w}^{(p+1)}_j\big\rangle\;\big(1+y^{(p)}_j\big)\big(1-y^{(p)}_j\big)\;y^{(p-1)}_i$$

El producto interno es la forma compacta de $\sum_k \delta^{(p+1)}_k\,w^{(p+1)}_{kj}$. Y $\mathbf{w}^{(p+1)}_j$ es la **columna** $j$ de $\mathbf{W}^{(p+1)}$: los pesos que **salen** de la neurona $j$, no los que entran.

**Paso 3 — Aclaro los dos bordes.** Arriba (capa de salida) no hay $p+1$: el producto interno se reemplaza por $e_j$. Abajo (primera capa) no hay $p-1$: $y^{(p-1)}_i$ se reemplaza por la entrada $x_i$. **En el medio, la fórmula es la misma para todas.**

---

# 8. Base radial: los pesos de salida

**Adónde quiero llegar:** $\;w_{kj}(n+1) = w_{kj}(n) - \eta\,e_k(n)\,\varphi_j(n)$

**La estrategia:** la misma que LMS. Es corta porque la salida es **lineal** en los pesos: no hay activación que derivar.

**Paso 1 — Escribo el criterio.** Ojo, acá el error está definido al revés que en el multicapa:

$$e_k = y_k - d_k \qquad \xi = \tfrac{1}{2}\sum_k e_k^2$$

**Paso 2 — Aplico la cadena. (M1)**

$$\frac{\partial \xi}{\partial w_{kj}} = \frac{\partial \xi}{\partial e_k}\;\frac{\partial e_k}{\partial y_k}\;\frac{\partial y_k}{\partial w_{kj}}$$

**Paso 3 — Resuelvo los tres. (M2, M3, M4)**

$$\frac{\partial \xi}{\partial e_k} = e_k \qquad \frac{\partial e_k}{\partial y_k} = +1 \qquad \frac{\partial y_k}{\partial w_{kj}} = \varphi_j$$

El primero: sobrevive el término $k$ y el 2 se cancela con el $\tfrac12$. El segundo da $+1$ porque ahora $e = y - d$. El tercero: $y_k = \sum_j w_{kj}\varphi_j$, sobrevive el término $j$.

**Paso 4 — Reemplazo en el gradiente. (M4)**

$$w_{kj}(n+1) = w_{kj}(n) - \eta\,\frac{\partial \xi}{\partial w_{kj}} = \boxed{\;w_{kj}(n) - \eta\,e_k(n)\,\varphi_j(n)\;}$$

> **OJO — el signo cambió porque cambió la definición del error**
> Con $e = y - d$ la actualización **resta**; con $e = d - y$, como en el multicapa, **suma**. Es la misma regla. Fijate siempre cómo está definido $e$ antes de escribir el signo.

---

# 9. Hopfield: la energía nunca sube

**Adónde quiero llegar:** $\;\Delta E \le 0\;$ en todo paso.

**La estrategia:** actualizar **una sola** neurona y aislar en la energía los términos que la contienen. Todo lo demás no se mueve.

**Paso 1 — Escribo la energía.**

$$E(\mathbf{y}) = -\frac{1}{2}\sum_{j}\sum_{i} w_{ji}\,y_i\,y_j$$

**Paso 2 — Separo los términos que contienen a la neurona $j$.** En la doble suma, $y_j$ aparece **dos veces** por cada otra neurona $i$: una cuando el índice de afuera vale $j$, y otra cuando el de adentro vale $j$:

$$E = -\frac{1}{2}\left[\sum_{i} w_{ji}\,y_i\,y_j + \sum_{i} w_{ij}\,y_j\,y_i\right] + (\text{términos sin } y_j)$$

El término $i=j$ no existe porque $w_{jj}=0$.

**Paso 3 — Uso la simetría para juntar las dos sumas.** Como $w_{ij} = w_{ji}$, las dos sumas son **iguales**:

$$E = -\frac{1}{2}\cdot 2\,y_j\sum_{i} w_{ji}\,y_i + (\ldots) = -\,y_j\,v_j + (\text{términos sin } y_j)$$

El 2 se come el $\tfrac12$, y reconozco el campo local $v_j = \sum_i w_{ji}\,y_i$ **(M5)**. **Acá se usó la simetría, y hay que decirlo:** sin ella las dos sumas no serían iguales y esta línea no cierra.

**Paso 4 — Calculo cuánto cambia $E$ al actualizar $y_j$.** Los términos sin $y_j$ no se mueven **(M3)**, y $v_j$ tampoco, porque no contiene a $y_j$:

$$\Delta E = -\big(y_j^{\text{nuevo}} - y_j\big)\,v_j$$

**Paso 5 — Caso 1: la neurona cambió.** Entonces $y_j^{\text{nuevo}} = -y_j$, y la diferencia vale $-2y_j$:

$$\Delta E = -(-2y_j)\,v_j = 2\,y_j\,v_j$$

Pero si cambió fue porque su valor viejo **no** coincidía con el signo de $v_j$. Tienen signos distintos, el producto es negativo: $\Delta E < 0$.

**Paso 6 — Caso 2: la neurona no cambió.** La diferencia es cero: $\Delta E = 0$.

**Paso 7 — Junto los dos casos.**

$$\boxed{\;\Delta E \le 0\;}$$

**Paso 8 — Cierro con la finitud.** $E$ nunca sube, está acotada por abajo, y hay $2^N$ estados posibles: no puede bajar para siempre. La red se detiene en una cantidad finita de pasos.

---

# 10. BPTT: el caso $t = 0$

**Adónde quiero llegar:** $\;\dfrac{\partial E_0}{\partial w_{ji}} = \delta_{0,j}\,y_{-1,i}$

**La estrategia:** con un solo instante la red desenrollada tiene una sola capa. Es la deducción 5 otra vez, con índices de tiempo.

> **OJO — en BPTT el error está definido como $e = y - d$**
> Al revés que en el multicapa. Por eso la actualización final **resta** ($\mathbf{W} \leftarrow \mathbf{W} - \eta\,\Delta\mathbf{W}$), igual que en base radial.

**Paso 1 — Aplico la cadena, tres eslabones. (M1)**

$$\frac{\partial E_0}{\partial w_{ji}} = \frac{\partial E_0}{\partial y_{0,j}}\;\frac{\partial y_{0,j}}{\partial v_{0,j}}\;\frac{\partial v_{0,j}}{\partial w_{ji}}$$

**Paso 2 — Primer factor. (M4, M2)**

$$\frac{\partial E_0}{\partial y_{0,j}} = \frac{\partial}{\partial y_{0,j}}\,\tfrac{1}{2}\sum_k e_{0,k}^2 = \sum_k e_{0,k}\,\frac{\partial e_{0,k}}{\partial y_{0,j}} = e_{0,j}$$

Sobrevive sólo $k=j$, porque $\partial e_{0,k}/\partial y_{0,j} = 1$ únicamente cuando $k=j$.

**Paso 3 — Segundo factor.** La derivada de la activación:

$$\frac{\partial y_{0,j}}{\partial v_{0,j}} = \varphi'(v_{0,j}) = \tfrac{1}{2}\big(1-y_{0,j}\big)\big(1+y_{0,j}\big)$$

**Paso 4 — Tercer factor. (M4, M2)**

$$v_{0,j} = \sum_\ell w_{j\ell}\,y_{-1,\ell} \quad\Longrightarrow\quad \frac{\partial v_{0,j}}{\partial w_{ji}} = y_{-1,i}$$

**Paso 5 — Bautizo los dos primeros y junto.**

$$\delta_{0,j} \triangleq \frac{\partial E_0}{\partial y_{0,j}}\,\frac{\partial y_{0,j}}{\partial v_{0,j}} = \big(y_{0,j} - d_{0,j}\big)\,\varphi'(v_{0,j}) \qquad\Longrightarrow\qquad \boxed{\;\frac{\partial E_0}{\partial w_{ji}} = \delta_{0,j}\,y_{-1,i}\;}$$

---

# 11. BPTT: el caso $t = 1$, dos aportes

**Adónde quiero llegar:** $\;\dfrac{\partial E_1}{\partial w_{ji}} = \delta_{1,j}\,y_{0,i} + \delta_{0,j}\,y_{-1,i}$

**La estrategia:** con dos instantes, el **mismo** peso actuó dos veces —en $t=0$ y en $t=1$— así que $E_1$ depende de él por **dos caminos**, y hay que sumar los dos.

**Paso 1 — Separo los dos caminos.**

$$\frac{\partial E_1}{\partial w_{ji}} = \underbrace{\frac{\partial E_1}{\partial w_{1,ji}}}_{\text{directo}} + \underbrace{\frac{\partial E_1}{\partial w_{0,ji}}}_{\text{indirecto}}$$

$w_{0,ji}$ y $w_{1,ji}$ son **el mismo peso**; la notación sólo marca en qué instante actúa. Se **suman** porque es la regla de la cadena para una variable que aparece en dos lugares.

**Paso 2 — El directo: es la deducción 10 corrida un instante.**

$$\frac{\partial E_1}{\partial w_{1,ji}} = e_{1,j}\;\varphi'(v_{1,j})\;y_{0,i} = \delta_{1,j}\,y_{0,i}$$

**Paso 3 — El indirecto: la cadena hasta $t=0$. (M1)**

$$\frac{\partial E_1}{\partial w_{0,ji}} = \frac{\partial E_1}{\partial y_{0,j}}\;\frac{\partial y_{0,j}}{\partial v_{0,j}}\;\frac{\partial v_{0,j}}{\partial w_{0,ji}}$$

Los dos últimos ya los conozco: $\varphi'(v_{0,j})$ y $y_{-1,i}$. El trabajo está en el primero.

**Paso 4 — Abro $\partial E_1/\partial y_{0,j}$ atravesando el instante 1. (M4, M1)**

$$\frac{\partial E_1}{\partial y_{0,j}} = \sum_k e_{1,k}\;\frac{\partial e_{1,k}}{\partial y_{1,k}}\;\frac{\partial y_{1,k}}{\partial v_{1,k}}\;\frac{\partial v_{1,k}}{\partial y_{0,j}}$$

La salida de $j$ en $t=0$ entra por las conexiones recurrentes a **todas** las neuronas $k$ de $t=1$. Es exactamente la deducción 6, con «capa siguiente» reemplazado por «instante siguiente». La suma queda entera.

**Paso 5 — Resuelvo los eslabones.**

$$\frac{\partial e_{1,k}}{\partial y_{1,k}} = 1 \qquad \frac{\partial y_{1,k}}{\partial v_{1,k}} = \varphi'(v_{1,k}) \qquad \frac{\partial v_{1,k}}{\partial y_{0,j}} = w_{jk}$$

**Paso 6 — Reconozco $\delta_{1,k}$ y junto. (M5)**

$$\frac{\partial E_1}{\partial w_{0,ji}} = \left(\sum_k \underbrace{e_{1,k}\,\varphi'(v_{1,k})}_{\delta_{1,k}}\,w_{jk}\right)\varphi'(v_{0,j})\;y_{-1,i} = \delta_{0,j}\,y_{-1,i}$$

> **OJO — este $\delta_{0,j}$ no es el de la deducción 10**
> Se llaman igual y son distintos: aquél venía de $E_0$, éste de retropropagar $E_1$ un instante. Decilo en voz alta cuando lo escribas.

**Paso 7 — Sumo los dos aportes.**

$$\boxed{\;\frac{\partial E_1}{\partial w_{ji}} = \delta_{1,j}\,y_{0,i} + \delta_{0,j}\,y_{-1,i}\;}$$

---

# 12. BPTT: la generalización

**Adónde quiero llegar:** la fórmula para un $t$ cualquiera.

**Paso 1 — Reconozco el patrón.** En $t=1$ hubo dos aportes, uno por instante. En $t$ va a haber $t+1$: uno por cada instante en que actuó el peso.

$$\frac{\partial E_t}{\partial w_{ji}} = \sum_{\tau=t}^{0}\delta_{\tau,j}\,y_{\tau-1,i}$$

**Paso 2 — Escribo cómo se calcula cada $\delta$.** En el instante donde se midió el error es directo; hacia atrás se arrastra igual que en la capa oculta:

$$\delta_{\tau,j} = \begin{cases} \big(y_{\tau,j} - d_{\tau,j}\big)\,\varphi'(v_{\tau,j}) & \tau = t \\[6pt] \left(\displaystyle\sum_k w_{jk}\,\delta_{\tau+1,k}\right)\varphi'(v_{\tau,j}) & \tau < t \end{cases}$$

**Paso 3 — Sumo sobre todos los instantes con error.**

$$\frac{\partial E}{\partial w_{ji}} = \sum_{t}\sum_{\tau=t}^{0}\delta_{\tau,j}\,y_{\tau-1,i} \qquad\qquad w_{ji} \leftarrow w_{ji} - \eta\,\frac{\partial E}{\partial w_{ji}}$$

**Leído en voz alta:** *es back-propagation con el tiempo haciendo de profundidad, y con los pesos compartidos entre todas las capas; por eso los aportes se suman.*

---

# 13. BPTT: los pesos de entrada

**Adónde quiero llegar:** $\;\dfrac{\partial E_t}{\partial w^{I}_{ji}} = \sum_{\tau=t}^{0}\delta_{\tau,j}\,x_{\tau,i}$

**La estrategia:** repetir todo y ver qué cambia. Cambia **un solo factor**.

**Paso 1 — Miro el último eslabón de la cadena. (M4, M2)** Antes era:

$$\frac{\partial v_{0,j}}{\partial w_{ji}} = \frac{\partial}{\partial w_{ji}}\sum_\ell w_{j\ell}\,y_{-1,\ell} = y_{-1,i}$$

y ahora es:

$$\frac{\partial v_{0,j}}{\partial w^{I}_{ji}} = \frac{\partial}{\partial w^{I}_{ji}}\sum_\ell w^{I}_{j\ell}\,x_{0,\ell} = x_{0,i}$$

**Paso 2 — Todo lo demás es igual.** Los $\delta$ son **exactamente los mismos**, porque agrupan lo que pasa **dentro** de la neurona y no saben por dónde entró la señal:

$$\boxed{\;\frac{\partial E_t}{\partial w^{I}_{ji}} = \sum_{\tau=t}^{0}\delta_{\tau,j}\,x_{\tau,i}\;}$$

---

# 14. BPTT optimizado: el $\delta^*$

**Adónde quiero llegar:** $\;\delta^*_{t,j} = \left[\big(y_{t,j} - d_{t,j}\big) + \sum_k w_{jk}\,\delta^*_{t+1,k}\right]\varphi'(v_{t,j})$

**La estrategia:** escribir todos los aportes juntos y **sacar factor común**. Aparece una recursión que se calcula en un solo barrido.

**Paso 1 — Escribo el gradiente completo para $T = 3$, agrupando por instante.** En notación simplificada:

$$\frac{\partial E}{\partial w} = \frac{\partial E_2}{\partial v_2}\frac{\partial v_2}{\partial w} + \left(\frac{\partial E_1}{\partial v_1} + \frac{\partial E_2}{\partial v_2}\frac{\partial v_2}{\partial v_1}\right)\frac{\partial v_1}{\partial w} + \left(\frac{\partial E_0}{\partial v_0} + \Big[\ldots\Big]\frac{\partial v_1}{\partial v_0}\right)\frac{\partial v_0}{\partial w}$$

Cada $\partial v_t/\partial w$ está multiplicado por lo que le llega **de ese instante y de todos los posteriores**.

**Paso 2 — Le pongo nombre a cada paréntesis. (M5)**

$$\delta^*_2 = \frac{\partial E_2}{\partial v_2} \qquad \delta^*_1 = \frac{\partial E_1}{\partial v_1} + \delta^*_2\,\frac{\partial v_2}{\partial v_1} \qquad \delta^*_0 = \frac{\partial E_0}{\partial v_0} + \delta^*_1\,\frac{\partial v_1}{\partial v_0}$$

Cada uno es **el anterior, actualizado**: se lo pasa un instante para atrás y se le suma el error directo de ese instante.

**Paso 3 — Escribo la regla general.**

$$\delta^*_t \triangleq \frac{\partial E_t}{\partial v_t} + \delta^*_{t+1}\,\frac{\partial v_{t+1}}{\partial v_t}$$

**Paso 4 — Desarrollo los dos términos. (M4)**

$$\frac{\partial E_t}{\partial v_{t,j}} = \big(y_{t,j} - d_{t,j}\big)\,\varphi'(v_{t,j}) \qquad \delta^*_{t+1}\,\frac{\partial v_{t+1}}{\partial v_{t,j}} = \sum_k \delta^*_{t+1,k}\,w_{jk}\,\varphi'(v_{t,j})$$

**Paso 5 — Saco $\varphi'$ de factor común. (M6)**

$$\boxed{\;\delta^*_{t,j} = \left[\big(y_{t,j} - d_{t,j}\big) + \sum_k w_{jk}\,\delta^*_{t+1,k}\right]\varphi'(v_{t,j})\;}$$

**Paso 6 — Escribo el gradiente con una sola suma.**

$$\frac{\partial E}{\partial w_{ji}} = \sum_{t=T-1}^{0}\delta^*_{t,j}\,y_{t-1,i} \qquad\qquad \frac{\partial E}{\partial w^{I}_{ji}} = \sum_{t=T-1}^{0}\delta^*_{t,j}\,x_{t,i}$$

Desapareció la suma interna sobre $\tau$: de $O(T^2)$ a $O(T)$. **Da el mismo gradiente**, sólo reorganizado.

---

# 15. LVQ1-O: el $\alpha$ óptimo

**Adónde quiero llegar:** $\;\alpha_c(n) = \dfrac{\alpha_c(n-1)}{1 + s(n)\,\alpha_c(n-1)}$

**La estrategia:** reescribir la regla de LVQ1 como combinación, abrirla un paso para atrás, ver que con $\alpha$ constante los patrones viejos pesan menos, e imponer que pesen igual.

**Paso 1 — Escribo la regla de LVQ1.**

$$\mathbf{m}_c(n+1) = \mathbf{m}_c(n) + s(n)\,\alpha(n)\big[\mathbf{x}(n) - \mathbf{m}_c(n)\big]$$

**Paso 2 — Distribuyo y agrupo por $\mathbf{m}_c(n)$. (M6)**

$$\mathbf{m}_c(n+1) = \big[1 - s(n)\alpha(n)\big]\,\mathbf{m}_c(n) + s(n)\alpha(n)\,\mathbf{x}(n)$$

El prototipo nuevo es una **combinación** del viejo y del patrón que acaba de entrar.

**Paso 3 — Abro $\mathbf{m}_c(n)$ un paso más para atrás. (M4)** Reemplazo $\mathbf{m}_c(n)$ por su propia fórmula:

$$\mathbf{m}_c(n+1) = \big[1 - s(n)\alpha(n)\big]\Big\{\big[1 - s(n-1)\alpha(n-1)\big]\mathbf{m}_c(n-1) + s(n-1)\alpha(n-1)\,\mathbf{x}(n-1)\Big\} + s(n)\alpha(n)\,\mathbf{x}(n)$$

**Paso 4 — Leo cuánto pesa cada patrón.**

$$\text{peso de } \mathbf{x}(n) = s(n)\,\alpha(n) \qquad \text{peso de } \mathbf{x}(n-1) = \big[1 - s(n)\alpha(n)\big]\,s(n-1)\,\alpha(n-1)$$

El patrón anterior quedó multiplicado por un factor **más**. Con $\alpha$ constante y menor que 1, cada patrón viejo arrastra un factor extra: **los primeros pesan cada vez menos**, y el prototipo termina dependiendo casi sólo del final del archivo.

**Paso 5 — Impongo que pesen igual (en magnitud).**

$$\alpha_c(n) = \big[1 - s(n)\,\alpha_c(n)\big]\,\alpha_c(n-1)$$

**Paso 6 — Distribuyo el lado derecho. (M6)**

$$\alpha_c(n) = \alpha_c(n-1) - s(n)\,\alpha_c(n)\,\alpha_c(n-1)$$

**Paso 7 — Paso a la izquierda todo lo que tiene $\alpha_c(n)$.**

$$\alpha_c(n) + s(n)\,\alpha_c(n)\,\alpha_c(n-1) = \alpha_c(n-1)$$

**Paso 8 — Saco $\alpha_c(n)$ de factor común. (M6)**

$$\alpha_c(n)\big[1 + s(n)\,\alpha_c(n-1)\big] = \alpha_c(n-1)$$

**Paso 9 — Despejo.**

$$\boxed{\;\alpha_c(n) = \frac{\alpha_c(n-1)}{1 + s(n)\,\alpha_c(n-1)}\;}$$

**Leído en voz alta:** *cada prototipo tiene su propio $\alpha$: si acierta ($s=+1$) el denominador crece y $\alpha$ baja; si se equivoca ($s=-1$) el denominador achica y $\alpha$ sube.* Con la advertencia de la cátedra: **no sobrepasar $\alpha > 1$**.

---

# Las quince, de un vistazo

| # | Deducción | Movimientos clave | El paso que se traba |
|---|---|---|---|
| 1 | Descenso por gradiente | Taylor | por qué el menos |
| 2 | LMS | M1, M3, M2 | que $\mathbf{x}$ y $d$ son constantes |
| 3 | Cadena y $\delta$ | M1, M2 | por qué se corta ahí el $\delta$ |
| 4 | Derivada de la sigmoide | sumar y restar 1 | despejar $\frac{1}{1+e^{-v}}$ de la definición |
| 5 | $\delta$ de salida | M1, M2, M3 | el $-1$ que cancela el signo |
| 6 | $\delta$ oculta | M1, **no** M2, M5 | la suma queda entera; dos $\varphi'$ distintas |
| 7 | Capa $p$ | renombrar | los dos bordes |
| 8 | Pesos de RBF | M1, M2 | el signo depende de cómo se definió $e$ |
| 9 | $\Delta E \le 0$ | separar términos, simetría | juntar las dos sumas |
| 10 | BPTT $t=0$ | igual que la 5 | — |
| 11 | BPTT $t=1$ | dos caminos, M5 | los aportes se **suman** |
| 12 | BPTT general | reconocer el patrón | la recursión de $\delta$ |
| 13 | Pesos de entrada | cambia un factor | los $\delta$ son los mismos |
| 14 | $\delta^*$ | factor común | agrupar por instante |
| 15 | $\alpha$ óptimo | abrir un paso, despejar | imponer la condición |

> **IDEA DE FONDO — las cinco del perceptrón y BPTT son una sola**
> Las deducciones 2, 5, 6, 10 y 11 son **la misma cuenta**: la cadena $\xi \to e \to y \to v \to w$, recorrida hasta donde haga falta. Si el peso está pegado a la salida, la cadena es corta y sobrevive un solo término. Si está más atrás —en una capa oculta o en un instante anterior— hay que atravesar la capa (o el instante) siguiente, la suma queda entera, y aparece el $\delta$ de adelante. **Entendida una, están entendidas las cinco.**
