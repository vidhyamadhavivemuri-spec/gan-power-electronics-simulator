
"""Iterative electrothermal analysis using all modeled transistor losses."""

import math

from .loss_model import calculate_losses
from .parameters import SwitchingParameters
from .temperature_dependent_losses import (
    calculate_temperature_dependent_losses,
)
from .thermal_analysis import estimate_junction_temperature


def solve_full_electrothermal(
    parameters: SwitchingParameters,
    ambient_temperature_c: float,
    thermal_resistance_c_per_w: float,
    temperature_coefficient_per_c: float,
    reference_temperature_c: float = 25.0,
    initial_temperature_c: float | None = None,
    tolerance_c: float = 0.01,
    max_iterations: int = 1000,
) -> dict[str, float | int | bool]:
    """Iterate total transistor losses and junction temperature.

    Conduction loss changes with junction temperature. Switching and
    gate-drive losses remain temperature-independent in this simplified
    model.

    Returns a result with convergence status, iteration count, losses,
    estimated junction temperature, and efficiency.
    """
    numeric_values = {
        "ambient_temperature_c": ambient_temperature_c,
        "thermal_resistance_c_per_w": thermal_resistance_c_per_w,
        "temperature_coefficient_per_c": temperature_coefficient_per_c,
        "reference_temperature_c": reference_temperature_c,
        "tolerance_c": tolerance_c,
    }

    for name, value in numeric_values.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"{name} must be a finite number.")

    if thermal_resistance_c_per_w < 0:
        raise ValueError("Thermal resistance cannot be negative.")
    if temperature_coefficient_per_c < 0:
        raise ValueError("Temperature coefficient cannot be negative.")
    if tolerance_c <= 0:
        raise ValueError("Tolerance must be positive.")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int):
        raise ValueError("max_iterations must be a positive integer.")
    if max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer.")

    if initial_temperature_c is None:
        temperature_c = float(ambient_temperature_c)
    else:
        if (
            isinstance(initial_temperature_c, bool)
            or not isinstance(initial_temperature_c, (int, float))
            or not math.isfinite(initial_temperature_c)
        ):
            raise ValueError("Initial temperature must be a finite number.")
        temperature_c = float(initial_temperature_c)

    baseline = calculate_losses(parameters)

    for iteration in range(1, max_iterations + 1):
        adjusted = calculate_temperature_dependent_losses(
            parameters=parameters,
            reference_temperature_c=reference_temperature_c,
            junction_temperature_c=temperature_c,
            temperature_coefficient_per_c=temperature_coefficient_per_c,
        )

        thermal_result = estimate_junction_temperature(
            power_loss_w=adjusted["total_loss_w"],
            ambient_temperature_c=ambient_temperature_c,
            thermal_resistance_c_per_w=thermal_resistance_c_per_w,
        )
        updated_temperature_c = thermal_result["junction_temperature_c"]

        if not math.isfinite(updated_temperature_c):
            raise ValueError("Temperature estimate became nonfinite.")

        if abs(updated_temperature_c - temperature_c) <= tolerance_c:
            # Recalculate losses at the converged temperature.
            final_losses = calculate_temperature_dependent_losses(
                parameters=parameters,
                reference_temperature_c=reference_temperature_c,
                junction_temperature_c=updated_temperature_c,
                temperature_coefficient_per_c=temperature_coefficient_per_c,
            )

            # Confirm the final temperature/loss pair is self-consistent
            # within the requested tolerance.
            final_thermal_result = estimate_junction_temperature(
                power_loss_w=final_losses["total_loss_w"],
                ambient_temperature_c=ambient_temperature_c,
                thermal_resistance_c_per_w=thermal_resistance_c_per_w,
            )
            final_temperature_c = final_thermal_result["junction_temperature_c"]

            if abs(final_temperature_c - updated_temperature_c) <= tolerance_c:
                return {
                    "converged": True,
                    "iterations": iteration,
                    "junction_temperature_c": float(final_temperature_c),
                    "estimated_resistance_ohm": final_losses[
                        "estimated_resistance_ohm"
                    ],
                    "conduction_loss_w": final_losses["conduction_loss_w"],
                    "switching_loss_w": final_losses["switching_loss_w"],
                    "gate_drive_loss_w": final_losses["gate_drive_loss_w"],
                    "total_loss_w": final_losses["total_loss_w"],
                    "estimated_efficiency_percent": final_losses[
                        "estimated_efficiency_percent"
                    ],
                    "temperature_rise_c": float(
                        final_temperature_c - ambient_temperature_c
                    ),
                    "baseline_total_loss_w": baseline["total_loss_w"],
                }

        temperature_c = updated_temperature_c

    # Return the last calculated state if the iteration limit is reached.
    final_losses = calculate_temperature_dependent_losses(
        parameters=parameters,
        reference_temperature_c=reference_temperature_c,
        junction_temperature_c=temperature_c,
        temperature_coefficient_per_c=temperature_coefficient_per_c,
    )

    return {
        "converged": False,
        "iterations": max_iterations,
        "junction_temperature_c": float(temperature_c),
        "estimated_resistance_ohm": final_losses["estimated_resistance_ohm"],
        "conduction_loss_w": final_losses["conduction_loss_w"],
        "switching_loss_w": final_losses["switching_loss_w"],
        "gate_drive_loss_w": final_losses["gate_drive_loss_w"],
        "total_loss_w": final_losses["total_loss_w"],
        "estimated_efficiency_percent": final_losses[
            "estimated_efficiency_percent"
        ],
        "temperature_rise_c": float(
            temperature_c - ambient_temperature_c
        ),
        "baseline_total_loss_w": baseline["total_loss_w"],
    }
