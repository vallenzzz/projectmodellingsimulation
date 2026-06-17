import numpy as np
import matplotlib.pyplot as plt

# 1. Define the State Space
states = ["Patrol", "Chase", "Attack"]

# 2. Define the Transition Matrix
# Order: [Patrol, Chase, Attack]
transition_matrix = [
    [0.7, 0.3, 0.0],  # Probabilities if currently Patrolling
    [0.1, 0.6, 0.3],  # Probabilities if currently Chasing
    [0.0, 0.4, 0.6]   # Probabilities if currently Attacking
]

def simulate_enemy_ai(ticks, start_state):
    """Simulates the AI's behavior over a given number of engine ticks."""
    ai_history = [start_state]
    current_state = start_state
    
    for _ in range(ticks):
        # Find the index of our current state (0, 1, or 2)
        state_index = states.index(current_state)
        
        # Look up the transition probabilities for the current state
        probabilities = transition_matrix[state_index]
        
        # Pick the next state using the probabilities
        next_state = np.random.choice(states, p=probabilities)
        
        ai_history.append(next_state)
        current_state = next_state
        
    return ai_history

# --- Run the Simulation ---
np.random.seed(10) # Set seed for reproducibility
total_ticks = 50

# The guard spawns into the game in the 'Patrol' state
simulated_behavior = simulate_enemy_ai(total_ticks, start_state="Patrol")

# Count the time spent in each state
patrol_time = simulated_behavior.count("Patrol")
chase_time = simulated_behavior.count("Chase")
attack_time = simulated_behavior.count("Attack")

print("--- AI Simulation Results ---")
print(f"Total Ticks Simulated: {total_ticks}")
print(f"Time Patrolling: {patrol_time} ticks ({(patrol_time/total_ticks)*100:.1f}%)")
print(f"Time Chasing: {chase_time} ticks ({(chase_time/total_ticks)*100:.1f}%)")
print(f"Time Attacking: {attack_time} ticks ({(attack_time/total_ticks)*100:.1f}%)")

# Convert strings to numeric values for our y-axis (Patrol=0, Chase=1, Attack=2)
numeric_states = [states.index(state) for state in simulated_behavior]

plt.figure(figsize=(12, 4))
# We use a step plot because state changes are discrete (instantaneous)
plt.step(range(total_ticks + 1), numeric_states, where='post', color='red', linewidth=2)

# Format the graph
plt.yticks([0, 1, 2], states)
plt.title("Enemy AI Behavior Over Time (Markov Chain)")
plt.xlabel("Game Engine Ticks")
plt.ylabel("AI State")
plt.grid(axis='y', alpha=0.5, linestyle='--')

plt.show()