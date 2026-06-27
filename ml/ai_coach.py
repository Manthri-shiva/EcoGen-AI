"""
AI Coach Module for EcoGen AI

Generates personalized sustainability recommendations
based on the user's latest assessment.
"""


def generate_ai_coach_report(
    sustainability_score: float,
    eco_dna: str,
    carbon_footprint: float,
    electricity_kwh: float,
    water_liters: float,
    travel_km: float,
    waste_kg: float,
):
    """
    Generate personalized AI coaching recommendations.
    """

    strengths = []
    improvements = []
    recommendations = []

    # Sustainability Score
    if sustainability_score >= 85:
        strengths.append("Excellent sustainability performance.")
    elif sustainability_score >= 70:
        strengths.append("Good sustainability habits.")
    else:
        improvements.append("Improve your overall sustainability score.")

    # Carbon Footprint
    if carbon_footprint <= 250:
        strengths.append("Your carbon footprint is well controlled.")
    else:
        improvements.append("Reduce your carbon footprint.")

    # Electricity
    if electricity_kwh > 300:
        recommendations.append(
            "Reduce electricity consumption by switching to LED lighting and turning off unused appliances."
        )

    # Water
    if water_liters > 6000:
        recommendations.append(
            "Reduce water usage by fixing leaks and using water-efficient fixtures."
        )

    # Travel
    if travel_km > 20:
        recommendations.append(
            "Consider public transport, cycling, or carpooling to reduce travel emissions."
        )

    # Waste
    if waste_kg > 15:
        recommendations.append(
            "Separate recyclable waste and reduce single-use plastics."
        )

    # EcoDNA Advice
    eco_dna_actions = {
        "Energy Saver":
            "Install smart energy monitoring devices.",

        "Water Guardian":
            "Focus on rainwater harvesting and efficient irrigation.",

        "Eco Traveler":
            "Prioritize electric or shared transportation.",

        "Waste Warrior":
            "Improve recycling and composting practices.",

        "Eco Guardian":
            "Maintain your current sustainable lifestyle and inspire others.",
    }

    best_action = eco_dna_actions.get(
        eco_dna,
        "Continue improving your sustainable lifestyle.",
    )

    return {
        "strengths": strengths,
        "improvements": improvements,
        "recommendations": recommendations,
        "best_action": best_action,
        "estimated_improvement": "+5 to +10 Sustainability Points",
    }