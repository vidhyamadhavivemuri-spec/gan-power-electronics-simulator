import unittest

from src.gan_simulator.electrothermal import solve_electrothermal


class TestElectrothermal(unittest.TestCase):
    def test_converges_to_expected_temperature(self):
        result = solve_electrothermal(
            current_a=10.0,
            reference_resistance_ohm=0.05,
            reference_temperature_c=25.0,
            ambient_temperature_c=25.0,
            thermal_resistance_c_per_w=2.0,
            temperature_coefficient_per_c=0.004,
        )

        self.assertTrue(result["converged"])
        self.assertAlmostEqual(
            result["junction_temperature_c"], 34.0 / 0.96, places=2
        )

    def test_zero_current_gives_ambient_temperature(self):
        result = solve_electrothermal(
            current_a=0.0,
            reference_resistance_ohm=0.05,
            reference_temperature_c=25.0,
            ambient_temperature_c=30.0,
            thermal_resistance_c_per_w=2.0,
            temperature_coefficient_per_c=0.004,
        )

        self.assertTrue(result["converged"])
        self.assertAlmostEqual(
            result["junction_temperature_c"], 30.0
        )
        self.assertAlmostEqual(result["conduction_loss_w"], 0.0)

    def test_returns_expected_fields(self):
        result = solve_electrothermal(
            current_a=10.0,
            reference_resistance_ohm=0.05,
            reference_temperature_c=25.0,
            ambient_temperature_c=25.0,
            thermal_resistance_c_per_w=2.0,
            temperature_coefficient_per_c=0.004,
        )

        expected_fields = {
            "converged",
            "iterations",
            "junction_temperature_c",
            "estimated_resistance_ohm",
            "conduction_loss_w",
            "temperature_rise_c",
        }

        self.assertEqual(set(result.keys()), expected_fields)

    def test_rejects_negative_current(self):
        with self.assertRaises(ValueError):
            solve_electrothermal(-1.0, 0.05, 25.0, 25.0, 2.0, 0.004)

    def test_rejects_zero_reference_resistance(self):
        with self.assertRaises(ValueError):
            solve_electrothermal(10.0, 0.0, 25.0, 25.0, 2.0, 0.004)

    def test_rejects_negative_thermal_resistance(self):
        with self.assertRaises(ValueError):
            solve_electrothermal(10.0, 0.05, 25.0, 25.0, -2.0, 0.004)

    def test_rejects_nonpositive_tolerance(self):
        with self.assertRaises(ValueError):
            solve_electrothermal(
                10.0, 0.05, 25.0, 25.0, 2.0, 0.004,
                tolerance_c=0.0,
            )

    def test_reports_nonconvergence(self):
        result = solve_electrothermal(
            current_a=10.0,
            reference_resistance_ohm=0.05,
            reference_temperature_c=25.0,
            ambient_temperature_c=25.0,
            thermal_resistance_c_per_w=2.0,
            temperature_coefficient_per_c=0.004,
            tolerance_c=1e-12,
            max_iterations=1,
        )

        self.assertFalse(result["converged"])
        self.assertEqual(result["iterations"], 1)


if __name__ == "__main__":
    unittest.main()
