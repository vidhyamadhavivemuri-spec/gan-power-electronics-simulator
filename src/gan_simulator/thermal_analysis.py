import math
"""Estimate steady-state transistor junction temperature."""


def estimate_junction_temperature(
    power_loss_w: float,
    ambient_temperature_c: float,
    thermal_resistance_c_per_w: float,
) -> dict[str, float]:
    """Estimate junction temperature using a simple thermal-resistance model.

    Thermal resistance must represent the complete thermal path being modeled.
    This steady-state estimate does not model transient heating or cooling.
    """
    values = {
        "power_loss_w": power_loss_w,
        "ambient_temperature_c": ambient_temperature_c,
        "thermal_resistance_c_per_w": thermal_resistance_c_per_w,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number.")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")

    if power_loss_w < 0:
        raise ValueError("Power loss cannot be negative.")

    if thermal_resistance_c_per_w < 0:
        raise ValueError("Thermal resistance cannot be negative.")

    temperature_rise_c = (
        power_loss_w * thermal_resistance_c_per_w
    )
    junction_temperature_c = (
        ambient_temperature_c + temperature_rise_c
    )

    return {
        "power_loss_w": float(power_loss_w),
        "ambient_temperature_c": float(ambient_temperature_c),
        "thermal_resistance_c_per_w": float(
            thermal_resistance_c_per_w
        ),
        "temperature_rise_c": float(temperature_rise_c),
        "junction_temperature_c": float(junction_temperature_c),
    }
