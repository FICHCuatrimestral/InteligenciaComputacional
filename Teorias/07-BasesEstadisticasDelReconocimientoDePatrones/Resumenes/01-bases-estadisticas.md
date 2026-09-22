---
title: "Bases estadísticas del reconocimiento de patrones"
subtitle: "Inteligencia Computacional · FICH-UNL · César Martínez \\newline Diapositivas de *Bases estadísticas del reconocimiento de patrones* y las siete transcripciones de la clase"
lang: es
---

*Notación: ojo con la $y$. En esta unidad $\mathbf{y}$ es el **patrón crudo** recién adquirido y $\mathbf{x}$ es el **vector de características** que sale del preproceso. En las unidades de redes neuronales $y$ era la **salida** de una neurona. Son cosas distintas y conviene decirlo en voz alta al empezar.*

*Es la unidad más conceptual de la materia: casi no hay algoritmos, hay definiciones. Pero es la que le da el marco a todo lo demás — cuando decís «frontera de decisión» en el perceptrón, estás usando una definición de acá.*

---

## 1. De qué se trata

El punto de partida es una tarea que un humano resuelve sin esfuerzo: **¿cuántas llaves hay en esta imagen?** Con cuatro llaves separadas la contestás de un golpe de vista y sin ninguna incerteza, incluso si nunca viste una llave de ese modelo. Si la imagen se complica —aparecen tornillos, una cerradura, sombras, objetos solapados— empezás a necesitar segundos y pasadas de comprobación. Y si se complica lo suficiente, **te equivocás**.

Ese proceso es el que hay que reproducir en una máquina, y tiene tres partes: **detectar** los objetos, **identificarlos**, y **asignarles una etiqueta**.

El **aprendizaje maquinal** es la rama que se ocupa de eso: *programar máquinas para aprender a realizar una tarea, mejorando su desempeño en base a la experiencia.* Cada palabra de esa definición cuenta:

- **una tarea**: hay un objetivo específico a resolver;
- **desempeño**: tiene que poder medirse, porque si otro arma un sistema para la misma tarea hay que poder comparar cuál anda mejor;
- **experiencia**: cuantos más ejemplos se le muestren, mejor debería inferir sobre ejemplos nuevos que nunca vio.

Y dos restricciones que se le pueden pedir o no: **mínima intervención humana** (el objetivo de máxima es que funcione solo) y **conjunto reducido de ejemplos** — que importa porque en muchos campos conseguir datos es carísimo: juntar tomografías etiquetadas por un médico, por ejemplo.

### Claves de la sección 1

| Clave | Qué tenés que poder responder |
|---|---|
| La definición | Aprender una tarea, midiendo el desempeño, a partir de la experiencia |
| Las tres sub-tareas | Distinguir y aislar patrones, reunirlos en grupos, etiquetar los grupos |
| Las dos restricciones | Mínima intervención humana y pocos ejemplos, y por qué la segunda importa |

---

## 2. Dónde estamos parados: las dos ramas

Históricamente hay dos aproximaciones a la inteligencia artificial:

| | **IA clásica** | **Reconocimiento de formas** |
|---|---|---|
| Qué modela | el **razonamiento** humano | la **percepción** humana |
| Con qué técnicas | Lógica | Teoría de la Decisión Estadística y Teoría de Lenguajes Formales |
| Tipo de aprendizaje | **deductivo** | **inductivo** |

La diferencia práctica se ve con un ejemplo de la clase: detectar anemia a partir de un conteo de glóbulos rojos. En la **IA clásica** hay que sentar al médico al lado del programador para que vaya diciendo *«éste está sano, éste está anémico»* y con eso se escriben reglas `if…then`. En el **reconocimiento de formas** no se le pregunta las reglas a nadie: se le muestran ejemplos al sistema y las reglas salen de ahí.

> **IDEA DE FONDO — inductivo significa «a partir de ejemplos»**
> Es la palabra que separa las dos ramas, y es la que ubica a toda esta materia. Todo lo que viste —perceptrón, multicapa, radial, SOM— es aprendizaje inductivo.

### Las cuatro cosas que hace un sistema de reconocimiento

