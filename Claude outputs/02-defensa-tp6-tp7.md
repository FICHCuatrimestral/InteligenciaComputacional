# Defensa TP6 y TP7

Guía para leer antes de la defensa. Cubre los notebooks `Practicas/TP6/TP6-v2.ipynb` y `Practicas/TP7/Version1/TP7.ipynb`.

Cada parte tiene:

- **Qué hicimos**: lo que hay que contar.
- **Por qué**: la justificación de cada decisión.
- **Números**: los resultados para tener a mano.

Al final hay un repaso de conceptos y una lista de preguntas probables con respuestas cortas.

---

## 0. Antes de la defensa

- **Correr el TP7 completo** (`Run All`). Las tablas guardadas del Ejercicio 1 son de una versión vieja del código: dicen 8/10 para el enjambre en el inciso 1, y el código actual da 9/10. Las conclusiones ya tienen los números nuevos. Si no lo corrés, la tabla y la conclusión no coinciden.
- El TP6-v2 ya tiene los resultados guardados. Si lo volvés a correr tarda poco más de un minuto (el Ejercicio 2 es el más lento).

---

## 1. Guion corto para exponer

**TP6 (algoritmos genéticos)**

1. El algoritmo genético está separado en funciones chicas: crear individuo, selección por torneo, cruce, mutación, elitismo. La función `algoritmo_genetico` las junta y **no sabe qué problema resuelve**: recibe la población inicial, `decodificar` y `aptitud`.
2. Ejercicio 1: minimizar dos funciones. Comparamos contra gradiente descendiente. El genético llega al mínimo global en 10 de 10 corridas en las dos funciones. El gradiente llega en 1 de 10 y en 0 de 10, porque se queda en el mínimo local más cercano a donde arranca.
3. Ejercicio 2: elegir genes para clasificar leucemia. El mismo algoritmo genético, con otra representación (máscara de bits) y otra aptitud (UAR de un clasificador). Pasamos de 7129 genes a 2–4. El resultado en test mejora frente a usar todos los genes (0.83 contra 0.76), pero hay sobreajuste y un ranking simple da resultados parecidos o mejores.

**TP7 (inteligencia colectiva)**

1. Ejercicio 1: enjambre de partículas para las mismas dos funciones del TP6. Comparado contra un genético con las mismas evaluaciones de $f$. El enjambre converge mucho más rápido, pero en una corrida del inciso 1 quedó atrapado en un mínimo local (convergencia prematura).
2. Ejercicio 2: colonia de hormigas para el viajante (17 ciudades, óptimo 2085). Probamos 3 métodos de depósito y 4 tasas de evaporación. La mejor configuración fue depósito local con $\rho = 0.1$.

---

## 2. TP6, Ejercicio 1: minimizar funciones

### Qué hicimos

- $f_1(x) = -x \sin\sqrt{|x|}$ en $[-512, 512]$. Mínimo global: $f(420.97) = -418.98$.
- $f_2(x, y) = (x^2+y^2)^{0.25}\,[\sin^2(50 (x^2+y^2)^{0.1}) + 1]$ en $[-100, 100]^2$. Mínimo global: $f(0, 0) = 0$.
- 10 corridas del genético (semillas 0 a 9) y 10 corridas del gradiente desde puntos al azar.
- Una corrida "llega" si su $f$ queda a menos de 0.1 del mínimo global.

### El algoritmo genético

| Parámetro | Valor | Por qué |
|---|---|---|
| Representación | 20 bits por variable | Resolución de $0.001$ en $f_1$ y $0.0002$ en $f_2$ |
| Población | 50 | Cubre bien el dominio |
| Generaciones | 200 | Criterio de parada fijo: todas las corridas hacen el mismo trabajo |
| Selección | Torneo de 3 | Funciona con aptitud negativa; presión moderada |
| Cruce | Un punto, probabilidad 0.9 | El cruce es el operador principal |
| Mutación | $1/n_{bits}$ por bit | En promedio cambia 1 bit por hijo |
| Elitismo | El mejor pasa directo | La mejor aptitud nunca baja |
| Aptitud | $-f$ | El genético maximiza y buscamos un mínimo |

**Decodificar.** Los bits se pasan a un entero y el entero se lleva al intervalo:

$$x = a + \text{entero} \cdot \frac{b - a}{2^{20} - 1}$$

En $f_2$ el individuo tiene 40 bits: 20 para $x$ y 20 para $y$.

### El gradiente descendiente

