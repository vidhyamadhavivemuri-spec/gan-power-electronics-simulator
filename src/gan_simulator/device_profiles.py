
"""Illustrative semiconductor device profiles for simulation.

The values in this module are examples for software testing and learning.
They are not verified specifications for real commercial devices.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceProfile:
    """Electrical parameters used by the simplified loss model."""

    name: str
    technology: str
    rds_on_ohm: float
    rise_time_s: float
    fall_time_s: float
    gate_charge_c: float
    gate_voltage_v: float
    data_source: str = "Illustrative example; not a verified datasheet"


_DEVICE_PROFILES = {
    "example_gan": DeviceProfile(
        name="Example GaN Transistor",
        technology="GaN",
        rds_on_ohm=0.050,
        rise_time_s=20e-9,
        fall_time_s=20e-9,
        gate_charge_c=10e-9,
        gate_voltage_v=5.0,
    ),
    "example_silicon": DeviceProfile(
        name="Example Silicon MOSFET",
        technology="Silicon MOSFET",
        rds_on_ohm=0.080,
        rise_time_s=35e-9,
        fall_time_s=35e-9,
        gate_charge_c=25e-9,
        gate_voltage_v=10.0,
    ),
}


def list_device_profiles() -> list[DeviceProfile]:
    """Return all available example device profiles."""
    return list(_DEVICE_PROFILES.values())


def get_device_profile(profile_id: str) -> DeviceProfile:
    """Return a profile by ID, rejecting unknown IDs."""
    if not isinstance(profile_id, str):
        raise ValueError("Profile ID must be a string.")

    try:
        return _DEVICE_PROFILES[profile_id]
    except KeyError:
        raise ValueError(
            f"Unknown device profile: {profile_id}"
        ) from None
