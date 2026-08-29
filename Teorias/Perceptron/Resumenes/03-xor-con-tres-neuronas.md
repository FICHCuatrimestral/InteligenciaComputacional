---
title: "El XOR resuelto con tres neuronas"
subtitle: "Inteligencia Computacional · FICH-UNL · Diego Milone \\newline Guía de estudio — diapositivas 1--29 de *Perceptrón multicapa*, clases 006 a 008"
lang: es
---

*Se arma **a mano** la primera red neuronal: tres perceptrones que resuelven el XOR. Todavía no hay aprendizaje — primero se muestra que la solución **existe**, y recién después se busca cómo encontrarla sola. Viene de `02-metodos-de-gradiente.md` y sigue en `04-perceptron-multicapa.md`.*

---

## 1. El problema y la idea

Con codificación bipolar, el **o exclusivo** da $+1$ cuando exactamente una entrada es verdadera:

| $x_1$ | $x_2$ | XOR |
|:---:|:---:|:---:|
| $-1$ | $-1$ | $-1$ |
| $-1$ | $+1$ | $+1$ |
| $+1$ | $-1$ | $+1$ |
| $+1$ | $+1$ | $-1$ |

![Se ponga donde se ponga la recta, siempre queda un patrón del lado equivocado.](imagenes/01-xor-no-separable.png)

Ya sabemos por qué falla —un perceptrón simple decide con una recta y el XOR **no es linealmente separable**; la demostración está en `01` §5 y en `02` §7—. Lo nuevo es la salida:

> **La idea.** Dos perceptrones definen cada uno un semiplano; **un tercero se queda con la franja donde se intersecan**. Adentro, los dos casos verdaderos; afuera, los dos falsos.

Funciona por cómo está armado el XOR: los dos patrones que dan $+1$ están **sobre la diagonal** $x_1+x_2=0$, y los dos que dan $-1$ están uno a cada lado ($x_1+x_2 = \pm 2$). Entonces alcanzan **dos rectas paralelas de pendiente $-1$**, una de cada lado, que dejen la diagonal encerrada.

---

## 2. La herramienta: de la recta a los pesos

Ubicar las rectas en el dibujo es fácil. Lo que hay que saber hacer es **traducir una recta a pesos**, porque los pesos son lo único que existe en la red. Es la fórmula que se usa tres veces.

Partiendo de la frontera $\langle w, x\rangle = 0$ con $x_0 = -1$:

$$
w_0(-1) + w_1 x_1 + w_2 x_2 = 0
\qquad\Longrightarrow\qquad
\boxed{\;x_2 = \frac{w_0}{w_2} \;-\; \frac{w_1}{w_2}\,x_1\;}
$$

Leído como $x_2 = b + m\,x_1$:

$$
\text{ordenada al origen } b = \frac{w_0}{w_2}
\qquad\qquad
\text{pendiente } m = -\frac{w_1}{w_2}
$$

**El método:** se lee del gráfico la ordenada y la pendiente que se necesitan, se plantean esos dos cocientes, y se elige cualquier terna que los cumpla.

> **IDEA DE FONDO — los pesos no son únicos**
> Fijate qué aparece: **sólo cocientes**. Dos condiciones, tres incógnitas, queda un grado de libertad — la **escala** del vector. Verificado numéricamente:
>
> ```
>   factor   1.0: pesos [-1.  1.  1.]  ->  yA = [-1, 1, 1, 1]
>   factor   7.0: pesos [-7.  7.  7.]  ->  yA = [-1, 1, 1, 1]
>   factor  0.25: pesos [-0.25  0.25  0.25]  ->  yA = [-1, 1, 1, 1]
> ```
>
> Eso explica algo de la unidad anterior: por qué dos entrenamientos con inicializaciones distintas terminan en pesos distintos y **ambos correctos**. La solución no es un punto, es una **familia de vectores**.

