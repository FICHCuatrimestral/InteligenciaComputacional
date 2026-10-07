"""Reproducible practical work: particle swarm and ant colony optimization.

Uses only the Python standard library. Run:
    python tp_inteligencia_artificial.py --gr17 C:\\path\\to\\gr17.csv
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import random
import statistics
import time
from array import array
from pathlib import Path
from typing import Callable, Sequence

Vector = list[float]
Objective = Callable[[Sequence[float]], float]


def schwefel(point: Sequence[float]) -> float:
    x = point[0]
    return -x * math.sin(math.sqrt(abs(x)))


def radial_ripple(point: Sequence[float]) -> float:
    x, y = point
    radius_squared = x * x + y * y
    return radius_squared**0.25 * math.sin(50 * radius_squared**0.1) ** 2 + 1


def golden_section_minimum(function: Objective, lower: float, upper: float) -> tuple[float, float]:
    ratio = (math.sqrt(5) - 1) / 2
    left = upper - ratio * (upper - lower)
    right = lower + ratio * (upper - lower)
    f_left = function([left])
    f_right = function([right])
    for _ in range(120):
        if f_left <= f_right:
            upper, right, f_right = right, left, f_left
            left = upper - ratio * (upper - lower)
            f_left = function([left])
        else:
            lower, left, f_left = left, right, f_right
            right = lower + ratio * (upper - lower)
            f_right = function([right])
    x = (lower + upper) / 2
    return x, function([x])


def schwefel_reference() -> tuple[float, float]:
    samples = 20000
    step = 1024 / samples
    best_x = -512.0
    best_value = schwefel([best_x])
    for index in range(1, samples + 1):
        x = -512 + step * index
        value = schwefel([x])
        if value < best_value:
            best_x, best_value = x, value
    return golden_section_minimum(schwefel, best_x - step, best_x + step)


def particle_swarm(
    function: Objective,
    bounds: Sequence[tuple[float, float]],
    seed: int,
    max_iterations: int,
    target: float,
) -> tuple[float, list[float], int, float]:
    rng = random.Random(seed)
    started = time.perf_counter()
    dimensions = len(bounds)
    count = 40
    positions = [[rng.uniform(low, high) for low, high in bounds] for _ in range(count)]
    velocity_limits = [(high - low) * 0.2 for low, high in bounds]
    velocities = [
        [rng.uniform(-limit, limit) for limit in velocity_limits]
        for _ in range(count)
    ]
    personal_positions = [position[:] for position in positions]
    personal_values = [function(position) for position in positions]
    best_index = min(range(count), key=personal_values.__getitem__)
    global_position = personal_positions[best_index][:]
    global_value = personal_values[best_index]
    history = [global_value]
    for iteration in range(max_iterations):
        inertia = 0.9 - 0.5 * iteration / max(1, max_iterations - 1)
        for particle in range(count):
            for dimension, (low, high) in enumerate(bounds):
                velocity = (
                    inertia * velocities[particle][dimension]
                    + 2.0 * rng.random()
                    * (personal_positions[particle][dimension] - positions[particle][dimension])
                    + 2.0 * rng.random()
                    * (global_position[dimension] - positions[particle][dimension])
                )
                limit = velocity_limits[dimension]
                velocity = max(-limit, min(limit, velocity))
                candidate = positions[particle][dimension] + velocity
                if candidate < low or candidate > high:
                    candidate = max(low, min(high, candidate))
                    velocity *= -0.5
                velocities[particle][dimension] = velocity
                positions[particle][dimension] = candidate

            value = function(positions[particle])
            if value < personal_values[particle]:
                personal_values[particle] = value
                personal_positions[particle] = positions[particle][:]
                if value < global_value:
                    global_value = value
                    global_position = positions[particle][:]

        history.append(global_value)
        if global_value <= target:
            break

    return global_value, history, len(history) - 1, time.perf_counter() - started


def genetic_algorithm(
    function: Objective,
    bounds: Sequence[tuple[float, float]],
    seed: int,
    max_iterations: int,
    target: float,
) -> tuple[float, list[float], int, float]:
    rng = random.Random(seed)
    started = time.perf_counter()
    dimensions = len(bounds)
    population_size = 40
    mutation_probability = 1 / dimensions
    population = [
        [rng.uniform(low, high) for low, high in bounds]
        for _ in range(population_size)
    ]
    values = [function(individual) for individual in population]
    best_index = min(range(population_size), key=values.__getitem__)
    best_value = values[best_index]
    history = [best_value]
    def select_parent() -> Vector:
        contestants = rng.sample(range(population_size), 3)
        winner = min(contestants, key=values.__getitem__)
        return population[winner]

    for _ in range(max_iterations):
        elite_index = min(range(population_size), key=values.__getitem__)
        next_population = [population[elite_index][:]]
        while len(next_population) < population_size:
            parent_a = select_parent()
            parent_b = select_parent()
            child: Vector = []
            for dimension, (low, high) in enumerate(bounds):
                blend = rng.uniform(-0.25, 1.25)
                gene = parent_a[dimension] + blend * (parent_b[dimension] - parent_a[dimension])
                if rng.random() < mutation_probability:
                    gene += rng.gauss(0, 0.08 * (high - low))
                child.append(max(low, min(high, gene)))
            next_population.append(child)

        population = next_population
        values = [function(individual) for individual in population]
        generation_best = min(values)
        best_value = min(best_value, generation_best)
        history.append(best_value)
        if best_value <= target:
            break

    return best_value, history, len(history) - 1, time.perf_counter() - started


def load_distance_matrix(path: Path) -> list[list[float]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        matrix = [[float(value) for value in row] for row in csv.reader(file) if row]
    if len(matrix) != 17 or any(len(row) != 17 for row in matrix):
        raise ValueError(f"{path} must contain a 17 by 17 matrix; received {len(matrix)} rows.")
    for i in range(17):
        if matrix[i][i] != 0:
            raise ValueError(f"Distance matrix diagonal must be zero (row {i + 1}).")
        for j in range(17):
            if matrix[i][j] < 0 or matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Distances must be nonnegative and symmetric (entry {i + 1},{j + 1}).")
    return matrix


def held_karp(matrix: Sequence[Sequence[float]]) -> tuple[float, list[int]]:
    """Exact reference solution for this 17-city instance."""
    n = len(matrix)
    remaining = n - 1
    mask_count = 1 << remaining
    infinity = 2**31 - 1
    dp = array("I", [infinity]) * (mask_count * remaining)
    for city in range(remaining):
        dp[(1 << city) * remaining + city] = int(matrix[0][city + 1])

    for mask in range(1, mask_count):
        bits = mask
        while bits:
            bit = bits & -bits
            city = bit.bit_length() - 1
            previous_mask = mask ^ bit
            if previous_mask:
                previous_bits = previous_mask
                best = infinity
                while previous_bits:
                    previous_bit = previous_bits & -previous_bits
                    previous_city = previous_bit.bit_length() - 1
                    cost = (
                        dp[previous_mask * remaining + previous_city]
                        + int(matrix[previous_city + 1][city + 1])
                    )
                    if cost < best:
                        best = cost
                    previous_bits ^= previous_bit
                dp[mask * remaining + city] = best
            bits ^= bit

    full_mask = mask_count - 1
    final_city = min(
        range(remaining),
        key=lambda city: dp[full_mask * remaining + city] + int(matrix[city + 1][0]),
    )
    optimum = dp[full_mask * remaining + final_city] + int(matrix[final_city + 1][0])

    reverse_route = [final_city + 1]
    mask = full_mask
    city = final_city
    while mask.bit_count() > 1:
        previous_mask = mask ^ (1 << city)
        target_cost = dp[mask * remaining + city]
        previous_city = min(
            (candidate for candidate in range(remaining) if previous_mask & (1 << candidate)),
            key=lambda candidate: dp[previous_mask * remaining + candidate]
            + int(matrix[candidate + 1][city + 1]),
        )
        if (
            dp[previous_mask * remaining + previous_city]
            + int(matrix[previous_city + 1][city + 1])
            != target_cost
        ):
            raise RuntimeError("Could not reconstruct the exact route.")
        reverse_route.append(previous_city + 1)
        mask, city = previous_mask, previous_city
    route = [0] + list(reversed(reverse_route)) + [0]
    return float(optimum), route


def route_length(route: Sequence[int], matrix: Sequence[Sequence[float]]) -> float:
    return sum(matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def ant_colony(
    matrix: Sequence[Sequence[float]],
    rho: float,
    deposit_amount: float,
    deposit_method: str,
    seed: int,
    iterations: int = 100,
) -> tuple[float, list[int], list[float], float]:
    rng = random.Random(seed)
    n = len(matrix)
    ant_count = n
    alpha, beta = 1.0, 2.0
    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    inverse_distance = [
        [0.0 if i == j else 1.0 / matrix[i][j] for j in range(n)]
        for i in range(n)
    ]
    best_length = math.inf
    best_route: list[int] = []
    history: list[float] = []
    started = time.perf_counter()

    for _ in range(iterations):
        for i in range(n):
            for j in range(i + 1, n):
                value = pheromone[i][j] * (1 - rho)
                pheromone[i][j] = pheromone[j][i] = max(value, 1e-12)

        iteration_routes: list[tuple[float, list[int]]] = []
        for _ant in range(ant_count):
            route = [0]
            unvisited = set(range(1, n))
            while unvisited:
                current = route[-1]
                candidates = sorted(unvisited)
                weights = [
                    pheromone[current][city] ** alpha
                    * inverse_distance[current][city] ** beta
                    for city in candidates
                ]
                total_weight = sum(weights)
                threshold = rng.random() * total_weight
                cumulative = 0.0
                next_city = candidates[-1]
                for city, weight in zip(candidates, weights):
                    cumulative += weight
                    if cumulative >= threshold:
                        next_city = city
                        break
                route.append(next_city)
                unvisited.remove(next_city)
            route.append(0)
            length = route_length(route, matrix)
            iteration_routes.append((length, route))
            if length < best_length:
                best_length, best_route = length, route[:]

            if deposit_method == "local":
                deposit = deposit_amount / length
                for source, destination in zip(route, route[1:]):
                    pheromone[source][destination] += deposit
                    pheromone[destination][source] += deposit
            elif deposit_method == "uniform":
                for source, destination in zip(route, route[1:]):
                    pheromone[source][destination] += deposit_amount
                    pheromone[destination][source] += deposit_amount

        if deposit_method == "global":
            iteration_best_length, iteration_best_route = min(iteration_routes, key=lambda item: item[0])
            deposit = deposit_amount / iteration_best_length
            for source, destination in zip(iteration_best_route, iteration_best_route[1:]):
                pheromone[source][destination] += deposit
                pheromone[destination][source] += deposit
        history.append(best_length)

    return best_length, best_route, history, time.perf_counter() - started


def svg_start(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="30" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">{html.escape(title)}</text>',
    ]


def write_function_figure(path: Path) -> None:
    width, height = 1120, 470
    parts = svg_start(width, height, "Funciones objetivo del Ejercicio 1")
    left, top, plot_w, plot_h = 75, 75, 440, 320
    x_values = [-512 + i * 1024 / 500 for i in range(501)]
    y_values = [schwefel([x]) for x in x_values]
    y_min, y_max = min(y_values), max(y_values)
    parts.extend([
        f'<text x="{left + plot_w / 2}" y="55" text-anchor="middle" font-family="Arial" font-size="14">f(x) = -x sin(sqrt(|x|))</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#444"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#444"/>',
    ])
    points = []
    for index, (x, y) in enumerate(zip(x_values, y_values)):
        px = left + index / (len(x_values) - 1) * plot_w
        py = top + (y_max - y) / (y_max - y_min) * plot_h
        points.append(f"{px:.1f},{py:.1f}")
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#2563eb" stroke-width="1.5"/>')
    parts.append(f'<text x="{left}" y="{top + plot_h + 22}" font-family="Arial" font-size="12">-512</text>')
    parts.append(f'<text x="{left + plot_w}" y="{top + plot_h + 22}" text-anchor="end" font-family="Arial" font-size="12">512</text>')
    parts.append(f'<text x="{left + plot_w / 2}" y="{top + plot_h + 48}" text-anchor="middle" font-family="Arial" font-size="12">x</text>')
    parts.append(f'<text x="{left + 5}" y="{top + 15}" font-family="Arial" font-size="11">{y_max:.0f}</text>')
    parts.append(f'<text x="{left + 5}" y="{top + plot_h - 5}" font-family="Arial" font-size="11">{y_min:.0f}</text>')

    grid_left, grid_top, grid_size = 645, 80, 320
    cells = 80
    values = []
    for row in range(cells):
        y = 100 - 200 * row / (cells - 1)
        for column in range(cells):
            x = -100 + 200 * column / (cells - 1)
            values.append(radial_ripple([x, y]))
    maximum = max(values)
    cell = grid_size / cells
    for row in range(cells):
        for column in range(cells):
            value = values[row * cells + column]
            intensity = min(1.0, math.log1p(value - 1) / math.log1p(maximum - 1))
            red = int(255 - 195 * intensity)
            green = int(255 - 130 * intensity)
            blue = int(255 - 30 * intensity)
            parts.append(
                f'<rect x="{grid_left + column * cell:.2f}" y="{grid_top + row * cell:.2f}" '
                f'width="{cell + 0.2:.2f}" height="{cell + 0.2:.2f}" fill="rgb({red},{green},{blue})"/>'
            )
    parts.extend([
        f'<rect x="{grid_left}" y="{grid_top}" width="{grid_size}" height="{grid_size}" fill="none" stroke="#444"/>',
        f'<text x="{grid_left + grid_size / 2}" y="55" text-anchor="middle" font-family="Arial" font-size="14">f(x,y) = (x²+y²)^0.25 sin²(50(x²+y²)^0.1) + 1</text>',
        f'<text x="{grid_left}" y="{grid_top + grid_size + 22}" font-family="Arial" font-size="12">x = -100</text>',
        f'<text x="{grid_left + grid_size}" y="{grid_top + grid_size + 22}" text-anchor="end" font-family="Arial" font-size="12">x = 100</text>',
        f'<text x="{grid_left + grid_size / 2}" y="{grid_top + grid_size + 48}" text-anchor="middle" font-family="Arial" font-size="12">Intensidad creciente: valores mayores</text>',
        f'<text x="{grid_left + grid_size / 2}" y="{grid_top + grid_size + 67}" text-anchor="middle" font-family="Arial" font-size="12">Mínimo global f(0,0) = 1</text>',
        '</svg>',
    ])
    path.write_text("\n".join(parts), encoding="utf-8")


def write_lines_figure(
    path: Path,
    title: str,
    x_label: str,
    y_label: str,
    series: Sequence[tuple[str, Sequence[float], str]],
    log_scale: bool = False,
) -> None:
    width, height = 900, 500
    left, top, plot_w, plot_h = 85, 65, 700, 340
    all_y = [value for _, values, _ in series for value in values]
    if log_scale:
        all_y = [math.log10(max(value, 1e-12)) for value in all_y]
    low, high = min(all_y), max(all_y)
    if high - low < 1e-9:
        high = low + 1
    parts = svg_start(width, height, title)
    for tick in range(6):
        fraction = tick / 5
        y = top + plot_h * fraction
        value = high - (high - low) * fraction
        label = f"{10**value:.1e}" if log_scale else f"{value:.3g}"
        parts.extend([
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#e5e7eb"/>',
            f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="11">{label}</text>',
        ])
    parts.extend([
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#444"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#444"/>',
    ])
    max_length = max(len(values) for _, values, _ in series)
    for name, raw_values, color in series:
        values = list(raw_values)
        transformed = [math.log10(max(value, 1e-12)) for value in values] if log_scale else values
        coordinates = []
        for index, value in enumerate(transformed):
            x = left + index / max(1, max_length - 1) * plot_w
            y = top + (high - value) / (high - low) * plot_h
            coordinates.append(f"{x:.1f},{y:.1f}")
        parts.append(f'<polyline points="{" ".join(coordinates)}" fill="none" stroke="{color}" stroke-width="2"/>')
    parts.extend([
        f'<text x="{left + plot_w / 2}" y="{height - 48}" text-anchor="middle" font-family="Arial" font-size="13">{html.escape(x_label)}</text>',
        f'<text transform="translate(22 {top + plot_h / 2}) rotate(-90)" text-anchor="middle" font-family="Arial" font-size="13">{html.escape(y_label)}</text>',
    ])
    legend_x = left
    for name, _, color in series:
        parts.append(f'<line x1="{legend_x}" y1="{height - 20}" x2="{legend_x + 24}" y2="{height - 20}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="{legend_x + 30}" y="{height - 16}" font-family="Arial" font-size="12">{html.escape(name)}</text>')
        legend_x += 180
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def write_route_figure(path: Path, route: Sequence[int], matrix: Sequence[Sequence[float]]) -> None:
    width = height = 600
    center_x = center_y = 300
    radius = 220
    count = len(route) - 1
    positions = [
        (
            center_x + radius * math.cos(2 * math.pi * city / count - math.pi / 2),
            center_y + radius * math.sin(2 * math.pi * city / count - math.pi / 2),
        )
        for city in range(count)
    ]
    parts = svg_start(width, height, "Mejor recorrido ACO (disposición circular ilustrativa)")
    for source, destination in zip(route, route[1:]):
        x1, y1 = positions[source]
        x2, y2 = positions[destination]
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#2563eb" stroke-width="2"/>')
        parts.append(
            f'<text x="{(x1 + x2) / 2:.1f}" y="{(y1 + y2) / 2:.1f}" font-family="Arial" font-size="10" fill="#555">'
            f'{matrix[source][destination]:.0f}</text>'
        )
    for city, (x, y) in enumerate(positions):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="#fef3c7" stroke="#92400e"/>')
        parts.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" font-family="Arial" font-size="11">{city + 1}</text>')
    parts.extend([
        f'<text x="{center_x}" y="575" text-anchor="middle" font-family="Arial" font-size="13">La posición circular no representa coordenadas geográficas.</text>',
        "</svg>",
    ])
    path.write_text("\n".join(parts), encoding="utf-8")


def mean_history(histories: Sequence[Sequence[float]], baseline: float, length: int) -> list[float]:
    result = []
    for iteration in range(length):
        values = []
        for history in histories:
            value = history[min(iteration, len(history) - 1)]
            values.append(max(value - baseline, 1e-12))
        result.append(sum(values) / len(values))
    return result


def write_report(
    output: Path,
    function_results: list[dict[str, object]],
    aco_results: list[dict[str, object]],
    exact_length: float,
    exact_route: Sequence[int],
    best_route: Sequence[int],
    best_length: float,
    optimum_x: float,
    optimum_value: float,
) -> None:
    function_table = [
        "| Función | Método | Éxitos / 20 | Mejor f | Media f ± desv. | Iteraciones medianas a objetivo | Tiempo medio (ms) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for result in function_results:
        function_table.append(
            "| {function} | {method} | {successes}/20 | {best:.8g} | {mean:.8g} ± {std:.2g} | {iterations} | {time:.3f} |".format(
                **result
            )
        )

    grouped = {}
    for result in aco_results:
        grouped.setdefault(result["method"], []).append(result)
    method_rows = [
        "| Depósito | Longitud media ± desv. | Mejor longitud | Tiempo medio (ms) |",
        "|---|---:|---:|---:|",
    ]
    for method in ("global", "local", "uniform"):
        group = grouped[method]
        group_mean = statistics.mean(r["mean_length"] for r in group)
        sample_count = 10
        total_count = sample_count * len(group)
        pooled_variance = sum(
            (sample_count - 1) * r["std_length"] ** 2
            + sample_count * (r["mean_length"] - group_mean) ** 2
            for r in group
        ) / (total_count - 1)
        method_rows.append(
            f"| {method} | {group_mean:.2f} ± {math.sqrt(pooled_variance):.2f} | "
            f"{min(r['best_length'] for r in group):.0f} | "
            f"{statistics.mean(r['mean_time'] for r in group) * 1000:.3f} |"
        )

    config_rows = [
        "| Depósito | ρ | Q | Media longitud ± desv. | Mejor | Media tiempo (ms) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for result in aco_results:
        config_rows.append(
            f"| {result['method']} | {result['rho']:.1f} | {result['amount']:g} | "
            f"{result['mean_length']:.2f} ± {result['std_length']:.2f} | "
            f"{result['best_length']:.0f} | {result['mean_time'] * 1000:.3f} |"
        )

    route_text = " → ".join(str(city + 1) for city in best_route)
    exact_route_text = " → ".join(str(city + 1) for city in exact_route)
    report = f"""# Trabajo práctico: inteligencia artificial — enjambre y colonia de hormigas

