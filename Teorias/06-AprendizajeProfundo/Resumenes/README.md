# Apuntes — Introducción al aprendizaje profundo

Inteligencia Computacional · FICH-UNL · Diego Milone

| Archivo | Qué es |
|---|---|
| `01-aprendizaje-profundo.md` | La unidad completa: el mapa del aprendizaje automático, los cuatro problemas de las redes profundas (con el desvanecimiento del gradiente deducido y simulado), programación diferenciable, el mapa logístico, las cuatro formas de derivar, el grafo de primitivas, los modos directo y reverso con sus tablas, PyTorch por dentro, el entrenamiento de una neurona con dos criterios y tres activaciones, más capas, activaciones con `if`, el Lego de arquitecturas, cinco desarrollos para el pizarrón, formulario, errores típicos y autoevaluación |

Fuentes: `Introduccion al aprendizaje profundo 2026.pdf` (176 láminas). `Introduccion al aprendizaje profundo (video).pdf` y las transcripciones 001 a 008 se usaron sólo como referencia (ver abajo).

## Lo que hay que saber de las fuentes

- **Las transcripciones no sirven.** Son subtítulos automáticos de la charla grabada, con frases como *«y bogotá»* o *«la privada de china»* y muchos *[Música]*. Sólo confirman el orden de los temas. El énfasis del apunte sale de cómo están armadas las láminas: qué desarrollan paso a paso y qué repiten.
- **Hay dos juegos de diapositivas.** La versión *(video)* es de 2019: repasa perceptrón, XOR y retropropagación (ya están en la unidad 01) y no tiene la parte *Aprendizaje con ∂P*. El apunte sigue la de **2026**.
- **Muchas láminas son sólo imagen**: la línea de tiempo, el diagrama de bifurcación, las cuatro formas de derivar, los grafos de primitivas y las arquitecturas. Están reconstruidas en las figuras 1, 2, 4, 5 y 6.
- **Errata, lámina 147** (derivada de $v/(1+e^{-v})$): el numerador va $1+e^{-v}+v\,e^{-v}$, no $1+e^{-v}+v(1+e^{-v})$, y el resultado es $\sigma(v)[1+v(1-\sigma(v))]$, no $y[1+v(1-y)]$. En $v=3$ la lámina da $-13{,}07$ y el valor verdadero es $1{,}088$. Es la figura 8 y la sección 12.
- **Errata, lámina 154:** `y2a = 1/(1+torch.exp(-v1))` usa `v1` donde va `v2`. **Lámina 158:** `y = sigmoid(v1)` usa `v1` donde va `v`. Las dos corren sin error y entrenan otra red.
- **Inconsistencia, lámina 150:** el $\tfrac12$ de la sigmoide bipolar aparece junto con la derivada $y(1-y)$ de la logística.
- **Dos matices:** la lámina 36 lista la derivación simbólica y la numérica como sinónimos de la automática, cuando la 62 las presenta como alternativas. Y la lámina 77 dice que la exactitud «ayuda a evitar el desvanecimiento»; el apunte aclara en qué sentido (§5).
- **Lo que las láminas dejan sin terminar:** la cancelación de $y(1-y)$ con entropía cruzada (lámina 141) va completa en la §11. La recursión $d\ell_{n+1}/dx = (4-8\ell_n)\,d\ell_n/dx$, que es lo que hace el código de la lámina 75, va en la §4.

## Números del apunte

Todos salen de `../imagenes/graficos_profundo.py`, que imprime las verificaciones por consola:

| Afirmación | Verificación |
|---|---|
| Las cuatro formas de derivar el mapa logístico coinciden | En $x=0{,}3$: manual, simplificada y automática dan $1{,}3090816$; la numérica con $h=10^{-6}$, $1{,}3090056$ (error $7{,}6\times10^{-5}$) |
| El error numérico tiene forma de V | Mejor $h\approx10^{-9}$ (error $2\times10^{-8}$); con $h=10^{-13}$ vuelve a $1{,}3\times10^{-4}$ |
| Explosión de expresiones | $d\ell_6/dx$: 768 operaciones simbólicas contra 35 de la automática |
| Ejemplo de Baydin | Directo, reverso, motor propio y numérica centrada: $(5{,}5;\ 1{,}716338)$ |
| Gradiente de una neurona | A mano y automático coinciden, con error cuadrático y con entropía cruzada |
| Red 2-1-1 | Retropropagación a mano igual al motor automático en las 5 componentes |
| Desvanecimiento | 30 capas, 10 semillas: con sigmoide la capa 1 recibe $3\times10^{-19}$ del gradiente de la capa 30; con tanh, 0,1; con ReLU, del orden de 1 |
| Saturación | $v=-6$, $y_d=1$: la entropía cruzada empuja 200 veces más que el error cuadrático |

## Carpetas

- `../imagenes/`: los 11 PNG y el script que los genera (numpy y matplotlib; sympy sólo para la figura de explosión de expresiones).
- `../Transcripciones/`: las transcripciones de la charla.
- `../build/`: el filtro y el estilo para regenerar el PDF con Pandoc (a `estilo.tex` se le agregó el paquete `cancel`).

## Regenerar

```bash
python3 ../imagenes/graficos_profundo.py
../build/construir.sh 01-aprendizaje-profundo.md
```
