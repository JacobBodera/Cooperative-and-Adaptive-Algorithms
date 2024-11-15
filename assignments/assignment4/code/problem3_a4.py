import random

terminals = ['a0', 'a1', 'd0', 'd1', 'd2', 'd3']
functions = {
    'AND': lambda x, y: 0 if x == 0 else y,
    'OR': lambda x, y: 1 if x == 1 else y,
    'NOT': lambda x: not x,
    'IF': lambda x, y, z: y if x else z
}

def random_terminal():
    return random.choice(terminals)

def random_function():
    return random.choice(list(functions.keys()))

def generate_tree(depth=3):
    if depth == 0 or (depth > 1 and random.random() < 0.5):
        return random_terminal()
    else:
        function = random_function()
        if function == 'NOT':
            return [function, generate_tree(depth - 1)]
        elif function == 'IF':
            return [function, generate_tree(depth - 1), generate_tree(depth - 1), generate_tree(depth - 1)]
        else:
            return [function, generate_tree(depth - 1), generate_tree(depth - 1)]

