
import unittest

from src.gan_simulator.device_profiles import (
    get_device_profile,
    list_device_profiles,
)


class TestDeviceProfiles(unittest.TestCase):
    def test_lists_available_profiles(self):
        profiles = list_device_profiles()
        self.assertGreaterEqual(len(profiles), 2)

    def test_gan_profile(self):
        profile = get_device_profile("example_gan")
        self.assertEqual(profile.technology, "GaN")
        self.assertGreater(profile.rds_on_ohm, 0)
        self.assertGreater(profile.gate_charge_c, 0)

    def test_silicon_profile(self):
        profile = get_device_profile("example_silicon")
        self.assertEqual(profile.technology, "Silicon MOSFET")
        self.assertGreater(profile.rds_on_ohm, 0)

    def test_unknown_profile_is_rejected(self):
        with self.assertRaises(ValueError):
            get_device_profile("unknown_device")

    def test_profile_is_immutable(self):
        profile = get_device_profile("example_gan")
        with self.assertRaises(AttributeError):
            profile.name = "Changed name"


if __name__ == "__main__":
    unittest.main()
