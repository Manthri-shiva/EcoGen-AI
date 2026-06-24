"""
EcoGen AI Mission Engine
Generates sustainability missions based on user profile.
"""


def generate_missions(
    sustainability_score,
    electricity,
    water,
    travel,
    waste,
):
    missions = []

    if electricity > 250:
        missions.append(
            {
                "title": "⚡ Energy Saver Challenge",
                "description": "Reduce electricity usage by 10% this week.",
                "points": 50,
            }
        )

    if travel > 20:
        missions.append(
            {
                "title": "🚲 Green Commute Challenge",
                "description": "Use public transport or cycling for 3 days.",
                "points": 75,
            }
        )

    if water > 5000:
        missions.append(
            {
                "title": "💧 Water Guardian Challenge",
                "description": "Reduce water usage by 15%.",
                "points": 60,
            }
        )

    if waste > 10:
        missions.append(
            {
                "title": "♻ Waste Warrior Challenge",
                "description": "Reduce waste generation by 20%.",
                "points": 80,
            }
        )

    if sustainability_score >= 70:
        missions.append(
            {
                "title": "🌍 Climate Leader Challenge",
                "description": "Mentor others on sustainable practices.",
                "points": 100,
            }
        )

    return missions