- Paso: $p \leftarrow p - \eta \, \nabla f(p)$, 1000 iteraciones.
- El gradiente se calcula **numéricamente** con diferencias centradas: $\frac{f(p + h e_i) - f(p - h e_i)}{2h}$, con $h = 10^{-6}$. No hace falta derivar a mano, y el error es de orden $h^2$ (mejor que la diferencia hacia adelante, de orden $h$).
- Tasa $\eta = 1$ en $f_1$ y $\eta = 0.1$ en $f_2$. $f_1$ tiene un dominio grande y con 0.1 avanzaría muy lento. $f_2$ tiene pendientes grandes y con 1 saltaría sin control.
- Si el punto sale del dominio, queda en el borde.

### Números

| | Genético | Gradiente |
|---|---|---|
| Llegó al global, $f_1$ | **10/10** | 1/10 |
| $f$ promedio, $f_1$ | −418.98 | −158.35 |
| Llegó al global, $f_2$ | **10/10** | 0/10 |
| $f$ promedio, $f_2$ | 0.02 | 7.89 |
| Generación / iteración de llegada | 10 en $f_1$, 33 en $f_2$ (promedio) | se queda quieto en menos de 70 iteraciones |

### Cosas para explicar

- **El gradiente es local.** Solo mira la pendiente donde está parado. Va al mínimo del valle donde arranca. En $f_1$ la única corrida que llegó arrancó en $x_0 = 352.7$, dentro del valle del global. Las otras terminaron en $x \approx -302.5, -124.8, -25.9, 5.2, 65.5, 203.8$.
- **En $f_2$ el gradiente no llega nunca.** La función tiene anillos de mínimos locales alrededor del origen. Cada corrida baja al anillo más cercano y queda ahí. El gráfico 3D lo muestra.
- **El genético es global.** Evalúa 50 puntos repartidos por todo el dominio. La selección concentra la población en la mejor zona y la mutación sigue explorando.
- **¿Por qué el genético da 0.02 y no 0 en $f_2$?** Con 20 bits en $[-100, 100]$ el 0 no es representable. Los valores más cercanos son $\pm 0.0000954$. Ahí $f_2$ vale 0.01996, que es el mejor valor posible con esta codificación. Las 10 corridas lo encontraron. Es un límite de la **codificación**, no del algoritmo; con más bits baja.
- **Costo.** El genético evalúa $f$ unas 10 050 veces por corrida ($50 \times 200 + 50$). El gradiente, 2000 en $f_1$ y 4000 en $f_2$ (2 evaluaciones por variable por iteración). El genético es más caro, pero más iteraciones no sacan al gradiente de su valle.

---

## 3. TP6, Ejercicio 2: selección de genes

### Qué hicimos

- 38 pacientes de train (27 ALL, 11 AML), 34 de test (20 ALL, 14 AML), 7129 genes.
- Esquema **envolvente** (*wrapper*): el genético propone subconjuntos de genes y un clasificador dice qué tan buenos son.

Los pasos, en orden:

1. **Normalizar** cada gen con media y desvío de train.
2. **Prefiltro**: quedarse con los 50 genes de mayor señal/ruido.
3. **Genético**: cada individuo es una máscara de 50 bits (1 = uso el gen).
4. **Aptitud**: UAR de validación dejando uno afuera, con vecino más cercano, menos una penalización por cantidad de genes.
5. **Test**: se usa una sola vez al final, con los genes elegidos.

### Por qué cada decisión

**Normalizar** ($z = (x - \mu)/\sigma$)

- El vecino más cercano usa distancias. Los genes tienen escalas muy distintas: el desvío de cada gen va de 21 a 12 500. Sin normalizar, en la distancia mandan los genes de valores grandes, que no son necesariamente los importantes.
- La media y el desvío se calculan **solo con train**, y se aplican igual a test. Test representa pacientes nuevos: usar sus datos para normalizar sería una **fuga de datos** (usar información que en la realidad no tendríamos).

**Prefiltro por señal/ruido**

$$SN = \frac{|\mu_{ALL} - \mu_{AML}|}{\sigma_{ALL} + \sigma_{AML}}$$

