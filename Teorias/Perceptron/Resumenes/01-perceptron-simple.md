---
title: "El perceptrón simple"
subtitle: "Inteligencia Computacional · FICH-UNL · Diego Milone \\newline Guía de estudio — diapositivas 1--39 de *Perceptrón simple*, clases 001 a 004"
lang: es
---

*De la neurona biológica al primer algoritmo de aprendizaje. Sigue en `02-metodos-de-gradiente.md`.*

---

## 1. Qué se copia de la biología, y qué no

La neurona real tiene tres partes que interesan:

- **dendritas** — por donde entra la información, desde otras neuronas o desde sensores;
- **cuerpo neuronal** — donde se acumulan los estímulos;
- **axón** — la salida, una sola.

Las conexiones de entrada (las **sinapsis**) no pesan todas igual: algunas son **excitatorias** y empujan a la neurona a activarse, otras son **inhibitorias** y la frenan, y cada una puede ser fuerte o débil. Cuando la carga acumulada supera un **umbral**, la membrana se despolariza y sale **un único pulso** por el axón. Si no llega al umbral, no sale nada.

Eso último —**todo o nada**— es la propiedad que se modela.

> **IDEA DE FONDO — dónde vive el aprendizaje**
> Aprender, en el cerebro, es **modificar las sinapsis**: que algunas débiles se vuelvan fuertes, que otras se debiliten, que algunas se desconecten. La neurona no cambia; cambian sus conexiones.
> Eso es exactamente lo que va a hacer el algoritmo: **lo único que se toca son los pesos**.

**Lo que el modelo deja afuera**, y conviene saber que se deja afuera:

- **la dinámica temporal.** En la neurona real los estímulos llegan en momentos distintos; en el modelo se supone que **todas las entradas llegan a la vez** y que la evaluación es instantánea.
- **la mecánica de la despolarización**, los neurotransmisores, la propagación del impulso. Nada de eso aparece.

### Claves de la sección 1

| Clave | Qué tenés que poder responder |
|---|---|
| Las tres partes | Dendritas, cuerpo, axón: qué hace cada una |
| Excitatoria / inhibitoria | Qué significa y cómo se representa después |
| Todo o nada | Qué propiedad se modela y cuál se descarta |
| Dónde está el aprendizaje | Qué cambia cuando una red aprende |

---

## 2. El modelo

![Las entradas se ponderan, se suman, y el resultado pasa por la función de activación.](imagenes/26-modelo-neurona.png)

Cada entrada $x_i$ tiene un **peso sináptico** $w_i$, que es un número real: **positivo** si la conexión es excitatoria, **negativo** si es inhibitoria, **cero** si no hay conexión. El cuerpo neuronal hace dos cosas:

1. la **suma ponderada** de las entradas, $v = \sum w_i x_i$;
2. compara contra un **umbral** $u$: si lo supera, dispara.

### El truco del sesgo

Comparar contra un umbral es incómodo. Se lo pasa restando al otro lado:

$$
\sum_{i=1}^{N} w_i x_i > u
\qquad\Longleftrightarrow\qquad
\sum_{i=1}^{N} w_i x_i - u > 0
$$

Y ahora el paso que ordena todo: se escribe $-u$ como **una entrada más**, fija en $x_0 = -1$, con su propio peso $w_0 = u$. Así el umbral entra en la sumatoria y desaparece de la comparación:

$$
\boxed{\;y = \varphi\left(\sum_{i=0}^{N} w_i x_i\right) = \varphi\big(\langle w, x\rangle\big)\;}
\qquad\text{con } x_0 = -1
$$

Fijate que la sumatoria ahora arranca en $\mathbf{0}$ y no en 1: ése es el único rastro del cambio.