1. **Adquisición y representación del conocimiento**: tomar los patrones de la realidad y representarlos de alguna forma conveniente.
2. **Aprendizaje**: los algoritmos que infieren el sistema a partir de un conjunto de entrenamiento.
3. **Clasificación**: etiquetar patrones **nuevos**, no vistos en el entrenamiento. Eso es la capacidad de generalización.
4. **Evaluación**: los mecanismos para medir la bondad, la confianza o el error del sistema.

---

## 3. El diagrama de bloques

Todo sistema de reconocimiento tiene la misma estructura:

$$\text{mundo real} \;\longrightarrow\; \boxed{\text{adquisición}} \;\longrightarrow\; \boxed{\text{procesamiento}} \;\longrightarrow\; \boxed{\text{clasificación}} \;\longrightarrow\; \text{etiqueta}$$

- **(a) Adquisición**: la transducción del mundo real a una representación digital. Es la cámara, el micrófono, el analizador de sangre.
- **(b) Procesamiento digital**: acondicionamiento de la señal y, sobre todo, **representación alternativa** — de acá sale el vector descriptor.
- **(c) Clasificación**: la decisión sobre la clase.

El paso (b) es el que hace el trabajo pesado, y conviene entender por qué con el ejemplo de la clase. Una cara capturada en un rectángulo de $100 \times 100$ píxeles es, matemáticamente, un **vector de dimensión 10.000**. Construir un clasificador automático sobre 10.000 números es impracticable. Entonces el bloque de procesamiento mide unas pocas cosas —distancia entre ojos, distancia de la línea de ojos a la boca, tono de piel, relación de aspecto— y entrega **cinco números en vez de diez mil**, que son los que de verdad identifican a la persona.

> **OJO — dos bloques donde entra la experticia humana, y no son el clasificador**
> La **selección de características** (qué medir de la señal) y el **diseño del clasificador** (qué tipo usar) van siempre juntos y son donde el desarrollador pone lo que sabe. Y elegir mal una característica no es neutro: **puede confundir al sistema más de lo que lo ayuda**. El ejemplo de la clase es identificar personas por el color de ojos — hay muchísima gente con iris marrones, así que esa característica no discrimina nada.

### Claves de la sección 3

| Clave | Qué tenés que poder responder |
|---|---|
| Los tres bloques | Adquisición, procesamiento, clasificación, y qué hace cada uno |
| Para qué el preproceso | Reducir dimensión conservando lo que discrimina |
| El ejemplo de la cara | 10.000 píxeles → 5 medidas |
| Dónde entra el humano | Selección de características y diseño del clasificador |

---

## 4. Las dos aproximaciones, con el mismo ejemplo

| | **Geométrica o estadística** | **Estructural o sintáctica** |
|---|---|---|
| Base teórica | Teoría Estadística de la Decisión | Teoría de Lenguajes Formales |
| El patrón es… | un **vector numérico** | una **cadena de símbolos** |
| Las clases se representan por… | patrones prototipo | reglas sintácticas |
| Clasificadores típicos | gaussianos, basados en distancia, redes neuronales | autómatas, gramáticas, HMM |

**El mismo problema, resuelto de las dos formas** — OCR de dígitos manuscritos, distinguir ceros, seis y nueves:

**Aproximación geométrica.** Se parte la imagen al medio y se cuentan los píxeles blancos arriba y abajo: dos números, el **brillo superior** y el **brillo inferior**. Y esa medida tan simple funciona, porque los **9** tienen menos brillo arriba que los **6**, los **6** tienen menos brillo abajo que los **9**, y los **0** tienen brillo parecido en las dos mitades. Graficando los dos brillos como ejes aparecen tres nubes de puntos, y el clasificador son dos rectas que las separan. Un dígito nuevo se mide y se mira en qué región cayó.

**Aproximación sintáctica.** Se recorre el contorno del dígito desde una esquina, y en cada píxel se anota hacia dónde se movió usando un código de direcciones (4 u 8 símbolos). Un dígito queda convertido en una cadena tipo `000...06665...`. El clasificador es un autómata: un modelo por dígito, que va cambiando de estado según los símbolos que llegan, más una gramática que dice qué cadenas son válidas.