- Mide qué tan separadas están las medias de las dos clases, en relación con cuánto varía cada clase. Un valor alto es un gen que separa bien. Es la medida del trabajo original sobre estos datos (Golub et al., 1999).
- Se calcula solo con train.
- **Por qué hace falta:** sin prefiltro el genético sobreajusta. Con 7129 genes y 38 pacientes hay muchísimas combinaciones que separan perfecto a los 38 por casualidad. Experimento extra: el mismo genético sobre los 7129 genes dio validación ≈ 1.0 pero test entre 0.48 y 0.73.
- Además achica el espacio de búsqueda de $2^{7129}$ a $2^{50}$ subconjuntos.
- **Lo que se pierde:** el prefiltro mira cada gen por separado. Si dos genes solo sirven juntos, el ranking los descarta. Es un compromiso aceptable con tan pocos pacientes.

**Vecino más cercano (1-NN)**

- No tiene azar ni entrenamiento: el mismo subconjunto de genes tiene **siempre la misma aptitud**. Con una red neuronal la aptitud dependería de los pesos iniciales.
- Es barato. La aptitud se calcula miles de veces (30 individuos × 60 generaciones por corrida).
- Con 38 pacientes, un modelo con muchos parámetros sobreajusta enseguida.

**UAR** (ver conceptos): las clases están desbalanceadas, 27 ALL y 11 AML.

**Validación dejando uno afuera (*leave-one-out*)**

- Cada paciente de train se clasifica con los otros 37. Así se usan los 38 para validar.
- Con tan pocos pacientes no se puede apartar un conjunto de validación: quedarían muy pocos para comparar y cada error movería mucho el resultado.
- Con 1-NN no hay que reentrenar nada, así que es barato.

**Test solo al final.** Si la aptitud usara test, el genético elegiría los genes que mejor le van a esos 34 pacientes. El UAR de test dejaría de estimar lo que pasa con pacientes nuevos.

**Población inicial con pocos genes.** Cada bit se prende con probabilidad 10/50, así cada individuo arranca con unos 10 genes. Con bits al 50 % arrancaría con 25 genes, y buscamos subconjuntos chicos.

**Aptitud con penalización**

$$\text{aptitud} = \text{UAR}_{val} - \beta \cdot \frac{\text{genes usados}}{50}, \qquad \beta = 0.2$$

- Cada gen cuesta $0.2/50 = 0.004$. Un error de validación cuesta mucho más (0.019 un ALL, 0.045 un AML).
- En la práctica, $\beta$ funciona como **desempate**: entre subconjuntos que clasifican igual, gana el más chico.
- Una máscara vacía tiene aptitud 0, así pierde todos los torneos.

### Números

| Semilla | Genes | Cantidad | UAR validación | UAR test |
|---|---|---|---|---|
| 0 | 1744, 6470, 2120, 4051 | 4 | 1.0 | 0.87 |
| 1 | 4846, 2353 | 2 | 1.0 | 0.94 |
| 2 | 460, 6973, 4051 | 3 | 1.0 | 0.76 |
| 3 | 3319, 1248, 148 | 3 | 1.0 | 0.79 |
| 4 | 2758, 6538, 6375 | 3 | 1.0 | 0.81 |

| Método | Genes | UAR validación | UAR test |
|---|---|---|---|
| Todos los genes | 7129 | 0.80 | 0.76 |
| 3 mejores por señal/ruido | 3 | 0.94 | 0.86 |
| 10 mejores por señal/ruido | 10 | 1.00 | 0.93 |
| 50 candidatos | 50 | 0.96 | **0.96** |
| Genético (promedio) | 3 | 1.00 | 0.83 |

### Cosas para explicar

- **Sobreajuste.** La validación da 1.0 en todas las corridas y test es más bajo en todas. Ya en la **generación 0** el mejor individuo tenía validación 1.0, con 5 a 7 genes. La aptitud no distingue un subconjunto bueno de uno que tuvo suerte con train. Lo único que el genético puede mejorar es la penalización: baja de 5–7 genes a 2–4.
- **El ranking simple compite bien.** Con la misma cantidad de genes (3), los 3 mejores por señal/ruido dan 0.86 en test, contra 0.83 del genético. El genético gana en **tamaño**, no en desempeño.
- **Varios genes elegidos están lejos en el ranking** (puestos 28, 35, 39, 41, 47, 48 de 50). Ayudan a separar train, pero no separan bien las clases en general.
- **Cuánto vale una diferencia en test.** Con 34 pacientes, un error en un AML baja el UAR 0.036 y uno en un ALL, 0.025. La diferencia entre 0.83 y 0.93 son 3 o 4 pacientes.
- **Validación anidada (experimento extra).** El prefiltro usa los 38 pacientes, así que en la validación dejando uno afuera el paciente que queda afuera ya participó en elegir los candidatos. Es una fuga chica. Repitiendo prefiltro y genético dentro de cada partición, la validación baja de 1.0 a 0.79, mucho más cerca del test (0.83).
- **Cambiar $\beta$ (experimento extra).** Con $\beta = 0$ el genético elige 10–16 genes y el test promedio sube a 0.88. Con $\beta = 0.5$ elige 2–3 genes y baja a 0.80. $\beta$ elige el punto entre tamaño y desempeño.

