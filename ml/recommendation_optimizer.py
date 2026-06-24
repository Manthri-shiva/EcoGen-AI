"""
EcoGen AI Recommendation Optimizer

Advanced recommendation ranking engine.
"""

from typing import Dict, List


def get_optimized_recommendations(
    electricity: float,
    water: float,
    travel: float,
    waste: float,
):
    recommendations = []

    if electricity > 250:
        recommendations.append(
            {
                "title": "Switch to LED Lighting",
                "impact_score": 80,
                "roi_score": 90,
                "difficulty": 95,
                "carbon_saving": 15,
            }
        )

    if travel > 20:
        recommendations.append(
            {
                "title": "Use Public Transport",
                "impact_score": 92,
                "roi_score": 75,
                "difficulty": 70,
                "carbon_saving": 30,
            }
        )

    if water > 5000:
        recommendations.append(
            {
                "title": "Install Water Saving Fixtures",
                "impact_score": 70,
                "roi_score": 85,
                "difficulty": 80,
                "carbon_saving": 10,
            }
        )

    if waste > 10:
        recommendations.append(
            {
                "title": "Start Waste Segregation",
                "impact_score": 65,
                "roi_score": 80,
                "difficulty": 95,
                "carbon_saving": 8,
            }
        )

    for rec in recommendations:

        priority_score = (
            rec["impact_score"] * 0.5
            + rec["roi_score"] * 0.3
            + rec["difficulty"] * 0.2
        )

        rec["priority_score"] = round(priority_score, 2)

    recommendations.sort(
        key=lambda x: x["priority_score"],
        reverse=True,
    )

    return recommendations