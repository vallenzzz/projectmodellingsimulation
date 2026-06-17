import matplotlib.pyplot as plt
import networkx as nx
import numpy as np # Ensure numpy is imported for np.random.poisson
import random # Ensure random is imported for random.sample

# Proposed Additional Parameters for Malware Spread (not yet integrated into simulation logic)
vulnerability_rate = 0.8  # 80% of susceptible machines have a exploitable vulnerability
user_click_probability = 0.3 # 30% chance a user clicks a malicious link/attachment
#antivirus_adoption_rate = 0.6 # 60% of computers have antivirus installed
#patch_cycle_days = 7 # Average 7 days to patch a system after vulnerability detected
#reinfection_probability = 0.05 # 5% chance a 'recovered' machine can be re-infected
#quarantine_effectiveness = 0.7 # 70% chance an infected machine is successfully quarantined

# Malware Spread Parameters
malware_infection_probability = 0.5    # Higher chance of malware spreading on contact
malware_recovery_probability_mean = 0.08 # Slightly slower recovery for malware
malware_recovery_probability_std = 0.04 # Variability in patching/antivirus effectiveness

malware_days = 120                      # Simulation duration for malware spread
malware_N = 1000                        # Total computers in the network

# Initial network state for Malware
malware_S0 = 990                        # Many susceptible computers
malware_I0 = 10                         # A few initial infected machines
malware_R0 = 0                          # No recovered initially

# Generate individual recovery probabilities for each computer
malware_peer_recovery_probabilities = np.random.normal(loc=malware_recovery_probability_mean, scale=malware_recovery_probability_std, size=malware_N)
malware_peer_recovery_probabilities = np.clip(malware_peer_recovery_probabilities, 0.0, 1.0) # Ensure probabilities are between 0 and 1

np.random.seed(42)
random.seed(42)

# Create a random graph for the network topology
# Using Erdos-Renyi graph for simplicity: N nodes, p probability of edge creation
# N = total peers (from model parameters)
# p = probability of connection (adjust as needed for desired network density)

# For this example, let's aim for an average degree (average number of neighbors) of approximately 10.
# For an Erdos-Renyi graph, average degree = p * (N-1).
# So, p = average_degree / (N-1)

N_peers = malware_N # Use the N defined in the previous cell
avg_degree = 10
connection_probability = avg_degree / (N_peers - 1)

G = nx.erdos_renyi_graph(n=N_peers, p=connection_probability, seed=42)


def run_p2p_propagation_simulation_with_network(graph_G, current_infection_probability, current_peer_recovery_probabilities, num_peers, initial_S, initial_I, initial_R, simulation_days, vulnerability_rate, user_click_probability):
    """Agent-based P2P file propagation simulation with network topology and heterogeneous recovery rates"""
    # Initialize population: each agent has a state (0=S, 1=I, 2=R)
    population = [0] * initial_S + [1] * initial_I + [2] * initial_R
    random.shuffle(population)

    susceptible_history = []
    infected_history = []
    recovered_history = []

    for day in range(simulation_days):
        new_population = population.copy()

        # Get indices of seeders
        seeders = [i for i in range(num_peers) if population[i] == 1]

        # Seeders attempt to infect susceptible neighbors
        for seeder_idx in seeders:
            # Get neighbors of the current seeder
            neighbors = list(graph_G.neighbors(seeder_idx))

            if neighbors:
                num_contacts_attempted = np.random.poisson(lam=3)
                contacted_neighbors = random.sample(neighbors, min(num_contacts_attempted, len(neighbors)))

                for neighbor_idx in contacted_neighbors:
                    if population[neighbor_idx] == 0 and random.random() < current_infection_probability:
                        new_population[neighbor_idx] = 1  # Susceptible neighbor becomes seeder

            # Seeder may stop sharing based on its individual recovery probability
            if random.random() < current_peer_recovery_probabilities[seeder_idx]:
                new_population[seeder_idx] = 2  # Seeder becomes recovered

        population = new_population

        # Track population statistics
        susceptible_history.append(population.count(0))
        infected_history.append(population.count(1))
        recovered_history.append(population.count(2))

    return susceptible_history, infected_history, recovered_history


# Run multiple stochastic simulations for Malware Spread
num_simulations_malware = 100
all_S_malware = []
all_I_malware = []
all_R_malware = []

# Regenerate graph for this simulation if N changes, otherwise reuse G
# For simplicity, reusing G with N=1000 from previous setup. If malware_N were different, a new graph would be needed.