---

## 4. TP7, Ejercicio 1: enjambre de partículas

### Qué hicimos

- Las mismas $f_1$ y $f_2$ del TP6.
- Enjambre con mejor global (*gbest*): 20 partículas, 100 iteraciones.
- Comparado con un genético de 20 individuos y 100 generaciones. Los dos evalúan $f$ 20 veces por iteración, así que comparar iteraciones es comparar evaluaciones.
- 10 corridas de cada uno. Una corrida "llega" si su mejor $f$ queda a menos de 0.1 del mínimo.

### El algoritmo

Cada partícula tiene una **posición**, una **velocidad** y su **mejor posición propia** $y_k$. El enjambre conoce la **mejor posición global** $\hat{y}$.

En cada iteración:

1. Se busca el mejor global: la mejor posición propia con menor $f$.
2. Cada partícula calcula su nueva velocidad y se mueve:

$$v \leftarrow \underbrace{w\, v}_{\text{inercia}} + \underbrace{c_1 r_1 (y_k - x)}_{\text{cognitivo}} + \underbrace{c_2 r_2 (\hat{y} - x)}_{\text{social}} \qquad x \leftarrow x + v$$

3. Si el lugar nuevo es mejor que su mejor posición propia, la actualiza.

| Parámetro | Valor | Qué hace |
|---|---|---|
| $w$ (inercia) | 0.73 | Cuánto conserva de la velocidad anterior. Menor que 1 para que el enjambre frene y converja |
| $c_1$ (cognitivo) | 1.5 | Fuerza hacia su propio mejor lugar |
| $c_2$ (social) | 1.5 | Fuerza hacia el mejor del enjambre |
| $r_1, r_2$ | azar en $[0, 1]$, nuevos en cada dimensión | Evitan que todas vayan exactamente al mismo lugar |

Los valores $w \approx 0.73$ y $c \approx 1.5$ son los habituales del apunte (cercanos a los de Clerc: 0.729 y 1.49), que dan un enjambre estable.

**El genético del TP7** es más chico que el del TP6, para igualar evaluaciones: población 20, torneo de 2, cruce en un punto, mutación $1/n_{bits}$, y conserva los 2 mejores (reemplaza el 90 %).

### Números

| | Genético | Enjambre |
|---|---|---|
| Llegó al global, inciso 1 | 10/10 | 9/10 |
| Iteración de llegada, inciso 1 | 27 (entre 5 y 60) | **3** (entre 1 y 9) |
| Llegó al global, inciso 2 | 8/10 | **10/10** |
| Iteración de llegada, inciso 2 | 65 (entre 43 y 97) | **45** (entre 37 y 55) |
| $f$ promedio, inciso 2 | 0.11 | **0.011** |

### Cosas para explicar

- **El enjambre es más rápido.** Todas las partículas siguen al mejor global. Apenas una encuentra un buen valle, las demás van hacia ahí.
- **Convergencia prematura.** En la corrida que falló (inciso 1, semilla 7), todas las partículas se juntaron en el borde $x = -512$, con $f = -304.2$, el segundo mejor valle. Cuando todas están en el mismo lugar, $y_k - x = 0$ y $\hat{y} - x = 0$: los empujes valen 0. Solo queda la inercia, que se achica en cada paso ($w < 1$). El enjambre se frena y no sale más.
- **El genético no tiene ese problema** porque la mutación sigue creando puntos nuevos.
- **En el inciso 2 gana el enjambre.** Las partículas se mueven en los números reales y se acercan al origen tanto como haga falta. El genético está limitado por la resolución de 20 bits y por los anillos de mínimos locales (2 corridas quedaron en $f = 0.54$ y $f = 0.18$).
- **¿Por qué acá el genético llega 8/10 y en el TP6 10/10?** En el TP7 tiene 20 individuos y 100 generaciones (2000 evaluaciones). En el TP6 tenía 50 y 200 (10 000 evaluaciones).

