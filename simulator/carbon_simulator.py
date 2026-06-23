"""
EcoGen AI - Carbon Reduction Simulator

This module contains the reusable business logic for estimating monthly carbon
footprint, reduction potential, savings, and sustainability insights.

Dummy assumptions are documented inside the module so the simulator can run
independently before integrating with real database inputs.
"""

from __future__ import annotations

from typing import Dict, List


# ---------------------------------------------------------------------------
# Assumptions used for demo calculations
# ---------------------------------------------------------------------------
# These values are intentionally simple and transparent for UI testing.
# They should be replaced later with calibrated model-based constants.
# ---------------------------------------------------------------------------
ASSUMPTIONS = {
    "ac_co2_per_hour": 0.45,
    "travel_co2_per_km": 0.18,
    "water_co2_per_liter": 0.0008,
    "waste_co2_per_kg": 0.55,
    "electricity_rate": 0.18,
    "fuel_rate": 0.18,
    "water_rate": 0.002,
    "waste_rate": 0.10,
    "days_per_month": 30,
}


def calculate_carbon_footprint(
    ac_usage_hours: float,
    travel_distance_km: float,
    water_consumption_liters: float,
    waste_generated_kg: float,
) -> Dict[str, float]:
    """
    Calculate an approximate monthly carbon footprint from four lifestyle inputs.
    """
    if any(
        value < 0
        for value in (
            ac_usage_hours,
            travel_distance_km,
            water_consumption_liters,
            waste_generated_kg,
        )
    ):
        raise ValueError("All input values must be non-negative.")

    days = ASSUMPTIONS["days_per_month"]

    energy_emission = ac_usage_hours * ASSUMPTIONS["ac_co2_per_hour"] * days
    transport_emission = (
        travel_distance_km * ASSUMPTIONS["travel_co2_per_km"] * days
    )
    water_emission = (
        water_consumption_liters * ASSUMPTIONS["water_co2_per_liter"]
    )
    waste_emission = waste_generated_kg * ASSUMPTIONS["waste_co2_per_kg"]

    total = energy_emission + transport_emission + water_emission + waste_emission

    return {
        "energy": round(energy_emission, 2),
        "transport": round(transport_emission, 2),
        "water": round(water_emission, 2),
        "waste": round(waste_emission, 2),
        "total": round(total, 2),
    }


def calculate_reduction(current_total: float, improved_total: float) -> Dict[str, float]:
    """
    Compute the absolute and percentage reduction between current and improved scenarios.
    """
    if current_total < 0 or improved_total < 0:
        raise ValueError("Footprint values must be non-negative.")

    reduction = max(0.0, current_total - improved_total)
    percentage = 0.0 if current_total == 0 else (reduction / current_total) * 100

    return {
        "reduction": round(reduction, 2),
        "percentage": round(percentage, 2),
    }


def calculate_sustainability_score(carbon_footprint: float) -> int:
    """
    Convert a monthly carbon footprint (kg CO2) into a sustainability score (0-100).

    Rules (piecewise linear):
    - carbon <= 150 kg -> score in [70,100] (lower footprint -> closer to 100)
    - 150 < carbon <= 250 kg -> score in (30,70] (linear between these points)
    - carbon > 250 kg -> score below 30, decreasing with footprint

    Returns an integer in range 0..100.
    """
    if carbon_footprint is None:
        return 0

    try:
        total = float(carbon_footprint)
    except Exception:
        return 0

    # Clamp negative values
    if total <= 0:
        return 100

    if total <= 150:
        # Map 0 -> 100, 150 -> 70
        score = 70 + (150.0 - total) * (30.0 / 150.0)
    elif total <= 250:
        # Map 150 -> 70, 250 -> 30
        score = 70.0 - (total - 150.0) * (40.0 / 100.0)
    else:
        # For values above 250, decrease below 30. Every 10kg reduces score by 1 point.
        score = 30.0 - (total - 250.0) / 10.0

    # Clamp to 0..100 and return integer
    score = max(0.0, min(100.0, score))
    return int(round(score))


def simulate_future_impact(
    current_footprint: float,
    sustainability_score: float,
    months: int,
) -> Dict[str, float]:
    """
    Forecast future carbon and sustainability metrics for a given horizon.

    The function uses the current carbon footprint and the current sustainability
    score to choose a deterministic trend:
    - If sustainable habits are followed, the footprint improves by 2% per month.
    - If no action is taken, the footprint increases by 1% per month.

    Args:
        current_footprint: Current monthly carbon footprint in kg CO2.
        sustainability_score: Current sustainability score on a 0-100 scale.
        months: Forecast horizon in months (e.g. 3, 6, 12).

    Returns:
        A dictionary containing the forecast horizon, projected footprint,
        projected sustainability score, reduction potential, and estimated savings.
    """
    if current_footprint < 0:
        raise ValueError("current_footprint must be non-negative.")
    if months < 0:
        raise ValueError("months must be non-negative.")

    # Determine deterministic behavior based on existing sustainability score.
    sustainable_habits = sustainability_score >= 50.0
    monthly_change = 0.98 if sustainable_habits else 1.01

    projected_footprint = round(current_footprint * (monthly_change ** months), 2)
    projected_score = calculate_sustainability_score(projected_footprint)

    reduction_potential = max(0.0, round(current_footprint - projected_footprint, 2))
    estimated_savings = round(reduction_potential * 0.08, 2)

    return {
        "months": months,
        "projected_footprint": projected_footprint,
        "projected_score": projected_score,
        "reduction_potential": reduction_potential,
        "estimated_savings": estimated_savings,
    }


