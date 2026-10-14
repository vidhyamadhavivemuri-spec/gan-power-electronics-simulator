import unittest

from src.gan_simulator.temperature_model import (
    estimate_temperature_dependent_resistance,
)


class TestTemperatureModel(unittest.TestCase):
    def test_resistance_increases_with_temperature(self):
        result = estimate_temperature_dependent_resistance(
            reference_resistance_ohm=0.05,
            reference_temperature_c=25.0,
            junction_temperature_c=75.0,
            temperature_coefficient_per_c=0.004,
        )

        self.assertAlmostEqual(
            result["estimated_resistance_ohm"], 0.06
        )

    def test_resistance_at_reference_temperature(self):
        result = estimate_temperature_dependent_resistance(
            0.05, 25.0, 25.0, 0.004
        )

        self.assertAlmostEqual(
            result["estimated_resistance_ohm"], 0.05
        )

    def test_zero_temperature_coefficient(self):
        result = estimate_temperature_dependent_resistance(
            0.05, 25.0, 100.0, 0.0
        )

        self.assertAlmostEqual(
            result["estimated_resistance_ohm"], 0.05
        )

    def test_rejects_nonpositive_reference_resistance(self):
        with self.assertRaises(ValueError):
            estimate_temperature_dependent_resistance(
                0.0, 25.0, 75.0, 0.004
            )

    def test_rejects_negative_temperature_coefficient(self):
        with self.assertRaises(ValueError):
            estimate_temperature_dependent_resistance(
                0.05, 25.0, 75.0, -0.004
            )

    def test_rejects_nonfinite_values(self):
        with self.assertRaises(ValueError):
            estimate_temperature_dependent_resistance(
                0.05, 25.0, float("nan"), 0.004
            )

    def test_returns_expected_fields(self):
        result = estimate_temperature_dependent_resistance(
            0.05, 25.0, 75.0, 0.004
        )

        expected_fields = {
            "reference_resistance_ohm",
            "reference_temperature_c",
            "junction_temperature_c",
            "temperature_coefficient_per_c",
            "resistance_factor",
            "estimated_resistance_ohm",
        }

        self.assertEqual(set(result.keys()), expected_fields)


if __name__ == "__main__":
    unittest.main()
