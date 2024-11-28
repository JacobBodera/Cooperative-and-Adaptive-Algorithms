import random
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

PROB_MUTATION_VERSUS_CROSS = 0.4
PROB_MUTATION = 0.1

POP = 700
GEN = 2000
NUM_TEST_CASES = 300

DEPTH = 9
ADDRESSES = 16
OUTPUTS = 2 ** ADDRESSES

terminals = [f'x{i}' for i in range(ADDRESSES)]
functions = {
    'AND': lambda x, y: 0 if x == 0 else y,
    'OR': lambda x, y: 1 if x == 1 else y,
    'NOT': lambda x: int(not x),
    'IF': lambda x, y, z: y if x else z
}

# Fitness Cache
fitness_cache = {}

def cached_fitness(program, test_cases):
    program_str = str(program)
    if program_str in fitness_cache:
        return fitness_cache[program_str]
    fitness_score = fitness(program, test_cases)
    fitness_cache[program_str] = fitness_score
    return fitness_score

def random_terminal():
    return random.choice(terminals)

def random_function():
    return random.choice(list(functions.keys()))

def fitness(program, test_cases):
    num_correct = 0
    for inputs, expected in test_cases:
        if evaluate_program(program, inputs) == expected:
            num_correct += 1
    return num_correct / len(test_cases)

def generate_test_cases_16_middle_3():
    test_cases = []
    for i in range(2 ** ADDRESSES):
        binary_input = [(i >> j) & 1 for j in range(ADDRESSES)]
        inputs = {f'x{j}': binary_input[j] for j in range(ADDRESSES)}
        total = sum(binary_input)
        expected = 1 if (7 <= total <= 9) else 0
        test_cases.append((inputs, expected))
    return test_cases

def generate_program(depth=DEPTH):
    if depth == 0 or (depth > 1 and random.random() < 0.5):
        return random_terminal()
    else:
        function = random_function()
        if function == 'NOT':
            return [function, generate_program(depth - 1)]
        elif function == 'IF':
            return [function, generate_program(depth - 1), generate_program(depth - 1), generate_program(depth - 1)]
        else:
            return [function, generate_program(depth - 1), generate_program(depth - 1)]

def evaluate_program(program, inputs):
    if isinstance(program, str):
        return inputs[program]
    function = program[0]
    if function == 'NOT':
        return functions[function](evaluate_program(program[1], inputs))
    elif function == 'IF':
        return functions[function](evaluate_program(program[1], inputs),
                                   evaluate_program(program[2], inputs),
                                   evaluate_program(program[3], inputs))
    else:
        return functions[function](evaluate_program(program[1], inputs),
                                   evaluate_program(program[2], inputs))

def mutate(program, depth=DEPTH, prob=PROB_MUTATION):
    if random.random() < prob:
        return generate_program(depth)
    if isinstance(program, list):
        if program[0] == 'NOT':
            return [program[0], mutate(program[1], depth - 1)]
        elif program[0] == 'IF':
            return [program[0],
                    mutate(program[1], depth - 1),
                    mutate(program[2], depth - 1),
                    mutate(program[3], depth - 1)]
        else:
            return [program[0],
                    mutate(program[1], depth - 1),
                    mutate(program[2], depth - 1)]
    return program

def crossover(parent1, parent2):
    if isinstance(parent1, str) or isinstance(parent2, str):
        return parent2 if random.random() < 0.5 else parent1
    if len(parent1) != len(parent2):
        return parent1
    return [parent1[0]] + [crossover(p1, p2) for p1, p2 in zip(parent1[1:], parent2[1:])]

def parallel_fitness(population, test_cases):
    with ThreadPoolExecutor() as executor:
        fitness_scores = list(executor.map(lambda p: cached_fitness(p, test_cases), population))
    return fitness_scores

def start_environment(population_size, generations):
    population = [generate_program() for _ in range(population_size)]
    test_cases = generate_test_cases_16_middle_3()[:NUM_TEST_CASES]
    best_fitness = 0
    fitness_history = []

    for g in range(generations):
        fitness_scores = parallel_fitness(population, test_cases)
        population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
        best_fitness = fitness_scores[0]
        fitness_history.append(best_fitness)

        print(f"Generation: {g} --- Best Fitness: {best_fitness}")

        if best_fitness == 1.0:
            return population[0], best_fitness, fitness_history

        new_population = population[:10]
        while len(new_population) < population_size:
            if random.random() > PROB_MUTATION_VERSUS_CROSS:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                p_new = crossover(parent1, parent2)
            else:
                p = random.choice(population[:population_size // 2])
                p_new = mutate(p)
            new_population.append(p_new)

        population = new_population

    return population[0], best_fitness, fitness_history

solution, b_fitness, fitness_history = start_environment(POP, GEN)

print(f'SOLUTION: {solution}')
print(f'PARTIAL FITNESS: {b_fitness}')
print(f'COMPLETE FITNESS: {cached_fitness(solution, generate_test_cases_16_middle_3())}')

plt.plot(fitness_history)
plt.xlabel('Generations')
plt.ylabel('Best Fitness')
plt.title('Best Fitness Over Generations')
plt.grid()
plt.savefig('../images/problem3_middle4.png')