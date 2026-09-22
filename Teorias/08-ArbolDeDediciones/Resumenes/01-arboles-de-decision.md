---
title: "Árboles de decisión"
subtitle: "Inteligencia Computacional · FICH-UNL \\newline Apunte armado sobre el capítulo 8 (*Non-metric Methods*) de *Pattern Classification*, Duda, Hart \\& Stork"
lang: es
---

*Este tema no tiene diapositivas de cátedra en la carpeta: el apunte está armado sobre el capítulo 8 de Duda–Hart–Stork, que es la bibliografía de la materia. Todos los números de los ejemplos están verificados.*

*Nivel al que se toma: el método en detalle, el algoritmo de construcción, y sobre todo **el concepto de impureza** — qué se busca al medirla y qué decisión se toma con ella. Gini y entropía, sin deducciones. Ventajas y desventajas.*

---

## 1. Por qué hacen falta: los datos sin métrica

Todo lo que viste hasta acá —perceptrón, multicapa, radial, SOM, LVQ, el clasificador de Bayes— comparte un supuesto: los patrones son **vectores de números reales** y existe una **noción natural de distancia** entre ellos. En el vecino más cercano la distancia *es* el método; en una red neuronal aparece cuando dos entradas «cercanas» producen salidas parecidas.

Pero hay problemas donde eso no existe. El ejemplo de Duda: clasificar peces y mamíferos marinos usando información sobre **los dientes**. Algunos son finos y pequeños (la ballena, que filtra), otros vienen en varias filas (el tiburón), otros son colmillos (la morsa), y otros animales directamente no tienen (el calamar). **¿Cuál es la distancia entre «colmillo» y «varias filas»?** No hay. No tiene sentido decir que los dientes de una ballena se parecen más a los colmillos de una morsa que las filas del tiburón a la ausencia en el calamar.

A ese tipo de información se le dice **datos nominales**: discretos, sin orden natural y sin similitud definida. Se describen con una **tupla de propiedades**: una fruta puede ser $\{\text{rojo},\ \text{brillante},\ \text{dulce},\ \text{chica}\}$, que es la forma corta de *color = rojo*, *textura = brillante*, *sabor = dulce*, *tamaño = chico*.

> **OJO — «atributo» y «característica» no son sinónimos en este capítulo**
> Duda reserva **característica** (*feature*) para los datos de valor real, y usa **atributo** para los dos casos: nominales y reales. Es un detalle de vocabulario que conviene respetar acá.

### Claves de la sección 1

| Clave | Qué tenés que poder responder |
|---|---|
| Qué son datos nominales | Discretos, sin orden ni similitud natural |
| El ejemplo | Los dientes: no hay distancia entre «colmillo» y «sin dientes» |
| Por qué fallan los otros métodos | Todos suponen que existe una métrica |
| Cómo se describe un patrón | Tupla de propiedades, o cadena de atributos |

---

## 2. Qué es un árbol de decisión

La idea es la del juego de las **veinte preguntas**: clasificar mediante una secuencia de preguntas, donde **la próxima pregunta depende de la respuesta a la anterior**. Y sirve justo para datos nominales, porque todas las preguntas pueden ser del tipo *sí/no* o *«el valor de esta propiedad, ¿está en este conjunto?»*, que no necesitan ninguna métrica.

Esa secuencia se dibuja como un **árbol**, con este vocabulario:

- **Nodo raíz**: el primero, arriba por convención. Pregunta por el valor de una propiedad.
- **Ramas** o **enlaces**: salen de cada nodo, una por cada respuesta posible. Tienen que ser **mutuamente excluyentes y exhaustivas**: se sigue una y sólo una.
- **Nodos de decisión**: los internos; cada uno es la raíz de un **sub-árbol**.
- **Nodos hoja**: terminales, sin más preguntas. **Cada hoja lleva una etiqueta de clase.**

**Clasificar** es entonces: empezar en la raíz, responder la pregunta, bajar por la rama correspondiente, repetir, y al llegar a una hoja asignar su etiqueta.

Dos detalles del árbol de ejemplo de Duda (el de las frutas) que conviene notar:

