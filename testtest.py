import numpy as np
import scipy.io as sio

# --- 1. System Inputs (from Table 2 and Section 2.3.2.4) ---
FN = 1500.0           # Normal Load [N]
MU_0 = 0.134          # Static friction coefficient captured from experiments
NOMINAL_AREA = (133e-6) * (133e-6) # Micro-model area [m^2] from Section 2.2.2
H_RANGE = np.linspace(0.1, 1.63, 100) # Gap height [micrometers] up to RzSum

# --- 2. Asperity Contact Pressure Curve Calculation (p_Asp(h)) ---
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

# --- 3. Solid Friction Contribution Calculation (mu_Asp) ---
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

# --- 4. Generate Results ---
p_asp_results = get_p_asp_curve(H_RANGE)
mu_asp_results = [calculate_solid_friction(p) for p in p_asp_results]
print("Calculated asperity pressures and solid friction contributions for the given gap heights.")
print("Sample results:")
for h, p, mu in zip(H_RANGE[::10], p_asp_results[::10], mu_asp_results[::10]):
    print(f"Gap Height: {h:.2f} micrometers, Asperity Pressure: {p:.2e} Pa, Solid Friction COF: {mu:.4f}")

# Export for MATLAB
data_to_export = {
    'gap_height': H_RANGE,
    'asperity_pressure': p_asp_results,
    'solid_friction': np.array(mu_asp_results)
}
sio.savemat('contact_model_results.mat', data_to_export)

print("Calculation complete. Data saved for MATLAB.")