> **IDEA DE FONDO — por qué conviene tanto**
> Con la entrada extendida, el umbral **deja de ser un caso aparte**: es un peso más, se guarda como los demás y —lo importante— **se aprende como los demás**, con la misma fórmula. Si lo dejaras afuera, el algoritmo de aprendizaje necesitaría una regla especial sólo para él.
> Y de paso, el modelo entero queda escrito como **un producto interno**: dos vectores adentro, un escalar afuera. Ese escalar es el nivel de activación de la neurona.

$w_0$ aparece en la bibliografía como **umbral**, **sesgo** o **bias**: son la misma cosa.

### Claves de la sección 2

| Clave | Qué tenés que poder responder |
|---|---|
| Peso sináptico | Qué significa su signo y su magnitud |
| Las dos operaciones | Qué hace el cuerpo neuronal, en orden |
| La entrada extendida | Cómo se pasa de $>u$ a $>0$, y qué vale $x_0$ |
| Por qué conviene | Dos motivos: se aprende igual, y queda un producto interno |
| $u$, $w_0$, sesgo, bias | Que son la misma cosa |

---

## 3. Funciones de activación

$\varphi$ es la que convierte la activación lineal $v$ en la salida. Todas las de esta materia van entre $-1$ y $+1$.

![La misma forma en $S$, con tres niveles de suavidad.](imagenes/27-funciones-activacion.png)

$$
\mathrm{sgn}(v) = \begin{cases} +1 & v \ge 0 \\ -1 & v < 0\end{cases}
\qquad
\mathrm{sig}(v) = \frac{2}{1+e^{-a v}} - 1
$$

La **función signo** es el todo-o-nada literal. La **lineal a tramos** le agrega una zona de transición con pendiente $\alpha$. La **sigmoide** es la misma forma sin ninguna discontinuidad, y su parámetro $a$ controla la pendiente: cuanto más grande, más se parece al signo.

> **PARA LA DEFENSA — por qué importa la sigmoide**
> No es una cuestión estética. **La sigmoide es derivable en todo punto y el signo no**, y todo el método del gradiente exige derivar la función de activación. Con $a$ grande se recupera el comportamiento todo-o-nada de la neurona biológica **sin pagar el precio de la discontinuidad**.
> Es la razón por la que el perceptrón multicapa la usa y el perceptrón simple no la necesita.

> **OJO — las dos sigmoides de la bibliografía**
> Algunos libros usan una sigmoide entre $0$ y $1$ en vez de entre $-1$ y $+1$. Las dos son correctas —es convención—, pero **si mezclás fórmulas de un libro y otro no cierra nada**: cambian la derivada y la codificación de las salidas. Lo mismo con la codificación de las clases: hay textos con $\{0,1\}$ y otros con $\{-1,+1\}$. Acá se usa siempre **bipolar**, $\pm 1$.

Existen otras (gaussiana, sinusoidal) que aparecen más adelante en la materia.

### Claves de la sección 3

| Clave | Qué tenés que poder responder |
|---|---|
| Las tres | Nombrarlas y dibujarlas |
| El parámetro | Qué controla $a$ en la sigmoide |
| El motivo real | Por qué se necesita una función derivable |
| Bibliografía | Qué dos convenciones no hay que mezclar |

---

## 4. Qué puede decidir una neurona

Con dos entradas, la salida es $y = \mathrm{sgn}(w_1x_1 + w_2x_2)$ y lo interesante es la **frontera**: el lugar donde la suma ponderada vale exactamente cero, porque un poquito más y la neurona se activa, un poquito menos y no.

$$
w_1x_1 + w_2x_2 = 0
\qquad\Longrightarrow\qquad
x_2 = -\frac{w_1}{w_2}\,x_1
$$

**Es la ecuación de una recta**, y como no tiene término independiente, **pasa por el origen**. Los pesos fijan su pendiente.

Esa recta parte el plano en dos **semiplanos**: en todo uno la neurona da $+1$, en todo el otro da $-1$. Eso es todo lo que una neurona puede decidir.

