
"""Semiconductor device profiles for educational simulation.

Profiles explicitly distinguish illustrative examples from datasheet-backed
parameters. Datasheet values are valid only under their stated conditions.
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
    source_url: str = ""
    test_conditions: str = ""
    is_datasheet_verified: bool = False


_GS66508B_DATASHEET = (
    "Infineon/GaN Systems GS66508B datasheet, "
    "https://www.infineon.com/dgdl/Infineon-GS66508B-"
    "DataSheet-v01_00-EN.pdf?fileId=8ac78c8c8d2fe47b018e5161c92653de"
)

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
    "gs66508b": DeviceProfile(
        name="GS66508B (datasheet-based)",
        technology="GaN",
        rds_on_ohm=0.050,
        rise_time_s=3.7e-9,
        fall_time_s=5.2e-9,
        gate_charge_c=6.1e-9,
        gate_voltage_v=6.0,
        data_source=_GS66508B_DATASHEET,
        source_url=_GS66508B_DATASHEET.split(", ", 1)[1],
        test_conditions=(
            "RDS(on): typical 50 mΩ at TJ=25 °C, VGS=6 V, ID=9 A. "
            "Gate charge: 6.1 nC under the datasheet's stated gate-charge "
            "test conditions. Rise/fall times: 3.7/5.2 ns under the "
            "specified 400 V, 16 A, 6 V gate-drive, 5 Ω external "
            "gate-resistance switching test."
        ),
        is_datasheet_verified=True,
    ),
}


def list_device_profiles() -> list[DeviceProfile]:
    """Return all available device profiles."""
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
