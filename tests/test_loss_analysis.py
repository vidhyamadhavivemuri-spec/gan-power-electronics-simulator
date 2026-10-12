import unittest

from src.gan_simulator.loss_analysis import analyze_loss_breakdown


class TestLossAnalysis(unittest.TestCase):
    def test_identifies_switching_as_dominant(self):
        result = analyze_loss_breakdown({
            "conduction_loss_w": 5.0,
            "switching_loss_w": 8.0,
            "gate_drive_loss_w": 0.005,
        })

        self.assertEqual(result["dominant_component"], "Switching")
        self.assertAlmostEqual(result["dominant_percentage"], 8 / 13.005 * 100)

    def test_zero_losses(self):
        result = analyze_loss_breakdown({
            "conduction_loss_w": 0.0,
            "switching_loss_w": 0.0,
            "gate_drive_loss_w": 0.0,
        })

        self.assertEqual(result["dominant_component"], "None")
        self.assertEqual(result["dominant_percentage"], 0.0)

    def test_negative_loss_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_loss_breakdown({
                "conduction_loss_w": -1.0,
                "switching_loss_w": 2.0,
                "gate_drive_loss_w": 0.0,
            })


if __name__ == "__main__":
    unittest.main()
