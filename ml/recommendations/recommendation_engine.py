"""Rule-based sustainability recommendation engine for EcoGen AI.

This module contains helper functions to generate actionable recommendations
for energy, transport, water and waste, based on numeric usage metrics.
It also builds a personalized plan and estimates reduction potential.
"""

from __future__ import annotations

from typing import Any, Dict, List, Union


Recommendation = Dict[str, Union[str, float]]


def _validate_float(value: Any, name: str) -> float:
    """Validate that the input can be converted to a float."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a numeric value") from exc


def _build_recommendation(category: str, priority: str, action: str, estimated_reduction: str) -> Recommendation:
    """Construct a recommendation dictionary."""
    return {
        "category": category,
        "priority": priority,
        "action": action,
        "estimated_reduction": estimated_reduction,
    }


def generate_energy_recommendations(electricity_bill: Union[float, int]) -> List[Recommendation]:
    """Generate energy recommendations based on electricity bill usage."""
    bill = _validate_float(electricity_bill, "electricity_bill")

    if bill > 3000:
        priority = "HIGH"
        return [
            _build_recommendation(
                "Energy",
                priority,
                "Replace incandescent bulbs with LED lighting.",
                "10-20%",
            ),
            _build_recommendation(
                "Energy",
                priority,
                "Turn off standby devices and unplug idle electronics.",
                "5-10%",
            ),
            _build_recommendation(
                "Energy",
                priority,
                "Use energy-efficient appliances and monitor monthly usage.",
                "8-15%",
            ),
        ]
    if bill >= 1500:
        priority = "MEDIUM"
        return [
            _build_recommendation(
                "Energy",
                priority,
                "Use energy-efficient bulbs and smart power strips.",
                "5-10%",
            ),
            _build_recommendation(
                "Energy",
                priority,
                "Reduce heating and cooling consumption by adjusting thermostat settings.",
                "3-8%",
            ),
        ]

    priority = "LOW"
    return [
        _build_recommendation(
            "Energy",
            priority,
            "Continue monitoring electricity usage and maintain efficient habits.",
            "2-5%",
        )
    ]


def generate_transport_recommendations(daily_travel_km: Union[float, int]) -> List[Recommendation]:
    """Generate transportation recommendations based on daily travel distance."""
    km = _validate_float(daily_travel_km, "daily_travel_km")

    if km > 50:
        priority = "HIGH"
        return [
            _build_recommendation(
                "Transport",
                priority,
                "Use public transport at least twice a week.",
                "8-15%",
            ),
            _build_recommendation(
                "Transport",
                priority,
                "Carpool with colleagues and combine errands.",
                "5-10%",
            ),
            _build_recommendation(
                "Transport",
                priority,
                "Consider switching to an electric vehicle for daily commutes.",
                "10-20%",
            ),
        ]
    if km >= 20:
        priority = "MEDIUM"
        return [
            _build_recommendation(
                "Transport",
                priority,
                "Reduce unnecessary trips and plan routes efficiently.",
                "5-10%",
            ),
            _build_recommendation(
                "Transport",
                priority,
                "Use cycling or walking for short distances.",
                "3-7%",
            ),
        ]

    priority = "LOW"
    return [
        _build_recommendation(
            "Transport",
            priority,
            "Maintain current low travel habits and keep optimizing trip planning.",
            "2-4%",
        )
    ]


def generate_water_recommendations(water_usage: Union[float, int]) -> List[Recommendation]:
    """Generate water usage recommendations based on total usage."""
    water = _validate_float(water_usage, "water_usage")

    if water > 700:
        priority = "HIGH"
        return [
            _build_recommendation(
                "Water",
                priority,
                "Fix leaking taps and pipes immediately.",
                "3-6%",
            ),
            _build_recommendation(
                "Water",
                priority,
                "Install water-saving fixtures such as low-flow showerheads.",
                "4-8%",
            ),
            _build_recommendation(
                "Water",
                priority,
                "Reuse grey water for gardening and cleaning.",
                "2-4%",
            ),
        ]
    if water >= 400:
        priority = "MEDIUM"
        return [
            _build_recommendation(
                "Water",
                priority,
                "Reduce shower duration and use a bucket when washing.",
                "2-5%",
            ),
            _build_recommendation(
                "Water",
                priority,
                "Install faucet aerators and monitor usage regularly.",
                "2-4%",
            ),
        ]

    priority = "LOW"
    return [
        _build_recommendation(
            "Water",
            priority,
            "Keep practicing water-efficient habits and track monthly usage.",
            "1-3%",
        )
    ]


def generate_waste_recommendations(waste_generated: Union[float, int]) -> List[Recommendation]:
    """Generate waste reduction recommendations based on waste generated."""
    waste = _validate_float(waste_generated, "waste_generated")

    if waste > 50:
        priority = "HIGH"
        return [
            _build_recommendation(
                "Waste",
                priority,
                "Compost organic waste and separate recyclables.",
                "5-10%",
            ),
            _build_recommendation(
                "Waste",
                priority,
                "Reduce food waste by planning meals and using leftovers.",
                "4-8%",
            ),
            _build_recommendation(
                "Waste",
                priority,
                "Use reusable containers and avoid single-use plastics.",
                "3-7%",
            ),
        ]
    if waste >= 20:
        priority = "MEDIUM"
        return [
            _build_recommendation(
                "Waste",
                priority,
                "Recycle plastics, paper and glass consistently.",
                "3-6%",
            ),
            _build_recommendation(
                "Waste",
                priority,
                "Reduce packaging waste by choosing bulk or refillable products.",
                "2-5%",
            ),
        ]

    priority = "LOW"
    return [
        _build_recommendation(
            "Waste",
            priority,
            "Continue good waste separation habits and minimize disposable items.",
            "1-3%",
        )
    ]


def calculate_estimated_reduction(recommendations):
    """
    Calculate realistic total reduction potential.

    Instead of summing all recommendation percentages,
    use weighted reduction logic and cap the result.
    """

    if not recommendations:
        return 0.0

    high_count = 0
    medium_count = 0
    low_count = 0

    for recommendation in recommendations:

        priority = recommendation.get("priority", "LOW")

        if priority == "HIGH":
            high_count += 1

        elif priority == "MEDIUM":
            medium_count += 1

        else:
            low_count += 1

    estimated_reduction = (
        high_count * 4
        + medium_count * 2
        + low_count * 1
    )

    # Cap maximum realistic reduction
    estimated_reduction = min(
        estimated_reduction,
        45
    )

    return round(
        estimated_reduction,
        2
    )

def generate_personalized_plan(
    electricity_bill: Union[float, int],
    water_usage: Union[float, int],
    daily_travel_km: Union[float, int],
    waste_generated: Union[float, int],
    sustainability_score: Union[float, int],
    predicted_carbon_footprint: Union[float, int],
) -> Dict[str, Any]:
    """Generate a personalized sustainability recommendation plan."""
    score = _validate_float(sustainability_score, "sustainability_score")
    predicted = _validate_float(predicted_carbon_footprint, "predicted_carbon_footprint")

    energy_recs = generate_energy_recommendations(electricity_bill)
    transport_recs = generate_transport_recommendations(daily_travel_km)
    water_recs = generate_water_recommendations(water_usage)
    waste_recs = generate_waste_recommendations(waste_generated)

    all_recs = energy_recs + transport_recs + water_recs + waste_recs
    total_reduction = calculate_estimated_reduction(all_recs)

    note = (
        "Your sustainability score is strong, but there is still room for improvement. "
        if score >= 70
        else "Your sustainability score indicates there is good potential for impact with these actions. "
    )

    return {
        "sustainability_score": score,
        "predicted_carbon_footprint": predicted,
        "recommendations": {
            "energy": energy_recs,
            "transport": transport_recs,
            "water": water_recs,
            "waste": waste_recs,
        },
        "estimated_total_reduction_percent": total_reduction,
        "summary": note + f"Estimated total reduction potential is {total_reduction}%.",
    }


def _format_plan(plan: Dict[str, Any]) -> str:
    """Format the recommendation plan for display."""
    lines: List[str] = [
        "Personalized Sustainability Recommendation Plan",
        "==============================================",
        f"Sustainability Score: {plan['sustainability_score']}",
        f"Predicted Carbon Footprint: {plan['predicted_carbon_footprint']} kg CO2",
        f"Estimated Total Reduction Potential: {plan['estimated_total_reduction_percent']}%",
        "",
        plan['summary'],
        "",
    ]

    for category, recs in plan['recommendations'].items():
        lines.append(f"{category.capitalize()} Recommendations:")
        for rec in recs:
            lines.append(
                f"  - [{rec['priority']}] {rec['action']} (Estimated reduction: {rec['estimated_reduction']})"
            )
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    sample_plan = generate_personalized_plan(
        electricity_bill=3200,
        water_usage=750,
        daily_travel_km=65,
        waste_generated=55,
        sustainability_score=62,
        predicted_carbon_footprint=2100,
    )

    print(_format_plan(sample_plan))
