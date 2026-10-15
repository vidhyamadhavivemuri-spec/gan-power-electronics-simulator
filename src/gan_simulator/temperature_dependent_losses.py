
"""Estimate transistor losses using temperature-dependent on-resistance."""

import math

from src.gan_simulator.loss_model import calculate_losses
from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.temperature_model import (
    estimate_temperature_dependent_resistance,
)


def calculate_temperature_dependent_losses(
    parameters: SwitchingParameters,
    reference_temperature_c: float,
    junction_temperature_c: float,
    temperature_coefficient_per_c: float,
) -> dict[str, float]:
    """Recalculate losses using on-resistance at junction temperature.

    Switching and gate-drive losses retain the existing simplified model.
    Only conduction loss is adjusted for junction temperature.
    """
    temperatures_and_coefficients = (
        reference_temperature_c,
        junction_temperature_c,
        temperature_coefficient_per_c,
    )

    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in temperatures_and_coefficients
    ):
        raise ValueError("Temperatures and coefficient must be finite numbers.")

    baseline_losses = calculate_losses(parameters)

    resistance_result = estimate_temperature_dependent_resistance(
        reference_resistance_ohm=parameters.rds_on_ohm,
        reference_temperature_c=reference_temperature_c,
        junction_temperature_c=junction_temperature_c,
        temperature_coefficient_per_c=temperature_coefficient_per_c,
    )

    adjusted_conduction_loss_w = (
        parameters.current_a**2
        * resistance_result["estimated_resistance_ohm"]
    )

    switching_loss_w = baseline_losses["switching_loss_w"]
    gate_drive_loss_w = baseline_losses["gate_drive_loss_w"]

    total_loss_w = (
        adjusted_conduction_loss_w
        + switching_loss_w
        + gate_drive_loss_w
    )

    efficiency_percent = (
        100 * parameters.output_power_w
        / (parameters.output_power_w + total_loss_w)
    )

    return {
        "junction_temperature_c": float(junction_temperature_c),
        "estimated_resistance_ohm": (
            resistance_result["estimated_resistance_ohm"]
        ),
        "conduction_loss_w": adjusted_conduction_loss_w,
        "switching_loss_w": switching_loss_w,
        "gate_drive_loss_w": gate_drive_loss_w,
        "total_loss_w": total_loss_w,
        "estimated_efficiency_percent": efficiency_percent,
    }