for sim in range(num_simulations_malware):
    S_sim, I_sim, R_sim = run_p2p_propagation_simulation_with_network(
        G,
        malware_infection_probability,
        malware_peer_recovery_probabilities,
        malware_N,
        malware_S0,
        malware_I0,
        malware_R0,
        malware_days,
        vulnerability_rate, # Pass vulnerability rate
        user_click_probability # Pass user click probability
    )
    all_S_malware.append(S_sim)
    all_I_malware.append(I_sim)
    all_R_malware.append(R_sim)

# Convert to numpy arrays for easier calculation
all_S_malware = np.array(all_S_malware)
all_I_malware = np.array(all_I_malware)
all_R_malware = np.array(all_R_malware)

# Calculate statistics (mean and 95% confidence intervals)
mean_S_malware = np.mean(all_S_malware, axis=0)
std_S_malware = np.std(all_S_malware, axis=0)
mean_I_malware = np.mean(all_I_malware, axis=0)
std_I_malware = np.std(all_I_malware, axis=0)
mean_R_malware = np.mean(all_R_malware, axis=0)
std_R_malware = np.std(all_R_malware, axis=0)

ci_95_S_malware = 1.96 * std_S_malware
ci_95_I_malware = 1.96 * std_I_malware
ci_95_R_malware = 1.96 * std_R_malware

# Plot results with 95% confidence intervals
days_array_malware = np.arange(len(mean_S_malware))
plt.figure(figsize=(12, 7))

plt.plot(days_array_malware, mean_S_malware, label="Susceptible (Uninfected Computers)", linewidth=2, color='blue')
# plt.fill_between(days_array_malware, mean_S_malware - ci_95_S_malware, mean_S_malware + ci_95_S_malware, alpha=0.2, color='blue')

plt.plot(days_array_malware, mean_I_malware, label="Infected (Actively Spreading Malware)", linewidth=2, color='red')
# plt.fill_between(days_array_malware, mean_I_malware - ci_95_I_malware, mean_I_malware + ci_95_I_malware, alpha=0.2, color='red')

plt.plot(days_array_malware, mean_R_malware, label="Recovered (Patched/Cleaned Computers)", linewidth=2, color='green')
# plt.fill_between(days_array_malware, mean_R_malware - ci_95_R_malware, mean_R_malware + ci_95_R_malware, alpha=0.2, color='green')

plt.xlabel("Days")
plt.ylabel("Number of Computers")
plt.title("Malware Spread in a Computer Network (100 simulations with 95% CI)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Analyze peak infected statistics across simulations
peak_infected_all_malware = [max(all_I_malware[i]) for i in range(num_simulations_malware)]
peak_days_all_malware = [np.argmax(all_I_malware[i]) for i in range(num_simulations_malware)]

print("="*60)
print("MALWARE SPREAD IN COMPUTER NETWORK - STATISTICS")
print("="*60)
print(f"Number of simulations: {num_simulations_malware}")
print(f"Network size: {malware_N} computers")
print(f"Network type: Erdos-Renyi graph (p={connection_probability:.4f})") # Assuming G is reused
print(f"Initial state: {malware_S0} susceptible, {malware_I0} infected, {malware_R0} recovered")
print(f"\nInfection probability per contact: {malware_infection_probability}")
print(f"Heterogeneous Recovery Rates (Mean: {malware_recovery_probability_mean}, Std: {malware_recovery_probability_std})")
print(f"Vulnerability Rate: {vulnerability_rate}")
print(f"User Click Probability: {user_click_probability}")
print("\nPEAK INFECTED STATISTICS:")
print(f"  Mean peak infected: {np.mean(peak_infected_all_malware):.1f} \u00b1 {np.std(peak_infected_all_malware):.1f}")
print(f"  Min peak infected: {min(peak_infected_all_malware)}")
print(f"  Max peak infected: {max(peak_infected_all_malware)}")
print("\nPEAK TIMING STATISTICS:")
print(f"  Mean peak day: {np.mean(peak_days_all_malware):.1f} \u00b1 {np.std(peak_days_all_malware):.1f} days")
print(f"  Peak day range: {min(peak_days_all_malware)} - {max(peak_days_all_malware)} days")
print(f"\nFINAL STATE (Day {malware_days}):")
print(f"  Final susceptible (mean): {mean_S_malware[-1]:.1f}")
print(f"  Final infected (mean): {mean_I_malware[-1]:.1f}")
print(f"  Final recovered (mean): {mean_R_malware[-1]:.1f}")
print("="*60)