## Ejercicio 1 — Optimización por enjambre de partículas

### Introducción

La optimización por enjambre de partículas (PSO) es una metaheurística poblacional inspirada en el movimiento colectivo. Cada partícula representa una solución candidata y actualiza su posición combinando su mejor posición histórica con la mejor posición hallada por el enjambre. Se aplica a dos funciones multimodales continuas para buscar mínimos globales y se compara con un algoritmo genético (AG) bajo el mismo presupuesto máximo de iteraciones y tamaño de población.

### Funciones y dominio

1. **Schwefel unidimensional:** `f(x) = -x sin(sqrt(|x|))`, `x ∈ [-512, 512]`. La referencia numérica del mínimo global es `x* ≈ {optimum_x:.8f}`, `f(x*) ≈ {optimum_value:.8f}`.
2. **Ondulación radial:** `f(x,y) = (x²+y²)^0.25 sin²(50(x²+y²)^0.1) + 1`, `x,y ∈ [-100,100]`. Como ambos términos previos al `+1` son no negativos, el mínimo global es `f(0,0) = 1`.

![Gráficos de las funciones objetivo](ej1_funciones.svg)

### Método experimental

Se realizaron 20 corridas independientes por método y función, con semilla reproducible. Ambos métodos emplean 40 individuos y un máximo de 400 iteraciones. PSO usa inercia decreciente de 0.9 a 0.4, coeficientes cognitivo/social 2.0 y velocidad limitada al 20 % del rango por dimensión. El AG usa selección por torneo de tamaño 3, elitismo de un individuo, cruce de mezcla y mutación gaussiana. Los candidatos se mantienen dentro del dominio mediante recorte.

