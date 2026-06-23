import unittest

from ml.digital_twin import create_digital_twin_profile
from simulator.carbon_simulator import simulate_future_impact, calculate_sustainability_score


class TestEcoTwinAI(unittest.TestCase):
    def test_future_forecast_generation_3_months(self):
        forecast = simulate_future_impact(420.0, 55.0, 3)
        self.assertEqual(forecast["months"], 3)
        self.assertIsInstance(forecast["projected_footprint"], float)
        self.assertGreater(forecast["projected_footprint"], 0)

    def test_sustainability_score_projection(self):
        projected = simulate_future_impact(420.0, 55.0, 12)
        self.assertIn("projected_score", projected)
        self.assertIsInstance(projected["projected_score"], int)
        self.assertGreaterEqual(projected["projected_score"], 0)
        self.assertLessEqual(projected["projected_score"], 100)

    def test_reduction_potential_calculation(self):
        forecast = simulate_future_impact(420.0, 55.0, 12)
        self.assertAlmostEqual(forecast["reduction_potential"], 420.0 - forecast["projected_footprint"], places=2)

    def test_savings_estimation(self):
        forecast = simulate_future_impact(420.0, 55.0, 12)
        self.assertAlmostEqual(forecast["estimated_savings"], round(forecast["reduction_potential"] * 0.08, 2), places=2)

    def test_digital_twin_report_generation(self):
        profile = {
            "age": 35,
            "family_size": 4,
            "monthly_electricity_usage": 2200,
            "monthly_water_consumption": 5200,
            "daily_travel_distance": 22,
            "monthly_waste_generated": 18,
        }
        report = create_digital_twin_profile(
            user_profile=profile,
            carbon_footprint=420.0,
            sustainability_score=55.0,
            city="Hyderabad",
        )

        self.assertIsInstance(report, dict)
        self.assertIn("current_state", report)
        self.assertIn("future_predictions", report)
        self.assertIn("recommendations", report)
        self.assertIn("location_insights", report)

        current_state = report["current_state"]
        self.assertEqual(current_state["city"], "Hyderabad")
        self.assertEqual(current_state["carbon_footprint"], 420.0)
        self.assertEqual(current_state["sustainability_score"], 55)

        future_predictions = report["future_predictions"]
        self.assertIn("3_months", future_predictions)
        self.assertIn("6_months", future_predictions)
        self.assertIn("12_months", future_predictions)
        self.assertGreater(len(report["recommendations"]), 0)
        self.assertGreater(len(report["location_insights"]), 0)


if __name__ == "__main__":
    unittest.main()
