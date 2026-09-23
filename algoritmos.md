---
title: "Todos los algoritmos de la materia"
subtitle: "Inteligencia Computacional · FICH-UNL · cada ecuación en orden, y debajo qué dice en palabras"
lang: es
---

*Los resúmenes de cada unidad explican **por qué** funciona cada pieza, con las derivaciones y los ejemplos numéricos. Este archivo es sólo el **qué**: los algoritmos, uno atrás del otro, en el orden en que se ejecutan. Cada ecuación con un párrafo debajo que dice qué significa. Sirve para repasar de corrido y para desarrollar en la pizarra.*

| # | Algoritmo | Supervisado | Entrenamiento |
|---|---|---|---|
| 1 | Perceptrón simple — corrección de error | sí | iterativo |
| 2 | Perceptrón simple — gradiente (LMS) | sí | iterativo |
| 3 | Perceptrón multicapa — back-propagation | sí | iterativo |
| 4 | Base radial | mixto | dos fases |
| 5 | Hopfield | no | **directo** |
| 6 | BPTT | sí | iterativo |
| 7 | SOM | no | iterativo |
| 8 | LVQ1 | sí | iterativo |
| 9 | Capacidad de generalización y evaluación | — | *procedimiento* |

**Cómo está armada cada sección.** Arriba, el recuadro violeta **«contame sobre…»**: la respuesta de un minuto para cuando te piden que desarrolles el tema, en el orden *qué es → cómo está armado → cómo aprende → qué lo distingue → su límite*. Después la idea de fondo, las ecuaciones en orden, y al final la respuesta de treinta segundos con las repreguntas.

**Convenciones que cambian entre algoritmos** — las que más se mezclan en la pizarra:

- **Umbral:** entra como un peso más, $w_0$, con entrada fija $x_0 = -1$.
- **Signo del error:** perceptrón y multicapa usan $e = d - y$ y la regla **suma**; RBF (fase 2) y BPTT usan $e = y - d$ y la regla **resta**. Es la misma cuenta escrita al revés.
- **Paso:** $\eta$ en la corrección de error, $\mu$ en LMS y back-propagation (la equivalencia entre ellos se indica en cada sección), $\alpha$ en LVQ.
- **Derivada de la sigmoide simétrica** siempre en función de la salida: $\varphi'(v) = \tfrac12(1+y)(1-y)$.

---

# 1. Perceptrón simple — corrección de error

> **SI TE DICEN — «contame sobre el perceptrón simple»**
> «Es el modelo más simple de neurona artificial. Hace el producto interno entre sus pesos y la entrada —con el umbral metido como un peso más, con entrada fija $-1$— y le aplica la función signo: la salida es $\pm1$, así que clasifica en dos clases. Geométricamente traza un **hiperplano** y dice de qué lado cayó cada punto. Se entrena con supervisión, patrón por patrón: si acierta no se toca nada; si se equivoca, a los pesos se les suma $\tfrac{\eta}{2}$ por el error por la entrada, y eso **gira el hiperplano** hacia el lado correcto. Se repite hasta una pasada completa sin errores. Y el límite es la clave: eso está garantizado **sólo si el problema es linealmente separable**; con el XOR no converge nunca, y eso es lo que motiva el multicapa.»


> **IDEA DE FONDO — en qué consiste**
> Una sola neurona que traza una **recta** (un hiperplano) y dice de qué lado cayó cada punto. Tiene dos partes que se repiten patrón por patrón: **calcular la salida** y, **sólo si se equivocó, mover la recta**. La imagen para recordarlo: la recta está mal puesta, entra un punto que quedó del lado equivocado, y la recta **gira un poco hacia ese punto**. Si el punto ya estaba bien, no pasa nada. Repetido muchas veces, la recta se acomoda hasta no equivocarse con ninguno — y eso está garantizado **sólo si los datos se pueden separar con una recta**.


## Datos de partida

$$\{(\mathbf{x}(n),\ d(n))\}, \qquad x_0 = -1$$

Pares entrada–salida deseada. La componente $x_0=-1$ es fija y existe para que el umbral entre como un peso más, $w_0 = u$, y no haya que tratarlo aparte.

## Salida

$$y = \varphi\big(\langle \mathbf{w}, \mathbf{x}\rangle\big)$$

Se hace el producto interno entre los pesos y la entrada, y se le aplica la función de activación. Todo el perceptrón es eso.

$$\langle \mathbf{w}, \mathbf{x}\rangle = 0$$

Los puntos donde el producto interno da cero son la **frontera de decisión**: un hiperplano que parte el espacio de entrada en dos semiplanos.

## Adaptación

$$\mathbf{w}(n+1) = \mathbf{w}(n) + \frac{\eta}{2}\,\big[d(n)-y(n)\big]\,\mathbf{x}(n)$$

Si la salida coincide con la deseada, el corchete es cero y los pesos no se tocan. Si no coincide, los pesos se mueven en la dirección de la entrada, con el signo del error: la frontera gira hacia el lado que corrige ese patrón.

![El producto interno decide el lado; la corrección inclina $\mathbf{w}$ hacia el patrón y la recta, que es perpendicular, gira con él.](imagenes/algoritmos/01-frontera-y-giro.png){width=100%}

## Parada

$$d(n) = y(n) \quad \forall n$$

Se termina cuando una pasada completa por el conjunto no produce ninguna corrección. Está garantizado que eso pasa **sólo si el problema es linealmente separable**.

![Con XOR no existe recta: la frontera oscila para siempre. Con dos rectas —una capa oculta— sí se separa.](imagenes/algoritmos/02-xor.png){width=78%}

### Cómo se lee la regla

$e(n)$ es un **escalar** y $\mathbf{x}(n)$ un **vector**, así que la corrección $\tfrac{\eta}{2}e(n)\mathbf{x}(n)$ es un vector **en la dirección del patrón de entrada**, con magnitud proporcional al error y signo según si la salida se quedó corta o larga. Cada paso empuja a $\mathbf{w}$ a lo largo de $\mathbf{x}$, y como $\mathbf{w}$ es la normal de la frontera, la recta **gira** hacia el lado que corrige ese patrón.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Una neurona que traza un hiperplano y dice de qué lado cayó cada punto. Se le muestra un patrón: si acierta no se toca nada, y si se equivoca los pesos se mueven en la dirección del patrón, con el signo del error. Eso gira la frontera hacia el lado correcto. Se repite hasta una pasada completa sin correcciones, y eso está garantizado sólo si los datos son linealmente separables.»*
> **La repregunta segura:** ¿y si no son separables? No converge: queda oscilando. Ése es el límite que motiva el multicapa, y el ejemplo es el XOR.

---

\newpage

# 2. Perceptrón simple — regla del gradiente (LMS)

> **SI TE DICEN — «contame sobre LMS»**
> «Es la misma neurona con otra lógica de entrenamiento. En vez de corregir sólo cuando se equivoca, defino una función que **mide el error** —el error cuadrático— y muevo los pesos **en contra de su gradiente**, que es la dirección de máximo descenso. Para poder derivar uso la neurona **lineal**, sin el signo, porque el signo no es derivable. La cuenta da la regla de Widrow-Hoff: $\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\,e\,\mathbf{x}$, **velocidad por error por entrada**. El punto delicado es $\mu$: grande, oscila y se queda con el último patrón; chico, converge pero muy lento. Lo importante es que fija **el esquema de todo lo supervisado que viene después**: multicapa, radial y BPTT también bajan por el gradiente, sólo que con un gradiente más difícil de calcular.»


> **IDEA DE FONDO — en qué consiste**
> La misma neurona, pero con otra filosofía: en vez de reaccionar sólo cuando se equivoca, **define un número que mide lo mal que está** y se mueve siempre en la dirección que más lo baja. Tres partes: **definir el criterio de error**, **derivarlo** respecto de los pesos, y **moverse en contra de esa derivada**. La imagen: una pelota bajando por una ladera, donde la altura es el error y la posición son los pesos. Es el molde de todos los algoritmos supervisados que vienen después — multicapa, radial y BPTT son este mismo esquema con un gradiente más difícil de calcular.


*Mismo modelo de neurona; cambia de dónde sale el ajuste. Acá no se corrige el error, se minimiza una función.*

## Criterio

$$e^2(n) = \big[d(n) - \langle \mathbf{w}(n), \mathbf{x}(n)\rangle\big]^2, \qquad e(n) = d(n) - y(n)$$

Se define una medida de lo mal que está la red para el patrón actual: el error al cuadrado. Se trabaja en el **caso lineal** —$y = \langle \mathbf{w},\mathbf{x}\rangle$, sin activación— porque $\operatorname{sgn}$ no es derivable. Y el criterio va **sin** el $\tfrac12$: por eso el resultado lleva un $2\mu$.

## Regla del gradiente

$$\Delta \mathbf{w}(n) = -\mu\,\nabla_{\mathbf{w}}\,e^2(n)$$

Los pesos se mueven en la dirección **opuesta** al gradiente, que es la de máximo crecimiento del error: se baja por la superficie de error. $\mu$ dice qué tan grande es el paso.

![El gradiente apunta cuesta arriba; por eso el menos. Y el tamaño del paso decide si baja o rebota.](imagenes/algoritmos/03-gradiente.png){width=100%}

## LMS (Widrow-Hoff)

$$\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\,e(n)\,\mathbf{x}(n)$$

Resolviendo el gradiente para este criterio queda esto: paso, por error, por entrada. Es la misma forma que la corrección de error, y de hecho coinciden con $\eta = 4\mu$.

### Cómo se lee la regla

