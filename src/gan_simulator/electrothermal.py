"""Iterative electrothermal estimation for a power transistor."""

import math

from .temperature_model import (
    estimate_temperature_dependent_resistance,
)


def solve_electrothermal(
    current_a: float,
    reference_resistance_ohm: float,
    reference_temperature_c: float,
    ambient_temperature_c: float,
    thermal_resistance_c_per_w: float,
    temperature_coefficient_per_c: float,
    initial_temperature_c: float | None = None,
    tolerance_c: float = 0.01,
    max_iterations: int = 1000,
) -> dict[str, float | int | bool]:
    """Iterate conduction loss and junction temperature to convergence.

    This simplified model includes conduction loss only. It assumes
    constant current and a linear temperature-dependent resistance.
    """
    values = {
        "current_a": current_a,
        "reference_resistance_ohm": reference_resistance_ohm,
        "reference_temperature_c": reference_temperature_c,
        "ambient_temperature_c": ambient_temperature_c,
        "thermal_resistance_c_per_w": thermal_resistance_c_per_w,
        "temperature_coefficient_per_c": temperature_coefficient_per_c,
        "tolerance_c": tolerance_c,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")

    if current_a < 0:
        raise ValueError("Current cannot be negative.")
    if reference_resistance_ohm <= 0:
        raise ValueError("Reference resistance must be positive.")
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
        temperature_c = ambient_temperature_c
    else:
        if (
            isinstance(initial_temperature_c, bool)
            or not isinstance(initial_temperature_c, (int, float))
            or not math.isfinite(initial_temperature_c)
        ):
            raise ValueError("Initial temperature must be a finite number.")
        temperature_c = float(initial_temperature_c)

    for iteration in range(1, max_iterations + 1):
        resistance_result = estimate_temperature_dependent_resistance(
            reference_resistance_ohm=reference_resistance_ohm,
            reference_temperature_c=reference_temperature_c,
            junction_temperature_c=temperature_c,
            temperature_coefficient_per_c=temperature_coefficient_per_c,
        )

        resistance_ohm = resistance_result["estimated_resistance_ohm"]
        conduction_loss_w = current_a**2 * resistance_ohm

        updated_temperature_c = (
            ambient_temperature_c
            + conduction_loss_w * thermal_resistance_c_per_w
        )

        if not math.isfinite(updated_temperature_c):
            raise ValueError("Temperature estimate became nonfinite.")

        if abs(updated_temperature_c - temperature_c) <= tolerance_c:
            return {
                "converged": True,
                "iterations": iteration,
                "junction_temperature_c": float(updated_temperature_c),
                "estimated_resistance_ohm": float(resistance_ohm),
                "conduction_loss_w": float(conduction_loss_w),
                "temperature_rise_c": float(
                    updated_temperature_c - ambient_temperature_c
                ),
            }

        temperature_c = updated_temperature_c

    return {
        "converged": False,
        "iterations": max_iterations,
        "junction_temperature_c": float(temperature_c),
        "estimated_resistance_ohm": float(resistance_ohm),
        "conduction_loss_w": float(conduction_loss_w),
        "temperature_rise_c": float(
            temperature_c - ambient_temperature_c
        ),
    }