- **La misma pregunta puede aparecer en varios lugares** del árbol (*¿Tamaño?* aparece tres veces), y **distintas preguntas pueden tener distinta cantidad de ramas**.
- **Varias hojas distintas pueden llevar la misma etiqueta**. Manzana aparece en dos hojas.

### La interpretabilidad

Es la ventaja que distingue a los árboles de casi todo lo demás, y tiene **dos formas**:

**1. Se puede leer la decisión de un patrón concreto** como la conjunción de las decisiones a lo largo de su camino. Con propiedades $\{$sabor, color, forma, tamaño$\}$, el patrón $\mathbf{x} = \{$dulce, amarillo, fino, mediano$\}$ se clasifica como **Banana** porque *(color = amarillo)* **Y** *(forma = fina)*.

**2. Se puede describir una clase entera** con conjunciones y disyunciones:

$$\text{Manzana} = (\text{verde} \wedge \text{mediana}) \vee (\text{rojo} \wedge \text{mediana}) \;\equiv\; (\text{mediana} \wedge \neg\,\text{amarillo})$$

> **IDEA DE FONDO — por qué esto importa tanto**
> Una red neuronal entrenada es una matriz de pesos: anda, pero no te puede decir **por qué** decidió lo que decidió. Un árbol te devuelve una **regla en castellano**. En medicina, en agronomía o en cualquier dominio donde un humano tiene que firmar la decisión, eso vale más que un punto de exactitud. Es también la razón por la que los árboles son el lugar natural para **incorporar conocimiento previo de un experto** — aunque eso rinde sobre todo cuando el problema es simple y hay pocos datos.

Y dos beneficios más: **la clasificación es rapidísima** (una secuencia corta de preguntas simples), y el árbol **no necesita que los atributos sean numéricos**.

### Claves de la sección 2

| Clave | Qué tenés que poder responder |
|---|---|
| El vocabulario | Raíz, rama, nodo de decisión, hoja — y qué hay en cada uno |
| Cómo clasifica | De la raíz a una hoja, siguiendo una sola rama por nodo |
| Las ramas | Mutuamente excluyentes y exhaustivas |
| Las dos interpretabilidades | Regla de un patrón (conjunción del camino) y descripción de una clase |

---

## 3. CART: las seis preguntas

Hasta acá sabemos **usar** un árbol. Ahora hay que **construirlo** a partir de datos etiquetados, y ahí aparece el algoritmo.

La idea de fondo es simple y **recursiva**. Cualquier árbol va partiendo el conjunto de entrenamiento en subconjuntos cada vez más chicos. Lo ideal sería que en cada subconjunto todas las muestras tuvieran la **misma etiqueta** — se dice que el subconjunto es **puro** — y ahí se corta. Como en general eso no pasa, en cada nodo hay que decidir una de dos cosas:

> **o declaro este nodo una hoja y acepto una decisión imperfecta, o elijo otra propiedad y sigo partiendo.**

**CART** (*Classification and Regression Trees*) no es un algoritmo único sino un **marco general** que se puede instanciar de muchas formas. Y el marco consiste en **seis preguntas**, que es como conviene tenerlo ordenado en la cabeza:

| # | Pregunta | Sección |
|---|---|---|
| 1 | ¿Las propiedades se restringen a binarias o pueden ser multivaluadas? | §4 |
| 2 | **¿Qué propiedad se pregunta en cada nodo?** | §5 |
| 3 | ¿Cuándo se declara hoja a un nodo? | §6 |
| 4 | Si el árbol queda demasiado grande, ¿cómo se lo poda? | §7 |
| 5 | Si una hoja es impura, ¿qué etiqueta se le pone? | §8 |
| 6 | ¿Cómo se manejan los datos faltantes? | §9 |

> **PARA LA DEFENSA — si te piden «el algoritmo de construcción», contestá con estas seis**
> No es una lista que inventó el apunte: es la estructura con la que el libro organiza todo el capítulo. Enumerarlas y después desarrollar la segunda —que es la importante— muestra que tenés el método completo y no sólo la fórmula de Gini.

---

## 4. Pregunta 1 — cuántas ramas por nodo

Cada decisión en un nodo se llama **corte** (*split*), porque parte un subconjunto de los datos. La cantidad de ramas que bajan de un nodo es el **factor de ramificación** $B$, y la elige el diseñador; puede variar dentro de un mismo árbol.