La estructura **velocidad de aprendizaje $\times$ error $\times$ entrada** es la misma de la sección anterior, pero el origen es distinto: no sale de reaccionar ante un error, sale de **derivar una función y moverse en contra del gradiente**. Y ésa es la forma que se va a repetir en el multicapa, en la fase 2 de las radiales y en BPTT — lo único que cambia en cada uno es **cuán difícil es calcular ese gradiente**.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Misma neurona, otra filosofía: en vez de corregir cuando se equivoca, defino un número que mide lo mal que está —el error cuadrático— y me muevo siempre en la dirección que más lo baja, que es la opuesta al gradiente. La cuenta se hace en el caso lineal, sin activación, porque el signo no es derivable. El resultado es paso por error por entrada, y coincide con la corrección de error salvo una constante.»*
> **Las dos repreguntas seguras:** por qué el menos (el gradiente apunta cuesta **arriba**, al máximo crecimiento del error) y qué pasa con $\mu$ (grande: oscila y **la red se aprende el último patrón y se olvida los anteriores**; chico: converge pero lentísimo).

> Acá aparece por primera vez la estructura que se repite en todo lo que sigue: **velocidad de aprendizaje, por error, por entrada**.

---

\newpage

# 3. Perceptrón multicapa — back-propagation

> **SI TE DICEN — «contame sobre el perceptrón multicapa»**
> «Agrega **capas ocultas** con activación sigmoidea —la simétrica, entre $-1$ y $1$—. Combinando semiplanos puede formar regiones arbitrarias, así que ya no depende de que el problema sea lineal: resuelve el XOR. Se entrena con **retropropagación**, que es descenso por gradiente del error cuadrático, en tres pasos por patrón: **hacia adelante** capa por capa, **error** en la salida, y **deltas hacia atrás**. El problema central es que **las ocultas no tienen salida deseada**. Se resuelve con el **delta**, el gradiente de error local: en la salida es error por derivada de la activación; en una oculta se arma con los deltas de la capa siguiente, pesados por las conexiones que las unen. Así todos los pesos se ajustan con la misma regla: $\mu$ **por delta por entrada**. Los riesgos: mínimos locales, saturación (derivada casi cero) y sobreajuste, que se controla con un conjunto de monitoreo.»


> **IDEA DE FONDO — en qué consiste**
> Varias capas de neuronas, cada una alimentando a la siguiente. Por cada patrón se hacen **tres cosas en este orden**: **ir hacia adelante** calculando las salidas de capa en capa, **medir el error** en la última, y **volver hacia atrás repartiendo la culpa**. El problema que resuelve, y es todo el tema: una neurona oculta **no tiene salida deseada**, así que no se sabe cuánto se equivocó. La solución: su error se arma **juntando los errores de todas las neuronas que ella alimenta**, cada uno pesado por la conexión que las une. Eso es lo que significa «retropropagar»: el error viaja hacia atrás por los mismos cables que la señal viajó hacia adelante.


## Arquitectura

$$\mathbf{v}^{(p)} = \mathbf{W}^{(p)}\,\mathbf{y}^{(p-1)} \qquad y^{(p)}_j = \varphi\big(v^{(p)}_j\big)$$

Cada capa toma la salida de la anterior, la multiplica por su matriz de pesos y le aplica la activación. $\mathbf{W}^{(p)}$ es de $M_p \times (M_{p-1}+1)$: la columna extra es la del sesgo.

$$\varphi(v) = \frac{2}{1+e^{-bv}} - 1$$

La sigmoide **simétrica**, que va de $-1$ a $+1$. Se usa ésta y no la logística porque las salidas centradas en cero hacen que el aprendizaje sea más parejo.

![La derivada se apaga en los extremos: neurona saturada, $\delta\approx0$, parálisis.](imagenes/algoritmos/05-sigmoide.png){width=95%}

## Error

$$e_j(n) = d_j(n) - y_j(n) \qquad \xi(n) = \frac{1}{2}\sum_{j=1}^{M} e_j^2(n)$$

El error de cada neurona de salida, y el error instantáneo de la red como la suma de todos al cuadrado.

## Regla del gradiente

$$\Delta w_{ji}(n) = -\mu\,\frac{\partial \xi(n)}{\partial w_{ji}(n)}$$

Lo mismo que en el perceptrón, pero ahora el peso puede estar en cualquier capa y no hay salida deseada para las ocultas. Eso es lo que hay que resolver.

$$\frac{\partial \xi}{\partial w_{ji}} = \frac{\partial \xi}{\partial e_j}\,\frac{\partial e_j}{\partial y_j}\,\frac{\partial y_j}{\partial v_j}\,\frac{\partial v_j}{\partial w_{ji}}$$

La cadena a derivar. Los dos primeros factores dan el error, el tercero es la derivada de la activación y el cuarto es la entrada que llega por esa conexión.

![El corte del $\delta$: agrupa los tres factores de adentro de la neurona y deja afuera el único que depende de la conexión.](imagenes/algoritmos/06-cadena-delta.png){width=100%}

## La derivada de la activación

$$\varphi'(v_j) = \tfrac{1}{2}\big(1+y_j\big)\big(1-y_j\big)$$

Se escribe en función de la **salida**, no del campo local: como $y_j$ ya está calculado del paso hacia adelante, la derivada sale gratis. El $\tfrac12$ va (con $b$ general sería $b/2$).

## Los deltas

$$\delta_j(n) = -\frac{\partial \xi}{\partial y_j}\,\varphi'(v_j)$$

Se le pone nombre a todo lo que pasa **dentro** de la neurona, para separarlo de lo que pasa en la conexión.

$$\delta_j = -\frac{\partial \xi}{\partial y_j}\,\frac{\partial y_j}{\partial v_j} = -\frac{\partial \xi}{\partial v_j}$$

Los dos factores de la definición son la regla de la cadena de **una sola** derivada: la del error respecto del **campo local**. Así se lee el $\delta$ en una línea: **cuánta culpa tiene esa neurona en el error total** — cuánto bajaría el error si su estímulo neto cambiara un poquito, y en qué sentido conviene moverlo.

Su nombre completo es **gradiente de error local instantáneo**, y cada palabra está justificada: **gradiente** porque es una derivada, **local** porque es de esa neurona en particular, **instantáneo** porque está evaluado en la iteración $n$.

Y el corte no es arbitrario: de los cuatro factores de la cadena, el $\delta$ agrupa **los tres que dependen de la neurona** y deja afuera **el que depende de la conexión** ($y_i$). Por eso se calcula **una sola vez por neurona** y se reutiliza para todos los pesos que entran a ella — y por eso es **lo único que una capa necesita de la capa siguiente**, que es lo que hace posible propagar hacia atrás.

> **PARA LA DEFENSA — por qué la definición no se escribe con $e_j$, y el signo**
> Porque **una neurona oculta no tiene $e_j$**: no hay salida deseada para ella. Lo que sí existe siempre es $\partial\xi/\partial y_j$, que vale $-e_j$ en la capa de salida y $-\sum_k \delta_k w_{kj}$ en una oculta. La definición genérica es la única que sirve para los dos casos; definirla como $e_j\varphi'$ te deja sin forma de bajar a las ocultas.
> **El menos** de la definición es el que hace que la actualización quede **sumando**: se come el $-\mu$ de la regla del gradiente. En clase el $\delta$ aparece primero sin el menos y enseguida con él; la versión que se usa es **con** el menos.
> **La respuesta de treinta segundos:** *«El delta es el gradiente de error local instantáneo: menos la derivada del error respecto del campo local de esa neurona. Agrupa todo lo que pasa adentro de la neurona y deja afuera lo de la conexión, y por eso el ajuste queda delta por entrada. En la capa de salida sale del error verdadero; en una oculta, de los deltas de la capa siguiente pesados por los pesos que las unen.»*

$$\delta^{III}_j = \tfrac{1}{2}\,e_j\big(1+y^{III}_j\big)\big(1-y^{III}_j\big)$$

En la capa de salida hay salida deseada, así que el delta es directo: error por derivada de la activación.

$$\delta^{II}_j = \left[\sum_k \delta^{III}_k\,w^{III}_{kj}\right]\tfrac{1}{2}\big(1+y^{II}_j\big)\big(1-y^{II}_j\big)$$

En una capa oculta no hay salida deseada, así que el error se trae de atrás: se juntan los deltas de la capa siguiente, cada uno pesado por la conexión que lo une con esta neurona. **El corchete reemplaza al error**, y el resto de la fórmula es idéntico.

![Arriba el error se mide; abajo se pide prestado a las neuronas de adelante, pesado por los pesos que las unen.](imagenes/algoritmos/07-dos-deltas.png){width=95%}

## Actualización

$$\Delta w_{ji}(n) = \mu\,\delta_j(n)\,y_i(n) \qquad w_{ji}(n+1) = w_{ji}(n) + \Delta w_{ji}(n)$$

La regla vale para cualquier capa: paso, por delta de la neurona a la que llega la conexión, por la señal que entra por ella. Lo único que cambia entre capas es cómo se calculó el delta.

$$\Delta w^{(p)}_{j0} = \mu\,\delta^{(p)}_j\,(-1)$$

El peso de sesgo se ajusta igual, con la entrada fija $-1$.

## La generalización: una capa $p$ cualquiera

$$\Delta w^{(p)}_{ji}(n) = \eta\;\big\langle \boldsymbol{\delta}^{(p+1)},\ \mathbf{w}^{(p+1)}_j \big\rangle\;\big(1+y^{(p)}_j\big)\big(1-y^{(p)}_j\big)\;y^{(p-1)}_i(n)$$

Una sola fórmula para **todas** las capas, tenga la red tres o veinte. Los tres índices: $p$ es la capa donde estoy parado, $p-1$ de dónde viene la entrada, $p+1$ la capa siguiente. Leída en voz alta: **velocidad de aprendizaje, por error, por derivada de la activación en la capa actual, por entrada**. Y acá $\eta = \mu/2$, porque absorbe el $\tfrac12$ de la derivada.

