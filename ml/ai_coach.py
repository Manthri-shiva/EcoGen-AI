"""
EcoGen AI Coach
"""


def generate_ai_coach_report(
    sustainability_score,
    ecodna_type,
    carbon_footprint,
):

    strengths = []
    weaknesses = []

    if sustainability_score >= 70:
        strengths.append(
            "Strong sustainability habits"
        )
    else:
        weaknesses.append(
            "Sustainability score needs improvement"
        )

    if carbon_footprint > 400:
        weaknesses.append(
            "High carbon footprint"
        )
    else:
        strengths.append(
            "Controlled carbon footprint"
        )

    recommendations = {

        "Energy Saver": "Switch to LED lighting and smart appliances",

        "Water Guardian": "Reduce water consumption by 15%",

        "Eco Traveler": "Use public transport more frequently",

        "Waste Warrior": "Improve recycling and waste segregation",

    }

    best_action = recommendations.get(
        ecodna_type,
        "Continue current sustainability practices",
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "best_action": best_action,
        "estimated_improvement": "+5 Sustainability Points",
    }