import random
import matplotlib.pyplot as plt


# Random-walk agent visualization (unchanged behavior)
def random_walk_agents():
  num_agents = 50
  x = [random.randint(0, 50) for _ in range(num_agents)]
  y = [random.randint(0, 50) for _ in range(num_agents)]

  plt.scatter(x, y)
  plt.title("Initial Agent Positions")
  plt.show()

  for _ in range(50):
    for i in range(num_agents):
      x[i] += random.choice([-1, 0, 1])
      y[i] += random.choice([-1, 0, 1])

  plt.scatter(x, y)
  plt.title("Final Agent Positions")
  plt.show()


# Simple SIR simulation (population-level, daily steps)
def run_sir_simulation(population_size=100, infection_probability=0.20, recovery_probability=0.05, days=30, initial_recovered=20):
  # States: 0 = susceptible, 1 = infected, 2 = recovered
  population = [0] * population_size
  # initialize recovered individuals (assumption)
  initial_recovered = min(max(0, initial_recovered), max(0, population_size - 1))
  for i in range(initial_recovered):
    population[i] = 2
  # seed a single infected individual after the recovered block when possible
  infect_index = initial_recovered if initial_recovered < population_size else 0
  population[infect_index] = 1  # seed with a single infected individual

  susceptible_history = []
  infected_history = []
  recovered_history = []

  for day in range(days):
    new_population = population.copy()
    for i in range(population_size):
      if population[i] == 1:
        # infected individual may infect susceptibles
        for j in range(population_size):
          if population[j] == 0 and random.random() < infection_probability:
            new_population[j] = 1
        # infected individual may recover
        if random.random() < recovery_probability:
          new_population[i] = 2

    population = new_population

    susceptible_history.append(population.count(0))
    infected_history.append(population.count(1))
    recovered_history.append(population.count(2))

  # Plot results over time
  days_range = list(range(1, days + 1))
  plt.plot(days_range, susceptible_history, label="Susceptible")
  plt.plot(days_range, infected_history, label="Infected")
  plt.plot(days_range, recovered_history, label="Recovered")
  plt.xlabel("Day")
  plt.ylabel("Count")
  plt.title("SIR Simulation Over Time")
  plt.legend()
  plt.show()


if __name__ == "__main__":
  random_walk_agents()
  run_sir_simulation()