**Pero cualquier decisión se puede expresar con decisiones binarias.** En el árbol de las frutas, el nodo raíz pregunta por el color con $B=3$ (verde, amarillo, rojo); se lo puede reemplazar por dos nodos binarios encadenados: *«¿es verde?»*, y por la rama del «no», *«¿es amarillo?»*.

Por esa **potencia expresiva universal de los árboles binarios** y porque son más simples de entrenar, se trabaja casi siempre con $B=2$.

> **OJO — con datos numéricos el corte binario tiene forma geométrica**
> Si la pregunta de cada nodo es *«¿es $x_i \le x_{is}$?»*, la frontera que produce es un **hiperplano perpendicular a un eje**. Un árbol binario sobre datos reales dibuja entonces regiones de decisión formadas por **rectángulos alineados a los ejes**. Es la imagen que hay que tener en la cabeza, y es también su limitación (§12).

---

## 5. Pregunta 2 — la impureza: el corazón del método

Ésta es la pregunta en la que se concentra casi todo el trabajo de diseño, y es la que se toma.

**Qué se busca.** Se quiere elegir, en cada nodo, la pregunta que deje a los hijos **lo más puros posible** — es decir, con la mezcla de clases lo más parecida a «todos de la misma clase». Para poder elegir hace falta **medir** esa mezcla, y esa medida es la **impureza**.

### La definición

$i(N)$ denota la impureza del nodo $N$, y se le pide una sola cosa:

> $i(N) = 0$ si **todos** los patrones que llegan al nodo son de la misma clase, y **grande** cuando las clases están igualmente representadas.

En todo lo que sigue, $P(\omega_j)$ es **la fracción de los patrones del nodo $N$ que son de la clase $\omega_j$** — no una probabilidad de la población, sino una proporción medida en ese nodo.

### Las cuatro medidas

**Impureza de entropía** (o de información) — la más usada:

$$i(N) = -\sum_j P(\omega_j)\,\log_2 P(\omega_j)$$

Vale 0 si todos son de la misma clase y es positiva si no, con el máximo cuando las clases están repartidas por igual.

**Impureza de varianza** — la forma polinómica más simple, para dos clases:

$$i(N) = P(\omega_1)\,P(\omega_2)$$

**Impureza de Gini** — la generalización de la anterior a más de dos clases:

$$i(N) = \sum_{i \neq j} P(\omega_i)P(\omega_j) = 1 - \sum_j P^2(\omega_j)$$

Se lee así: **es la tasa de error esperada en ese nodo si la etiqueta se sorteara según la distribución de clases presente en él.**

**Impureza de clasificación**:

$$i(N) = 1 - \max_j P(\omega_j)$$

Mide la **mínima probabilidad de que un patrón de entrenamiento sea mal clasificado** en ese nodo. Es la más «picuda» de todas en el punto de clases equilibradas, pero tiene **derivada discontinua**, lo que trae problemas al buscar el óptimo.

> **OJO — en el caso de dos clases, varianza y Gini son la misma función**
> Con $c=2$, $1 - (P_1^2 + P_2^2) = 2P_1P_2$: son idénticas salvo un factor. Las cuatro curvas tienen su máximo en el punto de clases equilibradas y valen cero en los extremos.

### Cómo se elige la pregunta

Se elige la que produce la **mayor caída de impureza**:

$$\Delta i(T) = i(N) - P_L\,i(N_L) - (1 - P_L)\,i(N_R)$$

donde $N_L$ y $N_R$ son los hijos izquierdo y derecho, y $P_L$ es la fracción de patrones de $N$ que van a la izquierda con la pregunta $T$. **El mejor corte es el que maximiza $\Delta i(T)$.**

> **IDEA DE FONDO — con entropía, la caída de impureza *es* la ganancia de información**
> Por eso la literatura habla indistintamente de «maximizar la ganancia de información» y «minimizar la impureza de entropía»: es lo mismo dicho de dos maneras. Y como en un árbol binario cada pregunta es un sí/no, **esa ganancia no puede ser mayor que un bit**.

**Para cortes multivaluados** ($B > 2$) hace falta corregir: un corte en muchas ramas baja la impureza «gratis», sólo por partir en más pedazos. Se usa entonces la **razón de ganancia**, que divide $\Delta i$ por la entropía del propio reparto entre ramas.