$$\big\langle \boldsymbol{\delta}^{(p+1)},\ \mathbf{w}^{(p+1)}_j \big\rangle = \sum_k \delta^{(p+1)}_k\,w^{(p+1)}_{kj}$$

El producto interno desplegado. $k$ recorre las neuronas de la **capa siguiente** y $j$ queda fijo, así que $\mathbf{w}^{(p+1)}_j$ es **la columna $j$** de esa matriz: los pesos que **salen** de la neurona $j$, no los que entran. Hacia adelante se suma sobre el segundo índice de $w_{kj}$; hacia atrás, sobre el primero. Es la misma matriz transpuesta, y de ahí el nombre del método.

![Ida: fila. Vuelta: columna. Cambiar una por otra es el error más común del tema.](imagenes/algoritmos/04-fila-columna.png){width=95%}

## Los dos bordes

La fórmula general es idéntica en todas las capas y sólo falla en los extremos, porque ahí **falta un vecino**.

$$\Delta w^{(III)}_{ji} = \eta\;\underbrace{\big(d_j - y^{(III)}_j\big)}_{e_j}\;\big(1+y^{(III)}_j\big)\big(1-y^{(III)}_j\big)\;y^{(II)}_i$$

**Capa de salida:** no existe $p+1$, así que el producto interno se reemplaza por el **error verdadero**. Todo lo demás queda igual.

$$\Delta w^{(I)}_{ji} = \eta\;\big\langle \boldsymbol{\delta}^{(II)},\ \mathbf{w}^{(II)}_j \big\rangle\;\big(1+y^{(I)}_j\big)\big(1-y^{(I)}_j\big)\;x_i$$

**Primera capa:** no existe $p-1$, así que la «salida de la capa anterior» es la **entrada de la red**.

$$\delta^{(III)}_j \;\longrightarrow\; \delta^{(II)}_j \;\longrightarrow\; \delta^{(I)}_j$$

Y el orden no es negociable: los $\delta$ se calculan **de la salida hacia atrás**, porque cada capa necesita los de la siguiente. El de la capa de salida es el único que se puede calcular sin depender de nadie.

![La fórmula general sólo falla donde falta un vecino.](imagenes/algoritmos/08-bordes.png){width=95%}

## El corchete, desglosado un nivel

$$\big\langle \boldsymbol{\delta}^{(III)},\ \mathbf{w}^{(III)}_j \big\rangle = \tfrac{1}{2}\sum_k \big(d_k - y^{(III)}_k\big)\big(1+y^{(III)}_k\big)\big(1-y^{(III)}_k\big)\,w^{(III)}_{kj}$$

Reemplazando $\delta^{(III)}_k$ por su fórmula y sacando el $\tfrac12$ afuera de la suma, el corchete queda escrito **sólo con cosas ya calculadas**: las salidas deseadas, las salidas de la red y los pesos.

> **OJO — dos derivadas de activación distintas, y el $\tfrac12$**
> La derivada de adentro del corchete va evaluada en **$k$** (capa siguiente); la de afuera, en **$j$** (capa actual). Escribirlas con el mismo índice es el error más común del tema. Y de los dos $\tfrac12$: el de adentro es el del $\delta^{(p+1)}$ y se escribe; el de la capa actual está absorbido en $\eta$.
>
> **Y hasta acá no más.** Con más capas, cada $\delta^{(p+1)}$ tiene adentro otro corchete, y desplegar eso son cuatro renglones ilegibles. La gracia del $\delta$ es justamente **no** desplegarlo: se calcula una vez por neurona y en cada capa se lo trata como un número que ya está.

---

\newpage

# 4. Redes de base radial

> **SI TE DICEN — «contame sobre las redes de base radial»**
> «Es una red de dos capas donde las neuronas ocultas son **gaussianas** en vez de sigmoideas: cada una tiene un centro, responde fuerte si la entrada está cerca y casi nada si está lejos. Son **detectores locales**, burbujas, en vez de semiplanos. La salida es una **combinación lineal** de esas respuestas. El entrenamiento es **mixto, en dos fases**. Primero, **sin mirar etiquetas**, se ubican los centros con $k$-medias: cada dato va al centro más cercano y cada centro se muda al promedio de sus datos, hasta que nadie cambie. Después, **con las etiquetas**, se entrenan los pesos de salida con LMS, usando las gaussianas como entradas. La ventaja: esa segunda fase es un **problema lineal**, más simple que retropropagar. Como variante, después se pueden ajustar también centros y anchos por gradiente.»


> **IDEA DE FONDO — en qué consiste**
> Cambiar de representación para que el problema se vuelva fácil. Tiene **dos fases con criterios distintos**: primero, **sin mirar las etiquetas**, se ubican unas cuantas «burbujas» gaussianas donde hay datos; después, **mirando las etiquetas**, se decide cuánto pesa cada burbuja en la salida. La imagen: cada neurona oculta es un detector local que se enciende cuando la entrada cae cerca de su centro y se apaga si está lejos — al revés de la sigmoide, que responde a todo un semiespacio. Y la clave del método: una vez fijadas las burbujas, **la salida es una combinación lineal**, así que la segunda mitad es un problema lineal, sin capas ocultas que derivar.


*Dos fases con criterios distintos: la primera no supervisada ubica las funciones, la segunda supervisada las combina.*

## Arquitectura

$$\varphi_j(\mathbf{x}_\ell) = e^{-\lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 / 2\sigma_j^2}$$

Cada neurona oculta responde según **qué tan cerca** está la entrada de su centro $\boldsymbol{\mu}_j$: máximo si coincide, y cae con la distancia a una velocidad que fija $\sigma_j$. Es una activación local, al revés que la sigmoide, que responde a todo un semiespacio.

![La forma de la activación es toda la diferencia entre los dos métodos: semiespacios contra burbujas.](imagenes/algoritmos/09-local-vs-global.png){width=88%}

$$y_k(\mathbf{x}_\ell) = \sum_{j=1}^{M} w_{kj}\,\varphi_j(\mathbf{x}_\ell)$$

La salida es una **combinación lineal** de esas respuestas. Y ahí está la clave del método: fijadas las funciones radiales, la salida es lineal en los pesos, así que la segunda fase es un problema fácil.

![Cambiar un $w_{kj}$ sube o baja una campana; la forma y la posición no se tocan.](imagenes/algoritmos/11-combinacion.png){width=90%}

## Fase 1 — centros, no supervisada ($k$-medias)

$$J = \sum_j \sum_{\ell \in C_j} \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2$$

El criterio: que cada dato esté lo más cerca posible del centro de su grupo. Se minimiza alternando dos pasos.

$$\ell \in C_j \iff \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j \rVert^2 < \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_i \rVert^2 \quad \forall\, i \neq j$$

**Reasignación:** cada dato se asigna al centro más cercano.

$$\boldsymbol{\mu}_j = \frac{1}{|C_j|}\sum_{\ell \in C_j} \mathbf{x}_\ell$$

**Recálculo:** cada centro se muda al promedio de los datos que le tocaron. Se repite hasta que nadie cambia de grupo.

![Los patrones nunca se mueven: en el primer paso cambian de etiqueta, en el segundo salta el centro.](imagenes/algoritmos/10-kmedias.png){width=100%}

$$j^* = \arg\min_j \lVert \mathbf{x}_\ell - \boldsymbol{\mu}_j(n) \rVert \qquad \boldsymbol{\mu}_{j^*}(n+1) = \boldsymbol{\mu}_{j^*}(n) + \eta\big(\mathbf{x}_\ell - \boldsymbol{\mu}_{j^*}(n)\big)$$

La versión **en línea**, patrón por patrón: gana el centro más cercano y se corre un poco hacia el dato. Es la misma idea que el SOM pero sin vecindad.

## Fase 2 — pesos, supervisada

$$e_k(n) = y_k(n) - d_k(n) \qquad \xi(n) = \frac{1}{2}\sum_k e_k^2(n)$$

Recién acá aparecen las salidas deseadas. **Ojo con el signo:** acá el error se define al revés que en el perceptrón, $e = y - d$, y por eso la regla lleva $-\eta$. Es la misma cuenta que $+\eta\,(d-y)$.

$$\frac{\partial \xi}{\partial w_{kj}} = e_k(n)\,\varphi_j(n)$$

El gradiente es sencillo porque la salida es lineal en los pesos: no hay ninguna derivada de activación que arrastrar.

$$w_{kj}(n+1) = w_{kj}(n) - \eta\,e_k(n)\,\varphi_j(n)$$

Error por activación de la neurona oculta. Es LMS otra vez, con las $\varphi_j$ haciendo de entradas.

### Cómo se lee

$\varphi_j(\mathbf{x})$ se lee como **cuánto se parece la entrada al centro $j$**: vale 1 si cae justo encima y cae con la distancia a una velocidad que fija $\sigma_j$. Es un **detector local**, al revés de la sigmoide, que responde a todo un semiespacio. Y $w_{kj}$ se lee como **cuánto pesa esa burbuja en la salida $k$**.

Por eso la frontera de una RBF son **burbujas** y la de un multicapa son **semiespacios cortados**: la diferencia entre los dos métodos está en la forma de la activación, no en el algoritmo.

