
"""Convert a device profile into simulation parameters."""

from src.gan_simulator.device_profiles import DeviceProfile
from src.gan_simulator.parameters import SwitchingParameters


def create_switching_parameters(
    profile: DeviceProfile,
    voltage_v: float,
    current_a: float,
    frequency_hz: float,
    output_power_w: float,
) -> SwitchingParameters:
    """Combine device characteristics with operating conditions."""

    return SwitchingParameters(
        voltage_v=voltage_v,
        current_a=current_a,
        frequency_hz=frequency_hz,
        rds_on_ohm=profile.rds_on_ohm,
        rise_time_s=profile.rise_time_s,
        fall_time_s=profile.fall_time_s,
        gate_charge_c=profile.gate_charge_c,
        gate_voltage_v=profile.gate_voltage_v,
        output_power_w=output_power_w,
    )
