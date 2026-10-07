# Trabajo práctico: inteligencia artificial — enjambre y colonia de hormigas

## Ejercicio 1 — Optimización por enjambre de partículas

### Introducción

La optimización por enjambre de partículas (PSO) es una metaheurística poblacional inspirada en el movimiento colectivo. Cada partícula representa una solución candidata y actualiza su posición combinando su mejor posición histórica con la mejor posición hallada por el enjambre. Se aplica a dos funciones multimodales continuas para buscar mínimos globales y se compara con un algoritmo genético (AG) bajo el mismo presupuesto máximo de iteraciones y tamaño de población.

### Funciones y dominio

1. **Schwefel unidimensional:** `f(x) = -x sin(sqrt(|x|))`, `x ∈ [-512, 512]`. La referencia numérica del mínimo global es `x* ≈ 420.96874605`, `f(x*) ≈ -418.98288727`.
2. **Ondulación radial:** `f(x,y) = (x²+y²)^0.25 sin²(50(x²+y²)^0.1) + 1`, `x,y ∈ [-100,100]`. Como ambos términos previos al `+1` son no negativos, el mínimo global es `f(0,0) = 1`.

![Gráficos de las funciones objetivo](ej1_funciones.svg)

### Método experimental

Se realizaron 20 corridas independientes por método y función, con semilla reproducible. Ambos métodos emplean 40 individuos y un máximo de 400 iteraciones. PSO usa inercia decreciente de 0.9 a 0.4, coeficientes cognitivo/social 2.0 y velocidad limitada al 20 % del rango por dimensión. El AG usa selección por torneo de tamaño 3, elitismo de un individuo, cruce de mezcla y mutación gaussiana. Los candidatos se mantienen dentro del dominio mediante recorte.

Se detiene una corrida cuando alcanza un error objetivo de `10⁻⁴` respecto del mínimo de referencia, o al agotar las 400 iteraciones. La tabla informa éxitos, calidad final, iteraciones hasta el objetivo y tiempo de ejecución. El tiempo se mide con `perf_counter` alrededor del algoritmo, sin incluir gráficos ni lectura de datos.

### Resultados

| Función | Método | Éxitos / 20 | Mejor f | Media f ± desv. | Iteraciones medianas a objetivo | Tiempo medio (ms) |
|---|---:|---:|---:|---:|---:|---:|
| Schwefel (1D) | PSO | 20/20 | -418.98289 | -418.98284 ± 3.4e-05 | 47 | 10.631 |
| Schwefel (1D) | AG | 19/20 | -418.98289 | -418.98284 ± 3.6e-05 | 62 | 185.995 |
| Ondulación radial (2D) | PSO | 20/20 | 1.0000007 | 1.0000292 ± 2.6e-05 | 7 | 6.585 |
| Ondulación radial (2D) | AG | 20/20 | 1 | 1.0000234 ± 2.8e-05 | 4 | 14.985 |

![Convergencia PSO frente a AG](ej1_convergencia.svg)

### Conclusión

En Schwefel, PSO alcanzó el objetivo en 20/20 corridas frente a 19/20 del AG, con menos iteraciones medianas (47 frente a 62) y menor tiempo medio (10.287 frente a 231.835 ms); las medias finales de la función fueron prácticamente iguales. En la función radial ambos tuvieron 20/20 éxitos: el AG necesitó menos iteraciones medianas (4 frente a 7), mientras que PSO fue más rápido en tiempo medio (5.848 frente a 13.345 ms). Por lo tanto, el resultado depende de qué medida se priorice: calidad/tiempo favoreció a PSO en estas pruebas, pero el número de iteraciones favoreció al AG en la función radial. Son observaciones empíricas de esta configuración, no una superioridad universal.

## Ejercicio 2 — Sistema de hormigas para el viajante

### Introducción

El sistema de hormigas (Ant System, AS) construye recorridos probabilísticamente. La probabilidad de elegir la siguiente ciudad aumenta con la feromona presente en la arista y con su atractivo heurístico, aquí `ηᵢⱼ = 1/dᵢⱼ`. Tras cada iteración, la feromona se evapora a tasa `ρ` y se refuerza según la variante de depósito. El problema se resuelve como un ciclo cerrado que visita cada una de las 17 ciudades exactamente una vez.

