--[[
  Filtro de Pandoc para los apuntes de Inteligencia Computacional.

  1. Bloques de dos columnas:
       ::: {.fig-der ancho=0.44}
       ![epigrafe](figuras/x.png)

       Texto que acompaña a la figura.
       :::
     .fig-der  -> figura a la derecha, texto a la izquierda
     .fig-izq  -> figura a la izquierda, texto a la derecha
     El atributo `ancho` (fracción del ancho de texto) es opcional.

  2. Recuadros: una cita que empieza con **OJO**, **IDEA DE FONDO** o
     **PARA LA DEFENSA** se convierte en un tcolorbox del color correspondiente.
]]

local COLORES_RECUADRO = {
  ["OJO"]              = "recuadroojo",
  ["IDEA DE FONDO"]    = "recuadroidea",
  ["PARA LA DEFENSA"]  = "recuadrodefensa",
}

-- Pandoc 3 convierte un parrafo con una sola imagen con epigrafe en un bloque
-- Figure, asi que hay que contemplar las dos formas.
local function extraer_imagen(bloque)
  if bloque.t == "Para" and #bloque.content == 1 and bloque.content[1].t == "Image" then
    local imagen = bloque.content[1]
    return imagen.src, imagen.caption
  end
  if bloque.t == "Figure" then
    local encontrada = nil
    pandoc.walk_block(bloque, {
      Image = function(imagen)
        if encontrada == nil then encontrada = imagen end
      end
    })
    if encontrada ~= nil then
      local epigrafe = nil
      if bloque.caption ~= nil and bloque.caption.long ~= nil then
        epigrafe = pandoc.utils.blocks_to_inlines(bloque.caption.long)
      end
      if epigrafe == nil or #epigrafe == 0 then epigrafe = encontrada.caption end
      return encontrada.src, epigrafe
    end
  end
  return nil, nil
end

local function salida_latex()
  return FORMAT == "latex" or FORMAT == "beamer"
end

--------------------------------------------------------------------- columnas
function Div(elemento)
  local a_la_derecha = elemento.classes:includes("fig-der")
  local a_la_izquierda = elemento.classes:includes("fig-izq")
  if not (a_la_derecha or a_la_izquierda) then return nil end
  if not salida_latex() then return nil end   -- en HTML lo resuelve el CSS

  local ruta_imagen, epigrafe, bloques_de_texto = nil, nil, pandoc.List()
  for _, bloque in ipairs(elemento.content) do
    local ruta, pie = nil, nil
    if ruta_imagen == nil then ruta, pie = extraer_imagen(bloque) end
    if ruta ~= nil then
      ruta_imagen, epigrafe = ruta, pie
    else
      bloques_de_texto:insert(bloque)
    end
  end
  if ruta_imagen == nil then return nil end

  local ancho_figura = tonumber(elemento.attributes["ancho"] or "0.42")
  local ancho_texto = 0.95 - ancho_figura

  -- El texto se convierte a LaTeX aca mismo para poder emitir las dos minipages
  -- en UN solo bloque: si quedaran en bloques separados, Pandoc intercalaria
  -- lineas en blanco (\par) y las columnas se apilarian una debajo de la otra.
  local texto_latex = pandoc.write(pandoc.Pandoc(bloques_de_texto), "latex")

  local figura_latex = "\\includegraphics[width=\\linewidth]{" .. ruta_imagen .. "}"
  if epigrafe and #epigrafe > 0 then
    local pie_latex = pandoc.write(pandoc.Pandoc({pandoc.Plain(epigrafe)}), "latex")
    pie_latex = pie_latex:gsub("%s+$", "")
    figura_latex = figura_latex .. "\\\\[0.45em]\n{\\small\\itshape " .. pie_latex .. "}"
  end

  local columna_figura = "\\begin{minipage}[t]{" .. string.format("%.3f", ancho_figura)
    .. "\\textwidth}\\vspace{0pt}\\centering\n" .. figura_latex .. "\n\\end{minipage}"
  local columna_texto = "\\begin{minipage}[t]{" .. string.format("%.3f", ancho_texto)
    .. "\\textwidth}\\vspace{0pt}\\setlength{\\parskip}{0.6em}\n"
    .. texto_latex .. "\n\\end{minipage}"

  local izquierda, derecha
  if a_la_izquierda then
    izquierda, derecha = columna_figura, columna_texto
  else
    izquierda, derecha = columna_texto, columna_figura
  end

  return pandoc.RawBlock("latex",
    "\\medskip\\noindent\n" .. izquierda .. "\\hfill%\n" .. derecha .. "\n\\par\\medskip")
end

------------------------------------------------------------------- separadores
-- Las lineas ---: sobran en el PDF, las secciones ya separan.
function HorizontalRule()
  if salida_latex() then return {} end
  return nil
end

--------------------------------------------------------------------- recuadros
function BlockQuote(elemento)
  if not salida_latex() then return nil end
  local primer_bloque = elemento.content[1]
  if primer_bloque == nil or primer_bloque.t ~= "Para" then return nil end

  local primer_inline = primer_bloque.content[1]
  if primer_inline == nil or primer_inline.t ~= "Strong" then return nil end

  local encabezado = pandoc.utils.stringify(primer_inline)
  local etiqueta = encabezado:match("^([^—%-]+)")
  etiqueta = etiqueta and etiqueta:gsub("%s+$", "") or ""
  local entorno = COLORES_RECUADRO[etiqueta]
  if entorno == nil then return nil end

  -- Se quita el titulo del cuerpo: pasa a ser el titulo del recuadro.
  local resto = pandoc.List()
  for indice = 2, #primer_bloque.content do
    resto:insert(primer_bloque.content[indice])
  end
  while #resto > 0 and resto[1].t == "Space" do resto:remove(1) end
  if #resto > 0 and resto[1].t == "LineBreak" then resto:remove(1) end

  local cuerpo = pandoc.List()
  if #resto > 0 then cuerpo:insert(pandoc.Para(resto)) end
  for indice = 2, #elemento.content do
    cuerpo:insert(elemento.content[indice])
  end

  -- El titulo puede contener matematica ($w_C$), asi que se convierte a LaTeX
  -- en vez de aplanarlo a texto plano.
  local titulo_latex = pandoc.write(
    pandoc.Pandoc({pandoc.Plain(primer_inline.content)}), "latex")
  titulo_latex = titulo_latex:gsub("%s+$", "")

  local resultado = pandoc.List()
  resultado:insert(pandoc.RawBlock("latex",
    "\\begin{" .. entorno .. "}{" .. titulo_latex .. "}"))
  resultado:extend(cuerpo)
  resultado:insert(pandoc.RawBlock("latex", "\\end{" .. entorno .. "}"))
  return resultado
end