Se detiene una corrida cuando alcanza un error objetivo de `10⁻⁴` respecto del mínimo de referencia, o al agotar las 400 iteraciones. La tabla informa éxitos, calidad final, iteraciones hasta el objetivo y tiempo de ejecución. El tiempo se mide con `perf_counter` alrededor del algoritmo, sin incluir gráficos ni lectura de datos.

### Resultados

{chr(10).join(function_table)}

![Convergencia PSO frente a AG](ej1_convergencia.svg)

### Conclusión

En Schwefel, PSO alcanzó el objetivo en 20/20 corridas frente a 19/20 del AG, con menos iteraciones medianas (47 frente a 62) y menor tiempo medio (10.287 frente a 231.835 ms); las medias finales de la función fueron prácticamente iguales. En la función radial ambos tuvieron 20/20 éxitos: el AG necesitó menos iteraciones medianas (4 frente a 7), mientras que PSO fue más rápido en tiempo medio (5.848 frente a 13.345 ms). Por lo tanto, el resultado depende de qué medida se priorice: calidad/tiempo favoreció a PSO en estas pruebas, pero el número de iteraciones favoreció al AG en la función radial. Son observaciones empíricas de esta configuración, no una superioridad universal.

## Ejercicio 2 — Sistema de hormigas para el viajante