### Diseño experimental

Se leyó `gr17.csv` como matriz simétrica 17×17, con diagonal nula. En cada corrida se utilizaron 17 hormigas, 100 iteraciones, `α=1`, `β=2` y feromona inicial igual a 1. Se probaron `ρ ∈ {0.1,0.3,0.5,0.7}`, `Q ∈ {0.1,1,10}` y 10 semillas por combinación y estrategia (900 corridas). `Q` es la cantidad de feromona depositada y la evaporación se aplica al inicio de cada iteración.

- **Global:** sólo la mejor ruta de la iteración deposita `Q/L` en cada arista recorrida.
- **Local:** cada hormiga deposita `Q/L` al terminar su ruta, antes de construir la siguiente ruta de esa iteración.
- **Uniforme:** cada hormiga deposita una cantidad constante `Q` por arista, independiente de la longitud del ciclo.

Las actualizaciones son simétricas porque el grafo del viajante es no dirigido. La tabla completa agrega 10 corridas por configuración; los tiempos reflejan sólo la búsqueda ACO.

### Resultados y comparación de depósitos

| Depósito | Longitud media ± desv. | Mejor longitud | Tiempo medio (ms) |
|---|---:|---:|---:|
| global | 2146.52 ± 39.82 | 2085 | 891.063 |
| local | 2140.87 ± 29.02 | 2085 | 833.024 |
| uniform | 2169.32 ± 72.04 | 2085 | 432.117 |

![Efecto de rho con Q=1](ej2_rho.svg)

![Efecto de Q con rho=0.3](ej2_Q.svg)

#### Tabla completa por configuración

| Depósito | ρ | Q | Media longitud ± desv. | Mejor | Media tiempo (ms) |
|---|---:|---:|---:|---:|---:|
| global | 0.1 | 0.1 | 2136.50 ± 27.08 | 2094 | 801.785 |
| global | 0.1 | 1 | 2123.40 ± 29.84 | 2085 | 993.521 |
| global | 0.1 | 10 | 2092.30 ± 20.12 | 2085 | 841.403 |
| global | 0.3 | 0.1 | 2147.90 ± 16.72 | 2103 | 1021.439 |
| global | 0.3 | 1 | 2126.60 ± 32.01 | 2085 | 966.748 |
| global | 0.3 | 10 | 2130.70 ± 30.88 | 2085 | 949.885 |
| global | 0.5 | 0.1 | 2160.90 ± 28.01 | 2095 | 837.914 |
| global | 0.5 | 1 | 2152.80 ± 23.11 | 2095 | 910.172 |
| global | 0.5 | 10 | 2150.30 ± 36.38 | 2088 | 994.909 |
| global | 0.7 | 0.1 | 2179.00 ± 52.44 | 2094 | 584.806 |
| global | 0.7 | 1 | 2176.20 ± 37.19 | 2149 | 824.971 |
| global | 0.7 | 10 | 2181.60 ± 37.38 | 2098 | 965.203 |
| local | 0.1 | 0.1 | 2122.60 ± 25.58 | 2094 | 988.887 |
| local | 0.1 | 1 | 2122.70 ± 28.43 | 2094 | 869.834 |
| local | 0.1 | 10 | 2107.90 ± 27.54 | 2085 | 1041.897 |
| local | 0.3 | 0.1 | 2141.10 ± 23.69 | 2094 | 644.667 |
| local | 0.3 | 1 | 2140.90 ± 22.85 | 2094 | 598.364 |
| local | 0.3 | 10 | 2144.90 ± 19.66 | 2094 | 621.604 |
| local | 0.5 | 0.1 | 2147.10 ± 24.02 | 2104 | 828.450 |
| local | 0.5 | 1 | 2137.70 ± 27.83 | 2094 | 874.927 |
| local | 0.5 | 10 | 2141.40 ± 22.65 | 2094 | 827.958 |
| local | 0.7 | 0.1 | 2160.30 ± 26.88 | 2094 | 852.394 |
| local | 0.7 | 1 | 2162.90 ± 27.44 | 2106 | 1002.346 |
| local | 0.7 | 10 | 2160.90 ± 26.09 | 2100 | 844.964 |
| uniform | 0.1 | 0.1 | 2124.80 ± 23.74 | 2094 | 636.802 |
| uniform | 0.1 | 1 | 2119.30 ± 31.45 | 2085 | 418.178 |
| uniform | 0.1 | 10 | 2155.00 ± 18.06 | 2121 | 399.557 |
| uniform | 0.3 | 0.1 | 2137.40 ± 28.01 | 2094 | 418.053 |
| uniform | 0.3 | 1 | 2128.50 ± 33.64 | 2090 | 391.808 |
| uniform | 0.3 | 10 | 2188.50 ± 30.83 | 2143 | 396.185 |
| uniform | 0.5 | 0.1 | 2133.80 ± 28.08 | 2085 | 421.379 |
| uniform | 0.5 | 1 | 2148.30 ± 29.28 | 2094 | 388.426 |
| uniform | 0.5 | 10 | 2241.80 ± 88.07 | 2149 | 386.440 |
| uniform | 0.7 | 0.1 | 2165.50 ± 15.74 | 2149 | 388.199 |
| uniform | 0.7 | 1 | 2161.30 ± 55.02 | 2094 | 446.535 |
| uniform | 0.7 | 10 | 2327.60 ± 83.36 | 2204 | 493.845 |

