import numpy as np
import matplotlib.pyplot as plt
r = 0.8
K = 2000
P0 = 100
steps = 100
population = [P0]

for t in range(steps):
 P = population[-1]
 next_P = P + r * P * (1 - P/K)
 population.append(next_P)
 
plt.plot(population)
plt.title("Logistic Growth")
plt.xlabel("Time")
plt.ylabel("Population")
plt.show()