![Si las burbujas tienen que ser elipses, el escalar $\sigma_j$ se reemplaza por una matriz: los términos cruzados son los que la rotan.](imagenes/algoritmos/12-covarianza.png){width=95%}

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Se cambia de representación para que el problema se vuelva fácil. Primero, sin mirar las etiquetas, se ubican unas gaussianas donde hay datos —eso es $k$-medias—. Después, con las etiquetas, se decide cuánto pesa cada una en la salida. Y la clave: fijadas las gaussianas, la salida es una combinación lineal de ellas, así que la segunda fase es un problema lineal, sin capas ocultas que derivar.»*
> **Las repreguntas seguras:** por qué el entrenamiento es **mixto** (fase 1 no supervisada, fase 2 supervisada); qué pasa si las gaussianas tienen que ser elipses (se reemplaza el escalar $\sigma_j$ por una matriz de covarianza); y el **método 2**, que arranca con el método 1 y después ajusta todo —centros y anchos incluidos— por gradiente.

---

\newpage

# 5. Hopfield

> **SI TE DICEN — «contame sobre la red de Hopfield»**
> «Es una **memoria asociativa**: guarda patrones de $\pm1$, y si le das uno incompleto o con ruido te devuelve el guardado más parecido. Es **una sola capa**, todas las neuronas conectadas con todas, con **pesos simétricos y sin autoconexiones**. Tiene dos fases. **Almacenar no itera**: los pesos salen de una cuenta con la **regla de Hebb**, el promedio de $x_j x_i$ sobre los patrones, que mide cuánto coinciden esas dos neuronas. **Recuperar sí itera**: cargo el patrón sucio como estado inicial, sorteo una neurona, le pongo el signo de su campo local, y repito hasta $N$ pasos seguidos sin cambios. **Siempre converge**, porque con pesos simétricos hay una **energía que nunca sube**. Sus límites: capacidad baja, del orden de $N/(2\ln N)$ patrones, y **estados espurios**, como el negativo de cada patrón.»


> **IDEA DE FONDO — en qué consiste**
> Una memoria que se consulta **por contenido**: le das un dato roto y te devuelve el dato entero. Tiene **dos fases**: **almacenar**, que es una sola cuenta y no itera, y **recuperar**, que itera hasta quedarse quieta. La idea de fondo: el recuerdo **no se guarda en ningún lugar**, se guarda como **acuerdos entre las partes del recuerdo** — para cada par de neuronas, si suelen coincidir o suelen oponerse. Por eso están **todas conectadas con todas**, en una sola capa. Y recuperar es **una votación ponderada que se repite**: se sortea una neurona, las demás le dicen qué valor debería tener, **el peso del cable es cuánto vale cada voto**, gana la mayoría, y se repite hasta que nadie cambia.


## Datos de partida

$$\mathbf{x}^*_k \in \{-1,+1\}^N, \qquad k = 1,\dots,P$$

$P$ patrones para guardar, cada uno un vector de $N$ componentes que valen $-1$ o $+1$. Esos $N$ lugares son las $N$ neuronas.

## Fase 1 — Almacenamiento

$$w_{ji} = \frac{1}{N}\sum_{k=1}^{P} x^*_{kj}\,x^*_{ki} \qquad \forall\, i \neq j$$

Para cada par de neuronas se recorren los patrones multiplicando el valor que tiene una por el valor que tiene la otra. Como son $\pm1$, cada producto da $+1$ si coinciden y $-1$ si se oponen: el peso mide **en cuántos patrones coincidieron menos en cuántos difirieron**.

$$w_{jj} = 0 \qquad \forall\, j$$

Ninguna neurona se conecta consigo misma. Se impone: la fórmula daría $P/N$ y esa neurona se haría caso a sí misma por encima de todas las demás.

$$w_{ji} = w_{ij}$$

La conexión entre dos neuronas es una sola. Con la regla de arriba se cumple solo, porque el producto no distingue el orden.

![Escribir la memoria es una cuenta; leerla es dejar correr la red. Los dos carriles no se mezclan.](imagenes/algoritmos/13-hopfield-fases.png){width=100%}

## Fase 2 — Recuperación

$$\mathbf{y}(0) = \mathbf{x}$$

El patrón incompleto o con ruido se escribe directamente como estado inicial de las neuronas.

$$j^* = \operatorname{rnd}(N)$$

Se sortea cuál neurona se actualiza en este paso.

$$v_{j^*}(n) = \sum_{i=1}^{N} w_{j^*i}\,y_i(n-1)$$

El campo local: el valor actual de cada una de las demás, multiplicado por el peso que la une con la elegida, todo sumado. Es una votación ponderada, donde el peso es cuánto vale cada voto.

$$y_{j^*}(n) = \operatorname{sgn}\big(v_{j^*}(n)\big), \qquad \operatorname{sgn}(x) = \begin{cases} +1 & x > 0 \\ y_{j^*}(n-1) & x = 0 \\ -1 & x < 0 \end{cases}$$

El nuevo valor es el signo de ese total: gana la mayoría. En el empate la neurona conserva lo que tenía.

$$y_j(n) = y_j(n-1) \qquad \forall\, j \neq j^*$$

Las demás quedan como estaban: se toca **una sola** por paso.

$$\mathbf{y}(n) = \cdots = \mathbf{y}(n-N) \;\Longrightarrow\; \text{fin}$$

Se corta tras $N$ actualizaciones seguidas sin cambios. Recién ahí nada puede moverse después, porque a cada neurona le entraría lo mismo que ya le entró.

## Convergencia

$$E(\mathbf{y}) = -\frac{1}{2}\sum_{j}\sum_{i} w_{ji}\,y_i\,y_j$$

Cada par de neuronas aporta un término que baja la energía cuando el par está como su peso "quiere". El $\tfrac12$ compensa que la doble suma cuenta cada par dos veces.

$$\Delta E = -\big(y_{j^*}(n) - y_{j^*}(n-1)\big)\,v_{j^*}(n)$$

Al actualizar una sola neurona, los únicos términos que se mueven son los que la contienen. **Esto vale porque los pesos son simétricos:** si no, el par $(i,j)$ aportaría dos términos distintos.

$$\Delta E = 2\,y_{j^*}(n-1)\,v_{j^*}(n) < 0 \quad\text{si cambió} \qquad \Delta E = 0 \quad\text{si no cambió}$$

Si la neurona se dio vuelta fue porque su valor viejo no coincidía con el signo del campo: tienen signos distintos, el producto es negativo y la energía bajó.

$$\boxed{\;\Delta E \le 0\;} \;\wedge\; 2^N < \infty \;\Longrightarrow\; \text{converge en pasos finitos}$$

La energía nunca sube, está acotada por abajo y hay finitos estados: no puede bajar para siempre.

$$E(-\mathbf{y}) = E(\mathbf{y}) \qquad P_{\max} = \frac{N}{2\ln N}$$

Dar vuelta todas las neuronas no cambia la energía: por cada memoria guardada queda su negativo como estado espúreo.

La capacidad, en cambio, crece más lento que $N$, mientras la cantidad de pesos crece como $N^2$: guardar muchos patrones sale caro.

![La red rueda cuesta abajo hasta el mínimo más cercano: por eso recupera la memoria más parecida, y por eso también puede caer en uno espurio.](imagenes/algoritmos/14-energia.png){width=92%}

### Cómo se leen las tres piezas

**$w_{ji}$** — *coincidencias menos diferencias*: en cuántos patrones esas dos neuronas tuvieron el mismo valor, menos en cuántos difirieron. Es **el acuerdo** entre dos posiciones del dato.

**$v_j$** — *una votación ponderada*: cada neurona opina sobre cuánto debería valer $j$, y **el peso del cable es cuánto vale cada voto**. Positivo dice «tenemos que coincidir», negativo «tenemos que oponernos», cero «no opino».

**$E$** — *cuánta incomodidad hay en la red*: cuántos pares están en contra de lo que su peso quiere. Cada par contento la baja, cada par a disgusto la sube.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Es una memoria asociativa: se consulta por contenido y no por dirección. El recuerdo no se guarda en ningún lugar, se guarda como acuerdos entre las partes del recuerdo, y por eso están todas las neuronas conectadas con todas. Almacenar es una sola cuenta —Hebb—, y recuperar es una votación ponderada que se repite hasta que nadie cambia. Y siempre termina, porque hay una energía que nunca sube.»*
> **Las repreguntas seguras:** por qué es **hebbiano** (el peso crece cuando dos neuronas se activan juntas, no hay salida deseada en ningún momento, y el ajuste depende sólo de la correlación entre las dos actividades); por qué la diagonal es cero; qué pasa si los pesos no son simétricos (puede oscilar, y se cae la demostración); y qué es un estado espúreo.

---

\newpage

# 6. BPTT

> **SI TE DICEN — «contame sobre BPTT»**
> «Es cómo se entrena una **red recurrente**, donde la salida de un instante vuelve a entrar en el siguiente. La idea es **desenrollarla en el tiempo**: $T$ instantes son $T$ copias en fila, o sea una red profunda, y le aplico retropropagación. Primero recorro toda la secuencia **hacia adelante guardando** campos locales y salidas; después calculo los errores y **vuelvo hacia atrás en el tiempo** propagando los deltas con la **transpuesta** de la matriz de recurrencia. Dos diferencias con el multicapa: como **las copias comparten los mismos pesos**, los aportes de todos los instantes **se suman** sobre el mismo peso; y los pesos se actualizan **recién al final de la secuencia**. Como la memoria crece con $T$, se puede **truncar** la vuelta a pocos instantes, a costa de perder dependencias largas. Elman y Jordan son el caso truncado a un solo paso.»


> **IDEA DE FONDO — en qué consiste**
> Entrenar una red recurrente con back-propagation, **desenrollando el tiempo**: si la red se realimenta durante $T$ instantes, se la dibuja como $T$ copias en fila y se la trata como una red profunda. Tres partes: **ida** por toda la secuencia guardando todo, **medir los errores**, y **vuelta en el tiempo** acumulando gradientes. Las dos diferencias con el multicapa, que son de donde salen todas las preguntas: **el tiempo hace de profundidad**, y **las copias comparten los mismos pesos** — por eso los aportes de todos los instantes **se suman** sobre el mismo peso en vez de ajustar cada capa por separado.


