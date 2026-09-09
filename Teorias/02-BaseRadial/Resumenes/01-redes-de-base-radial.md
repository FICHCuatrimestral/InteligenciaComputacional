---
title: "Redes neuronales con funciones de base radial"
subtitle: "Inteligencia Computacional · FICH-UNL · Diego Milone \\newline Diapositivas de *Redes con funciones de base radial* y transcripciones de clase 015 a 018"
lang: es
---

*Notación: vectores columna; **negritas** para vectores y matrices ($\mathbf{x}$, $\mathbf{U}_j$). El subíndice $j$ recorre las neuronas de la capa radial, el $k$ las de la capa de salida, el $\ell$ los patrones y el $i$ las dimensiones de la entrada. Mantener esos cuatro índices separados es la mitad del tema.*

*Cinco diapositivas de la cátedra tienen sólo el título: el profesor dibujaba en el pizarrón. Las figuras 1, 2, 3, 5, 10 y 11 reconstruyen esos dibujos a partir de su descripción hablada, y están marcadas como tales.*

---

## El ejemplo que atraviesa el apunte

Cada sección de este apunte termina en un recuadro **EN NÚMEROS** que aplica lo que se acaba de
explicar sobre **el mismo caso**, elegido chico a propósito: **seis patrones, una sola entrada, tres
neuronas radiales**. Todo el ejemplo entra en media pizarra y las cuentas se hacen de memoria.

**Los datos.** Seis patrones sobre la recta, con la clase alternada de a pares:

| $\ell$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| $x_\ell$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| $d_\ell$ | $+1$ | $+1$ | $-1$ | $-1$ | $+1$ | $+1$ |

![Los seis patrones. Ningún umbral único los clasifica bien: el problema no es linealmente separable.](../imagenes/14-ejemplo-patrones.png)

**Por qué sirve este caso.** Un perceptrón simple con una entrada sólo puede poner **un** umbral:
todo lo que está a la izquierda va a una clase y todo lo que está a la derecha, a la otra. Acá la
clase $+1$ aparece **a los dos lados** de la clase $-1$, así que no hay umbral que sirva. Es el XOR
otra vez, aplastado sobre una recta: la misma dificultad, con la mitad de dibujo.

> **EN CRIOLLO — el problema en una frase**
> *"Los buenos están en los bordes y los malos en el medio."* Con una regla no se puede. Con tres
> aros —uno sobre cada par— sí: dos aros que suman y uno en el medio que resta.

**El recorrido.** Cada cuenta aparece dos veces: corta, en el recuadro de su sección, y de nuevo,
encadenada con las demás, en la sección 11.

| Sección | Qué se calcula sobre el ejemplo | Resultado |
|---|---|---|
| 4 | Una activación $\varphi_j$ a mano | $\varphi_1(x_3) = 0{,}0111$ |
| 6 | $k$-medias por lotes, dos iteraciones | $\boldsymbol{\mu} = 0{,}5\;\cdot\;2{,}5\;\cdot\;4{,}5$ |
| 6 | Un paso de $k$-medias online | $\mu_2: 2 \to 2{,}5$ |
| 7 | Las tres desviaciones | $\sigma_j = 0{,}5$ para las tres |
| 8 | La tabla completa de $\varphi$ y dos pasos de LMS | $6\times3$ activaciones |
| 11 | Todo junto, hasta la red entrenada | $\xi = 0{,}0007$ |

> **IDEA DE FONDO — por qué el ejemplo es de una sola dimensión**
> Porque en $\mathbb{R}^1$ la distancia $\lVert x - \mu_j \rVert$ es un valor absoluto, y **eso** es lo
> único que hay que entender de la capa radial. Todo lo que sigue —$k$-medias, $\sigma$, LMS— tiene
> exactamente la misma forma en $\mathbb{R}^{1}$ que en $\mathbb{R}^{1000}$: lo único que cambia es que
> la resta pasa a ser vectorial. Si podés hacer el caso de una dimensión sin mirar el apunte, el caso
> general es el mismo con negritas.

---

## 1. Por qué aparecen: el XOR, una vez más

El XOR ya está resuelto —con tres perceptrones, o con una capa oculta y back-propagation— pero vale la pena volver a mirar *cómo* quedó resuelto, porque ahí está la idea de esta unidad.

Cada neurona con sigmoide, vista en tres dimensiones, es **un papel doblado**: una zona plana en $-1$, una subida y una zona plana en $+1$. Con la función signo la subida sería un escalón; con la sigmoide es una rampa. Lo único que se elige al entrenar es *dónde* está el doblez y *hacia dónde* mira.

![Reconstrucción de las diapositivas 2 a 4](../imagenes/01-papel-doblado.png)

La franja del XOR sale de superponer dos de esos papeles: uno que sube a la izquierda, otro que sube a la derecha, y una tercera neurona que combina las dos regiones. Funciona, pero es un rodeo: para encerrar una zona hay que armarla como intersección de medios planos.

> **IDEA DE FONDO — el problema no era el XOR, era la forma de la función**
> Un hiperplano sigmoideo siempre parte el espacio en dos mitades **infinitas**. Para encerrar algo hay que cruzar varias mitades, y por eso hacen falta capas. Si en vez de un papel doblado se usa una función que ya viene **cerrada** —una campana alrededor de un centro— encerrar una región deja de ser un problema de combinar y pasa a ser un problema de ubicar.

![Reconstrucción de las diapositivas 4 y 5](../imagenes/02-sigmoide-vs-radial.png)

Se llama **radial** porque su valor depende sólo del **radio**: de la distancia al centro, no de la dirección. Todos los puntos que están a la misma distancia de $\boldsymbol{\mu}_j$ valen lo mismo.

![Reconstrucción de la diapositiva 6](../imagenes/03-regiones-radiales.png)

Con radiales, el XOR se resuelve poniendo un círculo sobre cada patrón positivo y sumando las dos salidas. No hay que combinar semiplanos: hay que ubicar centros.

> **EN CRIOLLO — tablones contra aros**
> Una sigmoide es un **tablón** apoyado sobre el patio: de un lado el suelo, del otro una tarima, y el
> tablón sigue hasta donde te alcance la vista. Para encerrar el cantero del medio necesitás cuatro
> tablones cruzados. Una radial es un **aro** que tirás alrededor del cantero: uno solo, y ya está.
> Cambiar de sigmoides a radiales es cambiar de *combinar cortes* a *tirar aros*.

### Claves de la sección 1

| Clave | Qué tenés que poder responder |
|---|---|
| Papel doblado | Qué forma tiene una sigmoide en 3D y por qué no encierra nada |
| Radial | Por qué se llama así: depende del radio, no de la dirección |
| El cambio de fondo | Se cambia la *función de activación*, no la arquitectura |

---

## 2. De dónde vienen: aproximación de funciones

Las RBF **no** nacieron como clasificadores. Nacieron para **aproximar funciones**:

$$\varphi : \mathbb{R}^N \to \mathbb{R}, \qquad d = \varphi(\mathbf{x})$$

La salida deseada $d$ es un **real continuo**, no un $\pm 1$. Ésa es la diferencia de origen con el perceptrón, y explica por qué la capa de salida termina siendo lineal.

La propuesta de aproximación es una suma pesada de funciones centradas:

$$h(\mathbf{x}) = \sum_j w_j\, \varphi\!\left(\lVert \mathbf{x} - \boldsymbol{\mu}_j \rVert\right)$$

y la $\varphi$ que se usa casi siempre —y la que usa la cátedra— es la gaussiana:

$$\varphi(\kappa) = e^{-\frac{\kappa^2}{2\sigma^2}}$$

![Diapositiva 10: cada pico es un centro, y su altura la fija el peso](../imagenes/04-suma-de-gaussianas.png)

> **IDEA DE FONDO — leé la fórmula de adentro hacia afuera**
> Primero una **distancia** $\lVert \mathbf{x} - \boldsymbol{\mu}_j \rVert$, que es un escalar. Después una **no linealidad** $\varphi$ aplicada a ese escalar. Recién al final una **combinación lineal** con los pesos. Todo lo raro de la red pasa en el primer paso: es el único lugar de la materia donde la entrada no se combina con los pesos mediante un producto interno, sino que se compara con un prototipo mediante una distancia.

> **EN CRIOLLO — la red es una consola de sonido**
> Imaginate $M$ parlantes repartidos en un salón. El centro $\boldsymbol{\mu}_j$ dice **dónde está**
> cada parlante, la desviación $\sigma_j$ **hasta dónde llega**, y el peso $w_j$ el **volumen**, que
> además puede ser negativo (el parlante en contrafase, restando). La salida de la red en un punto
> $\mathbf{x}$ es *lo que se escucha parado ahí*. Entrenar es: primero repartir los parlantes por el
> salón, después regular los volúmenes.

### Claves de la sección 2

| Clave | Qué tenés que poder responder |
|---|---|
| Origen | Aproximación de funciones con salida real, no clasificación |
| $\lVert \mathbf{x}-\boldsymbol{\mu}_j \rVert$ | Distancia a un prototipo, no producto interno |
| El rol de $w_j$ | Le da la altura (y el signo) a cada campana |

---

## 3. La arquitectura

![Reconstrucción de las diapositivas 11 y 12](../imagenes/05-arquitectura.png)

Tres columnas y muy pocas reglas:

