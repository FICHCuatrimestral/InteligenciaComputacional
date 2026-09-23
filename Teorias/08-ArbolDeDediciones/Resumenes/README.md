# Apuntes — Árboles de decisión

Inteligencia Computacional · FICH-UNL

| Archivo | Qué es |
|---|---|
| `01-arboles-de-decision.md` | El tema completo: datos nominales, qué es un árbol y su interpretabilidad, las seis preguntas de CART con el pseudocódigo de la construcción, cortes binarios y regiones rectangulares, las cuatro impurezas y la caída de impureza (con el nodo 90/10 resuelto paso a paso), cuándo parar, la poda y el efecto horizonte (con el XOR), etiquetas de las hojas, faltantes y cortes sustitutos, costos, complejidad, inestabilidad y su relación con los ensambles, árboles multivariados, ID3 / C4.5 / CART, ventajas y desventajas, tres desarrollos para el pizarrón, formulario, errores típicos y autoevaluación |

Este apunte reemplaza la versión sin figuras del commit «faltantes».

## Lo que hay que saber de las fuentes

- **No hay material de cátedra en la carpeta**: ni diapositivas ni transcripciones. El tema figura en la planificación («métodos básicos de aprendizaje supervisado», unidad 4) y como uno de los seis clasificadores del ejercicio 2 de la guía de TP 3. El apunte se arma sobre el **capítulo 8 de Duda, Hart & Stork**, que está en `Bibliografía/`. El árbol de las frutas, el nodo 90/10, las seis preguntas y la comparación ID3/C4.5 son de ahí.
- **Sin clase no hay énfasis del profesor.** El nivel elegido es el de un oral: el método, la construcción y la impureza, sin deducciones de teoría de la información. Si aparecen diapositivas de este tema, conviene revisar el alcance contra ellas.
- **Lo que se agregó y no está en el libro con estos números:** el pseudocódigo recursivo, el XOR como ejemplo del efecto horizonte, la escalera de la frontera oblicua medida en hojas, el experimento de sobreajuste y poda, el ejemplo de inestabilidad y la relación con *bagging*/AdaBoost del TP 3.

## Números del apunte

Todos salen de `../imagenes/graficos_arboles.py`, que tiene una implementación propia de CART (Gini o entropía, cortes axiales, poda de error reducido). Contra `DecisionTreeClassifier` de scikit-learn, con profundidad 4, las predicciones coinciden en el 98,8 %; las diferencias vienen del desempate entre cortes igual de buenos.

| Afirmación | Verificación |
|---|---|
| Nodo 90/10, corte (20,10) / (70,0) | $\Delta i$: clasificación 0,000; Gini 0,047; entropía 0,194 |
| Nodo (20,10) | Gini 0,444; entropía 0,918; clasificación 0,333 |
| Efecto horizonte (XOR, 400 puntos) | Mejor $\Delta i$ en la raíz: 0,0074. Con $\beta=0{,}01$: 1 hoja y error 0,453. Sin parada: 4 hojas y error 0 |
| Sobreajuste (círculo con 15 % de ruido, 20 semillas) | Árbol entero: 67 hojas y prueba 0,279. Podado con validación: 24 hojas y 0,225 (mejor en 20 de 20). Mejor profundidad: 4, con 0,214 |
| Frontera oblicua | Hojas del árbol puro: 6 (50 patrones), 14 (200), 29 (800); un nodo multivariado alcanza |
| Inestabilidad | Mover un punto 0,05 cambia la raíz de $x_2$ a $x_1$; cambia de clase el 23,5 % del cuadrado |

## Carpetas

- `../imagenes/`: los 7 PNG y el script que los genera (numpy y matplotlib; scikit-learn es opcional, sólo para el control).
- `../build/`: el filtro y el estilo para regenerar el PDF con Pandoc (figuras fijas en su lugar, como en 07).

## Regenerar

```bash
python3 ../imagenes/graficos_arboles.py
../build/construir.sh 01-arboles-de-decision.md
```
