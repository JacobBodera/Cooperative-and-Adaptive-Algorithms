import numpy as np
from random import choices

from matplotlib import pyplot as plt

# 0-28 positions
POSITIONS = [(1150.0, 1760.0), (840.0, 550.0), (830.0, 1770.0), (630.0, 1660.0),
             (1170.0, 2300.0), (490.0, 500.0), (40.0, 2090.0), (970.0, 1340.0),
             (1840.0, 1240.0), (750.0, 1100.0), (510.0, 700.0), (1260.0, 1500.0),
             (750.0, 2030.0), (750.0, 900.0), (1280.0, 790.0), (1030.0, 2070.0),
             (1280.0, 1200.0), (490.0, 2130.0), (1650.0, 650.0), (230.0, 590.0),
             (1460.0, 1420.0), (1490.0, 1630.0), (460.0, 860.0), (1260.0, 1910.0),
             (790.0, 2260.0), (1040.0, 950.0), (360.0, 1980.0), (710.0, 1310.0), (590.0, 1390.0)]
DISTANCES = np.zeros((len(POSITIONS), len(POSITIONS)))
for i in range(len(POSITIONS)):
    for j in range(len(POSITIONS)):
        if i != j:
            DISTANCES[i][j] = np.sqrt((POSITIONS[i][0] - POSITIONS[j][0]) ** 2 + (POSITIONS[i][1] - POSITIONS[j][1]) ** 2)
NUM_ANTS = 50 # 500
NUM_ITERATIONS = 150
EVAPORATION_RATE = 0.1 # 0.1
INITIAL_PHEROMONE = 1.0
ENFORCEMENT = 0.1 # 0.1
OFFLINE_ENFORCEMENT = 0.005

def prob_of_neighbours(curr_position, visited, pheromones):
    p_d_sum = 0
    p_d_ratios = list()
    for i in range(len(POSITIONS)):
        if i not in visited and DISTANCES[curr_position][i] > 0:  # Avoid zero distances
            ratio = pheromones[curr_position][i] / DISTANCES[curr_position][i]
            p_d_ratios.append(ratio)
            p_d_sum += ratio
    return [p / p_d_sum for p in p_d_ratios]

def evaporate(pheromones):
    return pheromones * (1 - EVAPORATION_RATE)

def enforce(pheromones, best_path):
    for i in range(len(best_path) - 1):
        pheromones[best_path[i]][best_path[i + 1]] += ENFORCEMENT / DISTANCES[best_path[i]][best_path[i + 1]]
    return pheromones

def offline_enforce(pheromones, visited):
    pheromones[visited[-1]][visited[-2]] += OFFLINE_ENFORCEMENT
    pheromones[visited[-2]][visited[-1]] += OFFLINE_ENFORCEMENT
    return pheromones


def aco_optimization():
    pheromones = np.full((len(POSITIONS), len(POSITIONS)), INITIAL_PHEROMONE)
    best_cost = float('inf')
    costs = []
    best_solution = []
    for _ in range(NUM_ITERATIONS):
        for ant in range(NUM_ANTS):
            current_position = 0  # Always going to start at 1st position
            visited = [current_position]
            distance = 0
            for i in range(len(POSITIONS) - 1):
                weights = prob_of_neighbours(current_position, visited, pheromones)
                candidates = [pos for pos in range(len(POSITIONS)) if pos not in visited]
                new_position = choices(population = candidates, weights=weights, k=1)[0]
                distance += DISTANCES[current_position][new_position]
                current_position = new_position
                visited.append(current_position)

            if distance <= best_cost:
                best_cost = distance
                best_solution = visited

            pheromones = offline_enforce(pheromones, visited)

        costs.append(best_cost)

        pheromones = evaporate(pheromones)
        pheromones = enforce(pheromones, best_solution)

        print(f"ITERATION: {_ + 1}\nCost: {best_cost}\nSolution: {best_solution}\n\n")

    return costs, best_solution

costs_over_time = []
best_costs = list()
for i in range(5):
    c, s = aco_optimization()
    costs_over_time.append(c)
    best_costs.append(c[-1])
    print(f"RUN {i + 1}")

print(f"Min: {min(best_costs)}\nMax: {max(best_costs)}\nMean: {np.mean(best_costs)}")

plt.figure(figsize=(10, 6))
for i, costs in enumerate(costs_over_time):
    plt.plot(range(1, len(costs) + 1), costs, label=f'Run {i+1}')

plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.title('Best Cost over Iterations for Multiple Runs')
plt.legend()
# plt.show()
plt.savefig("../images/problem3_a3_pop50.png", format="png", dpi=1000)










