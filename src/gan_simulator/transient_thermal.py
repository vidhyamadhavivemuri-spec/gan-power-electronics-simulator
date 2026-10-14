"""First-order transient thermal model for a power transistor."""

import math


def simulate_transient_temperature(
    time_s: list[float],
    ambient_temperature_c: float,
    power_step_w: float,
    thermal_resistance_c_per_w: float,
    thermal_capacitance_j_per_c: float,
    initial_temperature_c: float | None = None,
) -> dict[str, list[float] | float]:
    """Calculate junction temperature after a constant power step.

    Uses a first-order thermal RC model. A positive power step heats
    the device; a negative power step models a reduction in power.

    This simplified model assumes constant thermal properties.
    """
    values = {
        "ambient_temperature_c": ambient_temperature_c,
        "power_step_w": power_step_w,
        "thermal_resistance_c_per_w": thermal_resistance_c_per_w,
        "thermal_capacitance_j_per_c": thermal_capacitance_j_per_c,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")

    if thermal_resistance_c_per_w <= 0:
        raise ValueError("Thermal resistance must be positive.")

    if thermal_capacitance_j_per_c <= 0:
        raise ValueError("Thermal capacitance must be positive.")

    if not isinstance(time_s, list) or not time_s:
        raise ValueError("time_s must be a non-empty list.")

    for time in time_s:
        if (
            isinstance(time, bool)
            or not isinstance(time, (int, float))
            or not math.isfinite(time)
            or time < 0
        ):
            raise ValueError("Every time value must be finite and nonnegative.")

    if any(time_s[i] > time_s[i + 1] for i in range(len(time_s) - 1)):
        raise ValueError("time_s must be in nondecreasing order.")

    if initial_temperature_c is None:
        initial_temperature_c = ambient_temperature_c

    if (
        isinstance(initial_temperature_c, bool)
        or not isinstance(initial_temperature_c, (int, float))
        or not math.isfinite(initial_temperature_c)
    ):
        raise ValueError("Initial temperature must be a finite number.")

    time_constant_s = (
        thermal_resistance_c_per_w * thermal_capacitance_j_per_c
    )

    temperatures = [
        initial_temperature_c
        + power_step_w
        * thermal_resistance_c_per_w
        * (1.0 - math.exp(-time / time_constant_s))
        for time in time_s
    ]

    return {
        "time_s": [float(time) for time in time_s],
        "junction_temperature_c": temperatures,
        "time_constant_s": time_constant_s,
        "steady_state_temperature_c": (
            initial_temperature_c
            + power_step_w * thermal_resistance_c_per_w
        ),
    }