### Introducción

El sistema de hormigas (Ant System, AS) construye recorridos probabilísticamente. La probabilidad de elegir la siguiente ciudad aumenta con la feromona presente en la arista y con su atractivo heurístico, aquí `ηᵢⱼ = 1/dᵢⱼ`. Tras cada iteración, la feromona se evapora a tasa `ρ` y se refuerza según la variante de depósito. El problema se resuelve como un ciclo cerrado que visita cada una de las 17 ciudades exactamente una vez.

### Diseño experimental

Se leyó `gr17.csv` como matriz simétrica 17×17, con diagonal nula. En cada corrida se utilizaron 17 hormigas, 100 iteraciones, `α=1`, `β=2` y feromona inicial igual a 1. Se probaron `ρ ∈ {{0.1,0.3,0.5,0.7}}`, `Q ∈ {{0.1,1,10}}` y 10 semillas por combinación y estrategia (900 corridas). `Q` es la cantidad de feromona depositada y la evaporación se aplica al inicio de cada iteración.

- **Global:** sólo la mejor ruta de la iteración deposita `Q/L` en cada arista recorrida.
- **Local:** cada hormiga deposita `Q/L` al terminar su ruta, antes de construir la siguiente ruta de esa iteración.
- **Uniforme:** cada hormiga deposita una cantidad constante `Q` por arista, independiente de la longitud del ciclo.

