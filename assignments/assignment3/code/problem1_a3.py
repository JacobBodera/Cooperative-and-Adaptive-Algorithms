from random import uniform, choices, random
from matplotlib import pyplot as plt
from control_parameters import performance_results
import numpy as np
import matlab.engine

POPULATION_SIZE = 100
NUM_GENERATIONS = 150
CROSSOVER_PROB = 0.6
ALPHA = 0.6
MUTATION_PROB = 0.25
ELITISM_NUM = 2
ALLELE_BOUNDS = [(2, 18), (1.05, 9.42), (0.26, 2.37)]
ENG = matlab.engine.start_matlab()
ENG.eval("warning('off', 'all')", nargout=0)

def rand_kp():
    return round(uniform(ALLELE_BOUNDS[0][0], ALLELE_BOUNDS[0][1]), 2)

def rand_ti():
    return round(uniform(ALLELE_BOUNDS[1][0], ALLELE_BOUNDS[1][1]), 2)

def rand_td():
    return round(uniform(ALLELE_BOUNDS[2][0], ALLELE_BOUNDS[2][1]), 2)

def random_gene():
    return [rand_kp(), rand_ti(), rand_td()]

def initialize_population(size):
    return [random_gene() for _ in range(size)]

def fitness(gene):
    w_ise, w_tr, w_ts, w_mp = 0.01, 10, 1, 0.1
    ise, t_r, t_s, m_p =performance_results(kp=gene[0], ti=gene[1], td=gene[2], eng=ENG)
    return 100/(w_ise*ise + w_tr*t_r + w_ts*t_s + w_mp*m_p)

def selection(population):
    fitness_values = [fitness(gene) for gene in population]
    total_fitness = sum(fitness_values)
    proportional_gene_fitness = [f/total_fitness for f in fitness_values]
    selected_indices = choices(population=range(len(population)), weights=proportional_gene_fitness, k=2)
    return population[selected_indices[0]], population[selected_indices[1]]

def crossover(parent1, parent2): # WHOLE ARITHMETIC
    if random() < CROSSOVER_PROB:
        return ([round(parent1[i] * ALPHA + parent2[i] * (1 - ALPHA), 2) for i in range(len(parent1))],
                [round(parent1[i] * (1 - ALPHA) + parent2[i] * ALPHA, 2) for i in range(len(parent1))])
    else:
        return parent1, parent2

def mutate(gene):
    new_gene = []
    for i in range(len(gene)):
        if random() < MUTATION_PROB:
            new_gene.append(np.clip(
                a = gene[i] + np.random.uniform(low = -(ALLELE_BOUNDS[i][1] - ALLELE_BOUNDS[i][0]) / 2,
                                                high = (ALLELE_BOUNDS[i][1] - ALLELE_BOUNDS[i][0]) / 2),
                a_min=ALLELE_BOUNDS[i][0],
                a_max=ALLELE_BOUNDS[i][1]))
        else:
            new_gene.append(gene[i])
    return new_gene

def the_biggest_bang():
    best_genes = list()
    best_fitness = list()
    population = initialize_population(POPULATION_SIZE)
    population = sorted(population, key=lambda gene: fitness(gene), reverse=True)

    for generation in range(NUM_GENERATIONS):
        print(f"GENERATION {generation + 1}")
        new_population = population[:ELITISM_NUM]

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = selection(new_population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))

        population = new_population
        population = sorted(population, key=lambda gene: fitness(gene), reverse=True)
        best_genes.append(population[0])
        best_fitness.append(fitness(population[0]))
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness[-1]}, Best Gene = {best_genes[-1]}")

    return best_genes, best_fitness


genes, fit = the_biggest_bang()
ENG.quit()

print(f"Best Gene: {genes[-1]}")

plt.plot(range(1, NUM_GENERATIONS + 1), fit)
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Genetic Algorithm (P = 100, G = 150)")
plt.grid()
plt.savefig("../images/problem1_a3_p100_g150.png", format="png", dpi=1000)




