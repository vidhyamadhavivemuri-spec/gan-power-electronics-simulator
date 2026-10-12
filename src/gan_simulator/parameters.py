from dataclasses import dataclass


@dataclass(frozen=True)
class SwitchingParameters:
    """Operating and device parameters for a switching transistor."""

    voltage_v: float
    current_a: float
    frequency_hz: float
    rds_on_ohm: float
    rise_time_s: float
    fall_time_s: float
    gate_charge_c: float
    gate_voltage_v: float
    output_power_w: float