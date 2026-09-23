#!/usr/bin/env bash
set -euo pipefail
B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pandoc "${1:-algoritmos.md}" --from=markdown+fenced_divs+pipe_tables+tex_math_dollars --pdf-engine=xelatex \
 --lua-filter="$B/apunte.lua" --include-in-header="$B/estilo.tex" -V geometry:"a4paper,margin=2.0cm" -V fontsize:10pt \
 -V linestretch:1.05 -V colorlinks:true -V lang:es -V fontfamily:"" -V mainfont:"TeX Gyre Pagella" -V sansfont:"TeX Gyre Heros" \
 -V monofont:"DejaVu Sans Mono" -o "$(basename "${1:-algoritmos.md}" .md).pdf"