> **OJO — vale para múltiplos positivos, no para cualquiera**
> Con un factor **negativo** la recta es idéntica pero la neurona clasifica **al revés**:
>
> ```
>   factor   1.0: pesos [-1.  1.  1.]  ->  yA = [-1,  1,  1,  1]
>   factor  -1.0: pesos [ 1. -1. -1.]  ->  yA = [ 1, -1, -1, -1]
> ```
>
> O sea: **la recta fija la dirección de $w$; el signo fija de qué lado está el $+1$.** Si te dan una recta y te piden los pesos, tenés que decidir también el sentido.

### Claves de la sección 2

| Clave | Qué tenés que poder responder |
|---|---|
| La fórmula | Deducirla desde $\langle w,x\rangle=0$ |
| $b$ y $m$ | Qué cociente da cada uno |
| No unicidad | Cuántas condiciones, cuántas incógnitas, qué queda libre |
| El signo | Qué cambia al multiplicar $w$ por un negativo |

---

## 3. Las dos neuronas de la primera capa

Se aplica la fórmula de la sección 2 dos veces, a dos rectas paralelas de pendiente $-1$ que dejan la diagonal en el medio: una que corta en $-1$ y otra en $+1$.

![Las dos rectas son paralelas y sólo difieren en el corrimiento. En el panel de B queda punteada la recta de A, para ver el desplazamiento.](imagenes/30-rectas-a-y-b.png)

| | Recta | Cocientes | Pesos | Qué calcula |
|:---:|---|---|---|---|
| **A** | $x_1+x_2 = -1$ | $\frac{w_0}{w_2}=-1$, $\frac{w_1}{w_2}=+1$ | $w_A = [-1,\,+1,\,+1]^{T}$ | $y_A = \mathrm{sgn}(x_1+x_2+1)$ |
| **B** | $x_1+x_2 = +1$ | $\frac{w_0}{w_2}=+1$, $\frac{w_1}{w_2}=+1$ | $w_B = [+1,\,+1,\,+1]^{T}$ | $y_B = \mathrm{sgn}(x_1+x_2-1)$ |

En palabras: **A suma las dos entradas y le agrega 1; B suma las dos entradas y le resta 1.** Las dos devuelven el signo.

| $(x_1,x_2)$ | $x_1{+}x_2{+}1$ | $y_A$ | $x_1{+}x_2{-}1$ | $y_B$ |
|:---:|:---:|:---:|:---:|:---:|
| $(-1,-1)$ | $-1$ | $-1$ | $-3$ | $-1$ |
| $(-1,+1)$ | $+1$ | $+1$ | $-1$ | $-1$ |
| $(+1,-1)$ | $+1$ | $+1$ | $-1$ | $-1$ |
| $(+1,+1)$ | $+3$ | $+1$ | $+1$ | $+1$ |

> **IDEA DE FONDO — el sesgo es lo único que cambia**
> $w_A$ y $w_B$ tienen **idénticos $w_1$ y $w_2$** y difieren **sólo en $w_0$**. Los pesos de las entradas fijan la *orientación* de la recta; el sesgo fija su *corrimiento*. Dos neuronas con la misma orientación y distinto sesgo generan una franja — que es exactamente lo que hace falta.
> Es el argumento más directo de por qué sin sesgo esto sería imposible: ambas rectas pasarían por el origen, serían la misma, y no habría franja.

> **OJO — ninguna de las dos resuelve nada por su cuenta**
> A da $+1$ también para $(+1,+1)$, que debería dar $-1$. En clase se lo llama *"una fase, una parte de la resolución"*. Si te preguntan qué aprende una neurona oculta, la respuesta no es "media función XOR": es **una pregunta binaria sobre la entrada**.

### Claves de la sección 3

| Clave | Qué tenés que poder responder |
|---|---|
| $w_A$ y $w_B$ | Los pesos y de qué cocientes salen |
| En palabras | Qué operación hace cada neurona |
| Rol de $w_0$ | Qué controla el sesgo frente a $w_1,w_2$ |
| Sin sesgo | Por qué la construcción se caería |

---

## 4. Las tres franjas y lo que tiene que hacer C

