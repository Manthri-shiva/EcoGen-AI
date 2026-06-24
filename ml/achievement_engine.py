"""
EcoGen AI Achievement Engine

Unlocks sustainability badges based on
user sustainability score and completed missions.
"""


def get_achievements(
    sustainability_score,
    completed_missions,
):
    achievements = []

    if sustainability_score >= 20:
        achievements.append(
            {
                "badge": "🌱 Green Starter",
                "description": "Started your sustainability journey.",
            }
        )

    if sustainability_score >= 40:
        achievements.append(
            {
                "badge": "⚡ Energy Saver",
                "description": "Maintained good energy efficiency.",
            }
        )

    if sustainability_score >= 50:
        achievements.append(
            {
                "badge": "🚲 Eco Commuter",
                "description": "Reduced transportation emissions.",
            }
        )

    if sustainability_score >= 60:
        achievements.append(
            {
                "badge": "💧 Water Guardian",
                "description": "Practicing responsible water usage.",
            }
        )

    if sustainability_score >= 70:
        achievements.append(
            {
                "badge": "♻ Waste Warrior",
                "description": "Excellent waste reduction habits.",
            }
        )

    if sustainability_score >= 85:
        achievements.append(
            {
                "badge": "🌍 Climate Champion",
                "description": "Outstanding sustainability performance.",
            }
        )

    if completed_missions >= 5:
        achievements.append(
            {
                "badge": "🏅 Mission Master",
                "description": "Completed 5 sustainability missions.",
            }
        )

    if completed_missions >= 10:
        achievements.append(
            {
                "badge": "🏆 Eco Legend",
                "description": "Completed 10 sustainability missions.",
            }
        )

    return achievements