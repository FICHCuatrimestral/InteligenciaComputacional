# Verifica los números que cita Resumenes/01-tp7.md (los resultados de las corridas salen del notebook TP7.ipynb)
import csv

# velocidad a mano (1 dimension)
x, v, y, y_hat = 2, 0.5, 1, 0
w, c1, c2, r1, r2 = 0.73, 1.5, 1.5, 0.5, 0.8
inercia = w * v
cognitivo = c1 * r1 * (y - x)
social = c2 * r2 * (y_hat - x)
v_nueva = inercia + cognitivo + social
print("inercia", inercia, " cognitivo", cognitivo, " social", social, " v", round(v_nueva, 3), " x", round(x + v_nueva, 3))

# probabilidad de la hormiga en la ciudad 0
D = [[float(v) for v in fila] for fila in csv.reader(open("../gr17.csv"))]
candidatas = [6, 5, 2]
pesos = [0.1 * (1 / D[0][j]) for j in candidatas]
for j, p in zip(candidatas, pesos):
    print("ciudad", j, "d =", D[0][j], " peso", round(p, 6), " p =", round(p / sum(pesos), 3))

# deposito con Q = 1, recorrido de largo 2100, tramo 0-6
print("global", round(1 / 2100, 6), " uniforme", 1, " local", round(1 / D[0][6], 4))
print("evaporacion rho 0.1 sobre 0.5:", 0.9 * 0.5)
print("rho 0.01: queda despues de 200 iteraciones", round(0.99**200, 3), " rho 0.5 despues de 10:", round(0.5**10, 4))
