
import unittest

from src.gan_simulator.loss_model import calculate_losses
from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.temperature_dependent_losses import (
    calculate_temperature_dependent_losses,
)


class TestTemperatureDependentLosses(unittest.TestCase):
    def setUp(self):
        self.parameters = SwitchingParameters(
            400,       # voltage_v
            10,        # current_a
            100000,    # frequency_hz
            0.05,      # rds_on_ohm
            20e-9,     # rise_time_s
            20e-9,     # fall_time_s
            10e-9,     # gate_charge_c
            5,         # gate_voltage_v
            500,       # output_power_w
        )

    def test_reference_temperature_matches_original_losses(self):
        original = calculate_losses(self.parameters)

        result = calculate_temperature_dependent_losses(
            self.parameters, 25.0, 25.0, 0.004
        )

        self.assertAlmostEqual(
            result["conduction_loss_w"],
            original["conduction_loss_w"],
        )
        self.assertAlmostEqual(
            result["total_loss_w"],
            original["total_loss_w"],
        )
        self.assertAlmostEqual(
            result["estimated_efficiency_percent"],
            original["estimated_efficiency_percent"],
        )

    def test_higher_temperature_increases_conduction_loss(self):
        result = calculate_temperature_dependent_losses(
            self.parameters, 25.0, 100.0, 0.004
        )
        original = calculate_losses(self.parameters)

        self.assertGreater(
            result["conduction_loss_w"],
            original["conduction_loss_w"],
        )
        self.assertGreater(
            result["total_loss_w"],
            original["total_loss_w"],
        )

    def test_switching_and_gate_drive_losses_remain_unchanged(self):
        original = calculate_losses(self.parameters)

        result = calculate_temperature_dependent_losses(
            self.parameters, 25.0, 100.0, 0.004
        )

        self.assertAlmostEqual(
            result["switching_loss_w"],
            original["switching_loss_w"],
        )
        self.assertAlmostEqual(
            result["gate_drive_loss_w"],
            original["gate_drive_loss_w"],
        )

    def test_zero_temperature_coefficient_preserves_losses(self):
        original = calculate_losses(self.parameters)

        result = calculate_temperature_dependent_losses(
            self.parameters, 25.0, 150.0, 0.0
        )

        self.assertAlmostEqual(
            result["total_loss_w"],
            original["total_loss_w"],
        )

    def test_negative_temperature_coefficient_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_temperature_dependent_losses(
                self.parameters, 25.0, 100.0, -0.004
            )

    def test_non_finite_temperature_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_temperature_dependent_losses(
                self.parameters, 25.0, float("nan"), 0.004
            )


if __name__ == "__main__":
    unittest.main()