- **Entradas.** Los pesos entre la entrada y la capa radial **se fijan en 1** y no se entrenan. La entrada llega entera a cada gaussiana; lo que la neurona hace con ella lo deciden $\boldsymbol{\mu}_j$ y $\sigma_j$.
- **Capa radial.** Cada neurona es una gaussiana en $\mathbb{R}^N$, con $N$ la dimensión de la entrada. **No tiene sesgo**: sus parámetros son el vector de medias y la desviación.
- **Salida.** Un perceptrón simple con **salida lineal**: los pesos $w_{kj}$, la entrada $-1$ y su $w_{k0}$, y ninguna función de activación no lineal. Puede haber varias neuronas de salida.

> **OJO — dos negaciones que se preguntan**
> La capa radial **no** tiene sesgo, y la capa de salida **no** tiene no linealidad. Las dos son al revés que en el perceptrón multicapa, y las dos tienen la misma explicación: la no linealidad de esta red está toda concentrada en la gaussiana.

### Claves de la sección 3

| Clave | Qué tenés que poder responder |
|---|---|
| Pesos de entrada | Fijos en 1, no se entrenan |
| Capa radial | Sin sesgo; parámetros $\boldsymbol{\mu}_j$ y $\sigma_j$ |
| Capa de salida | Perceptrón simple lineal, con su $-1$ y su $w_{k0}$ |

---

## 4. El modelo matemático

$$y_k(\mathbf{x}_\ell) = \sum_{j=1}^{M} w_{kj}\, \varphi_j(\mathbf{x}_\ell)
\qquad\text{con}\qquad
\varphi_j(\mathbf{x}_\ell) = e^{-\frac{\lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2}{2\sigma_j^2}}$$

Dos líneas y está toda la red. Conviene decirlas en voz alta así: *"la salida $k$ es la suma pesada de las $M$ salidas radiales, y cada salida radial es una gaussiana centrada en su propio $\boldsymbol{\mu}_j$"*.

Los índices, uno por uno:

| Índice | Recorre | Cuántos |
|:---:|---|---|
| $k$ | neuronas de la capa de salida | tantas como salidas pida el problema |
| $j$ | neuronas de la capa radial | $M$, se elige |
| $\ell$ | patrones del conjunto de entrenamiento | los que haya |
| $i$ o $k'$ | dimensiones de la entrada | $N$ |

**¿Cuáles son los parámetros a entrenar?** La pregunta está textual en la diapositiva 15, así que conviene tener la respuesta lista:

1. los centros $\boldsymbol{\mu}_j$ — uno por neurona radial, cada uno en $\mathbb{R}^N$;
2. las desviaciones $\sigma_j$ — o la matriz $\mathbf{U}_j$ en el caso general;
3. los pesos $w_{kj}$ de la capa de salida.

> **PARA LA DEFENSA — el modelo de la diapositiva está simplificado**
> Hay **un solo** $\sigma_j$ por neurona, igual para todas las dimensiones: la gaussiana es esférica. El caso general —una matriz de covarianza por neurona— es la sección 9. Si te preguntan por el modelo "posta", ése es.

> **EN NÚMEROS — una activación, a mano**
> Adelantando los centros que va a encontrar $k$-medias en la sección 6 —$\mu_1 = 0{,}5$,
> $\mu_2 = 2{,}5$, $\mu_3 = 4{,}5$, todos con $\sigma_j = 0{,}5$— la activación de la primera neurona
> ante el tercer patrón, $x_3 = 2$, sale en tres pasos:
> $$\text{distancia: } \lVert x_3 - \mu_1 \rVert = |2 - 0{,}5| = 1{,}5
> \qquad\Longrightarrow\qquad
> \frac{1{,}5^2}{2\,(0{,}5)^2} = \frac{2{,}25}{0{,}5} = 4{,}5$$
> $$\varphi_1(x_3) = e^{-4{,}5} = 0{,}0111$$
> Con la **misma** cuenta, la segunda neurona —que tiene el centro justo al lado, a $0{,}5$— da
> $\varphi_2(x_3) = e^{-0{,}5} = 0{,}6065$. Un patrón que está a **tres veces** la distancia activa
> **cincuenta y cinco veces menos**: ésa es la localidad de la que habla la sección 10, en números.

---

## 5. El entrenamiento es mixto

Ésta es la particularidad de la unidad, y es lo primero que hay que decir si te preguntan por RBF:

> **IDEA DE FONDO — una red, dos paradigmas de aprendizaje**
> La capa radial se entrena **sin supervisión**: no se usa la salida deseada $d$ en ningún momento. La capa de salida se entrena **con supervisión**, igual que un perceptrón. Es el primer método no supervisado de la materia, y la primera red que combina los dos paradigmas.

La cátedra plantea dos métodos:

**Método 1 (el que se usa).** Dos etapas separadas.

1. Adaptación **no supervisada** de las RBF — por $k$-medias, por mapas autoorganizativos u otros.
2. Adaptación **supervisada** de los $w_{kj}$ — por LMS.

**Método 2.** Se inicializa con el método 1 y después se hace una adaptación supervisada de **todo**, incluidos los parámetros de la capa radial, calculando $\dfrac{\partial \xi}{\partial \mu_{ji}}$ y $\dfrac{\partial \xi}{\partial \sigma_j}$.

En general se adaptan las RBF y los $w_{kj}$ **por separado**. Es lo que vamos a desarrollar.

> **EN CRIOLLO — dos oficios distintos, uno después del otro**
> Primero entra alguien que **no sabe de qué se trata el problema** y sólo mira dónde se amontonan los
> puntos, para plantar ahí los parlantes: ése es $k$-medias, y nunca ve las etiquetas $d$. Recién
> después entra el que **sí** sabe las respuestas correctas y se limita a subir y bajar los volúmenes
> hasta que suene bien: ése es el LMS. El primero acomoda el espacio; el segundo lo aprovecha.

---

## 6. Etapa 1 — los centros por $k$-medias

### 6.1 Qué se busca

Encontrar $k$ conjuntos $C_j$ de patrones tales que:

- cada conjunto sea **lo más diferente posible** de los demás;
- los patrones **dentro** de cada conjunto sean **lo más parecidos posible** entre ellos;

y, para cada uno, su **centroide** $\boldsymbol{\mu}_j$ — que después será el centro de la gaussiana de la neurona $j$.

> **OJO — la $k$ de $k$-medias es la cantidad de neuronas radiales**
> No es un índice más: si ponés 10 neuronas en la capa radial, $k$-medias tiene que encontrar 10 conjuntos. Elegir la arquitectura y elegir $k$ son la misma decisión.

El criterio a minimizar es la suma de las distancias de cada patrón a su propio centroide:

$$\min J = \sum_{j=1}^{k} \sum_{\ell \in C_j} \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2$$

![El ejemplo que dibuja el profesor: correr el centroide sólo agranda $J$](../imagenes/07-centroide-bien-y-mal.png)

### 6.2 $k$-medias por lotes

1. **Inicialización.** Se forman los $k$ conjuntos $C_j(0)$ repartiendo los patrones $\mathbf{x}_\ell$ **al azar**.
2. **Centroides.** $\displaystyle \boldsymbol{\mu}_j(n) = \frac{1}{|C_j(n)|} \sum_{\ell \in C_j(n)} \mathbf{x}_\ell$ — un promedio vectorial simple, no ponderado.
3. **Reasignación.** Cada patrón se va al conjunto cuyo centroide tenga más cerca: $$\ell \in C_j(n) \iff \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 < \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_i \rVert^2 \quad \forall\, i \neq j$$
4. **Volver a 2** hasta que no se realicen reasignaciones.

![Los cuatro pasos, con tres grupos](../imagenes/06-kmedias-por-lotes.png)

> **IDEA DE FONDO — el promedio del paso 2 no es una receta, es la solución exacta**
> Con los conjuntos fijos, derivá $J$ respecto de $\boldsymbol{\mu}_j$ y igualá a cero: $\;\nabla_{\boldsymbol{\mu}_j} J = -2\sum_{\ell \in C_j}(\mathbf{x}_\ell - \boldsymbol{\mu}_j) = \mathbf{0}$, o sea $\sum_\ell \mathbf{x}_\ell = |C_j|\,\boldsymbol{\mu}_j$. El promedio **es** el punto donde el gradiente se anula. Por eso $k$-medias no necesita paso de aprendizaje: resuelve exactamente medio problema en cada iteración, y alterna.

**El criterio de parada es discreto.** No se para cuando $J$ baja poco: se para cuando **ningún patrón cambia de conjunto**. Si nadie se mueve, los centroides tampoco cambian, y la iteración siguiente sería idéntica.

> **EN CRIOLLO — los mozos del salón**
> $k$ mozos y un montón de mesas. Cada mesa se anota con el mozo que tiene **más cerca**; después cada
> mozo se para **en el medio** de las mesas que le tocaron. Al correrse, algunas mesas quedan más cerca
> de otro mozo y se cambian, y hay que volver a pararse en el medio. Se repite hasta que **ninguna mesa
> se cambia de mozo**: ahí el reparto se estabilizó. Los dos pasos que alternan son literalmente
> *"anotarse con el más cercano"* y *"pararse en el medio de los míos"*.

