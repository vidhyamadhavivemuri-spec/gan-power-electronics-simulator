import unittest

from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.loss_model import calculate_losses


class TestLossModel(unittest.TestCase):

    def setUp(self):
        self.params = SwitchingParameters(
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

    def test_conduction_loss(self):
        result = calculate_losses(self.params)
        self.assertAlmostEqual(result["conduction_loss_w"], 5.0)

    def test_switching_loss(self):
        result = calculate_losses(self.params)
        self.assertAlmostEqual(result["switching_loss_w"], 8.0)

    def test_gate_drive_loss(self):
        result = calculate_losses(self.params)
        self.assertAlmostEqual(result["gate_drive_loss_w"], 0.005)

    def test_total_loss(self):
        result = calculate_losses(self.params)
        self.assertAlmostEqual(result["total_loss_w"], 13.005)

    def test_efficiency(self):
        result = calculate_losses(self.params)
        self.assertAlmostEqual(
            result["estimated_efficiency_percent"],
            100 * 500 / (500 + 13.005),
        )

    def test_zero_current(self):
        params = SwitchingParameters(
            voltage_v=400,
            current_a=0,
            frequency_hz=100_000,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=10e-9,
            gate_voltage_v=5,
            output_power_w=500,
        )
        result = calculate_losses(params)
        self.assertAlmostEqual(result["conduction_loss_w"], 0.0)
        self.assertAlmostEqual(result["switching_loss_w"], 0.0)

    def test_negative_voltage_is_rejected(self):
        params = SwitchingParameters(
            voltage_v=-400,
            current_a=10,
            frequency_hz=100_000,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=10e-9,
            gate_voltage_v=5,
            output_power_w=500,
        )
        with self.assertRaises(ValueError):
            calculate_losses(params)

    def test_zero_output_power_is_rejected(self):
        params = SwitchingParameters(
            voltage_v=400,
            current_a=10,
            frequency_hz=100_000,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=10e-9,
            gate_voltage_v=5,
            output_power_w=0,
        )
        with self.assertRaises(ValueError):
            calculate_losses(params)


if __name__ == "__main__":
    unittest.main()
