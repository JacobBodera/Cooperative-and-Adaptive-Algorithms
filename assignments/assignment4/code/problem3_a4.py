import random
import itertools

PROB_MUTATION_VERSUS_CROSS = 0.4
PROB_MUTATION = 0.1

POP = 500
GEN = 500
NUM_TEST_CASES = 0

DEPTH = 5
ADDRESSES = 3
OUTPUTS = 2**ADDRESSES

# terminals = ['a0', 'a1', 'a2', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
terminals = [f'a{i}' for i in range(ADDRESSES)] + [f'd{i}' for i in range(OUTPUTS)]
functions = {
    'AND': lambda x, y: 0 if x == 0 else y,
    'OR': lambda x, y: 1 if x == 1 else y,
    'NOT': lambda x: not x,
    'IF': lambda x, y, z: y if x else z
}
fitness_cache = {}

def random_terminal():
    return random.choice(terminals)

def random_function():
    return random.choice(list(functions.keys()))

def fitness_mult_6(program):
    num_correct = 0
    for a0 in [0, 1]:
        for a1 in [0, 1]:
            for d0 in [0, 1]:
                for d1 in [0, 1]:
                    for d2 in [0, 1]:
                        for d3 in [0, 1]:
                            inputs = {'a0': a0, 'a1': a1, 'd0': d0, 'd1': d1, 'd2': d2, 'd3': d3}
                            expected_d = inputs[f'd{(a0 * 2) + a1}']
                            if evaluate_program(program, inputs) == expected_d:
                                num_correct += 1
    return num_correct / 64.0

def cached_fitness(program, test_cases):
    program_str = str(program)
    if program_str in fitness_cache:
        return fitness_cache[program_str]
    fitness_score = fitness(program, test_cases)
    fitness_cache[program_str] = fitness_score
    return fitness_score

def fitness(program, test_cases):
    num_correct = 0
    for inputs, expected in test_cases:
        if evaluate_program(program, inputs) == expected:
            num_correct += 1
    return num_correct / len(test_cases)

def generate_test_cases(num_tests = 0, num_addresses = ADDRESSES, num_outputs = OUTPUTS):
    all_cases = list(itertools.product([0, 1], repeat = num_addresses + num_outputs))
    random.shuffle(all_cases)
    cases = all_cases[:num_tests] if num_tests > 0 else all_cases
    test_cases = []
    for c in cases:
        test_case = {}
        expected_address = 0
        for i in range(num_addresses):
            test_case[f'a{i}'] = c[i]
            expected_address = expected_address | c[i] << (num_addresses - 1 - i)
        for j in range(num_outputs):
            test_case[f'd{j}'] = c[num_addresses + j]
        expected_output = test_case[f'd{expected_address}']
        test_cases.append((test_case, expected_output))

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
            return [program[0],
                    mutate(program[1], depth - 1)]
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

def start_environment(population_size, generations):
    population = [generate_program() for _ in range(population_size)]
    test_cases = generate_test_cases(num_tests=NUM_TEST_CASES, num_addresses=ADDRESSES, num_outputs=OUTPUTS)
    best_fitness = 0
    for g in range(generations):
        # current_mutation_rate = max(PROB_MUTATION, (1 - g / generations))

        population = sorted(population, key=lambda p: cached_fitness(p, test_cases), reverse=True)
        best_fitness = cached_fitness(population[0], test_cases)
        print(f"Generation: {g} --- Best Fitness: {best_fitness}")

        if best_fitness == 1.0:
            return population[0], best_fitness

        new_population = population[:POP // 20]
        while len(new_population) < population_size:
            if random.random() > PROB_MUTATION_VERSUS_CROSS:
                parent1, parent2 = random.choices(population[:population_size // 2], k=2)
                p_new = crossover(parent1, parent2)
            else:
                p = random.choice(population[:population_size // 2])
                p_new = mutate(p)
            new_population.append(p_new)

        population = new_population

    return population[0], best_fitness

solution, b_fitness = start_environment(POP, GEN)

print(f'SOLUTION: {solution}')
print(f'PARTIAL FITNESS: {b_fitness}')

print(f'COMPLETE FITNESS: {fitness(solution, generate_test_cases())}')



# print(len(generate_test_cases()))



