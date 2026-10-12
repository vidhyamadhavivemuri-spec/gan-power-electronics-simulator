import unittest

from src.gan_simulator.device_comparison import compare_devices
from src.gan_simulator.parameters import SwitchingParameters


class TestDeviceComparison(unittest.TestCase):
    def setUp(self):
        self.gan = SwitchingParameters(
            voltage_v=400,
            current_a=10,
            frequency_hz=100_000,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=10e-9,
            gate_voltage_v=5,
            output_power_w=500,
        )

        self.silicon = SwitchingParameters(
            voltage_v=400,
            current_a=10,
            frequency_hz=100_000,
            rds_on_ohm=0.08,
            rise_time_s=50e-9,
            fall_time_s=50e-9,
            gate_charge_c=30e-9,
            gate_voltage_v=10,
            output_power_w=500,
        )

    def test_returns_both_devices(self):
        results = compare_devices(self.gan, self.silicon)
        self.assertIn("GaN", results)
        self.assertIn("Silicon", results)

    def test_returns_expected_loss_fields(self):
        results = compare_devices(self.gan, self.silicon)

        for device in ("GaN", "Silicon"):
            self.assertIn("conduction_loss_w", results[device])
            self.assertIn("switching_loss_w", results[device])
            self.assertIn("total_loss_w", results[device])
            self.assertIn(
                "estimated_efficiency_percent", results[device]
            )

    def test_assumed_gan_parameters_have_lower_modeled_loss(self):
        results = compare_devices(self.gan, self.silicon)

        self.assertLess(
            results["GaN"]["total_loss_w"],
            results["Silicon"]["total_loss_w"],
        )


if __name__ == "__main__":
    unittest.main()