def calculate_cost_savings(
    current_inputs: Dict[str, float],
    improved_inputs: Dict[str, float],
) -> Dict[str, float]:
    """
    Estimate monthly financial savings from reducing consumption habits.

    The formula uses simple per-unit proxies documented in ASSUMPTIONS.
    """
    current_footprint = calculate_carbon_footprint(**current_inputs)
    improved_footprint = calculate_carbon_footprint(**improved_inputs)

    reduction = calculate_reduction(
        current_footprint["total"],
        improved_footprint["total"],
    )

    days = ASSUMPTIONS["days_per_month"]

    energy_saved_hours = max(
        0.0,
        (current_inputs["ac_usage_hours"] - improved_inputs["ac_usage_hours"]) * days,
    )
    travel_saved_km = max(
        0.0,
        (
            current_inputs["travel_distance_km"]
            - improved_inputs["travel_distance_km"]
        )
        * days,
    )
    water_saved_liters = max(
        0.0,
        current_inputs["water_consumption_liters"]
        - improved_inputs["water_consumption_liters"],
    )
    waste_saved_kg = max(
        0.0,
        current_inputs["waste_generated_kg"] - improved_inputs["waste_generated_kg"],
    )

    energy_savings = energy_saved_hours * ASSUMPTIONS["electricity_rate"]
    transport_savings = travel_saved_km * ASSUMPTIONS["fuel_rate"]
    water_savings = water_saved_liters * ASSUMPTIONS["water_rate"]
    waste_savings = waste_saved_kg * ASSUMPTIONS["waste_rate"]

    total_savings = (
        energy_savings + transport_savings + water_savings + waste_savings
    )

    return {
        "energy_savings": round(energy_savings, 2),
        "transport_savings": round(transport_savings, 2),
        "water_savings": round(water_savings, 2),
        "waste_savings": round(waste_savings, 2),
        "total_savings": round(total_savings, 2),
        "carbon_reduction": reduction["reduction"],
        "reduction_percentage": reduction["percentage"],
    }


def generate_insights(
    current_inputs: Dict[str, float],
    improved_inputs: Dict[str, float],
) -> List[str]:
    """
    Generate practical sustainability recommendations from scenario results.
    """
    current = calculate_carbon_footprint(**current_inputs)
    improved = calculate_carbon_footprint(**improved_inputs)
    reduction = calculate_reduction(current["total"], improved["total"])

    insights: List[str] = []

    if reduction["percentage"] >= 15:
        insights.append(
            "Excellent progress: your improved scenario reduces emissions significantly."
        )
    elif reduction["percentage"] >= 8:
        insights.append(
            "Good improvement: small habit changes can produce meaningful monthly savings."
        )
    else:
        insights.append(
            "You are making progress, but stronger efficiency actions could improve the outcome."
        )

    if improved_inputs["ac_usage_hours"] < current_inputs["ac_usage_hours"]:
        insights.append(
            "Reducing AC usage is one of the fastest ways to lower monthly emissions."
        )

    if improved_inputs["travel_distance_km"] < current_inputs["travel_distance_km"]:
        insights.append(
            "Lower travel distance or shifting to public transport can reduce transport emissions."
        )

    if improved_inputs["water_consumption_liters"] < current_inputs["water_consumption_liters"]:
        insights.append(
            "Reducing water usage supports both savings and improved resource efficiency."
        )

    if improved_inputs["waste_generated_kg"] < current_inputs["waste_generated_kg"]:
        insights.append(
            "Cutting waste generation and improving recycling practices can lower your footprint."
        )

    return insights


if __name__ == "__main__":
    sample_current = {
        "ac_usage_hours": 8,
        "travel_distance_km": 25,
        "water_consumption_liters": 5000,
        "waste_generated_kg": 15,
    }

    sample_improved = {
        "ac_usage_hours": 5,
        "travel_distance_km": 18,
        "water_consumption_liters": 4000,
        "waste_generated_kg": 10,
    }

    current_footprint = calculate_carbon_footprint(**sample_current)
    improved_footprint = calculate_carbon_footprint(**sample_improved)
    reduction = calculate_reduction(
        current_footprint["total"],
        improved_footprint["total"],
    )
    savings = calculate_cost_savings(sample_current, sample_improved)
    insights = generate_insights(sample_current, sample_improved)

    print("Current footprint:", current_footprint)
    print("Improved footprint:", improved_footprint)
    print("Reduction:", reduction)
    print("Savings:", savings)
    print("Insights:", insights)