### El ejemplo que hay que saber: por qué Gini y no clasificación

Es el ejemplo de Duda, y es el que muestra que las medidas **no son equivalentes**. Un nodo con **90 patrones de $\omega_1$ y 10 de $\omega_2$**:

| Medida | Impureza del padre |
|---|---|
| clasificación | $1 - 0{,}9 = 0{,}100$ |
| Gini | $1 - (0{,}9^2 + 0{,}1^2) = 0{,}180$ |
| entropía | $0{,}469$ |

Supongamos que **ningún corte logra mayoría de $\omega_2$ en alguno de los hijos**. Entonces la impureza de clasificación se queda en $0{,}1$ pase lo que pase, y **no distingue ningún corte de otro**.

Pero mirá este corte: manda **70 de $\omega_1$ y 0 de $\omega_2$** a la derecha, y **20 de $\omega_1$ y 10 de $\omega_2$** a la izquierda. Es claramente bueno: dejó un hijo **puro**.

| Medida | $i(N_L)$ | $i(N_R)$ | ponderado | $\Delta i$ |
|---|---|---|---|---|
| clasificación | $0{,}333$ | $0$ | $0{,}100$ | $\mathbf{0{,}000}$ |
| Gini | $0{,}444$ | $0$ | $0{,}133$ | $\mathbf{0{,}047}$ |
| entropía | $0{,}918$ | $0$ | $0{,}276$ | $\mathbf{0{,}194}$ |

**La impureza de clasificación no ve ninguna mejora. Gini y entropía sí.**

> **PARA LA DEFENSA — la frase de Duda sobre esto**
> *Gini «anticipa» los cortes útiles que vienen después.* Aunque nuestro objetivo final sea clasificar bien, conviene **no** usar la tasa de error como criterio de corte, porque es ciega a los cortes que todavía no separan clases pero preparan el terreno para los siguientes.

> **OJO — el dato que contradice la intuición, y que conviene decir**
> *«La elección particular de la función de impureza raramente parece afectar al clasificador final y a su exactitud.»* Lo que **sí** la determina es **el criterio de parada y el método de poda**. Si te preguntan «¿Gini o entropía?», la respuesta completa es: en la práctica da casi igual —se usa entropía por simplicidad computacional y por su base en teoría de la información—, y **lo que hay que cuidar es cuándo parar y cómo podar**.

### Claves de la sección 5

| Clave | Qué tenés que poder responder |
|---|---|
| Qué es la impureza | La mezcla de clases en un nodo; 0 si es puro, máxima si están parejas |
| Qué es $P(\omega_j)$ acá | La **fracción de patrones del nodo** de esa clase |
| Las cuatro medidas | Entropía, varianza, Gini, clasificación — y escribir al menos Gini y entropía |
| Qué se decide con ella | Qué pregunta va en cada nodo: la que maximiza $\Delta i$ |
| $\Delta i$ | La fórmula con los hijos ponderados por la fracción que va a cada uno |
| Gini vs. clasificación | El ejemplo 90/10, y la frase de que Gini «anticipa» |
| Qué importa más | La parada y la poda, no la medida |

---

## 6. Pregunta 3 — cuándo parar

Si se sigue partiendo hasta el final, cada hoja termina con un solo patrón: impureza cero y **sobre-ajuste** garantizado. Si se para demasiado pronto, queda un árbol que no aprendió. Es el mismo compromiso de la unidad de generalización, con otra ropa.

Las opciones:

- **Validación cruzada.** Se entrena con una parte y se corta cuando el error sobre la otra parte deja de bajar.
- **Umbral de reducción de impureza.** Se corta cuando el mejor $\Delta i$ disponible no supera un umbral. Tiene dos ventajas: el árbol crece **desbalanceado** y puede seguir por algunas ramas y no por otras, y **usa todos los datos de entrenamiento**.
- **Criterio de complejidad.** Minimizar $\sum_{\text{hojas}} i(N) + \alpha\,(\text{tamaño del árbol})$, que es la idea de **longitud de descripción mínima**: la suma de impurezas mide la incerteza que queda, y el tamaño mide la complejidad del clasificador. El problema es fijar $\alpha$.
- **Significancia estadística.** Se prueba si el corte candidato **difiere significativamente de un corte al azar**, con un test $\chi^2$. Si el corte más significativo del nodo no supera el nivel de confianza elegido, se deja de partir.