> **PARA LA DEFENSA — el ejemplo del brillo sirve para todo**
> Es el ejemplo que el profesor usa en toda la clase: primero para mostrar la aproximación geométrica, después para las probabilidades, y al final para el clasificador de Bayes. Si lo tenés, tenés la unidad.

---

## 5. Patrón, características, clases

**Patrón**: el objeto de interés, el que se quiere identificar. Puede estar bien definido —las cuatro llaves separadas— o ser **difuso**: la voz de una persona en la grabación de un restaurante llena de conversaciones, o la cara de alguien en una tribuna de fútbol.

Formalmente, el patrón **adquirido** es una variable aleatoria $n$-dimensional:

$$\mathbf{y} = [y_1\ y_2\ \dots\ y_n]^{\mathsf{T}}, \qquad y_i \in \mathbb{R}$$

que es un punto del **espacio de patrones** $P \in \mathbb{R}^n$.

La **extracción de características** lo convierte en un vector más chico que conserva lo que sirve para clasificar:

$$\mathbf{x} = [x_1\ x_2\ \dots\ x_d]^{\mathsf{T}}, \qquad d \le n$$

y ése vive en el **espacio de características** $E \in \mathbb{R}^d$. Con $d = n$ no se reduce nada: es sólo un cambio de representación (por ejemplo una transformación lineal que maximiza la varianza). Con $d < n$ hay **reducción de dimensionalidad**, que es el caso habitual.

### Las tres propiedades deseables de las características

1. **Precisión**: objetos diferentes → representaciones diferentes.
2. **Unicidad o determinismo**: cada objeto tiene una representación única.
3. **Continuidad en el espacio**: pequeñas perturbaciones del objeto producen pequeñas perturbaciones de su representación.

> **OJO — la tercera es la importante, y hay que saber por qué**
> Las dos primeras se pueden relajar y el sistema igual anda. La **continuidad** no, porque es la que da **robustez al ruido y capacidad de generalización**: si me saco una foto con un poco menos de luz, o con anteojos, el punto se mueve **poco** en el espacio de características y el sistema me sigue reconociendo. Sin continuidad, un cambio mínimo en la señal manda el punto a cualquier parte.

### Las clases

$$\Omega = \{\omega_1,\ \omega_2,\ \dots,\ \omega_c\} \qquad\qquad \Omega^* = \Omega \cup \{\omega_0\}$$

$c$ es la cantidad de clases y $\Omega$ el conjunto de etiquetas. El conjunto **extendido** agrega $\omega_0$, la **clase de rechazo**: la opción de decir *«no me arriesgo»*. Existe porque a veces equivocarse sale más caro que no contestar.

### Claves de la sección 5

| Clave | Qué tenés que poder responder |
|---|---|
| $\mathbf{y}$ vs. $\mathbf{x}$ | Patrón adquirido ($n$) vs. vector de características ($d \le n$) |
| Las tres propiedades | Precisión, unicidad, continuidad — y cuál es la que no se puede relajar |
| Por qué la continuidad | Robustez al ruido y generalización |
| $\omega_0$ | La clase de rechazo, y para qué sirve |

---

## 6. El clasificador estadístico

Acá está la definición central de la unidad.

Un **clasificador estadístico** es una máquina formada por $c$ **funciones discriminantes**, una por clase:

$$g_i : E \to \mathbb{R}, \qquad 1 \le i \le c$$

y la regla de decisión es comparar sus valores:

$$\mathbf{x} \text{ se asigna a la clase } \omega_i \;\iff\; g_i(\mathbf{x}) > g_j(\mathbf{x}) \quad \forall\, j \neq i$$

En castellano: **cada clase le pone un puntaje al patrón, y gana el puntaje más alto.**

### Regiones y fronteras de decisión

El clasificador **parte el espacio en $c$ regiones**:

$$R_i = \{\mathbf{x} \in E : g_i(\mathbf{x}) > g_j(\mathbf{x})\ \forall\, j \neq i\}$$

y las **fronteras de decisión** son las superficies donde se empata:

$$g_i(\mathbf{x}) - g_j(\mathbf{x}) = 0$$