## Datos de partida

$$\{(\mathbf{x}_t,\ \mathbf{d}_t)\}_{t=0}^{T-1}$$

Una secuencia, con salida deseada en los instantes que la tengan. No todos necesitan tenerla.

## Inicialización

$$\mathbf{W}^{I},\ \mathbf{W} \sim \text{al azar, chicos} \qquad \mathbf{y}_{-1} = \mathbf{0} \qquad \Delta\mathbf{W} = \Delta\mathbf{W}^{I} = \mathbf{0}$$

Pesos chicos para que las neuronas no arranquen saturadas con $\varphi'\approx0$. Estado previo nulo y acumuladores en cero.

## Paso hacia adelante

$$\mathbf{v}_t = \mathbf{W}^{I}\mathbf{x}_t + \mathbf{W}\,\mathbf{y}_{t-1} \qquad \mathbf{y}_t = \varphi(\mathbf{v}_t)$$

Lo que entra tiene dos partes: la entrada de ese instante y la salida de la propia red en el anterior. Ésa es toda la recurrencia, y la **misma** $\mathbf{W}$ se usa en todos los instantes.

$$\text{guardar } \mathbf{v}_t,\ \mathbf{y}_t \quad \forall\, t$$

La vuelta va a necesitar $\varphi'(\mathbf{v}_t)$ de cada instante. Es la diferencia práctica más grande con el multicapa, y la razón de que la memoria crezca con $T$.

## Error

$$\mathbf{e}_t = \mathbf{y}_t - \mathbf{d}_t \qquad E = \frac{1}{2}\sum_{t}\sum_{k} e_{t,k}^2$$

El error de la secuencia es la suma de los errores de todos los instantes. Los que no tienen salida deseada aportan cero. Igual que en la RBF, $e = y - d$: por eso la actualización del final **resta**.

## Gradiente — forma derivada

$$\delta_{t,j} = e_{t,j}\,\varphi'(v_{t,j})$$

En el instante donde se midió el error, el delta es directo: igual que la capa de salida del multicapa.

$$\delta_{\tau,j} = \left(\sum_k w_{kj}\,\delta_{\tau+1,k}\right)\varphi'(v_{\tau,j}) \qquad \tau < t$$

Hacia atrás en el tiempo, el delta se arrastra: los deltas del instante siguiente, pesados por las conexiones, por la derivada de la activación de esta neurona en este instante. **El tiempo hace de profundidad.** Ojo con el índice: hacia adelante $v_{\tau+1,k}$ recibe $w_{kj}\,y_{\tau,j}$, así que hacia atrás se suma sobre $k$ con $w_{kj}$ — es la columna $j$, lo mismo que $\mathbf{W}^{\mathsf{T}}$ en la forma optimizada.

![Desenrollada, la recurrencia es una red profunda con una copia por instante y la misma $\mathbf{W}$ repetida.](imagenes/algoritmos/15-bptt.png){width=100%}

$$\frac{\partial E_t}{\partial w_{ji}} = \sum_{\tau=0}^{t} \delta_{\tau,j}\,y_{\tau-1,i} \qquad \frac{\partial E_t}{\partial w^{I}_{ji}} = \sum_{\tau=0}^{t} \delta_{\tau,j}\,x_{\tau,i}$$

El error de un instante se reparte sobre **todos** los anteriores, porque el mismo peso participó en todos, y los aportes se **suman**. Para los pesos de entrada los deltas son los mismos: cambia sólo el último factor.

## Gradiente — forma optimizada

$$\boldsymbol{\delta}^*_T = \mathbf{0} \qquad \boldsymbol{\delta}^*_t = \big[\mathbf{e}_t + \mathbf{W}^{\mathsf{T}}\boldsymbol{\delta}^*_{t+1}\big] \odot \varphi'(\mathbf{v}_t)$$

El delta acumulado junta el error medido en ese instante con todo lo arrastrado de los posteriores, ya sumado. Se recorre de $T-1$ a $0$, al revés que la propagación. La **transpuesta** es lo que distingue la ida de la vuelta.

$$\Delta\mathbf{W} \mathrel{+}= \boldsymbol{\delta}^*_t\,\mathbf{y}_{t-1}^{\mathsf{T}} \qquad \Delta\mathbf{W}^{I} \mathrel{+}= \boldsymbol{\delta}^*_t\,\mathbf{x}_t^{\mathsf{T}}$$

En el mismo barrido se acumulan los dos gradientes. Da **exactamente el mismo** gradiente que la forma derivada, reorganizado, pero en **un solo barrido**: el costo baja de $O(T^2)$ a $O(T)$.

## Actualización

$$\mathbf{W} \leftarrow \mathbf{W} - \eta\,\Delta\mathbf{W} \qquad \mathbf{W}^{I} \leftarrow \mathbf{W}^{I} - \eta\,\Delta\mathbf{W}^{I}$$

Los pesos se tocan **al final de la secuencia**. Si se actualizaran en el medio del barrido, los deltas que faltan usarían una $\mathbf{W}$ distinta de la que se usó hacia adelante.

## Truncado

$$\tau \ge \max(0,\ t-P) \qquad\qquad O(T^2) \longrightarrow O(T\,P)$$

Truncar limita la vuelta a $P$ instantes: el costo pasa a $O(T\,P)$, pero se pierden las dependencias más largas que $P$. Las dos cosas abaratan el cálculo, con una diferencia que se pregunta: **truncar cambia el gradiente (es una aproximación); optimizar con $\delta^*$ no (da el mismo, exacto).**

## Arquitecturas con retardo

$$\tilde{\mathbf{x}}_t = \big(\mathbf{x}_t,\ \mathbf{x}_{t-1},\ \dots,\ \mathbf{x}_{t-D}\big)$$

**TDNN:** la entrada se amplía con sus retardos y la red vuelve a ser hacia adelante. Toda la memoria está en la entrada, no en la red.

$$\mathbf{y}_t = \varphi\big(\mathbf{W}^{I}\mathbf{x}_t + \mathbf{W}^{C}\mathbf{c}_t\big), \qquad \mathbf{c}_t = \mathbf{y}^{\text{oculta}}_{t-1} \;\;(\text{Elman}) \qquad \mathbf{c}_t = \mathbf{y}^{\text{salida}}_{t-1}\;\;(\text{Jordan})$$

La capa de contexto guarda la salida anterior —de la oculta en Elman, de la salida en Jordan— y se trata como una entrada más con valores congelados. Con eso se entrena con back-propagation común: es BPTT truncada a un solo paso.

### Cómo se lee

**$\delta_{\tau,j}$** es el mismo delta del multicapa, con «capa siguiente» reemplazado por «**instante** siguiente»: el tiempo hace de profundidad. **$\delta^*_t$** es el delta **acumulado**: ya trae sumados los errores de todos los instantes posteriores, y por eso alcanza un solo barrido.

Y la suma sobre $\tau$ se lee así: **el error de un instante se reparte sobre todos los instantes anteriores, porque el mismo peso participó en todos**. Los aportes **se suman** — no se promedian.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Es back-propagation con el tiempo haciendo de profundidad. Si la red se realimenta durante $T$ instantes, la dibujo como $T$ copias en fila y la trato como una red profunda. Con dos diferencias: las copias comparten los mismos pesos, así que los aportes de todos los instantes se suman sobre el mismo peso; y hay que guardar toda la secuencia hacia adelante, porque la vuelta necesita la derivada de la activación de cada instante.»*
> **Las repreguntas seguras:** los aportes se **suman**, no se promedian; hacia adelante va $\mathbf{W}$ y hacia atrás $\mathbf{W}^{\mathsf{T}}$; los pesos se actualizan **al final** de la secuencia, nunca en el medio del barrido; y **truncar no es lo mismo que optimizar** — truncar cambia el gradiente, el $\delta^*$ da exactamente el mismo.

---

\newpage

# 7. SOM

> **SI TE DICEN — «contame sobre el SOM»**
> «El mapa de Kohonen es una red **no supervisada** que acomoda prototipos sobre los datos **y además los deja ordenados**. Cada neurona tiene un vector de pesos **en el mismo espacio que las entradas** y un lugar en una **grilla**, normalmente 2D. Por cada patrón, dos pasos: **competencia** —gana la neurona más cercana al dato— y **adaptación** —la ganadora **y sus vecinas de la grilla** se acercan al dato una fracción $\eta$—. Esa vecindad es lo que lo separa de $k$-medias: produce el **ordenamiento topológico**, neuronas vecinas en el mapa representan zonas vecinas de los datos. Se entrena en **tres etapas**: ordenamiento (vecindad grande, $\eta$ alta), transición, y ajuste fino (vecindad cero, $\eta$ chica). Se corta por épocas, porque no hay error que medir. Sirve para agrupar y visualizar datos de alta dimensión y, etiquetando las neuronas al final, para clasificar.»


> **IDEA DE FONDO — en qué consiste**
> Acomodar unos pocos prototipos para que representen a muchos datos, **y además queden ordenados entre sí**. Dos partes por cada patrón: **competir** (gana el prototipo más cercano) y **adaptar** (el ganador se corre un poco hacia el dato). La imagen clave: los pesos de cada neurona **viven en el mismo espacio que los datos**, así que son un punto que se va mudando hacia donde hay datos. Y lo que lo hace un *mapa* y no una simple cuantización: **cuando el ganador se mueve, arrastra a sus vecinos de la grilla**. Por eso neuronas contiguas terminan representando zonas contiguas del espacio de entrada.


