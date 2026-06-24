"""
EcoGen AI - What If Scenario Engine
"""

from typing import Dict


def simulate_scenario(
    current_footprint: float,
    sustainability_score: float,
    ac_reduction: float,
    travel_reduction: float,
    water_reduction: float,
    waste_reduction: float,
) -> Dict[str, float]:
    """
    Simulate future footprint after sustainability improvements.
    """

    total_reduction_percent = (
        (ac_reduction * 0.35)
        + (travel_reduction * 0.35)
        + (water_reduction * 0.15)
        + (waste_reduction * 0.15)
    )

    total_reduction_percent = min(total_reduction_percent, 80)

    carbon_saved = (
        current_footprint
        * total_reduction_percent
        / 100
    )

    new_footprint = (
        current_footprint
        - carbon_saved
    )

    future_score = (
        sustainability_score
        + (total_reduction_percent * 0.4)
    )

    future_score = min(future_score, 100)

    return {
        "current_footprint": round(current_footprint, 2),
        "new_footprint": round(new_footprint, 2),
        "carbon_saved": round(carbon_saved, 2),
        "reduction_percentage": round(total_reduction_percent, 2),
        "future_score": round(future_score, 2),
    }