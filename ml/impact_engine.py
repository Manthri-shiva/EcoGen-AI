"""
EcoGen AI Impact Engine
"""


def calculate_impact(
    footprint,
    electricity_reduction,
    travel_reduction,
    water_reduction,
    waste_reduction,
):

    impact = (
        electricity_reduction * 0.4
        + travel_reduction * 0.3
        + water_reduction * 0.1
        + waste_reduction * 0.2
    )

    new_footprint = footprint * (
        1 - impact / 100
    )

    return {
        "current": footprint,
        "future": round(
            new_footprint,
            2,
        ),
        "saved": round(
            footprint - new_footprint,
            2,
        ),
        "impact_score": round(
            impact,
            1,
        ),
    }