---

## 5. TP7, Ejercicio 2: colonia de hormigas

### Qué hicimos

- Problema del viajante con 17 ciudades (`gr17`, de la biblioteca TSPLIB). Óptimo conocido: **2085**.
- Solo tenemos distancias entre ciudades, no coordenadas.
- La cantidad de recorridos distintos es $(n-1)!/2 = 16!/2 \approx 10^{13}$: no se pueden probar todos.
- 3 métodos de depósito × 4 tasas de evaporación ($\rho$ = 0.01, 0.1, 0.5, 0.9) × 10 corridas.
- Fijos: 10 hormigas, $\alpha = 1$, $\beta = 1$, $Q = 1$, feromona inicial al azar en $[0, 0.1]$, máximo 200 iteraciones.

### El algoritmo

En cada iteración:

1. **Cada hormiga construye un recorrido.** Arranca en una ciudad al azar. Elige la próxima entre las no visitadas (**lista tabú**), por ruleta, con probabilidad proporcional a $\sigma_{ij}^\alpha \, \eta_{ij}^\beta$:
   - $\sigma_{ij}$: feromona de la conexión.
   - $\eta_{ij} = 1/d_{ij}$: el **deseo**. Las ciudades cercanas atraen más.
   - $\alpha$ y $\beta$ regulan cuánto pesa cada uno.
2. **Se guarda el mejor recorrido** visto hasta ahora.
3. **Se actualizan las feromonas:**
   - **Evaporación** en todas las conexiones: $\sigma_{ij} \leftarrow (1-\rho)\,\sigma_{ij}$.
   - **Depósito** en los tramos que usó cada hormiga.
4. **Corte:** si todas las hormigas hicieron el mismo camino, o al llegar a 200 iteraciones.

**Métodos de depósito** (cantidad que suma cada hormiga en cada tramo de su recorrido):

| Método | Cantidad | Qué premia |
|---|---|---|
| Global | $Q / L_k$ | Que el recorrido completo sea corto |
| Uniforme | $Q$ | Solo que la hormiga pasó por ahí |
| Local | $Q / d_{ij}$ | Que ese tramo sea corto |

**¿Por qué $\beta = 1$?** Con $\beta = 2$ el deseo $1/d$ pesa tanto que todas las configuraciones llegan al óptimo y no se ve el efecto de $\rho$ ni del depósito.

**Comparar recorridos.** `[0, 1, 2]`, `[1, 2, 0]` y `[0, 2, 1]` son el mismo recorrido cerrado. Por eso para el criterio de corte se comparan como conjuntos de tramos.

### Números (largo promedio de 10 corridas, entre paréntesis las que llegaron a 2085)

| $\rho$ | Global | Uniforme | Local |
|---|---|---|---|
| 0.01 | 2242 (0/10) | 2125 (1/10) | 2093 (4/10) |
| 0.1 | 2102 (2/10) | 2104 (4/10) | **2091 (5/10)** |
| 0.5 | 2108 (1/10) | 2117 (1/10) | 2114 (3/10) |
| 0.9 | 2122 (1/10) | 2124 (1/10) | 2114 (2/10) |

Iteración en que encuentran el mejor recorrido, con $\rho = 0.1$: local 82, uniforme 145, global 166.

### Cosas para explicar

- **$\rho = 0.1$ fue la mejor en los tres métodos.**
- **$\rho$ chico (0.01):** la feromona casi no se borra. Lo depositado al principio y las feromonas iniciales al azar pesan hasta el final. Con depósito global es el peor caso (2242, ninguna llegó). Con depósito local casi no afecta.
- **$\rho$ grande (0.5, 0.9):** se olvida todo enseguida. La colonia encuentra su mejor recorrido antes, pero más largo. Es convergencia prematura: no aprovecha lo que aprendió.
- **El local fue el mejor método.** Premia los tramos cortos, que son los que forman un buen recorrido. Además encuentra el mejor antes.
- **El global arranca lento.** Con $Q = 1$ deposita $1/L \approx 0.0005$ por tramo, mucho menos que la feromona inicial (hasta 0.1). Tarda muchas iteraciones en que su depósito pese más que el azar inicial. En la iteración 10 su mejor largo promedio es 2649, contra 2282 del local.
- **El uniforme** deposita lo mismo para un recorrido bueno que para uno malo. Refuerza los tramos muy usados, pero no distingue calidad.
- **Tiempo.** Todas las corridas tardan menos de medio segundo. En ninguna todas las hormigas hicieron el mismo camino, así que siempre terminaron por las 200 iteraciones. Por eso el tiempo de búsqueda se midió hasta encontrar el mejor recorrido (en iteraciones y en segundos).

