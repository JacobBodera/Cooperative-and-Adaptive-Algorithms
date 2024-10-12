from random import randint

import numpy as np
import random

def calc_cost(configuration, flow, dist):
    assignment_cost = 0
    for i in range(len(configuration)):
        for j in range(len(configuration)):
            assignment_cost += flow[configuration[i]][configuration[j]] * dist[i][j]
    return assignment_cost

def generate_neighbours(configuration):
    neighbours = []
    for i in range(len(configuration)):
        for j in range(i + 1, len(configuration)):
            neighbour = configuration.copy()
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbours.append(neighbour)
    return neighbours

def generate_random_neighbours(configuration, k=10):
    neighbors = []
    n = len(configuration)
    for _ in range(k):
        i, j = random.sample(range(n), 2)
        neighbour = configuration.copy()
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        neighbors.append(neighbour)
    return neighbors

def diversify_solution(current_configuration, num_swaps=3):
    for _ in range(num_swaps):
        i, j = random.sample(range(len(current_configuration)), 2)
        current_configuration[i], current_configuration[j] = current_configuration[j], current_configuration[i]
    return current_configuration

def tabu_search(flow, dist, tabu_size, max_iter):
    n = len(flow)
    current_config = list(range(n))
    random.shuffle(current_config)
    print(f"Initial configuration: {current_config}")
    initial_configuration = current_config
    tabu = []

    best_config = current_config
    best_cost = calc_cost(current_config, flow, dist)

    shuffle_light = 0
    shuffle_medium = 0
    shuffle_large = 0
    for i in range(max_iter):
        if shuffle_light > 200:
            shuffle_light = 0
            print("LIGHT SHUFFLE")
            current_config = diversify_solution(current_config, num_swaps=2)
        if shuffle_medium > 1000:
            shuffle_medium = 0
            print("MID SHUFFLE")
            current_config = diversify_solution(current_config, num_swaps=4)
        if shuffle_large > 5000:
            shuffle_large = 0
            print("LARGE SHUFFLE")
            current_config = diversify_solution(current_config, num_swaps=6)


        # neighbours = generate_random_neighbours(current_config, k = 120)
        neighbours = generate_neighbours(current_config)
        neighbours_cost = []
        for neighbour in neighbours:
            neighbours_cost.append((neighbour, calc_cost(neighbour, flow, dist)))

        neighbours_cost.sort(key=lambda x: x[1])
        neighbours_cost = neighbours_cost[:80]

        # if i % 2000 == 0:
        #     tabu_size = random.randint(1, 10)
        #     print(f"Tabu Size: {tabu_size}")

        for neighbour, cost in neighbours_cost:
            move = tuple(sorted([current_config.index(neighbour[0]), current_config.index(neighbour[1])]))

            if move not in tabu or cost < best_cost:
                current_config = neighbour
                current_cost = cost
                if current_cost != best_cost:
                    tabu.append(move)

                if len(tabu) > tabu_size:
                    tabu.pop(0)
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_config = current_config
                    shuffle_light = 0
                    shuffle_medium = 0
                    shuffle_large = 0
                break
        shuffle_light += 1
        shuffle_medium += 1
        shuffle_large += 1
        if best_cost == 2570:
            break

        if i % 25 == 0:
            print(f"Iteration: {i}: best cost: {best_cost}")

    return initial_configuration, best_config, best_cost


flow_matrix = np.loadtxt("assignment-2-Flow.csv", delimiter=",")
dist_matrix = np.loadtxt("assignment-2-Distance.csv", delimiter=",")

configs = list()
costs = list()
initial = list()

for i in range(5):
    init, con, cost = tabu_search(flow_matrix, dist_matrix, 5, 20000)
    configs.append(con)
    costs.append(cost)
    initial.append(init)

for i in range(len(configs)):
    print(f"Iteration {i}:\nInitial config: {initial[i]}\nBest configuration found: {configs[i]}\nCost: {costs[i]}\n")
