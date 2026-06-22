"""
EcoGen AI - Green Product Recommendation Engine

This module ranks eco-friendly products based on sustainability metrics,
cost savings, adoption ease, and environmental impact.
"""

from __future__ import annotations

from typing import Any, Dict, List


PRODUCTS = [
    {
        "name": "LED Bulb Pack",
        "category": "LED Bulbs",
        "estimated_cost": 35,
        "annual_cost_savings": 18,
        "carbon_reduction_potential": 12,
        "impact_score": 82,
        "ease_of_adoption": 9,
    },
    {
        "name": "Smart Plug Kit",
        "category": "Smart Plugs",
        "estimated_cost": 40,
        "annual_cost_savings": 22,
        "carbon_reduction_potential": 10,
        "impact_score": 78,
        "ease_of_adoption": 8,
    },
    {
        "name": "Solar Panel Starter Kit",
        "category": "Solar Panels",
        "estimated_cost": 650,
        "annual_cost_savings": 140,
        "carbon_reduction_potential": 35,
        "impact_score": 95,
        "ease_of_adoption": 4,
    },
    {
        "name": "Low-Flow Showerhead",
        "category": "Water Saving Devices",
        "estimated_cost": 28,
        "annual_cost_savings": 16,
        "carbon_reduction_potential": 8,
        "impact_score": 74,
        "ease_of_adoption": 9,
    },
    {
        "name": "Energy Efficient Refrigerator",
        "category": "Energy Efficient Appliances",
        "estimated_cost": 900,
        "annual_cost_savings": 95,
        "carbon_reduction_potential": 22,
        "impact_score": 89,
        "ease_of_adoption": 5,
    },
    {
        "name": "Compost Bin Kit",
        "category": "Waste Management Products",
        "estimated_cost": 55,
        "annual_cost_savings": 12,
        "carbon_reduction_potential": 9,
        "impact_score": 76,
        "ease_of_adoption": 7,
    },
]


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_roi(estimated_cost: Any, annual_cost_savings: Any) -> float:
    """Calculate return on investment percentage."""
    cost = _safe_float(estimated_cost)
    savings = _safe_float(annual_cost_savings)
    if cost <= 0:
        return 0.0
    return round((savings / cost) * 100, 2)


def estimate_carbon_savings(
    carbon_footprint: Any,
    electricity_usage: Any,
    water_consumption: Any,
    sustainability_score: Any,
) -> Dict[str, float]:
    """
    Estimate carbon savings potential based on user profile metrics.
    """
    footprint = _safe_float(carbon_footprint)
    electricity = _safe_float(electricity_usage)
    water = _safe_float(water_consumption)
    score = _safe_float(sustainability_score)

    # A simple heuristic that scales savings with lifestyle intensity.
    electricity_factor = min(electricity / 250.0, 2.0)
    water_factor = min(water / 5000.0, 2.0)
    score_factor = max(0.5, score / 100.0)

    estimated = {
        "carbon_footprint_adjustment": round(footprint * 0.02 * score_factor, 2),
        "electricity_savings": round(20 * electricity_factor * score_factor, 2),
        "water_savings": round(15 * water_factor * score_factor, 2),
    }
    return estimated


def rank_recommendations(recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank recommendations by impact, savings, and adoption ease."""
    def sort_key(item: Dict[str, Any]) -> tuple:
        return (
            _safe_float(item.get("impact_score")),
            _safe_float(item.get("annual_cost_savings")),
            _safe_float(item.get("ease_of_adoption")),
        )

    return sorted(recommendations, key=sort_key, reverse=True)


def recommend_products(
    carbon_footprint: Any,
    electricity_usage: Any,
    water_consumption: Any,
    sustainability_score: Any,
) -> List[Dict[str, Any]]:
    """
    Recommend eco-friendly products based on the user's sustainability profile.
    """
    savings = estimate_carbon_savings(
        carbon_footprint=carbon_footprint,
        electricity_usage=electricity_usage,
        water_consumption=water_consumption,
        sustainability_score=sustainability_score,
    )

    recommendations = []
    for product in PRODUCTS:
        roi = calculate_roi(
            product["estimated_cost"],
            product["annual_cost_savings"],
        )

        # Adjust recommendation score using user context.
        context_multiplier = 1.0
        if product["category"] == "LED Bulbs":
            context_multiplier = 1.1 if electricity_usage else 1.0
        elif product["category"] == "Solar Panels":
            context_multiplier = 1.2 if electricity_usage > 300 else 1.0
        elif product["category"] == "Water Saving Devices":
            context_multiplier = 1.1 if water_consumption > 5000 else 1.0

        adjusted_impact = product["impact_score"] * context_multiplier
        recommendations.append(
            {
                "name": product["name"],
                "category": product["category"],
                "estimated_cost": product["estimated_cost"],
                "annual_cost_savings": product["annual_cost_savings"],
                "carbon_reduction_potential": product["carbon_reduction_potential"],
                "roi": roi,
                "impact_score": round(adjusted_impact, 2),
                "ease_of_adoption": product["ease_of_adoption"],
                "estimated_carbon_savings": round(
                    savings["carbon_footprint_adjustment"]
                    + (product["carbon_reduction_potential"] * 0.1),
                    2,
                ),
            }
        )

    return rank_recommendations(recommendations)

