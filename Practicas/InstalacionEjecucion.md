# Instalación y ejecución

Guía común para los TPs de esta carpeta (`TP1`, `TP2`, ...). Cada TP es una carpeta
autocontenida con su propio notebook, código y datos:

| ruta (dentro de cada `TPx/`) | qué es |
|---|---|
| `TP.ipynb` | notebook principal con los ejercicios y su análisis |
| `src/` | código reutilizado por el notebook (carga de datos, gráficos, etc.) |
| `Dataset/` | archivos de patrones provistos por la cátedra |
| `IC_GTPx.pdf` | enunciado original |

Las dependencias (`requirements.txt`) están acá, en `Perceptrón/`, compartidas por todos los TPs.

## Cómo ejecutarlo

Hace falta Python 3.10 o superior y **Visual Studio Code**. No hace falta abrir Jupyter en el
navegador: se trabaja íntegramente dentro de VS Code.

### 1. Instalar las extensiones de VS Code

En VS Code, abrir el panel de extensiones (`Ctrl+Shift+X`) e instalar estas dos, ambas
publicadas por **Microsoft**:

| extensión | identificador | para qué |
|---|---|---|
| **Python** | `ms-python.python` | reconocer el intérprete y los entornos virtuales |
| **Jupyter** | `ms-toolsai.jupyter` | abrir y ejecutar archivos `.ipynb` |


Buscar por el identificador (por ejemplo `ms-toolsai.jupyter`) evita instalar alguna de las
muchas extensiones parecidas de terceros. Alternativamente, desde una terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

### 2. Ubicarse en la carpeta del TP

Abrir en VS Code la carpeta del TP que corresponda, por ejemplo `Perceptrón/TP1` o
`Perceptrón/TP2` (*Archivo → Abrir carpeta…*).

> **Importante:** hay que abrir **esa** carpeta (`TPx/`), no `Perceptrón/` ni la raíz del
> repositorio. Cada notebook importa su paquete `src/` y busca los datos en `Dataset/`
> mediante rutas relativas, así que si se abre desde otro lado fallan el `import` y la
> lectura de los CSV.

### 3. Crear el entorno virtual e instalar las dependencias

En la terminal integrada de VS Code (`Ctrl+Ñ`), estando en la carpeta del TP (`TPx/`):

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

> Si PowerShell bloquea la activación con un error de *execution policy*, ejecutar una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 4. Abrir el notebook y elegir el kernel

Abrir `TP.ipynb`. Arriba a la derecha aparece el botón **Select Kernel**: elegir
*Python Environments…* y seleccionar el intérprete que dice `.venv` (queda marcado como
**Recommended**).

Si `.venv` no aparece en la lista, cerrar y volver a abrir VS Code para que detecte el
entorno recién creado.

### 5. Ejecutar

Botón **Run All** en la barra superior del notebook, o `Ctrl+Enter` celda por celda.

> Las celdas que generan animaciones o entrenan sobre datos que no separan linealmente pueden
> tardar un par de minutos. Es esperable, no significa que se haya colgado.