---

## 6. Conceptos

**Individuo / cromosoma.** Una solución posible codificada. En el TP6, una lista de bits.

**Aptitud (*fitness*).** Qué tan buena es una solución. El genético busca la mayor. Por eso, para minimizar $f$, usamos aptitud $= -f$.

**Selección por torneo.** Se sortean $k$ individuos y gana el de mayor aptitud. Ventajas frente a la ruleta:

- Solo compara, así que funciona con aptitudes negativas (la ruleta necesita valores positivos).
- Usa el orden y no el valor, así que no le afecta la escala. Si todas las aptitudes son parecidas (como en el Ejercicio 2, entre 0.97 y 0.99), la ruleta sería casi un sorteo.
- El tamaño $k$ regula la presión: torneo más grande, más ventaja para los mejores.

**Cruce en un punto.** Se corta a los dos padres en el mismo lugar y se intercambian las partes. Combina partes buenas de soluciones distintas.

**Mutación.** Cada bit cambia con probabilidad baja ($1/n_{bits}$: en promedio un bit por hijo). Mantiene la **diversidad**: puede crear bits que ningún padre tenía. Mucha mutación es búsqueda al azar; muy poca, la población se estanca.

**Elitismo.** El mejor individuo pasa sin cambios a la siguiente generación. Garantiza que la mejor aptitud **nunca baja**. Sin elitismo, el mejor podría perderse: no salir en los torneos, o salir y que el cruce o la mutación lo arruinen.

**Exploración y explotación.** Explorar es buscar en zonas nuevas; explotar es refinar alrededor de lo bueno ya encontrado. La mutación explora; la selección explota. En el enjambre, la inercia ayuda a explorar y los términos cognitivo y social, a explotar.

**Convergencia prematura.** La población (o el enjambre, o la colonia) se concentra en un mínimo local antes de encontrar el global, y pierde la diversidad para salir.

**Mínimo local y global.** El global es el menor valor de toda la función. Un local es el menor valor de su zona. Los métodos que solo miran la pendiente (gradiente) quedan en el local de su zona.

**Gradiente descendiente.** Moverse en contra del gradiente, que es la dirección en que $f$ baja más rápido. La **tasa** $\eta$ define el tamaño del paso: muy chica, avanza lento; muy grande, salta sin control.

**UAR (*Unweighted Average Recall*).** El promedio del porcentaje de aciertos de cada clase:

$$\text{UAR} = \frac{1}{2}\left(\frac{\text{ALL bien clasificados}}{\text{total ALL}} + \frac{\text{AML bien clasificados}}{\text{total AML}}\right)$$

Con clases desbalanceadas, el porcentaje de aciertos (*accuracy*) engaña. Un clasificador que dice siempre ALL acierta 71 % en train sin aprender nada, pero su UAR es 0.5, lo mismo que tirar una moneda.

**Recall de una clase.** De los pacientes de esa clase, qué porcentaje se clasificó bien.

**Normalización (z-score).** Restar la media y dividir por el desvío de cada característica. Así todas tienen la misma escala y ninguna domina la distancia.

**Fuga de datos (*data leakage*).** Usar en el entrenamiento información que no se tendría en la realidad, por ejemplo los datos de test. El resultado queda mejor de lo que es.

**Sobreajuste.** El modelo se ajusta a los datos que vio (incluso a su ruido) y funciona peor con datos nuevos. Se nota cuando validación es mucho mejor que test.

**Señal/ruido.** Ver sección 3. Mide cuánto separa un gen a las dos clases.

**Selección de características envolvente (*wrapper*) y de filtro.** El **filtro** puntúa cada característica por separado, sin clasificador (el prefiltro señal/ruido). El **envolvente** evalúa subconjuntos con el clasificador (el genético). Usamos los dos: filtro para achicar, envolvente para elegir.

**Vecino más cercano (1-NN).** Clasifica un caso nuevo con la clase del caso conocido más parecido (menor distancia).

**Validación dejando uno afuera.** Se saca un caso, se clasifica con el resto, y se repite con cada caso.

**Enjambre de partículas (PSO).** Ver sección 4. Inercia, cognitivo, social; mejor propio y mejor global.

