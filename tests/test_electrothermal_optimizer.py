
import unittest

from src.gan_simulator.electrothermal_optimizer import (
    optimize_electrothermal_frequency,
)
from src.gan_simulator.parameters import SwitchingParameters


class TestElectrothermalOptimizer(unittest.TestCase):
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

    def optimize(self, frequencies, **kwargs):
        defaults = {
            "base_parameters": self.parameters,
            "frequencies_hz": frequencies,
            "ambient_temperature_c": 25.0,
            "thermal_resistance_c_per_w": 2.0,
            "temperature_coefficient_per_c": 0.004,
        }
        defaults.update(kwargs)
        return optimize_electrothermal_frequency(**defaults)

    def test_selects_lowest_loss_feasible_frequency(self):
        result = self.optimize([50_000.0, 100_000.0, 200_000.0])

        self.assertEqual(result["optimal_frequency_hz"], 50_000.0)
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(result["feasible_candidate_count"], 3)

    def test_returns_temperature_and_loss_for_each_candidate(self):
        result = self.optimize([50_000.0, 100_000.0])

        for candidate in result["sweep_results"]:
            self.assertIn("total_loss_w", candidate)
            self.assertIn("junction_temperature_c", candidate)
            self.assertIn("estimated_efficiency_percent", candidate)
            self.assertIn("temperature_feasible", candidate)

    def test_temperature_constraint_rejects_hot_candidates(self):
        result = self.optimize(
            [50_000.0, 100_000.0, 200_000.0],
            max_junction_temperature_c=50.0,
        )

        self.assertLess(
            result["feasible_candidate_count"],
            result["candidate_count"],
        )
        self.assertLessEqual(
            result["estimated_junction_temperature_c"],
            50.0,
        )

    def test_raises_when_no_candidate_is_feasible(self):
        with self.assertRaises(ValueError):
            self.optimize(
                [50_000.0, 100_000.0],
                max_junction_temperature_c=20.0,
            )

    def test_rejects_empty_frequency_list(self):
        with self.assertRaises(ValueError):
            self.optimize([])

    def test_rejects_nonpositive_frequency(self):
        with self.assertRaises(ValueError):
            self.optimize([0.0, 100_000.0])

    def test_rejects_negative_temperature_coefficient(self):
        with self.assertRaises(ValueError):
            self.optimize(
                [50_000.0],
                temperature_coefficient_per_c=-0.004,
            )


if __name__ == "__main__":
    unittest.main()
