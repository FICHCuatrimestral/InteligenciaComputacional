# Inteligencia Computacional

Material de la cursada de Inteligencia Computacional (Ingeniería en Informática, FICH–UNL). Esta es la materia que estoy cursando este cuatrimestre — va a tener más dedicación que el resto del repositorio.

## Temario

**1. Redes neuronales.**

- **Perceptrón multicapa (MLP):** la red neuronal "clásica" — capas de neuronas totalmente conectadas, entrenadas típicamente con backpropagation. Es el punto de partida para todo lo demás: aprendizaje supervisado por descenso de gradiente sobre una función de error.
- **Redes con funciones de base radial (RBF):** en vez de la activación sigmoidea/ReLU del MLP, cada neurona de la capa oculta responde según la distancia a un centro (típicamente una gaussiana) — útil para interpolación y clasificación con fronteras de decisión localizadas.
- **Mapas auto-organizativos (SOM, de Kohonen):** aprendizaje **no supervisado** — la red se auto-organiza para proyectar datos de alta dimensión sobre una grilla de baja dimensión (2D), preservando relaciones de vecindad. Sirve para clustering y visualización.
- **Redes de Hopfield:** red recurrente completamente conectada que funciona como memoria asociativa — converge a un "mínimo de energía" que corresponde a un patrón aprendido, útil para reconstruir patrones a partir de versiones incompletas o ruidosas.

**2. Introducción a los sistemas basados en conocimiento.** Sistemas que representan y razonan sobre conocimiento explícito (reglas, hechos) en vez de aprenderlo de datos — el puente conceptual hacia la lógica borrosa, que es una forma de representar conocimiento impreciso.

**3. Lógica borrosa (fuzzy logic).**

- **Teoría de los conjuntos borrosos:** a diferencia de la lógica clásica (pertenece / no pertenece), un elemento puede pertenecer a un conjunto con un grado de membresía entre 0 y 1 — formaliza matemáticamente conceptos imprecisos del lenguaje natural ("bastante caliente", "casi lleno").
- **Memorias asociativas borrosas (FAM):** extienden la idea de memoria asociativa (como Hopfield) al dominio borroso, mapeando conjuntos borrosos de entrada a conjuntos borrosos de salida.
- **Sistemas de control borroso:** la aplicación más extendida de la lógica borrosa — un controlador que decide una acción a partir de reglas del tipo "SI la temperatura es alta Y la humedad es baja ENTONCES aumentar el flujo de aire", sin necesitar un modelo matemático exacto del sistema.

**4. Computación evolutiva.**

- **Diseño de la solución de problemas mediante computación evolutiva:** cómo modelar un problema de optimización o búsqueda como una "evolución" — definir la representación de una solución (cromosoma), la función de aptitud (fitness) y los operadores de variación.
- **Algoritmos genéticos:** el algoritmo evolutivo clásico — una población de soluciones candidatas evoluciona mediante selección (las mejores tienen más chances de reproducirse), cruza (combinar dos soluciones) y mutación (variación aleatoria), iterando por generaciones hacia mejores soluciones.
- **Variantes de computación evolutiva:** programación genética (evoluciona programas/árboles de expresión en vez de vectores), estrategias evolutivas, y su relación con otras metaheurísticas bio-inspiradas de optimización por enjambres (PSO, ACO) presentes en la bibliografía de la materia.

**5. Aplicaciones.** Casos de uso reales combinando estas técnicas — reconocimiento de patrones, control, optimización — que es también donde va a vivir el proyecto personal de la materia.

## Bibliografía

La carpeta `Bibliografía-20260811/` tiene el material de cátedra (Haykin, Bishop, Kosko y Freeman-Skapura para redes neuronales; Zadeh y Siler-Buckler para lógica borrosa; Goldberg, Michalewicz, Mitchell y Koza para computación evolutiva; Kennedy-Eberhart y Dorigo-Stützle para inteligencia de enjambres). **No se sube al repositorio**: son libros con derechos de autor y en conjunto pesan varios cientos de MB — no tiene sentido ni es legal tenerlos en un repo público. Quedan solo en la máquina local (ver `.gitignore`).

## Proyecto

Todavía por definir — la idea es un proyecto que crezca junto con la cursada, sumando una técnica nueva a medida que se va dando en clase, en vez de encararlo todo de una. Se va a documentar acá a medida que tome forma.

## Apuntes

- **[Perceptrón simple](Perceptrón/apunte/)** — material de estudio de la Unidad 1, construido
  sobre las clases 001–005 y cruzado con Haykin, Freeman & Skapura y Kosko. Incluye
  [versión PDF de 46 páginas](Perceptrón/apunte/Perceptron-simple-apunte.pdf), 15 figuras
  vectoriales, diagramas editables en Excalidraw y las fuentes para regenerarlo.