---

## 7. Pregunta 4 — la poda, y el efecto horizonte

Parar tiene un problema de fondo, y tiene nombre: **el efecto horizonte** (*horizon effect*).

La decisión óptima en un nodo $N$ **no está influida por lo que pasaría en sus descendientes**. Entonces un criterio de parada puede declarar hoja a $N$ y con eso **cortar la posibilidad de cortes muy buenos más abajo**. Dicho de otro modo: parar sesga el aprendizaje hacia árboles donde la mayor reducción de impureza está **cerca de la raíz**.

La alternativa es **podar**:

1. Se hace crecer el árbol **entero**, hasta que las hojas tengan impureza mínima — más allá de cualquier horizonte.
2. Se consideran todos los **pares de hojas hermanas** (las que cuelgan de un mismo padre).
3. Todo par cuya eliminación produzca un aumento **pequeño** de impureza se elimina, y el padre pasa a ser hoja. Ese padre, a su vez, puede ser podado después.

Podar es exactamente **la operación inversa de partir**. Y después de podar es normal que las hojas queden a distintos niveles y el árbol quede desbalanceado.

> **OJO — los dos nombres**
> Parar antes es **pre-poda**; podar después de crecer es **post-poda**. Son los mismos objetos que ya conocés con otro nombre: es el **corte temprano** de la unidad de generalización, aplicado a la estructura en vez de a las épocas.

**Poda de reglas.** Un enfoque distinto: cada hoja tiene asociada una **regla** —la conjunción de todas las decisiones desde la raíz hasta ella—, así que el árbol entero se puede escribir como una lista de reglas. Después se eliminan las precondiciones redundantes o las que no mejoran el desempeño sobre un conjunto de validación. Tiene dos ventajas propias:

- permite **eliminar un nodo en unos contextos y conservarlo en otros** — en la poda de nodos hay que quedárselo o tirarlo para todos los patrones;
- puede eliminar información de nodos **cercanos a la raíz**, cosa que la poda por impureza, que fusiona hojas, no puede.

**Poda vs. parada, en una línea:** podar es mejor porque evita el efecto horizonte y **usa toda la información del conjunto de entrenamiento**, pero es más caro; con conjuntos muy grandes el costo puede ser prohibitivo.

---

## 8. Pregunta 5 — qué etiqueta lleva cada hoja

Es el paso más simple de todos. Si la hoja es pura, lleva esa clase. Si no lo es —que es lo normal cuando hubo parada o poda—, lleva **la clase con más patrones representados** en ella: mayoría simple.

> **OJO — una impureza extremadamente baja no es una buena noticia**
> Puede ser el síntoma de que el árbol se está sobre-ajustando a los datos de entrenamiento.

---

## 9. Pregunta 6 — atributos faltantes

Hay dos situaciones distintas y se resuelven distinto.

**Durante el entrenamiento.** Lo ingenuo sería descartar los patrones incompletos, pero eso desperdicia datos. Lo que se hace es calcular las impurezas **usando sólo la información presente**: si hay $n$ patrones en el nodo y uno no tiene el atributo $x_3$, los cortes sobre $x_1$ y $x_2$ se evalúan con los $n$ patrones y los cortes sobre $x_3$ con los $n-1$ que lo tienen. Se elige, como siempre, el de mayor caída de impureza.

**Durante la clasificación.** Acá hay que haber previsto el problema al entrenar. Cada nodo interno guarda, además de su **corte primario**, una lista ordenada de **cortes sustitutos** (*surrogate splits*): cortes sobre **otros** atributos, elegidos no por su reducción de impureza sino por su **asociación predictiva** con el primario.

La asociación predictiva entre dos cortes es simplemente **la cantidad de patrones que los dos mandan para el mismo lado**. El primer sustituto es el que más se parece al primario en ese sentido; el segundo, el mejor entre los atributos que quedan.

Al clasificar un patrón incompleto se usa el corte primario si se puede, y si el atributo falta se baja al **primer sustituto que no involucre un atributo faltante**.

