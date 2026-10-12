from math import isfinite

from .parameters import SwitchingParameters


def calculate_losses(p: SwitchingParameters) -> dict[str, float]:
    """Calculate simplified transistor losses and estimated efficiency."""

    values = (
        p.voltage_v,
        p.current_a,
        p.frequency_hz,
        p.rds_on_ohm,
        p.rise_time_s,
        p.fall_time_s,
        p.gate_charge_c,
        p.gate_voltage_v,
        p.output_power_w,
    )

    if not all(isfinite(v) for v in values):
        raise ValueError("All parameters must be finite numbers.")

    if any(v < 0 for v in values):
        raise ValueError("Parameters cannot be negative.")

    if p.output_power_w <= 0:
        raise ValueError("Output power must be greater than zero.")

    conduction = p.current_a**2 * p.rds_on_ohm

    switching = (
        0.5
        * p.voltage_v
        * p.current_a
        * (p.rise_time_s + p.fall_time_s)
        * p.frequency_hz
    )

    gate_drive = (
        p.gate_charge_c
        * p.gate_voltage_v
        * p.frequency_hz
    )

    total = conduction + switching + gate_drive
    efficiency = 100 * p.output_power_w / (p.output_power_w + total)

    return {
        "conduction_loss_w": conduction,
        "switching_loss_w": switching,
        "gate_drive_loss_w": gate_drive,
        "total_loss_w": total,
        "estimated_efficiency_percent": efficiency,
    }