Como las rectas son paralelas y B está por encima de A, el plano queda en **tres bandas**, cada una con su **código** $(y_A, y_B)$:

![Los dos patrones verdaderos quedan encerrados en la franja del medio.](imagenes/04-tres-franjas.png)

| Región | $y_A$ | $y_B$ | Patrón | $y_C$ deseada |
|---|:---:|:---:|---|:---:|
| arriba de ambas | $+1$ | $+1$ | $(+1,+1)$ | $-1$ |
| **franja del medio** | $+1$ | $-1$ | $(-1,+1)$ y $(+1,-1)$ | $+1$ |
| abajo de ambas | $-1$ | $-1$ | $(-1,-1)$ | $-1$ |
| — | $-1$ | $+1$ | **nunca ocurre** | **X** |

> **IDEA DE FONDO — por qué hay una X**
> $y_A=-1$ con $y_B=+1$ querría decir "estoy **debajo** de A pero **encima** de B". Como B está por arriba de A, esa región **no existe**: *"nunca se forman regiones con esa intersección"*. Va una **X — don't care**: la salida de C ahí es irrelevante.
> Contable: de $2^2=4$ códigos posibles, la capa oculta genera **sólo 3**.

> **IDEA DE FONDO — la capa oculta cambia la representación**
> Éste es *el* concepto de toda la unidad. El problema sigue siendo linealmente inseparable en el plano $(x_1,x_2)$ y siempre lo va a ser. Pero en el plano $(y_A, y_B)$ **los tres códigos alcanzables sí son separables**, y ahí un perceptrón simple común lo termina.
> Cada neurona oculta responde una pregunta binaria; el vector de respuestas es una **codificación nueva** del patrón, una en la que el problema ya es fácil.

Notá además que dos patrones distintos —$(-1,+1)$ y $(+1,-1)$— **comparten código**. La capa oculta los volvió indistinguibles, y está bien: la función pide lo mismo para los dos.

### Claves de la sección 4

| Clave | Qué tenés que poder responder |
|---|---|
| Las tres franjas | Cuáles son y qué código tiene cada una |
| El *don't care* | Por qué esa combinación es geométricamente imposible |
| Cambio de representación | Por qué el problema sí se resuelve en el plano oculto |

---

## 5. El perceptrón C

Tercera aplicación de la misma fórmula, pero **en el plano oculto**: las entradas de C ya no son $x_1,x_2$ sino $y_A,y_B$.

![Los tres códigos alcanzables, ahora sí separables por una recta.](imagenes/05-plano-oculto.png)

En el apunte de cátedra este plano se dibuja con **$y_B$ en el eje horizontal y $y_A$ en el vertical**, y la recta se escribe $y_A = +1 + y_B$ — ordenada $+1$, pendiente $+1$. De ahí:

$$
\frac{w_{C0}}{w_{C2}} = +1
\qquad
-\frac{w_{C1}}{w_{C2}} = +1
\qquad\Longrightarrow\qquad
w_C = \begin{bmatrix} +1 \\ -1 \\ +1 \end{bmatrix}
\qquad
y_C = \mathrm{sgn}(y_A - y_B - 1)
$$

En palabras: **toma la salida de A, le resta la de B, le resta 1, y devuelve el signo.**

| $y_A$ | $y_B$ | $y_A - y_B - 1$ | $y_C$ | ¿cierra? |
|:---:|:---:|:---:|:---:|:---:|
| $+1$ | $-1$ | $+1$ | $+1$ | sí |
| $+1$ | $+1$ | $-1$ | $-1$ | sí |
| $-1$ | $-1$ | $-1$ | $-1$ | sí |
| $-1$ | $+1$ | $-3$ | $-1$ | *don't care* |

> **OJO — el orden de los subíndices de $w_C$ es una trampa**
> $w_{C1}$ y $w_{C2}$ están numerados según **los ejes del gráfico del plano oculto**, donde el eje 1 (horizontal) es $y_B$ y el eje 2 (vertical) es $y_A$. Por eso aparece $w_{C1}=-1$ y sin embargo la ecuación queda $\mathrm{sgn}(y_A - y_B - 1)$: el $-1$ le corresponde a **$y_B$**.
> En el diagrama de la red no hay ambigüedad: **A→C pesa $+1$ y B→C pesa $-1$**. Si te confundís, guiate por el diagrama, no por los subíndices.