> **IDEA DE FONDO — el sustituto es un reemplazo por correlación**
> Esta estrategia equivale a reemplazar el valor que falta por el del atributo **más correlacionado** con él. Aprovecha al máximo las asociaciones locales entre atributos.

Y un detalle que el libro remarca: **a veces el hecho de que un atributo falte es en sí mismo informativo.** En diagnóstico médico, que no esté medida la glucemia puede significar que el médico tuvo un motivo para no pedirla. En ese caso conviene representar «falta» como **un valor más** del atributo, y usarlo para clasificar.

---

## 10. Priors y costos

Hasta acá se asumió que cada clase aparece con la misma frecuencia en entrenamiento y en test. Si no es así, se **pondera** las muestras para corregir las frecuencias a priori.

Y si además los errores no cuestan lo mismo —el problema de la anemia de la unidad de bases estadísticas—, se usa una **matriz de costos** $\lambda_{ij}$: lo que cuesta clasificar como $\omega_i$ un patrón que era $\omega_j$. Eso entra directamente en la impureza:

$$i(N) = \sum_{ij} \lambda_{ij}\,P(\omega_i)P(\omega_j) \qquad \textbf{(Gini ponderada)}$$

que es la que se usa durante el entrenamiento.

---

## 11. Costo computacional, e inestabilidad

**Complejidad.** Con $n$ patrones en $d$ dimensiones, dos clases, cortes paralelos a los ejes e impureza de entropía:

| | Complejidad | Se lee |
|---|---|---|
| Entrenamiento, sólo la raíz | $O(d\,n\log n)$ | hay que **ordenar** los datos por cada atributo |
| Entrenamiento, total | $O\big(d\,n\,(\log n)^2\big)$ | sumando nivel por nivel; los niveles son $O(\log n)$ |
| **Clasificación** | $O(\log n)$ | es simplemente la profundidad del árbol |
| Espacio | $O(n)$ | la cantidad de nodos |

> **PARA LA DEFENSA — la moraleja de la tabla**
> **Entrenar es muchísimo más caro que clasificar**, y la diferencia **crece** con el tamaño del problema. Un árbol entrenado es de los clasificadores más rápidos que existen en uso: unas pocas comparaciones y listo.

**Inestabilidad.** Es la desventaja más seria y hay que saber explicarla. En el ejemplo de Duda, mover **un solo punto de entrenamiento** apenas —el punto marcado con asterisco, movido un poco hacia abajo— produce **un árbol y unas regiones de decisión radicalmente distintos**.

La causa: la creación del árbol es **discreta y voraz** (*greedy*). Cada corte se elige mirando sólo el nodo actual, y una decisión distinta cerca de la raíz cambia todo lo que cuelga de ella. Cualquier clasificador cambia un poco si cambiás un poco los datos; un árbol puede cambiar **entero**.

---

## 12. Árboles multivariados

El problema de los cortes paralelos a los ejes: si los datos se separan bien por una recta **oblicua**, un árbol de cortes axiales necesita una escalera de muchísimos nodos para aproximarla, y queda enorme y frágil.

La solución es permitir que cada nodo pregunte por una **combinación lineal** de las características:

$$\text{¿es } \textstyle\sum_i w_i x_i < w_0\ ?$$

Con eso los cortes van en **direcciones arbitrarias** y el árbol se vuelve mucho más chico y compacto. Para encontrar esos pesos en cada nodo se usa **LMS**, y el motivo es el que ya conocés: en casi todos los casos interesantes los datos **no son linealmente separables**, y LMS funciona igual, mientras que los métodos que exigen separabilidad no.

> **IDEA DE FONDO — acá se cierra el círculo con la primera unidad**
> Cada nodo de un árbol multivariado **es un perceptrón**. El árbol pasa a ser una forma de combinar muchos clasificadores lineales chiquitos en una estructura de decisiones anidadas.

---

## 13. Otros algoritmos: ID3 y C4.5

