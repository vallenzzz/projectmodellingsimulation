import simpy
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Simulation Parameters ---
N_CUSTOMERS = 300
N_SERVERS = 3
RANDOM_SEED = 42
INTERARRIVAL_TIME = 30.0  # Average time between arrivals
SERVICE_TIME = 40.0       # Average time to wait before departure
#SIM_TIME = 500           # Total minutes to simulate

# We will use these lists to collect data for analysis later!
wait_times = []
queue_times = [0.0]
queue_lengths = [0]

# Helper to record queue state as it changes

def record_queue_state(time, length):
    if queue_times and queue_times[-1] == time:
        queue_lengths[-1] = length
    else:
        queue_times.append(time)
        queue_lengths.append(length)

# --- 2. Defining the Processes ---

def customer(env, name, atm):
    """Models a single passenger waiting at the airport."""
    arrival_time = env.now
    print(f"[{arrival_time/60:06.2f}] {name} arrived at the airport.")
    
    # Request the Counter (This automatically adds the customer to the queue if it's busy)
    request = atm.request()
    record_queue_state(env.now, len(atm.queue))

    with request:
        # Pause the passenger until it's their turn
        yield request
        
        # Calculate how long they waited
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        print(f"[{env.now/60:06.2f}] {name} started arrived at the airport (Waited: {wait_time:.2f} mins). ")
        
        # Simulate the time it takes to wait
        # We use an exponential distribution for randomness
        time_at_airport = np.random.exponential(SERVICE_TIME)
        yield env.timeout(time_at_airport)

    # Record queue length after service completion and resource release
    record_queue_state(env.now, len(atm.queue))
    print(f"[{env.now/60:06.2f}] {name} finished waiting and departed.")

def customer_generator(env, atm):
    """Generates new customers up to N_CUSTOMERS."""
    customer_id = 1
    for _ in range(N_CUSTOMERS):
        # Determine the time until the NEXT customer arrives
        time_until_next = np.random.exponential(INTERARRIVAL_TIME)
        
        # Pause the generator until that time passes
        yield env.timeout(time_until_next)
        
        # Create a new customer process
        env.process(customer(env, f"Customer {customer_id}", atm))
        customer_id += 1

# --- 3. Running the Simulation ---
print("--- Airport Simulation ---")

# Set the random seed so our results are reproducible
np.random.seed(RANDOM_SEED)

# Create the environment and the single-server resource
env = simpy.Environment()
airport = simpy.Resource(env, capacity=N_SERVERS)

# Start the generator
env.process(customer_generator(env, airport))

# Run the simulation until all generated customer processes are complete
env.run()

print("\n--- Simulation Complete ---")

# 1. Calculate basic statistics
average_wait = np.mean(wait_times)
max_wait = np.max(wait_times)
total_passengers = len(wait_times)

print(f"Total passengers served: {total_passengers}")
print(f"Average wait time: {average_wait:.2f} minutes")
print(f"Maximum wait time: {max_wait:.2f} minutes")

# 2. Visualize the queue length over time
queue_hours = [t / 60 for t in queue_times]
plt.figure(figsize=(10, 5))
plt.step(queue_hours, queue_lengths, where='post', marker='o', color='b')
plt.yticks(range(0, max(queue_lengths) + 1))
plt.title("Number of passengers in queue vs. Time")
plt.xlabel("Time (Hours)")
plt.ylabel("Customers Waiting in Queue")
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.grid(True, alpha=0.5)
plt.show()

# 3. Visualize busy servers over time
busy_servers = [N_SERVERS - len(atm.queue) for atm in [airport] * len(queue_times)]
plt.figure(figsize=(10, 5))
plt.step(queue_hours, busy_servers, where='post', marker='o', color='g')
plt.yticks(range(0, max(queue_lengths) + 1))
plt.title("Number of Busy Servers vs. Time")
plt.xlabel("Time (Hours)")
plt.ylabel("Busy Servers")
plt.ylim(bottom=0, top=N_SERVERS)
plt.xlim(left=0)
plt.grid(True, alpha=0.5)
plt.show()

# 4. Visualize the distribution of wait times
plt.figure(figsize=(10, 5))
plt.hist(wait_times, bins=15, color='purple', edgecolor='black', alpha=0.7)
plt.title("Distribution of Wait Times")
plt.xlabel("Wait Time (Minutes)")
plt.ylabel("Number of Passengers")
plt.grid(axis='y', alpha=0.5)
plt.show()