## Datos de partida

$$\{\mathbf{x}(n)\} \subset \mathbb{R}^M, \qquad \text{sin etiquetas}$$

Sólo vectores de entrada. El entrenamiento es **no supervisado**: la red se organiza a partir de cómo están distribuidos los datos.

## Arquitectura

$$\mathbf{w}_j \in \mathbb{R}^M, \qquad j = 1,\dots,N$$

Los pesos de cada neurona viven **en el mismo espacio que las entradas**: son un punto del espacio de datos, no coeficientes. Por eso tiene sentido la distancia entre una entrada y una neurona.

Las neuronas están además en una grilla, que no tiene nada que ver con $\mathbb{R}^M$: define **quién es vecino de quién**, y es lo único que la topología aporta.

![Los dos espacios del método. La vecindad se mide arriba; la competencia, abajo. Confundirlos es el error clásico del tema.](imagenes/algoritmos/16-som-dos-espacios.png){width=95%}

## Inicialización

$$\mathbf{w}_j(0) \sim \text{al azar, chicos y distintos entre sí}$$

Distintos obligatoriamente: dos neuronas que arrancan en el mismo punto ganan y se mueven siempre juntas, y nunca se separan.

## Competencia

$$j^*(n) = G(\mathbf{x}(n)) = \arg\min_{\forall j}\big\{\lVert \mathbf{x}(n) - \mathbf{w}_j(n)\rVert\big\}$$

Se presenta una entrada y gana la neurona más cercana en el espacio de datos, midiendo con distancia euclídea.

## Vecindad

$$h_{G,i} = \beta(n)\,e^{-\frac{|G-i|^2}{2\sigma^2(n)}}$$

La influencia sobre cada neurona decae con su distancia **en la grilla** a la ganadora: la de al lado se mueve casi tanto como ella, una lejana casi nada. Con entorno uniforme, en cambio, es $\beta(n)$ adentro del radio y cero afuera.

![La influencia se mide sobre los índices de la grilla, no sobre los datos.](imagenes/algoritmos/17-vecindad.png){width=95%}

## Adaptación

$$\mathbf{w}_j(n+1) = \begin{cases} \mathbf{w}_j(n) + \eta(n)\big(\mathbf{x}(n) - \mathbf{w}_j(n)\big) & y_j \in \Lambda_G(n) \\[2pt] \mathbf{w}_j(n) & y_j \notin \Lambda_G(n) \end{cases}$$

La ganadora y sus vecinas se mueven hacia la entrada: el paréntesis es el vector que va de la neurona al dato, y $\eta$ dice qué fracción de ese camino se recorre. Las de afuera del entorno no se tocan. Ésta es la versión con **entorno uniforme**, la que se implementa.

$$\mathbf{w}_j(n+1) = \mathbf{w}_j(n) + h_{G,j}(n)\,\big(\mathbf{x}(n) - \mathbf{w}_j(n)\big) \qquad \forall\, j$$

Con **vecindad gaussiana**, cada neurona recibe $h_{G,j}(n)$ en lugar de $\eta(n)$: la ganadora se mueve con el pico $\beta(n)$ y las demás cada vez menos según su distancia en la grilla. No hay corte en seco, y achicar $\sigma(n)$ es la forma continua de reducir el entorno.

Que se muevan **las vecinas de la grilla** es lo único que separa un SOM de una cuantización vectorial cualquiera: es lo que hace que neuronas contiguas terminen representando zonas contiguas del espacio de entrada.

## Decaimiento — las tres etapas

$$\eta(n) \downarrow, \qquad \Lambda_G(n) \downarrow$$

| Etapa | $\Lambda_G$ | $\eta$ | Épocas |
|---|---|---|---|
| Ordenamiento | $\approx$ medio mapa | 0,9 – 0,7 | 500 – 1000 |
| Transición | $\to 1$, lineal | $\to 0{,}1$ | $\approx$ 1000 |
| Ajuste fino | $0$ | 0,1 – 0,01, cte. | $\approx$ 3000 |

Primero se ordena el mapa a lo grande con entorno amplio y pasos largos; después se afina con entorno nulo y pasos cortos. No hay error que mirar: se corta por cantidad de épocas.

![Las dos cantidades se apagan juntas: primero ordenar, después afinar.](imagenes/algoritmos/18-etapas.png){width=90%}

### Cómo se lee la adaptación

$\mathbf{x} - \mathbf{w}_j$ **no es un error contra una salida deseada**: es el vector que va de la neurona al dato, dos puntos del mismo espacio. Y $\eta$ es **qué fracción de ese trecho se recorre**. Por eso el entrenamiento es no supervisado aunque la fórmula se parezca a la del gradiente.

Y hay **dos distancias distintas** en el algoritmo, que es lo que más se confunde: la de la competencia se mide **en el espacio de los datos**; la de la vecindad, **en la grilla**. Una neurona puede tener su peso lejísimos del patrón y actualizarse igual, sólo porque en el mapa está al lado de la ganadora. **Eso es exactamente lo que produce el ordenamiento topológico.**

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Acomoda unos pocos prototipos para que representen a muchos datos, y además queden ordenados entre sí. Por cada patrón: gana el prototipo más cercano y se corre un poco hacia el dato. Lo que lo hace un mapa y no una simple cuantización es que el ganador arrastra a sus vecinos de la grilla, y por eso neuronas contiguas terminan representando zonas contiguas del espacio de entrada.»*
> **Las repreguntas seguras:** por qué $k$-medias **no** tiene ordenamiento topológico (no hay vecindad: se mueve sólo el ganador); para qué sirve la etapa de ordenamiento y qué parámetros son clave ($\Lambda_G$ grande y $\eta$ alta); y por qué los pesos iniciales tienen que ser **distintos entre sí**.

---

\newpage

# 8. LVQ1

> **SI TE DICEN — «contame sobre LVQ»**
> «Es la **versión supervisada** de la idea del SOM. Hay prototipos en el espacio de datos, **cada uno con una clase asignada**. Por cada patrón gana el más cercano y comparo su clase con la del dato: **si coincide, el prototipo se acerca; si no, se aleja**. Se mueve **sólo el ganador**, sin vecindad, porque no busco un mapa ordenado sino **ubicar bien la frontera entre clases**. Un dato nuevo toma la clase del prototipo más cercano. La variante **LVQ1-O** le da a cada prototipo **su propia tasa de aprendizaje**, que baja cuando acierta y sube cuando se equivoca, para que todos los patrones pesen parecido y el resultado no dependa del orden en que se presentaron.»


> **IDEA DE FONDO — en qué consiste**
> Lo mismo que el SOM pero **con etiquetas y con castigo**. Tres partes: **competir**, **ver si el ganador era de la clase correcta**, y **premiar o castigar**. Si acertó, el prototipo se acerca al dato; si se equivocó, **se aleja**. Eso es todo lo que cambia, y cambia el objetivo: al SOM le importa cubrir bien el espacio, a LVQ le importa **dónde queda la frontera entre clases**. Por eso acá no hay vecindad: se mueve sólo el ganador.


## Datos de partida

$$\{(\mathbf{x}(n),\ d(n))\}, \qquad \mathcal{C}(i) \text{ asignada a cada prototipo}$$

Acá **sí** hay etiquetas: LVQ es supervisado. Y cada prototipo tiene su clase asignada de antemano.

## Ganador

$$c(n) = \arg\min_i\big\{\lVert \mathbf{x}(n) - \mathbf{m}_i(n)\rVert\big\}$$

Igual que en el SOM: gana el prototipo más cercano.

## Signo

$$s(c,d,n) = \begin{cases} +1 & \mathcal{C}(c(n)) = d(n) \\ -1 & \mathcal{C}(c(n)) \neq d(n) \end{cases}$$

Acá está toda la diferencia con el SOM: se compara la clase del prototipo que ganó con la clase verdadera del dato.

## Adaptación

$$\mathbf{m}_c(n+1) = \mathbf{m}_c(n) + s(c,d,n)\,\alpha\big[\mathbf{x}(n) - \mathbf{m}_c(n)\big]$$

El ganador se mueve **hacia** el dato si acertó la clase, y se **aleja** si se equivocó. El castigo es lo que no existe en el SOM, y es lo que empuja la frontera entre clases a su lugar.

![Todo LVQ está en el signo.](imagenes/algoritmos/19-lvq.png){width=95%}

$$\mathbf{m}_i(n+1) = \mathbf{m}_i(n) \qquad \forall\, i \neq c$$

Se mueve **sólo el ganador**: no hay vecindad. A LVQ no le interesa la topología, le interesa la frontera de decisión.

## Forma combinación

$$\mathbf{m}_c(n+1) = \big[1 - s(n)\alpha(n)\big]\,\mathbf{m}_c(n) + s(n)\alpha(n)\,\mathbf{x}(n)$$

La misma regla reescrita: el prototipo nuevo es una combinación del viejo y del patrón que acaba de entrar. Escrita así se ve el problema del $\alpha$ constante.

## LVQ1-O — el $\alpha$ óptimo

$$\alpha_c(n) = \big[1 - s(n)\alpha_c(n)\big]\,\alpha_c(n-1)$$

La condición que se impone: que el patrón anterior siga pesando lo mismo que el actual después de este paso. Con $\alpha$ constante no pasa — cada patrón viejo arrastra un factor más, y el prototipo termina dependiendo casi sólo del final del archivo, que es un orden arbitrario.

$$\boxed{\;\alpha_c(n) = \frac{\alpha_c(n-1)}{1 + s(n)\,\alpha_c(n-1)}\;}$$

