"""
EcoGen AI - Rewards Engine

This module calculates sustainability rewards, assigns achievement badges,
tracks streaks, and estimates milestone progress for the rewards dashboard.
"""

from __future__ import annotations

from typing import Any, Dict, List


BADGE_LEVELS = [
    {
        "name": "Green Beginner",
        "min_points": 0,
        "description": "Starting your sustainability journey.",
    },
    {
        "name": "Eco Explorer",
        "min_points": 150,
        "description": "You are building strong eco-friendly habits.",
    },
    {
        "name": "Eco Warrior",
        "min_points": 350,
        "description": "Your actions are creating meaningful impact.",
    },
    {
        "name": "Sustainability Champion",
        "min_points": 650,
        "description": "You are leading the way for lasting change.",
    },
    {
        "name": "Planet Guardian",
        "min_points": 1000,
        "description": "You are protecting the planet through consistent action.",
    },
]


def _validate_number(value: Any, name: str) -> float:
    """Convert a value to float and raise a clear error if invalid."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a numeric value.") from exc


def calculate_points(
    sustainability_score: Any,
    carbon_reduction: Any,
    planner_completion: Any,
    daily_streak: Any,
    weekly_streak: Any,
    monthly_streak: Any,
) -> Dict[str, float]:
    """
    Calculate reward points from sustainability metrics and streak data.

    Returns a dictionary containing the total and per-category point breakdown.
    """
    score = _validate_number(sustainability_score, "sustainability_score")
    reduction = _validate_number(carbon_reduction, "carbon_reduction")
    planner = _validate_number(planner_completion, "planner_completion")
    daily = _validate_number(daily_streak, "daily_streak")
    weekly = _validate_number(weekly_streak, "weekly_streak")
    monthly = _validate_number(monthly_streak, "monthly_streak")

    score_points = min(score * 1.5, 200.0)
    reduction_points = min(reduction * 2.5, 300.0)
    planner_points = min(planner * 1.8, 250.0)
    streak_points = (daily * 4.0) + (weekly * 10.0) + (monthly * 18.0)

    total = round(score_points + reduction_points + planner_points + streak_points, 2)

    return {
        "score_points": round(score_points, 2),
        "reduction_points": round(reduction_points, 2),
        "planner_points": round(planner_points, 2),
        "streak_points": round(streak_points, 2),
        "total_points": total,
    }


def assign_badge(points: Any) -> Dict[str, Any]:
    """
    Assign the correct badge based on the user's point total.
    """
    total_points = _validate_number(points, "points")

    current_badge = BADGE_LEVELS[0]
    for badge in BADGE_LEVELS[1:]:
        if total_points >= badge["min_points"]:
            current_badge = badge

    next_badge = None
    for badge in BADGE_LEVELS:
        if total_points < badge["min_points"]:
            next_badge = badge
            break

    if next_badge is None:
        next_badge = BADGE_LEVELS[-1]
        remaining = 0
        progress_value = 100
    else:
        remaining = max(0, next_badge["min_points"] - int(total_points))
        progress_value = min(
            100,
            round((total_points / next_badge["min_points"]) * 100)
            if next_badge["min_points"]
            else 100,
        )

    return {
        "current_badge": current_badge["name"],
        "current_badge_description": current_badge["description"],
        "next_badge": next_badge["name"],
        "next_badge_target": next_badge["min_points"],
        "remaining_to_next": remaining,
        "progress_to_next": progress_value,
    }


def calculate_streak(
    daily_streak: Any,
    weekly_streak: Any,
    monthly_streak: Any,
) -> Dict[str, Any]:
    """
    Normalize streak values and return a summary for display.
    """
    daily = _validate_number(daily_streak, "daily_streak")
    weekly = _validate_number(weekly_streak, "weekly_streak")
    monthly = _validate_number(monthly_streak, "monthly_streak")

    return {
        "daily_streak": int(daily),
        "weekly_streak": int(weekly),
        "monthly_streak": int(monthly),
        "best_streak": max(int(daily), int(weekly), int(monthly)),
    }


def get_next_milestone(points: Any) -> Dict[str, Any]:
    """
    Calculate the next reward milestone for the user.
    """
    total_points = _validate_number(points, "points")

    for badge in BADGE_LEVELS:
        if total_points < badge["min_points"]:
            return {
                "name": badge["name"],
                "target": badge["min_points"],
                "remaining": max(0, badge["min_points"] - int(total_points)),
            }

    return {
        "name": BADGE_LEVELS[-1]["name"],
        "target": BADGE_LEVELS[-1]["min_points"],
        "remaining": 0,
    }


def get_earned_achievements(points: Any) -> List[Dict[str, Any]]:
    """
    Return a list of badges that the user has unlocked.
    """
    total_points = _validate_number(points, "points")

    earned = []
    for badge in BADGE_LEVELS:
        if total_points >= badge["min_points"]:
            earned.append(
                {
                    "name": badge["name"],
                    "description": badge["description"],
                    "threshold": badge["min_points"],
                }
            )

    return earned