| | **CART** | **ID3** | **C4.5** |
|---|---|---|---|
| Datos | nominales y reales | **sólo nominales** (los reales se discretizan en intervalos) | como CART |
| Ramas | binarias (por convención) | $B_j$ = cantidad de valores del atributo $j$ | multivaluadas con datos nominales |
| Impureza | cualquiera; suele ser entropía | razón de ganancia (por los cortes multivaluados) | razón de ganancia |
| Parada | varias | cuando todo es puro o **no quedan variables** | heurísticas por significancia estadística |
| Poda | sí | no, en su presentación estándar | sí, **y poda de reglas** (C4.5Rules) |
| Faltantes al clasificar | **cortes sustitutos** | — | **baja por las $B$ ramas** y combina las hojas, pesadas por las probabilidades de decisión del nodo |

Dos consecuencias de la última fila, que son buena respuesta de oral:

- C4.5 **no aprovecha las correlaciones entre atributos**, que es justamente lo que hacen los sustitutos de CART.
- Pero como no tiene que calcular ni guardar los sustitutos, **C4.5 ocupa menos memoria**. Si el espacio es la preocupación principal, es preferible.

**¿Cuál es el mejor?** La respuesta del libro: **ninguno domina a los demás.** Vale más comparar las piezas que los nombres — la medida de impureza, el criterio de parada, el método de poda — porque con cuidado se puede armar un árbol con cualquier combinación. Y tres recomendaciones concretas:

- la **entropía** anda aceptablemente en casi todos los casos y es el default natural;
- **podar es preferible a parar**, salvo que el conjunto sea tan grande que resulte carísimo;
- la **discretización de ID3** desaprovecha la información de orden de los datos reales, así que conviene sólo si el costo computacional no deja otra.

---

## 14. Ventajas y desventajas

| Ventajas | Desventajas |
|---|---|
| **Interpretables**: dan reglas legibles, no una matriz de pesos | **Inestables**: mover un punto de entrenamiento puede cambiar el árbol entero |
| Sirven para **datos nominales**, donde no hay métrica | La construcción es **voraz**: cada corte se elige mirando sólo el nodo actual |
| **Clasificación rapidísima**: $O(\log n)$ | **Efecto horizonte** si se usa parada en vez de poda |
| No exigen que los atributos sean numéricos ni comparables entre sí | Los cortes axiales **no se llevan bien con fronteras oblicuas** |
| Manejan **datos faltantes** de forma natural (sustitutos) | Tendencia al **sobre-ajuste** si no se poda |
| Admiten **costos y priors** directamente en la impureza | Malos para **inferir conceptos simples** que involucran muchos atributos a la vez (por ejemplo «¿más de la mitad de los atributos vale +1?») |
| Lugar natural para meter **conocimiento del experto** | Entrenar es **caro** comparado con clasificar |

> **PARA LA DEFENSA — dónde se ubican frente a lo demás**
> La conclusión de Duda: los árboles dan una exactitud **comparable** a la de las redes neuronales y a la del vecino más cercano, **sobre todo cuando no hay información previa sobre qué forma debería tener el clasificador**. Y son particularmente útiles con **datos no métricos**, que es el terreno donde los otros directamente no juegan.

---

## 15. Para la pizarra

### Guion — «Explicá los árboles de decisión»

**Paso 1 — Empezás por el problema, no por el árbol.** *«Todos los métodos que vimos suponen que los patrones son vectores reales y que hay una distancia. Con datos nominales —los dientes de un animal, el color de una fruta— esa distancia no existe.»* Ahí te ganaste el derecho a presentar otro método.

**Paso 2 — Dibujás el árbol de las frutas** y nombrás las piezas: raíz, ramas excluyentes y exhaustivas, nodos de decisión, hojas con etiqueta. Mostrás cómo baja un patrón.

**Paso 3 — Decís la ventaja que los distingue**, y las dos formas: la regla de un patrón (la conjunción del camino) y la descripción de una clase entera.

**Paso 4 — Planteás el problema de construirlo** y enunciás **las seis preguntas de CART**. Decís que vas a desarrollar la segunda.

**Paso 5 — La impureza.** Escribís qué se le pide ($0$ si es puro, máxima si están parejas), escribís **entropía y Gini**, y decís qué es $P(\omega_j)$ — *la fracción de patrones de ese nodo*, no una probabilidad de la población. **Ésta es la trampa más común del tema.**

**Paso 6 — La decisión.** Escribís $\Delta i(T)$ y decís la frase: *«se elige la pregunta que más baja la impureza, ponderando los hijos por la fracción de patrones que va a cada uno»*. Si usás entropía, eso **es** la ganancia de información.

