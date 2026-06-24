"""
EcoGen AI - EcoDNA Engine

Creates a sustainability identity based on user behaviour.
"""


def get_ecodna_type(
    electricity: float,
    water: float,
    travel: float,
    waste: float,
) -> str:
    """
    Determine the user's EcoDNA type.
    """

    if travel < 10:
        return "🚲 Green Commuter"

    if water < 3000:
        return "💧 Water Guardian"

    if electricity < 200:
        return "⚡ Energy Saver"

    if waste < 5:
        return "♻️ Zero Waste Hero"

    return "🌱 Eco Starter"