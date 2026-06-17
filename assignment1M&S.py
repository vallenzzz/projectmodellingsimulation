import numpy as np
import simpy
import matplotlib.pyplot as plt
import scipy.io as sio # To export data for MATLAB

# --- 1. System Parameters (from Table 1 & 2 of the source) ---
FN = 1500.0          # Normal Load [N]
MU_0 = 0.134         # Static friction coefficient [5, 6]
SPEED_RANGE = np.linspace(0, 500, 50) # Shaft speed n [1/min] [3, 6]
VISCOSITY_90C = 0.01021 # Dynamic viscosity eta_0 [Pa*s] [6]
ALPHA = 1.2e-8       # Pressure viscosity coefficient [6]
NOMINAL_AREA = (133e-6) * (133e-6) # Micro-model area [m^2] [7]
H_RANGE = np.linspace(0.1, 1.63, 100) # Gap height [micrometers] up to RzSum

#Inputs with +10% variation
#FN = 1650.0
#MU_0 = 0.147
#SPEED_RANGE = np.linspace(0, 550, 50)
#VISCOSITY_90C = 0.01123
#ALPHA = 1.32e-8
#NOMINAL_AREA = (133e-6) * (133e-6)
#H_RANGE = np.linspace(0.1, 1.63, 100) # Gap height [micrometers] up to RzSum

#Inputs with +20% variation
#FN = 1800.0
#MU_0 = 0.161
#SPEED_RANGE = np.linspace(0, 600, 50)
#VISCOSITY_90C = 0.01225
#ALPHA = 1.44e-8
#NOMINAL_AREA = (133e-6) * (133e-6)
#H_RANGE = np.linspace(0.1, 1.63, 100) # Gap height [micrometers] up to RzSum


# --- 2. Deterministic Contact Model (Functional Placeholder) ---
# In the paper, this is solved by Abaqus [8]. 
# Here we use the derived relationship p_Asp(h) [7, 9].
def calculate_p_asp(h):
    """Calculates asperity contact pressure based on gap height h."""
    # Based on Fig 13, pressure increases exponentially as h decreases.
    # We use an approximation of the 'FEM elastic' curve.
    if h > 1.6: # RzSum limit [10]
        return 0.0
    return 10**6 * np.exp(-5 * h) # Simulated p_Asp(h) curve in [Pa]


# --- 3. Macro Model: Friction Calculation ---
def calculate_friction(n, h_equi):
    """Calculates total COF at a specific speed and gap height equilibrium."""
    # Hydrodynamic friction (simplified Reynolds approach) [11, 12]
    # In reality, this requires solving Eq. 2 & 3 in the source.
    mu_hyd = 0.001 * (n / 500) * (1.0 / h_equi) 
    
    # Solid friction contribution [5, 13]
    p_asp = calculate_p_asp(h_equi)
    f_asp = p_asp * NOMINAL_AREA 
    mu_asp = MU_0 * (f_asp / FN)
    
    return mu_hyd + mu_asp


# --- 4. Asperity Contact Pressure Curve Calculation (p_Asp(h)) ---
# According to Eq. 20, p_Asp(h) = F(h) / A. 
# We approximate the "FEM elastic" curve from Figure 13 for this simulation.
def get_p_asp_curve(h_values):
    """
    Simulates the deterministic FEM output for pressure vs. gap height.
    Pressure is measured in Pa (N/m^2).
    """
    # Based on Fig 13, p_Asp is ~100MPa at h=0.2 and ~0.001MPa at h=1.2
    # This exponential decay approximates the deterministic FEM results.
    pressures_pa = 2.5e8 * np.exp(-7.5 * h_values) 
    return pressures_pa

# --- 5. Solid Friction Contribution Calculation (mu_Asp) ---
def calculate_solid_friction(p_asp_val):
    """
    Calculates the solid friction component using Eq. 6:
    mu_Asp = mu_0 * (F_Asp / FN)
    where F_Asp = integral of p_Asp over the area A.
    """
    # Resulting force from asperity contact pressure [Section 26]
    f_asp = p_asp_val * NOMINAL_AREA 
    
    # Solid friction contribution to total COF [Eq. 6]
    mu_asp = MU_0 * (f_asp / FN)
    return mu_asp

# --- 6. Generate Results ---
p_asp_results = get_p_asp_curve(H_RANGE)
mu_asp_results = [calculate_solid_friction(p) for p in p_asp_results]
print("Calculated asperity pressures and solid friction contributions for the given gap heights.")
print("Sample results:")
for h, p, mu in zip(H_RANGE[::10], p_asp_results[::10], mu_asp_results[::10]):
    print(f"Gap Height: {h:.2f} micrometers, Asperity Pressure: {p:.2e} Pa, Solid Friction COF: {mu:.4f}")


# --- 7. SimPy Simulation of the Stribeck Cycle ---
def stribeck_test_process(env, results):
    """Simulates the experimental Start/Stop cycle described in Fig 3."""
    for speed in SPEED_RANGE:
        # Step 1: Find equilibrium gap height h (Simplified iterative solver)
        # In the source, this is an iterative EHD equilibrium [13].
        h_equi = 1.2 - (speed / 1000) # Simplified h variation with speed
        
        # Step 2: Calculate COF
        cof = calculate_friction(speed, h_equi)
        
        # Log results
        results.append((speed, cof))
        
        # Simulate time for the speed ramp [4]
        yield env.timeout(0.1) 


# --- 8. Execution ---
env = simpy.Environment()
stribeck_results = []
env.process(stribeck_test_process(env, stribeck_results))
env.run()


# --- 9. Export for MATLAB / Plotting ---
speeds, cofs = zip(*stribeck_results)
data_to_export = {'speed': np.array(speeds), 'cof': np.array(cofs)}
sio.savemat('stribeck_data.mat', data_to_export)

print("Simulation complete. Data saved to 'stribeck_data.mat' for MATLAB.")

# Python visualization (as a backup)
plt.semilogy(speeds, cofs)
plt.title("Simulated Stribeck Curve (Deterministic Model Logic)")
plt.xlabel("Speed [min^-1]")
plt.ylabel("COF [-]")
plt.grid(True, which="both")
plt.show()
