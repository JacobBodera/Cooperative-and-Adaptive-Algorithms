from asyncio import current_task
from math import cos, exp, pi
from random import uniform, random

'''
x1, x2 are in range

Basic SA Algorithm:
- set current solution to initial solution s = s_0
- set temperature to initial temp t = t_0
- set temperature reduction function alpha

'''
def easom(x1, x2):
    return -cos(x1)*cos(x2)*exp(-(x1 - pi)**2 - (x2 - pi)**2)

def cost(x1, x2, t):
    if t == "easom":
        return easom(x1, x2) * 1E7
    else:
        return -(x1**2 + x2**2)


def cool(temp, alpha):
    return temp ** alpha

def sim_annealing(t_0, alpha, bounds, max_iterations):
    # Initial random guess within bounds
    x1 = uniform(bounds[0][0], bounds[0][1])
    x2 = uniform(bounds[1][0], bounds[1][1])

    current_x = (x1, x2)
    min_cost = 100000
    current_cost = cost(x1, x2, t = "easom")

    temp = t_0
    with open("output.txt", "w") as file:

        for i in range(max_iterations):
            # new x's in neighbourhood and ensure in bounds
            neighbourhood_factor = 10
            new_x1 = min(max(current_x[0] + uniform(-1, 1) * neighbourhood_factor, bounds[0][0]), bounds[0][1])
            new_x2 = min(max(current_x[1] + uniform(-1, 1) * neighbourhood_factor, bounds[1][0]), bounds[1][1])

            new_x = (new_x1, new_x2)
            new_cost = cost(new_x1, new_x2, t = "easom")

            if new_cost < current_cost:
                min_cost = current_cost

            delta_cost = new_cost - current_cost

            file.write("iteration " + str(i) + "\n")
            file.write(str(current_x) + " " + str(current_cost) + "\n")
            file.write("temperature: " + str(temp) + "\n")

            if temp < 1E-5:
                return current_x, current_cost

            # accept new x
            if delta_cost < 0:
                current_x = new_x
                current_cost = new_cost
            else:
                if random() < exp(-delta_cost/temp):
                    current_x = new_x
                    current_cost = new_cost

            temp = cool(temp, alpha)

        file.close()
        print("MINIMUM COST: " + str(min_cost))
        return current_x, current_cost



x_bounds = [(-100, 100), (-100, 100)]

# print(easom(1.2*pi, 1.2*pi))

solution = sim_annealing(t_0 = 100, alpha = 0.99, bounds = x_bounds, max_iterations = 20000)
print(solution)