> **EN NÚMEROS — $k$-medias sobre los seis patrones**
> Se arranca con un reparto al azar en tres grupos: $C_1 = \{x_1, x_3\}$, $C_2 = \{x_2, x_4\}$,
> $C_3 = \{x_5, x_6\}$, o sea $\{0, 2\}$, $\{1, 3\}$ y $\{4, 5\}$.
>
> **Iteración 1 — centroides.** $\;\mu_1 = \tfrac{0+2}{2} = 1$, $\;\mu_2 = \tfrac{1+3}{2} = 2$,
> $\;\mu_3 = \tfrac{4+5}{2} = 4{,}5$. El criterio arranca en
> $J = (1^2{+}1^2) + (1^2{+}1^2) + (0{,}5^2{+}0{,}5^2) = 4{,}5$.
>
> **Iteración 1 — reasignación.** Cada patrón se fija cuál de los tres centroides tiene más cerca:
>
> | $x_\ell$ | a $\mu_1{=}1$ | a $\mu_2{=}2$ | a $\mu_3{=}4{,}5$ | va a |
> |:---:|:---:|:---:|:---:|:---:|
> | $0$ | $\mathbf{1{,}0}$ | $2{,}0$ | $4{,}5$ | $C_1$ |
> | $1$ | $\mathbf{0{,}0}$ | $1{,}0$ | $3{,}5$ | $C_1$ |
> | $2$ | $1{,}0$ | $\mathbf{0{,}0}$ | $2{,}5$ | $C_2$ |
> | $3$ | $2{,}0$ | $\mathbf{1{,}0}$ | $1{,}5$ | $C_2$ |
> | $4$ | $3{,}0$ | $2{,}0$ | $\mathbf{0{,}5}$ | $C_3$ |
> | $5$ | $4{,}0$ | $3{,}0$ | $\mathbf{0{,}5}$ | $C_3$ |
>
> Los grupos quedaron $\{0,1\}$, $\{2,3\}$ y $\{4,5\}$: **cambiaron**, así que se vuelve al paso 2.
>
> **Iteración 2 — centroides.** $\;\mu_1 = 0{,}5$, $\;\mu_2 = 2{,}5$, $\;\mu_3 = 4{,}5$, y ahora
> $J = 3 \times (0{,}5^2 {+} 0{,}5^2) = 1{,}5$ — bajó de $4{,}5$ a $1{,}5$.
>
> **Iteración 2 — reasignación.** Cada patrón ya está pegado a su centroide, a $0{,}5$ de distancia, y
> el siguiente centroide está a $2$. **Nadie se mueve** $\Rightarrow$ el algoritmo para.

![Las dos iteraciones sobre los seis patrones. La tercera es idéntica a la segunda: por eso se corta.](../imagenes/15-ejemplo-kmedias.png)

> **OJO — fijate que $k$-medias nunca miró las clases**
> Los grupos que encontró, $\{0,1\}$, $\{2,3\}$ y $\{4,5\}$, coinciden con los pares de clase igual.
> Eso **no** es porque el algoritmo las conociera —no vio ni un solo $d_\ell$— sino porque en este
> problema los patrones de la misma clase están juntos. Es exactamente la apuesta de las RBF: *si los
> datos se agrupan por geometría, los grupos van a servir para clasificar*.

### 6.3 $k$-medias online, y el gradiente que la diapositiva saltea

En lugar de recorrer todo el conjunto y después ajustar, se ajusta **patrón por patrón**. La diapositiva 30 escribe $\nabla_{\boldsymbol{\mu}} J = 0$ y en la línea siguiente aparece la regla ya hecha. Éstos son los pasos del medio.

Para el patrón $\mathbf{x}_\ell$ que acaba de entrar, el único término de $J$ que le corresponde es el de su conjunto:

$$J_\ell = \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 = (\mathbf{x}_\ell - \boldsymbol{\mu}_j)^{\mathsf{T}} (\mathbf{x}_\ell - \boldsymbol{\mu}_j)$$

Se deriva respecto del vector $\boldsymbol{\mu}_j$, con la regla de la cadena (la derivada interna es $-\mathbf{I}$):

$$\nabla_{\boldsymbol{\mu}_j} J_\ell = 2\,(\mathbf{x}_\ell - \boldsymbol{\mu}_j) \cdot (-1) = -2\,(\mathbf{x}_\ell - \boldsymbol{\mu}_j)$$

Se da un paso **en contra** del gradiente, con velocidad $\eta'$:

$$\boldsymbol{\mu}_j(n+1) = \boldsymbol{\mu}_j(n) - \eta' \nabla_{\boldsymbol{\mu}_j} J_\ell = \boldsymbol{\mu}_j(n) + 2\eta'\,(\mathbf{x}_\ell - \boldsymbol{\mu}_j(n))$$