> **IDEA DE FONDO — esto ya lo venías usando sin la definición**
> La «frontera de decisión» del perceptrón es exactamente esto con $c=2$ y funciones lineales. Un clasificador de mínima distancia —el del SOM etiquetado, el de LVQ— también entra acá: su función discriminante es $g_i(\mathbf{x}) = -\lVert \mathbf{x} - \mathbf{m}_i\rVert$, y elegir el prototipo más cercano es elegir el $g_i$ más grande. **Todos los clasificadores de la materia son casos particulares de esta definición.**

### Clasificadores básicos

**Lineal** — las funciones discriminantes son combinaciones lineales de las características:

$$g(\mathbf{x}) = \sum_{i=1}^{d} w_i x_i + w_0 = \mathbf{w}^{\mathsf{T}}\mathbf{x} + w_0$$

Tiene $d+1$ parámetros y sus fronteras son **hiperplanos**.

**Cuadrático** — se agregan los productos entre características:

$$g(\mathbf{x}) = \sum_{i=1}^{d}\sum_{j=1}^{d} w_{ij}x_i x_j + \sum_{i=1}^{d} w_i x_i + w_0 = \mathbf{x}^{\mathsf{T}}\mathbf{W}\mathbf{x} + \mathbf{w}^{\mathsf{T}}\mathbf{x} + w_0$$

Tiene $\tfrac{1}{2}d(d+1) + d + 1$ parámetros y sus fronteras son **hipercuádricas** (elipsoides, paraboloides, hiperboloides).

> **OJO — el precio de la flexibilidad**
> El cuadrático puede trazar fronteras curvas, pero sus parámetros crecen con $d^2$. Es el mismo compromiso que viste en generalización: más parámetros libres, más capacidad de ajuste y más riesgo de sobre-ajuste.

### Claves de la sección 6

| Clave | Qué tenés que poder responder |
|---|---|
| La definición | $c$ funciones discriminantes y la regla del máximo |
| Región de decisión | Dónde gana una $g_i$ |
| Frontera | Donde se empata: $g_i - g_j = 0$ |
| Lineal vs. cuadrático | Cuántos parámetros y qué forma de frontera |

---

## 7. Las cuatro probabilidades

Todo lo que sigue apunta a construir **una buena función discriminante**. La respuesta va a ser una probabilidad, pero hay que llegar por partes. Van las cuatro definiciones, con el ejemplo de la anemia (clasificar un análisis de sangre en *sano* o *anémico* según el conteo de glóbulos rojos).

### 7.1 Probabilidad a priori $P(\omega_i)$

*La probabilidad de que una muestra cualquiera sea de la clase $\omega_i$, **antes** de mirar la muestra.*

Es la proporción de casos de esa clase en la población: qué fracción de la gente es anémica. Se cumple $0 \le P(\omega_i) \le 1$ y $\sum_i P(\omega_i) = 1$.

Con esto sólo ya se puede armar un clasificador **trivial**: decidir siempre por la clase más probable a priori.

> **OJO — el clasificador trivial acierta muchísimo y no sirve para nada**
> Si el 1 % de la población es anémica, decir *«sano»* siempre acierta el 99 %. Un desempeño altísimo, y un sistema inútil. Y hay algo peor, que es lo que el profesor remarca: **el costo de los dos errores no es el mismo.** Decirle «sano» a un anémico hace que no reciba tratamiento; decirle «anémico» a un sano le cuesta un suplemento de hierro. Nada de esto está contemplado en las probabilidades, y por eso los clasificadores a priori son simples pero inefectivos.

### 7.2 Densidad condicional $P(\mathbf{x}|\omega_i)$

*La probabilidad de observar la muestra $\mathbf{x}$ **sabiendo** que la etiqueta es $\omega_i$.*

La imagen mental de la clase: dos contenedores, uno con todos los análisis de los sanos y otro con los de los anémicos. Metés la mano **en uno de los dos** y preguntás qué chance hay de sacar un conteo de cuatro millones. Caracteriza **cómo se distribuyen las muestras dentro de cada clase**.

Condiciones: $P(\mathbf{x}|\omega_i) \ge 0$ y $\int_E P(\mathbf{x}|\omega_i)\,d\mathbf{x} = 1$.

### 7.3 Probabilidad conjunta $P(\mathbf{x}, \omega_i)$

*La probabilidad de observar la muestra $\mathbf{x}$ **y** que sea de la clase $\omega_i$.*

