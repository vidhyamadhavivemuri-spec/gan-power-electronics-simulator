import unittest

import numpy as np

from src.gan_simulator.waveforms import generate_switching_waveforms


class TestWaveforms(unittest.TestCase):

    def test_waveform_arrays_have_expected_size(self):
        result = generate_switching_waveforms(
            400, 10, 100_000, 20e-9, 20e-9, 1000
        )
        self.assertEqual(len(result["time_s"]), 1000)
        self.assertEqual(len(result["voltage_v"]), 1000)
        self.assertEqual(len(result["current_a"]), 1000)

    def test_waveforms_stay_within_bounds(self):
        result = generate_switching_waveforms(
            400, 10, 100_000, 20e-9, 20e-9
        )
        self.assertTrue(np.all(result["voltage_v"] >= 0))
        self.assertTrue(np.all(result["voltage_v"] <= 400))
        self.assertTrue(np.all(result["current_a"] >= 0))
        self.assertTrue(np.all(result["current_a"] <= 10))

    def test_invalid_frequency_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_switching_waveforms(
                400, 10, 0, 20e-9, 20e-9
            )

    def test_transition_times_must_fit_period(self):
        with self.assertRaises(ValueError):
            generate_switching_waveforms(
                400, 10, 100_000, 6e-6, 6e-6
            )


if __name__ == "__main__":
    unittest.main()
