# TP1 — Perceptrón simple

Resolución de la Guía de trabajos prácticos 1 de Inteligencia Computacional (FICH–UNL).

El desarrollo completo —consignas, código ejecutable, resultados y análisis— está en
**[`TP1.ipynb`](TP1.ipynb)**. El notebook está guardado sin resultados, así que hay que
ejecutarlo para ver las salidas y los gráficos.

## Contenido

| ruta | qué es |
|---|---|
| `TP1.ipynb` | notebook principal: los tres ejercicios con su análisis |
| `src/perceptron.py` | clase `Perceptron`: pesos, umbral, activación, entrenamiento y prueba |
| `src/data_loader.py` | lectura de los archivos de patrones separados por comas |
| `src/graficos.py` | rutinas de graficación |
| `Dataset/` | archivos de patrones provistos por la cátedra |
| `IC_GTP1.pdf` | enunciado original |

## Cómo ejecutarlo

Hace falta Python 3.10 o superior.

**1. Clonar el repositorio y ubicarse en esta carpeta**

```bash
git clone https://github.com/FICHCuatrimestral/InteligenciaComputacional.git
cd "InteligenciaComputacional/Perceptrón/TP1"
```

**2. Crear un entorno virtual e instalar las dependencias**

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Abrir el notebook**

Con **VS Code**: abrir `TP1.ipynb` y, cuando pida el kernel, elegir el intérprete de
`.venv`. Requiere tener instalada la extensión *Jupyter* de Microsoft.

Con **Jupyter** en el navegador:

```bash
pip install notebook
jupyter notebook TP1.ipynb
```

**4. Ejecutar todas las celdas** (en VS Code, botón *Run All*).

> **Importante:** el notebook debe ejecutarse desde esta carpeta (`Perceptrón/TP1`), porque
> importa el paquete `src/` y busca los datos en `Dataset/` mediante rutas relativas. Tanto
> VS Code como Jupyter usan por defecto la carpeta del notebook como directorio de trabajo,
> así que abriéndolo normalmente funciona sin necesidad de configurar nada.

## Reproducibilidad

Los pesos se inicializan con una semilla fija (`semilla = 42`), de modo que todas las
corridas dan exactamente los mismos resultados que los citados en el análisis.
