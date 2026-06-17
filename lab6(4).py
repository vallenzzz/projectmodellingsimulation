import matplotlib.pyplot as plt
import numpy as np

beta = 0.3
gamma = 0.1
days = 160

N = 1000
S0 = 699
I0 = 1
R0 = 300
S = [S0]
I = [I0]
R = [R0]

for day in range(days):
 St = S[-1]
 It = I[-1]
 Rt = R[-1]
 new_infections = beta * St * It / N
 new_recoveries = gamma * It
 next_S = St - new_infections
 next_I = It + new_infections - new_recoveries
 next_R = Rt + new_recoveries
 S.append(next_S)
 I.append(next_I)
 R.append(next_R)

plt.figure(figsize=(10,6))
plt.plot(S,label="Susceptible")
plt.plot(I,label="Infected")
plt.plot(R,label="Recovered")
plt.xlabel("Days")
plt.ylabel("Population")
plt.title("SIR Epidemic Model")
plt.legend()
plt.grid(True)
plt.show()

peak_infected = max(I)
peak_day = I.index(peak_infected)
print("Peak infected:", peak_infected)
print("Peak day:", peak_day)