**Paso 7 (el remate).** Dos cosas, en este orden: que la **elección de la medida casi no cambia el resultado**, y que lo que sí importa es **la parada y la poda**. Y si querés cerrar con algo que se nota: el ejemplo 90/10 donde la impureza de clasificación no ve un corte que Gini sí ve.

---

## 16. Formulario

| Qué | Fórmula |
|---|---|
| Impureza de entropía | $i(N) = -\sum_j P(\omega_j)\log_2 P(\omega_j)$ |
| Impureza de varianza (2 clases) | $i(N) = P(\omega_1)P(\omega_2)$ |
| Impureza de Gini | $i(N) = \sum_{i\neq j}P(\omega_i)P(\omega_j) = 1 - \sum_j P^2(\omega_j)$ |
| Impureza de clasificación | $i(N) = 1 - \max_j P(\omega_j)$ |
| Caída de impureza | $\Delta i(T) = i(N) - P_L\,i(N_L) - (1-P_L)\,i(N_R)$ |
| Gini ponderada por costos | $i(N) = \sum_{ij}\lambda_{ij}P(\omega_i)P(\omega_j)$ |
| Criterio de complejidad | $\sum_{\text{hojas}} i(N) + \alpha\,\text{tamaño}$ |
| Nodo multivariado | ¿es $\sum_i w_i x_i < w_0$? |
| Complejidad de clasificación | $O(\log n)$ |
| Complejidad de entrenamiento | $O(d\,n\,(\log n)^2)$ |

---

## 17. Errores típicos

| Error | Lo correcto |
|---|---|
| Decir que $P(\omega_j)$ es la probabilidad a priori de la clase | Es **la fracción de patrones de ese nodo** que son de esa clase |
| Comparar impurezas de los hijos sin ponderar | Van pesadas por la **fracción de patrones** que va a cada hijo |
| Usar la tasa de error como criterio de corte | Es ciega a cortes útiles: el ejemplo 90/10. Por eso Gini o entropía |
| Decir que Gini y entropía dan árboles muy distintos | En la práctica la medida casi no cambia el resultado; lo que cambia es parada y poda |
| Confundir parar con podar | Parar es **pre**-poda y sufre el efecto horizonte; podar crece entero y después fusiona |
| Decir que el árbol es estable porque es determinista | Es determinista **y** muy inestable: un punto distinto puede cambiar el árbol entero |
| Decir que los árboles son lentos | **Entrenar** es caro; **clasificar** es de lo más rápido que hay, $O(\log n)$ |
| Creer que un árbol necesita atributos numéricos | Es justamente al revés: su terreno son los datos **nominales** |

---

## 18. Autoevaluación

1. ¿Por qué el perceptrón o el vecino más cercano no sirven para el problema de los dientes? ¿Qué supuesto se rompe?
2. Dibujá un árbol chiquito y nombrá todas sus partes. ¿Qué condición tienen que cumplir las ramas de un nodo?
3. Escribí la regla que clasifica un patrón concreto de tu árbol, y la descripción lógica de una de sus clases.
4. Enumerá las seis preguntas de CART.
5. ¿Por qué alcanza con árboles binarios?
6. ¿Qué propiedad se le exige a una función de impureza? Escribí entropía y Gini.
7. En un nodo con 30 patrones (20 de $\omega_1$ y 10 de $\omega_2$), calculá Gini y la impureza de clasificación.
8. Escribí $\Delta i(T)$ y explicá por qué los hijos van ponderados.
9. Con el nodo 90/10: mostrá un corte que la impureza de clasificación no distingue y Gini sí. ¿Qué significa que Gini «anticipa»?
10. ¿Qué es el efecto horizonte y cuál es el remedio?
11. ¿Qué gana la poda de reglas frente a la poda de nodos?
12. ¿Qué es un corte sustituto y cómo se elige? ¿Cómo resuelve C4.5 el mismo problema?
13. ¿Por qué un árbol es inestable? Nombrá la causa de fondo.
14. ¿Cómo se incorporan costos distintos por tipo de error?
15. Escribí tres ventajas y tres desventajas, y decí en qué terreno un árbol le gana a una red neuronal.