Las actualizaciones son simétricas porque el grafo del viajante es no dirigido. La tabla completa agrega 10 corridas por configuración; los tiempos reflejan sólo la búsqueda ACO.

### Resultados y comparación de depósitos

{chr(10).join(method_rows)}

![Efecto de rho con Q=1](ej2_rho.svg)

![Efecto de Q con rho=0.3](ej2_Q.svg)

#### Tabla completa por configuración

{chr(10).join(config_rows)}

La solución exacta de referencia, calculada por programación dinámica de Held–Karp, tiene longitud **{exact_length:.0f}** y ruta `{exact_route_text}`. La mejor ruta observada por ACO tiene longitud **{best_length:.0f}** y ruta `{route_text}`. Esta referencia permite cuantificar la brecha de las metaheurísticas; Held–Karp no forma parte del tiempo informado para ACO.

![Recorrido ACO](ej2_recorrido.svg)

### Conclusión

En el promedio de las 12 configuraciones por regla de depósito, el método local obtuvo la menor longitud media (2140.87; desvío combinado 29.02), seguido del global (2146.52; 39.82) y el uniforme (2169.32; 72.04). El uniforme fue el más rápido en promedio (551.526 ms por corrida), aunque encontró rutas más largas; el global promedió 835.489 ms y el local 609.849 ms. Las tres reglas alcanzaron el óptimo exacto 2085 al menos una vez. La mejor media entre configuraciones individuales fue 2092.30 con depósito global, `ρ=0.1` y `Q=10`; aumentar `ρ` tendió a empeorar las longitudes al fijar `Q=1`. Con `ρ=0.3`, `Q=10` perjudicó especialmente al depósito uniforme (media 2188.50), mientras que el depósito local fue más estable entre los tres valores de `Q`.