$$P(\mathbf{x}, \omega_i) = P(\omega_i)\,P(\mathbf{x}|\omega_i)$$

Ahora los dos contenedores se vuelcan en uno solo, se revuelve, y se mete la mano ahí. Es menor que la condicional, porque además de sacar ese valor tiene que tocarte la clase.

### 7.4 Densidad incondicional $P(\mathbf{x})$

*La probabilidad de observar la muestra $\mathbf{x}$, **sin importar** de qué clase sea.*

$$P(\mathbf{x}) = \sum_{j=1}^{c} P(\mathbf{x}, \omega_j) = \sum_{j=1}^{c} P(\mathbf{x}|\omega_j)\,P(\omega_j)$$

Es la suma sobre todas las clases de la anterior. Describe cómo se distribuyen las muestras con independencia de las clases.

### Los cuatro números, sobre el ejemplo del brillo

Volviendo al OCR de ceros y nueves, con el brillo como característica:

| Cantidad | Valor | Se lee |
|---|---|---|
| $P(\omega = 0)$ | $0{,}5$ | hay tantos ceros como nueves: el clasificador trivial no sirve |
| $P(x = 45\,\vert\,\omega = 0)$ | $0{,}033$ | mirando **sólo** la campana de los ceros, cuánto vale en el brillo 45 |
| $P(x = 45,\ \omega = 0)$ | $0{,}016$ | la anterior por la a priori: $0{,}033 \times 0{,}5 \approx 0{,}016$ |
| $P(x = 45)$ | $0{,}054$ | la suma sobre las dos clases: la curva negra |

> **PARA LA DEFENSA — cómo no confundirlas**
> Las cuatro se distinguen por **qué se sabe y qué se pregunta**. *A priori*: sé la clase, no miro la muestra. *Condicional*: sé la clase, pregunto por la muestra. *Conjunta*: pregunto por las dos juntas. *Incondicional*: pregunto por la muestra y no me importa la clase. Si te trabás, acordate de los contenedores: la condicional es meter la mano en **un** contenedor, la incondicional es meterla en **todo mezclado**.

### Claves de la sección 7

| Clave | Qué tenés que poder responder |
|---|---|
| Las cuatro | Escribirlas y decir qué se sabe y qué se pregunta en cada una |
| La conjunta | Que es el producto de las dos primeras |
| La incondicional | Que es la suma de la conjunta sobre todas las clases |
| El clasificador trivial | Por qué acierta mucho y no sirve, y el tema del costo del error |

---

## 8. La probabilidad a posteriori y la regla de Bayes

Ésta es **la pregunta que de verdad queremos contestar**: le damos al sistema el patrón medido —el brillo es 45, el conteo es de tres millones— y queremos que nos diga la clase.

**Probabilidad a posteriori** $P(\omega_i|\mathbf{x})$: *la probabilidad de que la muestra $\mathbf{x}$ pertenezca a $\omega_i$*. Se calcula con la **regla de Bayes**:

$$P(\omega_i|\mathbf{x}) = \frac{P(\mathbf{x}|\omega_i)\,P(\omega_i)}{P(\mathbf{x})} = \frac{P(\mathbf{x}|\omega_i)\,P(\omega_i)}{\sum_{j=1}^{c} P(\mathbf{x}|\omega_j)\,P(\omega_j)}$$

Se cumple $0 \le P(\omega_i|\mathbf{x}) \le 1$ y $\sum_i P(\omega_i|\mathbf{x}) = 1$.

> **IDEA DE FONDO — Bayes es una actualización**
> La a posteriori se puede leer como la **a priori corregida después de haber observado $\mathbf{x}$**. Antes de medir nada, mi mejor apuesta era $P(\omega_i)$; midiendo $\mathbf{x}$, la evidencia me mueve esa apuesta. El numerador la empuja según lo bien que $\mathbf{x}$ encaja en esa clase, y el denominador normaliza para que todo sume 1.

**Qué forma tiene.** En el ejemplo de los dígitos: para los brillos bajos la a posteriori del cero vale prácticamente **1** y la del nueve **0**; para los brillos altos pasa al revés. Y en el medio se cruzan. **Ese punto de cruce es la frontera de decisión** de la sección 6, y es donde el sistema tiene la máxima incerteza.

---

