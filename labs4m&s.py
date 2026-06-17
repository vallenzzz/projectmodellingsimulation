import simpy
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Simulation Parameters ---
RANDOM_SEED = 42
INTERARRIVAL_TIME = 3.0  # Average time between arrivals
SERVICE_TIME = 4.0       # Average time to use the ATM
SIM_TIME = 500           # Total minutes to simulate

# We will use this list to collect data for analysis later!
wait_times = []

# --- 2. Defining the Processes ---

def customer(env, name, atm):
    """Models a single customer using the ATM."""
    arrival_time = env.now
    print(f"[{arrival_time:06.2f}] {name} arrived at the ATM.")
    
    # Request the ATM (This automatically adds the customer to the queue if it's busy)
    with atm.request() as request:
        # Pause the customer until it's their turn
        yield request
        
        # Calculate how long they waited
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        print(f"[{env.now:06.2f}] {name} started using the ATM (Waited: {wait_time:.2f} mins).")
        
        # Simulate the time it takes to do the bank transaction
        # We use an exponential distribution for randomness
        time_at_atm = np.random.exponential(SERVICE_TIME)
        yield env.timeout(time_at_atm)
        
        print(f"[{env.now:06.2f}] {name} finished and left.")

def customer_generator(env, atm):
    """Generates new customers infinitely over time."""
    customer_id = 1
    while True:
        # Determine the time until the NEXT customer arrives
        time_until_next = np.random.exponential(INTERARRIVAL_TIME)
        
        # Pause the generator until that time passes
        yield env.timeout(time_until_next)
        
        # Create a new customer process
        env.process(customer(env, f"Customer {customer_id}", atm))
        customer_id += 1

# --- 3. Running the Simulation ---
print("--- Single-Server ATM Simulation ---")

# Set the random seed so our results are reproducible
np.random.seed(RANDOM_SEED)

# Create the environment and the single-server resource
env = simpy.Environment()
atm = simpy.Resource(env, capacity=1)

# Start the generator
env.process(customer_generator(env, atm))

# Run the virtual clock!
env.run(until=SIM_TIME)

print("\n--- Simulation Complete ---")

# 1. Calculate basic statistics
average_wait = np.mean(wait_times)
max_wait = np.max(wait_times)
total_customers = len(wait_times)

print(f"Total customers served: {total_customers}")
print(f"Average wait time: {average_wait:.2f} minutes")
print(f"Maximum wait time: {max_wait:.2f} minutes")

# 2. Visualize the Wait Times
plt.figure(figsize=(10, 5))
plt.plot(range(1, total_customers + 1), wait_times, marker='o', linestyle='-', color='b')

plt.title("Customer Wait Times at the ATM")
plt.xlabel("Customer Number (in order of arrival)")
plt.ylabel("Wait Time (Minutes)")
plt.axhline(y=average_wait, color='r', linestyle='--', label=f'Avg Wait: {average_wait:.2f} min')
plt.legend()
plt.grid(True, alpha=0.5)

plt.show()

# 3. View the distribution of wait times
plt.figure(figsize=(10, 5))
plt.hist(wait_times, bins=15, color='purple', edgecolor='black', alpha=0.7)
plt.title("Distribution of Wait Times")
plt.xlabel("Wait Time (Minutes)")
plt.ylabel("Number of Customers")
plt.grid(axis='y', alpha=0.5)
plt.show()