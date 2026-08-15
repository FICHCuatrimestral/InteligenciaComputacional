# Inteligencia Computacional

Material de la cursada de Inteligencia Computacional (Ingeniería en Informática, FICH–UNL).

---

## Cómo empezar

Guía para clonar el repositorio y poder trabajar sobre él. Si nunca usaste Git, seguí los
cuatro pasos en orden.

### 1. Instalar Git

- **Windows:** descargar el instalador de [git-scm.com](https://git-scm.com/download/win) y
  aceptar las opciones por defecto. Incluye *Git Bash* y el gestor de credenciales.
- **Linux (Debian/Ubuntu):** `sudo apt install git`
- **macOS:** `brew install git`, o `xcode-select --install`.

Para verificar que quedó instalado:

```bash
git --version
```

### 2. Configurar Git

Estos datos quedan registrados en cada commit que hagas, así que conviene usar el nombre y
el correo reales. Se configuran una sola vez por computadora:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.correo@ejemplo.com"
```

Recomendado además:

```bash
# Que las ramas nuevas se llamen "main" en lugar de "master"
git config --global init.defaultBranch main

# Manejo de fines de línea (evita que todo el archivo aparezca como modificado)
git config --global core.autocrlf true    # en Windows
git config --global core.autocrlf input   # en Linux o macOS
```

> El ajuste de `core.autocrlf` importa cuando el equipo mezcla sistemas operativos: Windows
> termina las líneas con CRLF y Linux/macOS con LF. Sin esta configuración, Git puede marcar
> archivos enteros como modificados aunque no hayas tocado nada.

Para revisar cómo quedó todo:

```bash
git config --global --list
```

### 3. Clonar el repositorio

```bash
git clone https://github.com/FICHCuatrimestral/InteligenciaComputacional.git
cd InteligenciaComputacional
```

> **Ojo con el tamaño:** el repositorio incluye la bibliografía de la cátedra en PDF, así que
> la clonación descarga alrededor de 300 MB. Puede demorar unos minutos según la conexión.

La primera vez que hagas `push`, GitHub va a pedirte que te autentiques. **La contraseña de
tu cuenta no sirve**: hay que usar un *Personal Access Token*.

1. Entrar a GitHub → *Settings* → *Developer settings* → *Personal access tokens* →
   *Tokens (classic)* → *Generate new token*.
2. Marcar el permiso `repo` y generar el token.
3. Copiarlo (se muestra una sola vez) y pegarlo cuando Git pida la contraseña.

En Windows el gestor de credenciales lo guarda y no vuelve a preguntar. Como alternativa
podés configurar una clave SSH siguiendo la
[guía oficial de GitHub](https://docs.github.com/es/authentication/connecting-to-github-with-ssh).

### 4. Flujo de trabajo

Antes de empezar a trabajar, traer los cambios de los demás:

```bash
git pull
```

Después de modificar archivos:

```bash
git status                      # ver qué cambió
git add .                       # preparar los cambios
git commit -m "Descripción breve de lo que hiciste"
git push                        # subirlos al repositorio
```

Si `git push` es rechazado porque alguien subió cambios antes que vos, resolvelo con:

```bash
git pull --rebase
git push
```

---

## Contenido del repositorio

| carpeta | qué contiene |
|---|---|
| `Perceptrón/TP1/` | resolución de la Guía de trabajos prácticos 1 |
| `Perceptrón/apunte/` | apunte de estudio de la Unidad 1 y transcripciones de las clases |
| `Bibliografía/` | libros y papers de la cátedra |
| `Planificacion.pdf` | planificación de la materia presentada a Secretaría Académica |

## Trabajos prácticos

- **[TP1 — Perceptrón simple](Perceptrón/TP1/)** — implementación del perceptrón simple con
  cantidad variable de entradas, visualización de la recta de separación durante el
  entrenamiento y análisis del comportamiento frente a datos con distinta dispersión.
  Todo el desarrollo está en [`TP1.ipynb`](Perceptrón/TP1/TP1.ipynb); las instrucciones para
  ejecutarlo están en el [README del TP](Perceptrón/TP1/README.md).

## Apuntes

- **[Perceptrón simple](Perceptrón/apunte/)** — material de estudio de la Unidad 1,
  construido sobre las clases 001–005 y cruzado con Haykin, Freeman & Skapura y Kosko.
  Incluye una [versión en PDF de 46 páginas](Perceptrón/apunte/Perceptron-simple-apunte.pdf)
  y las transcripciones de las clases.

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

La carpeta `Bibliografía/` reúne el material de cátedra: Haykin, Bishop, Kosko y
Freeman-Skapura para redes neuronales; Zadeh y Siler-Buckler para lógica borrosa; Goldberg,
Michalewicz, Mitchell y Koza para computación evolutiva; Kennedy-Eberhart y Dorigo-Stützle
para inteligencia de enjambres.

## Proyecto

Todavía por definir — la idea es un proyecto que crezca junto con la cursada, sumando una
técnica nueva a medida que se va dando en clase, en vez de encararlo todo de una. Se va a
documentar acá a medida que tome forma.
