import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

x = [0.1, 0.3, 0.5, 0.6, 0.9]
y = [5.02, 4.99, 5.43, 4.96, 4.82]

x_smooth = np.linspace(min(x), max(x), 200)

spline = make_interp_spline(x, y, k=3)
y_smooth = spline(x_smooth)

plt.plot(x_smooth, y_smooth)
plt.xlabel("Mutation Probability")
plt.ylabel("Best Fitness")
plt.title("GA Fitness with Varying Mutation Probability")
plt.grid()
# plt.show()
plt.savefig("../images/problem1_a3_mutation_prob.png", format="png", dpi=1000)