Estos datos ilustran el compromiso entre exploración, retención de feromona, calidad y tiempo. No existe una única configuración que minimice simultáneamente las tres medidas: el método local tuvo mejor longitud media global, el uniforme fue más rápido y el global con `ρ=0.1, Q=10` dio la mejor media de una configuración. Las conclusiones se basan en 10 corridas por caso; más réplicas podrían afinar las diferencias. Los resultados pueden reproducirse ejecutando el script incluido con la matriz `gr17.csv`.

## Archivos generados

- `resultados_ej1.csv`: resultados individuales PSO/AG.
- `resultados_ej2.csv`: estadísticas por configuración ACO.
- Gráficos SVG incluidos junto a este informe.

Para repetir los experimentos desde la carpeta extraída, con Python 3:

```text
python tp_inteligencia_artificial.py --gr17 "C:\\Users\\Mirian\\Downloads\\gr17.csv" --output resultados_tp_ia
```

"""
    (output / "informe_tp_ia.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gr17",
        type=Path,
        default=Path(r"C:\Users\Mirian\Downloads\gr17.csv"),
        help="Path to the 17 by 17 gr17 distance matrix.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "resultados_tp_ia",
        help="Directory for the report, tables, and SVG figures.",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    reference_x, reference_value = schwefel_reference()
    function_specs = [
        ("Schwefel (1D)", schwefel, [(-512.0, 512.0)], reference_value, 1e-4),
        ("Ondulación radial (2D)", radial_ripple, [(-100.0, 100.0)] * 2, 1.0, 1e-4),
    ]
    function_results: list[dict[str, object]] = []
    all_histories: dict[tuple[str, str], list[list[float]]] = {}
    with (args.output / "resultados_ej1.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["funcion", "metodo", "semilla", "mejor_f", "iteraciones", "exito", "tiempo_s"])
        for function_index, (name, function, bounds, minimum, tolerance) in enumerate(function_specs):
            for method, optimizer in (("PSO", particle_swarm), ("AG", genetic_algorithm)):
                values, iterations, durations, successes = [], [], [], []
                histories = []
                for repetition in range(20):
                    seed = 20261007 + function_index * 1000 + repetition
                    value, history, used_iterations, duration = optimizer(
                        function, bounds, seed, 400, minimum + tolerance
                    )
                    values.append(value)
                    iterations.append(used_iterations)
                    durations.append(duration)
                    successes.append(value <= minimum + tolerance)
                    histories.append(history)
                    writer.writerow([
                        name, method, seed, f"{value:.12g}", used_iterations,
                        int(value <= minimum + tolerance), f"{duration:.9f}",
                    ])
                all_histories[(name, method)] = histories
                successful_iterations = [count for count, success in zip(iterations, successes) if success]
                function_results.append({
                    "function": name,
                    "method": method,
                    "successes": sum(successes),
                    "best": min(values),
                    "mean": statistics.mean(values),
                    "std": statistics.stdev(values),
                    "iterations": f"{statistics.median(successful_iterations):.0f}" if successful_iterations else "—",
                    "time": statistics.mean(durations) * 1000,
                })

    write_function_figure(args.output / "ej1_funciones.svg")
    convergence_series = []
    for name, _, _, minimum, _ in function_specs:
        for method, color in (("PSO", "#2563eb"), ("AG", "#dc2626")):
            histories = all_histories[(name, method)]
            convergence_series.append((
                f"{name} — {method}",
                mean_history(histories, minimum, 401),
                color if name == "Schwefel (1D)" else ("#60a5fa" if method == "PSO" else "#f87171"),
            ))
    write_lines_figure(
        args.output / "ej1_convergencia.svg",
        "Convergencia media: error respecto del mínimo de referencia",
        "Iteración",
        "Error medio (escala logarítmica)",
        convergence_series,
        log_scale=True,
    )

    matrix = load_distance_matrix(args.gr17)
    exact_length, exact_route = held_karp(matrix)
    aco_results: list[dict[str, object]] = []
    best_route: list[int] = []
    best_length = math.inf
    with (args.output / "resultados_ej2.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "deposito", "rho", "Q", "corridas", "longitud_media",
            "desviacion_estandar", "mejor_longitud", "tiempo_medio_s",
            "brecha_vs_optimo_pct",
        ])
        for method in ("global", "local", "uniform"):
            for rho in (0.1, 0.3, 0.5, 0.7):
                for amount in (0.1, 1.0, 10.0):
                    lengths, durations, routes = [], [], []
                    for repetition in range(10):
                        seed = 20261007 + repetition
                        length, route, _, duration = ant_colony(
                            matrix, rho, amount, method, seed, iterations=100
                        )
                        lengths.append(length)
                        durations.append(duration)
                        routes.append(route)
                        if length < best_length:
                            best_length, best_route = length, route[:]
                    mean_length = statistics.mean(lengths)
                    std_length = statistics.stdev(lengths)
                    mean_time = statistics.mean(durations)
                    aco_results.append({
                        "method": method,
                        "rho": rho,
                        "amount": amount,
                        "mean_length": mean_length,
                        "std_length": std_length,
                        "best_length": min(lengths),
                        "mean_time": mean_time,
                        "best_routes": routes,
                    })
                    writer.writerow([
                        method, rho, amount, len(lengths), f"{mean_length:.6f}",
                        f"{std_length:.6f}", f"{min(lengths):.0f}",
                        f"{mean_time:.9f}", f"{100 * (mean_length - exact_length) / exact_length:.6f}",
                    ])

    rho_series = []
    for method, color in (("global", "#2563eb"), ("local", "#dc2626"), ("uniform", "#059669")):
        selected = [r for r in aco_results if r["method"] == method and r["amount"] == 1.0]
        rho_series.append((method, [r["mean_length"] for r in selected], color))
    write_lines_figure(
        args.output / "ej2_rho.svg",
        "Efecto de la evaporación ρ (Q=1)",
        "Tasa de evaporación ρ",
        "Longitud media de ruta",
        rho_series,
    )
    amount_series = []
    for method, color in (("global", "#2563eb"), ("local", "#dc2626"), ("uniform", "#059669")):
        selected = [r for r in aco_results if r["method"] == method and r["rho"] == 0.3]
        amount_series.append((method, [r["mean_length"] for r in selected], color))
    write_lines_figure(
        args.output / "ej2_Q.svg",
        "Efecto de la cantidad depositada Q (ρ=0.3)",
        "Cantidad de feromona depositada Q",
        "Longitud media de ruta",
        amount_series,
    )
    write_route_figure(args.output / "ej2_recorrido.svg", best_route, matrix)
    write_report(
        args.output,
        function_results,
        aco_results,
        exact_length,
        exact_route,
        best_route,
        best_length,
        reference_x,
        reference_value,
    )
    print(f"Report: {args.output / 'informe_tp_ia.md'}")
    print(f"Exact gr17 optimum: {exact_length:.0f}")
    print(f"Best ACO route: {best_length:.0f}")
    print(f"Outputs: {args.output}")


if __name__ == "__main__":
    main()
