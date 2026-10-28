
import unittest

from src.gan_simulator.device_profiles import get_device_profile


class TestVerifiedDeviceProfiles(unittest.TestCase):
    def test_gs66508b_is_available(self):
        profile = get_device_profile("gs66508b")
        self.assertEqual(profile.name, "GS66508B (datasheet-based)")
        self.assertEqual(profile.technology, "GaN")

    def test_profile_has_source_and_conditions(self):
        profile = get_device_profile("gs66508b")
        self.assertTrue(profile.is_datasheet_verified)
        self.assertIn("infineon.com", profile.source_url)
        self.assertTrue(profile.test_conditions)

    def test_gs66508b_electrical_values(self):
        profile = get_device_profile("gs66508b")
        self.assertAlmostEqual(profile.rds_on_ohm, 0.050)
        self.assertAlmostEqual(profile.gate_charge_c, 6.1e-9)
        self.assertAlmostEqual(profile.rise_time_s, 3.7e-9)
        self.assertAlmostEqual(profile.fall_time_s, 5.2e-9)
        self.assertAlmostEqual(profile.gate_voltage_v, 6.0)

    def test_example_profiles_remain_unverified(self):
        profile = get_device_profile("example_gan")
        self.assertFalse(profile.is_datasheet_verified)
        self.assertEqual(profile.source_url, "")


if __name__ == "__main__":
    unittest.main()