> **IDEA DE FONDO — el caso general**
> Con $N$ entradas la frontera $\langle w,x\rangle = 0$ es un **hiperplano en $\mathbb{R}^N$**. Con 2 entradas es una recta, con 3 un plano, con 28 un hiperplano en $\mathbb{R}^{28}$.
> Y no es un ejemplo forzado: si la entrada fuera una imagen de $1024\times1024$ y cada píxel una entrada, la neurona estaría trazando un hiperplano en $\mathbb{R}^{1\,000\,000}$.

Un problema que se puede resolver así se llama **linealmente separable**.

### Claves de la sección 4

| Clave | Qué tenés que poder responder |
|---|---|
| La frontera | Qué ecuación la define y por qué esa zona es la interesante |
| Recta por el origen | Por qué no tiene ordenada al origen |
| Semiplanos | Qué decide la neurona en cada uno |
| Caso general | Qué es la frontera con $N$ entradas |
| Separabilidad lineal | Qué quiere decir |

---

## 5. El sesgo: sin él no se resuelve ni el OR

Probemos con el OR, codificado en bipolar: da $+1$ salvo cuando las dos entradas son falsas.

| $x_1$ | $x_2$ | OR |
|:---:|:---:|:---:|
| $-1$ | $-1$ | $-1$ |
| $-1$ | $+1$ | $+1$ |
| $+1$ | $-1$ | $+1$ |
| $+1$ | $+1$ | $+1$ |

![Con la recta anclada al origen siempre falla uno; corriéndola, se resuelve.](imagenes/28-or-y-sesgo.png)

Con una recta que pasa por el origen, se la incline como se la incline, **siempre queda un patrón del lado equivocado**. La solución es despegarla del origen, y eso es exactamente lo que hace $w_0$:

$$
w_1x_1 + w_2x_2 - w_0 = 0
\qquad\Longrightarrow\qquad
x_2 = \frac{w_0}{w_2} - \frac{w_1}{w_2}\,x_1
$$

Ahora hay **ordenada al origen**, y vale $w_0 / w_2$. Con $w_1 = w_2 = 1$ y $w_0 = -1$ queda la recta $x_1 + x_2 = -1$, que resuelve el OR.

> **PARA LA DEFENSA — la demostración en una línea**
> Que "siempre falla uno" se puede *demostrar*, no sólo mostrar. Una recta que pasa por el origen deja **dos puntos opuestos siempre en semiplanos distintos** —si $x$ está de un lado, $-x$ está del otro—.
> Ahora mirá el OR: los patrones $(-1,+1)$ y $(+1,-1)$ son opuestos, y los dos tienen que dar $+1$, o sea que necesitan estar del **mismo** lado. Imposible sin sesgo.

> **OJO — el caso degenerado, y por qué no cuenta**
> Hay una escapatoria: poner la recta *justo encima* de esos dos puntos, sobre la diagonal $x_1+x_2=0$. Ahí el producto interno da exactamente cero, y como la convención es $\mathrm{sgn}(0)=+1$, los dos salen $+1$ y parece que funciona.
> No cuenta, por dos razones: depende de una **convención arbitraria** sobre el valor en cero, y es **infinitamente frágil** — mové un peso una milésima y se rompe. Los patrones quedan sobre la frontera, que es el peor lugar posible.

**Conclusión operativa:** toda neurona de toda red lleva su sesgo. Sin él, ni siquiera el OR.

### Claves de la sección 5

| Clave | Qué tenés que poder responder |
|---|---|
| El OR | La tabla en bipolar |
| El fracaso | Por qué ninguna recta por el origen sirve |
| La demostración | El argumento de los puntos opuestos |
| El caso degenerado | Cuál es y por qué no vale |
| La ordenada | Qué cociente la da |

---

## 6. Cómo aprende: corrección de error

Hasta acá los pesos los pusimos nosotros mirando el dibujo. La idea de una red neuronal es otra: **mostrarle ejemplos y que los pesos salgan solos**.