## 9. El clasificador de Bayes

Y ahí está la idea: si la a posteriori ya se comporta como queremos que se comporte una función discriminante —una es mayor donde están los ceros, la otra donde están los nueves— entonces **usémosla como función discriminante**.

**Regla de clasificación de Bayes:** asignar a $\mathbf{x}$ la clase con mayor probabilidad a posteriori.

$$\hat{\omega} = \arg\max_{\omega_i : 1 \le i \le c} P(\omega_i|\mathbf{x})$$

$$g_i(\mathbf{x}) = P(\omega_i|\mathbf{x})$$

### Las tres formas equivalentes

$$g_i(\mathbf{x}) = \frac{P(\mathbf{x}|\omega_i)P(\omega_i)}{P(\mathbf{x})} \;\equiv\; P(\mathbf{x}|\omega_i)P(\omega_i) \;\equiv\; \log P(\mathbf{x}|\omega_i) + \log P(\omega_i)$$

**Y hay que saber justificar los dos pasos:**

1. **Se tira el denominador** porque $P(\mathbf{x})$ es **el mismo para todas las clases**: divide a todas por igual y no cambia cuál es la mayor.
2. **Se aplica el logaritmo** porque es una función **monótona creciente**: no cambia el orden de los valores, y convierte el producto en suma, lo que simplifica las cuentas más adelante (sobre todo con gaussianas).

> **OJO — qué significa que dos clasificadores sean equivalentes**
> $(g_1,\dots,g_c) \equiv (f(g_1),\dots,f(g_c))$ si producen **las mismas regiones de decisión**. Lo que importa de una función discriminante no son sus valores, es **el orden** entre ellas. Por eso se le puede aplicar cualquier función monótona creciente sin cambiar el clasificador.

### El error de Bayes

Para un patrón concreto, el error es la probabilidad de que la clase ganadora no sea la verdadera:

$$P(\text{error}|\mathbf{x}) = 1 - \max_{1 \le i \le c} P(\omega_i|\mathbf{x})$$

Con los números del ejemplo: si el brillo es 30, la a posteriori del cero vale 1, y $1 - 1 = 0$: **error cero**, estoy seguro. Si el brillo es 40 y las a posteriori son $0{,}8$ y $0{,}2$, el error es $1 - 0{,}8 = 0{,}2$: un 20 % de chance de equivocarme con ese patrón.

Promediando sobre todos los patrones posibles:

$$P(\text{error}) = \int_E P(\text{error}|\mathbf{x})\,P(\mathbf{x})\,d\mathbf{x}$$

> **PARA LA DEFENSA — la frase que hay que decir sobre el clasificador de Bayes**
> Es el clasificador **de mínimo error**: es lo mejor que se puede hacer, y ningún método puede superarlo. Su error es la **cota inferior teórica** del problema.

---

## 10. Por qué no se puede usar, y por qué existe el resto de la materia

Si el clasificador de Bayes es óptimo, ¿por qué no lo usamos y listo? Porque **no conocemos lo que necesita**:

- **$P(\omega_i)$ es desconocida.** La proporción de anémicos la podés estimar de tu muestra, pero si hacés el estudio en otra región del mundo puede cambiar, porque esa población es naturalmente distinta.
- **$P(\mathbf{x}|\omega_i)$ es desconocida.** Podés armar el histograma con mil individuos, pero si sumás diez más el histograma cambia. Nunca tenés la distribución verdadera, tenés una estimación.
- Y aunque las tuvieras, **las regiones de integración** del error son complejas.

Faltan justamente **los dos factores del numerador**, así que el clasificador de Bayes es imposible de construir en la práctica.

> **IDEA DE FONDO — ésta es la frase que cierra la unidad y justifica toda la materia**
> *«Todo lo que van a aprender en la materia son métodos que **aproximan** al clasificador de Bayes.»* El error de Bayes es la cota que no se puede bajar, y el perceptrón, el multicapa, las redes de base radial, los clasificadores gaussianos y todo lo demás son intentos de acercarse lo más posible a ella **sin conocer las distribuciones**. Si te preguntan «¿para qué sirve esta unidad si el clasificador no se puede construir?», la respuesta es ésa: sirve para saber contra qué se compara todo lo demás.

