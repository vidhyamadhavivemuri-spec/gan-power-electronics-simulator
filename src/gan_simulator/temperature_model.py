"""Simple temperature-dependent on-resistance model."""

import math


def estimate_temperature_dependent_resistance(
    reference_resistance_ohm: float,
    reference_temperature_c: float,
    junction_temperature_c: float,
    temperature_coefficient_per_c: float,
) -> dict[str, float]:
    """Estimate on-resistance using a linear temperature model.

    The temperature coefficient is an assumed model parameter,
    not a universal value for GaN transistors.
    """
    values = {
        "reference_resistance_ohm": reference_resistance_ohm,
        "reference_temperature_c": reference_temperature_c,
        "junction_temperature_c": junction_temperature_c,
        "temperature_coefficient_per_c": (
            temperature_coefficient_per_c
        ),
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")

    if reference_resistance_ohm <= 0:
        raise ValueError("Reference resistance must be positive.")

    if temperature_coefficient_per_c < 0:
        raise ValueError(
            "Temperature coefficient cannot be negative in this model."
        )

    resistance_factor = 1.0 + temperature_coefficient_per_c * (
        junction_temperature_c - reference_temperature_c
    )

    if resistance_factor <= 0:
        raise ValueError(
            "The model predicts nonpositive resistance; "
            "check the input temperatures and coefficient."
        )

    estimated_resistance_ohm = (
        reference_resistance_ohm * resistance_factor
    )

    return {
        "reference_resistance_ohm": float(reference_resistance_ohm),
        "reference_temperature_c": float(reference_temperature_c),
        "junction_temperature_c": float(junction_temperature_c),
        "temperature_coefficient_per_c": float(
            temperature_coefficient_per_c
        ),
        "resistance_factor": float(resistance_factor),
        "estimated_resistance_ohm": float(
            estimated_resistance_ohm
        ),
    }