El archivo de entrenamiento tiene, en cada línea, las entradas y **la salida que debería dar**. Y no son sólo los cuatro casos perfectos: puede haber $(+0{,}9;\ +1{,}1)$ con salida deseada $+1$, o $(-0{,}7;\ -1{,}1)$ con salida $-1$. Casos con ruido, que es lo que hay en el mundo real.

El algoritmo:

**1. Inicialización.** Los pesos arrancan **al azar y chicos**, por ejemplo en $[-0{,}5;\ +0{,}5]$.

**2. Para cada ejemplo**, se calcula la salida $y(n) = \varphi\big(\langle w(n), x(n)\rangle\big)$ y:

- **Si acertó** ($y = d$): **no se toca nada.** Es el **principio de mínima perturbación**.
- **Si erró**: se **penaliza**, moviendo los pesos *en el sentido opuesto al que contribuyeron al error*.

Desarmemos la penalización. Supongamos entradas positivas:

- Dio $+1$ y tenía que dar $-1$ → la suma ponderada tiene que **bajar** → hay que **restar** una proporción de las entradas: $w(n+1) = w(n) - \eta\,x(n)$.
- Dio $-1$ y tenía que dar $+1$ → tiene que **subir** → **sumar**: $w(n+1) = w(n) + \eta\,x(n)$.

### La misma regla, vista como geometría

![Sumar acerca el vector de pesos a la entrada; restarlo lo aleja. Como la frontera es perpendicular a $w$, mover $w$ la hace girar.](imagenes/29-geometria-correccion.png)

Hay una forma de ver la regla que la vuelve obvia, y conviene tenerla porque es lo que se dibuja en la pizarra.

Acordate de que la frontera $\langle w, x\rangle = 0$ es **el conjunto de puntos perpendiculares a $w$**. O sea: **el vector de pesos apunta hacia el semiplano donde la neurona da $+1$**, y la frontera es la recta que lo cruza en ángulo recto.

Entonces la regla es sólo esto:

- **Faltó activarse** ($d=+1$, $y=-1$): $x$ está del lado equivocado, el ángulo entre $w$ y $x$ pasa de $90°$. Sumar $\eta\,x$ **acerca $w$ a $x$**, achica ese ángulo, y el producto interno se vuelve positivo.
- **Se activó de más** ($d=-1$, $y=+1$): al revés. Restar $\eta\,x$ **aleja $w$ de $x$**, el ángulo pasa de $90°$ y el producto interno se vuelve negativo.

> **IDEA DE FONDO — mover el vector es girar la recta**
> Los pesos y la frontera son la misma cosa vista de dos maneras. Cuando el algoritmo mueve $w$ un poquito, la frontera **gira** —porque siempre queda perpendicular a él— y lo hace en la dirección que corrige ese patrón.
> Por eso $\eta$ tiene el rol que tiene: es cuánto gira la recta en cada corrección. Grande, pega saltos; chico, la va acomodando de a poco.

### Los tres casos, en una sola fórmula

$$
\boxed{\;w(n+1) = w(n) + \frac{\eta}{2}\big[d(n) - y(n)\big]\,x(n)\;}
$$

Y funciona porque, con salidas $\pm 1$, el error $d - y$ sólo puede valer tres cosas:

| Situación | $d - y$ | Qué hace la fórmula |
|---|:---:|---|
| acertó | $0$ | no cambia nada — mínima perturbación |
| dio $-1$, iba $+1$ | $+2$ | suma $\eta\,x(n)$ |
| dio $+1$, iba $-1$ | $-2$ | resta $\eta\,x(n)$ |

> **IDEA DE FONDO — de dónde sale ese $\tfrac{1}{2}$**
> Del $2$ de la tabla. Como el error sólo puede valer $0$ o $\pm 2$, el $\tfrac{1}{2}$ lo normaliza y deja la corrección en $0$ o $\pm\eta$ limpio. **No es un factor mágico: está puesto para cancelar el 2 de las salidas bipolares.**

