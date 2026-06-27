"""
Analysis Engine for EcoGen AI

Calculates sustainability metrics from
monthly user assessment data.
"""


class AnalysisEngine:
    """
    Core sustainability analysis engine.
    """

    @staticmethod
    def calculate(
        electricity_kwh: float,
        water_liters: float,
        travel_km: float,
        waste_kg: float,
    ):
        """
        Perform complete sustainability analysis.
        """

        # -----------------------------
        # Carbon Footprint
        # -----------------------------

        carbon = (
            electricity_kwh * 0.45
            + water_liters * 0.001
            + (travel_km * 30 * 0.21)
            + waste_kg * 1.8
        )

        carbon = round(carbon, 2)

        # -----------------------------
        # Sustainability Score
        # -----------------------------

        score = max(
            0,
            min(
                100,
                round(100 - carbon / 10, 1),
            ),
        )

        # -----------------------------
        # EcoDNA
        # -----------------------------

        if score >= 90:
            eco_dna = "Eco Visionary"

        elif score >= 80:
            eco_dna = "Green Innovator"

        elif score >= 70:
            eco_dna = "Eco Guardian"

        elif score >= 60:
            eco_dna = "Eco Learner"

        else:
            eco_dna = "Starter"

        # -----------------------------
        # Journey
        # -----------------------------

        if score >= 90:
            journey = "Sustainability Legend"

        elif score >= 80:
            journey = "Eco Champion"

        elif score >= 70:
            journey = "Green Warrior"

        elif score >= 60:
            journey = "Eco Explorer"

        else:
            journey = "Beginner"

        # -----------------------------
        # Reward Points
        # -----------------------------

        reward_points = int(score * 10)

        # -----------------------------
        # Return Results
        # -----------------------------

        return {
            "carbon_footprint": carbon,
            "sustainability_score": score,
            "eco_dna": eco_dna,
            "journey_level": journey,
            "reward_points": reward_points,
        }