y absorbiendo el 2 en la constante ($\eta = 2\eta'$) queda la regla de la diapositiva:

$$\boxed{\;\boldsymbol{\mu}_j(n+1) = \boldsymbol{\mu}_j(n) + \eta\,\big(\mathbf{x}_\ell - \boldsymbol{\mu}_j(n)\big)\;}$$

**El algoritmo completo:**

1. **Inicialización.** Se eligen $k$ patrones al azar y se usan directamente como centroides iniciales: $\boldsymbol{\mu}_j(0) = \mathbf{x}'_\ell$.
2. **Selección del ganador.** $\;j^* = \arg\min_j \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j(n) \rVert$
3. **Adaptación.** $\;\boldsymbol{\mu}_{j^*}(n+1) = \boldsymbol{\mu}_{j^*}(n) + \eta\,(\mathbf{x}_\ell - \boldsymbol{\mu}_{j^*}(n))$
4. **Volver a 2** hasta no encontrar mejoras significativas en $J$.

![Sólo el ganador se mueve, y sólo una fracción $\eta$ del camino](../imagenes/08-kmedias-online.png)

> **OJO — leé la regla geométricamente antes de memorizarla**
> $\mathbf{x}_\ell - \boldsymbol{\mu}_{j^*}$ es el vector que va **del centroide al patrón**. La regla dice: *dá un paso de tamaño $\eta$ en esa dirección*. Con $\eta = 1$ el centroide salta encima del patrón y se olvida de todo lo anterior; con $\eta = 0$ no aprende nunca. Es exactamente la misma lectura que la corrección de error del perceptrón.

> **OJO — tres diferencias entre las dos versiones**
> **(1)** Por lotes cada vuelta del ciclo procesa **todo** el conjunto; online, **un solo patrón**. **(2)** Por lotes se mueven **todos** los centroides a la vez; online, **sólo el ganador**. **(3)** Por lotes no hay $\eta$; online sí. El criterio de parada también cambia: reasignaciones nulas contra "no hay mejoras significativas en $J$".

> **EN NÚMEROS — un paso de $k$-medias online**
> Partiendo de los mismos centroides de la primera iteración, $\mu_1 = 1$, $\mu_2 = 2$,
> $\mu_3 = 4{,}5$, y con $\eta = 0{,}5$, entra el patrón $x_4 = 3$.
>
> **Ganador:** las distancias son $|3-1| = 2$, $|3-2| = 1$ y $|3-4{,}5| = 1{,}5$, así que
> $j^{*} = 2$.
>
> **Adaptación:** $\;\mu_2 \leftarrow 2 + 0{,}5\,(3 - 2) = 2 + 0{,}5 = \mathbf{2{,}5}$.
>
> El centroide caminó **la mitad** del camino hacia el patrón, y los otros dos **no se tocaron**.
> Con $\eta = 1$ hubiera saltado a $3$, encima del patrón; con $\eta = 0{,}1$ hubiera llegado sólo a
> $2{,}1$. Que en este caso caiga justo en el $2{,}5$ que da la versión por lotes es una casualidad
> agradable del ejemplo, no una regla.

### Claves de la sección 6

| Clave | Qué tenés que poder responder |
|---|---|
| $J$ | Suma de distancias al cuadrado de cada patrón a su centroide |
| Los dos pasos que alternan | Recalcular centroides / reasignar patrones |
| Por qué el promedio | Es la solución exacta de $\nabla J = 0$ con los conjuntos fijos |
| $j^*$ | El centroide ganador: el más cercano al patrón que entró |
| Parada | Sin reasignaciones (lotes) / sin mejoras en $J$ (online) |

---

## 7. Cómo se elige $\sigma$

$k$-medias entrega los centros, no los anchos. Para $\sigma_j$ el criterio de la cátedra es directo: **una vez que tenés el centroide, calculás la desviación de los patrones que quedaron en ese conjunto respecto de él.**

$$\sigma_j^2 = \frac{1}{N\,|C_j|} \sum_{\ell \in C_j} \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2$$

![Un grupo apretado da una gaussiana chica; uno desparramado, una grande](../imagenes/13-sigma-desde-el-grupo.png)

> **OJO — la fórmula exacta es reconstrucción, el criterio no**
> En la clase el criterio se dice en palabras ("calcular la desviación entre ese centroide y todos los puntos que están adentro del conjunto") y no queda escrito en ninguna diapositiva. La expresión de arriba es esa idea puesta en símbolos: promedio de las distancias al cuadrado, dividido por $N$ para que quede una varianza **por dimensión** compatible con el $2\sigma_j^2$ del denominador. Si en el pizarrón te piden "la" fórmula, decí el criterio y escribila; lo que se evalúa es que entiendas de dónde sale, no un número.

> **IDEA DE FONDO — por qué se puede ser tan informal con $\sigma$**
> Porque **los pesos de salida arreglan lo que $\sigma$ no ajusta**. Si una gaussiana quedó ancha de más, su $w_{kj}$ puede bajarle la importancia en la suma final. Ésa es la razón por la que hasta el modelo más pobre —todas las gaussianas del mismo tamaño, $\mathbf{U}_j = \mathbf{I}$— funciona bien en la práctica, y es textual de la clase 018.

> **EN CRIOLLO — $\sigma$ es el alcance de la antena**
> El centroide dice **dónde** se planta la antena; $\sigma$, **hasta dónde llega la señal**. Y el
> criterio es de sentido común: si los clientes de esa antena están todos apretados a la vuelta,
> alcanza con una antena chica; si están desparramados, hay que ponerle más potencia. Nada más que eso
> dice la fórmula.

> **EN NÚMEROS — las tres desviaciones del ejemplo**
> El grupo $C_1 = \{0, 1\}$ tiene centroide $\mu_1 = 0{,}5$, y sus dos patrones están **los dos** a
> $0{,}5$ de él. Con $N = 1$ y $|C_1| = 2$:
> $$\sigma_1^2 = \frac{1}{1 \times 2}\Big[(0 - 0{,}5)^2 + (1 - 0{,}5)^2\Big]
> = \frac{0{,}25 + 0{,}25}{2} = 0{,}25
> \qquad\Longrightarrow\qquad \sigma_1 = 0{,}5$$
> Los otros dos grupos tienen exactamente la misma forma —dos patrones separados por $1$— así que
> $\sigma_2 = \sigma_3 = 0{,}5$ también. Las tres gaussianas quedan **del mismo tamaño**, que es el
> caso $\mathbf{U}_j = \sigma^2\mathbf{I}$ de la sección 9.
>
> **El control:** $\sigma$ tiene que dar del orden del **medio ancho del grupo**. Acá el grupo mide
> $1$ de punta a punta y $\sigma$ dio $0{,}5$. Si te da $5$ o $0{,}01$, te equivocaste en la cuenta.

---

## 8. Etapa 2 — los pesos de la capa de salida

### 8.1 El desdoblamiento: por qué esto es un perceptrón simple

La etapa 1 terminó. Los $\boldsymbol{\mu}_j$ y los $\sigma_j$ quedan **fijos**, y los pesos de entrada ya estaban fijos en 1. Entonces, para cada patrón, la capa radial produce siempre el mismo vector de salidas $\boldsymbol{\varphi}(\mathbf{x}_\ell)$.

![La misma red, mirada de las dos maneras](../imagenes/09-desdoblamiento.png)

La imagen que usa el profesor: es como si alguien tomara tu archivo con las columnas $x_1, x_2$ y te devolviera **otro archivo** con las columnas $\varphi_1, \varphi_2, \varphi_3, \varphi_4$. Con ese archivo nuevo entrenás, y te olvidás de que hubo una etapa previa.

$$\mathbf{y} = \mathbf{W}\,\boldsymbol{\varphi}(\mathbf{x}_\ell)$$

Métodos para obtener $\mathbf{W}$:

- **pseudo-inversa** de $\boldsymbol{\varphi}(\mathbf{x}_\ell)$ — despejar $\mathbf{W}$ de un tirón, sin iterar;
- **gradiente descendente** sobre el error cuadrático instantáneo (**LMS**) — el que se desarrolla.

> **IDEA DE FONDO — de acá sale toda la ventaja de las RBF**
> Con la capa radial congelada, el problema que queda es **lineal en los parámetros**. No hay retropropagación, no hay derivada de sigmoide, no hay mínimos locales del lado supervisado. Cuando en la comparación con el MLP se dice "convergencia más simple (linealidad)", se está hablando exactamente de esto.

> **EN CRIOLLO — las gaussianas te entregan un boletín**
> Cada neurona radial es un examinador que mira el patrón y pone una nota del $0$ al $1$: *"¿cuánto se
> parece esto a mi prototipo?"*. Con $M$ neuronas, cada patrón sale con un **boletín de $M$ notas**. La
> capa de salida no vuelve a mirar el patrón nunca más: sólo mira el boletín y decide. Y decidir a
> partir de un boletín de notas es un perceptrón simple.

> **EN NÚMEROS — el boletín de los seis patrones**
> Con $\mu = (0{,}5;\;2{,}5;\;4{,}5)$ y $\sigma_j = 0{,}5$, o sea
> $\varphi_j(x) = e^{-2\,(x - \mu_j)^2}$, el archivo nuevo del que habla el profesor es éste:
>
> | $\ell$ | $x_\ell$ | $\varphi_1$ | $\varphi_2$ | $\varphi_3$ | $d_\ell$ |
> |:---:|:---:|:---:|:---:|:---:|:---:|
> | 1 | $0$ | $\mathbf{0{,}6065}$ | $0{,}0000$ | $0{,}0000$ | $+1$ |
> | 2 | $1$ | $\mathbf{0{,}6065}$ | $0{,}0111$ | $0{,}0000$ | $+1$ |
> | 3 | $2$ | $0{,}0111$ | $\mathbf{0{,}6065}$ | $0{,}0000$ | $-1$ |
> | 4 | $3$ | $0{,}0000$ | $\mathbf{0{,}6065}$ | $0{,}0111$ | $-1$ |
> | 5 | $4$ | $0{,}0000$ | $0{,}0111$ | $\mathbf{0{,}6065}$ | $+1$ |
> | 6 | $5$ | $0{,}0000$ | $0{,}0000$ | $\mathbf{0{,}6065}$ | $+1$ |
>
> Sólo hay tres valores en toda la tabla: $e^{-0{,}5} = 0{,}6065$ para el centro propio,
> $e^{-4{,}5} = 0{,}0111$ para el centro de al lado y prácticamente $0$ para el lejano.
> **Ése es el archivo con el que se entrena la capa de salida**, y las columnas $x_\ell$ ya no se usan.

![Los mismos seis patrones, antes y después de pasar por la capa radial](../imagenes/17-ejemplo-desdoblamiento.png)

> **PARA LA DEFENSA — acá se ve por qué el problema dejó de ser difícil**
> En el eje $x$ los patrones $+1$ estaban **partidos en dos grupos** con los $-1$ en el medio: ningún
> umbral servía. En el espacio $(\varphi_1, \varphi_2)$ los dos grupos de $+1$ **cayeron los dos cerca
> del origen** —porque ninguno activa a $\varphi_2$— y los $-1$ quedaron arriba, solos. Con
> $\varphi_2 = 0{,}3$ alcanza. La capa radial no clasificó nada: **cambió el sistema de coordenadas**,
> y en el sistema nuevo el problema es linealmente separable. Es la misma idea que la capa oculta del
> MLP, con otra herramienta.

### 8.2 La derivación completa

**Error de la neurona de salida $k$** — notar el orden de la resta:

$$e_k(n) = y_k(n) - d_k(n)$$

**Criterio:**

$$\xi(n) = \frac{1}{2}\sum_k e_k^2(n) = \frac{1}{2}\sum_k \left( \sum_j w_{kj}(n)\,\varphi_j(n) - d_k(n) \right)^{\!2}$$

El cuadrado está para que un error positivo en una salida no se compense con uno negativo en otra —si se cancelaran, el criterio diría cero con todas las neuronas equivocadas—, y el $\tfrac{1}{2}$ está para que se simplifique al derivar. Podría ser valor absoluto; el cuadrado se elige por la facilidad de la derivada.

**Derivada respecto de un peso.** De la sumatoria externa sobre $k$ sólo sobrevive el término de esa neurona:

$$\frac{\partial \xi(n)}{\partial w_{kj}(n)} = \left( \sum_i w_{ki}(n)\,\varphi_i(n) - d_k(n) \right) \frac{\partial}{\partial w_{kj}} \left( \sum_i w_{ki}(n)\,\varphi_i(n) - d_k(n) \right)$$

Adentro del paréntesis derecho: $d_k$ es constante y se va; de la sumatoria sobre $i$, todos los términos con $i \neq j$ son constantes respecto de $w_{kj}$ y también se van. Queda sólo $\varphi_j$. Y el paréntesis izquierdo es, por definición, $e_k$:

$$\boxed{\;\frac{\partial \xi(n)}{\partial w_{kj}(n)} = e_k(n)\,\varphi_j(n)\;}$$

**Regla de aprendizaje** — paso en contra del gradiente:

$$w_{kj}(n+1) = w_{kj}(n) - \eta\, e_k(n)\, \varphi_j(n)$$

y escrita entera, sin abreviar el error:

$$w_{kj}(n+1) = w_{kj}(n) - \eta \left( \sum_i w_{ki}(n)\,\varphi_i(n) - d_k(n) \right) \varphi_j(n)$$

### 8.3 La trampa del signo

En la unidad del perceptrón el error era $e = d - y$ y la regla sumaba. Acá el error es $e_k = y_k - d_k$ y la regla **resta**. El profesor lo menciona al pasar: *"acá hay un pequeño cambio de notación respecto a lo que habíamos encontrado"*.

> **OJO — son la misma regla, y hay que poder mostrarlo en dos renglones**
> $$-\eta\,(y_k - d_k)\,\varphi_j \;=\; +\eta\,(d_k - y_k)\,\varphi_j$$
> El signo del paso y el orden de la resta se cancelan. Lo que **no** podés hacer es mezclar: si escribís $e = d - y$ tenés que sumar, y si escribís $e = y - d$ tenés que restar. La forma de no equivocarse es no memorizar el signo sino **derivarlo**: siempre se va en contra del gradiente, y el gradiente hereda el orden de la resta que hayas elegido.

**El control de tres segundos.** Suponé una sola salida, $\varphi_j > 0$, y que la red da **de más**: $y > d$, o sea $e > 0$. La regla resta $\eta e \varphi_j$, así que $w$ **baja**, y con eso $y$ baja. Correcto. Si te da al revés, tenés un signo cambiado.

> **EN NÚMEROS — los dos primeros pasos del LMS**
> Con todos los pesos en cero, $\eta = 0{,}5$, y la entrada extra $-1$ con su peso $w_0$:
>
> **Entra $x_1 = 0$** ($\varphi = (0{,}6065;\,0;\,0)$, $d = +1$).
> $y = 0$, así que $e = y - d = -1$. Sólo se mueven los pesos cuya entrada no es nula:
> $$w_1 \leftarrow 0 - 0{,}5\,(-1)(0{,}6065) = \mathbf{0{,}3033}
> \qquad w_0 \leftarrow 0 - 0{,}5\,(-1)(-1) = \mathbf{-0{,}5}$$
> El error era negativo —la red daba **de menos**— y el peso **subió**. Correcto.
>
> **Entra $x_2 = 1$** ($\varphi = (0{,}6065;\,0{,}0111;\,0)$, $d = +1$).
> Ahora la red ya contesta algo: $\;y = 0{,}3033\,(0{,}6065) + (-0{,}5)(-1) = 0{,}6839$, y el error
> bajó a $e = -0{,}3161$. La corrección es **más chica que la anterior**, porque es proporcional al
> error.
>
> Fijate que $w_2$ y $w_3$ **no se movieron** en el primer paso: sus $\varphi_j$ valían cero. En una
> red radial, cada patrón corrige casi exclusivamente los pesos de **su propia** neurona. Eso es
> aprendizaje local, y es lo contrario del MLP, donde cada patrón toca todos los pesos.

### Claves de la sección 8

| Clave | Qué tenés que poder responder |
|---|---|
| El desdoblamiento | Congelada la capa radial, queda un perceptrón simple lineal |
| Los dos métodos | Pseudo-inversa y LMS |
| $\partial \xi / \partial w_{kj}$ | $e_k \varphi_j$, y de dónde sale cada factor |
| El signo | $e = y - d$ y la regla resta; con $e = d-y$ sumaría |

---

## 9. Las gaussianas $N$-dimensionales

Hasta acá cada gaussiana tenía un solo $\sigma_j$: era esférica. El caso general reemplaza ese escalar por una **matriz de covarianza** $\mathbf{U}_j \in \mathbb{R}^{N \times N}$:

$$\mathcal{N}(\mathbf{x}, \boldsymbol{\mu}_j, \mathbf{U}_j) = \frac{1}{(2\pi)^{N/2}\,|\mathbf{U}_j|^{1/2}} \cdot e^{-\frac{1}{2}\left[(\mathbf{x}-\boldsymbol{\mu}_j)^{\mathsf{T}} \mathbf{U}_j^{-1} (\mathbf{x}-\boldsymbol{\mu}_j)\right]}$$

**Cómo leer el exponente.** $(\mathbf{x}-\boldsymbol{\mu}_j)^{\mathsf{T}}(\ldots)(\mathbf{x}-\boldsymbol{\mu}_j)$ es la misma resta multiplicada dos veces: es la **norma al cuadrado** que teníamos antes, sólo que con la matriz metida en el medio. Y la matriz aparece **invertida**, que es lo mismo que decir que está *dividiendo*: en $\mathbb{R}^1$, $\mathbf{U}_j^{-1}$ es el escalar $1/\sigma_j^2$ y se recupera exactamente la fórmula de la sección 4. Lo de adelante es una constante y no cambia la forma.

![Los cuatro casos, del más simple al más general](../imagenes/12-casos-de-covarianza.png)

La cátedra los numera al revés, del más simple al más completo:

**Caso simplificado 3 — $\mathbf{U}_j = \mathbf{I}$.** No queda nada en el denominador:

$$\mathcal{N}'(\mathbf{x}, \boldsymbol{\mu}_j) = e^{-\frac{1}{2}\sum_{k=1}^{N}(x_k - \mu_{jk})^2}$$

Círculos perfectos, **todos del mismo tamaño**, que sólo se pueden mover. Parece pobrísimo, y sin embargo alcanza para la mayoría de los problemas: los pesos de salida le dan a cada gaussiana la importancia que corresponda. Es el modelo que la cátedra usa en la práctica.

**Caso simplificado 2 — $\mathbf{U}_j = \sigma^2\mathbf{I}$, diagonal igual.** El $\sigma$ sale afuera de la sumatoria porque es un escalar:

$$\mathcal{N}(\mathbf{x}, \boldsymbol{\mu}_j, \mathbf{U}_j) = \frac{1}{(2\pi)^{N/2}\,\sigma^{N}} \cdot e^{-\frac{1}{2\sigma^2}\sum_{k=1}^{N}(x_k - \mu_{jk})^2}$$

Círculos de **distinto tamaño**: grande donde los patrones estén desparramados, chico donde estén apretados. Es el caso de la sección 7.

**Caso simplificado 1 — $\mathbf{U}_j$ diagonal general, con $\sigma_{jk}$.** Una varianza por dimensión y por neurona:

$$\mathcal{N}(\mathbf{x}, \boldsymbol{\mu}_j, \mathbf{U}_j) = \frac{1}{(2\pi)^{N/2}\,\prod_{k=1}^{N} \sigma_{jk}} \cdot e^{-\frac{1}{2}\sum_{k=1}^{N} \frac{(x_k - \mu_{jk})^2}{\sigma_{jk}^2}}$$

Ahora hay **elipses**: si los patrones se estiran en una dirección, la gaussiana se acuesta y los abarca sin tragarse otros que no correspondían. Pero sólo horizontales o verticales — **alineadas a los ejes**, nunca rotadas.

**Caso general.** La matriz completa. En $\mathbb{R}^2$:

$$\mathbf{U}_j = \begin{pmatrix} \sigma_{j11} & \sigma_{j12} \\ \sigma_{j21} & \sigma_{j22} \end{pmatrix}$$

Los de la diagonal son las varianzas de cada dimensión —lo del caso anterior—. Los **cruzados** son las varianzas entre dimensiones: cuánta relación hay entre la dimensión 1 y la 2. Son los que permiten **rotar** la elipse, y con eso se cubren todas las formas posibles.

> **OJO — dos constantes de normalización están mal en las diapositivas**
> La 53 escribe $(2\pi)^{N/2}\sqrt{N}\,\sigma$ donde va $(2\pi)^{N/2}\sigma^{N}$, y la 54 escribe $(2\pi)^{N/2}\sqrt{\sum_k \sigma_{jk}^2}$ donde va $(2\pi)^{N/2}\prod_k \sigma_{jk}$. Las dos coinciden con la correcta **sólo en $N=1$**; ya en $N=3$ dan alrededor del 30 % del valor que deberían.
> En la red **no molesta**, porque la constante se la come el peso $w_{kj}$ de la salida —de hecho la cátedra usa la gaussiana sin normalizar—. Pero si te piden escribir la gaussiana multivariada, escribí $|\mathbf{U}_j|^{1/2}$ en el denominador y de ahí bajá a cada caso: es siempre el determinante, y para una matriz diagonal el determinante es el **producto** de la diagonal.

> **EN CRIOLLO — del aro al lazo**
> $\mathbf{U}_j = \mathbf{I}$ son **aros de hula-hula, todos iguales**: sólo podés moverlos de lugar.
> $\sigma^2\mathbf{I}$ te deja además **elegir el diámetro** de cada uno. La diagonal general te deja
> **aplastarlos** para arriba o para el costado, pero siempre derechos. Y la matriz completa te deja
> **girarlos**: los términos cruzados son la perilla de rotación. Cada caso agrega una libertad, y
> ninguna cambia la idea de fondo, que sigue siendo *encerrar una zona alrededor de un centro*.

### Claves de la sección 9

| Clave | Qué tenés que poder responder |
|---|---|
| El exponente | Norma al cuadrado con $\mathbf{U}_j^{-1}$ en el medio; en $\mathbb{R}^1$ es $1/\sigma^2$ |
| $\mathbf{U}_j = \mathbf{I}$ | Círculos iguales; alcanza porque los $w_{kj}$ compensan |
| Diagonal general | Elipses alineadas a los ejes |
| Matriz completa | Los términos cruzados son los que rotan la elipse |

---

## 10. Comparación RBF-NN contra MLP

| RBF-NN | MLP |
|---|---|
| 1 capa oculta | $p$ capas ocultas |
| distancia a prototipos gaussianos | hiperplanos sigmoideos |
| representaciones **locales** sumadas | representaciones **distribuidas** combinadas |
| convergencia más simple (linealidad) | back-propagation, con sus mínimos locales |
| entrenamiento más rápido | más lento |
| arquitectura más simple | más capas que elegir |
| combina dos paradigmas de aprendizaje | supervisado de punta a punta |

**Por qué le alcanza una capa oculta.** En el MLP la cantidad de capas decidía qué regiones se podían formar: semiplano, convexa, arbitraria. Acá no hace falta esa escalera, porque cada gaussiana se ubica donde quiera y con el tamaño que quiera; agregando neuronas se arma cualquier región, por complicada que sea.

![Con suficientes gaussianas se arma cualquier región, incluso con agujeros](../imagenes/11-region-compleja.png)

**Local contra global.** Es la diferencia de fondo entre las dos arquitecturas:

![Reconstrucción de la diapositiva 44](../imagenes/10-local-vs-global.png)

Una gaussiana abarca **una zona acotada** del espacio y fuera de ella no dice nada. Un hiperplano siempre cubre **media hiperesfera**: separa la mitad que sí de la mitad que no, en todo el espacio, hasta el infinito.

> **EN CRIOLLO — la linterna y el meridiano**
> Una gaussiana es una **linterna**: ilumina un círculo y del círculo para afuera no dice nada. Un
> hiperplano sigmoideo es un **meridiano trazado sobre el planeta**: te parte el mundo entero en dos
> mitades, y opina sobre cualquier punto por lejos que esté. Si te preguntan por un lugar del que la
> RBF no sabe nada, todas las linternas contestan "casi cero" —y eso mismo es la señal de que no
> sabe—; el MLP, en cambio, siempre te va a decir *norte* o *sur*, con total seguridad.

> **PARA LA DEFENSA — la consecuencia práctica de "local"**
> Que las representaciones sean locales quiere decir que **cada neurona es responsable de una región**, y que se puede mirar una gaussiana y decir de qué se ocupa. En el MLP la respuesta a un patrón está repartida entre todas las neuronas ocultas y ninguna es responsable de nada en particular. Por eso una RBF es más fácil de inspeccionar, y por eso también se degrada distinto: un patrón lejos de todos los centros activa **poco a todas** las neuronas, mientras que un MLP siempre contesta algo con confianza.

---

## 11. El ejemplo completo, de punta a punta

Las mismas seis filas de siempre, ahora encadenadas: de los datos crudos a la red entrenada, sin
saltear ningún paso. Cada bloque dice **qué fórmula aplica y de qué sección sale**.

### Los datos y la decisión de arquitectura

| $\ell$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| $x_\ell$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| $d_\ell$ | $+1$ | $+1$ | $-1$ | $-1$ | $+1$ | $+1$ |

**Se eligen $M = 3$ neuronas radiales**, y con eso queda elegido el $k$ de $k$-medias: son la misma
decisión (§6.1). La red es $1 \to 3 \to 1$.

**Los parámetros a entrenar** (§4) son diez: tres centros $\mu_j$, tres desviaciones $\sigma_j$, tres
pesos $w_j$ y el umbral $w_0$. Los primeros seis salen de la etapa no supervisada; los últimos cuatro,
de la supervisada.

![La red del ejemplo, con todos los valores ya puestos](../imagenes/19-ejemplo-arquitectura.png)

### Etapa 1a — Los centros por $k$-medias

> **Fórmulas: §6.2.** Centroide $\;\mu_j = \frac{1}{|C_j|}\sum_{\ell \in C_j} x_\ell\;$ y reasignación
> al centroide más cercano, hasta que nadie se mueva.

Con el reparto inicial al azar $\{0,2\}$, $\{1,3\}$, $\{4,5\}$ los centroides arrancan en $1$, $2$ y
$4{,}5$; después de la primera reasignación los grupos pasan a $\{0,1\}$, $\{2,3\}$, $\{4,5\}$ y los
centroides a $0{,}5$, $2{,}5$ y $4{,}5$; en la segunda vuelta **ningún patrón cambia de grupo** y el
algoritmo corta. El criterio bajó de $J = 4{,}5$ a $J = 1{,}5$.

$$\boldsymbol{\mu} = (0{,}5;\quad 2{,}5;\quad 4{,}5)$$

**En ningún momento se usó $d_\ell$.** Si tapás la fila de las clases, esta etapa sale igual.

### Etapa 1b — Los anchos

> **Fórmula: §7.** $\;\sigma_j^2 = \frac{1}{N|C_j|}\sum_{\ell \in C_j} \lVert x_\ell - \mu_j \rVert^2$,
> con $N = 1$.

Los tres grupos tienen la misma forma —dos patrones a $0{,}5$ del centroide—, así que las tres
desviaciones son iguales:

$$\sigma_j^2 = \frac{0{,}25 + 0{,}25}{2} = 0{,}25 \qquad\Longrightarrow\qquad \sigma_j = 0{,}5$$

![Las tres neuronas radiales ya definidas. Cada patrón cae en el pico de una y en la cola de las otras.](../imagenes/16-ejemplo-gaussianas.png)

**Acá termina la etapa no supervisada.** La capa radial queda **congelada**.

### Etapa 2a — El desdoblamiento

> **Idea: §8.1.** Con la capa radial fija, cada patrón se convierte de una vez y para siempre en su
> vector de activaciones $\boldsymbol{\varphi}(x_\ell)$, y lo que queda es un perceptrón simple lineal.

$$\varphi_j(x) = e^{-\frac{(x - \mu_j)^2}{2\,(0{,}5)^2}} = e^{-2\,(x-\mu_j)^2}$$

| $\ell$ | $x_\ell$ | $\varphi_1$ | $\varphi_2$ | $\varphi_3$ | $-1$ | $d_\ell$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | $0$ | $0{,}6065$ | $0{,}0000$ | $0{,}0000$ | $-1$ | $+1$ |
| 2 | $1$ | $0{,}6065$ | $0{,}0111$ | $0{,}0000$ | $-1$ | $+1$ |
| 3 | $2$ | $0{,}0111$ | $0{,}6065$ | $0{,}0000$ | $-1$ | $-1$ |
| 4 | $3$ | $0{,}0000$ | $0{,}6065$ | $0{,}0111$ | $-1$ | $-1$ |
| 5 | $4$ | $0{,}0000$ | $0{,}0111$ | $0{,}6065$ | $-1$ | $+1$ |
| 6 | $5$ | $0{,}0000$ | $0{,}0000$ | $0{,}6065$ | $-1$ | $+1$ |

Ésta es la tabla con la que se entrena de acá en adelante. La columna $x_\ell$ **ya no se usa**.

### Etapa 2b — Los pesos, primero a ojo

Antes de poner el LMS a girar, conviene ver que la solución **se puede escribir a mano**, y eso explica
para qué sirve cada peso. Como cada patrón activa a una sola neurona con $0{,}6065$, para que la salida
dé $\pm 1$ alcanza con:

$$w_j = \pm\frac{1}{0{,}6065} = \pm\,e^{1/2} = \pm\,1{,}6487
\qquad\text{con los signos } (+,\,-,\,+) \text{ y } w_0 = 0$$

Verificación sobre el primer patrón: $\;y(0) = 1{,}6487 \times 0{,}6065 = 1{,}0000$. Sobre el tercero:
$\;y(2) = 1{,}6487\,(0{,}0111) - 1{,}6487\,(0{,}6065) = 0{,}0183 - 1{,}0000 = -0{,}9817$. El criterio
sobre los seis patrones da $\xi = 0{,}0007$: prácticamente cero.

![Las tres campanas ya pesadas, y la suma. La del medio entra restando: ése es el trabajo del signo de $w_2$.](../imagenes/18-ejemplo-salida.png)

> **PARA LA DEFENSA — mirá el dibujo de abajo y contá lo que hace cada parámetro**
> $\mu_j$ puso **dónde** está cada campana, $\sigma_j$ **cuán ancha** es, el **signo** de $w_j$ decide
> si esa zona vota $+1$ o $-1$, y el **módulo** de $w_j$ ajusta la altura para que el pico llegue justo
> a $1$. Con esas cuatro frases explicás la red entera sin escribir una sola ecuación.

### Etapa 2c — Los pesos por LMS

> **Fórmula: §8.2.** $\;e = y - d\;$ y $\;w_j \leftarrow w_j - \eta\,e\,\varphi_j$. Con
> $\eta = 0{,}5$ y todos los pesos inicializados en cero.

**Primer patrón** ($x_1 = 0$, $d = +1$): $y = 0$, $e = -1$, y se corrigen sólo los pesos con entrada no
nula:

$$w_1 \leftarrow 0 - 0{,}5(-1)(0{,}6065) = 0{,}3033
\qquad
w_0 \leftarrow 0 - 0{,}5(-1)(-1) = -0{,}5$$

**Segundo patrón** ($x_2 = 1$, $d = +1$): ahora $y = 0{,}3033\,(0{,}6065) + (-0{,}5)(-1) = 0{,}6839$,
con lo que $e = -0{,}3161$ y las correcciones son **tres veces más chicas** que las del paso anterior.

**Tercer patrón** ($x_3 = 2$, $d = -1$): $y = 0{,}6635$, o sea $e = +1{,}6635$ — el error más grande de
la época, porque la red venía aprendiendo a contestar $+1$ y éste es el primer patrón negativo. La
corrección hace $w_2 \leftarrow -0{,}5027$: **el peso del medio se vuelve negativo**, que es
exactamente el signo de la solución a ojo.

Y así con los seis, época tras época:

| Época | $\xi$ sobre los seis patrones | $w_1$ | $w_2$ | $w_3$ | $w_0$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $0$ (arranque) | $3{,}0000$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $1{,}3434$ | $0{,}390$ | $-0{,}653$ | $0{,}571$ | $-0{,}512$ |
| $2$ | $0{,}5799$ | $0{,}485$ | $-1{,}163$ | $0{,}899$ | $-0{,}375$ |
| $3$ | $0{,}2651$ | $0{,}616$ | $-1{,}520$ | $1{,}079$ | $-0{,}304$ |
| $5$ | $0{,}0634$ | $0{,}860$ | $-1{,}924$ | $1{,}209$ | $-0{,}262$ |
| $10$ | $0{,}0018$ | $1{,}135$ | $-2{,}165$ | $1{,}188$ | $-0{,}287$ |

### El control

Después de diez épocas la red contesta $(0{,}98;\;0{,}95;\;-1{,}01;\;-1{,}01;\;0{,}98;\;1{,}01)$
contra las deseadas $(+1;\,+1;\,-1;\,-1;\,+1;\,+1)$: los seis patrones bien, con el signo correcto y
el módulo casi en $1$.

> **OJO — el LMS no llega a los mismos pesos que la solución a ojo, y está bien**
> A ojo salía $(+1{,}65;\,-1{,}65;\,+1{,}65)$ con $w_0 = 0$; el LMS terminó cerca de
> $(+1{,}14;\,-2{,}17;\,+1{,}19)$ con $w_0 = -0{,}29$. **Las dos soluciones sirven**: con cuatro
> parámetros y seis ecuaciones que se pueden satisfacer casi exactamente, hay muchas combinaciones que
> dan bien, y el gradiente encuentra la que está más cerca del punto de partida. Lo que se compara no
> son los pesos: es el error.

> **IDEA DE FONDO — dónde estuvo la dificultad, en todo el ejemplo**
> En ningún lado. $k$-medias fueron dos iteraciones de promediar y comparar; $\sigma$ fue una raíz
> cuadrada; los pesos, un LMS de perceptrón simple. **La red nunca tuvo que retropropagar nada**,
> porque las dos etapas se resolvieron por separado, y ésa es la ventaja de la que habla la sección 10.

### Claves de la sección 11

| Clave | Qué tenés que poder responder |
|---|---|
| Contar parámetros | $3$ centros $+$ $3$ anchos $+$ $3$ pesos $+$ $1$ umbral $= 10$ |
| Qué fórmula en cada etapa | §6 los centros, §7 los anchos, §8 los pesos |
| La tabla de $\varphi$ | Construirla a partir de $\mu$ y $\sigma$, y saber que reemplaza a los $x$ |
| La solución a ojo | $w_j = \pm 1/\varphi_{\text{pico}}$, y qué significa cada signo |
| Por qué el LMS da otros pesos | Hay muchas soluciones buenas; lo que se compara es $\xi$ |

---

## 12. Para la pizarra

### Guion: qué dibujar primero

| Si te preguntan… | Arrancá dibujando |
|---|---|
| Cualquier cosa, si te dejan elegir | Los seis patrones de la sección 11: el guion D0 los usa para todo |
| ¿Por qué funciones radiales? | El XOR con los cuatro puntos, y encima el papel doblado contra el círculo |
| La arquitectura | Las tres columnas: 2 entradas, 4 gaussianas, un $\Sigma$. Después los pesos 1 y el $-1$ |
| El modelo | Las **dos** fórmulas de la sección 4, una debajo de la otra |
| ¿Qué se entrena? | Una lista de tres: $\boldsymbol{\mu}_j$, $\sigma_j$, $w_{kj}$ — y aclarar cuál en cada etapa |
| $k$-medias | Una nube de puntos con dos centroides y las distancias dibujadas |
| El entrenamiento de la salida | La red desdoblada: la capa radial tachada y las $\varphi_j$ como entradas nuevas |
| RBF vs MLP | Un círculo al lado de una recta que cruza toda la hoja |
| Gaussianas $N$-dim | Cuatro cuadraditos: círculos iguales, círculos distintos, elipses, elipses rotadas |

### D0 — Explicar toda la unidad en cinco minutos, con el ejemplo

Éste es el guion que conviene tener automatizado: **seis números en el pizarrón y la unidad entera
sale sola**. Cada paso es una línea de dibujo y una frase.

| # | Qué escribís o dibujás | Qué decís mientras lo hacés |
|:---:|---|---|
| 1 | La recta con $0\,1\,2\,3\,4\,5$; círculos llenos en $0,1,4,5$ y vacíos en $2,3$ | *"seis patrones, los buenos en los bordes y los malos en el medio"* |
| 2 | Una raya vertical en cualquier lado, y una cruz encima | *"un perceptrón pone un umbral, y con un umbral esto no se resuelve"* |
| 3 | Tres campanas sobre $0{,}5$, $2{,}5$ y $4{,}5$ | *"en vez de cortar, tiro tres aros: uno por grupo"* |
| 4 | $\mu_j = \frac{1}{|C_j|}\sum x_\ell$ al costado | *"los centros no los elijo yo: los da $k$-medias, sin mirar las clases"* |
| 5 | $\sigma_j = 0{,}5$ debajo de cada campana | *"el ancho sale de la dispersión del propio grupo"* |
| 6 | La tabla $6 \times 3$ de $\varphi$, aunque sea con dos filas | *"cada patrón deja de ser un número y pasa a ser un boletín de tres notas"* |
| 7 | Los signos $+\;-\;+$ arriba de las campanas | *"y ahora una suma pesada alcanza: la del medio entra restando"* |
| 8 | $w_{kj}(n{+}1) = w_{kj}(n) - \eta\,e_k\varphi_j$ | *"y esos pesos salen por LMS, que es el perceptrón simple de siempre"* |

**El cierre hablado:** *"la capa radial cambió el sistema de coordenadas sin supervisión, y en el
sistema nuevo el problema quedó lineal"*. Si llegás a decir esa frase, ya diste la unidad.

### D1 — La regla de $k$-medias online

**Te preguntan:** deducí cómo se mueve el centroide en la versión online.

**Arrancás escribiendo:** $J_\ell = \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2$

1. Pasalo a producto: $(\mathbf{x}_\ell - \boldsymbol{\mu}_j)^{\mathsf{T}}(\mathbf{x}_\ell - \boldsymbol{\mu}_j)$.
2. Derivá respecto de $\boldsymbol{\mu}_j$; la derivada interna es $-1$.
   **Llegás a:** $\nabla_{\boldsymbol{\mu}_j} J_\ell = -2(\mathbf{x}_\ell - \boldsymbol{\mu}_j)$
3. Paso en contra del gradiente: $\boldsymbol{\mu}_j - \eta' \nabla$.
   **Llegás a:** $\boldsymbol{\mu}_j + 2\eta'(\mathbf{x}_\ell - \boldsymbol{\mu}_j)$
4. Absorbé el 2 en la constante.
   **Llegás a:** $\boldsymbol{\mu}_j(n+1) = \boldsymbol{\mu}_j(n) + \eta(\mathbf{x}_\ell - \boldsymbol{\mu}_j(n))$

**Trampa:** el signo. El gradiente da $-2(\ldots)$ y el descenso pone otro menos: los dos menos dan el **más** de la regla final. Si te queda un menos, perdiste uno de los dos.

**Cierre hablado:** *"el centroide da un paso hacia el patrón, de una fracción $\eta$ del camino"*.

### D2 — La regla LMS de la capa de salida

**Te preguntan:** deducí la actualización de los pesos de la capa de salida.

**Arrancás escribiendo:** $e_k = y_k - d_k$ y $\xi = \tfrac{1}{2}\sum_k e_k^2$

1. Reemplazá $y_k$ por su expresión: $\xi = \tfrac{1}{2}\sum_k \left(\sum_j w_{kj}\varphi_j - d_k\right)^2$.
2. Derivá respecto de $w_{kj}$. El cuadrado baja un 2 que se come al $\tfrac{1}{2}$.
   **Llegás a:** $\left(\sum_i w_{ki}\varphi_i - d_k\right) \cdot \dfrac{\partial}{\partial w_{kj}}\left(\sum_i w_{ki}\varphi_i - d_k\right)$
3. Argumentá qué sobrevive: $d_k$ es constante; de la suma sobre $i$ sólo queda $i=j$.
   **Llegás a:** $\partial \xi / \partial w_{kj} = e_k\,\varphi_j$
4. Paso en contra del gradiente.
   **Llegás a:** $w_{kj}(n+1) = w_{kj}(n) - \eta\,e_k(n)\,\varphi_j(n)$

**Trampa:** el orden de la resta. Con $e = y - d$ la regla **resta**. Decilo en voz alta cuando lo escribas, para que se vea que no es un error.

**Cierre hablado:** *"es el LMS del perceptrón simple con salida lineal; la única diferencia es que la entrada ahora es $\varphi_j$ en vez de $x_i$"*.

### D3 — Por qué el promedio es el centroide

**Te preguntan:** ¿por qué en el paso 2 de $k$-medias se promedia?

1. Escribí $J$ con los conjuntos fijos y derivá respecto de $\boldsymbol{\mu}_j$.
   **Llegás a:** $-2\sum_{\ell \in C_j}(\mathbf{x}_\ell - \boldsymbol{\mu}_j) = \mathbf{0}$
2. Repartí la suma: $\sum_\ell \mathbf{x}_\ell - |C_j|\,\boldsymbol{\mu}_j = \mathbf{0}$.
   **Llegás a:** $\boldsymbol{\mu}_j = \dfrac{1}{|C_j|}\sum_{\ell \in C_j} \mathbf{x}_\ell$

**Cierre hablado:** *"no es una heurística: con los conjuntos fijos, el promedio es el mínimo exacto"*.

### D4 — Resolver el ejemplo de seis patrones

**Te preguntan:** dados $x = 0,1,2,3,4,5$ con $d = +1,+1,-1,-1,+1,+1$, armá una RBF que los clasifique.

1. **Elegí $M$.** Tres grupos de dos $\Rightarrow$ $M = 3$ neuronas radiales, y ése es también el $k$.
2. **Corré $k$-medias.** Reparto al azar, promediar, reasignar, repetir.
   **Llegás a:** $\mu = (0{,}5;\,2{,}5;\,4{,}5)$
3. **Calculá los anchos** con la dispersión de cada grupo.
   **Llegás a:** $\sigma_j^2 = \frac{0{,}25+0{,}25}{2} = 0{,}25$, o sea $\sigma_j = 0{,}5$
4. **Escribí la tabla de $\varphi$.** Alcanza con dos filas: sólo hay tres valores distintos.
   **Llegás a:** $0{,}6065$ en el centro propio, $0{,}0111$ en el vecino, $0$ en el lejano
5. **Poné los pesos.** Cada patrón activa una sola neurona, así que $w_j = \pm 1/0{,}6065$.
   **Llegás a:** $w = (+1{,}6487;\,-1{,}6487;\,+1{,}6487)$, $w_0 = 0$
6. **Verificá un patrón.** $y(0) = 1{,}6487 \times 0{,}6065 = 1{,}0000$ ✓

**Trampa:** olvidarse de que $k$-medias **no mira** las clases. Si te preguntan por qué los grupos
coincidieron con las clases, la respuesta es que en este problema los patrones de la misma clase están
geométricamente juntos, no que el algoritmo lo supiera.

**Cierre hablado:** *"con $\sigma$ chico las gaussianas casi no se pisan, así que el problema se
vuelve trivial: cada neurona vota por su zona y el peso decide con qué signo"*.

---

## 13. Formulario

| Qué | Fórmula |
|---|---|
| Salida de la red | $y_k(\mathbf{x}_\ell) = \sum_{j=1}^{M} w_{kj}\varphi_j(\mathbf{x}_\ell)$ |
| Función radial | $\varphi_j(\mathbf{x}_\ell) = e^{-\lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 / 2\sigma_j^2}$ |
| Criterio de $k$-medias | $J = \sum_j \sum_{\ell \in C_j} \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2$ |
| Centroide (lotes) | $\boldsymbol{\mu}_j = \frac{1}{|C_j|}\sum_{\ell \in C_j} \mathbf{x}_\ell$ |
| Reasignación | $\ell \in C_j \iff \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 < \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_i \rVert^2\ \forall i \neq j$ |
| Ganador (online) | $j^* = \arg\min_j \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j(n) \rVert$ |
| Adaptación (online) | $\boldsymbol{\mu}_{j^*}(n+1) = \boldsymbol{\mu}_{j^*}(n) + \eta(\mathbf{x}_\ell - \boldsymbol{\mu}_{j^*}(n))$ |
| Error de salida | $e_k(n) = y_k(n) - d_k(n)$ |
| Criterio supervisado | $\xi(n) = \frac{1}{2}\sum_k e_k^2(n)$ |
| Gradiente | $\partial \xi / \partial w_{kj} = e_k(n)\varphi_j(n)$ |
| Regla de aprendizaje | $w_{kj}(n+1) = w_{kj}(n) - \eta\,e_k(n)\varphi_j(n)$ |
| Gaussiana general | $\mathcal{N} = \frac{1}{(2\pi)^{N/2}|\mathbf{U}_j|^{1/2}} e^{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_j)^{\mathsf{T}}\mathbf{U}_j^{-1}(\mathbf{x}-\boldsymbol{\mu}_j)}$ |

