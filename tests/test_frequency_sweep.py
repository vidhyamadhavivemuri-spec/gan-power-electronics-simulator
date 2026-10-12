import unittest

from src.gan_simulator.frequency_sweep import analyze_frequency_sweep
from src.gan_simulator.parameters import SwitchingParameters


class TestFrequencySweep(unittest.TestCase):
    def setUp(self):
        self.parameters = SwitchingParameters(
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

    def test_returns_one_result_per_frequency(self):
        results = analyze_frequency_sweep(
            self.parameters, [50_000, 100_000, 200_000]
        )
        self.assertEqual(len(results), 3)

    def test_switching_loss_increases_with_frequency(self):
        results = analyze_frequency_sweep(
            self.parameters, [50_000, 100_000, 200_000]
        )
        losses = [result["switching_loss_w"] for result in results]
        self.assertLess(losses[0], losses[1])
        self.assertLess(losses[1], losses[2])

    def test_empty_frequency_list_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_frequency_sweep(self.parameters, [])

    def test_nonpositive_frequency_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_frequency_sweep(self.parameters, [100_000, 0])


if __name__ == "__main__":
    unittest.main()
