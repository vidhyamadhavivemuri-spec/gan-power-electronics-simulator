import unittest

from src.gan_simulator.frequency_optimizer import optimize_switching_frequency
from src.gan_simulator.parameters import SwitchingParameters


class TestFrequencyOptimizer(unittest.TestCase):
    def setUp(self):
        self.parameters = SwitchingParameters(
            voltage_v=400.0,
            current_a=10.0,
            frequency_hz=100_000.0,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=10e-9,
            gate_voltage_v=5.0,
            output_power_w=3000.0,
        )

    def test_selects_frequency_with_lowest_total_loss(self):
        frequencies = [50_000.0, 100_000.0, 200_000.0]

        result = optimize_switching_frequency(self.parameters, frequencies)

        self.assertEqual(result["optimal_frequency_hz"], 50_000.0)
        self.assertEqual(result["candidate_count"], 3)

    def test_returns_all_sweep_results(self):
        frequencies = [50_000.0, 100_000.0]

        result = optimize_switching_frequency(self.parameters, frequencies)

        self.assertEqual(len(result["sweep_results"]), 2)
        self.assertIn("minimum_total_loss_w", result)
        self.assertIn("estimated_efficiency_percent", result)

    def test_rejects_empty_frequency_list(self):
        with self.assertRaises(ValueError):
            optimize_switching_frequency(self.parameters, [])

    def test_rejects_nonpositive_frequency(self):
        with self.assertRaises(ValueError):
            optimize_switching_frequency(self.parameters, [0.0, 100_000.0])


if __name__ == "__main__":
    unittest.main()
