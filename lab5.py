import numpy as np
import matplotlib.pyplot as plt

# 1. Define the State Space
states = ["Sunny", "Rainy"]

# 2. Define the Transition Matrix
# Row 0: Sunny probabilities [Sunny->Sunny, Sunny->Rainy]
# Row 1: Rainy probabilities [Rainy->Sunny, Rainy->Rainy]
transition_matrix = [
    [0.7, 0.3],  
    [0.5, 0.5]   
]

def simulate_markov_chain(days, start_state):
    """Simulates the weather over a given number of days."""
    # We use a list to keep track of the history for our graph
    weather_history = [start_state]
    current_state = start_state
    
    for _ in range(days):
        # Find the index of our current state (0 for Sunny, 1 for Rainy)
        state_index = states.index(current_state)
        
        # Look up the probabilities for tomorrow based on today
        probabilities = transition_matrix[state_index]
        
        # THE MARKOV MAGIC: Pick the next state using numpy's random choice!
        # p=probabilities tells numpy to weight the dice roll
        next_state = np.random.choice(states, p=probabilities)
        
        weather_history.append(next_state)
        current_state = next_state # Update our state for the next loop
        
    return weather_history

# --- Run the Simulation ---
np.random.seed(42) # For reproducible results
total_days = 30

# Let's say today is Sunny. What does the next month look like?
simulated_month = simulate_markov_chain(total_days, start_state="Sunny")

# Count the results
sunny_days = simulated_month.count("Sunny")
rainy_days = simulated_month.count("Rainy")

print(f"Over {total_days} days, we had {sunny_days} Sunny days and {rainy_days} Rainy days.")

# --- Visualize the output ---
# Convert strings to numbers for graphing (Sunny=1, Rainy=0)
numeric_weather = [1 if day == "Sunny" else 0 for day in simulated_month]

plt.figure(figsize=(10, 3))
plt.step(range(total_days + 1), numeric_weather, where='post', color='orange')
plt.yticks([0, 1], ['Rainy', 'Sunny'])
plt.title("30-Day Markov Chain Weather Simulation")
plt.xlabel("Days")
plt.grid(axis='y', alpha=0.5)
plt.show()