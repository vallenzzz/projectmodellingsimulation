import numpy as np
import matplotlib.pyplot as plt
r = 0.1
d = 0.3
P0 = 100
years = 50
population = [P0]

for t in range(years):
 P = population[-1]
 next_P = P * (1 + r - d)
 population.append(next_P)

plt.plot(population)
plt.title("Exponential Population Growth")
plt.xlabel("Year")
plt.ylabel("Population")
plt.show()