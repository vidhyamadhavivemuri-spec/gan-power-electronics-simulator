
import unittest

from src.gan_simulator.full_electrothermal import solve_full_electrothermal
from src.gan_simulator.parameters import SwitchingParameters


class TestFullElectrothermal(unittest.TestCase):
    def setUp(self):
        self.parameters = SwitchingParameters(
            400.0,
            10.0,
            100000.0,
            0.05,
            20e-9,
            20e-9,
            10e-9,
            5.0,
            3000.0,
        )

    def solve(self, **overrides):
        settings = {
            "parameters": self.parameters,
            "ambient_temperature_c": 25.0,
            "thermal_resistance_c_per_w": 2.0,
            "temperature_coefficient_per_c": 0.004,
        }
        settings.update(overrides)
        return solve_full_electrothermal(**settings)

    def test_converges(self):
        result = self.solve()

        self.assertTrue(result["converged"])
        self.assertGreater(result["iterations"], 0)

    def test_includes_all_three_loss_components(self):
        result = self.solve()

        self.assertGreater(result["conduction_loss_w"], 0)
        self.assertGreater(result["switching_loss_w"], 0)
        self.assertGreater(result["gate_drive_loss_w"], 0)

        component_sum = (
            result["conduction_loss_w"]
            + result["switching_loss_w"]
            + result["gate_drive_loss_w"]
        )
        self.assertAlmostEqual(result["total_loss_w"], component_sum)

    def test_temperature_matches_thermal_balance(self):
        result = self.solve()

        expected_temperature = (
            25.0 + result["total_loss_w"] * 2.0
        )
        self.assertAlmostEqual(
            result["junction_temperature_c"],
            expected_temperature,
            delta=0.02,
        )

    def test_zero_thermal_resistance(self):
        result = self.solve(thermal_resistance_c_per_w=0.0)

        self.assertTrue(result["converged"])
        self.assertAlmostEqual(result["junction_temperature_c"], 25.0)

    def test_reports_nonconvergence(self):
        result = self.solve(
            tolerance_c=1e-12,
            max_iterations=1,
        )

        self.assertFalse(result["converged"])
        self.assertEqual(result["iterations"], 1)

    def test_rejects_negative_temperature_coefficient(self):
        with self.assertRaises(ValueError):
            self.solve(temperature_coefficient_per_c=-0.001)

    def test_rejects_negative_thermal_resistance(self):
        with self.assertRaises(ValueError):
            self.solve(thermal_resistance_c_per_w=-1.0)


if __name__ == "__main__":
    unittest.main()
