from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.gan_simulator.frequency_sweep import analyze_frequency_sweep
from src.gan_simulator.parameters import SwitchingParameters

base_parameters = SwitchingParameters(
    voltage_v=400,
    current_a=10,
    frequency_hz=100_000,
    rds_on_ohm=0.05,
    rise_time_s=20e-9,
    fall_time_s=20e-9,
    gate_charge_c=10e-9,
    gate_voltage_v=5,
    output_power_w=500,
)

frequencies = [
    50_000,
    100_000,
    150_000,
    200_000,
    250_000,
    300_000,
    400_000,
    500_000,
]

results = analyze_frequency_sweep(base_parameters, frequencies)

frequency_khz = [r["frequency_hz"] / 1000 for r in results]
conduction = [r["conduction_loss_w"] for r in results]
switching = [r["switching_loss_w"] for r in results]
gate_drive = [r["gate_drive_loss_w"] for r in results]
total = [r["total_loss_w"] for r in results]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].plot(frequency_khz, conduction, marker="o", label="Conduction loss")
axes[0].plot(frequency_khz, switching, marker="s", label="Switching loss")
axes[0].plot(frequency_khz, gate_drive, marker="^", label="Gate-drive loss")
axes[0].set_xlabel("Switching frequency (kHz)")
axes[0].set_ylabel("Power loss (W)")
axes[0].set_title("Individual Loss Components")
axes[0].grid(True)
axes[0].legend()

axes[1].plot(frequency_khz, total, marker="o")
axes[1].set_xlabel("Switching frequency (kHz)")
axes[1].set_ylabel("Total transistor loss (W)")
axes[1].set_title("Total Loss vs Switching Frequency")
axes[1].grid(True)

plt.tight_layout()
plt.show()