## Errores típicos

| Error | Cómo se detecta |
|---|---|
| Sumar en la regla de los pesos | Con $e = y-d$ la regla **resta**. Chequeo: si $y > d$, $w$ tiene que bajar |
| Restar en la regla de $k$-medias | Los dos menos (gradiente y descenso) dan **más**: el centroide va **hacia** el patrón |
| Poner sesgo en la capa radial | No tiene. El $-1$ está en la entrada de la **capa de salida** |
| Poner sigmoide en la salida | Es **lineal**: viene de aproximación de funciones |
| Confundir la $k$ de $k$-medias con la $k$ de $y_k$ | Una es la cantidad de neuronas **radiales**, la otra indexa las de **salida** |
| Decir que $k$-medias usa la salida deseada | Es **no supervisado**: $d$ no aparece en toda la etapa 1 |
| Escribir $\sqrt{\sum \sigma^2}$ en la gaussiana | Va el **determinante**: para diagonal, el **producto** de la diagonal |

## Autoevaluación

1. Dibujá una sigmoide en 3D y explicá por qué no puede encerrar una región.
2. ¿Por qué la capa radial no tiene sesgo y la de salida no tiene no linealidad?
3. Escribí las dos fórmulas del modelo y nombrá los cuatro índices.
4. ¿Qué parámetros se entrenan en cada etapa, y cuál usa la salida deseada?
5. Deducí la regla de $k$-medias online desde $\nabla J$.
6. ¿Por qué el paso 2 de $k$-medias por lotes es un promedio?
7. Explicá el desdoblamiento: por qué la etapa 2 es un perceptrón simple.
8. Deducí $\partial \xi / \partial w_{kj}$ justificando qué términos se anulan.
9. ¿Por qué la regla de esta unidad resta y la del perceptrón sumaba?
10. ¿Por qué a una RBF le alcanza una capa oculta y a un MLP no?
11. ¿Qué quiere decir que las representaciones sean locales?
12. Dibujá los cuatro casos de $\mathbf{U}_j$ y decí qué gana cada uno.
13. ¿Cómo se estima $\sigma_j$, y por qué se puede ser poco exigente con ese valor?