Despejando queda esto: un $\alpha$ propio de cada prototipo, que decrece solo cuando acierta y crece cuando se equivoca. **Hay que saturarlo en 1** (la advertencia de la cátedra: «no sobrepasar $\alpha > 1$»). Con $s=-1$ el denominador es $1-\alpha_c(n-1) < 1$ y $\alpha$ crece; si se acumulan errores seguidos pasa de 1, el prototipo se pasa de largo del patrón en cada corrección y el algoritmo se vuelve inestable.

### Cómo se lee

Todo LVQ está en el **signo**. Con $s=+1$ el prototipo se acerca al dato; con $s=-1$ **se aleja**. Ese castigo no existe en el SOM, y es lo que cambia el objetivo: al SOM le importa **cubrir bien el espacio**, a LVQ le importa **dónde queda la frontera entre clases**. Por eso acá no hay vecindad — la topología no le interesa.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Es el SOM con etiquetas y con castigo. Gana el prototipo más cercano, se mira si su clase era la correcta, y si acertó se acerca al dato y si se equivocó se aleja. Se mueve sólo el ganador: no hay vecindad, porque no busca un mapa ordenado sino una buena frontera de decisión.»*
> **Las repreguntas seguras:** dónde entra la supervisión (**desde la primera iteración**, a diferencia del SOM etiquetado, donde entra recién después de entrenar); por qué no tiene ordenamiento topológico; y el problema del $\alpha$ constante — los primeros patrones pesan cada vez menos y el prototipo termina dependiendo del final del archivo, que es un orden arbitrario.

---

\newpage

# 9. Capacidad de generalización y protocolo de evaluación

> **SI TE DICEN — «contame sobre generalización y evaluación»**
> «Generalizar es **funcionar bien con datos que la red no vio**, que es lo que realmente importa: el error de entrenamiento se puede llevar a cero memorizando. Como ese error no se puede calcular, **se estima con datos apartados**. Los datos se parten en **tres conjuntos disjuntos y estratificados**: entrenamiento ajusta los pesos, monitoreo decide hiperparámetros y cuándo parar, y prueba se mira **una sola vez** al final. El **sobreajuste** se ve en las curvas: entrenamiento sigue bajando mientras monitoreo toca un mínimo y sube; ahí se corta, **parada temprana**. Con pocos datos, **validación cruzada de $k$ particiones**: se entrena $k$ veces rotando qué bloque es de prueba y se reporta **media y varianza** del error. Para medir, la **matriz de confusión**: sensibilidad, especificidad, precisión, exactitud, $F_1$. **Nunca una sola medida**, porque con clases desbalanceadas la exactitud engaña.»


> **IDEA DE FONDO — en qué consiste**
> Contestar «¿qué tan bien anda esto?» **sin engañarse**. Lo que interesa no es el error sobre los datos con los que entrené —ése lo puedo llevar a cero memorizando— sino el error sobre datos que la red **nunca vio**. Como ese error no se puede calcular, se **estima**, y todo el protocolo existe para que esa estimación no esté inflada. Tres partes: **partir los datos** en conjuntos con trabajos distintos, **monitorear** el entrenamiento para saber cuándo parar, y **medir** con el número adecuado. La trampa que hay que saber nombrar: si elegís la cantidad de épocas o la arquitectura mirando el conjunto de prueba, ese número **ya no mide generalización**, porque lo usaste para decidir.


*No es un algoritmo de aprendizaje, pero es procedimiento y se pregunta igual.*

## Qué es generalizar

$$\varepsilon_{\text{gen}} = E\big[\varepsilon(\mathbf{x})\big]_{\mathbf{x}\sim\text{población}} \;\approx\; \varepsilon_{\text{prueba}}$$

La **capacidad de generalización** es el error esperado sobre toda la población de datos posibles, no sólo los que tengo. Como la población no se conoce, se la representa con un puñado de patrones **apartados desde el principio** y nunca usados para ajustar nada: ésa es la única estimación honesta que existe.

$$\varepsilon_{\text{entrenamiento}} \;\leq\; \varepsilon_{\text{prueba}}$$

En la práctica, casi siempre: el entrenamiento optimizó justo sobre esos patrones. (No es un teorema — con pocos patrones de prueba puede salir al revés por azar — pero si pasa seguido hay que sospechar de la partición.) Por eso **el error de entrenamiento nunca se reporta como resultado** — no mide nada que le importe a nadie. La distancia entre los dos números es lo que se llama **brecha de generalización**.

## Memorizar contra generalizar

$$\varepsilon_{\text{entren}}(n) \downarrow \quad\text{mientras}\quad \varepsilon_{\text{monit}}(n) \uparrow$$

El síntoma del **sobreajuste**, y es lo único que hay que saber dibujar: dos curvas contra las épocas. La de entrenamiento baja siempre; la de monitoreo baja, toca un mínimo y **vuelve a subir**. A partir de ese punto la red dejó de aprender la regla y empezó a aprender el ruido de los patrones concretos que le tocaron.

![El único dibujo que hay que saber hacer del tema: dos curvas, un mínimo, y ahí se corta.](imagenes/algoritmos/20-parada-temprana.png){width=90%}

| Capacidad del modelo | Error de entrenamiento | Error de monitoreo | Nombre |
|---|---|---|---|
| Insuficiente | alto | alto | **subajuste** — ni siquiera puede representar la regla |
| Adecuada | bajo | bajo | el punto que se busca |
| Excesiva | ≈ 0 | alto | **sobreajuste** — memorizó |

La capacidad se regula con la **cantidad de parámetros** (neuronas ocultas, capas, cantidad de centros en una RBF) y con **cuánto se entrena**. Con muchos parámetros y muchas épocas, cualquier red pasa por todos los puntos de entrenamiento — y no sirve para nada.

> **OJO — sobreajuste no es un error del algoritmo**
> El algoritmo hace exactamente lo que se le pidió: minimizar el error sobre el conjunto de entrenamiento. El problema es que **ése no era el objetivo real**. Por eso la solución no está adentro del algoritmo sino afuera: en cómo se parten los datos y cuándo se corta.

## Las tres particiones

$$\mathcal{D} = \mathcal{D}_{\text{entren}} \cup \mathcal{D}_{\text{monit}} \cup \mathcal{D}_{\text{prueba}}, \qquad \mathcal{D}_i \cap \mathcal{D}_j = \emptyset$$

El conjunto se parte en tres pedazos **disjuntos**. Disjuntos de verdad: un patrón repetido en dos conjuntos arruina la medición igual que si no se hubiera partido nada.

$$\mathcal{D}_{\text{entren}} \to \mathbf{W} \qquad \mathcal{D}_{\text{monit}} \to \text{hiperparámetros y parada} \qquad \mathcal{D}_{\text{prueba}} \to \text{el número final}$$

Cada uno tiene **un solo trabajo**, y ésa es la frase para el oral:

- **Entrenamiento** (≈ 50–70 %): es el único que entra en la regla de actualización. Sus patrones ajustan los pesos.
- **Monitoreo** o validación (≈ 15–25 %): **no ajusta pesos**, sólo se mide sobre él. Con eso se decide cuántas épocas, cuántas neuronas ocultas, qué $\mu$, qué arquitectura.
- **Prueba** (≈ 15–25 %): se guarda en un cajón y se mira **una sola vez**, al final, con todo ya decidido. Es el que estima la generalización.

$$\text{proporción de clases en cada partición} \;=\; \text{proporción en } \mathcal{D}$$

**Estratificación:** las tres particiones tienen que respetar la proporción original de clases. Si el 10 % de los datos es de la clase positiva, el 10 % de cada partición también. Sin eso, una partición puede quedarse sin ejemplos de una clase y el número no significa nada.

Y antes de partir, **se mezcla**: un archivo ordenado por clase partido tal cual deja el conjunto de prueba con una sola clase adentro.

![Tres conjuntos disjuntos con un trabajo cada uno, y la misma proporción de clases en los tres.](imagenes/algoritmos/21-particiones.png){width=95%}

> **OJO — la normalización también se contamina**
> Media, desvío, mínimos y máximos para normalizar se calculan **sólo con el conjunto de entrenamiento** y después se aplican a los otros dos. Calcularlos sobre todo el conjunto es filtrar información de la prueba hacia el entrenamiento, y el error de prueba sale optimista.

## Monitoreo y parada temprana

$$n^{*} = \arg\min_{n}\; \varepsilon_{\text{monit}}(n) \qquad \mathbf{W}^{*} = \mathbf{W}(n^{*})$$

**Parada temprana:** se entrena midiendo el error de monitoreo época por época, y se guarda la red del **mínimo de esa curva**, no la del final. El entrenamiento puede seguir un rato más para confirmar que el mínimo era el mínimo —eso es la *paciencia*— pero los pesos que quedan son los de $n^{*}$.

$$\varepsilon_{\text{monit}} \text{ decide} \;\Longrightarrow\; \varepsilon_{\text{monit}} \text{ ya no mide}$$

Y acá está la razón de ser del tercer conjunto, que es lo que más se pregunta. El monitoreo **no entrena** —sus patrones nunca entran en $\Delta w$— pero **sí decide**: la época elegida es la que a él le convino. Después de usarlo para elegir, su error quedó tan sesgado como el de entrenamiento, sólo que menos. Por eso hace falta un conjunto de **prueba** que no haya participado de ninguna decisión.

## Validación cruzada de $k$ particiones ($k$-fold)

$$\mathcal{D} = \bigcup_{j=1}^{k}\mathcal{F}_j, \qquad \mathcal{F}_i \cap \mathcal{F}_j = \emptyset, \qquad |\mathcal{F}_j| \approx N/k$$

