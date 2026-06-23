"""EcoGen AI Digital Twin module.

This module synthesizes user profile data, location intelligence,
Sustainability Advisor guidance, and EcoTwin forecasts into a composite
Digital Twin profile.
"""

from __future__ import annotations

from typing import Any, Dict, List

from chatbot.sustainability_advisor import generate_advice_report
from ml.location.location_engine import (
    generate_location_insights,
    generate_location_recommendations,
    get_location_profile,
)
from simulator.carbon_simulator import simulate_future_impact


def create_digital_twin_profile(
    user_profile: Dict[str, Any],
    carbon_footprint: float,
    sustainability_score: float,
    city: str,
) -> Dict[str, Any]:
    """
    Create a Digital Twin profile combining user state, future forecasts,
    sustainability advice, and location intelligence.

    Args:
        user_profile: Dictionary containing user profile fields such as age,
            household size, and consumption patterns.
        carbon_footprint: Current monthly carbon footprint in kg CO2.
        sustainability_score: Current sustainability score on a 0-100 scale.
        city: City name used for location intelligence.

    Returns:
        A dictionary with the Digital Twin overview, future predictions,
        advisor recommendations, and location-specific insights.
    """
    if not isinstance(user_profile, dict):
        raise TypeError("user_profile must be a dictionary.")

    if carbon_footprint < 0:
        raise ValueError("carbon_footprint must be non-negative.")

    if not 0 <= sustainability_score <= 100:
        raise ValueError("sustainability_score must be between 0 and 100.")

    if not isinstance(city, str) or not city.strip():
        raise ValueError("city must be a non-empty string.")

    normalized_city = city.strip().title()

    current_state: Dict[str, Any] = {
        "user_profile": user_profile.copy(),
        "carbon_footprint": round(carbon_footprint, 2),
        "sustainability_score": int(round(sustainability_score)),
        "city": normalized_city,
    }

    future_predictions: Dict[str, Any] = {
        "3_months": simulate_future_impact(
            carbon_footprint,
            sustainability_score,
            3,
        ),
        "6_months": simulate_future_impact(
            carbon_footprint,
            sustainability_score,
            6,
        ),
        "12_months": simulate_future_impact(
            carbon_footprint,
            sustainability_score,
            12,
        ),
    }

    advisor_inputs: Dict[str, Any] = {
        "monthly_electricity_usage": user_profile.get("monthly_electricity_usage", 0),
        "monthly_water_consumption": user_profile.get("monthly_water_consumption", 0),
        "daily_travel_distance": user_profile.get("daily_travel_distance", 0),
        "monthly_waste_generated": user_profile.get("monthly_waste_generated", 0),
        "sustainability_score": sustainability_score,
    }

    sustainability_report = generate_advice_report(advisor_inputs)

    recommendations: List[str] = []
    for rec in sustainability_report.get("recommendations", []):
        recommendation_text = (
            f"{rec.get('priority', 'Medium')} priority: {rec.get('recommendation', '')}"
        ).strip()
        if recommendation_text:
            recommendations.append(recommendation_text)

    location_insights = generate_location_insights(normalized_city)
    location_recommendations = generate_location_recommendations(normalized_city)

    return {
        "current_state": current_state,
        "future_predictions": future_predictions,
        "recommendations": recommendations,
        "location_insights": location_insights + location_recommendations,
    }
