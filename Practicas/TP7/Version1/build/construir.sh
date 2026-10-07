#!/usr/bin/env bash
# Construye el PDF de un apunte a partir del .md.
#   uso: ./build/construir.sh xor-con-tres-neuronas.md
set -euo pipefail

ARCHIVO_MD="${1:?falta el archivo .md}"
DIRECTORIO_BUILD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOMBRE_BASE="$(basename "$ARCHIVO_MD" .md)"

pandoc "$ARCHIVO_MD" \
  --from=markdown+fenced_divs+pipe_tables+tex_math_dollars \
  --to=pdf \
  --pdf-engine=xelatex \
  --lua-filter="$DIRECTORIO_BUILD/apunte.lua" \
  --include-in-header="$DIRECTORIO_BUILD/estilo.tex" \
  --variable=geometry:"a4paper,margin=2.0cm" \
  --variable=fontsize:10pt \
  --variable=linestretch:1.05 \
  --variable=colorlinks:true \
  --variable=lang:es \
  --variable=fontfamily:"" \
  --variable=mainfont:"TeX Gyre Pagella" \
  --variable=sansfont:"TeX Gyre Heros" \
  --variable=monofont:"DejaVu Sans Mono" \
  --shift-heading-level-by=-1 \
  --output="$NOMBRE_BASE.pdf"

echo "generado: $NOMBRE_BASE.pdf"
