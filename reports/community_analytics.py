"""
EcoGen AI - Community Impact Analytics Engine

This module computes community-level sustainability metrics, aggregates
user statistics, and generates trend data for the analytics dashboard.
"""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_sample_user_data() -> List[Dict[str, Any]]:
    """Create dummy community data when database data is unavailable."""
    return [
        {
            "user_id": 1,
            "name": "Aarav",
            "sustainability_score": 82,
            "carbon_reduction": 38,
            "energy_saved": 120,
            "water_saved": 1500,
            "waste_reduced": 7,
            "cost_savings": 24,
        },
        {
            "user_id": 2,
            "name": "Meera",
            "sustainability_score": 76,
            "carbon_reduction": 31,
            "energy_saved": 95,
            "water_saved": 1100,
            "waste_reduced": 5,
            "cost_savings": 18,
        },
        {
            "user_id": 3,
            "name": "Rohan",
            "sustainability_score": 88,
            "carbon_reduction": 44,
            "energy_saved": 140,
            "water_saved": 1700,
            "waste_reduced": 9,
            "cost_savings": 29,
        },
        {
            "user_id": 4,
            "name": "Sana",
            "sustainability_score": 71,
            "carbon_reduction": 27,
            "energy_saved": 78,
            "water_saved": 980,
            "waste_reduced": 4,
            "cost_savings": 14,
        },
    ]


def calculate_community_impact(users: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """
    Calculate aggregate community-wide sustainability metrics.
    """
    records = users if users is not None else build_sample_user_data()

    total_users = len(records)
    total_carbon_reduction = sum(_safe_float(item.get("carbon_reduction")) for item in records)
    total_energy_saved = sum(_safe_float(item.get("energy_saved")) for item in records)
    total_water_saved = sum(_safe_float(item.get("water_saved")) for item in records)
    total_waste_reduced = sum(_safe_float(item.get("waste_reduced")) for item in records)
    total_cost_savings = sum(_safe_float(item.get("cost_savings")) for item in records)

    avg_score = (
        sum(_safe_float(item.get("sustainability_score")) for item in records) / total_users
        if total_users
        else 0
    )

    return {
        "total_registered_users": total_users,
        "total_carbon_reduction": round(total_carbon_reduction, 2),
        "total_energy_saved": round(total_energy_saved, 2),
        "total_water_saved": round(total_water_saved, 2),
        "total_waste_reduced": round(total_waste_reduced, 2),
        "total_cost_savings": round(total_cost_savings, 2),
        "community_sustainability_score": round(avg_score, 2),
    }


def generate_leaderboard(users: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    """Generate a ranked leaderboard of top contributors."""
    records = users if users is not None else build_sample_user_data()

    sorted_users = sorted(
        records,
        key=lambda item: (
            _safe_float(item.get("sustainability_score")),
            _safe_float(item.get("carbon_reduction")),
        ),
        reverse=True,
    )

    leaderboard = []
    for index, user in enumerate(sorted_users, start=1):
        leaderboard.append(
            {
                "rank": index,
                "name": str(user.get("name", f"User {index}")),
                "sustainability_score": _safe_float(user.get("sustainability_score")),
                "carbon_reduction": _safe_float(user.get("carbon_reduction")),
                "energy_saved": _safe_float(user.get("energy_saved")),
                "water_saved": _safe_float(user.get("water_saved")),
            }
        )

    return leaderboard


def aggregate_user_statistics(users: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """Aggregate per-category impact statistics."""
    records = users if users is not None else build_sample_user_data()

    return {
        "average_score": round(
            sum(_safe_float(item.get("sustainability_score")) for item in records)
            / len(records)
            if records
            else 0,
            2,
        ),
        "average_carbon_reduction": round(
            sum(_safe_float(item.get("carbon_reduction")) for item in records)
            / len(records)
            if records
            else 0,
            2,
        ),
        "average_energy_saved": round(
            sum(_safe_float(item.get("energy_saved")) for item in records)
            / len(records)
            if records
            else 0,
            2,
        ),
    }


def calculate_monthly_trends(users: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """Create monthly trend data for charts."""
    records = users if users is not None else build_sample_user_data()

    # Use simple sample month labels for visualization.
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    monthly_data = {
        "months": months,
        "carbon_reduction": [18, 22, 26, 31, 35, 40],
        "energy_saved": [90, 98, 105, 112, 120, 128],
        "water_saved": [900, 980, 1040, 1120, 1200, 1280],
        "community_score": [68, 70, 73, 75, 78, 81],
    }

    # If real user records are supplied, scale the trends slightly.
    if records:
        scale_factor = sum(_safe_float(item.get("carbon_reduction")) for item in records) / 100
        monthly_data["carbon_reduction"] = [
            round(value * (scale_factor / 2 + 0.6), 1)
            for value in monthly_data["carbon_reduction"]
        ]
        monthly_data["energy_saved"] = [
            round(value * (scale_factor / 10 + 0.8), 1)
            for value in monthly_data["energy_saved"]
        ]
        monthly_data["water_saved"] = [
            round(value * (scale_factor / 18 + 0.7), 1)
            for value in monthly_data["water_saved"]
        ]

    return monthly_data


def create_dataframe(users: List[Dict[str, Any]] | None = None) -> pd.DataFrame:
    """Create a DataFrame for dashboard visualizations."""
    records = users if users is not None else build_sample_user_data()
    return pd.DataFrame(records)