**Colonia de hormigas (ACO).** Ver sección 5. Feromona, evaporación, deseo, lista tabú, $\alpha$, $\beta$.

**Inteligencia colectiva.** Agentes simples que siguen reglas locales y, juntos, resuelven un problema que ninguno resuelve solo. Las partículas comparten el mejor global; las hormigas se comunican indirectamente a través de la feromona (**estigmergia**).

---

## 7. Preguntas probables

### TP6

**¿Por qué la aptitud es $-f$ y no $1/f$?**
Porque $f_1$ puede ser negativa o cero, y $1/f$ cambiaría de signo o explotaría. $-f$ invierte el orden en todo el dominio, y con torneo el signo no importa.

**¿Por qué 20 bits?**
Por la resolución: $(b-a)/(2^{20}-1)$ da 0.001 en $f_1$ y 0.0002 en $f_2$. Con 10 bits la resolución de $f_1$ sería 1, y el mínimo podría quedar entre dos valores representables.

**¿Por qué torneo y no ruleta?**
Porque la aptitud es negativa en el Ejercicio 1 (la ruleta necesita valores positivos) y porque en el Ejercicio 2 las aptitudes son todas parecidas (la ruleta sería casi un sorteo).

**¿Qué pasa si sacás el elitismo?**
El mejor individuo puede perderse y la mejor aptitud puede bajar. Además habría que guardar el mejor de toda la corrida aparte, porque el de la última generación ya no sería necesariamente el mejor.

**¿Por qué mutación $1/n_{bits}$?**
Para cambiar en promedio un bit por hijo. Mantiene diversidad sin destruir lo que trae el cruce.

**¿Por qué falla el gradiente?**
Porque es un método local: va al mínimo del valle donde arranca. Las funciones tienen muchos mínimos locales. Más iteraciones no ayudan; sí ayudaría arrancar desde muchos puntos (*multistart*).

**¿Por qué el genético no llega a 0 en $f_2$?**
Porque el 0 no es representable con 20 bits en $[-100, 100]$. El punto más cercano da 0.01996, que es lo mejor posible con esa codificación.

**¿La comparación es justa en evaluaciones?**
No del todo: el genético evalúa unas 10 000 veces y el gradiente 2000–4000. Pero el gradiente ya está quieto en su valle antes de las 100 iteraciones; más evaluaciones no lo sacan.

**¿Por qué normalizar? ¿Por qué con datos de train?**
Porque el clasificador usa distancias y los genes tienen escalas muy distintas. Con train, porque test representa pacientes nuevos: usar sus datos sería fuga de datos.

**¿Por qué UAR y no accuracy?**
Clases desbalanceadas (27 ALL, 11 AML). Decir siempre ALL da 71 % de accuracy y UAR 0.5.

**¿Por qué vecino más cercano y no una red neuronal?**
Es determinista (la aptitud no depende del azar), barato (se evalúa miles de veces) y no tiene parámetros que sobreajusten con 38 pacientes.

**¿Por qué el prefiltro?**
Sin él el genético sobreajusta: validación 1.0 y test entre 0.48 y 0.73. Con 7129 genes hay muchísimas combinaciones que separan train por casualidad.

**¿Para qué sirve $\beta$?**
Para preferir subconjuntos chicos. Cada gen cuesta 0.004, mucho menos que un error. Actúa como desempate.

**¿Por qué la validación da 1.0 y test no?**
Sobreajuste a la validación: el genético busca justamente lo que maximiza la validación, y con 38 pacientes hay muchos subconjuntos que la llevan a 1.0 por casualidad. Ya en la generación 0 había individuos con 1.0.

**Si los 10 mejores del ranking dan 0.93, ¿para qué sirve el genético?**
El genético gana en tamaño: 3 genes en vez de 10, un modelo más simple. En desempeño, el ranking simple compite igual o mejor. Bajando $\beta$ el genético usa más genes y mejora el test (0.88 con $\beta = 0$).

**¿Encontraron "los genes de la leucemia"?**
No con certeza. Cada semilla elige genes distintos (solo el 4051 se repite), todos con validación 1.0. Es **un** subconjunto chico que funciona, no **el** subconjunto.

**¿Cómo estimarías el desempeño sin usar test?**
Con validación anidada: repetir prefiltro y genético dentro de cada partición de la validación. Da 0.79.

### TP7

**¿Qué hace cada término de la velocidad?**
Inercia: sigue en la dirección que traía. Cognitivo: va hacia su propio mejor lugar. Social: va hacia el mejor del enjambre.