### Claves de la sección 5

| Clave | Qué tenés que poder responder |
|---|---|
| Recta de C | Ordenada, pendiente, y en qué plano vive |
| $w_C$ | Los tres pesos |
| En palabras | Qué operación hace C |
| Subíndices | Por qué $w_{C1}=-1$ corresponde a $y_B$ |

---

## 6. La red completa

![Los nueve pesos. Las dos entradas $-1$ son la misma convención de sesgo aplicada en cada capa.](imagenes/06-arquitectura.png)

| Conexión | Peso | | Conexión | Peso |
|---|:---:|---|---|:---:|
| $x_1 \to A$ | $+1$ | | $x_1 \to B$ | $+1$ |
| $x_2 \to A$ | $+1$ | | $x_2 \to B$ | $+1$ |
| $x_0 \to A$ | $-1$ | | $x_0 \to B$ | $+1$ |
| $A \to C$ | $+1$ | | $B \to C$ | $-1$ |
| $x_0 \to C$ | $+1$ | | | |

$$
\left.
\begin{aligned}
y_A &= \mathrm{sgn}(x_1 + x_2 + 1) \\
y_B &= \mathrm{sgn}(x_1 + x_2 - 1)
\end{aligned}
\right\}
\;\Longrightarrow\;
y_C = \mathrm{sgn}(y_A - y_B - 1)
$$

### Verificación

Un caso a mano, el $(-1,-1)$:

$$
\langle w_A, x\rangle = \underbrace{(-1)(-1)}_{\text{sesgo}} + (+1)(-1) + (+1)(-1) = +1 -1 -1 = -1 \;\Rightarrow\; y_A = -1
$$
$$
\langle w_B, x\rangle = (+1)(-1) + (+1)(-1) + (+1)(-1) = -3 \;\Rightarrow\; y_B = -1
$$
$$
y = \mathrm{sgn}\big[(+1)(-1) + (-1)(-1) + (-1)(-1)\big] = \mathrm{sgn}(-1) = -1 \quad\checkmark
$$

> **OJO — el signo del sesgo es donde se equivoca todo el mundo**
> El sesgo aporta $w_0 \cdot x_0 = w_0 \cdot (-1) = -w_0$. O sea que **un peso de sesgo positivo resta y uno negativo suma**. En A, con $w_{A0}=-1$, el término vale $+1$; en B, con $w_{B0}=+1$, vale $-1$.

Los cuatro casos, por programa (`imagenes/verificacion_red_xor.py`):

```
  x1  x2 |   vA  yA |   vB  yB |   vC   y |   d  ok
--------------------------------------------------------
  -1  -1 |   -1  -1 |   -3  -1 |   -1  -1 |  -1  True
  -1   1 |    1   1 |   -1  -1 |    1   1 |   1  True
   1  -1 |    1   1 |   -1  -1 |    1   1 |   1  True
   1   1 |    3   1 |    1   1 |   -1  -1 |  -1  True
```

> **IDEA DE FONDO — dos de los cuatro casos son el mismo**
> Las filas $(-1,+1)$ y $(+1,-1)$ son **idénticas columna por columna**. La razón: en la primera capa **todos los pesos de entrada valen $+1$**, así que A y B reciben $x_1+x_2$ y no distinguen de cuál entrada vino cada valor.
> No es casualidad del ejemplo: es una **simetría de la red**. El XOR es simétrico en sus argumentos y se lleva bien con eso — pero si el problema **no** fuera simétrico, esos pesos iguales serían una limitación grave.

