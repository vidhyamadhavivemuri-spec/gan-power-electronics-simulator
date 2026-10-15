
import unittest

from src.gan_simulator.device_profile_adapter import (
    create_switching_parameters,
)
from src.gan_simulator.device_profiles import get_device_profile
from src.gan_simulator.parameters import SwitchingParameters


class TestDeviceProfileAdapter(unittest.TestCase):
    def test_creates_switching_parameters(self):
        profile = get_device_profile("example_gan")

        parameters = create_switching_parameters(
            profile=profile,
            voltage_v=400.0,
            current_a=10.0,
            frequency_hz=100000.0,
            output_power_w=3000.0,
        )

        self.assertIsInstance(parameters, SwitchingParameters)
        self.assertEqual(parameters.voltage_v, 400.0)
        self.assertEqual(parameters.current_a, 10.0)
        self.assertEqual(parameters.frequency_hz, 100000.0)
        self.assertEqual(parameters.output_power_w, 3000.0)

    def test_uses_device_specific_parameters(self):
        profile = get_device_profile("example_gan")

        parameters = create_switching_parameters(
            profile=profile,
            voltage_v=400.0,
            current_a=10.0,
            frequency_hz=100000.0,
            output_power_w=3000.0,
        )

        self.assertEqual(parameters.rds_on_ohm, profile.rds_on_ohm)
        self.assertEqual(parameters.rise_time_s, profile.rise_time_s)
        self.assertEqual(parameters.fall_time_s, profile.fall_time_s)
        self.assertEqual(parameters.gate_charge_c, profile.gate_charge_c)
        self.assertEqual(parameters.gate_voltage_v, profile.gate_voltage_v)


if __name__ == "__main__":
    unittest.main()
