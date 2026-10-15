import numpy as np
import matplotlib.pyplot as plt

from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.frequency_thermal_analysis import (
    analyze_frequency_thermal_behavior,
)


parameters = SwitchingParameters(
    voltage_v=400,
    current_a=10,
    frequency_hz=100_000,
    rds_on_ohm=0.05,
    rise_time_s=20e-9,
    fall_time_s=20e-9,
    gate_charge_c=20e-9,
    gate_voltage_v=5,
    output_power_w=1000,
)

frequencies_hz = np.linspace(50_000, 500_000, 50)

results = analyze_frequency_thermal_behavior(
    base_parameters=parameters,
    frequencies_hz=frequencies_hz.tolist(),
    ambient_temperature_c=25,
    thermal_resistance_c_per_w=2,
)

frequencies_khz = [
    result["frequency_hz"] / 1000 for result in results
]
total_losses_w = [result["total_loss_w"] for result in results]
junction_temperatures_c = [
    result["junction_temperature_c"] for result in results
]

fig, ax1 = plt.subplots(figsize=(10, 6))

loss_line = ax1.plot(
    frequencies_khz,
    total_losses_w,
    label="Total Power Loss",
    linewidth=2,
)
ax1.set_xlabel("Switching Frequency (kHz)")
ax1.set_ylabel("Total Power Loss (W)")
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
temperature_line = ax2.plot(
    frequencies_khz,
    junction_temperatures_c,
    label="Junction Temperature",
    linewidth=2,
    linestyle="--",
)
ax2.set_ylabel("Junction Temperature (°C)")

lines = loss_line + temperature_line
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="upper left")

plt.title("Switching Frequency vs Power Loss and Junction Temperature")
fig.tight_layout()

output_path = "examples/frequency_vs_temperature.png"
fig.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"Graph saved to {output_path}")
plt.show()