**¿Qué pasa si $c_2 = 0$? ¿Y si $c_1 = 0$?**
Con $c_2 = 0$ cada partícula busca sola, sin compartir información: son 20 búsquedas independientes. Con $c_1 = 0$ todas van directo al mejor global: converge rápido pero con más riesgo de convergencia prematura.

**¿Por qué $w < 1$?**
Para que la velocidad se vaya achicando y el enjambre converja. Con $w \geq 1$ las velocidades pueden crecer sin límite.

**¿Por qué una corrida del enjambre falló?**
Convergencia prematura: todas las partículas se juntaron en $x = -512$. Ahí los términos cognitivo y social valen 0 y la inercia se apaga. No hay nada que las saque, porque el enjambre no tiene mutación.

**¿Cómo lo evitarías?**
Más partículas; usar mejor local (*lbest*, cada partícula ve solo a sus vecinas) en vez de global; agregar una perturbación al azar (como una mutación); o reiniciar las partículas cuando se juntan.

**¿Por qué el enjambre es mejor en el inciso 2?**
Trabaja directo en los números reales, sin la resolución de 20 bits, y converge rápido hacia el mejor global.

**¿Por qué el genético del TP7 es distinto al del TP6?**
Para comparar con las mismas evaluaciones de $f$: 20 individuos y 100 generaciones, igual que el enjambre.

**¿Qué pasa cuando una partícula sale del dominio?**
Se la deja en el borde. Por eso la corrida que falló quedó justo en $x = -512$.

**¿Qué es $\alpha$ y $\beta$ en las hormigas?**
$\alpha$ pesa la feromona (lo aprendido por la colonia). $\beta$ pesa el deseo $1/d$ (la información del problema, que la ciudad esté cerca). Con $\alpha = 0$ es una búsqueda golosa al azar; con $\beta = 0$ solo importa la feromona.

**¿Para qué sirve la evaporación?**
Para olvidar caminos malos. Sin evaporación, la feromona del principio (cuando los recorridos son malos) pesaría para siempre.

**¿Para qué la lista tabú?**
Para que cada hormiga visite cada ciudad una sola vez, que es lo que pide el problema.

**¿Por qué el local es el mejor depósito?**
Premia directamente los tramos cortos, y un buen recorrido está hecho de tramos cortos. El global premia el recorrido completo, pero con $Q = 1$ deposita muy poco y tarda en pesar más que la feromona inicial.

**¿Por qué nunca cortó por "todas hicieron el mismo camino"?**
Con $\alpha = \beta = 1$ la elección por ruleta mantiene bastante azar, y siempre hay alguna hormiga que se desvía. Por eso se midió el tiempo hasta encontrar el mejor recorrido.

**¿Cómo saben que 2085 es el óptimo?**
Es un problema de la biblioteca TSPLIB, con óptimo conocido y publicado.

**¿En qué se parecen y en qué se diferencian el enjambre y las hormigas?**
Los dos son inteligencia colectiva: agentes simples que comparten información. Las partículas comparten el mejor global directamente y trabajan en espacios continuos. Las hormigas se comunican indirectamente con la feromona y resuelven problemas combinatorios (recorridos).

---

## 8. Números para tener a mano

| | Valor |
|---|---|
| Mínimo de $f_1$ | $f(420.97) = -418.98$ |
| Mínimo de $f_2$ | $f(0, 0) = 0$; el genético llega a 0.01996 |
| TP6 Ej. 1: genético / gradiente | 10/10 y 10/10 / 1/10 y 0/10 |
| TP6 Ej. 2: genes elegidos | 2 a 4 (3 en promedio) |
| TP6 Ej. 2: UAR test | genético 0.83, todos los genes 0.76, top 3 0.86, top 10 0.93, 50 candidatos 0.96 |
| TP6 Ej. 2: sin prefiltro | test 0.48 a 0.73 |
| TP6 Ej. 2: validación anidada | 0.79 |
| TP7 Ej. 1: llegó al global | inciso 1: genético 10/10, enjambre 9/10; inciso 2: genético 8/10, enjambre 10/10 |
| TP7 Ej. 1: iteración de llegada | inciso 1: 27 contra 3; inciso 2: 65 contra 45 |
| TP7 Ej. 2: óptimo gr17 | 2085 |
| TP7 Ej. 2: mejor configuración | local, $\rho = 0.1$: largo promedio 2091, 5/10 al óptimo |