### Claves de las secciones 8 a 10

| Clave | Qué tenés que poder responder |
|---|---|
| Regla de Bayes | Escribirla y nombrar cada factor |
| A posteriori | Que es la a priori actualizada por la evidencia |
| El clasificador | $\hat\omega = \arg\max P(\omega_i\vert\mathbf{x})$, y que es de mínimo error |
| Las equivalencias | Por qué se puede tirar $P(\mathbf{x})$ y por qué se puede aplicar $\log$ |
| El error | $1 - \max P(\omega_i\vert\mathbf{x})$, y qué significa en un punto concreto |
| Por qué no se usa | $P(\omega_i)$ y $P(\mathbf{x}\vert\omega_i)$ desconocidas |

---

## 11. Para la pizarra

### Guion A — «Definí un clasificador estadístico»

**Paso 1.** Escribís las $c$ funciones discriminantes $g_i : E \to \mathbb{R}$ y la regla del máximo.

**Paso 2.** Dibujás el espacio partido en regiones y marcás una frontera. Escribís $R_i$ y $g_i - g_j = 0$.

**Paso 3.** Das los dos casos básicos: lineal (fronteras hiperplanos, $d+1$ parámetros) y cuadrático (hipercuádricas, $\tfrac12 d(d+1)+d+1$).

**Paso 4 (el remate).** *«Y el perceptrón es exactamente esto con dos clases y funciones lineales.»* Conectarlo con lo que ya sabés es lo que muestra que entendiste la definición y no la memorizaste.

### Guion B — «Deducí el clasificador de Bayes»

**Paso 1.** Planteás qué querés: una función discriminante que use toda la información disponible. La candidata natural es *«qué probabilidad hay de que esta muestra sea de esta clase»*.

**Paso 2.** Escribís las cuatro definiciones previas, en orden: a priori, condicional, conjunta, incondicional. **Acá va el ejemplo de los dos contenedores**, que se entiende solo.

**Paso 3.** Escribís la regla de Bayes y decís que la a posteriori es la a priori **actualizada** por la evidencia.

> **Llegás a:** $\;P(\omega_i|\mathbf{x}) = \dfrac{P(\mathbf{x}|\omega_i)P(\omega_i)}{P(\mathbf{x})}$

**Paso 4.** Proponés usarla como función discriminante y escribís la regla de decisión.

> **Llegás a:** $\;\hat\omega = \arg\max_{\omega_i} P(\omega_i|\mathbf{x})$

**Paso 5.** Das las dos simplificaciones **con su justificación**: se tira $P(\mathbf{x})$ porque es común a todas las clases; se aplica $\log$ porque es monótona creciente y no cambia el orden.

**Paso 6 (el cierre honesto).** Decís que es de mínimo error **y** que no se puede construir, porque $P(\omega_i)$ y $P(\mathbf{x}|\omega_i)$ son desconocidas. Y rematás: *«todo el resto de la materia son métodos que lo aproximan»*.

---

## 12. Formulario

