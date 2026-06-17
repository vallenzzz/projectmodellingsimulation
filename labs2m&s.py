initial_population = 5000
growth_rate = 0.05
years_to_simulate = 20

population_history = [initial_population]

# The Simulation Loop
for year in range(1, years_to_simulate + 1): # Loop through each year of the simulation (starting from 1 to 20) range(1,20+1)
    current_pop = population_history[-1] # Get the most recent population value from the history list initial_population-1
    new_pop = current_pop + (current_pop * growth_rate) # Calculate the new population by applying the growth rate to the current population
    if new_pop > 10000:
        new_pop = 10000 # Cap the population at 10000 to prevent unrealistic growth
    population_history.append(new_pop) # Append the new population value to the history list for tracking

print(f"Final Population: {population_history[-1]:.2f}")

import matplotlib.pyplot as plt

time_steps = list(range(years_to_simulate + 1))

plt.plot(time_steps, population_history, marker='o', color='blue')
plt.title("Deterministic Population Growth Simulation")
plt.xlabel("Years Passed")
plt.ylabel("Total Population")
plt.grid(True)
plt.show()