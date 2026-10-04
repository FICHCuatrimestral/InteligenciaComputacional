"""Experimentos extra del apunte de defensa (01-defensa-tp6.md).

Toma las definiciones del notebook TP6-v2.ipynb (las celdas del motor, del
ejercicio 1 y del ejercicio 2, sin las corridas ni los gráficos) y corre:
  - la validación anidada (prefiltro y AG recalculados sin el paciente que se valida),
  - el AG sin prefiltro (sobre los 7129 genes),
  - el barrido de beta,
  - la comparación con y sin normalizar.
Se corre desde Practicas/TP6/:   python3 Resumenes/experimentos_defensa.py
Tarda unos 5 minutos.
"""
import json, math, sys
import matplotlib
matplotlib.use("Agg")

nb = json.load(open("TP6-v2.ipynb", encoding="utf-8"))
codigo = "\n".join("".join(nb["cells"][i]["source"]) for i in (2, 3, 5, 19, 20, 21, 22, 23))
exec(codigo)

Xtr, ytr = X_train, y_train

def sn_sin(j, idx):
    a = [Xtr[i][j] for i in idx if ytr[i] == 0]; b = [Xtr[i][j] for i in idx if ytr[i] == 1]
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sa = math.sqrt(sum((v - ma) ** 2 for v in a) / len(a)); sb = math.sqrt(sum((v - mb) ** 2 for v in b) / len(b))
    return abs(ma - mb) / (sa + sb)

print("un error en un AML de test baja el UAR", 1 / 14 / 2, "; en un ALL", 1 / 20 / 2)

# validación anidada: los 10 mejores del ranking
pred = []
for i in range(len(Xtr)):
    idx = [k for k in range(len(Xtr)) if k != i]
    sn = sorted(((sn_sin(j, idx), j) for j in range(n_genes)), reverse=True)
    pred.append(clasificar(Xtr[i], [Xtr[k] for k in idx], [ytr[k] for k in idx], [j for _, j in sn[:10]]))
print("top 10, validación anidada:", round(uar(ytr, pred), 3), " ingenua:", uar_validacion(candidatos[:10]))

# validación anidada: prefiltro + AG (semilla 0)
pred, tam = [], []
for i in range(len(Xtr)):
    idx = [k for k in range(len(Xtr)) if k != i]
    sn = sorted(((sn_sin(j, idx), j) for j in range(n_genes)), reverse=True)
    X_train = [Xtr[k] for k in idx]; y_train = [ytr[k] for k in idx]     # uar_validacion usa estas globales
    genes, _ = SeleccionDeGenes([j for _, j in sn[:50]], semilla=0).ejecutar()
    tam.append(len(genes))
    pred.append(clasificar(Xtr[i], X_train, y_train, genes))
X_train, y_train = Xtr, ytr
print("prefiltro + AG, validación anidada:", round(uar(ytr, pred), 3), " genes promedio:", sum(tam) / len(tam))
sys.stdout.flush()

for beta in (0.0, 0.2, 0.5):
    filas = []
    for s in range(5):
        g, _ = SeleccionDeGenes(candidatos, beta=beta, semilla=s).ejecutar()
        filas.append((len(g), round(uar_validacion(g), 3), round(uar_test(g), 3)))
    print("beta", beta, filas, "test promedio", round(sum(f[2] for f in filas) / 5, 3)); sys.stdout.flush()

for s in range(5):
    g, _ = SeleccionDeGenes(list(range(n_genes)), semilla=s).ejecutar()
    print("sin prefiltro, semilla", s, "genes", len(g), "val", round(uar_validacion(g), 3), "test", round(uar_test(g), 3)); sys.stdout.flush()

Xr, yr = leer_csv("leukemia_train.csv"); Xt, yt = leer_csv("leukemia_test.csv")
crudo = lambda genes: uar(yt, [clasificar(p, Xr, yr, genes) for p in Xt])
print("todos los genes: normalizado", round(uar_test(list(range(n_genes))), 3), "crudo", round(crudo(list(range(n_genes))), 3))
print("top 10: normalizado", round(uar_test(candidatos[:10]), 3), "crudo", round(crudo(candidatos[:10]), 3))
