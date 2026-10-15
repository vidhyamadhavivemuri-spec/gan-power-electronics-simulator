import unittest

from src.gan_simulator.parameters import SwitchingParameters
from src.gan_simulator.frequency_thermal_analysis import (
    analyze_frequency_thermal_behavior,
)


class TestFrequencyThermalAnalysis(unittest.TestCase):

    def setUp(self):
        self.parameters = SwitchingParameters(
            voltage_v=400,
            current_a=10,
            frequency_hz=100_000,
            rds_on_ohm=0.05,
            rise_time_s=20e-9,
            fall_time_s=20e-9,
            gate_charge_c=20e-9,
            gate_voltage_v=5,
            output_power_w=1000,
        )

    def test_returns_one_result_per_frequency(self):
        results = analyze_frequency_thermal_behavior(
            self.parameters,
            [50_000, 100_000, 200_000],
            ambient_temperature_c=25,
            thermal_resistance_c_per_w=2,
        )
        self.assertEqual(len(results), 3)

    def test_temperature_increases_with_frequency(self):
        results = analyze_frequency_thermal_behavior(
            self.parameters,
            [50_000, 100_000, 200_000],
            ambient_temperature_c=25,
            thermal_resistance_c_per_w=2,
        )
        temperatures = [
            result["junction_temperature_c"] for result in results
        ]
        self.assertEqual(temperatures, sorted(temperatures))
        self.assertLess(temperatures[0], temperatures[-1])

    def test_returns_expected_fields(self):
        results = analyze_frequency_thermal_behavior(
            self.parameters,
            [100_000],
            ambient_temperature_c=25,
            thermal_resistance_c_per_w=2,
        )
        expected_fields = {
            "frequency_hz",
            "total_loss_w",
            "estimated_efficiency_percent",
            "temperature_rise_c",
            "junction_temperature_c",
        }
        self.assertEqual(set(results[0].keys()), expected_fields)

    def test_junction_temperature_matches_thermal_model(self):
        results = analyze_frequency_thermal_behavior(
            self.parameters,
            [100_000],
            ambient_temperature_c=25,
            thermal_resistance_c_per_w=2,
        )
        result = results[0]
        self.assertAlmostEqual(
            result["junction_temperature_c"],
            25 + result["total_loss_w"] * 2,
        )


if __name__ == "__main__":
    unittest.main()