El conjunto se parte en $k$ bloques (*folds*) disjuntos y del mismo tamaño, **estratificados** igual que antes. Se usa cuando hay **pocos datos**: apartar un 20 % fijo para prueba sería desperdiciar patrones y, además, el resultado dependería demasiado de cuáles tocaron.

$$\varepsilon_j = \varepsilon\big(\mathcal{F}_j\big) \quad \text{entrenando con} \quad \mathcal{D}\setminus\mathcal{F}_j, \qquad j = 1,\dots,k$$

Se entrena $k$ veces. En la vuelta $j$, el bloque $\mathcal{F}_j$ hace de prueba y los otros $k-1$ de entrenamiento. Así **cada patrón se usa para medir exactamente una vez** y para entrenar $k-1$ veces. Cada vuelta **reinicializa los pesos de cero**: si no, la segunda red arrancaría sabiendo cosas del bloque que le toca medir.

![Con $k=5$: cinco entrenamientos, y cada bloque hace de prueba exactamente una vez.](imagenes/algoritmos/22-kfold.png){width=90%}

$$\bar{\varepsilon} = \frac{1}{k}\sum_{j=1}^{k}\varepsilon_j \qquad \sigma^2_\varepsilon = \frac{1}{k}\sum_{j=1}^{k}\big(\varepsilon_j - \bar{\varepsilon}\big)^2$$

El resultado es la **media** de los $k$ errores, y **la varianza se reporta siempre con ella**: dice si el resultado es estable o si dependió de qué patrones tocaron. Una media de 8 % con desvío de 1 % y otra de 8 % con desvío de 6 % son resultados completamente distintos.

$$k = N \;\Longrightarrow\; \textit{leave-one-out}$$

El caso extremo: cada bloque es **un solo patrón**. Se entrena $N$ veces y se mide sobre uno cada vez. Aprovecha el máximo de datos posible, pero cuesta $N$ entrenamientos y la estimación tiene **mucha varianza**. Los valores usuales son $k = 5$ o $k = 10$, que equilibran costo y estabilidad.

> **OJO — la validación cruzada evalúa un método, no entrega un modelo**
> Al terminar hay $k$ redes distintas, y ninguna es «la» red. Lo que se estimó es qué tan bien anda **el procedimiento** (esta arquitectura, con estos hiperparámetros, sobre estos datos). Elegido el procedimiento, el modelo final se entrena **de nuevo, con todos los datos**.
> Y si dentro de la validación cruzada además hay que elegir hiperparámetros, el conjunto de monitoreo sale de los $k-1$ bloques de entrenamiento — **nunca** del bloque que está haciendo de prueba.

## Matriz de confusión

|  | predijo $\oplus$ | predijo $\ominus$ | total real |
|---|---|---|---|
| **es $\oplus$** | $t_\oplus$ | $f_\ominus$ | $N_\oplus$ |
| **es $\ominus$** | $f_\oplus$ | $t_\ominus$ | $N_\ominus$ |

La tabla cruza **lo que era** (filas) contra **lo que dijo** (columnas). La diagonal son los aciertos; fuera de la diagonal, los dos tipos de error, que casi nunca cuestan lo mismo.

$$N_\oplus = t_\oplus + f_\ominus \qquad N_\ominus = f_\oplus + t_\ominus \qquad N = N_\oplus + N_\ominus$$

Los totales por fila son los que **realmente** pertenecen a cada clase. Ojo con la lectura de los nombres: $f_\ominus$ es «dijo negativo y erró», o sea que **era positivo**. El subíndice nombra lo que la red **dijo**, no lo que era.

![Cada medida mira una parte distinta de la tabla: una fila, una columna, o todo.](imagenes/algoritmos/23-confusion.png){width=100%}

$$s^{+} = \frac{t_\oplus}{N_\oplus} \qquad s^{-} = \frac{t_\ominus}{N_\ominus} \qquad p = \frac{t_\oplus}{t_\oplus + f_\oplus} \qquad a = \frac{t_\oplus + t_\ominus}{N}$$

**Sensibilidad** $s^{+}$: de los que **eran** positivos, cuántos agarré (una fila). **Especificidad** $s^{-}$: de los que **eran** negativos, cuántos dejé pasar bien (la otra fila). **Precisión** $p$: de los que **dije** positivos, cuántos acerté (una columna). **Exactitud** $a$: la diagonal sobre el total.

$$F_1 = \frac{2t_\oplus}{2t_\oplus + f_\oplus + f_\ominus} = 2\,\frac{s^{+}p}{s^{+}+p} \qquad G = \sqrt{s^{+}p}$$

Combinan sensibilidad y precisión en un número: $F_1$ es su **media armónica** y $G$ la **geométrica**. Las dos castigan el desbalance: si una de las dos es cero, el combinado es cero, cosa que un promedio común no haría.

> **OJO — el clasificador trivial, que es la repregunta clásica**
> Con 95 % de negativos, una red que contesta **siempre negativo** consigue $a = 0{,}95$, $s^{-} = 1$ y $s^{+} = 0$. La exactitud sola la haría pasar por excelente. Por eso **nunca se reporta una sola medida**, y por eso con clases desbalanceadas se mira $F_1$, $G$ o la matriz completa.

![Dos clasificadores con exactitud parecida y utilidad opuesta.](imagenes/algoritmos/24-trivial.png){width=92%}

$$e = 1-a \qquad \delta_e = \frac{e_r - e}{e_r}$$

La mejora relativa respecto de un sistema de referencia: pasar de 98 % a 99 % de exactitud es **reducir el error a la mitad**, y pasar de 50 % a 51 % no es lo mismo aunque el salto de exactitud sea igual.

## Medidas para predicción

$$e_i = y_i - \hat{y}_i \qquad \tilde{\varepsilon}_A = \frac{1}{N}\sum_i \lvert e_i\rvert \qquad \tilde{\varepsilon}_S = \frac{1}{N}\sum_i e_i^2 \qquad \tilde{\varepsilon}_R = \sqrt{\tilde{\varepsilon}_S}$$

No se puede usar la suma de los errores: los signos se compensan. Por eso valor absoluto o cuadrado, y la raíz del cuadrático para volver a las **unidades del dato**. El cuadrático castiga más los errores grandes; el absoluto trata a todos igual.

### Cómo se lee

Todo el protocolo se lee con **una sola pregunta por conjunto: ¿este número participó de alguna decisión?** El de entrenamiento participó de todas, así que no mide nada. El de monitoreo participó de una —cuándo parar y qué arquitectura—, así que mide de más. El de prueba no participó de ninguna: es el único que estima la generalización, y por eso se mira **una sola vez**.

Y la matriz de confusión se lee **por dirección**: sensibilidad y especificidad miran **una fila** cada una (de los que **eran** de esa clase, cuántos agarré); la precisión mira **una columna** (de los que **dije** de esa clase, cuántos acerté); la exactitud mira todo. Un clasificador que dice siempre lo mismo engaña a varias de ellas.

> **PARA LA DEFENSA — la respuesta de treinta segundos**
> *«Generalizar es andar bien con datos que la red no vio, y como ese error no se puede calcular, se estima apartando datos desde el principio. Los datos se parten en tres conjuntos disjuntos y estratificados: entrenamiento ajusta los pesos, monitoreo decide cuándo parar y qué arquitectura usar, y prueba se mira una sola vez al final. Si hay pocos datos se usa validación cruzada de k particiones: se entrena k veces rotando cuál bloque hace de prueba, y se reporta la media de los k errores junto con la varianza.»*
> **Las repreguntas seguras:** por qué no alcanza con dos conjuntos (**porque el monitoreo decide, y lo que decide ya no puede medir**); cómo se ve el sobreajuste (**las dos curvas: entrenamiento baja, monitoreo toca un mínimo y sube — ahí se corta**); por qué cada vuelta de la validación cruzada **reinicializa los pesos**; y por qué la exactitud sola no sirve (**el clasificador trivial con clases desbalanceadas**).

---

\newpage

# Los algoritmos, lado a lado

| Algoritmo | Qué ajusta | Criterio | Competitivo | Parada |
|---|---|---|---|---|
| Perceptrón (corrección) | $\mathbf{w}$ | $d - y$ | no | sin errores en una pasada |
| Perceptrón (LMS) | $\mathbf{w}$ | $e^2$ | no | épocas / error |
| Multicapa | todas las $\mathbf{W}^{(p)}$ | $\tfrac12\sum e_j^2$ | no | épocas / monitoreo |
| Base radial fase 1 | $\boldsymbol{\mu}_j$ | $J$ de $k$-medias | **sí** | sin reasignaciones |
| Base radial fase 2 | $w_{kj}$ | $\tfrac12\sum e_k^2$ | no | épocas / error |
| Hopfield | $w_{ji}$ (una vez) | — (Hebb) | no | $N$ pasos sin cambios |
| BPTT | $\mathbf{W}$, $\mathbf{W}^{I}$ | $\tfrac12\sum_t\sum_k e^2$ | no | épocas |
| SOM | $\mathbf{w}_j$ y vecinas | — | **sí** | épocas |
| LVQ1 | $\mathbf{m}_c$ | acierto de clase | **sí** | épocas |

## Las cuatro frases que ordenan todo

1. **Perceptrón, multicapa, RBF fase 2 y BPTT son el mismo esquema:** bajar por el gradiente de un error cuadrático. Lo que cambia es qué tan difícil es calcular ese gradiente.
2. ***k*-medias, SOM y LVQ son el mismo esquema:** gana el más cercano y se mueve hacia el dato. Lo que cambia es quién más se mueve — nadie, los vecinos de la grilla, o el ganador con signo.
3. **Hopfield es el único que no itera para entrenar:** una cuenta y listo. Y es el único que itera para usarse.
4. **La activación decide la forma de la frontera:** sigmoide, semiespacios; radial, burbujas locales.
