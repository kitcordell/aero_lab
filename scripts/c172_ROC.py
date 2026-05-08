#%% Imports
from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from aircraft.c172_params import params
from solvers.trim_solver import max_ROC
from utils.plot_theme import AERO_COLORS, set_aerospace_theme, style_axes

DATA_DIR = ROOT_DIR / "data"

set_aerospace_theme()



# initial guess = [theta, delta_e, gamma]
theta_guess = np.deg2rad(5.0)  # 5 degrees
delta_e_guess = np.deg2rad(-2.0)  # -2 degrees
gamma_guess = np.deg2rad(3.0)  # 3 degrees climb

x0 = np.array([theta_guess, delta_e_guess, gamma_guess])


throttle = 1.0
V = 90.0
alt_0 = 0
trim_target = [throttle, V, alt_0]

min_alt = 0
max_alt = 12000

alt_array = np.arange(min_alt, max_alt + 1000, 1000)  # Altitude array from 0 to 12,000 ft in 1,000 ft increments
ROC_alt_array = np.zeros_like(alt_array, dtype=float)  # To store max ROC at each altitude

#%% Compute max ROC across altitudes
for i, altitude in enumerate(alt_array):
    trim_target[2] = altitude
    V_array, ROC_array, V_max_ROC, ROC_max = max_ROC(x0, trim_target, params, verbose=False)
    ROC_alt_array[i] = ROC_max


#%% POH Data
roc_poh = pd.read_csv(DATA_DIR / "c172_roc.csv",sep=",",engine="python",skipinitialspace=True) # read POH data

print("\n", roc_poh)

poh_roc_alt = roc_poh["press_alt_ft"]
poh_roc_0C = roc_poh["fpm_0C"]
poh_roc_M20C = roc_poh["fpm_M20C"]
poh_roc_20C = roc_poh["fpm_20C"]
poh_roc_40C = roc_poh["fpm_40C"]

# Plot POH ROC vs simulated ROC and speed sweep together
fig, (ax_alt, ax_speed) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("C172 Climb Performance", fontsize=13, fontweight="bold")

ax_alt.plot(poh_roc_alt, poh_roc_20C, label="POH ROC", color=AERO_COLORS["amber"])
ax_alt.plot(alt_array, ROC_alt_array * 60, label="Sim ROC", color=AERO_COLORS["cyan"])
ax_alt.set_title("Rate of Climb vs Altitude @ 20C")
ax_alt.set_xlabel("Altitude (ft)")
ax_alt.set_ylabel("Rate of Climb (ft/min)")
ax_alt.legend()
style_axes(ax_alt)

ax_speed.plot(V_array, ROC_array * 60, label="Rate of Climb", color=AERO_COLORS["green"])
ax_speed.plot(
    V_max_ROC,
    ROC_max * 60,
    "o",
    color=AERO_COLORS["red"],
    markeredgecolor=AERO_COLORS["text"],
    label="Max ROC",
)
ax_speed.set_title("Rate of Climb vs Airspeed")
ax_speed.set_xlabel("Airspeed (ft/s)")
ax_speed.set_ylabel("Rate of Climb (ft/min)")
ax_speed.legend()
style_axes(ax_speed)

fig.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
