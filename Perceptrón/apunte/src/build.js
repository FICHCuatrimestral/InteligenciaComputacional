/* Compila contenido.html -> apunte.html (autocontenido) y apunte.pdf */
const fs = require('fs');
const path = require('path');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({packages: AllPackages, inlineMath: [['$', '$']]});
const svg = new SVG({fontCache: 'none'});
const doc = mathjax.document('', {InputJax: tex, OutputJax: svg});

function render(src, display) {
  const node = doc.convert(src, {display, em: 16, ex: 8, containerWidth: 700});
  let out = adaptor.outerHTML(node);
  out = out.replace(/<mjx-container[^>]*>/, '').replace(/<\/mjx-container>$/, '');
  return display ? `<div class="eq">${out}</div>` : `<span class="ieq">${out}</span>`;
}

const DIR = '/home/claude/work';
let body = fs.readFileSync(path.join(DIR, 'contenido.html'), 'utf8');

// figuras: {{fig01_neurona}}
body = body.replace(/\{\{([a-z0-9_]+)\}\}/g, (m, name) => {
  const f = path.join(DIR, 'figs/out', name + '.svg');
  if (!fs.existsSync(f)) { console.error('FALTA FIGURA:', name); return m; }
  return fs.readFileSync(f, 'utf8');
});

// math
const protect = [];
body = body.replace(/<code[\s\S]*?<\/code>|<pre[\s\S]*?<\/pre>/g, (m) => {
  protect.push(m); return `@@P${protect.length - 1}@@`;
});
body = body.replace(/\$\$([\s\S]+?)\$\$/g, (m, s) => render(s.trim(), true));
body = body.replace(/\$([^$\n]+?)\$/g, (m, s) => render(s.trim(), false));
body = body.replace(/@@P(\d+)@@/g, (m, i) => protect[+i]);

const css = fs.readFileSync(path.join(DIR, 'estilo.css'), 'utf8');
const html = `<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perceptrón simple — material de estudio</title>
<style>${css}</style></head><body>${body}</body></html>`;

fs.writeFileSync(path.join(DIR, 'apunte.html'), html);
console.log('HTML ok — ' + (html.length / 1024).toFixed(0) + ' KB');
