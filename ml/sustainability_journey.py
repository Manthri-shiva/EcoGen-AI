"""
EcoGen AI Sustainability Journey
"""


def get_journey_stage(score):

    if score < 30:
        return "🌱 Starter"

    elif score < 60:
        return "🚀 Eco Explorer"

    elif score < 80:
        return "🏆 Green Champion"

    else:
        return "🌍 Climate Leader"