> **PARA LA DEFENSA — las tres cosas que hay que decir**
> 1. **La neurona de salida no es un mecanismo nuevo**: es el mismo perceptrón simple, sobre entradas transformadas.
> 2. **Las regiones dejan de ser semiplanos**: al intersecarlos aparecen regiones convexas, y con más capas, arbitrarias.
> 3. **Acá todavía no hay aprendizaje.** Todo se diseñó a mano. La pregunta abierta —¿cómo encuentra la red estos pesos sola, si nadie dice cuál era la salida deseada de A o de B?— es la que responde **back-propagation**.

> **PARA LA DEFENSA — qué la hace una red**
> No la cantidad de neuronas: que **la salida de unas sea la entrada de otras**. Tres perceptrones en paralelo, sin conectarse, seguirían dando tres fronteras lineales independientes y ninguno resolvería el XOR. Es la **composición** la que produce la frontera no lineal.

### Claves de la sección 6

| Clave | Qué tenés que poder responder |
|---|---|
| El diagrama | Dibujar la red con los nueve pesos, de memoria |
| El sesgo | Cuántas entradas $x_0=-1$ hay y qué signo aporta |
| Verificación | Rehacer un caso a mano |
| La simetría | Por qué dos patrones dan lo mismo en toda la red |
| Red vs. perceptrones | Qué la hace una red |

---

## 7. Lo que viene

En `04-perceptron-multicapa.md`: qué regiones puede formar cada arquitectura, la notación matricial general, el cambio de $\mathrm{sgn}$ por la sigmoide, y **back-propagation** — el método del gradiente extendido para que la red encuentre sola estos pesos.

---

## Formulario

| Expresión | Qué es |
|---|---|
| $x_2 = \frac{w_0}{w_2} - \frac{w_1}{w_2}x_1$ | **la frontera en función de los pesos** |
| $w_A = [-1,\,+1,\,+1]^{T}$ | $y_A = \mathrm{sgn}(x_1+x_2+1)$ |
| $w_B = [+1,\,+1,\,+1]^{T}$ | $y_B = \mathrm{sgn}(x_1+x_2-1)$ |
| $w_C = [+1,\,-1,\,+1]^{T}$ | $y_C = \mathrm{sgn}(y_A-y_B-1)$, con el eje 1 $=y_B$ |
| $(y_A, y_B)$ | código de la capa oculta: 3 alcanzables de 4 |

## Errores típicos

- Decir que el perceptrón simple "no aprende" el XOR. **No existe solución.**
- Pensar que cada neurona oculta resuelve media función. Resuelven **una pregunta binaria**.
- Inventarle un valor a la **X** de la tabla. Es un *don't care* con razón geométrica.
- Confundir los planos: A y B viven en $(x_1,x_2)$; C en $(y_A,y_B)$.
- Creer que los pesos son únicos. Sólo importan **los cocientes**; queda libre la escala positiva.
- Asignarle a $y_A$ el peso $w_{C1}=-1$ por el subíndice. En el plano oculto el eje 1 es $y_B$.
- Copiar el sesgo con el signo del peso. Aporta $-w_0$.
- Creer que esto salió de un entrenamiento. **Está diseñado a mano.**

## Autoevaluación

1. ¿Por qué alcanzan dos rectas paralelas, y por qué de pendiente $-1$?
2. Deducí $x_2 = \frac{w_0}{w_2} - \frac{w_1}{w_2}x_1$ desde $\langle w,x\rangle=0$.
3. Te dan la recta $x_2 = 2 - 3x_1$: proponé dos vectores de pesos distintos que la generen con la misma clasificación.
4. Obtené $w_A$ y $w_B$ desde sus rectas, sin mirar.
5. Explicá en una frase por qué la fila $(-1,+1)$ lleva una X.
6. ¿En qué espacio el problema se volvió separable, y por qué eso no contradice que el XOR no lo sea?
7. Dibujá la red completa con sus nueve pesos.
8. Calculá a mano el caso $(+1,+1)$ y comprobá que da $-1$.
9. ¿Por qué $(-1,+1)$ y $(+1,-1)$ dan idéntico en toda la red?
10. ¿Qué hace que esto sea una red y no tres perceptrones sueltos?
11. ¿Qué información le falta a la red para aprender estos pesos sola?