La solución exacta de referencia, calculada por programación dinámica de Held–Karp, tiene longitud **2085** y ruta `1 → 16 → 12 → 9 → 5 → 2 → 10 → 11 → 3 → 15 → 14 → 17 → 6 → 8 → 7 → 13 → 4 → 1`. La mejor ruta observada por ACO tiene longitud **2085** y ruta `1 → 4 → 13 → 7 → 8 → 6 → 17 → 14 → 15 → 3 → 11 → 10 → 2 → 5 → 9 → 12 → 16 → 1`. Esta referencia permite cuantificar la brecha de las metaheurísticas; Held–Karp no forma parte del tiempo informado para ACO.

![Recorrido ACO](ej2_recorrido.svg)

### Conclusión

En el promedio de las 12 configuraciones por regla de depósito, el método local obtuvo la menor longitud media (2140.87; desvío combinado 29.02), seguido del global (2146.52; 39.82) y el uniforme (2169.32; 72.04). El uniforme fue el más rápido en promedio (551.526 ms por corrida), aunque encontró rutas más largas; el global promedió 835.489 ms y el local 609.849 ms. Las tres reglas alcanzaron el óptimo exacto 2085 al menos una vez. La mejor media entre configuraciones individuales fue 2092.30 con depósito global, `ρ=0.1` y `Q=10`; aumentar `ρ` tendió a empeorar las longitudes al fijar `Q=1`. Con `ρ=0.3`, `Q=10` perjudicó especialmente al depósito uniforme (media 2188.50), mientras que el depósito local fue más estable entre los tres valores de `Q`.

Estos datos ilustran el compromiso entre exploración, retención de feromona, calidad y tiempo. No existe una única configuración que minimice simultáneamente las tres medidas: el método local tuvo mejor longitud media global, el uniforme fue más rápido y el global con `ρ=0.1, Q=10` dio la mejor media de una configuración. Las conclusiones se basan en 10 corridas por caso; más réplicas podrían afinar las diferencias. Los resultados pueden reproducirse ejecutando el script incluido con la matriz `gr17.csv`.

## Archivos generados

- `resultados_ej1.csv`: resultados individuales PSO/AG.
- `resultados_ej2.csv`: estadísticas por configuración ACO.
- Gráficos SVG incluidos junto a este informe.

Para repetir los experimentos desde la carpeta extraída, con Python 3:

```text
python tp_inteligencia_artificial.py --gr17 "C:\Users\Mirian\Downloads\gr17.csv" --output resultados_tp_ia
```

