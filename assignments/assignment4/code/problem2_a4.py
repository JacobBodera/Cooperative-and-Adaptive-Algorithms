import numpy as np
from matplotlib import pyplot as plt


BOUNDS = (-5, 5)
NUMBER_PARTICLES = 5
MAX_ITERATIONS = 200


def objective(pos):
    x, y = pos
    return (4 - (2.1*x**2) + (x**4 / 3))*x**2 + x*y + (-4 + (4*y**2))*y**2

def initialize_swarm(num_particles, bounds):
    positions = np.random.uniform(bounds[0], bounds[1], (num_particles, 2))
    velocities = np.zeros((num_particles, 2))
    return positions, velocities

def update_velocities(x, v, pbest, gbest, w=0.792, c1=1.4944, c2=1.4944):
    r1 = np.random.uniform(low=0, high=1, size=2)
    r2 = np.random.uniform(low=0, high=1, size=2)
    return (
            w * v +
            c1 * r1 * (pbest - x) +
            c2 * r2 * (gbest - x)
    )

def update_positions(positions, velocities, bounds):
    return np.clip(a = positions + velocities, a_min = bounds[0], a_max = bounds[1])

def deploy_swarm(num_particles, bounds, max_iterations):
    positions, velocities = initialize_swarm(num_particles, bounds)
    # Best positions for each particle
    personal_bests = positions.copy()
    # Best fitness of each particle
    personal_fitness_bests = np.apply_along_axis(lambda position: objective(position),1, personal_bests)
    # The best position
    global_best = personal_bests[np.argmin(personal_fitness_bests)]
    # The fitness of the best position
    global_fitness_best = min(personal_fitness_bests)

    # Data for plots
    particle_trajectories = [[] for _ in range(num_particles)]
    initial_positions = positions.copy()
    avg_fitness_history = []
    best_fitness_history = []

    for i in range(num_particles):
        particle_trajectories[i].append(positions[i].copy())

    for iteration in range(max_iterations):
        # Updating average history
        avg_fitness = np.mean([objective(pos) for pos in positions])
        avg_fitness_history.append(avg_fitness)
        best_fitness_history.append(global_fitness_best)

        for p in range(num_particles):
            velocities[p] = update_velocities(x = positions[p], v = velocities[p],
                                              pbest = personal_bests[p], gbest = global_best)
            positions[p] = update_positions(positions[p], velocities[p], bounds=bounds)

            # Updating trajectory information
            particle_trajectories[p].append(positions[p].copy())

            # Updating particles personal best
            p_fitness = objective(positions[p])
            if p_fitness < personal_fitness_bests[p]:
                personal_bests[p] = positions[p]
                personal_fitness_bests[p] = p_fitness
            # Updating global best
            if p_fitness < global_fitness_best:
                global_best = positions[p]
                global_fitness_best = p_fitness

    return global_best, global_fitness_best, particle_trajectories, initial_positions, avg_fitness_history, best_fitness_history


gbest, fbest, trajectories, initial_ps, avg_fitness_hist, best_fitness_hist = deploy_swarm(NUMBER_PARTICLES, BOUNDS, MAX_ITERATIONS)

ACTUAL_MIN_POS = [0.089840, -0.712659]
ACTUAL_MIN_FIT = objective(ACTUAL_MIN_POS)

print(f"Best Position: {gbest}\nBest Fitness: {fbest}")
print(f"% Error: {100*abs(fbest - ACTUAL_MIN_FIT)/abs(ACTUAL_MIN_FIT)}")

## Trajectory plot
plt.figure(figsize=(10, 8))
for particle_path in trajectories:
    particle_path = np.array(particle_path)
    plt.plot(particle_path[:, 0], particle_path[:, 1], linestyle="--", marker="o", markersize=2, alpha=0.5)

# Mark initial positions
initial_positions = np.array(initial_ps)
plt.scatter(initial_positions[:, 0], initial_positions[:, 1], color="blue", marker="x", s=20, label="Starting Positions")

# Mark final global best
plt.plot(gbest[0], gbest[1], "ro", markersize=10, label="Global Best Position")

plt.xlim(BOUNDS[0], BOUNDS[1])
plt.ylim(BOUNDS[0], BOUNDS[1])
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Particle Trajectories and Final Global Best Position")
plt.legend()
plt.grid(True)
plt.savefig('../images/problem2_a4_trajectories.png')

## Average fitness plot
plt.figure(figsize=(10, 6))
plt.plot(avg_fitness_hist, label="Average Fitness")
plt.plot(best_fitness_hist, label="Best Fitness", color="red")
plt.xlabel("Iteration")
plt.ylabel("Fitness Value")
plt.title("Average Fitness and Best Fitness Over Time")
plt.legend()
plt.grid(True)
plt.savefig('../images/problem2_a4_fitness.png')
