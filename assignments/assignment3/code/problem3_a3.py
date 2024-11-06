import numpy as np
from random import choices

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
NUM_ANTS = 10
NUM_ITERATIONS = 100
EVAPORATION_RATE = 1
INITIAL_PHEROMONE = 1

def prob_of_neighbours(curr_position, visited, pheromones):
    p_d_sum = 0
    p_d_ratios = list()
    for i in range(len(POSITIONS)):
        if i in visited:
            continue
        else:
            p_d_ratios.append(pheromones[curr_position][i]/DISTANCES[curr_position][i])
            p_d_sum += pheromones[curr_position][i]/DISTANCES[curr_position][i]
    return [p_d_ratios[i] / p_d_sum for i in range(len(p_d_ratios))]

def evaporate(pheromones):
    for i in range(len(pheromones)):
        for j in range(len(pheromones[0])):
            pheromones[i][j] = (1 - EVAPORATION_RATE) * pheromones[i][j]
    return pheromones

def enforce(pheromones, visited):
    


def aco_optimization():
    pheromones = np.full((len(POSITIONS), len(POSITIONS)), INITIAL_PHEROMONE)
    best_cost = None
    best_solution = None
    for _ in range(NUM_ITERATIONS):
        for ant in range(NUM_ANTS):
            current_position = 0  # Always going to start at 1st position
            visited = [current_position]
            distance = 0
            for i in range(len(POSITIONS)):
                new_position = choices(population = [pos for pos in [i for i in range(len(POSITIONS))] if pos not in visited],
                                       weights = prob_of_neighbours(current_position, visited, pheromones),
                                       k = 1)
                distance += DISTANCES[current_position][new_position]
                current_position = new_position
                visited.append(current_position)

            if best_cost is None or distance < best_cost or best_solution is None:
                best_cost = distance
                best_solution = visited

            pheromones = evaporate(pheromones)
            pheromones = enforce(pheromones)






