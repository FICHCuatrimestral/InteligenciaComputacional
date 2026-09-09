# Cómo se construyen los PDF de los apuntes

Los apuntes se escriben en Markdown (`*.md`) y se convierten a PDF con **Pandoc +
XeLaTeX**. El `.md` sigue siendo la fuente editable; el PDF es un derivado.

## Uso

```bash
./build/construir.sh xor-con-tres-neuronas.md
```

Requiere `pandoc` y una distribución de LaTeX con XeLaTeX. Si no los tenés
instalados, pedime el PDF y lo genero yo.

## Bloques de dos columnas

Para que una figura quede al costado del texto en vez de cortarlo:

```markdown
:::: {.fig-der ancho=0.40}
![Epígrafe de la figura.](figuras/02-perceptron-A.png)

Este párrafo y los que sigan quedan a la izquierda de la figura.

Podés poner varios párrafos.
::::
```

- `.fig-der` → figura a la derecha, texto a la izquierda.
- `.fig-izq` → figura a la izquierda, texto a la derecha.
- `ancho` es la fracción del ancho de página que ocupa la figura (por defecto `0.42`).

**Limitación:** dentro de estos bloques van párrafos, listas y ecuaciones, pero
**no tablas ni recuadros**. Las tablas de Pandoc se convierten en `longtable` y no
entran en una columna. Una figura sin bloque (`![...](...)` suelta) sale a todo el
ancho, que es lo correcto para diagramas apaisados.

## Recuadros

Una cita que arranca con `**OJO — ...**`, `**IDEA DE FONDO — ...**`,
`**PARA LA DEFENSA — ...**`, `**EN CRIOLLO — ...**` o `**EN NÚMEROS — ...**` se
convierte automáticamente en un recuadro de color:

```markdown
> **OJO — título del recuadro**
> Contenido del recuadro.
```

## Archivos

| Archivo | Qué hace |
|---|---|
| `construir.sh` | invoca a Pandoc con todas las opciones |
| `apunte.lua` | filtro: dos columnas, recuadros, separadores |
| `estilo.tex` | encabezado LaTeX: colores, tipografías, títulos, pie de página |

| Etiqueta | Para qué se usa | Color |
|---|---|---|
| `OJO` | trampas, errores frecuentes, cosas que se preguntan | naranja |
| `IDEA DE FONDO` | el porqué conceptual detrás de una fórmula | azul |
| `PARA LA DEFENSA` | lo que hay que poder decir en un oral | verde |
| `EN CRIOLLO` | la analogía en palabras, sin ecuaciones | ocre |
| `EN NÚMEROS` | la cuenta hecha sobre el ejemplo del apunte | violeta |
