from pathlib import Path
import sys

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
from src.gan_simulator.waveforms import generate_switching_waveforms

waveforms = generate_switching_waveforms(
    voltage_v=400,
    current_a=10,
    frequency_hz=100_000,
    rise_time_s=20e-9,
    fall_time_s=20e-9,
)

time_us = waveforms["time_s"] * 1e6

fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

axes[0].plot(time_us, waveforms["voltage_v"])
axes[0].set_ylabel("Drain-source voltage (V)")
axes[0].set_title("Illustrative GaN Switching Waveforms")
axes[0].grid(True)

axes[1].plot(time_us, waveforms["current_a"])
axes[1].set_xlabel("Time (µs)")
axes[1].set_ylabel("Drain current (A)")
axes[1].grid(True)

plt.tight_layout()
plt.show()
