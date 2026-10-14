import unittest

from src.gan_simulator.thermal_analysis import (
    estimate_junction_temperature,
)


class TestThermalAnalysis(unittest.TestCase):
    def test_calculates_junction_temperature(self):
        result = estimate_junction_temperature(
            power_loss_w=10.0,
            ambient_temperature_c=25.0,
            thermal_resistance_c_per_w=3.0,
        )

        self.assertAlmostEqual(
            result["temperature_rise_c"], 30.0
        )
        self.assertAlmostEqual(
            result["junction_temperature_c"], 55.0
        )

    def test_zero_power_loss(self):
        result = estimate_junction_temperature(
            power_loss_w=0.0,
            ambient_temperature_c=30.0,
            thermal_resistance_c_per_w=2.0,
        )

        self.assertAlmostEqual(
            result["junction_temperature_c"], 30.0
        )

    def test_rejects_negative_power_loss(self):
        with self.assertRaises(ValueError):
            estimate_junction_temperature(-1.0, 25.0, 2.0)

    def test_rejects_negative_thermal_resistance(self):
        with self.assertRaises(ValueError):
            estimate_junction_temperature(5.0, 25.0, -2.0)

    def test_rejects_nonfinite_values(self):
        with self.assertRaises(ValueError):
            estimate_junction_temperature(float("nan"), 25.0, 2.0)

    def test_returns_expected_fields(self):
        result = estimate_junction_temperature(5.0, 25.0, 2.0)

        expected_fields = {
            "power_loss_w",
            "ambient_temperature_c",
            "thermal_resistance_c_per_w",
            "temperature_rise_c",
            "junction_temperature_c",
        }

        self.assertEqual(set(result.keys()), expected_fields)


if __name__ == "__main__":
    unittest.main()