**3. Repetir** con el ejemplo siguiente, y volver a pasar por todo el archivo tantas veces como haga falta.

> **PARA LA DEFENSA — qué tiene de bueno y qué le falta**
> Lo bueno: es intuitivo y funciona. Lo que le falta: **es un argumento de sentido común, no una deducción**. Nadie demostró que ese sea el mejor ajuste, ni cuánto conviene que valga $\eta$.
> Ésa es la puerta que abre la sección siguiente de la unidad: llegar **a la misma fórmula** minimizando una función de error con el método del gradiente. No para cambiar el algoritmo, sino porque **ese camino formal sí generaliza** al perceptrón multicapa, donde la intuición ya no alcanza.

### Claves de la sección 6

| Clave | Qué tenés que poder responder |
|---|---|
| Los datos | Qué tiene cada línea del archivo, y por qué hay ruido |
| Inicialización | Cómo arrancan los pesos |
| Mínima perturbación | Qué se hace cuando la salida es correcta |
| Penalización | Los dos casos de error y qué se hace en cada uno |
| Geometría | Por qué $w$ apunta al semiplano positivo y qué le pasa a la frontera al mover $w$ |
| La fórmula única | Cómo cubre los tres casos con una sola expresión |
| El $\tfrac{1}{2}$ | Qué normaliza |
| Lo que falta | Por qué se rehace todo con el gradiente |

---

## Formulario

| Expresión | Qué es |
|---|---|
| $v = \langle w, x\rangle = \sum_{i=0}^{N} w_i x_i$ | activación lineal, con $x_0 = -1$ |
| $y = \varphi(v)$ | salida de la neurona |
| $\mathrm{sgn}(v) = +1$ si $v \ge 0$, $-1$ si no | función signo |
| $\mathrm{sig}(v) = \frac{2}{1+e^{-av}} - 1$ | sigmoide simétrica |
| $\langle w, x\rangle = 0$ | frontera de decisión |
| $x_2 = \frac{w_0}{w_2} - \frac{w_1}{w_2}x_1$ | la frontera, como recta |
| $w(n+1) = w(n) + \frac{\eta}{2}[d(n)-y(n)]\,x(n)$ | **regla por corrección de error** |

## Errores típicos

- Decir que $x_0 = +1$. Vale $-1$: viene de pasar el umbral restando.
- Olvidar que la sumatoria arranca en $0$ cuando se usa la entrada extendida.
- Creer que la recta $\langle w,x\rangle=0$ tiene ordenada al origen sin sesgo. **Pasa por el origen.**
- Explicar la necesidad del sesgo sólo con el dibujo, teniendo a mano el argumento de los puntos opuestos.
- Mezclar la codificación $\{0,1\}$ con la bipolar $\{-1,+1\}$, o las dos sigmoides.
- Presentar la regla de corrección de error como si estuviera deducida. **Es intuitiva**; la deducción viene después.

## Autoevaluación

1. Nombrá las tres partes de la neurona y qué modela cada una.
2. ¿Qué cambia en una red cuando aprende?
3. Pasá de $\sum_{i=1}^{N} w_ix_i > u$ a la forma con entrada extendida, explicando cada paso.
4. Dos razones por las que conviene meter el umbral adentro de la sumatoria.
5. Dibujá las tres funciones de activación y decí cuál es derivable y por qué eso importa.
6. ¿Qué forma tiene la frontera de decisión con 2 entradas? ¿Y con $N$?
7. Demostrá que ninguna recta por el origen resuelve el OR.
8. ¿Cuál es el caso degenerado y por qué no cuenta como solución?
9. Escribí la regla de corrección de error y mostrá que cubre los tres casos.
10. Dibujá $w$, $x$ y la frontera, y mostrá geométricamente qué hace sumar y qué hace restar $\eta x$.
11. ¿Por qué se rehace todo esto con el método del gradiente si ya funciona?
