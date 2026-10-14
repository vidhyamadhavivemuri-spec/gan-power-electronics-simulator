import math
import unittest

from src.gan_simulator.transient_thermal import (
    simulate_transient_temperature,
)


class TestTransientThermal(unittest.TestCase):
    def test_heating_starts_at_initial_temperature(self):
        result = simulate_transient_temperature(
            time_s=[0.0, 1.0],
            ambient_temperature_c=25.0,
            power_step_w=10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
        )

        self.assertAlmostEqual(
            result["junction_temperature_c"][0], 25.0
        )

    def test_heating_approaches_steady_state(self):
        result = simulate_transient_temperature(
            time_s=[0.0, 1000.0],
            ambient_temperature_c=25.0,
            power_step_w=10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
        )

        self.assertAlmostEqual(
            result["junction_temperature_c"][-1],
            45.0,
            places=2,
        )

    def test_temperature_rises_during_heating(self):
        result = simulate_transient_temperature(
            time_s=[0.0, 5.0, 10.0],
            ambient_temperature_c=25.0,
            power_step_w=10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
        )

        temperatures = result["junction_temperature_c"]
        self.assertLess(temperatures[0], temperatures[1])
        self.assertLess(temperatures[1], temperatures[2])

    def test_negative_power_step_models_cooling(self):
        result = simulate_transient_temperature(
            time_s=[0.0, 5.0, 10.0],
            ambient_temperature_c=25.0,
            power_step_w=-10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
            initial_temperature_c=45.0,
        )

        temperatures = result["junction_temperature_c"]
        self.assertAlmostEqual(temperatures[0], 45.0)
        self.assertGreater(temperatures[0], temperatures[1])
        self.assertGreater(temperatures[1], temperatures[2])

    def test_time_constant(self):
        result = simulate_transient_temperature(
            time_s=[0.0],
            ambient_temperature_c=25.0,
            power_step_w=10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
        )

        self.assertAlmostEqual(result["time_constant_s"], 10.0)

    def test_custom_initial_temperature(self):
        result = simulate_transient_temperature(
            time_s=[0.0],
            ambient_temperature_c=25.0,
            power_step_w=10.0,
            thermal_resistance_c_per_w=2.0,
            thermal_capacitance_j_per_c=5.0,
            initial_temperature_c=30.0,
        )

        self.assertAlmostEqual(
            result["junction_temperature_c"][0], 30.0
        )
        self.assertAlmostEqual(
            result["steady_state_temperature_c"], 50.0
        )

    def test_rejects_empty_time_list(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [], 25.0, 10.0, 2.0, 5.0
            )

    def test_rejects_negative_time(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [-1.0, 0.0], 25.0, 10.0, 2.0, 5.0
            )

    def test_rejects_unsorted_time_values(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [0.0, 2.0, 1.0], 25.0, 10.0, 2.0, 5.0
            )

    def test_rejects_zero_thermal_resistance(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [0.0], 25.0, 10.0, 0.0, 5.0
            )

    def test_rejects_zero_thermal_capacitance(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [0.0], 25.0, 10.0, 2.0, 0.0
            )

    def test_rejects_nonfinite_power(self):
        with self.assertRaises(ValueError):
            simulate_transient_temperature(
                [0.0], 25.0, math.inf, 2.0, 5.0
            )


if __name__ == "__main__":
    unittest.main()