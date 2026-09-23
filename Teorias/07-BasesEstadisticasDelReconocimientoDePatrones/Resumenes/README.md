# Apuntes — Bases estadísticas del reconocimiento de patrones

Inteligencia Computacional · FICH-UNL · César Martínez

| Archivo | Qué es |
|---|---|
| `01-bases-estadisticas.md` | La unidad completa: aprendizaje maquinal y las dos ramas de la IA, patrón y diagrama de bloques, las aproximaciones geométrica y sintáctica sobre el mismo OCR, patrón / características / clases, el clasificador estadístico (regiones, fronteras, lineal y cuadrático con el conteo de parámetros deducido), las cuatro probabilidades con los números de la lámina 31, la regla de Bayes deducida, el clasificador de Bayes, su error y por qué es mínimo, el efecto de la a priori, por qué no se puede construir, tres desarrollos para el pizarrón, formulario, errores típicos y autoevaluación |

Fuentes: `Introducción al reconocimiento estadístico de patrones.pdf` (44 láminas) y las transcripciones 001 a 007. Este apunte reemplaza la versión sin figuras del commit «faltantes».

## Lo que hay que saber de las fuentes

- **Las transcripciones son buenas** (siete clases, sin duplicados ni saltos). De ahí salen los dos ejemplos que atraviesan la unidad: la anemia con los «dos contenedores» y el brillo de los dígitos.
- **Las láminas con figura no tienen el desarrollo escrito**: el diagrama funcional (13), el OCR geométrico y sintáctico (15 a 19), los histogramas con $g_0$ y $g_1$ (26), los planos (27) y las curvas de probabilidad (31 y 33). Están reconstruidas en las figuras 1 a 8. El código de contorno de la figura 2 lo calcula el script.
- **Lámina 31:** $P(x=45,\omega=0)$ figura como 0,016, pero $0{,}5\times0{,}033 = 0{,}0165$ (truncamiento). Además, $P(x|\omega)$ es una **densidad**, no una probabilidad: el apunte lo aclara con un OJO.
- **Lámina 26:** con las fórmulas de la lámina, la frontera es $x=45{,}5$ y en $x=55$ vale $g_1=0{,}35$ y $g_0=0{,}16$. En la clase se dicen 45, 0,32 y 0,2, que son lecturas a ojo del gráfico.
- **El «brillo 40 → 0,8 y 0,2» de la clase es ilustrativo.** Con densidades que respetan los números de la lámina 31, ese 0,8/0,2 aparece cerca de $x=42{,}5$.
- **Dos cosas que la lámina afirma sin mostrar, y el apunte desarrolla:** por qué el de Bayes es de mínimo error (argumento punto a punto, más un barrido de umbrales) y por qué el cuadrático tiene $\tfrac12 d(d+1)+d+1$ parámetros (simetría de $\mathbf W$).

## Números del apunte

Todos salen de `../imagenes/graficos_bayes.py`. Las dos gaussianas del ejemplo (0: $\mu=38{,}9$, $\sigma=4{,}2$; 9: $\mu=48{,}1$, $\sigma=2{,}7$) se calcularon para reproducir la lámina 31: picos de 0,095 y 0,147, $p(45|0)=0{,}033$ y $p(45)=0{,}054$.

| Afirmación | Verificación |
|---|---|
| Las cuatro probabilidades en $x=45$ | 0,5; 0,0330; 0,0165; 0,0540; y $P(45\vert9)=0{,}075$ |
| A posteriori en 45 | $P(0\vert45)=0{,}306$, $P(9\vert45)=0{,}694$ |
| Frontera de Bayes | $x^* = 43{,}99$ (y un segundo cruce en 65,6: regiones no conexas) |
| Error de Bayes | 0,0876, por la fórmula cerrada y por integración numérica |
| Bayes es mínimo | Umbral 40: 0,199; 42: 0,121; **44: 0,0876**; 45: 0,098; 48: 0,247 |
| Efecto de la a priori | $P(0)=0{,}9$: frontera 47,0, error 0,058; $P(0)=0{,}99$: error 0,0100, igual al del trivial |
| Parámetros | $d=2$: 3 y 6; $d=10$: 11 y 66; $d=100$: 101 y 5151 |

## Carpetas

- `../imagenes/`: los 8 PNG y el script de Python que los genera.
- `../Transcripciones/`: las transcripciones de la clase.
- `../build/`: el filtro y el estilo para regenerar el PDF con Pandoc. `estilo.tex` fija las figuras en su lugar (`float` con `H`): con figuras flotantes, los recuadros partibles desbordaban la página sobre el pie.

## Regenerar

```bash
python3 ../imagenes/graficos_bayes.py
../build/construir.sh 01-bases-estadisticas.md
```
