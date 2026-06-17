import numpy as np
import matplotlib.pyplot as plt

a, b, c, d = 0.1, 0.04, 0.1, 0.01
R0, W0 = 40, 9
steps = 200
rabbits = [R0]
wolves = [W0]
for t in range(steps):
 R = rabbits[-1]
 W = wolves[-1]

 next_R = R + a*R - b*R*W
 next_W = W - c*W + d*R*W

 rabbits.append(next_R)
 wolves.append(next_W)

plt.plot(rabbits, label="Rabbits")
plt.plot(wolves, label="Wolves")
plt.legend()
plt.show()