| Qué | Fórmula |
|---|---|
| Patrón adquirido | $\mathbf{y} = [y_1 \dots y_n]^{\mathsf{T}} \in P \subset \mathbb{R}^n$ |
| Vector de características | $\mathbf{x} = [x_1 \dots x_d]^{\mathsf{T}} \in E \subset \mathbb{R}^d$, con $d \le n$ |
| Clases | $\Omega = \{\omega_1,\dots,\omega_c\}$; con rechazo: $\Omega^* = \Omega \cup \{\omega_0\}$ |
| Regla de decisión | $\mathbf{x} \to \omega_i$ si $g_i(\mathbf{x}) > g_j(\mathbf{x})\ \forall j \neq i$ |
| Región de decisión | $R_i = \{\mathbf{x} : g_i(\mathbf{x}) > g_j(\mathbf{x})\ \forall j\neq i\}$ |
| Frontera de decisión | $g_i(\mathbf{x}) - g_j(\mathbf{x}) = 0$ |
| Clasificador lineal | $g(\mathbf{x}) = \mathbf{w}^{\mathsf{T}}\mathbf{x} + w_0$, con $d+1$ parámetros |
| Clasificador cuadrático | $g(\mathbf{x}) = \mathbf{x}^{\mathsf{T}}\mathbf{W}\mathbf{x} + \mathbf{w}^{\mathsf{T}}\mathbf{x} + w_0$, con $\tfrac12 d(d+1)+d+1$ |
| Conjunta | $P(\mathbf{x},\omega_i) = P(\omega_i)P(\mathbf{x}|\omega_i)$ |
| Incondicional | $P(\mathbf{x}) = \sum_j P(\mathbf{x}|\omega_j)P(\omega_j)$ |
| Regla de Bayes | $P(\omega_i|\mathbf{x}) = \dfrac{P(\mathbf{x}|\omega_i)P(\omega_i)}{P(\mathbf{x})}$ |
| Clasificador de Bayes | $\hat\omega = \arg\max_{\omega_i} P(\omega_i|\mathbf{x})$ |
| Formas equivalentes | $P(\omega_i|\mathbf{x}) \equiv P(\mathbf{x}|\omega_i)P(\omega_i) \equiv \log P(\mathbf{x}|\omega_i) + \log P(\omega_i)$ |
| Error puntual | $P(\text{error}|\mathbf{x}) = 1 - \max_i P(\omega_i|\mathbf{x})$ |
| Error medio | $P(\text{error}) = \int_E P(\text{error}|\mathbf{x})P(\mathbf{x})\,d\mathbf{x}$ |

---

## 13. Errores típicos

| Error | Lo correcto |
|---|---|
| Confundir $P(\mathbf{x}\vert\omega_i)$ con $P(\omega_i\vert\mathbf{x})$ | La condicional sabe la clase y pregunta por la muestra; la a posteriori es al revés |
| Decir que el clasificador trivial «anda mal» | Anda **muy bien** en aciertos; el problema es que ignora el costo del error y no aprende nada |
| Escribir la incondicional sin la a priori | Es $\sum_j P(\mathbf{x}\vert\omega_j)P(\omega_j)$, no la suma de las condicionales sola |
| Tirar $P(\mathbf{x})$ sin justificar | Se puede porque es **común a todas las clases**; hay que decirlo |
| Decir que el logaritmo «simplifica» y nada más | La razón es que es **monótona creciente**: no altera el orden, y por eso no cambia las regiones |
| Decir que el clasificador de Bayes es imposible «porque es muy complejo» | Es imposible porque **no se conocen $P(\omega_i)$ ni $P(\mathbf{x}\vert\omega_i)$** |
| Confundir la $\mathbf{y}$ de esta unidad con la salida de una neurona | Acá $\mathbf{y}$ es el patrón crudo adquirido |
| Llamar «patrón» al vector de características | El patrón es el objeto; $\mathbf{x}$ es su descripción. La clase avisa que la literatura los mezcla |

---

## 14. Autoevaluación

1. Enunciá la definición de aprendizaje maquinal con sus tres elementos.
2. ¿Qué diferencia a la IA clásica del reconocimiento de formas? Nombrá el tipo de aprendizaje de cada una.
3. Dibujá el diagrama de bloques y decí qué hace cada uno. ¿En cuáles entra la experticia humana?
4. ¿Por qué hace falta la extracción de características? Usá el ejemplo de la cara.
5. Nombrá las tres propiedades deseables de las características y decí cuál es la que no se puede relajar, y por qué.
6. Definí clasificador estadístico, región de decisión y frontera de decisión.
7. ¿Cuántos parámetros tiene un clasificador cuadrático en dimensión $d$? ¿Qué forma tienen sus fronteras?
8. Escribí las cuatro probabilidades y explicá cada una con el ejemplo de los contenedores.
9. Dados $P(x=45|\omega=0) = 0{,}033$ y $P(\omega=0)=0{,}5$, calculá la conjunta. ¿Qué te falta para la a posteriori?
10. Escribí la regla de Bayes y justificá las dos formas equivalentes del clasificador.
11. Si para un patrón las a posteriori valen $0{,}8$ y $0{,}2$, ¿cuál es el error puntual? ¿Y si valen $1$ y $0$?
12. ¿Por qué el clasificador de Bayes es de mínimo error y por qué igual no se puede construir?
13. ¿En qué sentido el perceptrón, el multicapa y las radiales son «aproximaciones» al clasificador de Bayes?
