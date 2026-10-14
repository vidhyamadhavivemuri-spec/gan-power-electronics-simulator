"""Plot power losses against switching frequency."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.frequency_sweep import analyze_frequency_sweep


def main():
    # Example operating conditions for educational simulation.
    base_parameters = SwitchingParameters(
        voltage_v=400.0,
        current_a=10.0,
        frequency_hz=100_000.0,
        rds_on_ohm=0.05,
        rise_time_s=20e-9,
        fall_time_s=20e-9,
        gate_charge_c=20e-9,
        gate_voltage_v=5.0,
        output_power_w=1000.0,
    )

    # Sweep from 50 kHz to 500 kHz.
    frequencies_hz = np.linspace(50_000, 500_000, 50)

    results = analyze_frequency_sweep(
        base_parameters,
        frequencies_hz.tolist(),
    )

    frequencies_khz = frequencies_hz / 1000.0
    conduction_losses = [
        result["conduction_loss_w"] for result in results
    ]

    switching_losses = [
        result["switching_loss_w"] for result in results
    ]

    gate_drive_losses = [
        result["gate_drive_loss_w"] for result in results
    ]

    total_losses = [
        result["total_loss_w"] for result in results
    ]


    plt.figure(figsize=(10, 6))
    plt.plot(frequencies_khz, conduction_losses, label="Conduction loss")
    plt.plot(frequencies_khz, switching_losses, label="Switching loss")
    plt.plot(frequencies_khz, gate_drive_losses, label="Gate-drive loss")
    plt.plot(frequencies_khz, total_losses, label="Total loss", linewidth=2)

    plt.title("Power Loss vs. Switching Frequency")
    plt.xlabel("Switching frequency (kHz)")
    plt.ylabel("Estimated power loss (W)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = PROJECT_ROOT / "examples" / "frequency_vs_loss.png"
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