**Sobre el ejemplo de los seis patrones** —éstas se contestan con lápiz, sin mirar el apunte:

14. Escribí los seis patrones y explicá en una frase por qué un perceptrón simple no los resuelve.
15. Partiendo del reparto $\{0,2\}$, $\{1,3\}$, $\{4,5\}$, hacé las dos iteraciones de $k$-medias.
16. Calculá $\sigma_1$ a partir del grupo $\{0,1\}$ y su centroide.
17. Calculá $\varphi_2(x_5)$ a mano. ¿Por qué da casi cero?
18. Armá la tabla $6\times3$ de activaciones y marcá el valor máximo de cada fila.
19. Dibujá los seis patrones en el plano $(\varphi_1, \varphi_2)$ y trazá una recta que los separe.
20. Sin usar el LMS, elegí los tres pesos a ojo y justificá el signo de cada uno.
21. Hacé el primer paso del LMS partiendo de todos los pesos en cero, con $\eta = 0{,}5$.
22. Contá los parámetros de la red del ejemplo y decí cuáles salen de cada etapa.
23. ¿Qué pasaría con la tabla de $\varphi$ si $\sigma$ fuese $2$ en vez de $0{,}5$?

---

## Cierre: el recorrido completo de la unidad

Cada pieza contesta la pregunta que dejó abierta la anterior:

