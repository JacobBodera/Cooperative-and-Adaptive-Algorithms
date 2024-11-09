import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools


def sphere(individual):
    return sum(x ** 2 for x in individual),


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def adaptive_es_deap(dim, generations, c, sigma_0):
    toolbox = base.Toolbox()
    toolbox.register("attribute", random.uniform, -5.12, 5.12)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, dim)
    toolbox.register("evaluate", sphere)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma_0, indpb=1.0)

    population = [toolbox.individual()]
    population[0].fitness.values = toolbox.evaluate(population[0])
    sigma = sigma_0
    costs = []
    success_rate_window = 20
    successes = []

    for generation in range(generations):
        mutant = toolbox.clone(population[0])
        toolbox.mutate(mutant)
        mutant[:] = [np.clip(x, -5.12, 5.12) for x in mutant]
        mutant.fitness.values = toolbox.evaluate(mutant)

        if mutant.fitness.values < population[0].fitness.values:
            population[0] = mutant
            successes.append(1)
        else:
            successes.append(0)

        if generation >= success_rate_window:
            success_rate = sum(successes[-success_rate_window:]) / success_rate_window
            if success_rate < 0.2:
                sigma *= c ** 2
            elif success_rate > 0.2:
                sigma /= c ** 2
            toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma, indpb=1.0)

        costs.append(population[0].fitness.values[0])

    return costs


dim = 10
sigma_0 = 0.1 / (2 * np.sqrt(3))
generations = 500
num_simulations = 50
c_values = [0.6, 0.8, 1.0]

average_costs = {c: np.zeros(generations) for c in c_values}

for c in c_values:
    total_costs = []
    for _ in range(num_simulations):
        costs = adaptive_es_deap(dim=dim, generations=generations, c=c, sigma_0=sigma_0)
        total_costs.append(costs)
    average_costs[c] = np.mean(total_costs, axis=0)

plt.figure(figsize=(12, 6))
for c in c_values:
    plt.plot(range(generations), average_costs[c], label=f"c = {c}")
plt.xlabel("Generation")
plt.ylabel("Average Cost")
plt.title("Adaptive (1+1)-ES on 10-dimensional Sphere Function (DEAP)")
plt.legend()
plt.grid()
# plt.savefig("../images/problem2_a3_deap.png", format="png", dpi=1000)
plt.show()