| La pregunta | La respuesta | Dónde |
|---|---|:---:|
| ¿Por qué no alcanza con sigmoides? | Un hiperplano parte el espacio en dos mitades infinitas; para encerrar una zona hay que combinar varias | §1 |
| ¿Y con qué se las reemplaza? | Con funciones que ya vienen cerradas: gaussianas alrededor de un centro | §1–2 |
| ¿Cómo queda la red, entonces? | Tres columnas: entrada con pesos fijos, capa radial sin sesgo, salida lineal | §3 |
| ¿Cuáles son los parámetros? | Los centros $\boldsymbol{\mu}_j$, los anchos $\sigma_j$ y los pesos $w_{kj}$ | §4 |
| ¿Cómo se entrenan? | En **dos etapas**: la radial sin supervisión, la de salida con supervisión | §5 |
| ¿Dónde se ponen los centros? | Donde se amontonan los patrones: $k$-medias, que nunca ve las clases | §6 |
| ¿Y los anchos? | Con la dispersión de cada grupo respecto de su propio centroide | §7 |
| ¿Y los pesos, sin retropropagar? | Congelada la capa radial queda un perceptrón simple lineal: LMS o pseudo-inversa | §8 |
| ¿Y si las gaussianas tienen que ser elipses? | Se reemplaza el escalar $\sigma_j$ por una matriz de covarianza $\mathbf{U}_j$ | §9 |
| ¿Por qué le alcanza una capa oculta? | Porque cada gaussiana es local: con suficientes se arma cualquier región | §10 |

> **PARA LA DEFENSA — la unidad en una frase**
> *Una red de base radial cambia el hiperplano sigmoideo por una campana centrada en un prototipo, y con
> eso parte el entrenamiento en dos: primero se buscan los prototipos sin supervisión —$k$-medias sobre
> los patrones—, y después, con la capa radial congelada, lo que queda es un perceptrón simple lineal
> que se entrena por LMS. La capa radial no clasifica: cambia el sistema de coordenadas para que el
> problema se vuelva lineal.*
